---
layout: default
title: "Chapter 3: Nodes and Edges"
parent: "LangGraph Tutorial"
nav_order: 3
---

# Chapter 3: Nodes and Edges

Welcome to the building blocks of LangGraph! This chapter dives deep into nodes and edges - the fundamental components that make up your graph-based AI applications. Understanding these concepts is crucial for building sophisticated workflows.

## Understanding Nodes

Nodes are the computational units in your LangGraph. Each node represents a specific function or operation that processes the current state and returns an updated state.

### Basic Node Structure

```python
from typing import TypedDict, Any
from langgraph.graph import StateGraph

class GraphState(TypedDict):
    messages: list
    current_step: str
    data: dict

def basic_node(state: GraphState) -> GraphState:
    """A basic node that processes state and returns updated state"""
    # Extract current state
    messages = state.get("messages", [])
    current_step = state.get("current_step", "start")

    # Perform some processing
    processed_data = process_messages(messages)

    # Return updated state
    return {
        **state,
        "messages": messages + [{"role": "system", "content": "Processing complete"}],
        "current_step": "processed",
        "data": {**state.get("data", {}), "processed_result": processed_data}
    }

def process_messages(messages: list) -> str:
    """Helper function for message processing"""
    return f"Processed {len(messages)} messages"
```

### Node Types and Patterns

```python
# 1. Processing Node
def data_processor_node(state: GraphState) -> GraphState:
    """Node focused on data processing"""
    data = state.get("data", {})
    processed = transform_data(data)

    return {
        **state,
        "data": processed,
        "processing_history": state.get("processing_history", []) + ["data_processed"]
    }

# 2. Decision Node
def decision_node(state: GraphState) -> GraphState:
    """Node that makes decisions based on state"""
    score = calculate_confidence_score(state)

    return {
        **state,
        "decision": "high_confidence" if score > 0.8 else "low_confidence",
        "confidence_score": score
    }

# 3. Communication Node
def communication_node(state: GraphState) -> GraphState:
    """Node that handles external communication"""
    result = send_external_request(state.get("data", {}))

    return {
        **state,
        "external_response": result,
        "communication_log": state.get("communication_log", []) + [result]
    }

# 4. Validation Node
def validation_node(state: GraphState) -> GraphState:
    """Node that validates state and data"""
    errors = validate_state(state)

    return {
        **state,
        "validation_errors": errors,
        "is_valid": len(errors) == 0
    }
```

## Advanced Node Patterns

### Async Nodes

```python
import asyncio
from typing import Awaitable

async def async_processing_node(state: GraphState) -> GraphState:
    """Asynchronous node for I/O operations"""
    data = state.get("data", {})

    # Simulate async operation
    await asyncio.sleep(1)
    result = await fetch_external_data(data.get("query"))

    return {
        **state,
        "async_result": result,
        "processing_time": "1s"
    }

async def fetch_external_data(query: str) -> dict:
    """Simulate external API call"""
    await asyncio.sleep(0.5)  # Simulate network delay
    return {"query": query, "result": f"Data for {query}"}
```

### Conditional Nodes

```python
def conditional_processing_node(state: GraphState) -> GraphState:
    """Node that processes differently based on conditions"""
    condition = state.get("condition", "default")
    data = state.get("data", {})

    if condition == "text_processing":
        result = process_text(data)
    elif condition == "data_analysis":
        result = analyze_data(data)
    elif condition == "image_processing":
        result = process_image(data)
    else:
        result = default_processing(data)

    return {
        **state,
        "processed_data": result,
        "processing_type": condition
    }
```

### Composite Nodes

```python
def composite_node(state: GraphState) -> GraphState:
    """Node that combines multiple operations"""
    # Step 1: Validate input
    if not validate_input(state):
        return {**state, "error": "Invalid input"}

    # Step 2: Process data
    processed = process_data(state.get("data", {}))

    # Step 3: Generate summary
    summary = generate_summary(processed)

    # Step 4: Update state
    return {
        **state,
        "processed_data": processed,
        "summary": summary,
        "composite_steps_completed": ["validation", "processing", "summary"]
    }
```

## Understanding Edges

Edges define the flow between nodes in your graph. They determine which node executes after another based on conditions or state.

### Basic Edge Types

```python
from langgraph.graph import StateGraph, END

# Create graph
graph = StateGraph(GraphState)

# Add nodes
graph.add_node("start", start_node)
graph.add_node("process", processing_node)
graph.add_node("validate", validation_node)
graph.add_node("end", end_node)

# Basic edges
graph.set_entry_point("start")  # Entry point
graph.add_edge("start", "process")  # Direct connection
graph.add_edge("process", "validate")  # Sequential flow
graph.add_edge("validate", END)  # Exit point
```

### Conditional Edges

