---
layout: default
title: "Chapter 1: Getting Started and Crate Setup"
nav_order: 1
parent: MCP Rust SDK Tutorial
---

# Chapter 1: Getting Started and Crate Setup

This chapter defines a clean onboarding baseline for rmcp projects.

## Learning Goals

- choose the right crate and feature set for your first implementation
- align runtime dependencies (`tokio`, `serde`, `schemars`) to SDK expectations
- bootstrap minimal client/server flows quickly
- avoid over-enabling transport/auth features before needed

## Baseline Setup

```toml
rmcp = { version = "0.15", features = ["server"] }
```

Start with one transport path and one capability surface, then add features incrementally.

## Source References

- [Rust SDK README Usage](https://github.com/modelcontextprotocol/rust-sdk/blob/main/README.md)
- [rmcp README Quick Start](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md)

## Summary

You now have a dependency baseline that keeps early integrations predictable.

Next: [Chapter 2: Service Model and Macro-Based Tooling](02-service-model-and-macro-based-tooling.md)
