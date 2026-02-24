---
layout: default
title: "Chapter 7: Monitoring"
parent: "Deer Flow Tutorial"
nav_order: 7
---

# Chapter 7: Monitoring

Welcome to **Chapter 7: Monitoring**. In this part of **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement comprehensive monitoring and observability for Deer Flow workflows.

## Overview

Effective monitoring is crucial for maintaining reliable workflows. This chapter covers metrics collection, logging, tracing, alerting, and dashboard creation for Deer Flow.

## Metrics Collection

### Built-in Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                    Deer Flow Metrics                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Workflow Metrics:                                              │
│  • deerflow_workflows_total{status}                             │
│  • deerflow_workflow_duration_seconds{workflow}                 │
│  • deerflow_workflows_active                                    │
│                                                                 │
│  Task Metrics:                                                  │
│  • deerflow_tasks_total{type, status}                          │
│  • deerflow_task_duration_seconds{type}                        │
│  • deerflow_task_retries_total{type}                           │
│  • deerflow_tasks_queued                                        │
│                                                                 │
│  Worker Metrics:                                                │
│  • deerflow_workers_active                                      │
│  • deerflow_worker_utilization{worker}                         │
│  • deerflow_worker_tasks_processed{worker}                     │
│                                                                 │
│  System Metrics:                                                │
│  • deerflow_queue_depth{queue}                                 │
│  • deerflow_scheduler_lag_seconds                              │
│  • deerflow_api_requests_total{endpoint, status}               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Prometheus Integration

```yaml
# config/metrics.yaml
metrics:
  enabled: true
  port: 9090
  path: /metrics

  prometheus:
    scrape_interval: 15s
    labels:
      environment: production
      service: deerflow

  custom_metrics:
    - name: data_processed_bytes
      type: counter
      description: "Total bytes processed"
      labels: [workflow, task]

    - name: processing_latency
      type: histogram
      description: "Processing latency distribution"
      buckets: [0.1, 0.5, 1, 5, 10, 30, 60]
```

### Custom Metrics

```python
from deerflow import Workflow
from deerflow.metrics import Counter, Histogram, Gauge

# Define custom metrics
records_processed = Counter(
    'deerflow_records_processed_total',
    'Total records processed',
    ['workflow', 'task', 'status']
)

processing_time = Histogram(
    'deerflow_processing_time_seconds',
    'Time to process records',
    ['workflow', 'task'],
    buckets=[0.1, 0.5, 1, 5, 10, 30]
)

active_connections = Gauge(
    'deerflow_active_connections',
    'Number of active database connections',
    ['database']
)

workflow = Workflow(name="instrumented_workflow")

@workflow.task(id="process_records")
def process_records(context):
    with processing_time.labels(
        workflow=context.workflow.name,
        task=context.task.id
    ).time():
        records = fetch_records()

        for record in records:
            try:
                process(record)
                records_processed.labels(
                    workflow=context.workflow.name,
                    task=context.task.id,
                    status="success"
                ).inc()
            except Exception:
                records_processed.labels(
                    workflow=context.workflow.name,
                    task=context.task.id,
                    status="error"
                ).inc()
```

## Logging

### Structured Logging

```python
from deerflow.logging import get_logger

logger = get_logger(__name__)

@workflow.task(id="logged_task")
def logged_task(context):
    logger.info(
        "Starting task processing",
        extra={
            "workflow_id": context.workflow.id,
            "task_id": context.task.id,
            "execution_id": context.execution.id,
            "params": context.params
        }
    )

    try:
        result = process_data()
        logger.info(
            "Task completed successfully",
            extra={
                "result_count": len(result),
                "duration_ms": context.elapsed_ms
            }
        )
        return result
    except Exception as e:
        logger.error(
            "Task failed",
            extra={"error": str(e)},
            exc_info=True
        )
        raise
```

### Log Configuration

