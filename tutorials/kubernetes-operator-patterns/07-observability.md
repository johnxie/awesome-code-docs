---
layout: default
title: "Kubernetes Operator Patterns - Chapter 7: Observability & Debugging"
nav_order: 7
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 7: Observability & Debugging - Metrics, Logging, Tracing, and Troubleshooting

Welcome to **Chapter 7: Observability & Debugging - Metrics, Logging, Tracing, and Troubleshooting**. In this part of **Kubernetes Operator Patterns: Building Production-Grade Controllers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master comprehensive observability for Kubernetes operators including metrics collection, structured logging, distributed tracing, and systematic debugging approaches.

## Overview

Observability is crucial for production operators. This chapter covers implementing metrics, logging, tracing, and debugging capabilities to ensure operators are maintainable and debuggable in production environments.

## Metrics Collection

### Prometheus Metrics

```go
// Prometheus metrics for operator observability
package metrics

import (
    "github.com/prometheus/client_golang/api"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
    "sigs.k8s.io/controller-runtime/pkg/metrics"
)

// Custom metrics for the database operator
var (
    // Reconciliation metrics
    ReconciliationTotal = promauto.With(metrics.Registry).NewCounterVec(
        prometheus.CounterOpts{
            Name: "postgresql_operator_reconciliations_total",
            Help: "Total number of reconciliations performed",
        },
        []string{"database", "result"},
    )

    ReconciliationDuration = promauto.With(metrics.Registry).NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "postgresql_operator_reconciliation_duration_seconds",
            Help:    "Duration of reconciliation operations",
            Buckets: prometheus.DefBuckets,
        },
        []string{"database", "operation"},
    )

    // Resource metrics
    DatabaseCount = promauto.With(metrics.Registry).NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "postgresql_operator_databases_total",
            Help: "Total number of databases managed",
        },
        []string{"status", "engine", "version"},
    )

    ResourceUsage = promauto.With(metrics.Registry).NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "postgresql_operator_resource_usage",
            Help: "Resource usage metrics",
        },
        []string{"resource_type", "database"},
    )

    // Error metrics
    ErrorsTotal = promauto.With(metrics.Registry).NewCounterVec(
        prometheus.CounterOpts{
            Name: "postgresql_operator_errors_total",
            Help: "Total number of errors encountered",
        },
        []string{"error_type", "database"},
    )

    // API metrics
    APICallsTotal = promauto.With(metrics.Registry).NewCounterVec(
        prometheus.CounterOpts{
            Name: "postgresql_operator_api_calls_total",
            Help: "Total number of API calls made",
        },
        []string{"api", "method", "status"},
    )

    APICallDuration = promauto.With(metrics.Registry).NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "postgresql_operator_api_call_duration_seconds",
            Help:    "Duration of API calls",
            Buckets: []float64{0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0},
        },
        []string{"api", "method"},
    )
)

// Metrics collector for real-time updates
type MetricsCollector struct {
    reconciler *DatabaseReconciler
}

func NewMetricsCollector(r *DatabaseReconciler) *MetricsCollector {
    return &MetricsCollector{reconciler: r}
}

func (mc *MetricsCollector) RecordReconciliation(database string, success bool, duration float64) {
    result := "success"
    if !success {
        result = "failure"
    }

    ReconciliationTotal.WithLabelValues(database, result).Inc()
    ReconciliationDuration.WithLabelValues(database, "total").Observe(duration)
}

func (mc *MetricsCollector) UpdateDatabaseCount() {
    // Query all databases and update metrics
    databases := &postgresqlv1.DatabaseList{}
    if err := mc.reconciler.List(context.Background(), databases); err != nil {
        return
    }

    // Reset all gauges
    DatabaseCount.Reset()

    // Count by status, engine, version
    statusCount := make(map[string]int)
    engineCount := make(map[string]int)
    versionCount := make(map[string]int)

    for _, db := range databases.Items {
        status := string(db.Status.Phase)
        engine := db.Spec.Engine
        version := db.Spec.Version

        statusCount[status]++
        engineCount[engine]++
        versionCount[version]++
    }

    // Update metrics
    for status, count := range statusCount {
        DatabaseCount.WithLabelValues(status, "", "").Set(float64(count))
    }

    for engine, count := range engineCount {
        DatabaseCount.WithLabelValues("", engine, "").Set(float64(count))
    }

    for version, count := range versionCount {
        DatabaseCount.WithLabelValues("", "", version).Set(float64(count))
    }
}

func (mc *MetricsCollector) RecordAPIError(api string, method string, statusCode int) {
    status := "error"
    if statusCode >= 200 && statusCode < 400 {
        status = "success"
    } else if statusCode >= 400 && statusCode < 500 {
        status = "client_error"
    } else if statusCode >= 500 {
        status = "server_error"
    }

    APICallsTotal.WithLabelValues(api, method, status).Inc()
}

func (mc *MetricsCollector) RecordResourceUsage(database string, cpu float64, memory float64, storage float64) {
    ResourceUsage.WithLabelValues("cpu", database).Set(cpu)
    ResourceUsage.WithLabelValues("memory", database).Set(memory)
    ResourceUsage.WithLabelValues("storage", database).Set(storage)
}
```

