---
layout: default
title: "Chapter 2: Core Protocol Model and Module Architecture"
nav_order: 2
parent: MCP Kotlin SDK Tutorial
---

# Chapter 2: Core Protocol Model and Module Architecture

This chapter explains how the Kotlin SDK separates protocol foundations from runtime roles.

## Learning Goals

- understand what lives in `kotlin-sdk-core` vs client/server modules
- map JSON-RPC and MCP model types to application layers
- use DSL helpers and protocol primitives without over-coupling
- decide when custom transport work belongs in core-level abstractions

## Architecture Boundaries

| Module | Responsibility |
|:-------|:---------------|
| `kotlin-sdk-core` | shared MCP types, JSON handling, protocol abstractions |
| `kotlin-sdk-client` | handshake + typed server calls + capability checks |
| `kotlin-sdk-server` | feature registration + session lifecycle + notifications |

## Design Notes

- `McpJson` and protocol models keep wire formats consistent across runtimes.
- `Protocol` logic centralizes request/response correlation and capability assertions.
- Client/server modules add role-specific ergonomics while reusing the same core schema model.

## Source References

- [Module Overview](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/docs/moduledoc.md)
- [kotlin-sdk-core Module Guide](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-core/Module.md)
- [kotlin-sdk-client Module Guide](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-client/Module.md)
- [kotlin-sdk-server Module Guide](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-server/Module.md)

## Summary

You now have a clear module-level mental model for Kotlin MCP architecture decisions.

Next: [Chapter 3: Client Runtime and Capability Negotiation](03-client-runtime-and-capability-negotiation.md)
