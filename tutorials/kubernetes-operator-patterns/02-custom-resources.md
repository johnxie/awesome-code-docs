---
layout: default
title: "Kubernetes Operator Patterns - Chapter 2: Custom Resource Definitions"
nav_order: 2
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 2: Custom Resource Definitions - Designing Robust APIs

> Master CRD design, OpenAPI validation, versioning strategies, and best practices for extending the Kubernetes API.

## Overview

Custom Resource Definitions (CRDs) are the foundation of Kubernetes operators. This chapter covers designing, implementing, and managing CRDs with proper validation, versioning, and API design principles.

## CRD Fundamentals

### CRD Structure and Components

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myapps.example.com  # <plural>.<group>
spec:
  group: example.com        # API group
  versions:                 # Supported versions
  - name: v1               # Version name
    served: true           # Serve this version via API
    storage: true          # Store objects in this version
    schema:                # OpenAPI schema validation
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas:
                type: integer
                minimum: 1
                maximum: 100
              image:
                type: string
                pattern: '^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$'
          status:
            type: object
            properties:
              phase:
                type: string
                enum: ["Pending", "Running", "Failed"]
  scope: Namespaced         # or Cluster
  names:
    plural: myapps         # Plural name
    singular: myapp        # Singular name
    kind: MyApp           # Kind name
    shortNames:           # Short names
    - ma
    categories:           # Categories for UI grouping
    - all
    - example
```

### CRD Naming Conventions

```yaml
# Good CRD naming
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.postgresql.example.com
spec:
  group: postgresql.example.com
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames:
    - db
    - dbs

# Bad CRD naming (too generic)
metadata:
  name: apps.example.com  # Too generic, conflicts possible
spec:
  names:
    plural: apps         # Conflicts with built-in apps group
```

### Go Type Definitions

```go
// +kubebuilder:object:generate=true
// +kubebuilder:object:root=true
// +kubebuilder:resource:shortName=db
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Age",type="date",JSONPath=".metadata.creationTimestamp"
// +kubebuilder:printcolumn:name="Phase",type="string",JSONPath=".status.phase"

type Database struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   DatabaseSpec   `json:"spec,omitempty"`
    Status DatabaseStatus `json:"status,omitempty"`
}

// DatabaseSpec defines the desired state
type DatabaseSpec struct {
    // Engine is the database engine (postgresql, mysql, mongodb)
    Engine string `json:"engine"`

    // Version is the database version
    Version string `json:"version"`

    // Storage is the storage configuration
    Storage *StorageSpec `json:"storage,omitempty"`

    // Backup defines backup configuration
    Backup *BackupSpec `json:"backup,omitempty"`
}

// DatabaseStatus defines the observed state
type DatabaseStatus struct {
    // Phase is the current phase
    Phase DatabasePhase `json:"phase"`

    // Message provides additional information
    Message string `json:"message,omitempty"`

    // Conditions represent the latest available observations
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}

type DatabasePhase string

const (
    DatabasePhasePending   DatabasePhase = "Pending"
    DatabasePhaseCreating  DatabasePhase = "Creating"
    DatabasePhaseRunning   DatabasePhase = "Running"
    DatabasePhaseFailed    DatabasePhase = "Failed"
    DatabasePhaseDeleting  DatabasePhase = "Deleting"
)

// StorageSpec defines storage configuration
type StorageSpec struct {
    // Size is the storage size (e.g., "10Gi")
    Size string `json:"size"`

    // ClassName is the storage class name
    ClassName string `json:"className,omitempty"`

    // AccessModes contains the desired access modes
    AccessModes []corev1.PersistentVolumeAccessMode `json:"accessModes,omitempty"`
}

// BackupSpec defines backup configuration
type BackupSpec struct {
    // Enabled specifies if backup is enabled
    Enabled bool `json:"enabled"`

    // Schedule is the backup schedule in cron format
    Schedule string `json:"schedule"`

    // RetentionDays is the number of days to retain backups
    RetentionDays int32 `json:"retentionDays"`
}
```

## OpenAPI Schema Validation

### Basic Schema Validation

```yaml
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
        properties:
          spec:
            type: object
            properties:
              engine:
                type: string
                enum: ["postgresql", "mysql", "mongodb"]
              version:
                type: string
                pattern: '^\d+\.\d+$'  # Semantic versioning
              replicas:
                type: integer
                minimum: 1
                maximum: 10
              storage:
                type: object
                properties:
                  size:
                    type: string
                    pattern: '^\d+(Gi|Mi|Ki)$'
                  className:
                    type: string
            required: ["engine", "version"]  # Required fields
          status:
            type: object
            properties:
              phase:
                type: string
                enum: ["Pending", "Running", "Failed"]
              message:
                type: string
