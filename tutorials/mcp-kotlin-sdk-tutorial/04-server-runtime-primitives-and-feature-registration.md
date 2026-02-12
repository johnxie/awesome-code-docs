---
layout: default
title: "Chapter 4: Server Runtime, Primitives, and Feature Registration"
nav_order: 4
parent: MCP Kotlin SDK Tutorial
---

# Chapter 4: Server Runtime, Primitives, and Feature Registration

This chapter explains how Kotlin MCP servers register and manage primitives with capability discipline.

## Learning Goals

- set `ServerOptions` and capabilities intentionally
- register tools, prompts, resources, and templates cleanly
- manage session lifecycle hooks and list-change notifications
- structure server code for later transport and scaling changes

## Primitive Registration Strategy

| Primitive | Typical API Surface |
|:----------|:--------------------|
| Tools | `addTool`, dynamic updates, list-changed notifications |
| Prompts | `addPrompt`, argument metadata, prompt retrieval |
| Resources | `addResource`, template exposure, optional subscriptions |

## Server Guidance

- advertise only capabilities you actively support.
- enable list-changed notifications only when clients need dynamic discovery.
- keep handlers deterministic and bounded to avoid long blocking tasks.

## Source References

- [Kotlin SDK README - Creating a Server](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/README.md#creating-a-server)
- [kotlin-sdk-server Module Guide](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-server/Module.md)
- [Kotlin MCP Server Sample](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/samples/kotlin-mcp-server/README.md)
- [Weather STDIO Sample](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/samples/weather-stdio-server/README.md)

## Summary

You now have a server-side primitive model that is consistent with MCP capability negotiation.

Next: [Chapter 5: Transports: stdio, Streamable HTTP, SSE, and WebSocket](05-transports-stdio-streamable-http-sse-and-websocket.md)
