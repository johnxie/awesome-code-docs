---
layout: default
title: "Chapter 3: Tool Integration"
parent: "SuperAGI Tutorial"
nav_order: 3
---

# Chapter 3: Tool Integration

Welcome to **Chapter 3: Tool Integration**. In this part of **SuperAGI Tutorial: Production-Ready Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Connect SuperAGI agents to external tools, APIs, and services for enhanced capabilities.

## Overview

Tools extend agent capabilities beyond text generation, enabling them to interact with external systems, access real-time data, execute code, and perform actions in the real world. This chapter covers built-in tools, custom tool development, and best practices for tool integration.

## Built-in Tools

### Web Tools

```python
from superagi.tools import (
    WebSearchTool,
    WebScraperTool,
    WebBrowserTool
)

# Web Search Tool
search_tool = WebSearchTool(
    name="web_search",
    description="Search the web for information",
    config={
        "search_engine": "google",  # google, bing, duckduckgo
        "max_results": 10,
        "safe_search": True
    }
)

# Execute search
results = search_tool.execute({
    "query": "latest developments in AI agents",
    "num_results": 5
})

print(f"Found {len(results['results'])} results")
for result in results['results']:
    print(f"- {result['title']}: {result['url']}")


# Web Scraper Tool
scraper_tool = WebScraperTool(
    name="web_scraper",
    description="Extract content from web pages",
    config={
        "timeout": 30,
        "extract_images": False,
        "convert_to_markdown": True
    }
)

content = scraper_tool.execute({
    "url": "https://example.com/article",
    "selectors": {
        "title": "h1",
        "content": "article",
        "author": ".author-name"
    }
})
```

### File Tools

```python
from superagi.tools import (
    FileReadTool,
    FileWriteTool,
    FileSearchTool
)

# File Read Tool
read_tool = FileReadTool(
    name="file_reader",
    description="Read content from files",
    config={
        "allowed_extensions": [".txt", ".md", ".json", ".py", ".csv"],
        "max_file_size": "10MB",
        "encoding": "utf-8"
    }
)

content = read_tool.execute({
    "file_path": "/data/document.txt",
    "read_mode": "full"  # or "lines", "chunk"
})


# File Write Tool
write_tool = FileWriteTool(
    name="file_writer",
    description="Write content to files",
    config={
        "allowed_directories": ["/output", "/temp"],
        "backup_existing": True
    }
)

result = write_tool.execute({
    "file_path": "/output/report.md",
    "content": "# Report\n\nContent here...",
    "mode": "write"  # or "append"
})


# File Search Tool
search_tool = FileSearchTool(
    name="file_search",
    description="Search for files matching criteria",
    config={
        "search_directories": ["/documents", "/data"],
        "recursive": True
    }
)

files = search_tool.execute({
    "pattern": "*.pdf",
    "name_contains": "report",
    "modified_after": "2024-01-01"
})
```

### Code Tools

```python
from superagi.tools import (
    CodeGeneratorTool,
    CodeExecutorTool,
    CodeReviewTool
)

# Code Generator
generator = CodeGeneratorTool(
    name="code_generator",
    description="Generate code based on specifications",
    config={
        "supported_languages": ["python", "javascript", "typescript"],
        "include_comments": True,
        "follow_best_practices": True
    }
)

code = generator.execute({
    "specification": "Create a function that validates email addresses",
    "language": "python",
    "include_tests": True
})


# Code Executor (Sandboxed)
executor = CodeExecutorTool(
    name="code_executor",
    description="Execute code in a sandboxed environment",
    config={
        "timeout": 30,
        "memory_limit": "512MB",
        "allowed_imports": ["numpy", "pandas", "requests"]
    }
)

result = executor.execute({
    "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
    """,
    "language": "python"
})
print(f"Output: {result['stdout']}")


# Code Review Tool
reviewer = CodeReviewTool(
    name="code_reviewer",
    description="Review code for issues and improvements",
    config={
        "check_security": True,
        "check_performance": True,
        "check_style": True
    }
)

review = reviewer.execute({
    "code": code_to_review,
    "language": "python",
    "review_level": "thorough"
})
```

