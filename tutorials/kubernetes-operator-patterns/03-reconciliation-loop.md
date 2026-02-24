---
layout: default
title: "Kubernetes Operator Patterns - Chapter 3: The Reconciliation Loop"
nav_order: 3
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 3: The Reconciliation Loop - Core Operator Logic

Welcome to **Chapter 3: The Reconciliation Loop - Core Operator Logic**. In this part of **Kubernetes Operator Patterns: Building Production-Grade Controllers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master the reconciliation loop, state management, idempotency, and error handling patterns that form the heart of Kubernetes operators.

## Overview

The reconciliation loop is the core mechanism that makes operators work. This chapter covers implementing robust reconciliation logic, managing state transitions, ensuring idempotency, and handling errors gracefully.

## Reconciliation Fundamentals

### The Control Loop Pattern

```go
// Basic reconciliation loop structure
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    // 1. OBSERVE: Get the current state of the world
    myApp, err := r.getMyApp(ctx, req.NamespacedName)
    if err != nil {
        if apierrors.IsNotFound(err) {
            log.Info("MyApp resource not found. Object must have been deleted.")
            return ctrl.Result{}, nil
        }
        log.Error(err, "Failed to get MyApp")
        return ctrl.Result{}, err
    }

    // 2. ANALYZE: Compare current state with desired state
    currentState, err := r.observeCurrentState(ctx, myApp)
    if err != nil {
        return ctrl.Result{}, err
    }

    desiredState := r.computeDesiredState(myApp)

    // 3. ACT: Make changes to achieve desired state
    if !r.statesEqual(currentState, desiredState) {
        if err := r.actuateDesiredState(ctx, myApp, currentState, desiredState); err != nil {
            return ctrl.Result{}, err
        }
    }

    // 4. REPORT: Update status and emit events
    if err := r.updateStatus(ctx, myApp, currentState); err != nil {
        return ctrl.Result{}, err
    }

    // 5. SCHEDULE: Return when to reconcile again
    return r.scheduleNextReconciliation(myApp, currentState), nil
}
```

### State Observation

```go
// State observation methods
func (r *MyAppReconciler) observeCurrentState(ctx context.Context, myApp *appsv1.MyApp) (*CurrentState, error) {
    state := &CurrentState{}

    // Check if deployment exists
    deployment := &appsv1.Deployment{}
    err := r.Get(ctx, client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, deployment)

    if err != nil && !apierrors.IsNotFound(err) {
        return nil, err
    }

    state.DeploymentExists = err == nil
    if state.DeploymentExists {
        state.DeploymentReplicas = *deployment.Spec.Replicas
        state.DeploymentImage = deployment.Spec.Template.Spec.Containers[0].Image
        state.DeploymentReady = r.isDeploymentReady(deployment)
    }

    // Check if service exists
    service := &corev1.Service{}
    err = r.Get(ctx, client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, service)

    state.ServiceExists = err == nil && !apierrors.IsNotFound(err)

    return state, nil
}

func (r *MyAppReconciler) isDeploymentReady(deployment *appsv1.Deployment) bool {
    // Check if deployment is ready
    for _, condition := range deployment.Status.Conditions {
        if condition.Type == appsv1.DeploymentAvailable {
            return condition.Status == corev1.ConditionTrue
        }
    }
    return false
}

type CurrentState struct {
    DeploymentExists   bool
    DeploymentReplicas int32
    DeploymentImage    string
    DeploymentReady    bool
    ServiceExists      bool
}
```

### Desired State Computation

```go
// Desired state computation
func (r *MyAppReconciler) computeDesiredState(myApp *appsv1.MyApp) *DesiredState {
    return &DesiredState{
        Replicas: myApp.Spec.Replicas,
        Image:    myApp.Spec.Image,
        Labels: map[string]string{
            "app":     myApp.Name,
            "version": "v1",
        },
    }
}

type DesiredState struct {
    Replicas int32
    Image    string
    Labels   map[string]string
}
```

## Idempotency and Safety

### Idempotent Operations

