---
layout: default
title: "Kubernetes Operator Patterns - Chapter 5: Status and Conditions"
nav_order: 5
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 5: Status and Conditions - Reporting Resource Status and Implementing Condition Patterns

Welcome to **Chapter 5: Status and Conditions - Reporting Resource Status and Implementing Condition Patterns**. In this part of **Kubernetes Operator Patterns: Building Production-Grade Controllers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master status reporting, condition patterns, and observability best practices for Kubernetes operators.

## Overview

Status reporting is crucial for operator observability. This chapter covers implementing comprehensive status reporting, condition patterns, and ensuring operators provide clear feedback about managed resources.

## Status Subresource

### Status Structure

```go
// Status subresource definition
type DatabaseStatus struct {
    // Phase represents the current phase of the database
    Phase DatabasePhase `json:"phase,omitempty"`

    // Message provides additional information about the current phase
    Message string `json:"message,omitempty"`

    // ObservedGeneration is the generation observed by the operator
    ObservedGeneration int64 `json:"observedGeneration,omitempty"`

    // Conditions represent the latest available observations
    Conditions []metav1.Condition `json:"conditions,omitempty"`

    // ConnectionString for connecting to the database
    ConnectionString string `json:"connectionString,omitempty"`

    // Endpoint is the database service endpoint
    Endpoint string `json:"endpoint,omitempty"`

    // Port is the database service port
    Port int32 `json:"port,omitempty"`

    // Ready indicates if the database is ready to accept connections
    Ready bool `json:"ready,omitempty"`

    // LastBackupTime indicates the last successful backup
    LastBackupTime *metav1.Time `json:"lastBackupTime,omitempty"`
}

// Status phase enum
type DatabasePhase string

const (
    DatabasePhasePending     DatabasePhase = "Pending"
    DatabasePhaseCreating    DatabasePhase = "Creating"
    DatabasePhaseRunning     DatabasePhase = "Running"
    DatabasePhaseFailed      DatabasePhase = "Failed"
    DatabasePhaseTerminating DatabasePhase = "Terminating"
)

// Status update methods
func (r *DatabaseReconciler) updateStatus(ctx context.Context, database *postgresqlv1.Database, phase DatabasePhase, message string) error {
    database.Status.Phase = phase
    database.Status.Message = message
    database.Status.ObservedGeneration = database.Generation

    return r.Status().Update(ctx, database)
}

func (r *DatabaseReconciler) updateStatusWithConditions(ctx context.Context, database *postgresqlv1.Database, conditions []metav1.Condition) error {
    database.Status.Conditions = conditions
    database.Status.ObservedGeneration = database.Generation

    return r.Status().Update(ctx, database)
}
```

### Status Updates in Reconciliation