### API Tools

```python
from superagi.tools import APITool

# Generic API Tool
api_tool = APITool(
    name="external_api",
    description="Call external APIs",
    config={
        "base_url": "https://api.example.com",
        "auth_type": "bearer",
        "auth_token": "${API_TOKEN}",  # From environment
        "timeout": 30,
        "rate_limit": 100  # requests per minute
    }
)

# Make API call
response = api_tool.execute({
    "method": "GET",
    "endpoint": "/users/123",
    "headers": {"Accept": "application/json"},
    "params": {"include": "profile"}
})

# POST request
response = api_tool.execute({
    "method": "POST",
    "endpoint": "/messages",
    "json_body": {
        "recipient": "user@example.com",
        "content": "Hello from SuperAGI!"
    }
})
```

## Custom Tool Development

### Tool Base Class

```python
from superagi.tools import BaseTool
from typing import Any, Dict
from pydantic import BaseModel, Field

class CustomToolInput(BaseModel):
    """Input schema for custom tool."""
    query: str = Field(..., description="The search query")
    limit: int = Field(default=10, description="Maximum results")

class CustomToolOutput(BaseModel):
    """Output schema for custom tool."""
    results: list
    total_count: int
    execution_time: float

class CustomSearchTool(BaseTool):
    """Custom tool implementation."""

    name: str = "custom_search"
    description: str = "Search custom data source"
    input_schema: type = CustomToolInput
    output_schema: type = CustomToolOutput

    def __init__(self, config: dict = None):
        super().__init__(config)
        self.data_source = self._initialize_data_source()

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool."""
        import time
        start_time = time.time()

        # Validate input
        validated_input = CustomToolInput(**input_data)

        # Perform search
        results = self._search(
            query=validated_input.query,
            limit=validated_input.limit
        )

        # Return output
        return CustomToolOutput(
            results=results,
            total_count=len(results),
            execution_time=time.time() - start_time
        ).dict()

    def _search(self, query: str, limit: int) -> list:
        """Perform the actual search."""
        # Implementation here
        return self.data_source.search(query, limit=limit)

    def _initialize_data_source(self):
        """Initialize the data source connection."""
        # Setup code here
        pass
```

### Tool with External Dependencies

```python
from superagi.tools import BaseTool
import subprocess

class DatabaseQueryTool(BaseTool):
    """Tool for querying databases."""

    name = "database_query"
    description = "Execute read-only database queries"

    def __init__(self, connection_string: str, **kwargs):
        super().__init__(**kwargs)
        self.connection_string = connection_string
        self._connection = None

    def setup(self):
        """Setup database connection."""
        import sqlalchemy
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self._connection = self.engine.connect()

    def teardown(self):
        """Cleanup database connection."""
        if self._connection:
            self._connection.close()

    def execute(self, input_data: dict) -> dict:
        """Execute a database query."""
        query = input_data.get("query", "")

        # Security: Only allow SELECT statements
        if not query.strip().upper().startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed"}

        try:
            result = self._connection.execute(query)
            rows = result.fetchall()
            columns = result.keys()

            return {
                "columns": list(columns),
                "rows": [dict(zip(columns, row)) for row in rows],
                "row_count": len(rows)
            }
        except Exception as e:
            return {"error": str(e)}
```

### Async Tools

