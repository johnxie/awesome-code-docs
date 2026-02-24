---
layout: default
title: "Chapter 6: Tool Integration"
parent: "LangGraph Tutorial"
nav_order: 6
---

# Chapter 6: Tool Integration

Welcome to **Chapter 6: Tool Integration**. In this part of **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! By now you understand how to build graphs with nodes, edges, and conditional logic. But real-world AI applications need to interact with the world - calling APIs, querying databases, and using external services. This is where **tool integration** comes in!

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `state`, `result`, `tool` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Tool Integration` as an operating subsystem inside **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `messages`, `tool_results`, `tools` as your checklist when adapting these patterns to your own repository.

## Understanding Tool Integration in LangGraph

Tools in LangGraph are functions that your AI agents can call during graph execution. They allow your graphs to interact with external systems and perform real-world tasks.

### Basic Tool Structure

```python
from langchain_core.tools import tool
from typing import Any, Dict

@tool
def search_weather(location: str) -> str:
    """Search for current weather conditions in a location."""
    # Your weather API call here
    return f"Weather in {location}: Sunny, 75°F"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    # Email sending logic here
    return f"Email sent to {to} successfully"
```

### Integrating Tools with LangGraph

```python
from langgraph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

class ToolState(TypedDict):
    messages: List[Dict[str, Any]]
    current_tools: List[str]
    tool_results: Dict[str, Any]

# Create tool-enabled LLM
llm = ChatOpenAI(temperature=0.7)
tools = [search_weather, send_email]
llm_with_tools = llm.bind_tools(tools)

def tool_node(state: ToolState) -> ToolState:
    """Execute tools based on LLM decisions."""
    messages = state["messages"]
    result = llm_with_tools.invoke(messages)

    # Check if tools were called
    if hasattr(result, 'tool_calls') and result.tool_calls:
        tool_results = {}
        for tool_call in result.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Execute the tool
            if tool_name == "search_weather":
                result = search_weather.invoke(tool_args)
            elif tool_name == "send_email":
                result = send_email.invoke(tool_args)

            tool_results[tool_name] = result

        return {
            **state,
            "messages": messages + [result],
            "tool_results": tool_results
        }

    return state
```

## Tool Categories and Patterns

### 1. API Tools

```python
@tool
def github_search(query: str, language: str = "python") -> str:
    """Search GitHub repositories."""
    import requests

    url = f"https://api.github.com/search/repositories"
    params = {
        "q": f"{query} language:{language}",
        "sort": "stars",
        "order": "desc"
    }

    response = requests.get(url, params=params)
    repos = response.json()["items"][:5]

    results = []
    for repo in repos:
        results.append(f"- {repo['full_name']}: {repo['description']}")

    return "\n".join(results)
```

### 2. Database Tools

```python
from sqlalchemy import create_engine, text

@tool
def query_database(sql_query: str) -> str:
    """Execute SQL queries on the database."""
    engine = create_engine("postgresql://user:pass@localhost/db")

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()

        # Format results
        if rows:
            headers = result.keys()
            formatted_rows = [dict(zip(headers, row)) for row in rows]
            return str(formatted_rows)
        else:
            return "No results found"

    except Exception as e:
        return f"Database error: {str(e)}"
```

### 3. File System Tools

```python
import os
from pathlib import Path

@tool
def list_directory(path: str = ".") -> str:
    """List contents of a directory."""
    try:
        entries = []
        for item in Path(path).iterdir():
            entry_type = "DIR" if item.is_dir() else "FILE"
            entries.append(f"{entry_type}: {item.name}")

        return "\n".join(entries)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@tool
