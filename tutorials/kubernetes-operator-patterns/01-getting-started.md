---
layout: default
title: "Kubernetes Operator Patterns - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 1: Getting Started with Kubernetes Operators

> Install Operator SDK, create your first operator project, and understand the core concepts and architecture.

## Overview

This chapter introduces Kubernetes Operators and guides you through setting up the development environment. You'll create your first operator and understand the fundamental concepts that make operators work.

## Understanding Operators

### What is a Kubernetes Operator?

A **Kubernetes Operator** is a software extension that uses custom resources to manage applications and their components. Operators follow Kubernetes principles:

- **Declarative**: Define desired state, operator makes it happen
- **Idempotent**: Same result regardless of how many times run
- **Self-healing**: Automatically recover from failures
- **Observable**: Provide metrics and status information

### Operator vs. Traditional Controllers

```yaml
# Traditional approach: Manual management
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: my-app:v1.0.0
---
# Manual scaling when needed
kubectl scale deployment my-app --replicas=5
```

```yaml
# Operator approach: Declarative management
apiVersion: example.com/v1
kind: MyApp
metadata:
  name: my-app-instance
spec:
  version: v1.0.0
  replicas: 3
  # Operator handles scaling, upgrades, backups, etc.
```

## Development Environment Setup

### Prerequisites

```bash
# Required tools
- Go 1.19+ (https://golang.org/dl/)
- Docker (https://docs.docker.com/get-docker/)
- kubectl (https://kubernetes.io/docs/tasks/tools/)
- Kubernetes cluster (kind, minikube, or cloud cluster)

# Recommended
- kustomize (https://kubectl.docs.kubernetes.io/installation/kustomize/)
- krew (https://krew.sigs.k8s.io/docs/user-guide/setup/install/)
```

### Installing Operator SDK

```bash
# Download Operator SDK
curl -L https://github.com/operator-framework/operator-sdk/releases/download/v1.32.0/operator-sdk_linux_amd64 -o operator-sdk
chmod +x operator-sdk

# Move to PATH
sudo mv operator-sdk /usr/local/bin/

# Verify installation
operator-sdk version
```

### Setting up Go Environment

```bash
# Install Go (if not already installed)
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# Add to PATH
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Create Go workspace
mkdir -p ~/go/{bin,src,pkg}
export GOPATH=~/go
export GOROOT=/usr/local/go
echo 'export GOPATH=~/go' >> ~/.bashrc
echo 'export GOROOT=/usr/local/go' >> ~/.bashrc

# Verify Go installation
go version
go env GOPATH GOROOT
```

### Setting up Kubernetes Cluster

```bash
# Using kind (recommended for development)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/

# Create kind cluster
cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF

kind create cluster --config kind-config.yaml --name operator-dev

# Verify cluster
kubectl cluster-info --context kind-operator-dev
kubectl get nodes
```

## Creating Your First Operator

### Initializing Operator Project

```bash
# Create project directory
mkdir my-first-operator
cd my-first-operator

# Initialize operator project
operator-sdk init --domain example.com --repo github.com/example/my-first-operator

# Verify project structure
tree -I vendor
```

### Project Structure Analysis

```
my-first-operator/
├── Dockerfile              # Container build file
├── Makefile               # Build automation
├── PROJECT                # Operator SDK project file
├── config/                # Kubernetes manifests
│   ├── default/          # Default configuration
│   ├── manager/          # Manager deployment
│   ├── manifests/        # CRDs and RBAC
│   └── prometheus/       # Monitoring configuration
├── go.mod                 # Go module file
├── go.sum                 # Go dependencies
├── hack/                  # Build and test scripts
└── main.go               # Operator entry point
```

### Understanding the Entry Point

