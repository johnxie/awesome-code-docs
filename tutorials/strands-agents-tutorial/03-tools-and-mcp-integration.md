---
layout: default
title: "Chapter 3: Tools and MCP Integration"
nav_order: 3
parent: Strands Agents Tutorial
---

# Chapter 3: Tools and MCP Integration

This chapter covers tool composition and MCP usage patterns for real capability expansion.

## Learning Goals

- build custom Python tools with decorators
- attach MCP servers through `MCPClient`
- manage tool discovery and lifecycle
- avoid hanging and stability pitfalls

## Integration Patterns

- static tool lists for predictable behavior
- directory-based tool loading for rapid iteration
- MCP-backed tool surfaces for external capabilities

## Reliability Considerations

Strands runs MCP communication through a background-thread architecture to hide async complexity. Treat MCP connection lifecycle and error handling as first-class operational concerns.

## Source References

- [Strands Tools Concepts](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/)
- [Strands MCP Tools Concepts](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/)
- [Strands MCP Client Architecture](https://github.com/strands-agents/sdk-python/blob/main/docs/MCP_CLIENT_ARCHITECTURE.md)

## Summary

You now have practical patterns for integrating tools and MCP safely in Strands.

Next: [Chapter 4: Model Providers and Runtime Strategy](04-model-providers-and-runtime-strategy.md)
