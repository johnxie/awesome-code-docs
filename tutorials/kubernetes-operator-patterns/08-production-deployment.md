---
layout: default
title: "Kubernetes Operator Patterns - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 8: Production Deployment - OLM, Helm Charts, Security, and Scaling

> Deploy operators to production with Operator Lifecycle Manager, Helm charts, enterprise security, and automated scaling strategies.

## Overview

Production deployment requires robust packaging, security, lifecycle management, and scaling. This chapter covers Operator Lifecycle Manager (OLM), Helm packaging, security hardening, and production scaling patterns.

## Operator Lifecycle Manager (OLM)

### OLM Bundle Creation

```yaml
# config/manifests/bases/postgresql-operator.clusterserviceversion.yaml
apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
metadata:
  name: postgresql-operator.v1.0.0
  namespace: placeholder
  annotations:
    alm-examples: '[{"apiVersion":"postgresql.example.com/v1","kind":"Database","metadata":{"name":"example-database"},"spec":{"engine":"postgresql","version":"14","replicas":1,"image":"postgres:14"}}]'
    capabilities: Seamless Upgrades
    categories: Database
    certified: "false"
    containerImage: quay.io/example/postgresql-operator:v1.0.0
    createdAt: "2024-01-01T00:00:00Z"
    description: PostgreSQL Operator for Kubernetes
    repository: https://github.com/example/postgresql-operator
    support: example.com
spec:
  displayName: PostgreSQL Operator
  description: |
    A Kubernetes operator for managing PostgreSQL databases with automated provisioning,
    scaling, backup, and recovery capabilities.
  provider:
    name: Example Inc.
  maturity: alpha
  version: 1.0.0
  replaces: postgresql-operator.v0.9.0
  links:
  - name: Documentation
    url: https://github.com/example/postgresql-operator/tree/main/docs
  - name: Source Code
    url: https://github.com/example/postgresql-operator
  maintainers:
  - email: operator@example.com
    name: Operator Team
  keywords:
  - postgresql
  - database
  - operator
  - kubernetes
  labels:
    alm-owner-postgresql: postgresql-operator
    operated-by: postgresql-operator
  selector:
    matchLabels:
      alm-owner-postgresql: postgresql-operator
  installModes:
  - supported: true
    type: OwnNamespace
  - supported: true
    type: SingleNamespace
  - supported: false
    type: MultiNamespace
  - supported: false
    type: AllNamespaces
  customresourcedefinitions:
    owned:
    - description: Represents a PostgreSQL database instance
      displayName: Database
      kind: Database
      name: databases.postgresql.example.com
      version: v1
      resources:
      - kind: Deployment
        name: ""
        version: v1
      - kind: Service
        name: ""
        version: v1
      - kind: PersistentVolumeClaim
        name: ""
        version: v1
  install:
    spec:
      deployments:
      - name: postgresql-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: postgresql-operator
          template:
            metadata:
              labels:
                app: postgresql-operator
            spec:
              containers:
              - name: operator
                image: quay.io/example/postgresql-operator:v1.0.0
                command:
                - /manager
                env:
                - name: WATCH_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.namespace
                - name: POD_NAME
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.name
                - name: OPERATOR_NAME
                  value: postgresql-operator
                resources:
                  limits:
                    cpu: 200m
                    memory: 256Mi
                  requests:
                    cpu: 100m
                    memory: 128Mi
                securityContext:
                  allowPrivilegeEscalation: false
                  capabilities:
                    drop:
                    - ALL
                  readOnlyRootFilesystem: true
                  runAsNonRoot: true
                  runAsUser: 65534
                  seccompProfile:
                    type: RuntimeDefault
      permissions:
      - rules:
        - apiGroups:
          - postgresql.example.com
          resources:
          - databases
          - databases/status
          - databases/finalizers
          verbs:
          - create
          - delete
          - get
          - list
          - patch
          - update
          - watch
        - apiGroups:
          - apps
          resources:
          - deployments
          verbs:
          - create
          - delete
          - get
          - list
          - patch
          - update
          - watch
        - apiGroups:
          - ""
          resources:
          - services
          - persistentvolumeclaims
          - configmaps
          - secrets
          verbs:
          - create
          - delete
          - get
          - list
          - patch
          - update
          - watch
        - apiGroups:
          - ""
          resources:
          - events
          verbs:
          - create
          - patch
          - update
        serviceAccountName: postgresql-operator
    strategy: deployment
```

### Creating OLM Bundle