```go
func (r *DatabaseReconciler) reconcileDatabase(ctx context.Context, database *postgresqlv1.Database) error {
    logger := log.FromContext(ctx)

    // Phase 1: Validation
    if err := r.validateDatabaseSpec(database); err != nil {
        r.updateStatus(ctx, database, DatabasePhaseFailed, fmt.Sprintf("Validation failed: %v", err))
        return err
    }

    // Phase 2: PVC creation
    if err := r.ensurePVC(ctx, database); err != nil {
        r.updateStatus(ctx, database, DatabasePhaseFailed, fmt.Sprintf("PVC creation failed: %v", err))
        return err
    }

    // Phase 3: Deployment creation
    if err := r.ensureDeployment(ctx, database); err != nil {
        r.updateStatus(ctx, database, DatabasePhaseFailed, fmt.Sprintf("Deployment creation failed: %v", err))
        return err
    }

    // Phase 4: Service creation
    if err := r.ensureService(ctx, database); err != nil {
        r.updateStatus(ctx, database, DatabasePhaseFailed, fmt.Sprintf("Service creation failed: %v", err))
        return err
    }

    // Phase 5: Wait for readiness
    if err := r.waitForDatabaseReady(ctx, database); err != nil {
        r.updateStatus(ctx, database, DatabasePhaseCreating, "Waiting for database to become ready")
        return err
    }

    // Phase 6: Update connection info
    if err := r.updateConnectionInfo(ctx, database); err != nil {
        r.updateStatus(ctx, database, DatabasePhaseFailed, fmt.Sprintf("Connection info update failed: %v", err))
        return err
    }

    // Success
    database.Status.Ready = true
    r.updateStatus(ctx, database, DatabasePhaseRunning, "Database is running and ready")

    return nil
}

func (r *DatabaseReconciler) waitForDatabaseReady(ctx context.Context, database *postgresqlv1.Database) error {
    // Check deployment readiness
    deployment := &appsv1.Deployment{}
    if err := r.Get(ctx, client.ObjectKey{
        Name:      database.Name,
        Namespace: database.Namespace,
    }, deployment); err != nil {
        return err
    }

    if deployment.Status.ReadyReplicas != *deployment.Spec.Replicas {
        return fmt.Errorf("deployment not ready: %d/%d replicas",
            deployment.Status.ReadyReplicas, *deployment.Spec.Replicas)
    }

    // Check if database is accepting connections
    return r.checkDatabaseConnectivity(ctx, database)
}

func (r *DatabaseReconciler) updateConnectionInfo(ctx context.Context, database *postgresqlv1.Database) error {
    service := &corev1.Service{}
    if err := r.Get(ctx, client.ObjectKey{
        Name:      database.Name,
        Namespace: database.Namespace,
    }, service); err != nil {
        return err
    }

    database.Status.Endpoint = fmt.Sprintf("%s.%s.svc.cluster.local", service.Name, service.Namespace)
    database.Status.Port = 5432 // PostgreSQL default port

    // Generate connection string
    database.Status.ConnectionString = fmt.Sprintf(
        "postgresql://%s:%s@%s:%d/%s",
        database.Spec.Username,
        "****", // Don't expose password in status
        database.Status.Endpoint,
        database.Status.Port,
        database.Name,
    )

    return nil
}
```

## Condition Patterns

### Condition Structure

```go
// Condition management
type ConditionManager struct {
    conditions []metav1.Condition
}

func (cm *ConditionManager) SetCondition(conditionType string, status metav1.ConditionStatus, reason, message string) {
    now := metav1.Now()

    // Find existing condition
    for i, condition := range cm.conditions {
        if condition.Type == conditionType {
            // Update existing condition
            if condition.Status != status || condition.Reason != reason || condition.Message != message {
                cm.conditions[i].LastTransitionTime = now
            }
            cm.conditions[i].Status = status
            cm.conditions[i].Reason = reason
            cm.conditions[i].Message = message
            cm.conditions[i].ObservedGeneration = 1 // Set appropriate generation
            return
        }
    }

    // Add new condition
    cm.conditions = append(cm.conditions, metav1.Condition{
        Type:               conditionType,
        Status:             status,
        Reason:             reason,
        Message:            message,
        LastTransitionTime: now,
        ObservedGeneration: 1,
    })
}

func (cm *ConditionManager) GetConditions() []metav1.Condition {
    return cm.conditions
}

func (cm *ConditionManager) IsConditionTrue(conditionType string) bool {
    for _, condition := range cm.conditions {
        if condition.Type == conditionType {
            return condition.Status == metav1.ConditionTrue
        }
    }
    return false
}

// Condition type constants
const (
    ConditionTypeReady             = "Ready"
    ConditionTypeAvailable         = "Available"
    ConditionTypeProgressing       = "Progressing"
    ConditionTypeDegraded          = "Degraded"
    ConditionTypeUpgradeable       = "Upgradeable"
    ConditionTypeDatabaseReady     = "DatabaseReady"
    ConditionTypeBackupReady       = "BackupReady"
    ConditionTypeReplicationReady  = "ReplicationReady"
)
```

### Condition Updates in Reconciliation

