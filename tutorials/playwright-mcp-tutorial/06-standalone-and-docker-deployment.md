---
layout: default
title: "Chapter 6: Standalone and Docker Deployment"
nav_order: 6
parent: Playwright MCP Tutorial
---

# Chapter 6: Standalone and Docker Deployment

This chapter covers deployment modes beyond basic stdio invocation.

## Learning Goals

- run Playwright MCP as a standalone HTTP MCP endpoint
- use Docker mode for cleaner host/runtime boundaries
- understand headless constraints in containerized mode
- connect clients to stable local MCP endpoints

## Deployment Patterns

| Pattern | Example | Best For |
|:--------|:--------|:---------|
| standalone local server | `npx @playwright/mcp@latest --port 8931` | multi-client local development |
| Docker hosted server | `mcr.microsoft.com/playwright/mcp` | cleaner runtime isolation |
| local stdio | default `npx` mode | simplest host integrations |

## Source References

- [README: Standalone MCP Server](https://github.com/microsoft/playwright-mcp/blob/main/README.md#standalone-mcp-server)
- [README: Docker Configuration](https://github.com/microsoft/playwright-mcp/blob/main/README.md#docker)
- [Dockerfile](https://github.com/microsoft/playwright-mcp/blob/main/Dockerfile)

## Summary

You now have options for scaling Playwright MCP beyond default client-managed execution.

Next: [Chapter 7: Tooling Surface and Automation Patterns](07-tooling-surface-and-automation-patterns.md)
