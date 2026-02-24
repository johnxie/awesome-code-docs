---
layout: default
title: "Chapter 4: Dependencies"
parent: "Deer Flow Tutorial"
nav_order: 4
---

# Chapter 4: Dependencies

Welcome to **Chapter 4: Dependencies**. In this part of **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master complex dependency relationships, conditional execution, and data flow between tasks.

## Overview

Dependencies define the execution order and relationships between tasks. Deer Flow supports various dependency patterns from simple chains to complex DAGs with conditional branching.

## Dependency Types

### Direct Dependencies

```json
{
  "tasks": [
    {
      "id": "task_a",
      "type": "shell",
      "command": "echo A"
    },
    {
      "id": "task_b",
      "type": "shell",
      "command": "echo B",
      "depends_on": ["task_a"]
    },
    {
      "id": "task_c",
      "type": "shell",
      "command": "echo C",
      "depends_on": ["task_b"]
    }
  ]
}
```

```
task_a ──▶ task_b ──▶ task_c
```

### Fan-Out Pattern

```json
{
  "tasks": [
    {
      "id": "source",
      "type": "python",
      "config": {"script": "fetch_data.py"}
    },
    {
      "id": "process_a",
      "depends_on": ["source"],
      "type": "python",
      "config": {"script": "process_a.py"}
    },
    {
      "id": "process_b",
      "depends_on": ["source"],
      "type": "python",
      "config": {"script": "process_b.py"}
    },
    {
      "id": "process_c",
      "depends_on": ["source"],
      "type": "python",
      "config": {"script": "process_c.py"}
    }
  ]
}
```

```
              ┌──▶ process_a
              │
source ───────┼──▶ process_b
              │
              └──▶ process_c
```

### Fan-In Pattern

```json
{
  "tasks": [
    {"id": "fetch_users", "type": "http", "config": {"url": "..."}},
    {"id": "fetch_orders", "type": "http", "config": {"url": "..."}},
    {"id": "fetch_products", "type": "http", "config": {"url": "..."}},
    {
      "id": "aggregate",
      "type": "python",
      "depends_on": ["fetch_users", "fetch_orders", "fetch_products"],
      "config": {"script": "aggregate.py"}
    }
  ]
}
```

```
fetch_users ────┐
                │
fetch_orders ───┼──▶ aggregate
                │
fetch_products ─┘
```

### Diamond Pattern

```json
{
  "tasks": [
    {"id": "start", "type": "shell", "command": "echo Start"},
    {"id": "path_a", "depends_on": ["start"], "type": "shell", "command": "echo A"},
    {"id": "path_b", "depends_on": ["start"], "type": "shell", "command": "echo B"},
    {
      "id": "finish",
      "depends_on": ["path_a", "path_b"],
      "type": "shell",
      "command": "echo Finish"
    }
  ]
}
```

```
        ┌──▶ path_a ──┐
        │             │
start ──┤             ├──▶ finish
        │             │
        └──▶ path_b ──┘
```

## Conditional Execution

### Basic Conditions

```json
{
  "id": "conditional_task",
  "type": "python",
  "depends_on": ["check_condition"],
  "condition": "${tasks.check_condition.output.should_run == true}",
  "config": {
    "script": "process.py"
  }
}
```

### Branch Patterns

```python
from deerflow import Workflow, BranchTask

workflow = Workflow(name="branching_example")

@workflow.task(id="check_type")
def check_data_type(context):
    data = context.params.get("data")
    if data.get("type") == "json":
        return {"branch": "json"}
    elif data.get("type") == "csv":
        return {"branch": "csv"}
    else:
        return {"branch": "default"}

@workflow.task(id="process_json", condition="check_type.output.branch == 'json'")
def process_json(context):
    # Process JSON data
    pass

@workflow.task(id="process_csv", condition="check_type.output.branch == 'csv'")
def process_csv(context):
    # Process CSV data
    pass

@workflow.task(id="process_default", condition="check_type.output.branch == 'default'")
def process_default(context):
    # Default processing
    pass
```

### Conditional Expressions

```json
{
  "tasks": [
    {
      "id": "load_data",
      "type": "python",
      "config": {"script": "load.py"},
      "outputs": ["record_count", "has_errors"]
    },
    {
      "id": "process_normal",
      "depends_on": ["load_data"],
      "condition": "${tasks.load_data.outputs.record_count > 0 && !tasks.load_data.outputs.has_errors}",
      "type": "python",
      "config": {"script": "process.py"}
    },
    {
      "id": "handle_errors",
      "depends_on": ["load_data"],
      "condition": "${tasks.load_data.outputs.has_errors}",
      "type": "python",
      "config": {"script": "error_handler.py"}
    },
    {
      "id": "skip_empty",
      "depends_on": ["load_data"],
      "condition": "${tasks.load_data.outputs.record_count == 0}",
      "type": "shell",
      "command": "echo 'No records to process'"
    }
  ]
}
```

## Data Flow

### Passing Outputs

