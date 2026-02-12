---
layout: default
title: "Chapter 2: SDK Architecture: Reactive Model and JSON Layer"
nav_order: 2
parent: MCP Java SDK Tutorial
---

# Chapter 2: SDK Architecture: Reactive Model and JSON Layer

Java SDK architecture choices are deliberate and affect interoperability and operability.

## Learning Goals

- understand the reactive-first API posture and sync facade rationale
- map JSON abstraction and Jackson implementation choices
- reason about observability propagation and logging strategy
- connect architecture choices to deployment constraints

## Architecture Highlights

- reactive streams are the primary abstraction for async and streaming MCP interactions
- sync APIs are layered on top for blocking-friendly usage
- JSON mapper and schema validation are abstracted, with Jackson implementations provided
- logging is SLF4J-based for backend neutrality

## Practical Implications

- keep async boundaries explicit when building high-throughput servers
- use sync facades only where blocking behavior is acceptable
- validate schema configuration early in integration tests
- propagate correlation and trace context across reactive boundaries

## Source References

- [Architecture and Design Decisions](https://github.com/modelcontextprotocol/java-sdk/blob/main/README.md#architecture-and-design-decisions)
- [mcp-core JSON and Schema Packages](https://github.com/modelcontextprotocol/java-sdk/tree/main/mcp-core/src/main/java/io/modelcontextprotocol/json)
- [mcp-json-jackson3 Module](https://github.com/modelcontextprotocol/java-sdk/tree/main/mcp-json-jackson3)

## Summary

You now understand why Java SDK core abstractions are shaped for bidirectional async protocol workloads.

Next: [Chapter 3: Client Transports and Connection Strategy](03-client-transports-and-connection-strategy.md)