```yaml
# config/logging.yaml
logging:
  level: INFO
  format: json

  handlers:
    console:
      enabled: true
      level: INFO

    file:
      enabled: true
      path: /var/log/deerflow/app.log
      rotation: daily
      retention: 30d

    elasticsearch:
      enabled: true
      hosts:
        - http://elasticsearch:9200
      index: deerflow-logs-{date}

  filters:
    - name: sensitive_data
      action: redact
      patterns:
        - "password"
        - "api_key"
        - "secret"
```

### Log Aggregation

```yaml
# fluent-bit/config.yaml
[INPUT]
    Name              tail
    Path              /var/log/deerflow/*.log
    Parser            json
    Tag               deerflow.*

[FILTER]
    Name              modify
    Match             deerflow.*
    Add               cluster ${CLUSTER_NAME}
    Add               environment ${ENVIRONMENT}

[OUTPUT]
    Name              es
    Match             deerflow.*
    Host              elasticsearch
    Port              9200
    Index             deerflow-logs
    Type              _doc
```

## Distributed Tracing

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from deerflow.tracing import DeerFlowInstrumentor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Instrument Deer Flow
DeerFlowInstrumentor().instrument()

# Custom spans
tracer = trace.get_tracer(__name__)

@workflow.task(id="traced_task")
def traced_task(context):
    with tracer.start_as_current_span("process_batch") as span:
        span.set_attribute("batch_size", 100)

        for i in range(100):
            with tracer.start_as_current_span(f"process_item_{i}"):
                process_item(i)

        span.set_attribute("items_processed", 100)
```

### Trace Context Propagation

```python
from deerflow.tracing import inject_context, extract_context

@workflow.task(id="upstream")
def upstream_task(context):
    # Inject trace context for downstream
    headers = {}
    inject_context(headers)

    # Pass to external service
    response = requests.post(
        "https://api.example.com/process",
        headers=headers,
        json={"data": "..."}
    )
    return response.json()

@workflow.task(id="downstream")
def downstream_task(context):
    # Extract context from upstream
    parent_context = extract_context(context.input.headers)

    with tracer.start_as_current_span("downstream", context=parent_context):
        # Continue trace
        pass
```

## Dashboards

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Deer Flow Overview",
    "panels": [
      {
        "title": "Workflow Executions",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(deerflow_workflows_total[5m])) by (status)",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "title": "Task Queue Depth",
        "type": "gauge",
        "targets": [
          {
            "expr": "deerflow_tasks_queued",
            "legendFormat": "Queued Tasks"
          }
        ]
      },
      {
        "title": "Worker Utilization",
        "type": "heatmap",
        "targets": [
          {
            "expr": "deerflow_worker_utilization",
            "legendFormat": "{{worker}}"
          }
        ]
      },
      {
        "title": "P95 Task Duration",
        "type": "stat",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(deerflow_task_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

### Key Metrics Dashboard

```yaml
# Dashboard panels
panels:
  - name: Workflow Success Rate
    query: |
      sum(rate(deerflow_workflows_total{status="success"}[1h]))
      /
      sum(rate(deerflow_workflows_total[1h])) * 100
    thresholds:
      critical: 95
      warning: 99

  - name: Average Task Duration
    query: |
      avg(rate(deerflow_task_duration_seconds_sum[5m])
      /
      rate(deerflow_task_duration_seconds_count[5m]))

  - name: Queue Wait Time
    query: |
      histogram_quantile(0.95,
        rate(deerflow_task_queue_time_seconds_bucket[5m]))

  - name: Error Rate
    query: |
      sum(rate(deerflow_tasks_total{status="failed"}[5m]))
      /
      sum(rate(deerflow_tasks_total[5m])) * 100
```

## Alerting

### Alert Rules

```yaml
# prometheus/alerts.yaml
groups:
  - name: deerflow
    rules:
      - alert: HighWorkflowFailureRate
        expr: |
          sum(rate(deerflow_workflows_total{status="failed"}[5m]))
          /
          sum(rate(deerflow_workflows_total[5m])) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High workflow failure rate"
          description: "Failure rate is {{ $value | humanizePercentage }}"

      - alert: TaskQueueBacklog
        expr: deerflow_tasks_queued > 1000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Task queue backlog"
          description: "{{ $value }} tasks in queue"

      - alert: WorkerPoolExhausted
        expr: deerflow_workers_active / deerflow_workers_total > 0.95
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Worker pool near capacity"

      - alert: SchedulerLag
        expr: deerflow_scheduler_lag_seconds > 60
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Scheduler lag detected"
          description: "Lag is {{ $value }} seconds"
