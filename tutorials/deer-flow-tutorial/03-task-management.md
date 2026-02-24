---
layout: default
title: "Chapter 3: Task Management"
parent: "Deer Flow Tutorial"
nav_order: 3
---

# Chapter 3: Task Management

Welcome to **Chapter 3: Task Management**. In this part of **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deep dive into task types, execution modes, and configuration options in Deer Flow.

## Overview

Tasks are the fundamental execution units in Deer Flow. Understanding the various task types and their configuration options is essential for building effective workflows.

## Task Architecture

### Task Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                      Task Lifecycle                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐   ┌──────────┐   ┌─────────┐   ┌──────────┐      │
│  │ CREATED │──▶│ SCHEDULED│──▶│ QUEUED  │──▶│ ASSIGNED │      │
│  └─────────┘   └──────────┘   └─────────┘   └──────────┘      │
│                                                    │            │
│                                                    ▼            │
│                                              ┌─────────┐        │
│                                              │ RUNNING │        │
│                                              └────┬────┘        │
│                         ┌────────────────────────┼────────┐     │
│                         ▼                        ▼        ▼     │
│                   ┌─────────┐              ┌─────────┐ ┌─────┐  │
│                   │ SUCCESS │              │ FAILED  │ │KILLED│  │
│                   └─────────┘              └────┬────┘ └─────┘  │
│                                                 │               │
│                                                 ▼               │
│                                            ┌─────────┐          │
│                                            │ RETRY   │          │
│                                            └─────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Task Components

```python
from deerflow import Task

class TaskDefinition:
    # Identity
    id: str                    # Unique task identifier
    name: str                  # Human-readable name
    type: str                  # Task type (shell, python, http, etc.)

    # Dependencies
    depends_on: List[str]      # Tasks that must complete first
    condition: str             # Conditional execution expression

    # Configuration
    config: Dict               # Task-type specific configuration
    timeout: int               # Maximum execution time
    retries: int               # Retry attempts on failure

    # Resources
    resources: Dict            # CPU, memory, etc.
    labels: Dict               # Metadata labels
```

## Built-in Task Types

### Shell Task

```python
from deerflow import ShellTask

task = ShellTask(
    id="run_script",
    command="python process.py --input ${input_file}",
    working_dir="/app/scripts",
    env={
        "PYTHONPATH": "/app/lib",
        "DEBUG": "true"
    },
    shell="/bin/bash",
    timeout=3600
)
```

```json
{
  "id": "shell_example",
  "type": "shell",
  "config": {
    "command": "python process.py",
    "working_dir": "/app",
    "env": {
      "ENV": "production"
    },
    "capture_output": true,
    "timeout": 3600
  }
}
```

### Python Task

```python
from deerflow import PythonTask

# Script-based
task = PythonTask(
    id="process_data",
    script="/app/scripts/process.py",
    function="main",
    args=["arg1", "arg2"],
    kwargs={"verbose": True},
    python_version="3.11",
    requirements=["pandas>=2.0", "numpy"]
)

# Inline function
@workflow.python_task(id="inline_task")
def process_records(input_data):
    import pandas as pd
    df = pd.DataFrame(input_data)
    return df.to_dict()
```

### HTTP Task

```python
from deerflow import HTTPTask

task = HTTPTask(
    id="call_api",
    method="POST",
    url="https://api.example.com/process",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer ${secrets.API_TOKEN}"
    },
    body={
        "data": "${tasks.previous.output}",
        "timestamp": "${now()}"
    },
    timeout=30,
    retry=RetryConfig(max_attempts=3, backoff="exponential")
)
```

### Docker Task

```python
from deerflow import DockerTask

task = DockerTask(
    id="containerized_job",
    image="myregistry/processor:latest",
    command=["python", "main.py"],
    volumes=[
        "/data:/app/data:ro",
        "/output:/app/output:rw"
    ],
    environment={
        "CONFIG_PATH": "/app/config.yaml"
    },
    resources={
        "memory": "4Gi",
        "cpu": "2",
        "gpu": "1"
    },
    pull_policy="IfNotPresent"
)
```

### Kubernetes Task

```python
from deerflow import KubernetesTask

task = KubernetesTask(
    id="k8s_job",
    namespace="workflows",
    pod_spec={
        "containers": [{
            "name": "worker",
            "image": "processor:latest",
            "resources": {
                "requests": {"memory": "1Gi", "cpu": "500m"},
                "limits": {"memory": "2Gi", "cpu": "1"}
            }
        }],
        "restartPolicy": "Never"
    },
    service_account="workflow-runner"
)
```

### SQL Task

```python
from deerflow import SQLTask

task = SQLTask(
    id="run_query",
    connection="postgres://user:pass@host:5432/db",
    query="""
        INSERT INTO results (date, count, total)
        SELECT
            CURRENT_DATE,
            COUNT(*),
            SUM(amount)
        FROM transactions
        WHERE date = '${params.date}'
    """,
    fetch_results=True
)
```

### Spark Task

```python
from deerflow import SparkTask

task = SparkTask(
    id="spark_etl",
    application="/app/jobs/etl_job.py",
    master="spark://spark-master:7077",
    deploy_mode="cluster",
    executor_memory="4g",
    executor_cores=2,
    num_executors=10,
    spark_conf={
        "spark.sql.shuffle.partitions": "200"
    },
    args=["--date", "${params.date}"]
)
```

## Custom Task Types

### Creating Custom Tasks