```go
// main.go - Operator entry point
package main

import (
    "flag"
    "os"

    "k8s.io/apimachinery/pkg/runtime"
    utilruntime "k8s.io/apimachinery/pkg/util/runtime"
    clientgoscheme "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/healthz"
    "sigs.k8s.io/controller-runtime/pkg/log/zap"

    examplev1 "github.com/example/my-first-operator/api/v1"
    "github.com/example/my-first-operator/controllers"
)

var (
    scheme   = runtime.NewScheme()
    setupLog = ctrl.Log.WithName("setup")
)

func init() {
    utilruntime.Must(clientgoscheme.AddToScheme(scheme))
    utilruntime.Must(examplev1.AddToScheme(scheme))
}

func main() {
    var metricsAddr string
    var enableLeaderElection bool
    var probeAddr string

    flag.StringVar(&metricsAddr, "metrics-bind-address", ":8080", "The address the metric endpoint binds to.")
    flag.StringVar(&probeAddr, "health-probe-bind-address", ":8081", "The address the probe endpoint binds to.")
    flag.BoolVar(&enableLeaderElection, "leader-elect", false, "Enable leader election for controller manager.")
    flag.Parse()

    ctrl.SetLogger(zap.New(zap.UseFlagOptions(&zap.Options{})))

    mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
        Scheme:                 scheme,
        MetricsBindAddress:     metricsAddr,
        Port:                   9443,
        HealthProbeBindAddress: probeAddr,
        LeaderElection:         enableLeaderElection,
        LeaderElectionID:       "my-first-operator.example.com",
    })
    if err != nil {
        setupLog.Error(err, "unable to start manager")
        os.Exit(1)
    }

    // Register controllers
    if err = (&controllers.MyFirstOperatorReconciler{
        Client: mgr.GetClient(),
        Scheme: mgr.GetScheme(),
    }).SetupWithManager(mgr); err != nil {
        setupLog.Error(err, "unable to create controller", "controller", "MyFirstOperator")
        os.Exit(1)
    }

    // Add health checks
    if err := mgr.AddHealthzCheck("healthz", healthz.Ping); err != nil {
        setupLog.Error(err, "unable to set up health check")
        os.Exit(1)
    }
    if err := mgr.AddReadyzCheck("readyz", healthz.Ping); err != nil {
        setupLog.Error(err, "unable to set up ready check")
        os.Exit(1)
    }

    setupLog.Info("starting manager")
    if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
        setupLog.Error(err, "problem running manager")
        os.Exit(1)
    }
}
```

## Creating Custom Resources

### Adding a New API

```bash
# Create API for custom resource
operator-sdk create api \
    --group apps \
    --version v1 \
    --kind MyApp \
    --resource \
    --controller

# This creates:
# - API definition (api/v1/myapp_types.go)
# - Controller (controllers/myapp_controller.go)
# - CRD manifest (config/crd/bases/apps.example.com_myapps.yaml)
```

### Understanding the API Definition

```go
// api/v1/myapp_types.go
package v1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// MyAppSpec defines the desired state of MyApp
type MyAppSpec struct {
    // Size is the size of the application deployment
    Size int32 `json:"size"`

    // Image is the container image to run
    Image string `json:"image"`
}

// MyAppStatus defines the observed state of MyApp
type MyAppStatus struct {
    // Nodes are the names of the pods
    Nodes []string `json:"nodes"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status

// MyApp is the Schema for the myapps API
type MyApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   MyAppSpec   `json:"spec,omitempty"`
    Status MyAppStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// MyAppList contains a list of MyApp
type MyAppList struct {
    metav1.TypeMeta `json:",inline"`
    metav1.ListMeta `json:"metadata,omitempty"`
    Items           []MyApp `json:"items"`
}

func init() {
    SchemeBuilder.Register(&MyApp{}, &MyAppList{})
}
```

### Custom Resource Definition (CRD)

```yaml
# config/crd/bases/apps.example.com_myapps.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myapps.apps.example.com
spec:
  group: apps.example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              size:
                type: integer
                minimum: 1
              image:
                type: string
          status:
            type: object
            properties:
              nodes:
                type: array
                items:
                  type: string
  scope: Namespaced
  names:
    plural: myapps
    singular: myapp
    kind: MyApp
    shortNames:
    - ma
```

## Implementing the Controller

### Basic Controller Structure

```go
// controllers/myapp_controller.go
package controllers

import (
    "context"
    "time"

    "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/runtime"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/log"

    appsv1 "github.com/example/my-first-operator/api/v1"
)

type MyAppReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=apps.example.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps/finalizers,verbs=update

func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    logger := log.FromContext(ctx)

    // Get the MyApp resource
    myApp := &appsv1.MyApp{}
    err := r.Get(ctx, req.NamespacedName, myApp)
    if err != nil {
        if errors.IsNotFound(err) {
            // Request object not found, could have been deleted
            return ctrl.Result{}, nil
        }
        // Error reading the object
        return ctrl.Result{}, err
    }

    logger.Info("Reconciling MyApp", "name", myApp.Name, "namespace", myApp.Namespace)

    // TODO: Implement reconciliation logic

    return ctrl.Result{}, nil
}

func (r *MyAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&appsv1.MyApp{}).
        Complete(r)
}
```

### Running the Operator Locally

```bash
# Install CRDs
make install

# Run operator locally (outside cluster)
make run

# In another terminal, create a custom resource
kubectl apply -f - <<EOF
apiVersion: apps.example.com/v1
kind: MyApp
metadata:
  name: my-app-sample
  namespace: default
