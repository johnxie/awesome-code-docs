---
layout: default
title: "Chapter 4: Semantic Search and Vector Processing"
nav_order: 4
parent: MCP Chrome Tutorial
---

# Chapter 4: Semantic Search and Vector Processing

MCP Chrome includes a semantic engine for intelligent tab-content discovery, powered by embeddings and vector search.

## Learning Goals

- understand semantic index architecture at a high level
- identify performance-sensitive parts of the vector pipeline
- plan retrieval quality checks for real workflows

## Semantic Pipeline

```mermaid
flowchart LR
    A[Tab content extraction] --> B[chunking]
    B --> C[embedding generation]
    C --> D[vector index]
    D --> E[query embedding]
    E --> F[similarity search]
    F --> G[ranked context results]
```

## Performance Signals from Architecture Docs

- WebAssembly SIMD is used for faster vector math operations.
- worker-based execution reduces UI blocking.
- vector database configuration controls recall, latency, and memory behavior.

## Source References

- [Architecture: AI Processing and Optimizations](https://github.com/hangwin/mcp-chrome/blob/master/docs/ARCHITECTURE.md)
- [Changelog](https://github.com/hangwin/mcp-chrome/blob/master/docs/CHANGELOG.md)

## Summary

You now have a functional mental model for how semantic tab search works and where tuning matters.

Next: [Chapter 5: Transport Modes and Client Configuration](05-transport-modes-and-client-configuration.md)