```python
def route_based_on_validation(state: GraphState) -> str:
    """Determine next node based on validation result"""
    is_valid = state.get("is_valid", False)
    error_count = len(state.get("validation_errors", []))

    if not is_valid:
        if error_count > 3:
            return "error_handler"
        else:
            return "retry_validation"
    else:
        return "success_handler"

# Add conditional edges
graph.add_conditional_edges(
    "validate",
    route_based_on_validation,
    {
        "error_handler": "handle_error",
        "retry_validation": "validate",
        "success_handler": "process_success"
    }
)
```

### Parallel Edges

```python
# Create parallel processing paths
graph.add_edge("start", "path_a_processor")
graph.add_edge("start", "path_b_processor")

# Converge paths
def combine_results(state: GraphState) -> GraphState:
    """Combine results from parallel processing"""
    path_a_result = state.get("path_a_result")
    path_b_result = state.get("path_b_result")

    combined = merge_results(path_a_result, path_b_result)

    return {
        **state,
        "combined_result": combined,
        "parallel_processing_complete": True
    }

graph.add_node("combiner", combine_results)
graph.add_edge("path_a_processor", "combiner")
graph.add_edge("path_b_processor", "combiner")
```

## Building Complex Graph Structures

### Sequential Processing Pipeline

```python
def create_processing_pipeline() -> StateGraph:
    """Create a sequential processing pipeline"""

    class PipelineState(TypedDict):
        data: dict
        pipeline_steps: list
        current_step: str
        results: dict

    graph = StateGraph(PipelineState)

    # Define pipeline steps
    def step1_ingest(state: PipelineState) -> PipelineState:
        return {**state, "pipeline_steps": ["ingest"], "current_step": "ingest"}

    def step2_validate(state: PipelineState) -> PipelineState:
        return {**state, "pipeline_steps": state["pipeline_steps"] + ["validate"], "current_step": "validate"}

    def step3_process(state: PipelineState) -> PipelineState:
        return {**state, "pipeline_steps": state["pipeline_steps"] + ["process"], "current_step": "process"}

    def step4_output(state: PipelineState) -> PipelineState:
        return {**state, "pipeline_steps": state["pipeline_steps"] + ["output"], "current_step": "complete"}

    # Add nodes
    graph.add_node("ingest", step1_ingest)
    graph.add_node("validate", step2_validate)
    graph.add_node("process", step3_process)
    graph.add_node("output", step4_output)

    # Create sequential flow
    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "validate")
    graph.add_edge("validate", "process")
    graph.add_edge("process", "output")
    graph.add_edge("output", END)

    return graph
```

### Branching Workflow

```python
def create_branching_workflow() -> StateGraph:
    """Create a workflow with conditional branching"""

    class WorkflowState(TypedDict):
        task_type: str
        priority: str
        assigned_to: str
        status: str

    graph = StateGraph(WorkflowState)

    def triage_task(state: WorkflowState) -> WorkflowState:
        """Determine task routing based on priority and type"""
        priority = state.get("priority", "medium")
        task_type = state.get("task_type", "general")

        if priority == "high":
            return {**state, "assigned_to": "senior_engineer", "status": "escalated"}
        elif task_type == "bug":
            return {**state, "assigned_to": "qa_engineer", "status": "assigned"}
        else:
            return {**state, "assigned_to": "junior_engineer", "status": "assigned"}

    def senior_engineer_process(state: WorkflowState) -> WorkflowState:
        return {**state, "status": "in_review"}

    def qa_engineer_process(state: WorkflowState) -> WorkflowState:
        return {**state, "status": "testing"}

    def junior_engineer_process(state: WorkflowState) -> WorkflowState:
        return {**state, "status": "developing"}

    # Add nodes
    graph.add_node("triage", triage_task)
    graph.add_node("senior_process", senior_engineer_process)
    graph.add_node("qa_process", qa_engineer_process)
    graph.add_node("junior_process", junior_engineer_process)

    # Define routing logic
    def route_task(state: WorkflowState) -> str:
        assigned_to = state.get("assigned_to")
        if assigned_to == "senior_engineer":
            return "senior_process"
        elif assigned_to == "qa_engineer":
            return "qa_process"
        else:
            return "junior_process"

    # Set up flow
    graph.set_entry_point("triage")
    graph.add_conditional_edges(
        "triage",
        route_task,
        {
            "senior_process": "senior_process",
            "qa_process": "qa_process",
            "junior_process": "junior_process"
        }
    )

    # All paths lead to end
    graph.add_edge("senior_process", END)
    graph.add_edge("qa_process", END)
    graph.add_edge("junior_process", END)

    return graph
```

## Error Handling in Nodes and Edges

