---
layout: default
title: "Chapter 5: Multi-Language Servers"
nav_order: 5
parent: MCP Servers Tutorial
---

# Chapter 5: Multi-Language Servers

The reference repository shows equivalent patterns across ecosystems.

## Comparison Lens

| Language | Typical Strength | Common Runtime |
|:---------|:------------------|:---------------|
| Python | Fast prototyping, AI ecosystem | CPython + asyncio |
| TypeScript | Web-native tooling, typing | Node.js |
| Rust | Performance and memory safety | native binary |

## Portability Principles

- Keep protocol contracts language-agnostic.
- Mirror tool names and schemas across implementations.
- Standardize error payloads for consistent client behavior.

## Summary

You can now evaluate implementation tradeoffs without changing protocol semantics.

Next: [Chapter 6: Custom Server Development](06-custom-server-development.md)
