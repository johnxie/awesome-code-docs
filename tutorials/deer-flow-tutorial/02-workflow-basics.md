---
layout: default
title: "Chapter 2: Workflow Basics"
parent: "Deer Flow Tutorial"
nav_order: 2
---

# Chapter 2: Workflow Basics

> Learn to create and manage basic workflows with Deer Flow's workflow definition system.

## Overview

Workflows are the core abstraction in Deer Flow. They define a series of tasks, their relationships, and execution parameters. This chapter covers fundamental workflow concepts and creation patterns.

## Workflow Structure

### Anatomy of a Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      Deer Flow Workflow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Workflow Metadata                     │   │
│  │  - Name, ID, Description                                 │   │
│  │  - Version, Tags, Labels                                 │   │
│  │  - Schedule, Triggers                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Task Definitions                     │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐               │   │
│  │  │ Task A  │──▶│ Task B  │──▶│ Task C  │               │   │
│  │  └─────────┘   └─────────┘   └─────────┘               │   │
│  │       │                            │                     │   │
│  │       └────────────┬───────────────┘                     │   │
│  │                    ▼                                     │   │
│  │              ┌─────────┐                                 │   │
│  │              │ Task D  │                                 │   │
│  │              └─────────┘                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Execution Configuration                 │   │
│  │  - Retry policies, Timeouts                              │   │
│  │  - Resource requirements                                 │   │
│  │  - Notifications, Callbacks                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow Definition Format

```json
{
  "name": "data_pipeline",
  "version": "1.0.0",
  "description": "Daily data processing pipeline",
  "metadata": {
    "owner": "data-team",
    "tags": ["etl", "daily"]
  },
  "tasks": [
    {
      "id": "extract",
      "type": "python",
      "config": {
        "script": "extract_data.py"
      }
    },
    {
      "id": "transform",
      "type": "python",
      "depends_on": ["extract"],
      "config": {
        "script": "transform_data.py"
      }
    },
    {
      "id": "load",
      "type": "python",
      "depends_on": ["transform"],
      "config": {
        "script": "load_data.py"
      }
    }
  ],
  "schedule": "0 2 * * *"
}
```

## Creating Workflows

### Using the CLI

```bash
# Create workflow from file
deerflow create -f workflow.json

# Create workflow with inline definition
deerflow create --name "my_workflow" \
    --task "step1:shell:echo Hello" \
    --task "step2:shell:echo World" \
    --depends "step2:step1"

# List workflows
deerflow list

# Get workflow details
deerflow get my_workflow

# Delete workflow
deerflow delete my_workflow
```

### Using the Python SDK

```python
from deerflow import Workflow, Task, ShellTask, PythonTask

# Create workflow
workflow = Workflow(
    name="data_pipeline",
    description="Daily data processing"
)

# Add tasks
extract = ShellTask(
    id="extract",
    command="python extract.py"
)

transform = PythonTask(
    id="transform",
    script="transform.py",
    depends_on=["extract"]
)

load = PythonTask(
    id="load",
    script="load.py",
    depends_on=["transform"]
)

workflow.add_tasks([extract, transform, load])

# Register workflow
workflow.register()
```

### Using the REST API

```bash
# Create workflow via API
curl -X POST http://localhost:8080/api/workflows \
    -H "Content-Type: application/json" \
    -d '{
        "name": "api_workflow",
        "tasks": [
            {"id": "task1", "type": "shell", "command": "echo Hello"}
        ]
    }'

# Get workflow
curl http://localhost:8080/api/workflows/api_workflow

# Update workflow
curl -X PUT http://localhost:8080/api/workflows/api_workflow \
    -H "Content-Type: application/json" \
    -d @updated_workflow.json
```

## Task Types

### Shell Tasks

```json
{
  "id": "shell_task",
  "type": "shell",
  "config": {
    "command": "python script.py",
    "working_dir": "/app/scripts",
    "env": {
      "ENV_VAR": "value"
    },
    "timeout": 3600
  }
}
```

### Python Tasks

```json
{
  "id": "python_task",
  "type": "python",
  "config": {
    "script": "process_data.py",
    "function": "main",
    "args": ["arg1", "arg2"],
    "kwargs": {"key": "value"},
    "requirements": ["pandas", "numpy"]
  }
}
```

### HTTP Tasks

```json
{
  "id": "api_call",
  "type": "http",
  "config": {
    "method": "POST",
    "url": "https://api.example.com/webhook",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    },
    "body": {
      "data": "${task.previous.output}"
    },
    "timeout": 30,
    "retry": {
      "max_attempts": 3,
      "backoff": "exponential"
    }
  }
}
```

### Docker Tasks