### Metrics Integration in Controllers

```go
// Integrate metrics into controller reconciliation
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    startTime := time.Now()
    databaseName := req.Name

    defer func() {
        duration := time.Since(startTime).Seconds()
        success := recover() == nil // Simple success check

        // Record reconciliation metrics
        r.metricsCollector.RecordReconciliation(databaseName, success, duration)
    }()

    // Get database
    database := &postgresqlv1.Database{}
    if err := r.Get(ctx, req.NamespacedName, database); err != nil {
        if apierrors.IsNotFound(err) {
            return ctrl.Result{}, nil
        }
        ErrorsTotal.WithLabelValues("get_database", databaseName).Inc()
        return ctrl.Result{}, err
    }

    // Reconciliation logic with metrics
    if err := r.reconcileDatabase(ctx, database); err != nil {
        ErrorsTotal.WithLabelValues("reconciliation", databaseName).Inc()
        return ctrl.Result{}, err
    }

    // Update database count metrics
    r.metricsCollector.UpdateDatabaseCount()

    return ctrl.Result{}, nil
}

func (r *DatabaseReconciler) reconcileDatabase(ctx context.Context, database *postgresqlv1.Database) error {
    // PVC creation with metrics
    if err := r.ensurePVC(ctx, database); err != nil {
        return err
    }

    // Deployment creation with metrics
    if err := r.ensureDeployment(ctx, database); err != nil {
        return err
    }

    // Service creation with metrics
    if err := r.ensureService(ctx, database); err != nil {
        return err
    }

    // Record resource usage
    if err := r.recordResourceUsage(ctx, database); err != nil {
        // Log but don't fail reconciliation
        r.logger.Error(err, "Failed to record resource usage")
    }

    return nil
}

func (r *DatabaseReconciler) recordResourceUsage(ctx context.Context, database *postgresqlv1.Database) error {
    // Get deployment
    deployment := &appsv1.Deployment{}
    if err := r.Get(ctx, client.ObjectKey{
        Name:      r.getResourceName(database, "deployment"),
        Namespace: database.Namespace,
    }, deployment); err != nil {
        return err
    }

    // Get resource usage from deployment spec
    if len(deployment.Spec.Template.Spec.Containers) > 0 {
        container := deployment.Spec.Template.Spec.Containers[0]

        // Record CPU and memory requests/limits
        cpuUsage := 0.0
        memoryUsage := 0.0

        if container.Resources.Requests != nil {
            if cpu := container.Resources.Requests.Cpu(); cpu != nil {
                // Convert to cores (simplified)
                cpuUsage = float64(cpu.MilliValue()) / 1000.0
            }
            if memory := container.Resources.Requests.Memory(); memory != nil {
                memoryUsage = float64(memory.Value()) / (1024 * 1024 * 1024) // GB
            }
        }

        r.metricsCollector.RecordResourceUsage(
            database.Name,
            cpuUsage,
            memoryUsage,
            0.0, // Storage would need to be calculated separately
        )
    }

    return nil
}
```