```

### Advanced Validation Rules

```yaml
spec:
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              # Conditional validation
              engine:
                type: string
                enum: ["postgresql", "mysql"]
              postgresql:
                type: object
                properties:
                  version:
                    type: string
                    enum: ["13", "14", "15"]
                # Only required when engine is postgresql
                oneOf:
                - required: ["postgresql"]
                  properties:
                    engine:
                      enum: ["postgresql"]
                - required: ["mysql"]
                  properties:
                    engine:
                      enum: ["mysql"]

              # Array validation with uniqueness
              tags:
                type: array
                items:
                  type: string
                  minLength: 1
                  maxLength: 50
                uniqueItems: true
                maxItems: 10

              # Complex nested validation
              network:
                type: object
                properties:
                  ports:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                        port:
                          type: integer
                          minimum: 1
                          maximum: 65535
                        protocol:
                          type: string
                          enum: ["TCP", "UDP", "SCTP"]
                      required: ["port", "protocol"]
                # Custom validation rule
                x-kubernetes-validations:
                - rule: "self.ports.all(p, p.port != 80 || p.name == 'http')"
                  message: "Port 80 must be named 'http'"

          # Status validation
          status:
            type: object
            properties:
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                    status:
                      type: string
                      enum: ["True", "False", "Unknown"]
                    lastTransitionTime:
                      type: string
                      format: date-time
                    reason:
                      type: string
                    message:
                      type: string
                  required: ["type", "status"]
```

### Validation Webhooks

```go
// Validation webhook implementation
package webhooks

