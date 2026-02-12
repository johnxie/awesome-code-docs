---
layout: default
title: "Chapter 3: Client Runtime and Capability Negotiation"
nav_order: 3
parent: MCP Kotlin SDK Tutorial
---

# Chapter 3: Client Runtime and Capability Negotiation

This chapter covers how Kotlin clients initialize connections and safely consume server capabilities.

## Learning Goals

- configure `Client` or `mcpClient` with precise capability declarations
- run initialization and handshake flows correctly
- use typed operations (`listTools`, `callTool`, `readResource`, `getPrompt`) safely
- enforce capability checks to reduce runtime protocol errors

## Client Flow Checklist

1. define `clientInfo` and `ClientOptions` capability set
2. select transport (stdio, SSE, streamable HTTP, WebSocket)
3. call `connect` and inspect negotiated `serverCapabilities`
4. invoke only methods exposed by the server
5. close the client cleanly after operation completion

## Common Failure Modes

- calling optional endpoints before capability verification
- assuming subscriptions/logging are always available
- skipping lifecycle cleanup, leaving in-flight requests unresolved

## Source References

- [Kotlin SDK README - Creating a Client](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/README.md#creating-a-client)
- [kotlin-sdk-client Module Guide](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-client/Module.md)
- [Kotlin MCP Client Sample](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/samples/kotlin-mcp-client/README.md)

## Summary

You now know how to run capability-safe client workflows in Kotlin.

Next: [Chapter 4: Server Runtime, Primitives, and Feature Registration](04-server-runtime-primitives-and-feature-registration.md)
