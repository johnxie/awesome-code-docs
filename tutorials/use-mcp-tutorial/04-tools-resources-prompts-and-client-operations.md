---
layout: default
title: "Chapter 4: Tools, Resources, Prompts, and Client Operations"
nav_order: 4
parent: use-mcp Tutorial
---

# Chapter 4: Tools, Resources, Prompts, and Client Operations

This chapter maps core MCP capability access into reusable React operations.

## Learning Goals

- call tools with explicit argument and error handling patterns
- list/read resources and use templates for contextual data access
- list/get prompts with argument-bound rendering flows
- standardize operation wrappers to reduce component complexity

## Client Operation Surface

| Operation | Hook Method |
|:----------|:------------|
| tool execution | `callTool` |
| resource reads | `listResources`, `readResource` |
| prompt access | `listPrompts`, `getPrompt` |

## Source References

- [use-mcp README - Quick Start](https://github.com/modelcontextprotocol/use-mcp/blob/main/README.md#quick-start)
- [Inspector Example README](https://github.com/modelcontextprotocol/use-mcp/blob/main/examples/inspector/README.md)

## Summary

You now have an operations model for integrating MCP capabilities into React workflows.

Next: [Chapter 5: Transport, Retry, and Reconnect Strategy](05-transport-retry-and-reconnect-strategy.md)