```

### Notification Channels

```yaml
# config/notifications.yaml
notifications:
  channels:
    slack:
      webhook: https://hooks.slack.com/services/...
      channel: "#deerflow-alerts"
      templates:
        critical: |
          :rotating_light: *CRITICAL ALERT*
          *Alert:* {{ .AlertName }}
          *Description:* {{ .Description }}
          *Value:* {{ .Value }}

    pagerduty:
      service_key: ${PAGERDUTY_KEY}
      severity_mapping:
        critical: critical
        warning: warning
        info: info

    email:
      smtp_host: smtp.example.com
      from: alerts@example.com
      to:
        - oncall@example.com

  routing:
    - match:
        severity: critical
      channels: [pagerduty, slack]

    - match:
        severity: warning
      channels: [slack]

    - match:
        severity: info
      channels: [email]
```

## Health Checks

### Endpoint Configuration

```python
from deerflow.health import HealthCheck, health_check

app = HealthCheck()

@health_check("database")
async def check_database():
    async with get_db_connection() as conn:
        await conn.execute("SELECT 1")
    return {"status": "healthy", "latency_ms": 5}

@health_check("queue")
async def check_queue():
    depth = await get_queue_depth()
    return {
        "status": "healthy" if depth < 10000 else "degraded",
        "queue_depth": depth
    }

@health_check("scheduler")
async def check_scheduler():
    lag = await get_scheduler_lag()
    return {
        "status": "healthy" if lag < 30 else "unhealthy",
        "lag_seconds": lag
    }

# Endpoints
# GET /health - Overall health
# GET /health/live - Liveness (is the process running)
# GET /health/ready - Readiness (can accept traffic)
```

## Summary

In this chapter, you've learned:

- **Metrics Collection**: Prometheus integration and custom metrics
- **Logging**: Structured logging and aggregation
- **Tracing**: Distributed tracing with OpenTelemetry
- **Dashboards**: Grafana dashboard creation
- **Alerting**: Alert rules and notifications
- **Health Checks**: Liveness and readiness probes

## Key Takeaways

1. **Instrument Everything**: Metrics for all operations
2. **Structured Logs**: JSON for easy querying
3. **Distributed Tracing**: Follow requests across services
4. **Meaningful Dashboards**: Focus on key indicators
5. **Actionable Alerts**: Alert on symptoms, not noise

## Next Steps

Ready to explore advanced orchestration patterns? Let's dive into Chapter 8.

---

**Ready for Chapter 8?** [Advanced Patterns](08-advanced-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `context`, `workflow`, `deerflow` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Monitoring` as an operating subsystem inside **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `task`, `status`, `rate` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Monitoring` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `context`.
2. **Input normalization**: shape incoming data so `workflow` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `deerflow`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Official Documentation](https://github.com/bytedance/deer-flow/tree/main/docs)
  Why it matters: authoritative reference on `Official Documentation` (github.com).
- [GitHub Repository](https://github.com/bytedance/deer-flow)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [API Reference](https://github.com/bytedance/deer-flow/blob/main/docs/API.md)
  Why it matters: authoritative reference on `API Reference` (github.com).
- [Community & Issues](https://github.com/bytedance/deer-flow/issues)
  Why it matters: authoritative reference on `Community & Issues` (github.com).
- [Workflow Examples](https://github.com/bytedance/deer-flow/tree/main/examples)
  Why it matters: authoritative reference on `Workflow Examples` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `context` and `workflow` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Scaling](06-scaling.md)
- [Next Chapter: Chapter 8: Advanced Patterns](08-advanced-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
