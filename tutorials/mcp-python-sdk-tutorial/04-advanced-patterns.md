---
layout: default
title: "MCP Python SDK Tutorial - Chapter 4: Advanced Patterns"
nav_order: 4
parent: MCP Python SDK Tutorial
---

# Chapter 4: Advanced Patterns

> Master structured outputs, progress tracking, context management, and advanced server patterns.

## Structured Outputs

Use Pydantic models for type-safe responses:

```python
from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    title: str
    url: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_found: int

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search":
        response = SearchResponse(
            query=arguments["query"],
            results=[
                SearchResult(title="Doc 1", url="/doc1", score=0.95),
                SearchResult(title="Doc 2", url="/doc2", score=0.87)
            ],
            total_found=2
        )

        return [TextContent(
            type="text",
            text=response.model_dump_json(indent=2)
        )]
```

## Progress Tracking

For long operations, send progress updates:

```python
from mcp.types import ProgressNotification

async def process_large_dataset(data, progress_token):
    total = len(data)

    for i, item in enumerate(data):
        # Process item
        await process_item(item)

        # Send progress
        progress = (i + 1) / total * 100
        await app.send_progress_notification(
            ProgressNotification(
                progress_token=progress_token,
                progress=progress,
                total=100.0
            )
        )
```

## Context Management

Share state across tool calls:

```python
class ServerContext:
    def __init__(self):
        self.cache = {}
        self.connections = {}

    async def get_cached(self, key):
        return self.cache.get(key)

    async def set_cached(self, key, value):
        self.cache[key] = value

context = ServerContext()

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_data":
        # Check cache first
        cached = await context.get_cached(arguments["key"])
        if cached:
            return [TextContent(type="text", text=f"Cached: {cached}")]

        # Fetch and cache
        data = await fetch_data(arguments["key"])
        await context.set_cached(arguments["key"], data)
        return [TextContent(type="text", text=str(data))]
```

## Batch Operations

Process multiple requests efficiently:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "batch_process":
        items = arguments["items"]

        # Process in parallel
        results = await asyncio.gather(*[
            process_item(item) for item in items
        ])

        return [TextContent(
            type="text",
            text=json.dumps({"results": results})
        )]
```

## Rate Limiting

```python
from asyncio import Semaphore

rate_limiter = Semaphore(5)  # Max 5 concurrent requests

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    async with rate_limiter:
        # Process request with rate limiting
        result = await expensive_operation(arguments)
        return [TextContent(type="text", text=result)]
```

## Streaming Responses

For real-time data:

```python
async def stream_logs(log_file):
    async with aiofiles.open(log_file, 'r') as f:
        while True:
            line = await f.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            yield line

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "tail_logs":
        lines = []
        async for line in stream_logs(arguments["file"]):
            lines.append(line)
            if len(lines) >= 100:
                break

        return [TextContent(type="text", text="".join(lines))]
```

## Next Steps

Chapter 5 covers authentication, security best practices, and OAuth integration.

**Continue to:** [Chapter 5: Authentication & Security](05-authentication-security.md)

---

*Previous: [← Chapter 3: Server Architecture](03-server-architecture.md)*
