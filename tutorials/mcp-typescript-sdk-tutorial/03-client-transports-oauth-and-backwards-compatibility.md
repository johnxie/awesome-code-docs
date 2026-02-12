---
layout: default
title: "Chapter 3: Client Transports, OAuth, and Backwards Compatibility"
nav_order: 3
parent: MCP TypeScript SDK Tutorial
---

# Chapter 3: Client Transports, OAuth, and Backwards Compatibility

Client reliability depends on explicit transport behavior and robust auth handling.

## Learning Goals

- connect clients over stdio, Streamable HTTP, and legacy SSE pathways
- implement fallback flow from HTTP to SSE for older servers
- apply OAuth helpers for secure remote server access
- structure client operations for parallel and multi-server usage

## Practical Client Pattern

1. prefer Streamable HTTP client transport
2. detect known legacy cases and apply SSE fallback
3. use high-level methods (`listTools`, `callTool`, `listResources`)
4. persist auth/token context in tested provider implementations

## Source References

- [Client Docs](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/client.md)
- [Client Examples Index](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/client/README.md)
- [Streamable HTTP Fallback Example](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/client/src/streamableHttpWithSseFallbackClient.ts)

## Summary

You now have a stronger strategy for client transport and auth compatibility.

Next: [Chapter 4: Tool, Resource, Prompt Design and Completions](04-tool-resource-prompt-design-and-completions.md)
