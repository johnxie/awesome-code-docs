---
layout: default
title: "OpenHands Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: OpenHands Tutorial
---

# Chapter 1: Getting Started with OpenHands

Welcome to **Chapter 1: Getting Started with OpenHands**. In this part of **OpenHands Tutorial: Autonomous Software Engineering Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Install OpenHands, understand its architecture, and execute your first autonomous coding task.

## Overview

OpenHands is a powerful autonomous AI software engineering agent that can perform complex coding tasks independently. This chapter covers installation, basic concepts, and your first hands-on experience with autonomous development.

## Installation and Setup

### System Requirements

```bash
# Minimum requirements
- Python 3.10+
- 8GB RAM (16GB recommended)
- Linux/macOS/Windows
- Node.js 18+ (for frontend components)

# For GPU acceleration (optional)
- CUDA 11.8+ (NVIDIA GPUs)
- ROCm 5.4+ (AMD GPUs)
```

### Installing OpenHands

```bash
# Install via pip
pip install openhands

# Or install from source for latest features
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands
pip install -e .

# Install with all optional dependencies
pip install openhands[all]
```

### Setting up API Keys

OpenHands requires API keys for the underlying language models:

```bash
# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"  # Alternative

# For other providers
export TOGETHER_API_KEY="your-together-api-key"
export DEEPINFRA_API_KEY="your-deepinfra-api-key"
```

### Configuration File

Create a configuration file for OpenHands:

```python
# config.toml
[core]
workspace_base = "./workspace"
persist_sandbox = false
run_as_openhands = true
runtime_startup_timeout = 120

[security]
confirmation_mode = false
security_analyzer = ""
allow_file_operations = true

[models]
embedding_model = "local"  # or "openai"
llm_model = "gpt-4"
api_key = "your-api-key"
custom_llm_provider = ""
max_input_tokens = 0
max_output_tokens = 0
input_cost_per_token = 0.0
output_cost_per_token = 0.0
ollama_base_url = ""
drop_params = false

[sandbox]
container_image = "ghcr.io/all-hands-ai/openhands:main"
local_runtime = "eventstream"
runtime_startup_timeout = 120
runtime_startup_env_vars = {}
enable_auto_fix = false
use_host_network = false
runtime_cls = "openhands.runtime.impl.eventstream.EventStreamRuntime"

[llm]
model = "gpt-4"
api_key = "your-api-key"
custom_llm_provider = ""
embedding_model = "local"
embedding_base_url = ""
max_input_tokens = 0
max_output_tokens = 0
input_cost_per_token = 0.0
output_cost_per_token = 0.0
ollama_base_url = ""
drop_params = false
```

## Core Architecture

### OpenHands Components

```python
from openhands import OpenHands, Task
from openhands.runtime import get_runtime
from openhands.agent import Agent

# Main components
agent = Agent()  # The AI agent
runtime = get_runtime()  # Execution environment
task = Task()  # Task specification

# Combined system
openhands = OpenHands(
    agent=agent,
    runtime=runtime
)
```

### Agent Types

OpenHands supports different agent types for various scenarios:

```python
from openhands.agent import CodeActAgent, BrowsingAgent, PlannerAgent

# CodeActAgent: Primary agent for coding tasks
code_agent = CodeActAgent()

# BrowsingAgent: For web-related tasks
browse_agent = BrowsingAgent()

# PlannerAgent: For complex multi-step planning
planner_agent = PlannerAgent()

# Custom agent configuration
custom_agent = CodeActAgent(
    llm_config={
        "model": "gpt-4",
        "api_key": "your-key",
        "temperature": 0.1,  # Lower temperature for coding
        "max_tokens": 4096
    }
)
```

### Runtime Environments

OpenHands provides different execution environments:

```python
from openhands.runtime import LocalRuntime, DockerRuntime, RemoteRuntime

# Local runtime (direct execution)
local_runtime = LocalRuntime()

# Docker runtime (sandboxed execution)
docker_runtime = DockerRuntime(
    container_image="ghcr.io/all-hands-ai/openhands:main",
    workspace_base="/workspace"
)

# Remote runtime (for distributed setups)
remote_runtime = RemoteRuntime(
    host="remote-server",
    port=8080
)
```

## Your First OpenHands Task

### Basic Task Execution

```python
from openhands import OpenHands

# Initialize OpenHands
openhands = OpenHands()

# Define a simple task
task = "Create a Python function that calculates the factorial of a number"

# Execute the task
result = openhands.run(
    task=task,
    workspace="./my_first_project"
)

# Check the result
print("Task completed!")
print(f"Generated code: {result.code}")
print(f"Execution output: {result.output}")
print(f"Files created: {result.files_created}")
```

### Understanding the Result