```go
func (r *DatabaseReconciler) reconcileWithConditions(ctx context.Context, database *postgresqlv1.Database) error {
    logger := log.FromContext(ctx)

    // Initialize condition manager
    cm := &ConditionManager{
        conditions: database.Status.Conditions,
    }

    // Set progressing condition
    cm.SetCondition(
        ConditionTypeProgressing,
        metav1.ConditionTrue,
        "Reconciling",
        "Starting database reconciliation",
    )

    // Update status with conditions
    database.Status.Conditions = cm.GetConditions()
    if err := r.Status().Update(ctx, database); err != nil {
        return err
    }

    // Phase 1: PVC reconciliation
    if err := r.ensurePVC(ctx, database); err != nil {
        cm.SetCondition(
            ConditionTypeReady,
            metav1.ConditionFalse,
            "PVCFailed",
            fmt.Sprintf("PVC creation failed: %v", err),
        )
        database.Status.Conditions = cm.GetConditions()
        r.Status().Update(ctx, database)
        return err
    }

    cm.SetCondition(
        ConditionTypeProgressing,
        metav1.ConditionTrue,
        "PVCReady",
        "Persistent volume claim is ready",
    )

    // Phase 2: Deployment reconciliation
    if err := r.ensureDeployment(ctx, database); err != nil {
        cm.SetCondition(
            ConditionTypeReady,
            metav1.ConditionFalse,
            "DeploymentFailed",
            fmt.Sprintf("Deployment creation failed: %v", err),
        )
        database.Status.Conditions = cm.GetConditions()
        r.Status().Update(ctx, database)
        return err
    }

    // Phase 3: Wait for deployment readiness
    if err := r.waitForDeploymentReady(ctx, database); err != nil {
        cm.SetCondition(
            ConditionTypeReady,
            metav1.ConditionFalse,
            "DeploymentNotReady",
            "Waiting for deployment to become ready",
        )
        database.Status.Conditions = cm.GetConditions()
        r.Status().Update(ctx, database)
        return err
    }

    cm.SetCondition(
        ConditionTypeProgressing,
        metav1.ConditionTrue,
        "DeploymentReady",
        "Deployment is ready",
    )

    // Phase 4: Database initialization
    if err := r.initializeDatabase(ctx, database); err != nil {
        cm.SetCondition(
            ConditionTypeDatabaseReady,
            metav1.ConditionFalse,
            "InitializationFailed",
            fmt.Sprintf("Database initialization failed: %v", err),
        )
        database.Status.Conditions = cm.GetConditions()
        r.Status().Update(ctx, database)
        return err
    }

    // Phase 5: Backup setup
    if database.Spec.Backup != nil {
        if err := r.setupBackup(ctx, database); err != nil {
            cm.SetCondition(
                ConditionTypeBackupReady,
                metav1.ConditionFalse,
                "BackupSetupFailed",
                fmt.Sprintf("Backup setup failed: %v", err),
            )
        } else {
            cm.SetCondition(
                ConditionTypeBackupReady,
                metav1.ConditionTrue,
                "BackupReady",
                "Backup system is configured",
            )
        }
    }

    // Final status update
    cm.SetCondition(
        ConditionTypeReady,
        metav1.ConditionTrue,
        "ReconciliationComplete",
        "Database is running and ready",
    )

    cm.SetCondition(
        ConditionTypeProgressing,
        metav1.ConditionFalse,
        "ReconciliationComplete",
        "Reconciliation completed successfully",
    )

    database.Status.Conditions = cm.GetConditions()
    database.Status.Ready = true

    return r.Status().Update(ctx, database)
}
```

## Advanced Status Patterns

### Hierarchical Status