spec:
  size: 3
  image: nginx:latest
EOF

# Check if the operator is reconciling
kubectl logs -f deployment/my-first-operator-controller-manager -n my-first-operator-system
```

## Understanding the Reconciliation Loop

### The Control Loop Concept

```go
// Conceptual reconciliation loop
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. OBSERVE: Get current state of the world
    currentState := r.observeCurrentState(req)

    // 2. ANALYZE: Compare current state with desired state
    desiredState := r.getDesiredState(req)
    differences := r.compareStates(currentState, desiredState)

    // 3. ACT: Make changes to achieve desired state
    if differences.exist() {
        err := r.actOnDifferences(differences)
        if err != nil {
            return ctrl.Result{}, err
        }
    }

    // 4. REPORT: Update status and metrics
    r.updateStatus(req, currentState)

    // 5. SCHEDULE: Return when to reconcile again
    return r.scheduleNextReconciliation(), nil
}
```

### Key Reconciliation Principles

**Idempotency**: The same reconciliation should produce the same result regardless of how many times it's run.

```go
// Idempotent reconciliation example
func (r *MyAppReconciler) reconcileDeployment(myApp *appsv1.MyApp) error {
    deployment := &appsv1.Deployment{}
    err := r.Get(context.TODO(), client.ObjectKey{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, deployment)

    if err != nil && errors.IsNotFound(err) {
        // Deployment doesn't exist, create it
        return r.createDeployment(myApp)
    } else if err != nil {
        return err
    }

    // Deployment exists, check if it matches desired state
    if needsUpdate(deployment, myApp) {
        return r.updateDeployment(deployment, myApp)
    }

    // Deployment is already correct
    return nil
}
```

**Error Handling**: Proper error handling and recovery mechanisms.

```go
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    logger := log.FromContext(ctx)

    // Get resource
    myApp := &appsv1.MyApp{}
    if err := r.Get(ctx, req.NamespacedName, myApp); err != nil {
        if errors.IsNotFound(err) {
            logger.Info("MyApp resource not found. Ignoring since object must be deleted")
            return ctrl.Result{}, nil
        }
        logger.Error(err, "Failed to get MyApp")
        return ctrl.Result{}, err
    }

    // Attempt reconciliation
    if err := r.reconcileMyApp(ctx, myApp); err != nil {
        logger.Error(err, "Failed to reconcile MyApp")

        // Update status with error
        myApp.Status.Phase = "Error"
        myApp.Status.Message = err.Error()
        if updateErr := r.Status().Update(ctx, myApp); updateErr != nil {
            logger.Error(updateErr, "Failed to update MyApp status")
        }

        // Retry after delay
        return ctrl.Result{RequeueAfter: time.Minute}, err
    }

    // Success
    myApp.Status.Phase = "Running"
    myApp.Status.Message = "Successfully reconciled"
    if err := r.Status().Update(ctx, myApp); err != nil {
        logger.Error(err, "Failed to update MyApp status")
    }

    return ctrl.Result{}, nil
}
```

## Building and Testing

### Building the Operator

```bash
# Build the operator image
make docker-build docker-push IMG=my-registry/my-first-operator:v0.1.0

# Deploy to cluster
make deploy IMG=my-registry/my-first-operator:v0.1.0

# Check deployment
kubectl get deployments -n my-first-operator-system
kubectl get pods -n my-first-operator-system
```

### Basic Testing

```bash
# Run unit tests
make test

# Run integration tests (requires cluster)
make test-integration

# Clean up
make undeploy
```

## Summary

In this chapter, we've covered:

- **Operator Fundamentals**: Understanding what operators are and why they matter
- **Development Setup**: Installing Operator SDK, Go, and Kubernetes cluster
- **Project Creation**: Initializing operator projects and understanding structure
- **Custom Resources**: Creating APIs and CRDs for custom resources
- **Controller Implementation**: Basic controller structure and reconciliation concepts
- **Local Development**: Running operators locally and testing with kubectl

## Key Takeaways

1. **Declarative Management**: Operators extend Kubernetes with declarative APIs for complex applications
2. **Reconciliation Loop**: Controllers continuously reconcile actual state with desired state
3. **Idempotent Operations**: Same result regardless of how many times operations are performed
4. **Custom Resources**: CRDs extend the Kubernetes API with domain-specific objects
5. **RBAC Security**: Proper permissions for controllers to manage cluster resources

Next, we'll dive deep into **Custom Resource Definitions** and how to design robust APIs for your operators.

---

**Ready for the next chapter?** [Chapter 2: Custom Resource Definitions](02-custom-resources.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*