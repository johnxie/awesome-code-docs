---
layout: default
title: "Chapter 5: Vector Stores and Workspace Memory"
nav_order: 5
parent: Cipher Tutorial
---

# Chapter 5: Vector Stores and Workspace Memory

Cipher supports multiple vector backends and optional workspace-scoped memory for team collaboration.

## Storage Strategy

| Component | Common Options |
|:----------|:---------------|
| vector store | Qdrant, Milvus, in-memory |
| chat/session history | SQLite or PostgreSQL paths |
| workspace memory | enabled via dedicated config/env settings |

## Source References

- [Vector stores docs](https://github.com/campfirein/cipher/blob/main/docs/vector-stores.md)
- [Workspace memory docs](https://github.com/campfirein/cipher/blob/main/docs/workspace-memory.md)
- [Chat history docs](https://github.com/campfirein/cipher/blob/main/docs/chat-history.md)

## Summary

You now know how to choose and operate Cipher storage backends for single-user and team scenarios.

Next: [Chapter 6: MCP Integration Patterns](06-mcp-integration-patterns.md)