## Structured Logging

### Logrus Integration

```go
// Structured logging with logrus
package logging

import (
    "context"
    "os"
    "runtime"
    "time"

    "github.com/sirupsen/logrus"
    "sigs.k8s.io/controller-runtime/pkg/log"
)

type LogrusLogger struct {
    *logrus.Logger
}

func NewLogrusLogger() *LogrusLogger {
    logger := logrus.New()

    // Set log level from environment
    level := os.Getenv("LOG_LEVEL")
    if level == "" {
        level = "info"
    }

    logLevel, err := logrus.ParseLevel(level)
    if err != nil {
        logLevel = logrus.InfoLevel
    }
    logger.SetLevel(logLevel)

    // JSON formatter for production
    logger.SetFormatter(&logrus.JSONFormatter{
        TimestampFormat: time.RFC3339,
        FieldMap: logrus.FieldMap{
            logrus.FieldKeyTime:  "timestamp",
            logrus.FieldKeyLevel: "level",
            logrus.FieldKeyMsg:   "message",
        },
    })

    // Output to stdout for containerized environments
    logger.SetOutput(os.Stdout)

    return &LogrusLogger{logger}
}

func (l *LogrusLogger) WithFields(fields map[string]interface{}) *LogrusLogger {
    return &LogrusLogger{l.WithFields(fields).Logger}
}

func (l *LogrusLogger) WithContext(ctx context.Context) *LogrusLogger {
    // Extract values from context
    requestID := ctx.Value("request_id")
    userID := ctx.Value("user_id")

    fields := make(map[string]interface{})

    if requestID != nil {
        fields["request_id"] = requestID
    }
    if userID != nil {
        fields["user_id"] = userID
    }

    return l.WithFields(fields)
}

func (l *LogrusLogger) WithDatabase(database string) *LogrusLogger {
    return l.WithFields(map[string]interface{}{
        "database": database,
        "component": "database_controller",
    })
}

// Convenience methods
func (l *LogrusLogger) Info(msg string, args ...interface{}) {
    if len(args) > 0 {
        l.Logger.Infof(msg, args...)
    } else {
        l.Logger.Info(msg)
    }
}

func (l *LogrusLogger) Error(msg string, err error, args ...interface{}) {
    fields := make(map[string]interface{})

    if err != nil {
        fields["error"] = err.Error()

        // Add stack trace for errors
        buf := make([]byte, 4096)
        n := runtime.Stack(buf, false)
        fields["stack_trace"] = string(buf[:n])
    }

    if len(args) > 0 {
        // Assume args are key-value pairs
        for i := 0; i < len(args); i += 2 {
            if i+1 < len(args) {
                fields[args[i].(string)] = args[i+1]
            }
        }
    }

    l.WithFields(fields).Logger.Error(msg)
}

func (l *LogrusLogger) DebugOperation(operation string, database string, duration time.Duration) {
    l.WithFields(map[string]interface{}{
        "operation": operation,
        "database":  database,
        "duration":  duration.String(),
        "duration_ms": duration.Milliseconds(),
    }).Logger.Debug("Operation completed")
}

// Global logger instance
var Logger = NewLogrusLogger()
```

### Context-Aware Logging