```python
# The result object contains detailed information
print(f"Task: {result.task}")
print(f"Status: {result.status}")  # 'completed', 'failed', etc.
print(f"Duration: {result.execution_time} seconds")

# Code generated by the agent
print("Generated code:")
print(result.code)

# Files created/modified
for file_path in result.files_created:
    print(f"Created: {file_path}")

for file_path in result.files_modified:
    print(f"Modified: {file_path}")

# Any errors or issues
if result.errors:
    print("Errors encountered:")
    for error in result.errors:
        print(f"  - {error}")
```

### Interactive Session

```python
from openhands import OpenHands

# Start an interactive session
openhands = OpenHands()

# Begin interactive mode
session = openhands.start_interactive_session(
    workspace="./interactive_workspace"
)

print("OpenHands interactive mode started!")
print("Type 'help' for commands, 'exit' to quit")

while True:
    user_input = input("> ")

    if user_input.lower() == 'exit':
        break
    elif user_input.lower() == 'help':
        print("Commands:")
        print("  help - Show this help")
        print("  status - Show current status")
        print("  files - List workspace files")
        print("  <task> - Execute a coding task")
        continue

    # Execute the user's task
    try:
        result = session.execute_task(user_input)
        print(f"Result: {result.output}")

        if result.code:
            print(f"Code generated: {result.code}")

    except Exception as e:
        print(f"Error: {e}")
```

## Task Specification

### Basic Task Format

```python
# Simple task specification
simple_task = {
    "description": "Create a hello world function in Python",
    "language": "python",
    "requirements": ["Function should return 'Hello, World!'"],
    "constraints": ["Use proper function naming", "Include docstring"]
}

# Execute simple task
result = openhands.run(task=simple_task)
```

### Advanced Task Specification

```python
# Complex task with detailed requirements
complex_task = {
    "description": "Build a REST API for a task management system",
    "components": {
        "backend": {
            "framework": "FastAPI",
            "database": "SQLite",
            "models": ["User", "Task", "Category"],
            "endpoints": [
                "POST /users - Create user",
                "GET /users/{id} - Get user",
                "POST /tasks - Create task",
                "GET /tasks - List tasks",
                "PUT /tasks/{id} - Update task",
                "DELETE /tasks/{id} - Delete task"
            ]
        },
        "frontend": {
            "framework": "React",
            "components": ["TaskList", "TaskForm", "UserProfile"],
            "features": ["CRUD operations", "Real-time updates"]
        },
        "testing": {
            "unit_tests": True,
            "integration_tests": True,
            "api_tests": True
        },
        "documentation": {
            "api_docs": True,
            "readme": True,
            "deployment_guide": True
        }
    },
    "requirements": [
        "Use proper error handling",
        "Implement input validation",
        "Add authentication/authorization",
        "Include comprehensive tests",
        "Create deployment configuration"
    ],
    "constraints": [
        "Follow REST API best practices",
        "Use type hints in Python",
        "Implement proper database relationships",
        "Ensure security best practices"
    ]
}

# Execute complex task
result = openhands.run(
    task=complex_task,
    max_execution_time=1800,  # 30 minutes
    save_progress=True
)
```

## Working with Workspaces

### Workspace Management

```python
from openhands.workspace import Workspace

# Create a new workspace
workspace = Workspace("./my_project")

# Initialize workspace with template
workspace.init_from_template("python-fastapi")

# Or start with empty workspace
workspace.create_empty()

# Workspace operations
print(f"Workspace path: {workspace.path}")
print(f"Files: {workspace.list_files()}")

# Create files
workspace.create_file("main.py", "print('Hello, World!')")

# Read files
content = workspace.read_file("main.py")
print(f"File content: {content}")

# Execute commands in workspace
result = workspace.run_command("python main.py")
print(f"Command output: {result.stdout}")
```

### Persistent Workspaces

```python
# Create persistent workspace for multi-session work
persistent_workspace = Workspace("./persistent_project", persistent=True)

# The workspace will remember state between OpenHands sessions
# Useful for long-running development projects

# Save workspace state
persistent_workspace.save_state()

# Load workspace state in new session
loaded_workspace = Workspace.load_state("./persistent_project")
```

## Error Handling and Debugging

### Common Issues and Solutions

```python
try:
    result = openhands.run(task="Create a Python web server")
except Exception as e:
    print(f"Execution failed: {e}")

    # Get detailed error information
    if hasattr(result, 'error_details'):
        print("Error details:")
        print(result.error_details)

    # Check logs
    logs = openhands.get_logs()
    print("Recent logs:")
    for log_entry in logs[-10:]:  # Last 10 entries
        print(f"  {log_entry['timestamp']}: {log_entry['message']}")
```

### Debugging Mode

```python
# Enable debugging mode for detailed execution tracing
openhands.enable_debug_mode()

# Run task with debugging
result = openhands.run(
    task="Debug this Python function: def add(a, b): return a + b",
    debug=True
)

# Access debug information
debug_info = result.debug_info
print("Execution trace:")
for step in debug_info['trace']:
    print(f"  Step {step['step']}: {step['action']}")
    print(f"    Result: {step['result']}")
    print(f"    Duration: {step['duration']}ms")
```

