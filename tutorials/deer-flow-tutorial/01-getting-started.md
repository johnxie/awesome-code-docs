---
layout: default
title: "Chapter 1: Getting Started with Deer Flow"
parent: "Deer Flow Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Deer Flow

Welcome to Deer Flow! This chapter will guide you through installing and setting up Deer Flow, understanding its core concepts, and creating your first distributed workflow.

## 🎯 What You'll Learn

- Deer Flow installation and setup
- Core concepts (workflows, tasks, dependencies)
- Basic workflow creation and execution
- Web interface and API usage
- First distributed workflow walkthrough

## 🏗️ Deer Flow Architecture

Deer Flow consists of several key components working together to orchestrate distributed workflows:

```mermaid
graph TB
    subgraph "Control Plane"
        A[Workflow Manager]
        B[Task Scheduler]
        C[Dependency Resolver]
        D[State Manager]
    end

    subgraph "Execution Plane"
        E[Worker Nodes]
        F[Task Executors]
        G[Resource Pool]
        H[Load Balancer]
    end

    subgraph "Data Plane"
        I[Workflow Store]
        J[Task Queue]
        K[Result Store]
        L[Metrics Store]
    end

    subgraph "Integration Layer"
        M[REST API]
        N[Web UI]
        O[CLI Tools]
        P[SDK Libraries]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    A --> I
    A --> J
    A --> K
    A --> L
    A --> M
    A --> N
    A --> O
    A --> P
```

### Core Components

1. **Workflow Manager**: Orchestrates workflow execution
2. **Task Scheduler**: Assigns tasks to workers
3. **Worker Nodes**: Execute tasks in parallel
4. **State Manager**: Tracks workflow and task states
5. **Result Store**: Persists task outputs and results

## 🚀 Installation Methods

### Method 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f deer-flow-server
```

**What this starts:**
- Deer Flow server (port 8080)
- Redis for task queuing
- PostgreSQL for data storage
- Web interface

### Method 2: Manual Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install python3.10 python3.10-venv postgresql redis-server

# Clone and setup
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
sudo -u postgres createdb deerflow
sudo -u postgres psql -c "CREATE USER deerflow WITH PASSWORD 'deerflow123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE deerflow TO deerflow;"

# Start Redis
sudo systemctl start redis-server

# Start the server
python run_server.py
```

### Method 3: Kubernetes Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deer-flow
spec:
  replicas: 3
  selector:
    matchLabels:
      app: deer-flow
  template:
    metadata:
      labels:
        app: deer-flow
    spec:
      containers:
      - name: deer-flow
        image: bytedance/deer-flow:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          value: "postgresql://deerflow:deerflow123@postgres:5432/deerflow"
        - name: REDIS_URL
          value: "redis://redis:6379"
        resources:
          limits:
            cpu: "1000m"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"
```

## ⚙️ Configuration

### Environment Variables

```bash
# Database configuration
export DATABASE_URL="postgresql://deerflow:deerflow123@localhost:5432/deerflow"

# Redis configuration
export REDIS_URL="redis://localhost:6379"

# Server configuration
export SERVER_HOST="0.0.0.0"
export SERVER_PORT="8080"

# Worker configuration
export WORKER_CONCURRENCY="4"
export WORKER_PREFETCH="2"

# Logging
export LOG_LEVEL="INFO"
export LOG_FILE="/var/log/deer-flow.log"
```

### Configuration File

```yaml
# config.yaml
server:
  host: "0.0.0.0"
  port: 8080
  workers: 4

database:
  url: "postgresql://deerflow:deerflow123@localhost:5432/deerflow"
  pool_size: 10
  max_overflow: 20

redis:
  url: "redis://localhost:6379"
  db: 0

worker:
  concurrency: 4
  prefetch: 2
  heartbeat: 30

logging:
  level: "INFO"
  file: "/var/log/deer-flow.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

monitoring:
  enabled: true
  metrics_port: 9090
```

## 🌐 Accessing Deer Flow

Once installed, access Deer Flow through:

```bash
# Web interface
open http://localhost:8080

# API endpoints
curl http://localhost:8080/api/health