```go
// Idempotent resource creation
func (r *MyAppReconciler) ensureDeployment(ctx context.Context, myApp *appsv1.MyApp, desired *DesiredState) error {
    deployment := &appsv1.Deployment{}
    err := r.Get(ctx, client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, deployment)

    if err != nil && apierrors.IsNotFound(err) {
        // Deployment doesn't exist, create it
        dep := r.deploymentForMyApp(myApp, desired)
        return r.Create(ctx, dep)
    } else if err != nil {
        return err
    }

    // Deployment exists, check if it needs updating
    if r.deploymentNeedsUpdate(deployment, desired) {
        updatedDep := r.updatedDeployment(deployment, myApp, desired)
        return r.Update(ctx, updatedDep)
    }

    // Deployment is already correct
    return nil
}

func (r *MyAppReconciler) deploymentNeedsUpdate(deployment *appsv1.Deployment, desired *DesiredState) bool {
    currentReplicas := deployment.Spec.Replicas
    desiredReplicas := desired.Replicas

    currentImage := deployment.Spec.Template.Spec.Containers[0].Image
    desiredImage := desired.Image

    return *currentReplicas != desiredReplicas || currentImage != desiredImage
}
```

### Safe Updates with Resource Version

```go
// Safe update with resource version check
func (r *MyAppReconciler) safeUpdateDeployment(ctx context.Context, deployment *appsv1.Deployment, myApp *appsv1.MyApp) error {
    // Get the latest version of the deployment
    latestDeployment := &appsv1.Deployment{}
    err := r.Get(ctx, client.ObjectKey{
        Name:      deployment.Name,
        Namespace: deployment.Namespace,
    }, latestDeployment)

    if err != nil {
        return err
    }

    // Update the spec
    latestDeployment.Spec.Replicas = &myApp.Spec.Replicas
    latestDeployment.Spec.Template.Spec.Containers[0].Image = myApp.Spec.Image

    // Update will fail if resource version changed (optimistic concurrency)
    return r.Update(ctx, latestDeployment)
}
```

### Conflict Resolution

```go
// Handle update conflicts
func (r *MyAppReconciler) updateWithConflictResolution(ctx context.Context, obj client.Object) error {
    for retries := 0; retries < 3; retries++ {
        err := r.Update(ctx, obj)
        if err == nil {
            return nil
        }

        if apierrors.IsConflict(err) {
            // Conflict occurred, refresh object and retry
            name := obj.GetName()
            namespace := obj.GetNamespace()

            // Refresh object from API server
            freshObj := obj.DeepCopyObject().(client.Object)
            if err := r.Get(ctx, client.ObjectKey{Name: name, Namespace: namespace}, freshObj); err != nil {
                return err
            }

            // Re-apply changes to fresh object
            r.reapplyChanges(freshObj, obj)

            // Update obj reference for next iteration
            obj = freshObj
            continue
        }

        // Non-conflict error
        return err
    }

    return fmt.Errorf("failed to update after 3 retries")
}

func (r *MyAppReconciler) reapplyChanges(target, source client.Object) {
    // Reapply the desired changes to the fresh object
    // This depends on the specific object type
    switch t := target.(type) {
    case *appsv1.Deployment:
        sourceDep := source.(*appsv1.Deployment)
        t.Spec.Replicas = sourceDep.Spec.Replicas
        t.Spec.Template.Spec.Containers[0].Image = sourceDep.Spec.Template.Spec.Containers[0].Image
    }
}
```

## Error Handling and Recovery

### Comprehensive Error Handling

```go
// Comprehensive error handling in reconciliation
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    logger := log.FromContext(ctx)
    startTime := time.Now()

    defer func() {
        duration := time.Since(startTime)
        logger.Info("Reconciliation completed",
            "duration", duration,
            "resource", req.String())
    }()

    // Get the MyApp resource
    myApp := &appsv1.MyApp{}
    if err := r.Get(ctx, req.NamespacedName, myApp); err != nil {
        if apierrors.IsNotFound(err) {
            logger.Info("MyApp resource not found. Ignoring since object must be deleted")
            return ctrl.Result{}, nil
        }
        logger.Error(err, "Failed to get MyApp resource")
        return ctrl.Result{}, err
    }

    // Add finalizer if not present
    if !controllerutil.ContainsFinalizer(myApp, myAppFinalizer) {
        controllerutil.AddFinalizer(myApp, myAppFinalizer)
        if err := r.Update(ctx, myApp); err != nil {
            logger.Error(err, "Failed to add finalizer")
            return ctrl.Result{}, err
        }
    }

    // Handle deletion
    if !myApp.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, myApp)
    }

    // Main reconciliation logic
    result, err := r.reconcileMyApp(ctx, myApp)
    if err != nil {
        // Update status with error
        myApp.Status.Phase = "Error"
        myApp.Status.Message = err.Error()
        myApp.Status.LastError = &metav1.Time{Time: time.Now()}

        if updateErr := r.Status().Update(ctx, myApp); updateErr != nil {
            logger.Error(updateErr, "Failed to update status with error")
        }

        // Return error and requeue
        return ctrl.Result{RequeueAfter: time.Minute}, err
    }

    // Success - update status
    myApp.Status.Phase = "Running"
    myApp.Status.Message = "Successfully reconciled"
    myApp.Status.ObservedGeneration = myApp.Generation

    if err := r.Status().Update(ctx, myApp); err != nil {
        logger.Error(err, "Failed to update status")
        return ctrl.Result{}, err
    }

    return result, nil
}
```

