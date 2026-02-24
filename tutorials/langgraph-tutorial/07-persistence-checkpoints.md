---
layout: default
title: "Chapter 7: Persistence and Checkpoints"
parent: "LangGraph Tutorial"
nav_order: 7
---

# Chapter 7: Persistence and Checkpoints

Welcome to **Chapter 7: Persistence and Checkpoints**. In this part of **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! Your LangGraph applications are getting sophisticated with tool integration, but what happens if your application crashes or gets interrupted? How do you save progress and resume where you left off? That's where **persistence and checkpoints** come in!

## What Problem Does This Solve?

Imagine you're building a complex AI workflow:
- A customer support chatbot having a long conversation
- A research assistant gathering data from multiple sources
- A coding tutor working through multiple exercises

Without persistence, all progress would be lost if:
- The server restarts
- The user disconnects
- An error occurs midway through execution

Persistence ensures your applications can **survive interruptions** and **resume seamlessly**.

## Understanding Persistence in LangGraph

Persistence in LangGraph means saving your graph's state to a durable storage system so it can be restored later. This includes:
- **Graph State**: All the data in your TypedDict
- **Execution History**: What steps have been completed
- **Current Position**: Where in the graph execution you are

### Basic Persistence Setup

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from typing import TypedDict

class PersistentState(TypedDict):
    messages: list
    current_step: str
    user_data: dict
    thread_id: str

# Create a memory-based checkpoint saver
memory_checkpoint = MemorySaver()

def process_step(state: PersistentState) -> PersistentState:
    """A node that processes data."""
    # Your processing logic here
    return {
        **state,
        "current_step": "processed",
        "user_data": {**state.get("user_data", {}), "processed_at": "now"}
    }

# Build graph with persistence
graph = StateGraph(PersistentState)
graph.add_node("process", process_step)
graph.set_entry_point("process")
graph.add_edge("process", END)

# Compile with checkpoint saver
persistent_graph = graph.compile(checkpointer=memory_checkpoint)
```

### Using Persistent Graphs

```python
# Create a unique thread for this conversation
config = {"configurable": {"thread_id": "user_123"}}

# First execution
initial_state = {
    "messages": [{"role": "user", "content": "Hello!"}],
    "current_step": "start",
    "user_data": {},
    "thread_id": "user_123"
}

result1 = persistent_graph.invoke(initial_state, config=config)
print(f"Step 1 result: {result1['current_step']}")

# Second execution (continues from checkpoint)
additional_state = {
    "messages": result1["messages"] + [{"role": "user", "content": "Continue processing"}]
}

result2 = persistent_graph.invoke(additional_state, config=config)
print(f"Step 2 result: {result2['current_step']}")
```

## Checkpoint Storage Options

### 1. Memory Checkpoints (Development)

```python
from langgraph.checkpoint.memory import MemorySaver

# Simple in-memory storage - good for development
memory_saver = MemorySaver()

# All checkpoints stored in memory
# Lost when application restarts
graph.compile(checkpointer=memory_saver)
```

### 2. SQLite Checkpoints (Production)

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persistent SQLite storage
sqlite_saver = SqliteSaver.from_conn_string("checkpoints.db")

# Checkpoints survive application restarts
# Good for single-server deployments
graph.compile(checkpointer=sqlite_saver)
```

### 3. PostgreSQL Checkpoints (Enterprise)

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Enterprise-grade PostgreSQL storage
postgres_saver = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/db"
)

# Supports multiple servers, advanced querying
# Best for production deployments
graph.compile(checkpointer=postgres_saver)
```

## Advanced Persistence Patterns

### Thread Management

```python
def create_user_thread(user_id: str) -> dict:
    """Create a new conversation thread for a user."""
    return {"configurable": {"thread_id": f"user_{user_id}"}}