# CLI tools
deer-flow --help
```

### Default Credentials
- **Web UI**: No authentication required (configure as needed)
- **API**: No authentication by default (add middleware for production)

## 🏃‍♂️ Your First Workflow

### Creating a Simple Workflow

```json
// simple_workflow.json
{
  "name": "hello_world",
  "description": "A simple hello world workflow",
  "version": "1.0",
  "tasks": [
    {
      "id": "hello_task",
      "name": "Hello Task",
      "type": "shell",
      "command": "echo 'Hello, Deer Flow!'",
      "timeout": 30
    }
  ]
}
```

### Submitting the Workflow

```bash
# Via API
curl -X POST http://localhost:8080/api/workflows \
  -H "Content-Type: application/json" \
  -d @simple_workflow.json

# Via CLI
deer-flow workflow submit simple_workflow.json

# Via Python SDK
from deerflow import WorkflowClient

client = WorkflowClient("http://localhost:8080")
workflow_id = client.submit_workflow("simple_workflow.json")
print(f"Workflow submitted: {workflow_id}")
```

### Monitoring Execution

```bash
# Check workflow status
curl http://localhost:8080/api/workflows/{workflow_id}/status

# View task logs
curl http://localhost:8080/api/workflows/{workflow_id}/tasks/{task_id}/logs

# Get workflow results
curl http://localhost:8080/api/workflows/{workflow_id}/result
```

## 📊 Understanding Workflow States

### Workflow States

```
Workflow States
├── PENDING     - Workflow submitted, waiting to start
├── RUNNING     - Workflow is currently executing
├── COMPLETED   - All tasks completed successfully
├── FAILED      - One or more tasks failed
├── CANCELLED   - Workflow was cancelled
└── TIMEOUT     - Workflow exceeded time limit
```

### Task States

```
Task States
├── PENDING     - Task waiting to be scheduled
├── SCHEDULED   - Task assigned to a worker
├── RUNNING     - Task is currently executing
├── COMPLETED   - Task completed successfully
├── FAILED      - Task execution failed
├── RETRY       - Task failed, will retry
├── CANCELLED   - Task was cancelled
└── TIMEOUT     - Task exceeded time limit
```

## 🔧 Workflow Definition

### Basic Task Types

```json
{
  "tasks": [
    {
      "id": "shell_task",
      "name": "Shell Command",
      "type": "shell",
      "command": "echo 'Hello World'",
      "working_directory": "/tmp",
      "environment": {
        "MY_VAR": "my_value"
      },
      "timeout": 30
    },
    {
      "id": "http_task",
      "name": "HTTP Request",
      "type": "http",
      "method": "GET",
      "url": "https://api.example.com/data",
      "headers": {
        "Authorization": "Bearer token"
      },
      "timeout": 60
    },
    {
      "id": "python_task",
      "name": "Python Function",
      "type": "python",
      "module": "my_module",
      "function": "my_function",
      "args": ["arg1", "arg2"],
      "kwargs": {"key": "value"}
    }
  ]
}
```

### Workflow Metadata

```json
{
  "name": "data_processing_pipeline",
  "description": "Process and analyze data files",
  "version": "1.0.0",
  "author": "Data Team",
  "tags": ["data", "processing", "analytics"],
  "timeout": 3600,
  "retry_policy": {
    "max_attempts": 3,
    "backoff": "exponential",
    "initial_delay": 1
  },
  "notifications": {
    "on_success": ["email@company.com"],
    "on_failure": ["alerts@company.com"]
  }
}
```

## 🔄 Task Dependencies

### Simple Dependencies

```json
{
  "tasks": [
    {
      "id": "extract_data",
      "name": "Extract Data",
      "type": "shell",
      "command": "python extract.py"
    },
    {
      "id": "transform_data",
      "name": "Transform Data",
      "type": "shell",
      "command": "python transform.py",
      "depends_on": ["extract_data"]
    },
    {
      "id": "load_data",
      "name": "Load Data",
      "type": "shell",
      "command": "python load.py",
      "depends_on": ["transform_data"]
    }
  ]
}
```

### Complex Dependencies

```json
{
  "tasks": [
    {
      "id": "task_a",
      "name": "Task A",
      "type": "shell",
      "command": "echo 'Task A'"
    },
    {
      "id": "task_b",
      "name": "Task B",
      "type": "shell",
      "command": "echo 'Task B'",
      "depends_on": ["task_a"]
    },
    {
      "id": "task_c",
      "name": "Task C",
      "type": "shell",
      "command": "echo 'Task C'",
      "depends_on": ["task_a"]
    },
    {
      "id": "task_d",
      "name": "Task D",
      "type": "shell",
      "command": "echo 'Task D'",
      "depends_on": ["task_b", "task_c"]
    }
  ]
}
```

## 📊 Monitoring Workflows

### Web Dashboard

The Deer Flow web interface provides:

- **Workflow Overview**: List of all workflows with status
- **Task Details**: Individual task execution details
- **Real-time Logs**: Live streaming of task logs
- **Performance Metrics**: Execution times and success rates
- **Dependency Graph**: Visual representation of task relationships

### API Monitoring

```bash
# Get workflow statistics
curl http://localhost:8080/api/workflows/stats