```python
from deerflow import TaskType, register_task_type

@register_task_type("my_custom")
class MyCustomTask(TaskType):
    """Custom task type for specific operations."""

    def __init__(self, config: dict):
        self.config = config

    def validate(self) -> bool:
        """Validate task configuration."""
        required = ["operation", "target"]
        return all(k in self.config for k in required)

    async def execute(self, context: TaskContext) -> TaskResult:
        """Execute the task."""
        operation = self.config["operation"]
        target = self.config["target"]

        # Perform custom logic
        result = await self._perform_operation(operation, target)

        return TaskResult(
            status="success",
            output=result
        )

    async def _perform_operation(self, op, target):
        # Implementation
        pass
```

### Using Custom Tasks

```json
{
  "id": "custom_operation",
  "type": "my_custom",
  "config": {
    "operation": "sync",
    "target": "s3://bucket/path"
  }
}
```

## Task Configuration

### Timeouts and Retries

```json
{
  "id": "resilient_task",
  "type": "http",
  "config": {
    "url": "https://api.example.com/endpoint"
  },
  "timeout": 300,
  "retry": {
    "max_attempts": 5,
    "initial_delay": 1,
    "max_delay": 60,
    "backoff": "exponential",
    "retry_on": ["timeout", "5xx"]
  }
}
```

### Resource Allocation

```json
{
  "id": "resource_intensive",
  "type": "docker",
  "config": {
    "image": "ml-model:latest"
  },
  "resources": {
    "cpu": "4",
    "memory": "16Gi",
    "gpu": {
      "count": 2,
      "type": "nvidia-tesla-v100"
    },
    "storage": {
      "size": "100Gi",
      "type": "ssd"
    }
  },
  "node_selector": {
    "node-type": "compute-optimized"
  }
}
```

### Environment and Secrets

```json
{
  "id": "secure_task",
  "type": "python",
  "config": {
    "script": "secure_process.py"
  },
  "env": {
    "LOG_LEVEL": "INFO",
    "CONFIG_PATH": "/etc/config"
  },
  "secrets": {
    "DB_PASSWORD": {
      "source": "vault",
      "path": "secret/data/db",
      "key": "password"
    },
    "API_KEY": {
      "source": "kubernetes",
      "name": "api-secrets",
      "key": "api-key"
    }
  }
}
```

## Task Execution Modes

### Sequential Execution

```json
{
  "tasks": [
    {"id": "step1", "type": "shell", "command": "echo Step 1"},
    {"id": "step2", "type": "shell", "command": "echo Step 2", "depends_on": ["step1"]},
    {"id": "step3", "type": "shell", "command": "echo Step 3", "depends_on": ["step2"]}
  ]
}
```

### Parallel Execution

```json
{
  "tasks": [
    {"id": "fetch_a", "type": "http", "config": {"url": "https://api.a.com"}},
    {"id": "fetch_b", "type": "http", "config": {"url": "https://api.b.com"}},
    {"id": "fetch_c", "type": "http", "config": {"url": "https://api.c.com"}},
    {
      "id": "combine",
      "type": "python",
      "depends_on": ["fetch_a", "fetch_b", "fetch_c"]
    }
  ]
}
```

### Dynamic Task Generation

```python
from deerflow import Workflow, DynamicTaskGroup

workflow = Workflow(name="dynamic_example")

@workflow.dynamic_tasks(id="process_files")
def generate_tasks(context):
    """Generate tasks based on runtime data."""
    files = context.params.get("files", [])

    tasks = []
    for i, file in enumerate(files):
        tasks.append({
            "id": f"process_{i}",
            "type": "python",
            "config": {
                "script": "process_file.py",
                "args": [file]
            }
        })

    return tasks
```

## Task Monitoring

### Logging

```python
from deerflow import TaskLogger

@workflow.task(id="logged_task")
def process_with_logging(context):
    logger = TaskLogger(context)

    logger.info("Starting processing")
    logger.debug(f"Parameters: {context.params}")

    try:
        result = do_work()
        logger.info(f"Completed with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise
```

### Metrics

```python
from deerflow import TaskMetrics

@workflow.task(id="metrics_task")
def process_with_metrics(context):
    metrics = TaskMetrics(context)

    with metrics.timer("processing_time"):
        records = fetch_records()

    metrics.gauge("records_fetched", len(records))

    processed = 0
    for record in records:
        process(record)
        processed += 1
        metrics.counter("records_processed")

    return {"processed": processed}
```

## Summary

In this chapter, you've learned:

- **Task Architecture**: Lifecycle and components
- **Built-in Types**: Shell, Python, HTTP, Docker, K8s, SQL, Spark
- **Custom Tasks**: Creating your own task types
- **Configuration**: Timeouts, retries, resources, secrets
- **Execution Modes**: Sequential, parallel, dynamic
- **Monitoring**: Logging and metrics

## Key Takeaways

1. **Choose Right Type**: Match task type to the job
2. **Configure Resources**: Allocate appropriate resources
3. **Handle Failures**: Use retries and timeouts
4. **Secure Secrets**: Use proper secret management
5. **Monitor Everything**: Log and metric all tasks

## Next Steps

Ready to learn about complex task dependencies? Let's explore Chapter 4.

---

**Ready for Chapter 4?** [Dependencies](04-dependencies.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `config`, `task`, `deerflow` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Task Management` as an operating subsystem inside **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `self`, `context`, `python` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Task Management` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `config`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
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
- search upstream code for `config` and `task` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Workflow Basics](02-workflow-basics.md)
- [Next Chapter: Chapter 4: Dependencies](04-dependencies.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