def get_thread_history(graph, thread_config: dict) -> list:
    """Get execution history for a thread."""
    history = []
    for state in graph.get_state_history(thread_config):
        history.append({
            "step": state.values.get("current_step"),
            "timestamp": state.metadata.get("timestamp"),
            "messages": state.values.get("messages", [])
        })
    return history

# Usage
thread_config = create_user_thread("john_doe")
history = get_thread_history(persistent_graph, thread_config)
```

### Selective State Persistence

```python
class SelectiveState(TypedDict):
    messages: list
    sensitive_data: dict  # Don't persist this
    public_data: dict     # Persist this
    thread_id: str

def filter_state_for_persistence(state: SelectiveState) -> dict:
    """Filter out sensitive data before persistence."""
    return {
        "messages": state["messages"],
        "public_data": state["public_data"],
        "thread_id": state["thread_id"]
        # sensitive_data is excluded
    }

# Custom checkpoint saver with filtering
class FilteredSaver(MemorySaver):
    def save_checkpoint(self, config, checkpoint, metadata):
        # Filter state before saving
        filtered_checkpoint = {
            **checkpoint,
            "values": filter_state_for_persistence(checkpoint["values"])
        }
        super().save_checkpoint(config, filtered_checkpoint, metadata)
```

### Checkpoint Metadata

```python
def save_checkpoint_with_metadata(graph, config, state, metadata: dict):
    """Save checkpoint with custom metadata."""
    # Add custom metadata
    enhanced_metadata = {
        **metadata,
        "user_id": state.get("user_id"),
        "session_type": "customer_support",
        "created_at": "2024-01-15T10:30:00Z"
    }

    # Save checkpoint
    graph.update_state(config, state, enhanced_metadata)

# Usage
metadata = {
    "step_name": "data_processing",
    "processing_time": 2.5,
    "memory_usage": "150MB"
}

save_checkpoint_with_metadata(persistent_graph, config, current_state, metadata)
```

## State Recovery and Resumption

### Automatic State Recovery

```python
def resume_conversation(graph, thread_config: dict, new_message: str):
    """Resume a conversation from the last checkpoint."""

    # Get the latest state
    latest_state = graph.get_state(thread_config)

    if latest_state:
        # Resume from checkpoint
        updated_state = {
            **latest_state.values,
            "messages": latest_state.values["messages"] + [
                {"role": "user", "content": new_message}
            ]
        }

        result = graph.invoke(updated_state, thread_config)
        return result
    else:
        # Start new conversation
        return start_new_conversation(graph, thread_config, new_message)
```

### Manual Checkpoint Restoration

```python
def restore_from_checkpoint(graph, thread_config: dict, checkpoint_id: str):
    """Restore graph to a specific checkpoint."""

    # Get all checkpoints for this thread
    checkpoints = list(graph.get_state_history(thread_config))

    # Find the specific checkpoint
    target_checkpoint = None
    for checkpoint in checkpoints:
        if checkpoint.metadata.get("checkpoint_id") == checkpoint_id:
            target_checkpoint = checkpoint
            break

    if target_checkpoint:
        # Restore to this checkpoint
        graph.update_state(thread_config, target_checkpoint.values)
        return target_checkpoint.values
    else:
        raise ValueError(f"Checkpoint {checkpoint_id} not found")
```

## Error Recovery with Checkpoints

### Graceful Error Handling

```python
def execute_with_error_recovery(graph, config, state):
    """Execute graph with automatic error recovery."""

    try:
        result = graph.invoke(state, config)
        return result

    except Exception as e:
        # Log the error
        logger.error(f"Graph execution failed: {str(e)}")

        # Save error state as checkpoint
        error_state = {
            **state,
            "error": str(e),
            "error_timestamp": "2024-01-15T10:30:00Z",
            "recovery_attempts": state.get("recovery_attempts", 0) + 1
        }

        graph.update_state(config, error_state)

        # Attempt recovery
        if error_state["recovery_attempts"] < 3:
            return retry_execution(graph, config, error_state)
        else:
            return handle_permanent_failure(error_state)
