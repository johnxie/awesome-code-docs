---
layout: default
title: "Chapter 2: Server Transports and Deployment Patterns"
nav_order: 2
parent: MCP TypeScript SDK Tutorial
---

# Chapter 2: Server Transports and Deployment Patterns

Server design starts with transport choice and state model, not with tool code.

## Learning Goals

- choose between stateless and stateful Streamable HTTP modes
- understand where deprecated SSE still matters
- map deployment pattern to session/event storage strategy
- pick framework adapter based on runtime constraints

## Deployment Pattern Matrix

| Pattern | Best For | Tradeoff |
|:--------|:---------|:---------|
| Stateless Streamable HTTP | simple API-style servers | no resumability/session continuity |
| Stateful + event store | richer interactions and resumability | external storage complexity |
| Local state + message routing | sticky-session architectures | highest operational complexity |

## Adapter Guidance

- `@modelcontextprotocol/node` for Node `http` integration
- `@modelcontextprotocol/express` for Express defaults + host validation helpers
- `@modelcontextprotocol/hono` for web-standard request handling

## Source References

- [Server Docs](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md)
- [Server Examples Index](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/README.md)
- [Node Adapter README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/middleware/node/README.md)

## Summary

You now have a transport-first architecture model for server implementation.

Next: [Chapter 3: Client Transports, OAuth, and Backwards Compatibility](03-client-transports-oauth-and-backwards-compatibility.md)
