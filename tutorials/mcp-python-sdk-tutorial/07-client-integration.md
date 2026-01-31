---
layout: default
title: "MCP Python SDK Tutorial - Chapter 7: Client Integration"
nav_order: 7
parent: MCP Python SDK Tutorial
---

# Chapter 7: Client Integration

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
