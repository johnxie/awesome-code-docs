---
layout: default
title: "Chapter 5: LSP and MCP Integration"
nav_order: 5
parent: Crush Tutorial
---

# Chapter 5: LSP and MCP Integration

This chapter explains how to extend Crush with richer code intelligence and external tools.

## Learning Goals

- configure LSP servers for stronger code context
- add MCP servers over stdio/http/sse transports
- control MCP timeouts, headers, and disabled tools
- operationalize integrations for team usage

## LSP Integration Pattern

```json
{
  "$schema": "https://charm.land/crush.json",
  "lsp": {
    "go": { "command": "gopls" },
    "typescript": { "command": "typescript-language-server", "args": ["--stdio"] }
  }
}
```

## MCP Integration Pattern

```json
{
  "$schema": "https://charm.land/crush.json",
  "mcp": {
    "filesystem": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/server.js"],
      "timeout": 120
    }
  }
}
```

## Integration Rollout Checklist

- verify server command reliability outside Crush first
- set explicit timeouts and minimal headers/secrets
- disable dangerous or irrelevant MCP tools by default
- document integration profile per repository type

## Source References

- [Crush README: LSPs](https://github.com/charmbracelet/crush/blob/main/README.md#lsps)
- [Crush README: MCPs](https://github.com/charmbracelet/crush/blob/main/README.md#mcps)
- [Crush schema](https://github.com/charmbracelet/crush/blob/main/schema.json)

## Summary

You now know how to wire Crush into language tooling and MCP ecosystems safely.

Next: [Chapter 6: Skills, Commands, and Workflow Customization](06-skills-commands-and-workflow-customization.md)
