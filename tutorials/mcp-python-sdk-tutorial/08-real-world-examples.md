---
layout: default
title: "MCP Python SDK Tutorial - Chapter 8: Real-World Examples"
nav_order: 8
parent: MCP Python SDK Tutorial
---

# Chapter 8: Real-World Examples

> Complete production-ready MCP server implementations for common use cases.

## Example 1: File System Server

```python
import aiofiles
import os
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, Resource, TextContent

app = Server("filesystem-mcp")

ALLOWED_DIR = Path("/data")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="read_file",
            description="Read file contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="list_directory",
            description="List directory contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"}
                },
                "required": ["path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "read_file":
        path = ALLOWED_DIR / arguments["path"]

        if not path.is_relative_to(ALLOWED_DIR):
            return [TextContent(type="text", text="❌ Access denied")]

        async with aiofiles.open(path, 'r') as f:
            content = await f.read()
            return [TextContent(type="text", text=content)]

    elif name == "list_directory":
        path = ALLOWED_DIR / arguments["path"]

        if not path.is_relative_to(ALLOWED_DIR):
            return [TextContent(type="text", text="❌ Access denied")]

        files = [f.name for f in path.iterdir()]
        return [TextContent(type="text", text="\n".join(files))]
```

## Example 2: Database Query Server

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncpg
import json

app = Server("database-mcp")

async def get_db():
    return await asyncpg.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="password"
    )

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="query_users",
            description="Query users table",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "description": "WHERE clause"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "query_users":
        conn = await get_db()

        try:
            where_clause = arguments.get("filter", "1=1")
            limit = arguments.get("limit", 10)

            # Parameterized query to prevent SQL injection
            query = f"SELECT * FROM users WHERE {where_clause} LIMIT $1"
            rows = await conn.fetch(query, limit)

            results = [dict(row) for row in rows]
            return [TextContent(type="text", text=json.dumps(results, indent=2))]

        finally:
            await conn.close()
```

## Example 3: API Integration Server

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx

app = Server("api-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="github_search",
            description="Search GitHub repositories",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "language": {"type": "string", "description": "Filter by language"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "github_search":
        async with httpx.AsyncClient() as client:
            params = {"q": arguments["query"]}
            if "language" in arguments:
                params["q"] += f" language:{arguments['language']}"

            response = await client.get(
                "https://api.github.com/search/repositories",
                params=params,
                headers={"Accept": "application/vnd.github.v3+json"}
            )

            data = response.json()
            repos = [
                {
                    "name": r["full_name"],
                    "stars": r["stargazers_count"],
                    "url": r["html_url"]
                }
                for r in data["items"][:5]
            ]

            return [TextContent(type="text", text=json.dumps(repos, indent=2))]
```

## Example 4: Multi-Tool Aggregator

Combine multiple capabilities:

```python
from mcp.server import Server
from mcp.types import Tool, Resource, TextContent
import asyncio

app = Server("multi-tool-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(name="search_files", description="Search filesystem", inputSchema={...}),
        Tool(name="query_database", description="Query database", inputSchema={...}),
        Tool(name="call_api", description="Call external API", inputSchema={...}),
        Tool(name="analyze_data", description="Analyze combined data", inputSchema={...})
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_data":
        # Orchestrate multiple data sources
        file_data, db_data, api_data = await asyncio.gather(
            search_files(arguments["query"]),
            query_database(arguments["query"]),
            call_api(arguments["query"])
        )

        # Combine and analyze
        analysis = perform_analysis(file_data, db_data, api_data)
        return [TextContent(type="text", text=json.dumps(analysis))]
```

## Production Patterns

### Error Recovery

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def call_external_api(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

### Caching

```python
from functools import lru_cache
import hashlib

class ResultCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl

    def get_key(self, name, arguments):
        data = f"{name}:{json.dumps(arguments, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()

    async def get_or_compute(self, name, arguments, compute_fn):
        key = self.get_key(name, arguments)

        if key in self.cache:
            cached_time, result = self.cache[key]
            if time.time() - cached_time < self.ttl:
                return result

        result = await compute_fn()
        self.cache[key] = (time.time(), result)
        return result
```

## Conclusion

You now have a complete understanding of building production MCP servers:

✅ Core primitives (Resources, Tools, Prompts)
✅ Transport layers (stdio, SSE, HTTP)
✅ Advanced patterns (progress, context, streaming)
✅ Security and authentication
✅ Production deployment
✅ Client integration
✅ Real-world examples

## Resources

- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Python SDK Docs**: [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- **Example Servers**: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

---

*Previous: [← Chapter 7: Client Integration](07-client-integration.md)*
*Start: [↑ Back to Index](index.md)*