```

### Checkpoint-Based Rollback

```python
def rollback_to_last_good_state(graph, config):
    """Rollback to the last successful checkpoint."""

    # Get checkpoint history
    history = list(graph.get_state_history(config))

    # Find the last successful checkpoint
    for checkpoint in history:
        if checkpoint.values.get("status") == "success":
            # Rollback to this state
            graph.update_state(config, checkpoint.values)
            return checkpoint.values

    # No good checkpoint found
    return None
```

## Building a Production-Ready Persistent Application

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
import logging

logger = logging.getLogger(__name__)

class ProductionState(TypedDict):
    messages: list
    current_step: str
    user_id: str
    session_data: dict
    error_count: int
    last_checkpoint: Optional[str]

# Initialize production checkpoint saver
checkpoint_saver = SqliteSaver.from_conn_string("./checkpoints.db")

def validate_state(state: ProductionState) -> bool:
    """Validate state before processing."""
    required_fields = ["messages", "user_id"]
    return all(field in state for field in required_fields)

def process_with_persistence(state: ProductionState) -> ProductionState:
    """Process state with comprehensive error handling."""

    if not validate_state(state):
        raise ValueError("Invalid state structure")

    try:
        # Your processing logic here
        processed_data = process_data(state["session_data"])

        new_state = {
            **state,
            "current_step": "processed",
            "session_data": processed_data,
            "last_checkpoint": "process_completed"
        }

        return new_state

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")

        # Update error count
        error_state = {
            **state,
            "error_count": state.get("error_count", 0) + 1,
            "last_error": str(e),
            "last_checkpoint": "error_occurred"
        }

        return error_state

def save_checkpoint_with_validation(graph, config, state):
    """Save checkpoint with validation."""
    if validate_state(state):
        graph.update_state(config, state)
        logger.info(f"Checkpoint saved for user {state['user_id']}")
    else:
        logger.warning("Invalid state - checkpoint not saved")

# Build production graph
production_graph = StateGraph(ProductionState)
production_graph.add_node("process", process_with_persistence)
production_graph.set_entry_point("process")
production_graph.add_edge("process", END)

# Compile with persistence
persistent_production_graph = production_graph.compile(checkpointer=checkpoint_saver)

# Usage example
def handle_user_request(user_id: str, message: str):
    """Handle user request with full persistence."""

    config = {"configurable": {"thread_id": f"user_{user_id}"}}

    # Try to get existing state
    existing_state = persistent_production_graph.get_state(config)

    if existing_state:
        # Resume existing conversation
        state = existing_state.values
        state["messages"].append({"role": "user", "content": message})
    else:
        # Start new conversation
        state = {
            "messages": [{"role": "user", "content": message}],
            "current_step": "start",
            "user_id": user_id,
            "session_data": {},
            "error_count": 0,
            "last_checkpoint": None
        }

    # Execute with persistence
    result = persistent_production_graph.invoke(state, config)

    # Save final checkpoint
    save_checkpoint_with_validation(persistent_production_graph, config, result)

    return result
```

## Checkpoint Management and Cleanup

### Automatic Cleanup

```python
def cleanup_old_checkpoints(graph, max_age_days: int = 30):
    """Clean up old checkpoints to save storage."""

    import time
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=max_age_days)

    # This would depend on your checkpoint storage implementation
    # For SQLite/PostgreSQL, you might run cleanup queries
    # For custom storage, implement cleanup logic

    logger.info(f"Cleaned up checkpoints older than {cutoff_date}")

def archive_completed_threads(graph, archive_threshold: int = 100):
    """Archive threads that have completed their workflow."""

    # Find completed threads
    completed_threads = []
    for thread_config in get_all_thread_configs(graph):
        state = graph.get_state(thread_config)
        if state and state.values.get("current_step") == "completed":
            completed_threads.append(thread_config)

    # Archive completed threads
    for thread_config in completed_threads:
        archive_thread(graph, thread_config)

    logger.info(f"Archived {len(completed_threads)} completed threads")
```

