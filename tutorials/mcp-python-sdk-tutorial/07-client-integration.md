---
layout: default
title: "MCP Python SDK Tutorial - Chapter 7: Client Integration"
nav_order: 7
parent: MCP Python SDK Tutorial
---

# Chapter 7: Client Integration

Welcome to **Chapter 7: Client Integration**. In this part of **MCP Python SDK Tutorial: Building AI Tool Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Integrate your MCP server with Claude Code, Claude.ai, and build custom MCP clients.

## Claude Code Integration

### Configuration

Add to `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Testing with Claude Code

```bash
# Start Claude Code
claude-code

# Test your server
> Use the my-server to list available tools
> Call the search tool with query "example"
```

## Claude.ai Integration

For Claude.ai (paid plans), servers must be published:

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "description": "Production MCP server",
  "author": "Your Name",
  "repository": "https://github.com/you/my-mcp-server",
  "license": "MIT"
}
```

## Custom Client

Build a custom MCP client:

```python
from mcp.client import Client
from mcp.client.stdio import StdioServerParameters, stdio_client
import asyncio

async def main():
    # Connect to server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        client = Client(read, write)

        # Initialize
        await client.initialize()

        # List tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools.tools]}")

        # Call tool
        result = await client.call_tool("search", {"query": "test"})
        print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Web Interface

Create a web UI for your MCP server:

```python
from fastapi import FastAPI, WebSocket
from mcp.server import Server
import json

app = FastAPI()
mcp_server = Server("web-mcp")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        # Receive request
        data = await websocket.receive_text()
        request = json.loads(data)

        # Process with MCP
        if request["method"] == "tools/list":
            tools = await mcp_server.list_tools()
            await websocket.send_json({
                "result": {"tools": [t.dict() for t in tools]}
            })

        elif request["method"] == "tools/call":
            result = await mcp_server.call_tool(
                request["params"]["name"],
                request["params"]["arguments"]
            )
            await websocket.send_json({
                "result": {"content": [c.dict() for c in result]}
            })
```

## REST API Wrapper

Expose MCP via REST:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict

@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    result = await mcp_server.call_tool(
        request.tool_name,
        request.arguments
    )
    return {"content": [c.dict() for c in result]}

@app.get("/tools/list")
async def list_tools():
    tools = await mcp_server.list_tools()
    return {"tools": [t.dict() for t in tools]}
```

## SDK Integration

Use with LangChain:

```python
from langchain.tools import StructuredTool

async def search_mcp(query: str) -> str:
    result = await mcp_server.call_tool("search", {"query": query})
    return result[0].text

search_tool = StructuredTool.from_function(
    func=search_mcp,
    name="search",
    description="Search using MCP server"
)
```

## Next Steps

Chapter 8 provides real-world examples and complete implementation patterns.

**Continue to:** [Chapter 8: Real-World Examples](08-real-world-examples.md)

---

*Previous: [← Chapter 6: Production Deployment](06-production-deployment.md)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `tools`, `server`, `result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Client Integration` as an operating subsystem inside **MCP Python SDK Tutorial: Building AI Tool Servers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `request`, `client`, `mcp_server` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Client Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `tools`.
2. **Input normalization**: shape incoming data so `server` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [MCP Python SDK repository](https://github.com/modelcontextprotocol/python-sdk)
  Why it matters: authoritative reference on `MCP Python SDK repository` (github.com).

Suggested trace strategy:
- search upstream code for `tools` and `server` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Production Deployment](06-production-deployment.md)
- [Next Chapter: Chapter 8: Real-World Examples](08-real-world-examples.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
