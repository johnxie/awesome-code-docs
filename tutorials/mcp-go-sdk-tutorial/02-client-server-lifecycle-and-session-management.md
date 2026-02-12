---
layout: default
title: "Chapter 2: Client/Server Lifecycle and Session Management"
nav_order: 2
parent: MCP Go SDK Tutorial
---

# Chapter 2: Client/Server Lifecycle and Session Management

Session lifecycle discipline is the difference between stable and flaky MCP behavior.

## Learning Goals

- understand the `Client` and `Server` as logical multi-peer entities
- use `ClientSession` and `ServerSession` lifecycles correctly
- align initialization timing with feature handler readiness
- close and wait on sessions to prevent goroutine leaks

## Session Flow Highlights

- `Client.Connect` initializes the session and returns a `ClientSession`
- `Server.Connect` creates a `ServerSession`; initialization completes after client `initialized`
- requests should be gated until initialization is complete
- always call `Close` and, where relevant, `Wait` in shutdown paths

## Operational Checklist

1. connect server transport before connecting client in in-memory tests
2. instrument initialization handlers to verify negotiated capability state
3. ensure shutdown path handles both local close and peer disconnect
4. test reconnect behavior under transport interruptions

## Source References

- [Protocol Lifecycle](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md#lifecycle)
- [mcp.Client](https://pkg.go.dev/github.com/modelcontextprotocol/go-sdk/mcp#Client)
- [mcp.Server](https://pkg.go.dev/github.com/modelcontextprotocol/go-sdk/mcp#Server)

## Summary

You now have lifecycle patterns that reduce race conditions and hanging sessions.

Next: [Chapter 3: Transports: stdio, Streamable HTTP, and Custom Flows](03-transports-stdio-streamable-http-and-custom-flows.md)