### Checkpoint Analytics

```python
def analyze_checkpoint_usage(graph):
    """Analyze checkpoint usage patterns."""

    stats = {
        "total_checkpoints": 0,
        "active_threads": 0,
        "completed_threads": 0,
        "failed_threads": 0,
        "average_session_length": 0,
        "storage_usage": "0MB"
    }

    # Collect statistics from checkpoint storage
    # This would vary based on your storage backend

    return stats

def generate_checkpoint_report(graph):
    """Generate a report on checkpoint usage."""

    stats = analyze_checkpoint_usage(graph)

    report = f"""
    Checkpoint Usage Report
    =======================
    Total Checkpoints: {stats['total_checkpoints']}
    Active Threads: {stats['active_threads']}
    Completed Threads: {stats['completed_threads']}
    Failed Threads: {stats['failed_threads']}
    Average Session Length: {stats['average_session_length']} steps
    Storage Usage: {stats['storage_usage']}
    """

    return report
```

## How It Works Under the Hood

### Checkpoint Structure

Each checkpoint contains:
1. **Configuration**: Thread ID and other config data
2. **State Values**: Your TypedDict data
3. **Metadata**: Timestamps, step info, custom data
4. **Graph Structure**: Node/edge information

```python
# Example checkpoint structure
{
    "config": {
        "configurable": {
            "thread_id": "user_123"
        }
    },
    "values": {
        "messages": [...],
        "current_step": "processing",
        "user_data": {...}
    },
    "metadata": {
        "timestamp": "2024-01-15T10:30:00Z",
        "step": 3,
        "source": "update"
    },
    "parent_config": {...}  # Previous checkpoint
}
```

### Persistence Flow

```mermaid
sequenceDiagram
    participant User
    participant Graph
    participant Checkpoint
    participant Storage

    User->>Graph: Execute step
    Graph->>Graph: Process state
    Graph->>Checkpoint: Create checkpoint
    Checkpoint->>Storage: Save to disk
    Storage->>Checkpoint: Confirm save
    Checkpoint->>Graph: Checkpoint saved
    Graph->>User: Return result

    Note over User,Storage: Later: Resume execution
    User->>Graph: Resume thread
    Graph->>Checkpoint: Load checkpoint
    Checkpoint->>Storage: Retrieve data
    Storage->>Checkpoint: Return data
    Checkpoint->>Graph: Restore state
    Graph->>User: Continue execution
```

## Best Practices for Persistence

### 1. Checkpoint Frequency

```python
# Checkpoint after important operations
def strategic_checkpointing(state):
    """Checkpoint only after significant state changes."""

    # Don't checkpoint for minor updates
    if state.get("minor_update"):
        return state

    # Checkpoint for major state changes
    if state.get("major_update"):
        # Save checkpoint here
        pass

    return state
```

### 2. State Size Management

```python
def optimize_state_size(state):
    """Keep state size manageable."""

    # Limit message history
    messages = state.get("messages", [])
    if len(messages) > 50:  # Keep only last 50 messages
        state["messages"] = messages[-50:]

    # Compress large data
    if "large_data" in state:
        state["large_data"] = compress_data(state["large_data"])

    return state
```

### 3. Thread Isolation

```python
def ensure_thread_isolation(graph, thread_config):
    """Ensure threads don't interfere with each other."""

    # Validate thread ID format
    thread_id = thread_config["configurable"]["thread_id"]
    if not thread_id.startswith("user_"):
        raise ValueError("Invalid thread ID format")

    # Check for thread conflicts
    existing_state = graph.get_state(thread_config)
    if existing_state and existing_state.metadata.get("locked"):
        raise ValueError("Thread is currently locked")

    return True
```

## Testing Persistent Applications

