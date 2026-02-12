---
layout: default
title: "Chapter 4: Client Patterns, Sampling, and Batching Flows"
nav_order: 4
parent: MCP Rust SDK Tutorial
---

# Chapter 4: Client Patterns, Sampling, and Batching Flows

Client reliability depends on disciplined async flow control and capability usage.

## Learning Goals

- structure client lifecycle and tool invocation loops cleanly
- handle sampling and progress flows without blocking the event loop
- use batching/multi-client patterns where they improve throughput
- keep error propagation explicit across async boundaries

## Client Strategy

- start from simple stdio or streamable client examples
- layer OAuth-enabled clients only when needed
- separate request orchestration from business logic
- test concurrent request patterns under realistic load

## Source References

- [Client Examples README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/clients/README.md)
- [Simple Chat Client README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/simple-chat-client/README.md)
- [rmcp README - Client Implementation](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md#client-implementation)

## Summary

You now have a client execution model for handling advanced capability flows under async load.

Next: [Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks](05-server-patterns-tools-resources-prompts-and-tasks.md)