## Security Considerations

### Sandboxed Execution

OpenHands runs in secure sandboxed environments by default:

```python
# Configure sandbox security
secure_openhands = OpenHands(
    runtime=DockerRuntime(
        container_image="ghcr.io/all-hands-ai/openhands:main",
        security_opts=[
            "--cap-drop=ALL",  # Drop all capabilities
            "--network=none",  # No network access
            "--read-only",     # Read-only root filesystem
            "--tmpfs=/tmp"     # Writable temp directory
        ]
    )
)

# Execute task in secure sandbox
result = secure_openhands.run(
    task="Create a file processing script",
    security_level="high"
)
```

### Permission Management

```python
# Configure execution permissions
permissions = {
    "file_operations": {
        "read": True,
        "write": True,
        "delete": False,  # Disable file deletion
        "execute": True
    },
    "network_access": {
        "outbound": False,  # No internet access
        "localhost": True   # Allow localhost connections
    },
    "command_execution": {
        "allowed_commands": ["python", "pip", "npm", "node"],
        "blocked_commands": ["rm", "sudo", "curl", "wget"]
    }
}

# Apply permissions
openhands.set_permissions(permissions)
```

## Performance Optimization

### Resource Configuration

```python
# Configure for optimal performance
high_perf_openhands = OpenHands(
    runtime=DockerRuntime(
        container_image="ghcr.io/all-hands-ai/openhands:main",
        resources={
            "cpu": "2.0",           # 2 CPU cores
            "memory": "4g",         # 4GB RAM
            "gpu": "1",             # 1 GPU (if available)
            "storage": "10g"        # 10GB storage
        }
    ),
    agent=CodeActAgent(
        llm_config={
            "model": "gpt-4",
            "temperature": 0.1,     # Lower temperature for consistency
            "max_tokens": 2048,     # Reasonable token limit
            "cache_enabled": True   # Enable response caching
        }
    )
)
```

### Caching and Reuse

```python
# Enable caching for repeated operations
openhands.enable_caching(
    cache_dir="./openhands_cache",
    max_cache_size="10g",
    ttl_seconds=3600  # 1 hour cache TTL
)

# Cache will automatically store and reuse:
# - Model responses for similar queries
# - Compiled code artifacts
# - Dependency installations
# - Test execution results
```

## Summary

In this chapter, we've covered:

- **Installation and Setup** - Getting OpenHands running with proper configuration
- **Core Architecture** - Understanding agents, runtimes, and task execution
- **Basic Task Execution** - Running your first autonomous coding tasks
- **Workspace Management** - Working with project directories and files
- **Security and Permissions** - Safe execution in sandboxed environments
- **Performance Optimization** - Configuring for optimal resource usage

OpenHands represents a significant advancement in AI-assisted software development, capable of handling complex, multi-step coding tasks autonomously.

## Key Takeaways

1. **Autonomous Execution**: OpenHands can complete entire development workflows independently
2. **Secure Sandboxing**: Code execution happens in isolated, secure environments
3. **Flexible Configuration**: Adaptable to different project requirements and constraints
4. **Comprehensive Results**: Detailed output including code, execution results, and metadata
5. **Production Ready**: Configurable security, performance, and resource management

Next, we'll explore **basic operations** - file manipulation, command execution, and environment management.

---

**Ready for the next chapter?** [Chapter 2: Basic Operations](02-basic-operations.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **OpenHands Tutorial: Autonomous Software Engineering Workflows**
- tutorial slug: **openhands-tutorial**
- chapter focus: **Chapter 1: Getting Started with OpenHands**
- system context: **Openhands Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started with OpenHands`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [OpenHands Repository](https://github.com/OpenHands/OpenHands)
- [OpenHands Docs](https://docs.openhands.dev/)
- [OpenHands Releases](https://github.com/OpenHands/OpenHands/releases)

### Cross-Tutorial Connection Map

- [OpenClaw Tutorial](../openclaw-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Continue Tutorial](../continue-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 1: Getting Started with OpenHands`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `print`, `result`, `openhands` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with OpenHands` as an operating subsystem inside **OpenHands Tutorial: Autonomous Software Engineering Workflows**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `task`, `workspace`, `OpenHands` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with OpenHands` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `print`.
2. **Input normalization**: shape incoming data so `result` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `openhands`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [OpenHands Repository](https://github.com/OpenHands/OpenHands)
  Why it matters: authoritative reference on `OpenHands Repository` (github.com).
- [OpenHands Docs](https://docs.openhands.dev/)
  Why it matters: authoritative reference on `OpenHands Docs` (docs.openhands.dev).
- [OpenHands Releases](https://github.com/OpenHands/OpenHands/releases)
  Why it matters: authoritative reference on `OpenHands Releases` (github.com).

Suggested trace strategy:
- search upstream code for `print` and `result` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Basic Operations - Files, Commands, and Environments](02-basic-operations.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