```go
// Hierarchical status for complex applications
type ApplicationStatus struct {
    Phase      ApplicationPhase     `json:"phase,omitempty"`
    Message    string              `json:"message,omitempty"`
    Components ComponentStatuses   `json:"components,omitempty"`
    Conditions []metav1.Condition  `json:"conditions,omitempty"`
}

type ComponentStatuses struct {
    API       ComponentStatus `json:"api,omitempty"`
    Database  ComponentStatus `json:"database,omitempty"`
    Cache     ComponentStatus `json:"cache,omitempty"`
    Queue     ComponentStatus `json:"queue,omitempty"`
}

type ComponentStatus struct {
    Phase      ComponentPhase      `json:"phase,omitempty"`
    Message    string             `json:"message,omitempty"`
    Ready      bool               `json:"ready,omitempty"`
    LastUpdate metav1.Time        `json:"lastUpdate,omitempty"`
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// Hierarchical status updates
func (r *ApplicationReconciler) updateComponentStatus(ctx context.Context, app *examplev1.Application, component string, status ComponentStatus) error {
    if app.Status.Components == nil {
        app.Status.Components = ComponentStatuses{}
    }

    // Update specific component status
    switch component {
    case "api":
        app.Status.Components.API = status
    case "database":
        app.Status.Components.Database = status
    case "cache":
        app.Status.Components.Cache = status
    case "queue":
        app.Status.Components.Queue = status
    }

    // Update overall application status based on components
    r.updateOverallStatus(app)

    return r.Status().Update(ctx, app)
}

func (r *ApplicationReconciler) updateOverallStatus(app *examplev1.Application) {
    components := []ComponentStatus{
        app.Status.Components.API,
        app.Status.Components.Database,
        app.Status.Components.Cache,
        app.Status.Components.Queue,
    }

    // Check if all components are ready
    allReady := true
    messages := []string{}

    for _, component := range components {
        if !component.Ready {
            allReady = false
            if component.Message != "" {
                messages = append(messages, component.Message)
            }
        }
    }

    if allReady {
        app.Status.Phase = ApplicationPhaseRunning
        app.Status.Message = "All components are running"
    } else {
        app.Status.Phase = ApplicationPhaseDegraded
        app.Status.Message = fmt.Sprintf("Components not ready: %s", strings.Join(messages, "; "))
    }
}
```

### Status Aggregation

```go
// Status aggregation from multiple sources
type StatusAggregator struct {
    ownedResources []client.Object
}

func (sa *StatusAggregator) aggregateStatus(ctx context.Context, c client.Client) (*AggregatedStatus, error) {
    status := &AggregatedStatus{}

    for _, resource := range sa.ownedResources {
        // Get resource status
        if err := c.Get(ctx, client.ObjectKeyFromObject(resource), resource); err != nil {
            if !apierrors.IsNotFound(err) {
                return nil, err
            }
            continue
        }

        // Aggregate based on resource type
        switch obj := resource.(type) {
        case *appsv1.Deployment:
            status.Deployments = append(status.Deployments, sa.getDeploymentStatus(obj))
        case *corev1.Service:
            status.Services = append(status.Services, sa.getServiceStatus(obj))
        case *corev1.PersistentVolumeClaim:
            status.PVCs = append(status.PVCs, sa.getPVCStatus(obj))
        }
    }

    // Calculate overall status
    status.Overall = sa.calculateOverallStatus(status)

    return status, nil
}

type AggregatedStatus struct {
    Overall     OverallStatus     `json:"overall"`
    Deployments []ResourceStatus  `json:"deployments,omitempty"`
    Services    []ResourceStatus  `json:"services,omitempty"`
    PVCs        []ResourceStatus  `json:"pvcs,omitempty"`
}

type ResourceStatus struct {
    Name    string `json:"name"`
    Status  string `json:"status"`
    Message string `json:"message,omitempty"`
    Ready   bool   `json:"ready"`
}

type OverallStatus string

const (
    OverallStatusHealthy   OverallStatus = "Healthy"
    OverallStatusDegraded  OverallStatus = "Degraded"
    OverallStatusUnhealthy OverallStatus = "Unhealthy"
)

func (sa *StatusAggregator) calculateOverallStatus(status *AggregatedStatus) OverallStatus {
    allResources := append(append(status.Deployments, status.Services...), status.PVCs...)

    unhealthyCount := 0
    for _, resource := range allResources {
        if !resource.Ready {
            unhealthyCount++
        }
    }

    if unhealthyCount == 0 {
        return OverallStatusHealthy
    } else if unhealthyCount < len(allResources)/2 {
        return OverallStatusDegraded
    } else {
        return OverallStatusUnhealthy
    }
}
```