```bash
# Generate OLM bundle
operator-sdk generate kustomize manifests --interactive=false

# Create bundle directory
mkdir -p bundle
operator-sdk generate bundle --package postgresql-operator --version 1.0.0 --default-channel stable

# Build and push bundle image
make bundle-build bundle-push BUNDLE_IMG=quay.io/example/postgresql-operator-bundle:v1.0.0

# Run bundle validation
operator-sdk bundle validate ./bundle

# Build and push catalog
make catalog-build catalog-push CATALOG_IMG=quay.io/example/postgresql-operator-catalog:v1.0.0
```

### OLM Installation

```bash
# Install OLM (if not already installed)
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.24.0/install.sh | bash

# Create operator group
cat <<EOF | kubectl apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: postgresql-operator-group
  namespace: postgresql-system
spec:
  targetNamespaces:
  - postgresql-system
EOF

# Create subscription
cat <<EOF | kubectl apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: postgresql-operator-subscription
  namespace: postgresql-system
spec:
  channel: stable
  name: postgresql-operator
  source: postgresql-operator-catalog
  sourceNamespace: olm
  installPlanApproval: Automatic
  startingCSV: postgresql-operator.v1.0.0
EOF

# Verify installation
kubectl get csv -n postgresql-system
kubectl get subscription -n postgresql-system
kubectl get installplan -n postgresql-system
```

## Helm Chart Packaging

### Operator Helm Chart Structure

```
helm/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── role.yaml
│   ├── rolebinding.yaml
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── customresourcedefinition.yaml
└── crds/
    └── postgresql.example.com_databases.yaml
```

### Chart.yaml Configuration

```yaml
# helm/Chart.yaml
apiVersion: v2
name: postgresql-operator
description: A Helm chart for PostgreSQL Operator
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
- postgresql
- database
- operator
- kubernetes
home: https://github.com/example/postgresql-operator
sources:
- https://github.com/example/postgresql-operator
maintainers:
- name: Operator Team
  email: operator@example.com
annotations:
  artifacthub.io/operator: "true"
  artifacthub.io/operatorCapabilities: Seamless Upgrades
  artifacthub.io/crds: |
    - kind: Database
      version: v1
      name: databases.postgresql.example.com
      displayName: Database
      description: Represents a PostgreSQL database instance
```

### Values Configuration

```yaml
# helm/values.yaml
# Default values for postgresql-operator
replicaCount: 1

image:
  repository: quay.io/example/postgresql-operator
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}
podLabels: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 65534

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

nodeSelector: {}

tolerations: []

affinity: {}

# Operator configuration
operator:
  watchNamespaces: ""
  logLevel: info
  metricsAddr: ":8080"
  probeAddr: ":8081"
  enableLeaderElection: true

# Database defaults
database:
  defaultEngine: postgresql
  defaultVersion: "14"
  defaultReplicas: 1
  defaultStorageSize: "10Gi"
  defaultStorageClass: ""

# Monitoring
monitoring:
  enabled: true
  serviceMonitor:
    enabled: false
    namespace: ""
    labels: {}

# Security
security:
  tls:
    enabled: true
    certManager:
      enabled: false
      issuerName: ""
  networkPolicy:
    enabled: false
```

### Helm Templates

```yaml
# helm/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "postgresql-operator.fullname" . }}
  labels:
    {{- include "postgresql-operator.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "postgresql-operator.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "postgresql-operator.selectorLabels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "postgresql-operator.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: manager
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: {{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          command:
            - /manager
          env:
            - name: WATCH_NAMESPACE
              value: {{ .Values.operator.watchNamespaces | quote }}
            - name: LOG_LEVEL
              value: {{ .Values.operator.logLevel | quote }}
            - name: METRICS_ADDR
              value: {{ .Values.operator.metricsAddr | quote }}
            - name: PROBE_ADDR
              value: {{ .Values.operator.probeAddr | quote }}
            - name: ENABLE_LEADER_ELECTION
              value: {{ .Values.operator.enableLeaderElection | quote }}
          ports:
            - name: metrics
              containerPort: 8080
              protocol: TCP
            - name: health
              containerPort: 8081
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /healthz
              port: health
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /readyz
              port: health
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### Helm Installation

```bash
# Add Helm repository
helm repo add postgresql-operator https://example.github.io/postgresql-operator
helm repo update

# Install operator
helm install postgresql-operator postgresql-operator/postgresql-operator \
  --namespace postgresql-system \
  --create-namespace \
  --set operator.watchNamespaces="database-system" \
  --set database.defaultStorageClass="fast-ssd"

# Upgrade operator
helm upgrade postgresql-operator postgresql-operator/postgresql-operator \
  --namespace postgresql-system \
  --set image.tag="v1.1.0"

# Uninstall operator
helm uninstall postgresql-operator --namespace postgresql-system