import (
    "context"
    "fmt"

    apierrors "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/runtime/schema"
    "k8s.io/apimachinery/pkg/util/validation/field"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/webhook"
    "sigs.k8s.io/controller-runtime/pkg/webhook/admission"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

type DatabaseValidator struct {
    client  client.Client
    decoder *admission.Decoder
}

func (v *DatabaseValidator) ValidateCreate(ctx context.Context, obj runtime.Object) error {
    database := obj.(*postgresqlv1.Database)
    return v.validateDatabase(database)
}

func (v *DatabaseValidator) ValidateUpdate(ctx context.Context, oldObj, newObj runtime.Object) error {
    oldDatabase := oldObj.(*postgresqlv1.Database)
    newDatabase := newObj.(*postgresqlv1.Database)

    // Prevent certain updates
    if oldDatabase.Spec.Engine != newDatabase.Spec.Engine {
        return apierrors.NewForbidden(
            schema.GroupResource{Group: "postgresql.example.com", Resource: "databases"},
            newDatabase.Name,
            field.Forbidden(field.NewPath("spec", "engine"), "engine cannot be changed after creation"),
        )
    }

    return v.validateDatabase(newDatabase)
}

func (v *DatabaseValidator) validateDatabase(database *postgresqlv1.Database) error {
    var allErrs field.ErrorList

    // Validate engine and version compatibility
    if database.Spec.Engine == "postgresql" {
        if database.Spec.Version != "13" && database.Spec.Version != "14" && database.Spec.Version != "15" {
            allErrs = append(allErrs, field.Invalid(
                field.NewPath("spec", "version"),
                database.Spec.Version,
                "PostgreSQL version must be 13, 14, or 15",
            ))
        }
    }

    // Validate storage size
    if database.Spec.Storage != nil {
        // Parse size (simplified validation)
        if len(database.Spec.Storage.Size) == 0 {
            allErrs = append(allErrs, field.Required(
                field.NewPath("spec", "storage", "size"),
                "storage size is required",
            ))
        }
    }

    if len(allErrs) == 0 {
        return nil
    }

    return apierrors.NewInvalid(
        schema.GroupKind{Group: "postgresql.example.com", Kind: "Database"},
        database.Name,
        allErrs,
    )
}

func (v *DatabaseValidator) SetupWebhookWithManager(mgr ctrl.Manager) error {
    v.client = mgr.GetClient()
    return ctrl.NewWebhookManagedBy(mgr).
        For(&postgresqlv1.Database{}).
        WithValidator(v).
        Complete()
}
```

## API Versioning and Evolution

### Versioning Strategy

```yaml
# Multiple versions in CRD
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.postgresql.example.com
spec:
  group: postgresql.example.com
  versions:
  - name: v1      # Current stable version
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        # v1 schema
  - name: v1beta1  # Previous beta version
    served: true
    storage: false  # Not used for storage
    schema:
      openAPIV3Schema:
        # v1beta1 schema (may be less strict)
  - name: v1alpha1 # Deprecated alpha version
    served: false  # No longer served
    storage: false
    schema:
      openAPIV3Schema:
        # v1alpha1 schema
```

### Version Conversion Webhooks

```go
// Conversion webhook for API version migration
type DatabaseConversionWebhook struct{}

func (w *DatabaseConversionWebhook) Convert(from, to *runtime.RawExtension, hub runtime.Object) error {
    fromGV := from.Object.GetObjectKind().GroupVersionKind()

    switch fromGV.Version {
    case "v1beta1":
        return w.convertV1Beta1ToV1(from, to)
    case "v1alpha1":
        return w.convertV1Alpha1ToV1(from, to)
    default:
        return fmt.Errorf("unsupported version: %s", fromGV.Version)
    }
}

func (w *DatabaseConversionWebhook) convertV1Beta1ToV1(from, to *runtime.RawExtension) error {
    // Convert v1beta1 Database to v1 Database
    v1beta1DB := &DatabaseV1Beta1{}
    if err := json.Unmarshal(from.Raw, v1beta1DB); err != nil {
        return err
    }

    // Apply conversion logic
    v1DB := &DatabaseV1{
        TypeMeta: metav1.TypeMeta{
            APIVersion: "postgresql.example.com/v1",
            Kind:       "Database",
        },
        ObjectMeta: v1beta1DB.ObjectMeta,
        Spec: DatabaseSpec{
            Engine:  v1beta1DB.Spec.Engine,
            Version: v1beta1DB.Spec.Version,
            // Add default values for new fields
            Replicas: 1,  // Default to 1 replica
        },
    }

    to.Raw, err := json.Marshal(v1DB)
    return err
}
```

### Conversion Functions

```go
// Conversion functions in Go types
func Convert_v1beta1_Database_To_v1_Database(in *DatabaseV1Beta1, out *DatabaseV1, s conversion.Scope) error {
    // Basic field conversion
    out.ObjectMeta = in.ObjectMeta
    out.Spec.Engine = in.Spec.Engine
    out.Spec.Version = in.Spec.Version

    // Handle renamed fields
    if in.Spec.Size != "" {
        out.Spec.Storage = &StorageSpec{
            Size: in.Spec.Size,
        }
    }

    // Set defaults for new fields
    if out.Spec.Replicas == 0 {
        out.Spec.Replicas = 1
    }

    return nil
}

func Convert_v1_Database_To_v1beta1_Database(in *DatabaseV1, out *DatabaseV1Beta1, s conversion.Scope) error {
    // Reverse conversion (may lose information)
    out.ObjectMeta = in.ObjectMeta
    out.Spec.Engine = in.Spec.Engine
    out.Spec.Version = in.Spec.Version

    if in.Spec.Storage != nil {
        out.Spec.Size = in.Spec.Storage.Size
    }

    return nil
}
```

## CRD Categories and UI Integration

### kubectl Integration

```yaml
# CRD with kubectl integration features
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.postgresql.example.com
  annotations:
    # kubectl integration
    "kubectl.kubernetes.io/default-column": "true"
    "kubectl.kubernetes.io/default-print-column": "true"
spec:
  group: postgresql.example.com
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        # Schema definition
    # Additional printer columns
    additionalPrinterColumns:
    - name: Age
      type: date
      jsonPath: .metadata.creationTimestamp
    - name: Phase
      type: string
      jsonPath: .status.phase
      description: Current phase of the database
    - name: Version
      type: string
      jsonPath: .spec.version
      description: Database version
    - name: Engine
      type: string
      jsonPath: .spec.engine
      description: Database engine
  names:
    categories:
    - postgresql
    - database
    - all
```

### kubectl Commands

```bash
# List databases with custom columns
kubectl get databases

# Output:
# NAME         AGE    PHASE     VERSION   ENGINE
# my-postgres  5m     Running   14        postgresql
# my-mysql     3m     Pending   8.0       mysql

# Get detailed information
kubectl describe database my-postgres

# Edit database spec
kubectl edit database my-postgres

# View logs
kubectl logs -l app=postgres-operator

# Scale database
kubectl scale database my-postgres --replicas=3
```

## Best Practices for CRD Design

### API Design Principles

```go
// Good: Clear, focused API
type Database struct {
    Spec DatabaseSpec `json:"spec"`
    Status DatabaseStatus `json:"status"`
}

type DatabaseSpec struct {
    // Clear, required fields
    Engine  string `json:"engine"`  // Required
    Version string `json:"version"` // Required

    // Optional fields with clear defaults
    Replicas *int32 `json:"replicas,omitempty"`

    // Complex nested structures
    Storage *StorageSpec `json:"storage,omitempty"`
    Backup  *BackupSpec  `json:"backup,omitempty"`
}

// Bad: Overly complex API
type Database struct {
    // Too many top-level fields
    Engine string `json:"engine"`
    Version string `json:"version"`
    Replicas int32 `json:"replicas"`
    StorageSize string `json:"storageSize"`
    StorageClass string `json:"storageClass"`
    BackupEnabled bool `json:"backupEnabled"`
    BackupSchedule string `json:"backupSchedule"`
    // ... many more fields
}
```

### Validation Best Practices

```yaml
# Comprehensive validation schema
openAPIV3Schema:
  type: object
  properties:
    spec:
      type: object
      properties:
        engine:
          type: string
          enum: ["postgresql", "mysql", "mongodb"]
          # Use x-kubernetes-validations for complex rules
          x-kubernetes-validations:
          - rule: "self == oldSelf || !oldSelf.exists"  # Immutable field
            message: "engine cannot be changed after creation"
        version:
          type: string
          pattern: '^\d+\.\d+(\.\d+)?$'  # Semantic versioning
        replicas:
          type: integer
          minimum: 1
          maximum: 10
          default: 1
        storage:
          type: object
          properties:
            size:
              type: string
              pattern: '^\d+[KMGT]i$'  # Kubernetes quantity format
            className:
              type: string
              maxLength: 63
      required: ["engine", "version"]  # Minimal required fields
```

### Documentation and Examples

```go
// Well-documented types
type DatabaseSpec struct {
    // Engine is the database engine to use.
    // Supported values: postgresql, mysql, mongodb
    // +kubebuilder:validation:Enum=postgresql;mysql;mongodb
    // +kubebuilder:validation:Required
    Engine string `json:"engine"`

    // Version is the version of the database engine.
    // For PostgreSQL: 13, 14, 15
    // For MySQL: 8.0, 8.1
    // +kubebuilder:validation:Required
    Version string `json:"version"`

    // Replicas is the number of database replicas.
    // Minimum: 1, Maximum: 10, Default: 1
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    // +kubebuilder:default=1
    Replicas int32 `json:"replicas,omitempty"`
}
```

## CRD Lifecycle Management

### Installation and Updates

```bash
# Install CRD
kubectl apply -f config/crd/bases/apps.example.com_myapps.yaml

# Check CRD status
kubectl get crd myapps.apps.example.com
kubectl describe crd myapps.apps.example.com

# Update CRD (be careful with existing resources)
kubectl apply -f config/crd/bases/apps.example.com_myapps.yaml

# Check for validation errors
kubectl get crd myapps.apps.example.com -o yaml
```

### Troubleshooting CRDs

```bash
# Check CRD events
kubectl describe crd myapps.apps.example.com

# Check validation errors
kubectl get events --field-selector reason=FailedCreate

# Debug webhook validation
kubectl logs -l app=webhook-server

# Test CRD with dry-run
kubectl apply -f myapp.yaml --dry-run=server

# Check API discovery
kubectl api-resources | grep myapp
kubectl api-versions | grep example.com
```

### CRD Cleanup

```bash
# Remove all custom resources first
kubectl delete myapps --all --all-namespaces

# Remove CRD
kubectl delete crd myapps.apps.example.com

# Clean up finalizers if needed
kubectl patch crd myapps.apps.example.com -p '{"metadata":{"finalizers":[]}}' --type=merge
```

## Summary

In this chapter, we've covered:

- **CRD Structure**: Components, naming conventions, and Go type definitions
- **OpenAPI Validation**: Schema validation, advanced rules, and webhooks
- **API Versioning**: Versioning strategies, conversion webhooks, and evolution
- **kubectl Integration**: Categories, printer columns, and custom commands
- **Best Practices**: API design, validation, documentation, and lifecycle management

## Key Takeaways

1. **Validation First**: Use OpenAPI schemas and webhooks for robust validation
2. **Version Carefully**: Plan API evolution with conversion webhooks
3. **Design for UX**: Good naming, categories, and kubectl integration
4. **Document Well**: Clear field descriptions and examples
5. **Test Thoroughly**: Validate CRDs with dry-run and comprehensive testing

Next, we'll explore the **reconciliation loop** - the heart of operator functionality and state management.

---

**Ready for the next chapter?** [Chapter 3: The Reconciliation Loop](03-reconciliation-loop.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*