```python
from deerflow import Workflow, Output

workflow = Workflow(name="data_flow_example")

@workflow.task(id="producer")
def produce_data():
    data = {
        "records": [1, 2, 3, 4, 5],
        "metadata": {"source": "api", "timestamp": "2024-01-15"}
    }
    return Output(
        data=data,
        artifacts={"data_file": "/tmp/data.json"}
    )

@workflow.task(id="consumer", depends_on=["producer"])
def consume_data(producer):
    records = producer.data["records"]
    data_file = producer.artifacts["data_file"]
    # Process the data
    return Output(data={"processed_count": len(records)})
```

### XCom-Style Communication

```json
{
  "tasks": [
    {
      "id": "extract",
      "type": "python",
      "config": {
        "script": "extract.py"
      },
      "publish": {
        "key": "extracted_data",
        "value": "${output.data}"
      }
    },
    {
      "id": "transform",
      "depends_on": ["extract"],
      "type": "python",
      "config": {
        "script": "transform.py",
        "args": ["${xcom.extracted_data}"]
      }
    }
  ]
}
```

### File-Based Data Passing

```json
{
  "tasks": [
    {
      "id": "generate",
      "type": "python",
      "config": {
        "script": "generate.py"
      },
      "artifacts": {
        "output": "/workflow/data/output.parquet"
      }
    },
    {
      "id": "analyze",
      "depends_on": ["generate"],
      "type": "python",
      "config": {
        "script": "analyze.py",
        "args": ["${tasks.generate.artifacts.output}"]
      }
    }
  ]
}
```

## Advanced Dependency Patterns

### Optional Dependencies

```json
{
  "id": "flexible_task",
  "type": "python",
  "dependencies": [
    {
      "task": "required_task",
      "type": "required"
    },
    {
      "task": "optional_task",
      "type": "optional"
    }
  ],
  "config": {
    "script": "process.py"
  }
}
```

### Trigger Rules

```json
{
  "tasks": [
    {"id": "task_a", "type": "shell", "command": "..."},
    {"id": "task_b", "type": "shell", "command": "..."},
    {"id": "task_c", "type": "shell", "command": "..."},
    {
      "id": "final_task",
      "depends_on": ["task_a", "task_b", "task_c"],
      "trigger_rule": "one_success",
      "type": "shell",
      "command": "echo Done"
    }
  ]
}
```

Trigger rules:
- `all_success` - All dependencies succeeded (default)
- `all_done` - All dependencies completed (success or fail)
- `one_success` - At least one succeeded
- `one_failed` - At least one failed
- `none_failed` - No failures (includes skipped)

### Cross-Workflow Dependencies

```python
from deerflow import Workflow, ExternalTaskSensor

workflow = Workflow(name="downstream")

# Wait for external workflow to complete
sensor = ExternalTaskSensor(
    id="wait_for_upstream",
    external_workflow="upstream_workflow",
    external_task="final_task",
    execution_date="{{ execution_date }}",
    timeout=3600,
    poke_interval=60
)

workflow.add_task(sensor)

@workflow.task(id="process", depends_on=["wait_for_upstream"])
def process_downstream():
    # Process after upstream completes
    pass
```

## Dependency Visualization

### Generating DAG Diagrams

```bash
# Generate visual representation
deerflow visualize my_workflow --format png --output workflow.png

# Interactive HTML view
deerflow visualize my_workflow --format html --output workflow.html

# Mermaid diagram
deerflow visualize my_workflow --format mermaid
```

### Validating Dependencies

```bash
# Check for cycles and issues
deerflow validate my_workflow

# Detailed dependency report
deerflow dependencies my_workflow --verbose
```

### Execution Order Preview

```bash
# Show execution order
deerflow order my_workflow

# Output:
# Level 0: task_a (parallel with task_b)
# Level 0: task_b (parallel with task_a)
# Level 1: task_c (after task_a)
# Level 1: task_d (after task_b)
# Level 2: task_e (after task_c, task_d)
```

## Summary

In this chapter, you've learned:

- **Dependency Types**: Direct, fan-out, fan-in, diamond
- **Conditional Execution**: Branches and expressions
- **Data Flow**: Outputs, XCom, artifacts
- **Advanced Patterns**: Optional deps, trigger rules, cross-workflow
- **Visualization**: DAG diagrams and validation

## Key Takeaways

1. **DAG Structure**: Dependencies form directed acyclic graphs
2. **Parallel When Possible**: Independent tasks run in parallel
3. **Conditions Enable Branching**: Dynamic workflow paths
4. **Data Passes Cleanly**: Use outputs and artifacts
5. **Validate Dependencies**: Check for cycles and issues

## Next Steps

Ready to learn about error handling and fault tolerance? Let's explore Chapter 5.

---

**Ready for Chapter 5?** [Error Handling](05-error-handling.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `depends_on`, `config`, `workflow` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Dependencies` as an operating subsystem inside **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `tasks`, `python`, `script` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Dependencies` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `depends_on`.
2. **Input normalization**: shape incoming data so `config` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `workflow`.
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
- search upstream code for `depends_on` and `config` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Task Management](03-task-management.md)
- [Next Chapter: Chapter 5: Error Handling](05-error-handling.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