```go
// Context-aware logging in controllers
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    logger := Logger.WithContext(ctx).WithDatabase(req.Name)

    startTime := time.Now()
    defer func() {
        duration := time.Since(startTime)
        logger.DebugOperation("reconciliation", req.Name, duration)
    }()

    logger.Info("Starting reconciliation")

    // Get database
    database := &postgresqlv1.Database{}
    if err := r.Get(ctx, req.NamespacedName, database); err != nil {
        if apierrors.IsNotFound(err) {
            logger.Info("Database not found, ending reconciliation")
            return ctrl.Result{}, nil
        }
        logger.Error("Failed to get database", err, "namespace", req.Namespace)
        return ctrl.Result{}, err
    }

    // Reconciliation logic with detailed logging
    if err := r.reconcileDatabase(ctx, database, logger); err != nil {
        logger.Error("Reconciliation failed", err,
            "phase", string(database.Status.Phase),
            "replicas", database.Spec.Replicas)
        return ctrl.Result{}, err
    }

    logger.Info("Reconciliation completed successfully",
        "phase", string(database.Status.Phase),
        "ready", database.Status.Ready)

    return ctrl.Result{}, nil
}

func (r *DatabaseReconciler) reconcileDatabase(ctx context.Context, database *postgresqlv1.Database, logger *LogrusLogger) error {
    logger.Info("Ensuring PVC exists")
    if err := r.ensurePVC(ctx, database); err != nil {
        logger.Error("PVC creation failed", err)
        return err
    }
    logger.Info("PVC ready")

    logger.Info("Ensuring deployment exists")
    if err := r.ensureDeployment(ctx, database); err != nil {
        logger.Error("Deployment creation failed", err)
        return err
    }
    logger.Info("Deployment ready")

    logger.Info("Ensuring service exists")
    if err := r.ensureService(ctx, database); err != nil {
        logger.Error("Service creation failed", err)
        return err
    }
    logger.Info("Service ready")

    // Update resource usage metrics
    if err := r.updateResourceMetrics(ctx, database); err != nil {
        logger.Error("Failed to update resource metrics", err)
        // Don't fail reconciliation for metrics errors
    }

    return nil
}
```

## Distributed Tracing

### OpenTelemetry Integration

```go
// Distributed tracing with OpenTelemetry
package tracing

import (
    "context"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
    "go.opentelemetry.io/otel/trace"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
)

var Tracer trace.Tracer

func InitTracer(serviceName string) error {
    // Create Jaeger exporter
    exp, err := jaeger.New(jaeger.WithCollectorEndpoint())
    if err != nil {
        return err
    }

    // Create resource
    res, err := resource.New(context.Background(),
        resource.WithAttributes(
            semconv.ServiceNameKey.String(serviceName),
            semconv.ServiceVersionKey.String("1.0.0"),
        ),
    )
    if err != nil {
        return err
    }

    // Create tracer provider
    tp := trace.NewTracerProvider(
        trace.WithBatcher(exp),
        trace.WithResource(res),
    )

    otel.SetTracerProvider(tp)
    Tracer = tp.Tracer(serviceName)

    return nil
}

type TraceHelper struct {
    tracer trace.Tracer
}

func NewTraceHelper() *TraceHelper {
    return &TraceHelper{tracer: Tracer}
}

func (t *TraceHelper) StartReconciliationSpan(ctx context.Context, database string) (context.Context, trace.Span) {
    ctx, span := t.tracer.Start(ctx, "reconcile_database",
        trace.WithAttributes(
            attribute.String("database.name", database),
            attribute.String("operation.type", "reconciliation"),
        ),
    )
    return ctx, span
}

func (t *TraceHelper) StartOperationSpan(ctx context.Context, operation string, database string) (context.Context, trace.Span) {
    ctx, span := t.tracer.Start(ctx, operation,
        trace.WithAttributes(
            attribute.String("operation.name", operation),
            attribute.String("database.name", database),
        ),
    )
    return ctx, span
}

func (t *TraceHelper) RecordError(span trace.Span, err error) {
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
}

func (t *TraceHelper) RecordDuration(span trace.Span, duration time.Duration) {
    span.SetAttributes(
        attribute.Int64("operation.duration_ms", duration.Milliseconds()),
    )
}

// Global trace helper
var TraceHelperInstance = NewTraceHelper()
```