## Status Validation Webhooks

### Status Validation

```go
// Status validation webhook
type StatusValidator struct{}

func (v *StatusValidator) ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) error {
    oldApp := oldObj.(*examplev1.Application)
    newApp := newObj.(*examplev1.Application)

    // Validate status transitions
    if err := v.validateStatusTransition(oldApp.Status.Phase, newApp.Status.Phase); err != nil {
        return err
    }

    // Validate condition updates
    if err := v.validateConditions(newApp.Status.Conditions); err != nil {
        return err
    }

    return nil
}

func (v *StatusValidator) validateStatusTransition(oldPhase, newPhase ApplicationPhase) error {
    // Define valid transitions
    validTransitions := map[ApplicationPhase][]ApplicationPhase{
        ApplicationPhasePending:    {ApplicationPhaseCreating, ApplicationPhaseFailed},
        ApplicationPhaseCreating:   {ApplicationPhaseRunning, ApplicationPhaseFailed},
        ApplicationPhaseRunning:    {ApplicationPhaseUpdating, ApplicationPhaseFailed, ApplicationPhaseTerminating},
        ApplicationPhaseUpdating:   {ApplicationPhaseRunning, ApplicationPhaseFailed},
        ApplicationPhaseFailed:     {ApplicationPhaseCreating, ApplicationPhaseTerminating},
        ApplicationPhaseTerminating: {}, // Terminal state
    }

    if allowed, exists := validTransitions[oldPhase]; exists {
        for _, phase := range allowed {
            if phase == newPhase {
                return nil
            }
        }
    }

    return fmt.Errorf("invalid status transition from %s to %s", oldPhase, newPhase)
}

func (v *StatusValidator) validateConditions(conditions []metav1.Condition) error {
    // Validate condition structure
    conditionTypes := make(map[string]bool)

    for _, condition := range conditions {
        // Check for duplicate condition types
        if conditionTypes[condition.Type] {
            return fmt.Errorf("duplicate condition type: %s", condition.Type)
        }
        conditionTypes[condition.Type] = true

        // Validate required fields
        if condition.Type == "" {
            return fmt.Errorf("condition type cannot be empty")
        }

        if condition.Status != metav1.ConditionTrue &&
           condition.Status != metav1.ConditionFalse &&
           condition.Status != metav1.ConditionUnknown {
            return fmt.Errorf("invalid condition status: %s", condition.Status)
        }

        // Validate timestamps
        if condition.LastTransitionTime.IsZero() {
            return fmt.Errorf("condition LastTransitionTime cannot be zero")
        }
    }

    return nil
}
```

## kubectl Integration

### Custom Columns and Printing

```yaml
# CRD with kubectl integration
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.postgresql.example.com
spec:
  group: postgresql.example.com
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        # Schema definition
    additionalPrinterColumns:
    - name: Phase
      type: string
      jsonPath: .status.phase
      description: Current phase of the database
    - name: Age
      type: date
      jsonPath: .metadata.creationTimestamp
    - name: Ready
      type: string
      jsonPath: ".status.conditions[?(@.type=='Ready')].status"
      description: Ready condition status
    - name: Endpoint
      type: string
      jsonPath: .status.endpoint
      priority: 1  # Hidden by default, shown with -o wide
    - name: Version
      type: string
      jsonPath: .spec.version
      priority: 1
```

### kubectl Commands