def read_file(file_path: str) -> str:
    """Read contents of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content[:1000] + "..." if len(content) > 1000 else content
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

## Advanced Tool Integration Patterns

### Tool Selection and Routing

```python
def route_to_tool(state: ToolState) -> str:
    """Route to appropriate tool based on user request."""
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()

    if any(word in last_message for word in ["weather", "temperature", "forecast"]):
        return "weather_tool"
    elif any(word in last_message for word in ["email", "send", "mail"]):
        return "email_tool"
    elif any(word in last_message for word in ["search", "find", "lookup"]):
        return "search_tool"
    else:
        return "general_tool"
```

### Tool Result Processing

```python
def process_tool_results(state: ToolState) -> ToolState:
    """Process and format tool execution results."""
    tool_results = state.get("tool_results", {})

    processed_results = {}
    for tool_name, result in tool_results.items():
        if isinstance(result, str):
            # Clean up the result
            processed_results[tool_name] = result.strip()
        elif isinstance(result, dict):
            # Format dictionary results
            processed_results[tool_name] = "\n".join([f"{k}: {v}" for k, v in result.items()])
        else:
            processed_results[tool_name] = str(result)

    return {
        **state,
        "processed_results": processed_results,
        "messages": state["messages"] + [
            {"role": "system", "content": f"Tool results: {processed_results}"}
        ]
    }
```

### Error Handling in Tool Execution

```python
def safe_tool_execution(state: ToolState) -> ToolState:
    """Execute tools with error handling."""
    try:
        # Tool execution logic
        result = execute_tools(state)
        return {
            **state,
            "tool_results": result,
            "execution_status": "success"
        }
    except Exception as e:
        return {
            **state,
            "error": str(e),
            "execution_status": "failed",
            "messages": state["messages"] + [
                {"role": "system", "content": f"Tool execution failed: {str(e)}"}
            ]
        }
```

## Building a Complete Tool-Integrated Graph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

class ToolIntegratedState(TypedDict):
    messages: List[Dict[str, Any]]
    available_tools: List[str]
    tool_results: Dict[str, Any]
    current_step: str

# Define tools
tools = [search_weather, send_email, github_search, query_database]

def analyze_request(state: ToolIntegratedState) -> ToolIntegratedState:
    """Analyze user request to determine needed tools."""
    messages = state["messages"]
    last_message = messages[-1]["content"]

    # Simple tool detection logic
    needed_tools = []
    if "weather" in last_message.lower():
        needed_tools.append("search_weather")
    if "email" in last_message.lower():
        needed_tools.append("send_email")
    if "github" in last_message.lower() or "repository" in last_message.lower():
        needed_tools.append("github_search")

    return {
        **state,
        "needed_tools": needed_tools,
        "current_step": "tools_identified"
    }

def execute_tools(state: ToolIntegratedState) -> ToolIntegratedState:
    """Execute identified tools."""
    needed_tools = state.get("needed_tools", [])
    tool_results = {}

    for tool_name in needed_tools:
        if tool_name == "search_weather":
            result = search_weather.invoke({"location": "New York"})
        elif tool_name == "send_email":
            result = send_email.invoke({
                "to": "user@example.com",
                "subject": "Test",
                "body": "Hello!"
            })
        elif tool_name == "github_search":
            result = github_search.invoke({"query": "machine learning"})

        tool_results[tool_name] = result

    return {
        **state,
        "tool_results": tool_results,
        "current_step": "tools_executed"
    }

def format_response(state: ToolIntegratedState) -> ToolIntegratedState:
    """Format tool results into final response."""
    tool_results = state.get("tool_results", {})

    response_parts = []
    for tool_name, result in tool_results.items():
        response_parts.append(f"**{tool_name.replace('_', ' ').title()}:**\n{result}")

    final_response = "\n\n".join(response_parts)

    return {
        **state,
        "final_response": final_response,
        "messages": state["messages"] + [
            {"role": "assistant", "content": final_response}
        ]
    }

# Build the graph
graph = StateGraph(ToolIntegratedState)

graph.add_node("analyze", analyze_request)
graph.add_node("execute", execute_tools)
graph.add_node("format", format_response)

graph.set_entry_point("analyze")
graph.add_edge("analyze", "execute")
graph.add_edge("execute", "format")
graph.add_edge("format", END)

tool_graph = graph.compile()
```

## Tool Integration Best Practices

### 1. Tool Documentation

```python
@tool
def complex_calculation(a: float, b: float, operation: str) -> str:
    """
    Perform complex mathematical calculations.

    Args:
        a: First number
        b: Second number
        operation: One of 'add', 'subtract', 'multiply', 'divide'

    Returns:
        String representation of the result

    Examples:
        complex_calculation(5, 3, "add") -> "Result: 8"
    """
    # Implementation here
    pass
```

### 2. Input Validation

```python
from pydantic import BaseModel, Field

class WeatherQuery(BaseModel):
    location: str = Field(..., description="City or location name")
    units: str = Field(default="celsius", description="Temperature units")

@tool
def validated_weather_search(query: WeatherQuery) -> str:
    """Search weather with validated input."""
    # Your weather API logic here
    return f"Weather for {query.location} in {query.units}"
```

### 3. Rate Limiting and Caching

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
@tool
def cached_api_call(endpoint: str) -> str:
    """Make API calls with caching to avoid rate limits."""
    # Implementation with caching
    pass

def rate_limited_tool(state):
    """Implement rate limiting logic."""
    last_call = state.get("last_tool_call", 0)
    current_time = time.time()

    if current_time - last_call < 1:  # 1 second rate limit
        return {**state, "rate_limited": True}

    # Execute tool
    return {**state, "last_tool_call": current_time}
```

## How It Works Under the Hood

### Tool Calling Mechanism

When an LLM decides to use a tool, it generates a special message containing:
1. **Tool Name**: Which tool to execute
2. **Tool Arguments**: Parameters for the tool
3. **Tool ID**: Unique identifier for tracking

```python
# Example of what the LLM generates
{
    "tool_calls": [
        {
            "id": "call_123",
            "type": "function",
            "function": {
                "name": "search_weather",
                "arguments": '{"location": "San Francisco"}'
            }
        }
    ]
}
```

### Tool Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Graph
    participant LLM
    participant Tool
    participant API

    User->>Graph: Send request
    Graph->>LLM: Process with tools
    LLM->>Graph: Tool call decision
    Graph->>Tool: Execute tool
    Tool->>API: Make API call
    API->>Tool: Return data
    Tool->>Graph: Tool result
    Graph->>LLM: Process result
    LLM->>Graph: Final response
    Graph->>User: Formatted response
```

## Common Tool Integration Patterns

### 1. Sequential Tool Execution

```python
def sequential_tools(state):
    """Execute tools in sequence."""
    # Tool 1: Gather data
    data = gather_data_tool.invoke(state)

    # Tool 2: Process data
    processed = process_data_tool.invoke({"data": data})

    # Tool 3: Format results
    result = format_results_tool.invoke({"processed": processed})

    return {**state, "final_result": result}
```

### 2. Parallel Tool Execution

```python
import asyncio

async def parallel_tools(state):
    """Execute multiple tools in parallel."""
    tasks = [
        weather_tool.invoke_async({"location": "NYC"}),
        news_tool.invoke_async({"topic": "technology"}),
        stock_tool.invoke_async({"symbol": "AAPL"})
    ]

    results = await asyncio.gather(*tasks)
    return {**state, "parallel_results": results}
```

### 3. Conditional Tool Selection

```python
def conditional_tools(state):
    """Choose tools based on conditions."""
    confidence = analyze_confidence(state)

    if confidence > 0.9:
        return use_precise_tool(state)
    elif confidence > 0.7:
        return use_balanced_tool(state)
    else:
        return use_fallback_tool(state)
```

## Testing Tool Integration

```python
def test_tool_integration():
    """Test tool integration with mock data."""

    # Mock tool for testing
    @tool
    def mock_weather(location: str) -> str:
        return f"Mock weather for {location}: 72°F, Sunny"

    # Test state
    test_state = {
        "messages": [{"role": "user", "content": "What's the weather in Paris?"}],
        "available_tools": ["mock_weather"]
    }

    # Test graph execution
    result = tool_graph.invoke(test_state)

    assert "Paris" in result["final_response"]
    assert result["execution_status"] == "success"
```

## Production Considerations

### 1. Tool Security

- Validate all tool inputs
- Implement authentication for external APIs
- Use API keys securely (environment variables)
- Log tool usage for monitoring

### 2. Error Handling

```python
def robust_tool_execution(state):
    """Execute tools with comprehensive error handling."""
    try:
        result = execute_tool_with_timeout(state, timeout=30)
        return {**state, "result": result, "status": "success"}
    except TimeoutError:
        return {**state, "error": "Tool execution timed out", "status": "timeout"}
    except Exception as e:
        return {**state, "error": str(e), "status": "failed"}
```

### 3. Monitoring and Logging

```python
def monitored_tool_execution(state):
    """Execute tools with monitoring."""
    start_time = time.time()

    # Log tool execution start
    logger.info(f"Starting tool execution: {state.get('current_tool')}")

    result = execute_tool(state)

    execution_time = time.time() - start_time

    # Log completion
    logger.info(f"Tool execution completed in {execution_time:.2f}s")

    return {
        **state,
        "result": result,
        "execution_time": execution_time,
        "timestamp": time.time()
    }
```

## What's Next?

Great job! You've learned how to integrate external tools with your LangGraph applications. This opens up endless possibilities for building practical AI systems.

In the next chapter, we'll explore **persistence and checkpoints** - how to save and restore your graph's state across executions. This is crucial for building reliable, resumable AI applications.

Ready to make your graphs persistent? Let's continue to [Chapter 7: Persistence and Checkpoints](07-persistence-checkpoints.md)!

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## How it Works Under the Hood

Under the hood, `Chapter 6: Tool Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `state`.
2. **Input normalization**: shape incoming data so `result` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `tool`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `state` and `result` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Multi-Agent Systems](05-multi-agent-systems.md)
- [Next Chapter: Chapter 7: Persistence and Checkpoints](07-persistence-checkpoints.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
