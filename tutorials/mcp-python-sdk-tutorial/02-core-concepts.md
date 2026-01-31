---
layout: default
title: "MCP Python SDK Tutorial - Chapter 2: Core Concepts"
nav_order: 2
parent: MCP Python SDK Tutorial
---

# Chapter 2: Core Concepts - Resources, Tools, and Prompts

> Master the three fundamental primitives of MCP: Resources for data access, Tools for AI actions, and Prompts for reusable templates.

## Overview

MCP servers expose three types of capabilities to AI clients:

1. **Resources** - Data sources (files, database records, API responses)
2. **Tools** - Executable functions (search, transform, create)
3. **Prompts** - Reusable prompt templates (analysis patterns, code review)

This chapter explores each primitive in depth with practical examples.

## Resources: Exposing Data

Resources let AI assistants read data without executing arbitrary code. Think of them as read-only endpoints.

### Resource Structure

```python
from mcp.types import Resource, TextResourceContents, BlobResourceContents

# Text resource
text_resource = Resource(
    uri="file:///data/config.json",
    name="Application Configuration",
    description="Main app config file",
    mimeType="application/json"
)

# Binary resource
image_resource = Resource(
    uri="file:///images/logo.png",
    name="Company Logo",
    mimeType="image/png"
)
```

### Implementing Resources

```python
from mcp.server import Server
from mcp.types import Resource, TextResourceContents
import json

app = Server("resource-demo")

# List available resources
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="config://app",
            name="App Config",
            description="Application configuration",
            mimeType="application/json"
        ),
        Resource(
            uri="data://users/stats",
            name="User Statistics",
            description="Current user metrics",
            mimeType="application/json"
        )
    ]

# Read resource content
@app.read_resource()
async def read_resource(uri: str) -> str | bytes:
    if uri == "config://app":
        config = {
            "api_key": "***",
            "debug_mode": True,
            "max_connections": 100
        }
        return json.dumps(config, indent=2)

    elif uri == "data://users/stats":
        stats = {
            "total_users": 1234,
            "active_today": 567,
            "avg_session_min": 23.5
        }
        return json.dumps(stats, indent=2)

    raise ValueError(f"Unknown resource: {uri}")
```

### Resource URI Schemes

Use custom URI schemes to organize resources:

```python
# File system
"file:///path/to/file.txt"

# Database
"db://postgres/users/123"

# API
"api://github/repos/owner/repo"

# Custom
"memory://cache/key"
"config://section/setting"
```

## Tools: Enabling Actions

Tools let AI execute functions with parameters. Unlike resources, tools can modify state and have side effects.

### Tool Definition

```python
from mcp.types import Tool

Tool(
    name="search_documents",
    description="Search through document database using keywords",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query"
            },
            "limit": {
                "type": "integer",
                "description": "Max results",
                "default": 10,
                "minimum": 1,
                "maximum": 100
            },
            "category": {
                "type": "string",
                "enum": ["all", "docs", "code", "config"],
                "default": "all"
            }
        },
        "required": ["query"]
    }
)
```

### Complex Tool Example

```python
import asyncio
from mcp.types import Tool, TextContent, ImageContent

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_code",
            description="Analyze Python code for issues and suggestions",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to analyze"},
                    "checks": {
                        "type": "array",
                        "items": {"enum": ["style", "security", "performance"]},
                        "default": ["style", "security"]
                    }
                },
                "required": ["code"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "analyze_code":
        code = arguments["code"]
        checks = arguments.get("checks", ["style", "security"])

        issues = []

        if "style" in checks:
            # Simple style check
            if "import *" in code:
                issues.append("❌ Style: Avoid wildcard imports")

        if "security" in checks:
            # Security check
            if "eval(" in code or "exec(" in code:
                issues.append("🔒 Security: Dangerous function usage")

        if "performance" in checks:
            # Performance check
            if "list(range(" in code:
                issues.append("⚡ Performance: Use range() directly in loops")

        result = "\n".join(issues) if issues else "✅ No issues found"

        return [TextContent(type="text", text=result)]
```

### Tool Best Practices

```python
# ✅ Good: Clear, specific tool
Tool(
    name="send_email",
    description="Send email via SMTP with optional attachments",
    inputSchema={...}
)

# ❌ Bad: Vague tool
Tool(
    name="do_thing",
    description="Does something",
    inputSchema={...}
)

# ✅ Good: Structured errors
try:
    result = process_data(args)
except FileNotFoundError as e:
    return [TextContent(
        type="text",
        text=f"Error: File '{e.filename}' not found. Please check the path."
    )]

# ❌ Bad: Generic errors
except Exception as e:
    return [TextContent(type="text", text="Error")]
```

