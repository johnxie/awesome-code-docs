---
layout: default
title: "Letta Tutorial - Chapter 4: Tool Integration"
nav_order: 4
has_children: false
parent: Letta Tutorial
---

# Chapter 4: Tool Integration

Welcome to **Chapter 4: Tool Integration**. In this part of **Letta Tutorial: Stateful LLM Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Extend agent capabilities with custom tools, functions, and external integrations.

## Overview

Tools allow agents to interact with the external world - calling APIs, running code, accessing databases, and more. This chapter covers creating and integrating tools with Letta agents.

## Built-in Tools

Letta comes with several built-in tools:

```bash
# List available tools
letta list-tools

# Enable tools for an agent
letta update-agent --name researcher --tools web_search,web_scrape,save_file
```

### Common Built-in Tools

- **web_search**: Search the web for information
- **web_scrape**: Extract content from web pages
- **save_file**: Save content to files
- **run_terminal**: Execute shell commands
- **read_file**: Read file contents
- **send_email**: Send emails (requires SMTP config)

## Creating Custom Tools

Define custom functions that agents can call:

```python
from letta import create_client
import requests

client = create_client()

# Define a custom tool function
def weather_lookup(city: str) -> str:
    """Get current weather for a city."""
    api_key = "your-openweather-api-key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {description}"
    else:
        return f"Could not get weather for {city}"

# Register the tool
client.add_tool(
    name="weather_lookup",
    func=weather_lookup,
    description="Get current weather information for a city"
)
```

## Tool Schema and Parameters

Define tool parameters with proper typing:

```python
from typing import Optional
from pydantic import BaseModel

class WeatherParams(BaseModel):
    city: str
    units: Optional[str] = "metric"  # metric, imperial, or kelvin

def weather_lookup(params: WeatherParams) -> str:
    """Get weather with flexible units."""
    # Implementation here
    pass

# Register with schema
client.add_tool(
    name="weather_lookup",
    func=weather_lookup,
    description="Get current weather for a city",
    parameters=WeatherParams
)
```

## Adding Tools to Agents

Enable tools for specific agents:

```python
# Add tools when creating agent
agent = client.create_agent(
    name="weather-assistant",
    persona="You are a weather assistant who can look up current conditions.",
    tools=["weather_lookup"]
)

# Or update existing agent
client.update_agent_tools("weather-assistant", ["weather_lookup", "web_search"])
```

## Tool Calling in Conversations

Agents automatically use tools when appropriate:

```bash
$ letta chat --name weather-assistant
Human: What's the weather like in Tokyo?

Assistant: I'll check the current weather for Tokyo using the weather lookup tool.

[Using tool: weather_lookup]
Weather in Tokyo: 22°C, clear sky

Assistant: The weather in Tokyo is currently 22°C with clear skies.
```

## Advanced Tool Examples

### Database Query Tool

```python
import sqlite3
from typing import List, Dict, Any

def query_database(query: str) -> List[Dict[str, Any]]:
    """Execute a read-only SQL query."""
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    finally:
        conn.close()

client.add_tool(
    name="query_database",
    func=query_database,
    description="Execute SQL queries on the company database (read-only)"
)
```

### Code Execution Tool

```python
import subprocess
import sys
from typing import Optional

def run_python_code(code: str, timeout: Optional[int] = 30) -> str:
    """Execute Python code safely."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"

        return output
    except subprocess.TimeoutExpired:
        return "Code execution timed out"
    except Exception as e:
        return f"Execution error: {str(e)}"

client.add_tool(
    name="run_python_code",
    func=run_python_code,
    description="Execute Python code and return the output"
)
```

### API Integration Tool

```python
import requests
from typing import Dict, Any, Optional

def call_rest_api(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make HTTP requests to REST APIs."""
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers or {},
            json=data,
            timeout=10
        )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "json": response.json() if response.headers.get("content-type", "").startswith("application/json") else None
        }
    except Exception as e:
        return {"error": str(e)}

client.add_tool(
    name="call_rest_api",
    func=call_rest_api,
    description="Make HTTP requests to REST APIs"
)
```

## Tool Safety and Permissions

Implement safety measures:

