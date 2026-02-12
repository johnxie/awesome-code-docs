---
layout: default
title: "Chapter 2: Service Model and Macro-Based Tooling"
nav_order: 2
parent: MCP Rust SDK Tutorial
---

# Chapter 2: Service Model and Macro-Based Tooling

rmcp macros and handler traits shape how maintainable your server code becomes.

## Learning Goals

- use `#[tool]`, `#[tool_router]`, and `#[tool_handler]` effectively
- keep service state and handler boundaries explicit
- generate schemas and typed interfaces with less manual boilerplate
- avoid macro-heavy patterns that hide critical protocol behavior

## Design Rules

- keep tools cohesive around one service domain
- use routers for explicit capability discovery boundaries
- validate generated schema output for complex input/output types
- document macro-generated behavior for team maintainability

## Source References

- [rmcp-macros README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp-macros/README.md)
- [rmcp README - Server Implementation](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md#server-implementation)

## Summary

You now have a practical model for macro-driven capability design in Rust.

Next: [Chapter 3: Transports: stdio, Streamable HTTP, and Custom Channels](03-transports-stdio-streamable-http-and-custom-channels.md)