```python
from superagi.tools import AsyncBaseTool
import asyncio
import aiohttp

class AsyncWebFetchTool(AsyncBaseTool):
    """Async tool for fetching multiple URLs."""

    name = "async_web_fetch"
    description = "Fetch multiple web pages concurrently"

    async def execute(self, input_data: dict) -> dict:
        """Fetch URLs asynchronously."""
        urls = input_data.get("urls", [])
        timeout = input_data.get("timeout", 30)

        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_url(session, url, timeout) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            "results": [
                {"url": url, "content": result if not isinstance(result, Exception) else str(result)}
                for url, result in zip(urls, results)
            ]
        }

    async def _fetch_url(self, session, url: str, timeout: int) -> str:
        """Fetch a single URL."""
        async with session.get(url, timeout=timeout) as response:
            return await response.text()
```

## Tool Management

### Tool Registry

```python
from superagi.tools import ToolRegistry

# Create registry
registry = ToolRegistry()

# Register tools
registry.register(WebSearchTool())
registry.register(FileReadTool())
registry.register(CodeExecutorTool())
registry.register(CustomSearchTool())

# Get tool by name
search_tool = registry.get("web_search")

# List all tools
for tool in registry.list_tools():
    print(f"{tool.name}: {tool.description}")

# Get tools by capability
code_tools = registry.get_by_capability("code_execution")
```

### Tool Permissions

```python
class ToolPermissionManager:
    """Manage tool permissions for agents."""

    def __init__(self):
        self.permissions = {}

    def grant(self, agent_id: str, tool_name: str, level: str = "full"):
        """Grant tool permission to an agent."""
        if agent_id not in self.permissions:
            self.permissions[agent_id] = {}

        self.permissions[agent_id][tool_name] = {
            "level": level,  # "full", "read_only", "limited"
            "granted_at": datetime.now()
        }

    def revoke(self, agent_id: str, tool_name: str):
        """Revoke tool permission."""
        if agent_id in self.permissions:
            self.permissions[agent_id].pop(tool_name, None)

    def check(self, agent_id: str, tool_name: str, action: str = "execute") -> bool:
        """Check if agent has permission for tool action."""
        if agent_id not in self.permissions:
            return False

        permission = self.permissions[agent_id].get(tool_name)
        if not permission:
            return False

        level = permission["level"]
        if level == "full":
            return True
        elif level == "read_only":
            return action in ["read", "list", "search"]
        elif level == "limited":
            return action == "read"

        return False
```

### Tool Execution Context

```python
class ToolExecutionContext:
    """Context for tool execution with logging and metrics."""

    def __init__(self, agent_id: str, task_id: str):
        self.agent_id = agent_id
        self.task_id = task_id
        self.start_time = None
        self.execution_log = []

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self._log_completion(duration, exc_val)

    def log_action(self, action: str, details: dict = None):
        """Log an action during execution."""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        })

    def _log_completion(self, duration: float, error: Exception = None):
        """Log execution completion."""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": "completed" if not error else "failed",
            "duration": duration,
            "error": str(error) if error else None
        })

# Usage
with ToolExecutionContext(agent_id="agent_1", task_id="task_123") as ctx:
    ctx.log_action("starting_search", {"query": "AI agents"})
    results = search_tool.execute({"query": "AI agents"})
    ctx.log_action("search_complete", {"result_count": len(results)})
```

## Tool Orchestration

### Tool Chaining

```python
class ToolChain:
    """Chain multiple tools together."""

    def __init__(self, tools: list):
        self.tools = tools

    def execute(self, initial_input: dict) -> dict:
        """Execute tools in sequence, passing output to next input."""
        current_data = initial_input

        for tool in self.tools:
            # Transform output to input for next tool
            tool_input = self._transform(current_data, tool)

            # Execute tool
            result = tool.execute(tool_input)

            # Handle errors
            if result.get("error"):
                return {"error": result["error"], "failed_at": tool.name}

            current_data = result

        return current_data

    def _transform(self, data: dict, next_tool) -> dict:
        """Transform data for next tool (override for custom logic)."""
        return data


# Example: Research chain
research_chain = ToolChain([
    WebSearchTool(),      # Search for information
    WebScraperTool(),     # Scrape relevant pages
    SummarizerTool(),     # Summarize content
    FileWriteTool()       # Save results
])

result = research_chain.execute({
    "query": "autonomous AI agents",
    "output_path": "/results/research.md"
})
```

