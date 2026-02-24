---
layout: default
title: "MCP Python SDK Tutorial - Chapter 4: Advanced Patterns"
nav_order: 4
parent: MCP Python SDK Tutorial
---

# Chapter 4: Advanced Patterns

Welcome to **Chapter 4: Advanced Patterns**. In this part of **MCP Python SDK Tutorial: Building AI Tool Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `arguments`, `text`, `call_tool` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Advanced Patterns` as an operating subsystem inside **MCP Python SDK Tutorial: Building AI Tool Servers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `self`, `TextContent` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Advanced Patterns` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `arguments`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `call_tool`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [MCP Python SDK repository](https://github.com/modelcontextprotocol/python-sdk)
  Why it matters: authoritative reference on `MCP Python SDK repository` (github.com).

Suggested trace strategy:
- search upstream code for `arguments` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Server Architecture](03-server-architecture.md)
- [Next Chapter: Chapter 5: Authentication & Security](05-authentication-security.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