# List running workflows
curl http://localhost:8080/api/workflows?status=running

# Get task execution history
curl http://localhost:8080/api/tasks/history

# Monitor system health
curl http://localhost:8080/api/health
```

## 🔧 Troubleshooting

### Common Issues

#### Connection Problems
```bash
# Check if services are running
docker-compose ps

# Verify API connectivity
curl http://localhost:8080/api/health

# Check logs
docker-compose logs deer-flow-server
```

#### Database Issues
```bash
# Check database connectivity
docker-compose exec postgres psql -U deerflow -d deerflow -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d
```

#### Worker Issues
```bash
# Check worker status
curl http://localhost:8080/api/workers

# Restart workers
docker-compose restart deer-flow-worker

# Scale workers
docker-compose up -d --scale deer-flow-worker=3
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Monitor queue length
curl http://localhost:8080/api/queue/stats

# Adjust worker concurrency
export WORKER_CONCURRENCY=8
docker-compose restart deer-flow-worker
```

## 🎯 Key Concepts

### Workflows
- **Definition**: JSON specification of tasks and dependencies
- **Execution**: Orchestrated by the workflow manager
- **State**: Tracked throughout lifecycle
- **Results**: Stored and accessible via API

### Tasks
- **Types**: Shell, HTTP, Python, custom
- **Dependencies**: Define execution order
- **Retries**: Automatic retry on failure
- **Timeouts**: Prevent hanging tasks

### Workers
- **Scaling**: Horizontal scaling for performance
- **Isolation**: Each worker runs in separate container
- **Monitoring**: Health checks and metrics
- **Resource**: CPU and memory allocation

## 📊 Performance Metrics

### Key Metrics to Monitor

```python
# Workflow metrics
workflow_metrics = {
    'total_workflows': 0,
    'running_workflows': 0,
    'completed_workflows': 0,
    'failed_workflows': 0,
    'average_execution_time': 0.0
}

# Task metrics
task_metrics = {
    'total_tasks': 0,
    'running_tasks': 0,
    'completed_tasks': 0,
    'failed_tasks': 0,
    'retry_rate': 0.0
}

# System metrics
system_metrics = {
    'cpu_usage': 0.0,
    'memory_usage': 0.0,
    'queue_length': 0,
    'worker_count': 0
}
```

## 🏆 Achievement Unlocked!

Congratulations! 🎉 You've successfully:

- ✅ Installed Deer Flow using Docker
- ✅ Configured the system components
- ✅ Created and executed your first workflow
- ✅ Explored the web interface and API
- ✅ Understood workflow and task states
- ✅ Set up basic monitoring

## 🚀 What's Next?

Ready to create more complex workflows? Let's explore [Chapter 2: Workflow Basics](02-workflow-basics.md) to learn about task types, dependencies, and advanced workflow patterns.

---

**Practice what you've learned:**
1. Experiment with different installation methods
2. Create workflows with multiple task types
3. Set up dependencies between tasks
4. Monitor workflow execution in the web UI
5. Explore the API endpoints for automation

*What's the first distributed workflow you want to build?* 🔀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Task`, `deer`, `flow` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Deer Flow` as an operating subsystem inside **Deer Flow Tutorial: Distributed Workflow Orchestration Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `localhost`, `http` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Deer Flow` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Task`.
2. **Input normalization**: shape incoming data so `deer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `flow`.
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
- search upstream code for `Task` and `deer` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Workflow Basics](02-workflow-basics.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