### Circuit Breaker Pattern

```go
// Circuit breaker for external dependencies
type CircuitBreaker struct {
    failureCount    int
    lastFailureTime time.Time
    state           string // "closed", "open", "half-open"
    threshold       int
    timeout         time.Duration
}

func (cb *CircuitBreaker) Call(operation func() error) error {
    if cb.state == "open" {
        if time.Since(cb.lastFailureTime) > cb.timeout {
            cb.state = "half-open"
        } else {
            return fmt.Errorf("circuit breaker is open")
        }
    }

    err := operation()

    if err != nil {
        cb.failureCount++
        cb.lastFailureTime = time.Now()

        if cb.failureCount >= cb.threshold {
            cb.state = "open"
        }

        return err
    }

    // Success
    cb.failureCount = 0
    cb.state = "closed"
    return nil
}

// Usage in operator
func (r *MyAppReconciler) callExternalAPIWithCircuitBreaker(ctx context.Context, myApp *appsv1.MyApp) error {
    cb := &CircuitBreaker{
        threshold: 3,
        timeout:   time.Minute * 5,
        state:     "closed",
    }

    return cb.Call(func() error {
        // External API call logic
        return r.callExternalAPI(ctx, myApp)
    })
}
```

## Resource Ownership and Garbage Collection

### Owner References and Finalizers

```go
const myAppFinalizer = "myapp.example.com/finalizer"

// Ensure owned resources exist
func (r *MyAppReconciler) ensureOwnedResources(ctx context.Context, myApp *appsv1.MyApp) error {
    // Create deployment if it doesn't exist
    if err := r.ensureDeployment(ctx, myApp); err != nil {
        return err
    }

    // Create service if it doesn't exist
    if err := r.ensureService(ctx, myApp); err != nil {
        return err
    }

    // Create configmap if it doesn't exist
    if err := r.ensureConfigMap(ctx, myApp); err != nil {
        return err
    }

    return nil
}

// Set owner reference on created resources
func (r *MyAppReconciler) deploymentForMyApp(myApp *appsv1.MyApp) *appsv1.Deployment {
    dep := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      myApp.Name,
            Namespace: myApp.Namespace,
            Labels: map[string]string{
                "app": myApp.Name,
            },
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &myApp.Spec.Replicas,
            Selector: &metav1.LabelSelector{
                MatchLabels: map[string]string{
                    "app": myApp.Name,
                },
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: map[string]string{
                        "app": myApp.Name,
                    },
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{{
                        Name:  "myapp",
                        Image: myApp.Spec.Image,
                        Ports: []corev1.ContainerPort{{
                            ContainerPort: 8080,
                            Name:          "http",
                        }},
                    }},
                },
            },
        },
    }

    // Set owner reference for garbage collection
    controllerutil.SetControllerReference(myApp, dep, r.Scheme)
    return dep
}
```

### Finalizer Implementation

