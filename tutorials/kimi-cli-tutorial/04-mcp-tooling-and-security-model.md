---
layout: default
title: "Chapter 4: MCP Tooling and Security Model"
nav_order: 4
parent: Kimi CLI Tutorial
---

# Chapter 4: MCP Tooling and Security Model

Kimi CLI can connect to external MCP servers to extend tool capabilities beyond built-ins.

## Core MCP Operations

```bash
kimi mcp add --transport http context7 https://mcp.context7.com/mcp
kimi mcp list
kimi mcp test context7
kimi mcp remove context7
```

## Security Model

- MCP tool calls follow the same approval system as other sensitive operations.
- OAuth flows are supported for compatible servers.
- YOLO mode auto-approves MCP actions and should be used with caution.

## Source References

- [MCP customization docs](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/mcp.md)
- [MCP command reference](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/reference/kimi-mcp.md)

## Summary

You now know how to add MCP capabilities while preserving operator control.

Next: [Chapter 5: ACP and IDE Integrations](05-acp-and-ide-integrations.md)