### Tracing Integration in Controllers

```go
// Integrate tracing into controller
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Start reconciliation span
    ctx, span := TraceHelperInstance.StartReconciliationSpan(ctx, req.Name)
    defer span.End()

    startTime := time.Now()
    defer func() {
        duration := time.Since(startTime)
        TraceHelperInstance.RecordDuration(span, duration)
    }()

    // Get database with tracing
    ctx, getSpan := TraceHelperInstance.StartOperationSpan(ctx, "get_database", req.Name)
    database := &postgresqlv1.Database{}
    err := r.Get(ctx, req.NamespacedName, database)
    getSpan.End()

    if err != nil {
        if apierrors.IsNotFound(err) {
            span.SetAttributes(attribute.Bool("database.found", false))
            return ctrl.Result{}, nil
        }
        TraceHelperInstance.RecordError(span, err)
        return ctrl.Result{}, err
    }

    span.SetAttributes(
        attribute.Bool("database.found", true),
        attribute.String("database.phase", string(database.Status.Phase)),
        attribute.Int32("database.replicas", database.Spec.Replicas),
    )

    // Reconciliation logic with tracing
    if err := r.reconcileWithTracing(ctx, database, span); err != nil {
        TraceHelperInstance.RecordError(span, err)
        return ctrl.Result{}, err
    }

    span.SetStatus(codes.Ok, "Reconciliation completed successfully")
    return ctrl.Result{}, nil
}

func (r *DatabaseReconciler) reconcileWithTracing(ctx context.Context, database *postgresqlv1.Database, parentSpan trace.Span) error {
    // PVC operation span
    ctx, pvcSpan := TraceHelperInstance.StartOperationSpan(ctx, "ensure_pvc", database.Name)
    err := r.ensurePVC(ctx, database)
    pvcSpan.End()

    if err != nil {
        TraceHelperInstance.RecordError(pvcSpan, err)
        return err
    }

    // Deployment operation span
    ctx, deploySpan := TraceHelperInstance.StartOperationSpan(ctx, "ensure_deployment", database.Name)
    err = r.ensureDeployment(ctx, database)
    deploySpan.End()

    if err != nil {
        TraceHelperInstance.RecordError(deploySpan, err)
        return err
    }

    // Service operation span
    ctx, svcSpan := TraceHelperInstance.StartOperationSpan(ctx, "ensure_service", database.Name)
    err = r.ensureService(ctx, database)
    svcSpan.End()

    if err != nil {
        TraceHelperInstance.RecordError(svcSpan, err)
        return err
    }

    return nil
}
```

## Debugging and Troubleshooting

### Debug Mode Configuration

```go
// Debug mode configuration
type DebugConfig struct {
    Enabled        bool          `json:"enabled"`
    LogLevel       string        `json:"logLevel"`
    TraceEnabled   bool          `json:"traceEnabled"`
    MetricsEnabled bool          `json:"metricsEnabled"`
    ProfileEnabled bool          `json:"profileEnabled"`
    DumpResources  bool          `json:"dumpResources"`
}

func (r *DatabaseReconciler) enableDebugMode() {
    r.debugConfig = &DebugConfig{
        Enabled:        true,
        LogLevel:       "debug",
        TraceEnabled:   true,
        MetricsEnabled: true,
        ProfileEnabled: true,
        DumpResources:  true,
    }

    // Set log level
    logrus.SetLevel(logrus.DebugLevel)

    // Enable profiling
    if r.debugConfig.ProfileEnabled {
        go r.startProfiling()
    }
}

func (r *DatabaseReconciler) startProfiling() {
    import _ "net/http/pprof"
    http.ListenAndServe("localhost:6060", nil)
}
```

### Resource Dumping for Debugging