```go
// Handle deletion with finalizers
func (r *MyAppReconciler) handleDeletion(ctx context.Context, myApp *appsv1.MyApp) (ctrl.Result, error) {
    logger := log.FromContext(ctx)

    // Check if finalizer is present
    if !controllerutil.ContainsFinalizer(myApp, myAppFinalizer) {
        return ctrl.Result{}, nil
    }

    logger.Info("Handling deletion of MyApp", "name", myApp.Name)

    // Perform cleanup
    if err := r.cleanupOwnedResources(ctx, myApp); err != nil {
        logger.Error(err, "Failed to cleanup owned resources")
        return ctrl.Result{}, err
    }

    // Remove finalizer
    controllerutil.RemoveFinalizer(myApp, myAppFinalizer)
    if err := r.Update(ctx, myApp); err != nil {
        logger.Error(err, "Failed to remove finalizer")
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}

func (r *MyAppReconciler) cleanupOwnedResources(ctx context.Context, myApp *appsv1.MyApp) error {
    logger := log.FromContext(ctx)

    // Delete deployment
    deployment := &appsv1.Deployment{}
    err := r.Get(ctx, client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, deployment)

    if err == nil {
        logger.Info("Deleting deployment", "name", deployment.Name)
        if err := r.Delete(ctx, deployment); err != nil {
            return err
        }
    } else if !apierrors.IsNotFound(err) {
        return err
    }

    // Delete service
    service := &corev1.Service{}
    err = r.Get(ctx, client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, service)

    if err == nil {
        logger.Info("Deleting service", "name", service.Name)
        if err := r.Delete(ctx, service); err != nil {
            return err
        }
    } else if !apierrors.IsNotFound(err) {
        return err
    }

    // Delete configmap
    configMap := &corev1.ConfigMap{}
    err = r.Get(ctx, client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, configMap)

    if err == nil {
        logger.Info("Deleting configmap", "name", configMap.Name)
        if err := r.Delete(ctx, configMap); err != nil {
            return err
        }
    } else if !apierrors.IsNotFound(err) {
        return err
    }

    return nil
}
```

## Event Recording and Monitoring

### Event Recording

```go
// Record events for observability
func (r *MyAppReconciler) recordEvent(ctx context.Context, myApp *appsv1.MyApp, eventType, reason, message string) {
    r.EventRecorder.Event(myApp, eventType, reason, message)
}

// Usage in reconciliation
func (r *MyAppReconciler) reconcileMyApp(ctx context.Context, myApp *appsv1.MyApp) (ctrl.Result, error) {
    logger := log.FromContext(ctx)

    // Attempt reconciliation
    if err := r.ensureOwnedResources(ctx, myApp); err != nil {
        r.recordEvent(ctx, myApp, corev1.EventTypeWarning, "ReconciliationFailed",
            fmt.Sprintf("Failed to reconcile owned resources: %v", err))
        return ctrl.Result{}, err
    }

    // Check if deployment is ready
    currentState, err := r.observeCurrentState(ctx, myApp)
    if err != nil {
        return ctrl.Result{}, err
    }

    if currentState.DeploymentReady {
        r.recordEvent(ctx, myApp, corev1.EventTypeNormal, "ReconciliationSuccessful",
            "Successfully reconciled all owned resources")
    } else {
        r.recordEvent(ctx, myApp, corev1.EventTypeNormal, "ReconciliationInProgress",
            "Owned resources created, waiting for readiness")
        return ctrl.Result{RequeueAfter: time.Minute}, nil
    }

    return ctrl.Result{}, nil
}
```

### Metrics Collection

```go
// Prometheus metrics in reconciliation
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    startTime := time.Now()
    defer func() {
        duration := time.Since(startTime).Seconds()
        r.reconciliationDuration.WithLabelValues(req.Namespace, req.Name).Observe(duration)
        r.reconciliationsTotal.WithLabelValues(req.Namespace).Inc()
    }()

    // Main reconciliation logic
    result, err := r.reconcileMyApp(ctx, req)

    if err != nil {
        r.reconciliationErrors.WithLabelValues(req.Namespace, req.Name).Inc()
    } else {
        r.reconciliationSuccess.WithLabelValues(req.Namespace, req.Name).Inc()
    }

    return result, err
}

// Metrics definitions (in controller setup)
func (r *MyAppReconciler) setupMetrics() {
    r.reconciliationsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "myapp_reconciliations_total",
            Help: "Total number of reconciliations",
        },
        []string{"namespace", "name"},
    )

    r.reconciliationErrors = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "myapp_reconciliation_errors_total",
            Help: "Total number of reconciliation errors",
        },
        []string{"namespace", "name"},
    )

    r.reconciliationDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "myapp_reconciliation_duration_seconds",
            Help:    "Duration of reconciliation in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"namespace", "name"},
    )

    // Register metrics
    prometheus.MustRegister(r.reconciliationsTotal)
    prometheus.MustRegister(r.reconciliationErrors)
    prometheus.MustRegister(r.reconciliationDuration)
}
```

## Advanced Reconciliation Patterns

### Hierarchical Reconciliation