```bash
# List databases with custom columns
kubectl get databases

# Output:
# NAME         PHASE      AGE    READY   ENDPOINT               VERSION
# my-postgres  Running    5m     True    my-postgres:5432       14
# my-mysql     Creating   2m     False   my-mysql:3306          8.0

# Get detailed status
kubectl describe database my-postgres

# Output includes:
# Status:
#   Phase:     Running
#   Ready:     true
#   Endpoint:  my-postgres.default.svc.cluster.local:5432
#   Conditions:
#     Type              Status  LastTransitionTime               Reason                  Message
#     ----              ------  ------------------               ------                  -------
#     Ready             True    2024-01-01T10:00:00Z             ReconciliationComplete  Database is running and ready
#     DatabaseReady     True    2024-01-01T09:58:00Z             InitializationComplete  Database initialized successfully
#     BackupReady       True    2024-01-01T09:59:00Z             BackupConfigured       Backup system configured

# Get status as JSON
kubectl get database my-postgres -o jsonpath='{.status}'

# Watch status changes
kubectl get database my-postgres --watch
```

## Event Recording

### Structured Event Recording

```go
// Event recording for status changes
func (r *DatabaseReconciler) recordStatusEvent(ctx context.Context, database *postgresqlv1.Database, eventType, reason, message string) {
    r.EventRecorder.Event(database, eventType, reason, message)
}

func (r *DatabaseReconciler) recordPhaseTransition(ctx context.Context, database *postgresqlv1.Database, oldPhase, newPhase DatabasePhase) {
    if oldPhase != newPhase {
        r.recordStatusEvent(
            ctx,
            database,
            corev1.EventTypeNormal,
            "PhaseTransition",
            fmt.Sprintf("Phase changed from %s to %s", oldPhase, newPhase),
        )
    }
}

func (r *DatabaseReconciler) recordConditionChange(ctx context.Context, database *postgresqlv1.Database, conditionType string, oldStatus, newStatus metav1.ConditionStatus) {
    if oldStatus != newStatus {
        eventType := corev1.EventTypeNormal
        if newStatus == metav1.ConditionFalse {
            eventType = corev1.EventTypeWarning
        }

        r.recordStatusEvent(
            ctx,
            database,
            eventType,
            "ConditionChanged",
            fmt.Sprintf("Condition %s changed from %s to %s", conditionType, oldStatus, newStatus),
        )
    }
}

// Enhanced status update with event recording
func (r *DatabaseReconciler) updateStatusWithEvents(ctx context.Context, database *postgresqlv1.Database, newPhase DatabasePhase, message string) error {
    oldPhase := database.Status.Phase

    // Update status
    database.Status.Phase = newPhase
    database.Status.Message = message
    database.Status.ObservedGeneration = database.Generation

    // Record phase transition
    r.recordPhaseTransition(ctx, database, oldPhase, newPhase)

    return r.Status().Update(ctx, database)
}
```

## Summary

In this chapter, we've covered:

- **Status Subresource**: Implementing comprehensive status reporting
- **Condition Patterns**: Using Kubernetes conditions for detailed status
- **Status Updates**: Safe status updates during reconciliation
- **Hierarchical Status**: Complex status structures for multi-component applications
- **kubectl Integration**: Custom columns and printing for better UX
- **Event Recording**: Structured event recording for observability

## Key Takeaways

1. **Status Subresource**: Use status subresource for reliable status reporting
2. **Condition Patterns**: Implement conditions for detailed, structured status
3. **Event Recording**: Record events for important status changes and transitions
4. **kubectl Integration**: Provide good CLI experience with custom columns
5. **Validation**: Use webhooks to validate status transitions and conditions
6. **Observability**: Status provides crucial observability into operator behavior

Next, we'll explore **testing operators** - unit tests, integration tests, and envtest framework for comprehensive operator testing.

---

**Ready for the next chapter?** [Chapter 6: Testing Operators](06-testing.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `database`, `Status`, `status` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Status and Conditions - Reporting Resource Status and Implementing Condition Patterns` as an operating subsystem inside **Kubernetes Operator Patterns: Building Production-Grade Controllers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `condition`, `json`, `metav1` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Status and Conditions - Reporting Resource Status and Implementing Condition Patterns` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `database`.
2. **Input normalization**: shape incoming data so `Status` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `status`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `database` and `Status` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Managing Owned Resources - Creating and Managing Kubernetes Objects](04-owned-resources.md)
- [Next Chapter: Chapter 6: Testing Operators - Unit Tests, Integration Tests, and envtest Framework](06-testing.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