## Prompts: Reusable Templates

Prompts are parameterized templates that AI can use consistently.

### Prompt Structure

```python
from mcp.types import Prompt, PromptMessage

Prompt(
    name="code_review",
    description="Perform code review with specific focus areas",
    arguments=[
        {
            "name": "code",
            "description": "Code to review",
            "required": True
        },
        {
            "name": "focus",
            "description": "Focus area: security, performance, or style",
            "required": False
        }
    ]
)
```

### Implementing Prompts

```python
from mcp.types import Prompt, PromptMessage, TextContent

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="analyze_performance",
            description="Analyze code for performance issues",
            arguments=[
                {"name": "language", "description": "Programming language", "required": True},
                {"name": "code", "description": "Code to analyze", "required": True}
            ]
        ),
        Prompt(
            name="explain_concept",
            description="Explain a technical concept",
            arguments=[
                {"name": "concept", "description": "Concept to explain", "required": True},
                {"name": "level", "description": "Expertise level: beginner/intermediate/advanced", "required": False}
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    if name == "analyze_performance":
        lang = arguments["language"]
        code = arguments["code"]

        return [
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"""Analyze this {lang} code for performance bottlenecks:

```{lang}
{code}
```

Focus on:
1. Time complexity
2. Memory usage
3. I/O operations
4. Algorithmic efficiency

Provide specific recommendations for improvement."""
                )
            )
        ]

    elif name == "explain_concept":
        concept = arguments["concept"]
        level = arguments.get("level", "intermediate")

        return [
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"""Explain the concept of '{concept}' at a {level} level.

Include:
- Definition and key principles
- Practical examples
- Common use cases
- Related concepts

Tailor complexity to {level} understanding."""
                )
            )
        ]
```

## Combining Primitives

Real-world servers often combine resources, tools, and prompts:

```python
from mcp.server import Server
from mcp.types import Resource, Tool, Prompt, TextContent
import json

app = Server("combined-demo")

# Resources: Expose data
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="data://metrics/daily",
            name="Daily Metrics",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "data://metrics/daily":
        return json.dumps({"views": 1234, "users": 567})
    raise ValueError(f"Unknown resource: {uri}")

# Tools: Enable actions
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_metrics",
            description="Analyze metrics and generate insights",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric_uri": {"type": "string"}
                },
                "required": ["metric_uri"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "analyze_metrics":
        # Read resource, process, return insights
        data = await read_resource(arguments["metric_uri"])
        metrics = json.loads(data)

        analysis = f"Views: {metrics['views']}, Users: {metrics['users']}, Ratio: {metrics['views']/metrics['users']:.2f}"
        return [TextContent(type="text", text=analysis)]

# Prompts: Provide templates
@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="metrics_report",
            description="Generate a metrics report",
            arguments=[{"name": "metric_uri", "required": True}]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    if name == "metrics_report":
        return [
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Generate a comprehensive report for metrics at {arguments['metric_uri']}"
                )
            )
        ]
```

## Type Safety with Pydantic

Use Pydantic for robust validation:

```python
from pydantic import BaseModel, Field, validator
from typing import Literal

class SearchArgs(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    limit: int = Field(10, ge=1, le=100, description="Max results")
    category: Literal["all", "docs", "code"] = "all"

    @validator('query')
    def validate_query(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Query cannot be empty")
        return v.strip()

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search":
        try:
            args = SearchArgs(**arguments)  # Validates automatically
            # Use args.query, args.limit, args.category
            results = perform_search(args.query, args.limit, args.category)
            return [TextContent(type="text", text=results)]
        except ValueError as e:
            return [TextContent(type="text", text=f"Validation error: {e}")]
```

## Progress Tracking

For long-running operations, report progress:

```python
from mcp.types import Tool, TextContent, ProgressNotification

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "process_large_file":
        file_path = arguments["path"]

        # Send progress notifications
        await app.send_progress_notification(
            ProgressNotification(
                progress_token="process-123",
                progress=0.0,
                total=100.0
            )
        )

        # Process in chunks
        for i in range(10):
            await process_chunk(file_path, i)
            await app.send_progress_notification(
                ProgressNotification(
                    progress_token="process-123",
                    progress=(i + 1) * 10.0,
                    total=100.0
                )
            )

        return [TextContent(type="text", text="Processing complete")]
```

## Next Steps

In Chapter 3, we'll explore server architecture including transport layers (stdio, SSE, HTTP) and lifecycle management.

**Continue to:** [Chapter 3: Server Architecture](03-server-architecture.md)

---

*Previous: [← Chapter 1: Getting Started](01-getting-started.md)*