```go
// Hierarchical reconciliation for complex applications
func (r *MyAppReconciler) reconcileHierarchical(ctx context.Context, myApp *appsv1.MyApp) error {
    // Level 1: Infrastructure resources
    if err := r.reconcileInfrastructure(ctx, myApp); err != nil {
        return fmt.Errorf("infrastructure reconciliation failed: %w", err)
    }

    // Level 2: Application resources
    if err := r.reconcileApplication(ctx, myApp); err != nil {
        return fmt.Errorf("application reconciliation failed: %w", err)
    }

    // Level 3: Configuration and policies
    if err := r.reconcileConfiguration(ctx, myApp); err != nil {
        return fmt.Errorf("configuration reconciliation failed: %w", err)
    }

    // Level 4: Monitoring and observability
    if err := r.reconcileMonitoring(ctx, myApp); err != nil {
        return fmt.Errorf("monitoring reconciliation failed: %w", err)
    }

    return nil
}

func (r *MyAppReconciler) reconcileInfrastructure(ctx context.Context, myApp *appsv1.MyApp) error {
    // Create namespace, network policies, etc.
    // This runs first and provides foundation for other resources
    return r.ensureNamespace(ctx, myApp)
}

func (r *MyAppReconciler) reconcileApplication(ctx context.Context, myApp *appsv1.MyApp) error {
    // Create deployments, services, configmaps, etc.
    // Depends on infrastructure being ready
    return r.ensureApplicationResources(ctx, myApp)
}
```

### Progressive Reconciliation

```go
// Progressive reconciliation with phases
type ReconciliationPhase string

const (
    PhaseInfrastructure ReconciliationPhase = "infrastructure"
    PhaseApplication    ReconciliationPhase = "application"
    PhaseConfiguration  ReconciliationPhase = "configuration"
    PhaseMonitoring     ReconciliationPhase = "monitoring"
    PhaseComplete       ReconciliationPhase = "complete"
)

func (r *MyAppReconciler) reconcileProgressive(ctx context.Context, myApp *appsv1.MyApp) (ctrl.Result, error) {
    currentPhase := r.getCurrentPhase(myApp)

    switch currentPhase {
    case PhaseInfrastructure:
        if err := r.reconcileInfrastructure(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        r.setPhase(myApp, PhaseApplication)
        return ctrl.Result{Requeue: true}, nil

    case PhaseApplication:
        if err := r.reconcileApplication(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        r.setPhase(myApp, PhaseConfiguration)
        return ctrl.Result{Requeue: true}, nil

    case PhaseConfiguration:
        if err := r.reconcileConfiguration(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        r.setPhase(myApp, PhaseMonitoring)
        return ctrl.Result{Requeue: true}, nil

    case PhaseMonitoring:
        if err := r.reconcileMonitoring(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        r.setPhase(myApp, PhaseComplete)
        return ctrl.Result{}, nil

    case PhaseComplete:
        // All phases complete, check for drift
        return r.reconcileDrift(ctx, myApp)

    default:
        return ctrl.Result{}, fmt.Errorf("unknown reconciliation phase: %s", currentPhase)
    }
}
```

## Summary

In this chapter, we've covered:

- **Reconciliation Fundamentals**: The observe-analyze-act-report cycle
- **Idempotency**: Ensuring operations are safe to repeat
- **Error Handling**: Comprehensive error handling and recovery
- **Resource Ownership**: Owner references and finalizers for garbage collection
- **Event Recording**: Observability through Kubernetes events
- **Advanced Patterns**: Hierarchical and progressive reconciliation

## Key Takeaways

1. **Observe-Analyze-Act-Report**: The four phases of reconciliation
2. **Idempotency is Critical**: Operations must be safe to repeat
3. **Error Handling**: Graceful failure handling with appropriate retries
4. **Resource Ownership**: Proper cleanup through owner references and finalizers
5. **Progressive Reconciliation**: Breaking complex operations into phases
6. **Observability**: Events, metrics, and logging for monitoring

Next, we'll explore **managing owned resources** - creating and managing Pods, Services, and other Kubernetes objects that operators control.

---

**Ready for the next chapter?** [Chapter 4: Managing Owned Resources](04-owned-resources.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `myApp`, `ctrl`, `Result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: The Reconciliation Loop - Core Operator Logic` as an operating subsystem inside **Kubernetes Operator Patterns: Building Production-Grade Controllers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Name`, `appsv1`, `func` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: The Reconciliation Loop - Core Operator Logic` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `myApp`.
2. **Input normalization**: shape incoming data so `ctrl` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `myApp` and `ctrl` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Custom Resource Definitions - Designing Robust APIs](02-custom-resources.md)
- [Next Chapter: Chapter 4: Managing Owned Resources - Creating and Managing Kubernetes Objects](04-owned-resources.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