```python
def safe_shell_command(command: str) -> str:
    """Execute safe shell commands only."""
    # Whitelist of allowed commands
    allowed_commands = ["ls", "pwd", "echo", "cat", "head", "tail", "grep"]

    cmd_base = command.split()[0]

    if cmd_base not in allowed_commands:
        return f"Command '{cmd_base}' is not allowed"

    # Additional safety checks
    if "rm" in command or ">" in command or "|" in command:
        return "Potentially dangerous command blocked"

    # Execute safely
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
    return result.stdout or result.stderr

client.add_tool(
    name="safe_shell",
    func=safe_shell_command,
    description="Execute safe shell commands from an approved list"
)
```

## Tool Discovery and Documentation

Help agents understand available tools:

```python
# Get all available tools
tools = client.list_tools()

for tool in tools:
    print(f"Tool: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Parameters: {tool.parameters}")
    print("---")
```

## Composing Tools

Create complex workflows by combining tools:

```python
def research_topic(topic: str) -> str:
    """Research a topic using multiple tools."""
    # Step 1: Search the web
    search_results = client.call_tool("web_search", {"query": topic})

    # Step 2: Extract key information
    key_info = client.call_tool("summarize_text", {"text": search_results})

    # Step 3: Save to file
    client.call_tool("save_file", {
        "filename": f"{topic}_research.txt",
        "content": key_info
    })

    return f"Research completed for {topic}"

client.add_tool(
    name="research_topic",
    func=research_topic,
    description="Complete research workflow: search, summarize, and save"
)
```

## Tool Error Handling

Handle tool failures gracefully:

```python
def robust_web_search(query: str) -> str:
    """Web search with fallback."""
    try:
        result = client.call_tool("web_search", {"query": query})
        return result
    except Exception as e:
        # Fallback to alternative search
        try:
            return client.call_tool("alternative_search", {"query": query})
        except Exception as e2:
            return f"Search failed: {str(e)}, fallback also failed: {str(e2)}"

client.add_tool(
    name="robust_web_search",
    func=robust_web_search,
    description="Web search with automatic fallback"
)
```

## Testing Tools

Create test suites for tool validation:

```python
def test_weather_tool():
    """Test the weather lookup tool."""
    result = client.call_tool("weather_lookup", {"city": "London"})

    assert "London" in result
    assert "°C" in result or "°F" in result
    print("Weather tool test passed")

def test_database_tool():
    """Test database query tool."""
    result = client.call_tool("query_database", {"query": "SELECT COUNT(*) FROM users"})

    assert isinstance(result, list)
    assert len(result) > 0
    print("Database tool test passed")

# Run tests
test_weather_tool()
test_database_tool()
```

## Tool Performance Monitoring

Track tool usage and performance:

```python
import time

def monitored_tool_call(tool_name: str, **kwargs):
    """Monitor tool performance."""
    start_time = time.time()

    try:
        result = client.call_tool(tool_name, kwargs)
        duration = time.time() - start_time

        # Log performance
        client.add_to_archival_memory(
            "system",
            f"Tool {tool_name} called successfully in {duration:.2f}s"
        )

        return result
    except Exception as e:
        duration = time.time() - start_time
        client.add_to_archival_memory(
            "system",
            f"Tool {tool_name} failed after {duration:.2f}s: {str(e)}"
        )
        raise
```

## Best Practices

1. **Security First**: Always validate inputs and restrict dangerous operations
2. **Error Handling**: Implement robust error handling and fallbacks
3. **Documentation**: Provide clear descriptions and parameter documentation
4. **Testing**: Thoroughly test tools before production use
5. **Monitoring**: Track tool performance and usage patterns
6. **Modularity**: Keep tools focused on single responsibilities
7. **Versioning**: Version tools and handle backward compatibility

Next: Manage long-running conversations and context.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `client`, `result`, `weather` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Tool Integration` as an operating subsystem inside **Letta Tutorial: Stateful LLM Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `tool`, `description`, `name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Tool Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `client`.
2. **Input normalization**: shape incoming data so `result` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `weather`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/letta-ai/letta)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `client` and `result` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Agent Configuration](03-configuration.md)
- [Next Chapter: Chapter 5: Conversation Management](05-conversations.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