# List releases
helm list --namespace postgresql-system
```

## Security Hardening

### Pod Security Standards

```yaml
# Pod security context
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql-operator
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534  # nobody user
        runAsGroup: 65534
        fsGroup: 65534
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: operator
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 65534
          runAsGroup: 65534
        # Mount empty dir for temp files
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
```

### Network Policies

```yaml
# Network policy for operator
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgresql-operator-network-policy
  namespace: postgresql-system
spec:
  podSelector:
    matchLabels:
      app: postgresql-operator
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow webhooks from API server
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: default  # API server namespace
    ports:
    - protocol: TCP
      port: 9443  # webhook port
  # Allow metrics scraping
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: monitoring
    ports:
    - protocol: TCP
      port: 8080  # metrics port
  egress:
  # Allow DNS resolution
  - to: []
    ports:
    - protocol: UDP
      port: 53
  # Allow HTTPS outbound (for external APIs)
  - to: []
    ports:
    - protocol: TCP
      port: 443
  # Allow communication within cluster
  - to:
    - podSelector: {}  # All pods in namespace
    ports:
    - protocol: TCP
  # Deny all other traffic
  - to: []
    ports: []
```

### RBAC Security

```yaml
# Least privilege RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: postgresql-operator-role
  namespace: postgresql-system
rules:
# CRD permissions
- apiGroups:
  - postgresql.example.com
  resources:
  - databases
  - databases/status
  - databases/finalizers
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
# Core resource permissions (minimal)
- apiGroups:
  - apps
  resources:
  - deployments
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
- apiGroups:
  - ""
  resources:
  - services
  - persistentvolumeclaims
  - configmaps
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
# Event permissions
- apiGroups:
  - ""
  resources:
  - events
  verbs:
  - create
  - patch
  - update
# Certificate permissions (for webhooks)
- apiGroups:
  - cert-manager.io
  resources:
  - certificates
  - issuers
  verbs:
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: postgresql-operator-rolebinding
  namespace: postgresql-system
subjects:
- kind: ServiceAccount
  name: postgresql-operator
  namespace: postgresql-system
roleRef:
  kind: Role
  name: postgresql-operator-role
  apiGroup: rbac.authorization.k8s.io
```

## Scaling Patterns

### Horizontal Pod Autoscaling

```yaml
# HPA for operator based on custom metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: postgresql-operator-hpa
  namespace: postgresql-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: postgresql-operator
  minReplicas: 1
  maxReplicas: 5
  metrics:
  # Scale on queue size
  - type: Pods
    pods:
      metric:
        name: operator_queue_size
      target:
        type: AverageValue
        averageValue: "10"
  # Scale on reconciliation rate
  - type: Pods
    pods:
      metric:
        name: operator_reconciliation_rate
      target:
        type: AverageValue
        averageValue: "50"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
```

### Operator Sharding

```go
// Sharding configuration for large clusters
type ShardingConfig struct {
    ShardCount     int      `json:"shardCount"`
    ShardSelector  string   `json:"shardSelector"`
    NamespaceSelector string `json:"namespaceSelector"`
}

func (r *DatabaseReconciler) isResponsibleForShard(database *postgresqlv1.Database) bool {
    // Simple sharding based on namespace hash
    if r.shardingConfig.ShardCount <= 1 {
        return true
    }

    namespaceHash := hashString(database.Namespace)
    responsibleShard := namespaceHash % r.shardingConfig.ShardCount

    return responsibleShard == r.shardID
}

func hashString(s string) int {
    h := 0
    for _, r := range s {
        h = 31*h + int(r)
    }
    return h
}

// Controller manager with sharding
func setupShardedManager(shardID int, totalShards int) (ctrl.Manager, error) {
    mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
        // ... other options
    })

    if err != nil {
        return nil, err
    }

    // Create sharded reconciler
    reconciler := &DatabaseReconciler{
        shardID: shardID,
        shardingConfig: &ShardingConfig{
            ShardCount: totalShards,
        },
    }

    // Only reconcile resources for this shard
    err = ctrl.NewControllerManagedBy(mgr).
        For(&postgresqlv1.Database{}).
        WithEventFilter(predicate.Funcs{
            CreateFunc: func(e event.CreateEvent) bool {
                db := e.Object.(*postgresqlv1.Database)
                return reconciler.isResponsibleForShard(db)
            },
            UpdateFunc: func(e event.UpdateEvent) bool {
                db := e.ObjectNew.(*postgresqlv1.Database)
                return reconciler.isResponsibleForShard(db)
            },
            DeleteFunc: func(e event.DeleteEvent) bool {
                db := e.Object.(*postgresqlv1.Database)
                return reconciler.isResponsibleForShard(db)
            },
        }).
        Complete(reconciler)

    return mgr, err
}
```

### Multi-Cluster Deployment

```yaml
# Multi-cluster operator deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql-operator
  namespace: postgresql-system
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: operator
        image: quay.io/example/postgresql-operator:v1.0.0
        env:
        # Cluster-aware configuration
        - name: CLUSTER_NAME
          valueFrom:
            configMapKeyRef:
              name: cluster-config
              key: clusterName
        - name: CLUSTER_REGION
          valueFrom:
            configMapKeyRef:
              name: cluster-config
              key: clusterRegion
        # Multi-cluster leader election
        - name: LEADER_ELECTION_NAMESPACE
          value: "postgresql-global"
        - name: LEADER_ELECTION_NAME
          value: "postgresql-operator-leader"
