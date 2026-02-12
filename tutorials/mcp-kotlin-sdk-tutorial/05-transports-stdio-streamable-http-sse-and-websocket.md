---
layout: default
title: "Chapter 5: Transports: stdio, Streamable HTTP, SSE, and WebSocket"
nav_order: 5
parent: MCP Kotlin SDK Tutorial
---

# Chapter 5: Transports: stdio, Streamable HTTP, SSE, and WebSocket

This chapter maps transport options to deployment and operational constraints.

## Learning Goals

- choose the right transport for local tooling vs remote services
- understand session behavior differences across transports
- align Ktor client/server dependencies with transport choices
- reduce transport-related debugging cycles in early deployment

## Transport Selection Matrix

| Transport | Best Fit |
|:----------|:---------|
| stdio | local CLI/editor integrations and subprocess servers |
| Streamable HTTP | web service-style request/response with streaming support |
| SSE | server push plus POST back-channel patterns |
| WebSocket | long-lived bidirectional sessions |

## Operational Notes

- stdio is easiest for local integrations but harder to observe at scale.
- HTTP/SSE paths require session and header handling discipline.
- WebSocket simplifies bi-directional messaging but needs robust connection lifecycle handling.

## Source References

- [Kotlin SDK README - Transports](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/README.md#transports)
- [kotlin-sdk-client Module Guide - Ktor Transports](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-client/Module.md)
- [kotlin-sdk-server Module Guide - Ktor Hosting](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-server/Module.md)

## Summary

You now have a practical framework for choosing Kotlin MCP transports by workload.

Next: [Chapter 6: Advanced Client Features: Roots, Sampling, and Elicitation](06-advanced-client-features-roots-sampling-and-elicitation.md)
