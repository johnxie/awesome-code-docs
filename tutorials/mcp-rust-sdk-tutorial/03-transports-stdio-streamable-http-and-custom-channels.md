---
layout: default
title: "Chapter 3: Transports: stdio, Streamable HTTP, and Custom Channels"
nav_order: 3
parent: MCP Rust SDK Tutorial
---

# Chapter 3: Transports: stdio, Streamable HTTP, and Custom Channels

Transport strategy should be deliberate, especially in async-heavy Rust services.

## Learning Goals

- choose transport features that match deployment topology
- reason about stdio subprocess vs streamable HTTP operational tradeoffs
- implement custom transport adapters safely
- preserve protocol guarantees while scaling concurrency

## Transport Feature Highlights

- `transport-io`: server stdio transport
- `transport-child-process`: client stdio transport
- streamable HTTP server/client features for networked deployments
- custom transport pathways for specialized channels

## Source References

- [rmcp README - Transport Options](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md#transport-options)
- [Examples Transport Index](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/README.md)
- [Client Examples - Streamable HTTP](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/clients/README.md)

## Summary

You now have a transport planning framework for matching capability requirements to runtime constraints.

Next: [Chapter 4: Client Patterns, Sampling, and Batching Flows](04-client-patterns-sampling-and-batching-flows.md)
