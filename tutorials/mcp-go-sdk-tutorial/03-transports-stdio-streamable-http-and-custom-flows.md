---
layout: default
title: "Chapter 3: Transports: stdio, Streamable HTTP, and Custom Flows"
nav_order: 3
parent: MCP Go SDK Tutorial
---

# Chapter 3: Transports: stdio, Streamable HTTP, and Custom Flows

Transport selection should follow deployment shape and threat model, not convenience.

## Learning Goals

- choose stdio vs streamable HTTP deliberately
- handle resumability/redelivery and stateless mode tradeoffs
- understand custom transport extension points
- apply concurrency expectations when handling calls and notifications

## Transport Patterns

| Pattern | When to Use | Watchouts |
|:--------|:------------|:----------|
| `CommandTransport` + `StdioTransport` | local process orchestration | subprocess lifecycle + stdout purity |
| `StreamableHTTPHandler` + `StreamableClientTransport` | remote/shared deployments | session ID handling, origin checks, reconnection semantics |
| custom `Transport` | bespoke runtime channels | strict JSON-RPC framing and lifecycle compatibility |

## Streamable Notes

- resumability requires an event store (`EventStore`)
- stateless mode exists but cannot support server-initiated request/response semantics the same way as stateful sessions
- concurrency guarantees are limited; design handlers for async request overlap

## Source References

- [Protocol Transports](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md#transports)
- [Streamable HTTP Example](https://github.com/modelcontextprotocol/go-sdk/blob/main/examples/http/README.md)
- [Custom Transport Example](https://github.com/modelcontextprotocol/go-sdk/tree/main/examples/server/custom-transport)

## Summary

You now have a transport strategy that is aligned with Go SDK behavior and operational constraints.

Next: [Chapter 4: Building Tools, Resources, and Prompts in Go](04-building-tools-resources-and-prompts-in-go.md)
