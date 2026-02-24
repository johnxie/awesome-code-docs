---
layout: default
title: "Chapter 5: Error Handling"
parent: "Deer Flow Tutorial"
nav_order: 5
---

# Chapter 5: Error Handling

Welcome to **Chapter 5: Error Handling**. In this part of **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement fault-tolerant workflows with retries, fallbacks, and recovery mechanisms.

## Overview

Production workflows must handle failures gracefully. Deer Flow provides comprehensive error handling mechanisms including retries, fallbacks, timeouts, and alerting to ensure workflow reliability.

## Retry Mechanisms

### Basic Retry Configuration

```json
{
  "id": "retryable_task",
  "type": "http",
  "config": {
    "url": "https://api.example.com/data"
  },
  "retry": {
    "max_attempts": 3,
    "delay": 5
  }
}
```

### Exponential Backoff

```json
{
  "id": "backoff_task",
  "type": "http",
  "config": {
    "url": "https://api.example.com/data"
  },
  "retry": {
    "max_attempts": 5,
    "initial_delay": 1,
    "max_delay": 60,
    "backoff": "exponential",
    "multiplier": 2
  }
}
```

```
Attempt 1: immediate
Attempt 2: wait 1s
Attempt 3: wait 2s
Attempt 4: wait 4s
Attempt 5: wait 8s (capped at max_delay)
```

### Retry Conditions

```json
{
  "id": "conditional_retry",
  "type": "http",
  "config": {
    "url": "https://api.example.com/data"
  },
  "retry": {
    "max_attempts": 3,
    "retry_on": {
      "exceptions": ["TimeoutError", "ConnectionError"],
      "status_codes": [429, 500, 502, 503, 504],
      "conditions": ["${output.retry_requested == true}"]
    },
    "no_retry_on": {
      "exceptions": ["AuthenticationError"],
      "status_codes": [400, 401, 403, 404]
    }
  }
}
```

### Python Retry Decorator

```python
from deerflow import Workflow, retry

workflow = Workflow(name="retry_example")

@workflow.task(id="flaky_operation")
@retry(
    max_attempts=3,
    backoff="exponential",
    retry_on=[TimeoutError, ConnectionError]
)
def flaky_operation(context):
    # This will be retried on failure
    response = make_api_call()
    return response
```

## Timeout Management

### Task Timeouts

```json
{
  "id": "bounded_task",
  "type": "python",
  "config": {
    "script": "long_running.py"
  },
  "timeout": {
    "execution": 3600,
    "idle": 300,
    "queue": 600
  }
}
```

- **execution**: Maximum total execution time
- **idle**: Maximum time without output
- **queue**: Maximum time waiting in queue

### Workflow Timeouts

```json
{
  "name": "timed_workflow",
  "timeout": 7200,
  "tasks": [
    {"id": "task1", "timeout": 1800, "...": "..."},
    {"id": "task2", "timeout": 1800, "...": "..."},
    {"id": "task3", "timeout": 1800, "...": "..."}
  ]
}
```

### Handling Timeouts

```python
from deerflow import Workflow, TimeoutError

@workflow.task(id="timeout_aware")
def process_with_timeout(context):
    try:
        result = long_operation()
        return result
    except TimeoutError:
        # Save partial progress
        save_checkpoint(context.checkpoint_path)
        raise
```

## Fallback Strategies

### Task-Level Fallbacks

```json
{
  "id": "primary_task",
  "type": "http",
  "config": {
    "url": "https://primary-api.com/data"
  },
  "fallback": {
    "task": {
      "type": "http",
      "config": {
        "url": "https://backup-api.com/data"
      }
    }
  }
}
```

### Cascading Fallbacks

```json
{
  "id": "resilient_fetch",
  "type": "http",
  "config": {"url": "https://api1.example.com"},
  "fallbacks": [
    {
      "type": "http",
      "config": {"url": "https://api2.example.com"}
    },
    {
      "type": "http",
      "config": {"url": "https://api3.example.com"}
    },
    {
      "type": "python",
      "config": {
        "script": "load_cached_data.py"
      }
    }
  ]
}
```

### Default Values

```python
from deerflow import Workflow, fallback_value

@workflow.task(id="with_default")
@fallback_value({"status": "unknown", "data": []})
def fetch_data(context):
    # If this fails, return the default value
    return fetch_from_api()
```

## Error Callbacks

### On Failure Handlers

```json
{
  "id": "monitored_task",
  "type": "python",
  "config": {"script": "process.py"},
  "on_failure": {
    "tasks": [
      {
        "id": "send_alert",
        "type": "http",
        "config": {
          "method": "POST",
          "url": "https://alerts.example.com/webhook",
          "body": {
            "message": "Task ${task.id} failed",
            "error": "${task.error}",
            "workflow": "${workflow.name}"
          }
        }
      },
      {
        "id": "cleanup",
        "type": "shell",
        "command": "rm -rf /tmp/task_${task.id}/*"
      }
    ]
  }
}
```

### Workflow-Level Handlers

```json
{
  "name": "monitored_workflow",
  "on_failure": {
    "notify": {
      "type": "slack",
      "channel": "#alerts",
      "message": "Workflow ${workflow.name} failed: ${workflow.error}"
    },
    "cleanup": {
      "type": "shell",
      "command": "cleanup.sh ${execution.id}"
    }
  },
  "on_success": {
    "notify": {
      "type": "slack",
      "channel": "#success",
      "message": "Workflow ${workflow.name} completed successfully"
    }
  },
  "tasks": [...]
}
```