```python
def test_persistence_recovery():
    """Test that persistence works correctly."""

    # Create test graph
    test_graph = create_persistent_graph()

    # Execute initial state
    config = {"configurable": {"thread_id": "test_thread"}}
    initial_state = {"messages": [{"role": "user", "content": "Hello"}]}

    result1 = test_graph.invoke(initial_state, config)
    assert result1["current_step"] == "processed"

    # Simulate application restart
    # (In real test, you'd recreate the graph object)

    # Resume from checkpoint
    resume_state = {"messages": result1["messages"] + [{"role": "user", "content": "Continue"}]}

    result2 = test_graph.invoke(resume_state, config)
    assert result2["messages"] == resume_state["messages"]

def test_error_recovery():
    """Test error recovery with checkpoints."""

    # Create graph that might fail
    unreliable_graph = create_graph_with_failures()

    # Execute with error
    config = {"configurable": {"thread_id": "error_test"}}

    try:
        result = unreliable_graph.invoke({"data": "test"}, config)
    except Exception:
        pass  # Expected to fail

    # Verify checkpoint was saved with error state
    state = unreliable_graph.get_state(config)
    assert "error" in state.values
    assert state.values["error_count"] >= 1
```

## Production Deployment Considerations

### 1. Database Configuration

```python
# Production database configuration
PRODUCTION_DB_CONFIG = {
    "host": "prod-db-cluster.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "database": "langgraph_checkpoints",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "sslmode": "require"
}

def create_production_saver():
    """Create production-ready checkpoint saver."""
    conn_string = (
        f"postgresql://{PRODUCTION_DB_CONFIG['user']}:"
        f"{PRODUCTION_DB_CONFIG['password']}@"
        f"{PRODUCTION_DB_CONFIG['host']}:"
        f"{PRODUCTION_DB_CONFIG['port']}/"
        f"{PRODUCTION_DB_CONFIG['database']}"
        f"?sslmode={PRODUCTION_DB_CONFIG['sslmode']}"
    )

    return PostgresSaver.from_conn_string(conn_string)
```

### 2. Monitoring and Alerting

```python
def monitor_checkpoint_health(graph):
    """Monitor checkpoint system health."""

    metrics = {
        "checkpoint_save_time": 0,
        "checkpoint_load_time": 0,
        "storage_usage_percent": 0,
        "error_rate": 0
    }

    # Collect metrics from checkpoint operations
    # Alert if metrics exceed thresholds

    if metrics["error_rate"] > 0.05:  # 5% error rate
        alert_admin("High checkpoint error rate detected")

    if metrics["storage_usage_percent"] > 90:
        alert_admin("Checkpoint storage usage above 90%")

    return metrics
```

### 3. Backup and Recovery

```python
def backup_checkpoints(graph, backup_path: str):
    """Create backup of all checkpoints."""

    import shutil
    import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_path}/checkpoints_backup_{timestamp}.db"

    # For SQLite storage
    if isinstance(graph.checkpointer, SqliteSaver):
        shutil.copy(graph.checkpointer.db_path, backup_file)

    logger.info(f"Checkpoint backup created: {backup_file}")

def restore_from_backup(backup_file: str):
    """Restore checkpoints from backup."""

    # Restore logic depends on storage type
    # For production systems, consider point-in-time recovery

    logger.info(f"Checkpoints restored from: {backup_file}")
```

## What's Next?

Excellent work! You've mastered persistence and checkpoints in LangGraph. Your applications can now survive interruptions and resume seamlessly.

In our final chapter, we'll put it all together with **production deployment** - scaling your LangGraph applications, monitoring performance, and deploying to production environments.

Ready to deploy your persistent AI applications? Let's finish strong with [Chapter 8: Production Deployment](08-production-deployment.md)!

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## How it Works Under the Hood

Under the hood, `Chapter 7: Persistence and Checkpoints` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `state`.
2. **Input normalization**: shape incoming data so `checkpoint` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `graph`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `state` and `checkpoint` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Tool Integration](06-tool-integration.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
