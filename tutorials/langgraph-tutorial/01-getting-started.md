---
layout: default
title: "Chapter 1: Getting Started with LangGraph"
parent: "LangGraph Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with LangGraph

Welcome to LangGraph! If you've ever wanted to build complex AI applications with multiple interacting components and persistent state, you're in the right place. LangGraph is a powerful library that extends LangChain to provide fine-grained control over both the flow and state of your AI applications.

## What Makes LangGraph Special?

LangGraph revolutionizes AI application development by:

- **Stateful Applications** - Maintain state across multiple interactions
- **Multi-Actor Coordination** - Coordinate multiple AI agents and tools
- **Complex Control Flow** - Implement conditional logic and branching
- **Persistent Memory** - Remember context across sessions
- **Error Recovery** - Handle failures gracefully with checkpoints
- **Scalable Architecture** - Build production-ready AI systems

## Installing LangGraph

### Basic Installation

```bash
# Install LangGraph and LangChain (requires Python 3.9+)
pip install langgraph langchain langchain-openai

# Or install with additional dependencies
pip install langgraph[all]

# For development (includes LangGraph CLI - replaces deprecated LangGraph Studio Desktop)
pip install langgraph[dev] langgraph-cli

# Install LangGraph CLI separately for graph debugging and visualization
pip install langgraph-cli
```

> **Note (2025)**: LangGraph Studio Desktop is deprecated as of v0.0.37 (March 2025). Use `langgraph-cli` for local development, debugging, and visualization.

### Environment Setup

```bash
# Set up your environment variables
export OPENAI_API_KEY="your-openai-api-key"
export LANGCHAIN_API_KEY="your-langchain-api-key"  # Optional
```

## Your First LangGraph Application

Let's create your first stateful AI application:

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Optional

# Define the state structure
class AgentState(TypedDict):
    messages: list
    current_step: str
    result: Optional[str]

# Initialize the LLM
llm = ChatOpenAI(temperature=0.7)

# Define the first node (entry point)
def start_conversation(state: AgentState) -> AgentState:
    """Initialize the conversation"""
    welcome_message = "Hello! I'm your AI assistant. How can I help you today?"

    return {
        **state,
        "messages": [{"role": "assistant", "content": welcome_message}],
        "current_step": "gathered_input"
    }

# Define the processing node
def process_request(state: AgentState) -> AgentState:
    """Process user input and generate response"""
    user_message = state["messages"][-1]["content"] if len(state["messages"]) > 1 else ""

    # Generate AI response
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful AI assistant. Be concise and friendly."},
        {"role": "user", "content": user_message}
    ])

    return {
        **state,
        "messages": state["messages"] + [{"role": "assistant", "content": response.content}],
        "current_step": "completed",
        "result": response.content
    }

# Create the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("start", start_conversation)
graph.add_node("process", process_request)

# Define the flow
graph.set_entry_point("start")
graph.add_edge("start", "process")
graph.add_edge("process", END)

# Compile the graph
app = graph.compile()

# Test the application
initial_state = {
    "messages": [{"role": "user", "content": "Tell me about LangGraph"}],
    "current_step": "start",
    "result": None
}

result = app.invoke(initial_state)
print("Final result:", result["result"])
```

## Understanding LangGraph Concepts

### State Management

```python
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

# Define comprehensive state
class ComprehensiveState(TypedDict):
    # Conversation history
    messages: List[BaseMessage]

    # Application state
    current_task: Optional[str]
    completed_tasks: List[str]
    pending_tasks: List[str]

    # Context and memory
    user_context: dict
    session_memory: dict

    # Results and outputs
    final_result: Optional[str]
    intermediate_results: List[dict]

    # Error handling
    errors: List[str]
    retry_count: int
```

### Node Functions

```python
def example_node(state: ComprehensiveState) -> ComprehensiveState:
    """Example node that demonstrates state manipulation"""

    # Extract current state
    current_task = state.get("current_task")
    messages = state.get("messages", [])

    # Process based on current state
    if current_task == "analyze":
        # Perform analysis
        analysis_result = perform_analysis(messages)
        new_state = {
            **state,
            "intermediate_results": state.get("intermediate_results", []) + [analysis_result],
            "current_task": "summarize"
        }
    elif current_task == "summarize":
        # Generate summary
        summary = generate_summary(state.get("intermediate_results", []))
        new_state = {
            **state,
            "final_result": summary,
            "completed_tasks": state.get("completed_tasks", []) + ["analysis", "summary"]
        }
    else:
        new_state = state

    return new_state