---
# Cluster configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-config
  namespace: postgresql-system
data:
  clusterName: "production-us-east"
  clusterRegion: "us-east-1"
  clusterType: "regional"
```

## Backup and Disaster Recovery

### Operator Backup Strategy

```go
// Operator backup and recovery
type BackupManager struct {
    client client.Client
}

func (bm *BackupManager) CreateOperatorBackup(ctx context.Context, namespace string) error {
    timestamp := time.Now().Format("20060102-150405")

    // Backup CRDs
    crdBackup := &corev1.ConfigMap{
        ObjectMeta: metav1.ObjectMeta{
            Name: fmt.Sprintf("operator-backup-crds-%s", timestamp),
            Namespace: namespace,
        },
        Data: map[string]string{
            "crds.yaml": bm.exportCRDs(ctx),
        },
    }

    if err := bm.client.Create(ctx, crdBackup); err != nil {
        return err
    }

    // Backup RBAC
    rbacBackup := &corev1.ConfigMap{
        ObjectMeta: metav1.ObjectMeta{
            Name: fmt.Sprintf("operator-backup-rbac-%s", timestamp),
            Namespace: namespace,
        },
        Data: map[string]string{
            "rbac.yaml": bm.exportRBAC(ctx, namespace),
        },
    }

    if err := bm.client.Create(ctx, rbacBackup); err != nil {
        return err
    }

    // Backup custom resources
    crBackup := &corev1.ConfigMap{
        ObjectMeta: metav1.ObjectMeta{
            Name: fmt.Sprintf("operator-backup-resources-%s", timestamp),
            Namespace: namespace,
        },
        Data: map[string]string{
            "databases.yaml": bm.exportCustomResources(ctx),
        },
    }

    return bm.client.Create(ctx, crBackup)
}

func (bm *BackupManager) RestoreOperator(ctx context.Context, namespace, timestamp string) error {
    // Restore in reverse order: CRDs, RBAC, then resources

    // Restore CRDs
    crdConfig := &corev1.ConfigMap{}
    if err := bm.client.Get(ctx, client.ObjectKey{
        Name: fmt.Sprintf("operator-backup-crds-%s", timestamp),
        Namespace: namespace,
    }, crdConfig); err != nil {
        return err
    }

    if err := bm.applyYAML(ctx, crdConfig.Data["crds.yaml"]); err != nil {
        return err
    }

    // Restore RBAC
    rbacConfig := &corev1.ConfigMap{}
    if err := bm.client.Get(ctx, client.ObjectKey{
        Name: fmt.Sprintf("operator-backup-rbac-%s", timestamp),
        Namespace: namespace,
    }, rbacConfig); err != nil {
        return err
    }

    if err := bm.applyYAML(ctx, rbacConfig.Data["rbac.yaml"]); err != nil {
        return err
    }

    // Wait for RBAC to be ready
    time.Sleep(10 * time.Second)

    // Restore custom resources
    crConfig := &corev1.ConfigMap{}
    if err := bm.client.Get(ctx, client.ObjectKey{
        Name: fmt.Sprintf("operator-backup-resources-%s", timestamp),
        Namespace: namespace,
    }, crConfig); err != nil {
        return err
    }

    return bm.applyYAML(ctx, crConfig.Data["databases.yaml"])
}
```

## Summary

In this final chapter, we've covered:

- **OLM Integration**: Bundle creation, validation, and installation
- **Helm Packaging**: Chart structure, templates, and deployment
- **Security Hardening**: Pod security, network policies, and RBAC
- **Scaling Strategies**: HPA, sharding, and multi-cluster deployment
- **Backup and Recovery**: Operator state backup and disaster recovery

## Key Takeaways

1. **OLM Packaging**: Standardized operator distribution and lifecycle management
2. **Helm Charts**: Flexible packaging for different deployment scenarios
3. **Security First**: Least privilege RBAC and network isolation
4. **Scalability**: Horizontal scaling and multi-cluster support
5. **Reliability**: Backup, recovery, and disaster recovery procedures

This concludes our comprehensive Kubernetes Operator Patterns tutorial. You now have the knowledge to build, test, deploy, and operate production-grade Kubernetes operators.

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*