```go
// Resource dumping for debugging
func (r *DatabaseReconciler) dumpResources(ctx context.Context, database *postgresqlv1.Database) error {
    if !r.debugConfig.DumpResources {
        return nil
    }

    logger := Logger.WithDatabase(database.Name)

    // Dump deployment
    deployment := &appsv1.Deployment{}
    if err := r.Get(ctx, client.ObjectKey{
        Name:      r.getResourceName(database, "deployment"),
        Namespace: database.Namespace,
    }, deployment); err == nil {
        logger.Debug("Current deployment state",
            "replicas", *deployment.Spec.Replicas,
            "ready_replicas", deployment.Status.ReadyReplicas,
            "available_replicas", deployment.Status.AvailableReplicas,
            "conditions", deployment.Status.Conditions)
    }

    // Dump service
    service := &corev1.Service{}
    if err := r.Get(ctx, client.ObjectKey{
        Name:      r.getResourceName(database, "service"),
        Namespace: database.Namespace,
    }, service); err == nil {
        logger.Debug("Current service state",
            "type", service.Spec.Type,
            "cluster_ip", service.Spec.ClusterIP,
            "ports", service.Spec.Ports)
    }

    // Dump PVC
    pvc := &corev1.PersistentVolumeClaim{}
    if err := r.Get(ctx, client.ObjectKey{
        Name:      r.getResourceName(database, "pvc"),
        Namespace: database.Namespace,
    }, pvc); err == nil {
        logger.Debug("Current PVC state",
            "status", pvc.Status.Phase,
            "capacity", pvc.Status.Capacity,
            "conditions", pvc.Status.Conditions)
    }

    return nil
}
```

### Health Checks and Diagnostics

```go
// Health checks and diagnostics
type HealthChecker struct {
    reconciler *DatabaseReconciler
}

func (hc *HealthChecker) RunDiagnostics(ctx context.Context, database *postgresqlv1.Database) *DiagnosticsReport {
    report := &DiagnosticsReport{
        Database: database.Name,
        Checks:   make(map[string]CheckResult),
    }

    // Check Kubernetes API connectivity
    report.Checks["api_connectivity"] = hc.checkAPIConnectivity(ctx)

    // Check resource existence
    report.Checks["deployment_exists"] = hc.checkResourceExists(ctx, database, "deployment")
    report.Checks["service_exists"] = hc.checkResourceExists(ctx, database, "service")
    report.Checks["pvc_exists"] = hc.checkResourceExists(ctx, database, "pvc")

    // Check resource health
    report.Checks["deployment_healthy"] = hc.checkDeploymentHealth(ctx, database)
    report.Checks["service_healthy"] = hc.checkServiceHealth(ctx, database)
    report.Checks["pvc_healthy"] = hc.checkPVCHHealth(ctx, database)

    // Calculate overall health
    report.OverallHealthy = hc.calculateOverallHealth(report.Checks)

    return report
}

type DiagnosticsReport struct {
    Database       string                 `json:"database"`
    Checks         map[string]CheckResult `json:"checks"`
    OverallHealthy bool                   `json:"overallHealthy"`
    Timestamp      time.Time              `json:"timestamp"`
}

type CheckResult struct {
    Status  string `json:"status"`  // "pass", "fail", "warn"
    Message string `json:"message"`
    Details string `json:"details,omitempty"`
}

func (hc *HealthChecker) checkAPIConnectivity(ctx context.Context) CheckResult {
    // Simple API connectivity check
    databases := &postgresqlv1.DatabaseList{}
    if err := hc.reconciler.List(ctx, databases); err != nil {
        return CheckResult{
            Status:  "fail",
            Message: "Cannot connect to Kubernetes API",
            Details: err.Error(),
        }
    }

    return CheckResult{
        Status:  "pass",
        Message: "Kubernetes API connection successful",
    }
}

func (hc *HealthChecker) checkResourceExists(ctx context.Context, database *postgresqlv1.Database, resourceType string) CheckResult {
    var obj client.Object
    var key client.ObjectKey

    switch resourceType {
    case "deployment":
        obj = &appsv1.Deployment{}
        key = client.ObjectKey{
            Name:      hc.reconciler.getResourceName(database, "deployment"),
            Namespace: database.Namespace,
        }
    case "service":
        obj = &corev1.Service{}
        key = client.ObjectKey{
            Name:      hc.reconciler.getResourceName(database, "service"),
            Namespace: database.Namespace,
        }
    case "pvc":
        obj = &corev1.PersistentVolumeClaim{}
        key = client.ObjectKey{
            Name:      hc.reconciler.getResourceName(database, "pvc"),
            Namespace: database.Namespace,
        }
    }

    if err := hc.reconciler.Get(ctx, key, obj); err != nil {
        if apierrors.IsNotFound(err) {
            return CheckResult{
                Status:  "fail",
                Message: fmt.Sprintf("%s resource not found", resourceType),
            }
        }
        return CheckResult{
            Status:  "fail",
            Message: fmt.Sprintf("Error checking %s resource", resourceType),
            Details: err.Error(),
        }
    }

    return CheckResult{
        Status:  "pass",
        Message: fmt.Sprintf("%s resource exists", resourceType),
    }
}

func (hc *HealthChecker) calculateOverallHealth(checks map[string]CheckResult) bool {
    for _, check := range checks {
        if check.Status == "fail" {
            return false
        }
    }
    return true
}
```