### Parallel Tool Execution

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelToolExecutor:
    """Execute multiple tools in parallel."""

    def __init__(self, max_workers: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute_parallel(self, tool_calls: list) -> list:
        """Execute multiple tool calls in parallel."""
        futures = []

        for call in tool_calls:
            tool = call["tool"]
            input_data = call["input"]
            future = self.executor.submit(tool.execute, input_data)
            futures.append((call["id"], future))

        results = []
        for call_id, future in futures:
            try:
                result = future.result(timeout=60)
                results.append({"id": call_id, "result": result, "status": "success"})
            except Exception as e:
                results.append({"id": call_id, "error": str(e), "status": "failed"})

        return results

# Usage
executor = ParallelToolExecutor(max_workers=10)

results = executor.execute_parallel([
    {"id": "search_1", "tool": search_tool, "input": {"query": "topic 1"}},
    {"id": "search_2", "tool": search_tool, "input": {"query": "topic 2"}},
    {"id": "search_3", "tool": search_tool, "input": {"query": "topic 3"}},
])
```

## Best Practices

### Tool Design Guidelines

```python
# 1. Clear, specific descriptions
class GoodTool(BaseTool):
    name = "github_issue_creator"
    description = """Create a new issue on GitHub.
    Requires: repository name, issue title, issue body.
    Optional: labels, assignees, milestone.
    Returns: issue URL and number."""

# 2. Comprehensive input validation
def execute(self, input_data: dict) -> dict:
    # Validate required fields
    required = ["repo", "title", "body"]
    missing = [f for f in required if f not in input_data]
    if missing:
        return {"error": f"Missing required fields: {missing}"}

    # Validate field formats
    if not self._is_valid_repo(input_data["repo"]):
        return {"error": "Invalid repository format. Expected: owner/repo"}

    # Proceed with execution
    ...

# 3. Graceful error handling
def execute(self, input_data: dict) -> dict:
    try:
        result = self._do_work(input_data)
        return {"success": True, "data": result}
    except AuthenticationError as e:
        return {"error": "Authentication failed", "details": str(e)}
    except RateLimitError as e:
        return {"error": "Rate limit exceeded", "retry_after": e.retry_after}
    except Exception as e:
        logger.exception("Unexpected error in tool execution")
        return {"error": "Internal error", "details": str(e)}

# 4. Proper cleanup
def execute(self, input_data: dict) -> dict:
    resource = None
    try:
        resource = self._acquire_resource()
        return self._process(resource, input_data)
    finally:
        if resource:
            self._release_resource(resource)
```

## Summary

In this chapter, you've learned:

- **Built-in Tools**: Web, file, code, and API tools
- **Custom Tools**: Creating tools from BaseTool
- **Tool Management**: Registry, permissions, and context
- **Tool Orchestration**: Chaining and parallel execution
- **Best Practices**: Design, validation, and error handling

## Key Takeaways

1. **Extend Capabilities**: Tools let agents interact with the real world
2. **Type Safety**: Use input/output schemas for validation
3. **Security**: Implement proper permissions and sandboxing
4. **Composition**: Chain tools for complex workflows
5. **Resilience**: Handle errors gracefully

## Next Steps

Now that you can integrate tools, let's explore Memory & Learning in Chapter 4 for persistent context and agent improvement.

---

**Ready for Chapter 4?** [Memory & Learning](04-memory-learning.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `tool`, `results` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Tool Integration` as an operating subsystem inside **SuperAGI Tutorial: Production-Ready Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `result`, `execute`, `error` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Tool Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `tool` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `results`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/TransformerOptimus/SuperAGI)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `tool` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Agent Architecture](02-agent-architecture.md)
- [Next Chapter: Chapter 4: Memory & Learning](04-memory-learning.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