```

## Building a Simple Chatbot

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List

class ChatState(TypedDict):
    messages: List[dict]
    conversation_stage: str

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

def handle_greeting(state: ChatState) -> ChatState:
    """Handle initial user greeting"""
    return {
        **state,
        "messages": state["messages"] + [
            {"role": "assistant", "content": "Hello! How can I assist you today?"}
        ],
        "conversation_stage": "awaiting_request"
    }

def process_user_input(state: ChatState) -> ChatState:
    """Process user input and generate response"""
    user_input = state["messages"][-1]["content"]

    # Generate AI response
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant. Keep responses concise."},
        {"role": "user", "content": user_input}
    ])

    return {
        **state,
        "messages": state["messages"] + [
            {"role": "assistant", "content": response.content}
        ],
        "conversation_stage": "response_given"
    }

def should_continue(state: ChatState) -> str:
    """Determine if conversation should continue"""
    last_message = state["messages"][-1]["content"].lower()

    if any(word in last_message for word in ["goodbye", "bye", "quit", "exit"]):
        return "end"
    else:
        return "continue"

# Create graph
chat_graph = StateGraph(ChatState)

# Add nodes
chat_graph.add_node("greet", handle_greeting)
chat_graph.add_node("process", process_user_input)

# Add edges
chat_graph.set_entry_point("greet")
chat_graph.add_edge("greet", "process")
chat_graph.add_conditional_edges(
    "process",
    should_continue,
    {
        "continue": "process",
        "end": END
    }
)

# Compile and test
chat_app = chat_graph.compile()

# Example conversation
conversation = chat_app.invoke({
    "messages": [{"role": "user", "content": "Hi there!"}],
    "conversation_stage": "greeting"
})

print("Conversation result:")
for msg in conversation["messages"]:
    print(f"{msg['role']}: {msg['content']}")
```

## Graph Visualization

```python
# Visualize your graph structure
from langgraph.graph import StateGraph
import json

def visualize_graph(graph: StateGraph) -> str:
    """Generate a simple text representation of the graph"""

    nodes = list(graph.nodes.keys())
    edges = []

    # Extract edges from the graph
    for node_name, node in graph.nodes.items():
        if hasattr(node, 'edges'):
            for edge in node.edges:
                edges.append((node_name, edge))

    # Create visualization
    visualization = "Graph Structure:\n"
    visualization += "Nodes: " + ", ".join(nodes) + "\n"
    visualization += "Edges:\n"

    for source, target in edges:
        visualization += f"  {source} -> {target}\n"

    return visualization

# Usage
print(visualize_graph(chat_graph))
```

## Error Handling and Debugging

```python
# Add error handling to your graph
def safe_node_execution(node_func):
    """Wrapper for safe node execution"""
    def wrapper(state):
        try:
            return node_func(state)
        except Exception as e:
            return {
                **state,
                "errors": state.get("errors", []) + [str(e)],
                "current_step": "error"
            }
    return wrapper

# Apply error handling
@safe_node_execution
def risky_node(state: ChatState) -> ChatState:
    """A node that might fail"""
    if len(state["messages"]) > 10:
        raise ValueError("Conversation too long")

    return {
        **state,
        "messages": state["messages"] + [
            {"role": "assistant", "content": "Processing..."}
        ]
    }

# Debug graph execution
def debug_graph_execution(graph, initial_state, max_steps=10):
    """Debug graph execution step by step"""
    state = initial_state
    step = 0

    print("Starting graph execution...")
    print(f"Initial state: {state}")

    while step < max_steps:
        try:
            new_state = graph.invoke(state)
            print(f"Step {step + 1}: {new_state}")

            if new_state == state:  # No change
                break

            state = new_state
            step += 1

        except Exception as e:
            print(f"Error at step {step + 1}: {e}")
            break

    return state
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed LangGraph** and set up your development environment
2. **Created your first stateful AI application** with persistent state
3. **Built a simple chatbot** with conditional logic and conversation flow
4. **Implemented comprehensive state management** with typed dictionaries
5. **Added error handling and debugging** capabilities
6. **Visualized graph structure** for better understanding

## Next Steps

Now that you understand LangGraph basics, let's explore state management in depth. In [Chapter 2: State Management](02-state-management.md), we'll dive into advanced state patterns, persistence, and memory management.

---

**Practice what you've learned:**
1. Create a custom chatbot for a specific domain
2. Add more complex conditional logic to your graph
3. Implement error recovery mechanisms
4. Build a multi-turn conversation system
5. Experiment with different state structures

*What kind of AI application will you build first with LangGraph?* 🤖