## Monitoring Dashboard

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "PostgreSQL Operator Dashboard",
    "tags": ["kubernetes", "operator", "postgresql"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Reconciliation Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(postgresql_operator_reconciliations_total[5m])",
            "legendFormat": "{{database}} - {{result}}"
          }
        ]
      },
      {
        "title": "Reconciliation Duration",
        "type": "heatmap",
        "targets": [
          {
            "expr": "postgresql_operator_reconciliation_duration_seconds",
            "legendFormat": "{{database}} - {{operation}}"
          }
        ]
      },
      {
        "title": "Database Status",
        "type": "table",
        "targets": [
          {
            "expr": "postgresql_operator_databases_total",
            "legendFormat": "{{status}} - {{engine}} {{version}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(postgresql_operator_errors_total[5m])",
            "legendFormat": "{{error_type}} - {{database}}"
          }
        ]
      }
    ]
  }
}
```

## Summary

In this chapter, we've covered:

- **Metrics Collection**: Prometheus metrics for reconciliation, resources, and errors
- **Structured Logging**: Logrus integration with context-aware logging
- **Distributed Tracing**: OpenTelemetry integration for request tracing
- **Debug Configuration**: Debug modes and resource dumping
- **Health Checks**: Comprehensive diagnostics and health monitoring
- **Monitoring Dashboards**: Grafana configurations for visualization

## Key Takeaways

1. **Metrics First**: Comprehensive metrics collection for operational visibility
2. **Structured Logging**: Consistent, searchable log formats with context
3. **Distributed Tracing**: End-to-end request tracing across services
4. **Debug Capabilities**: Built-in debugging tools for troubleshooting
5. **Health Monitoring**: Proactive health checks and diagnostics
6. **Visualization**: Dashboards for monitoring and alerting

Next, we'll explore **production deployment** - OLM installation, Helm charts, security, and scaling patterns.

---

**Ready for the next chapter?** [Chapter 8: Production Deployment](08-production-deployment.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `database`, `func`, `logger` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Observability & Debugging - Metrics, Logging, Tracing, and Troubleshooting` as an operating subsystem inside **Kubernetes Operator Patterns: Building Production-Grade Controllers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `metrics`, `Name`, `span` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Observability & Debugging - Metrics, Logging, Tracing, and Troubleshooting` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `database`.
2. **Input normalization**: shape incoming data so `func` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `logger`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `database` and `func` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Testing Operators - Unit Tests, Integration Tests, and envtest Framework](06-testing.md)
- [Next Chapter: Chapter 8: Production Deployment - OLM, Helm Charts, Security, and Scaling](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