### Python Callbacks

```python
from deerflow import Workflow, on_failure, on_success

workflow = Workflow(name="callback_example")

@workflow.on_failure
def handle_workflow_failure(context, error):
    send_alert(
        channel="#alerts",
        message=f"Workflow failed: {error}",
        execution_id=context.execution_id
    )
    cleanup_resources(context)

@workflow.on_success
def handle_workflow_success(context):
    update_dashboard(context.execution_id, status="success")

@workflow.task(id="risky_task")
@on_failure(lambda ctx, err: log_failure(ctx, err))
def risky_task(context):
    # Task implementation
    pass
```

## Circuit Breaker Pattern

### Implementation

```python
from deerflow import Workflow, CircuitBreaker

workflow = Workflow(name="circuit_breaker_example")

# Configure circuit breaker
breaker = CircuitBreaker(
    failure_threshold=5,      # Open after 5 failures
    reset_timeout=60,         # Try again after 60s
    half_open_requests=3      # Test with 3 requests
)

@workflow.task(id="protected_call")
@breaker.protect
def call_external_service(context):
    response = requests.get("https://unreliable-api.com")
    return response.json()
```

### Circuit States

```
┌─────────────────────────────────────────────────────────────────┐
│                   Circuit Breaker States                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    failures >= threshold    ┌─────────┐           │
│  │ CLOSED  │ ───────────────────────────▶│  OPEN   │           │
│  │(normal) │                             │ (fail   │           │
│  └────┬────┘                             │  fast)  │           │
│       │                                  └────┬────┘           │
│       │ success                               │                 │
│       │                                       │ timeout         │
│       │                                       ▼                 │
│       │                              ┌────────────────┐         │
│       │                              │   HALF-OPEN    │         │
│       │                              │ (test requests)│         │
│       │                              └────────┬───────┘         │
│       │                                       │                 │
│       │                    success ──────────┘                 │
│       │                                       │                 │
│       └───────────────────────────────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Dead Letter Queue

### Configuration

```json
{
  "name": "dlq_workflow",
  "dead_letter_queue": {
    "enabled": true,
    "queue": "workflow-dlq",
    "retention": "7d",
    "include_context": true
  },
  "tasks": [...]
}
```

### Processing Failed Tasks

```python
from deerflow import DLQProcessor

processor = DLQProcessor(queue="workflow-dlq")

# List failed tasks
failed = processor.list(
    workflow="my_workflow",
    since="2024-01-01"
)

# Retry a specific failure
processor.retry(failure_id="abc123")

# Retry all failures for a workflow
processor.retry_all(workflow="my_workflow")

# Purge old failures
processor.purge(older_than="7d")
```

## Recovery and Checkpoints

### Checkpoint System

```python
from deerflow import Workflow, checkpoint

workflow = Workflow(name="checkpoint_example")

@workflow.task(id="long_process")
@checkpoint(interval=100)  # Checkpoint every 100 items
def process_large_dataset(context):
    dataset = load_dataset()

    # Resume from checkpoint if exists
    start_idx = context.checkpoint.get("last_index", 0)

    for i, item in enumerate(dataset[start_idx:], start=start_idx):
        process_item(item)

        # Save checkpoint periodically
        if i % 100 == 0:
            context.save_checkpoint({"last_index": i})

    return {"processed": len(dataset)}
```

### Workflow Resume

```bash
# Resume failed workflow from last checkpoint
deerflow resume execution_id

# Resume from specific task
deerflow resume execution_id --from-task task_id

# Resume with modified parameters
deerflow resume execution_id --param key=new_value
```

## Alerting and Notifications

### Alert Configuration

```yaml
# config/alerts.yaml
alerts:
  channels:
    slack:
      webhook_url: https://hooks.slack.com/...
      default_channel: "#workflow-alerts"

    email:
      smtp_host: smtp.example.com
      from_address: alerts@example.com
      recipients:
        - team@example.com

    pagerduty:
      api_key: ${PAGERDUTY_KEY}
      service_id: P123ABC

  rules:
    - name: critical_failure
      condition: "workflow.status == 'failed' && workflow.tags.critical"
      channels: [slack, pagerduty]
      severity: critical

    - name: task_timeout
      condition: "task.status == 'timeout'"
      channels: [slack]
      severity: warning

    - name: retry_exhausted
      condition: "task.retries_exhausted"
      channels: [email]
      severity: high
```

## Summary

In this chapter, you've learned:

- **Retries**: Basic, exponential backoff, conditional
- **Timeouts**: Task and workflow level
- **Fallbacks**: Task fallbacks and defaults
- **Callbacks**: Failure and success handlers
- **Circuit Breaker**: Protect against cascading failures
- **Recovery**: Checkpoints and workflow resume
- **Alerting**: Notifications for failures

## Key Takeaways

1. **Retry Intelligently**: Use backoff and conditions
2. **Set Timeouts**: Prevent infinite waits
3. **Plan Fallbacks**: Have alternatives ready
4. **Checkpoint Progress**: Enable partial recovery
5. **Alert Early**: Catch failures before impact

## Next Steps

Ready to scale your workflows? Let's explore distributed execution in Chapter 6.

---

**Ready for Chapter 6?** [Scaling](06-scaling.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `workflow`, `task`, `context` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Error Handling` as an operating subsystem inside **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `config`, `Workflow`, `name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Error Handling` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `workflow`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `context`.
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
- search upstream code for `workflow` and `task` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Dependencies](04-dependencies.md)
- [Next Chapter: Chapter 6: Scaling](06-scaling.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