```python
class GraphError(Exception):
    """Custom error for graph operations"""
    pass

def error_handling_node(state: GraphState) -> GraphState:
    """Node with comprehensive error handling"""
    try:
        # Attempt processing
        result = risky_operation(state)

        return {
            **state,
            "result": result,
            "status": "success"
        }

    except ValueError as e:
        return {
            **state,
            "error": str(e),
            "error_type": "validation_error",
            "status": "error",
            "retry_count": state.get("retry_count", 0) + 1
        }

    except ConnectionError as e:
        return {
            **state,
            "error": str(e),
            "error_type": "connection_error",
            "status": "retry",
            "retry_count": state.get("retry_count", 0) + 1
        }

    except Exception as e:
        return {
            **state,
            "error": str(e),
            "error_type": "unknown_error",
            "status": "failed"
        }

def route_with_error_handling(state: GraphState) -> str:
    """Route based on processing status"""
    status = state.get("status", "unknown")
    retry_count = state.get("retry_count", 0)

    if status == "success":
        return "success_handler"
    elif status == "error" and retry_count < 3:
        return "retry_node"
    elif status == "retry" and retry_count < 5:
        return "retry_with_backoff"
    else:
        return "error_handler"
```

## Graph Visualization and Debugging

```python
def visualize_graph_structure(graph: StateGraph) -> str:
    """Generate a text-based visualization of the graph"""
    nodes = list(graph.nodes.keys())

    visualization = "Graph Structure:\n"
    visualization += f"Nodes ({len(nodes)}): {', '.join(nodes)}\n\n"

    # Show entry point
    if hasattr(graph, '_entry_point'):
        visualization += f"Entry Point: {graph._entry_point}\n"

    # Show edges
    visualization += "\nEdges:\n"
    for node_name in nodes:
        if hasattr(graph.nodes[node_name], 'edges'):
            edges = graph.nodes[node_name].edges
            if edges:
                for edge in edges:
                    visualization += f"  {node_name} -> {edge}\n"

    return visualization

def debug_graph_execution(graph: StateGraph, initial_state: dict, max_steps: int = 10):
    """Debug graph execution with detailed logging"""
    state = initial_state
    step = 0
    execution_log = []

    execution_log.append(f"Initial state: {state}")

    while step < max_steps:
        try:
            # Get current node
            current_node = determine_current_node(state)
            execution_log.append(f"Step {step + 1}: Executing node '{current_node}'")

            # Execute node
            node_function = graph.nodes[current_node]
            new_state = node_function(state)

            execution_log.append(f"Step {step + 1} result: {new_state}")

            # Check for completion
            if new_state.get("status") == "completed":
                execution_log.append("Graph execution completed successfully")
                break

            state = new_state
            step += 1

        except Exception as e:
            execution_log.append(f"Error at step {step + 1}: {e}")
            break

    return state, execution_log

def determine_current_node(state: dict) -> str:
    """Determine which node should execute next based on state"""
    # This is a simplified version - actual implementation would be more complex
    current_step = state.get("current_step", "start")

    node_mapping = {
        "start": "start_node",
        "processing": "process_node",
        "validating": "validate_node",
        "completed": "end_node"
    }

    return node_mapping.get(current_step, "start_node")
```

## Performance Optimization

```python
# Optimized node with caching
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_processing_node(cache_key: str, state_data: str) -> dict:
    """Node with built-in caching"""
    state = eval(state_data)  # In production, use safe deserialization

    # Expensive computation
    result = expensive_computation(state)

    return result

def optimized_node(state: GraphState) -> GraphState:
    """Optimized node with caching"""
    # Create cache key
    state_str = str(sorted(state.items()))
    cache_key = hashlib.md5(state_str.encode()).hexdigest()

    # Check cache
    cached_result = cached_processing_node(cache_key, state_str)

    if cached_result:
        return {**state, **cached_result}

    # Compute if not cached
    result = expensive_computation(state)

    return {**state, **result}

def expensive_computation(state: dict) -> dict:
    """Simulate expensive computation"""
    import time
    time.sleep(0.1)  # Simulate processing time
    return {"computed_result": "processed", "computation_time": 0.1}
```

## What We've Accomplished

Excellent! 🎉 You've mastered nodes and edges in LangGraph:

1. **Created various node types** - processing, decision, communication, validation
2. **Built advanced node patterns** - async, conditional, composite nodes
3. **Implemented edge types** - basic, conditional, and parallel edges
4. **Constructed complex graph structures** - pipelines and branching workflows
5. **Added comprehensive error handling** - custom errors and recovery mechanisms
6. **Created visualization tools** - graph structure debugging
7. **Optimized performance** - caching and efficient processing

## Next Steps

Ready for conditional logic and decision-making? In [Chapter 4: Conditional Logic](04-conditional-logic.md), we'll explore advanced routing, decision trees, and dynamic graph modification!

---

**Practice what you've learned:**
1. Build a custom node for your specific use case
2. Create a complex branching workflow with multiple paths
3. Implement error recovery with automatic retries
4. Add performance monitoring to your nodes
5. Build a visualization tool for your graphs

*What's the most complex graph structure you'll build?* 🔀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `state`, `graph`, `GraphState` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Nodes and Edges` as an operating subsystem inside **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `result`, `status`, `add_edge` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Nodes and Edges` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `state`.
2. **Input normalization**: shape incoming data so `graph` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `GraphState`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `state` and `graph` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: State Management](02-state-management.md)
- [Next Chapter: Chapter 4: Conditional Logic](04-conditional-logic.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
