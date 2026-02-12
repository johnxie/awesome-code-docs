---
layout: default
title: "Chapter 2: Client Configuration, Sessions, and Transport Choices"
nav_order: 2
parent: MCP Use Tutorial
---

# Chapter 2: Client Configuration, Sessions, and Transport Choices

Client configuration is where reliability is won or lost in multi-server MCP workflows.

## Learning Goals

- configure stdio and HTTP servers within one client profile
- manage session lifecycle and restart recovery expectations
- tune SSL, timeout, and header/auth options safely
- use allowed-server filtering and constructor variants for environment control

## Transport Choice Table

| Transport | Best For | Caveat |
|:----------|:---------|:-------|
| stdio | local process servers | process env/permissions drift |
| HTTP/Streamable HTTP | hosted services | auth/header/timeout correctness |
| SSE compatibility | legacy endpoints | migration needed over time |

## Source References

- [TypeScript Client Configuration](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/client/client-configuration.mdx)
- [Python Client Configuration](https://github.com/mcp-use/mcp-use/blob/main/docs/python/client/client-configuration.mdx)
- [TypeScript Client README](https://github.com/mcp-use/mcp-use/blob/main/libraries/typescript/packages/mcp-use/README.md)

## Summary

You now have a repeatable client configuration baseline for local and remote MCP servers.

Next: [Chapter 3: Agent Configuration, Tool Governance, and Memory](03-agent-configuration-tool-governance-and-memory.md)
