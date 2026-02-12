---
layout: default
title: "Chapter 5: Transport Modes and Client Configuration"
nav_order: 5
parent: MCP Chrome Tutorial
---

# Chapter 5: Transport Modes and Client Configuration

This chapter covers streamable HTTP and stdio transport choices for integrating MCP Chrome with clients.

## Learning Goals

- choose transport mode per client capabilities
- configure connection settings correctly
- reduce path and registration-related integration failures

## Transport Comparison

| Mode | Best For |
|:-----|:---------|
| streamable HTTP | modern MCP clients with HTTP transport support |
| stdio | clients that only support command-process integration |

## Streamable HTTP Example

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:12306/mcp"
    }
  }
}
```

## Source References

- [README Transport Setup](https://github.com/hangwin/mcp-chrome/blob/master/README.md)
- [MCP CLI Config](https://github.com/hangwin/mcp-chrome/blob/master/docs/mcp-cli-config.md)

## Summary

You now know how to align MCP Chrome transport configuration with client constraints.

Next: [Chapter 6: Visual Editor and Prompt Workflows](06-visual-editor-and-prompt-workflows.md)
