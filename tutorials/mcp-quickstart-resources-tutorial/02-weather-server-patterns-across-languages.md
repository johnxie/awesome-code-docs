---
layout: default
title: "Chapter 2: Weather Server Patterns Across Languages"
nav_order: 2
parent: MCP Quickstart Resources Tutorial
---

# Chapter 2: Weather Server Patterns Across Languages

This chapter compares weather server implementations to highlight shared protocol behavior.

## Learning Goals

- identify common MCP server primitives in each runtime
- compare runtime-specific setup/build differences
- reason about maintainability tradeoffs by language
- preserve behavior parity when customizing server examples

## Comparison Lens

1. tool declaration and `tools/list` response shape
2. stdio transport setup and lifecycle handling
3. dependency/runtime management per ecosystem
4. local test and run commands

## Source References

- [Weather Server (Go)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/weather-server-go/README.md)
- [Weather Server (Python)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/weather-server-python/README.md)
- [Weather Server (Rust)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/weather-server-rust/README.md)
- [Weather Server (TypeScript)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/weather-server-typescript/README.md)

## Summary

You now have a cross-language pattern model for MCP weather-server implementations.

Next: [Chapter 3: MCP Client Patterns and LLM Chat Loops](03-mcp-client-patterns-and-llm-chat-loops.md)
