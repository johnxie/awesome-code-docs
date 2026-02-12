---
layout: default
title: "Chapter 4: Client Integrations: Cursor, Claude, Windsurf, VS Code"
nav_order: 4
parent: Firecrawl MCP Server Tutorial
---

# Chapter 4: Client Integrations: Cursor, Claude, Windsurf, VS Code

Firecrawl MCP is widely used because it can be configured across major coding-agent clients.

## Learning Goals

- configure Firecrawl MCP for major client ecosystems
- standardize environment key handling across clients
- reduce configuration drift between local and team setups

## Integration Patterns

| Client | Integration Style |
|:-------|:------------------|
| Cursor | MCP server JSON in settings |
| Claude Desktop | `claude_desktop_config.json` command block |
| Windsurf | model config MCP section |
| VS Code | `mcp.servers` or workspace `mcp.json` |

## Source References

- [README Client Config Sections](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/README.md)

## Summary

You now have a cross-client setup model for consistent Firecrawl MCP usage.

Next: [Chapter 5: Configuration, Retries, and Credit Monitoring](05-configuration-retries-and-credit-monitoring.md)