```json
{
  "id": "docker_task",
  "type": "docker",
  "config": {
    "image": "python:3.11",
    "command": ["python", "script.py"],
    "volumes": [
      "/data:/app/data"
    ],
    "environment": {
      "ENV": "production"
    },
    "resources": {
      "memory": "2Gi",
      "cpu": "1"
    }
  }
}
```

## Workflow Execution

### Running Workflows

```bash
# Run workflow immediately
deerflow run my_workflow

# Run with parameters
deerflow run my_workflow --param date=2024-01-15 --param env=prod

# Run specific tasks only
deerflow run my_workflow --task transform --task load

# Dry run (validate without executing)
deerflow run my_workflow --dry-run
```

### Execution States

```
┌─────────────────────────────────────────────────────────────────┐
│                   Workflow Execution States                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│  │ PENDING │──▶│ RUNNING │──▶│ SUCCESS │   │         │        │
│  └─────────┘   └────┬────┘   └─────────┘   │         │        │
│                     │                       │ SKIPPED │        │
│                     ▼                       │         │        │
│               ┌─────────┐                  └─────────┘        │
│               │ FAILED  │                                      │
│               └────┬────┘                                      │
│                    │                                           │
│                    ▼                                           │
│               ┌─────────┐   ┌─────────┐                       │
│               │ RETRY   │──▶│ SUCCESS │                       │
│               └─────────┘   │ /FAILED │                       │
│                             └─────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Monitoring Execution

```bash
# Watch execution in real-time
deerflow watch execution_id

# Get execution status
deerflow status execution_id

# Get execution logs
deerflow logs execution_id
deerflow logs execution_id --task transform

# List recent executions
deerflow executions --workflow my_workflow --limit 10
```

## Input and Output

### Task Parameters

```json
{
  "id": "parameterized_task",
  "type": "python",
  "config": {
    "script": "process.py",
    "args": [
      "${params.date}",
      "${params.environment}"
    ]
  }
}
```

### Passing Data Between Tasks

```json
{
  "tasks": [
    {
      "id": "fetch_data",
      "type": "python",
      "config": {
        "script": "fetch.py"
      },
      "outputs": ["data_path", "record_count"]
    },
    {
      "id": "process_data",
      "type": "python",
      "depends_on": ["fetch_data"],
      "config": {
        "script": "process.py",
        "args": [
          "${tasks.fetch_data.outputs.data_path}"
        ]
      }
    }
  ]
}
```

### Using Python SDK for Data Flow

```python
from deerflow import Workflow, PythonTask, Output

workflow = Workflow(name="data_flow_example")

@workflow.task(id="producer")
def produce_data():
    data = {"records": 100, "file": "/tmp/data.csv"}
    return Output(data)

@workflow.task(id="consumer", depends_on=["producer"])
def consume_data(producer_output):
    print(f"Processing {producer_output['records']} records")
    print(f"File: {producer_output['file']}")
```

## Scheduling

### Cron Schedules

```json
{
  "name": "scheduled_workflow",
  "schedule": {
    "type": "cron",
    "expression": "0 2 * * *",
    "timezone": "UTC"
  },
  "tasks": [...]
}
```

### Interval Schedules

```json
{
  "name": "interval_workflow",
  "schedule": {
    "type": "interval",
    "every": "1h",
    "start_time": "2024-01-01T00:00:00Z"
  },
  "tasks": [...]
}
```

### Event Triggers

```json
{
  "name": "event_triggered",
  "triggers": [
    {
      "type": "webhook",
      "path": "/trigger/my_workflow"
    },
    {
      "type": "file",
      "path": "/data/incoming/*.csv",
      "event": "created"
    },
    {
      "type": "queue",
      "queue": "workflow-triggers",
      "filter": {"type": "process_request"}
    }
  ],
  "tasks": [...]
}
```

## Summary

In this chapter, you've learned:

- **Workflow Structure**: Metadata, tasks, and execution configuration
- **Creating Workflows**: CLI, SDK, and API methods
- **Task Types**: Shell, Python, HTTP, and Docker tasks
- **Execution**: Running, monitoring, and managing workflows
- **Data Flow**: Parameters and task outputs
- **Scheduling**: Cron, interval, and event triggers

## Key Takeaways

1. **JSON Definitions**: Workflows are declaratively defined
2. **Multiple Task Types**: Choose the right task type for each job
3. **Flexible Execution**: Run immediately or schedule
4. **Data Passing**: Tasks can share outputs
5. **Event-Driven**: Trigger workflows from various sources

## Next Steps

Ready to explore different task types in depth? Let's dive into Chapter 3.

---

**Ready for Chapter 3?** [Task Management](03-task-management.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
