---
layout: default
title: "Chapter 2: Core Document API and Query Lifecycle"
nav_order: 2
parent: Fireproof Tutorial
---

# Chapter 2: Core Document API and Query Lifecycle

Fireproof exposes familiar document-database operations with explicit support for change streams and query indexes.

## Core Operations

| Operation | Purpose |
|:----------|:--------|
| `put` | insert or update document |
| `get` | retrieve by `_id` |
| `del` / `remove` | delete by `_id` |
| `query` | indexed lookups |
| `changes` | incremental change feed |
| `allDocs` | full document scan |

## Implementation Notes

In the core implementation, `DatabaseImpl` delegates durable operations through a ledger write queue and CRDT-backed data model.

## Practical Pattern

Use `changes` or subscriptions to avoid full reload loops when building reactive interfaces.

## Source References

- [DatabaseImpl API surface](https://github.com/fireproof-storage/fireproof/blob/main/core/base/database.ts)

## Summary

You now understand the document lifecycle and read/query semantics.

Next: [Chapter 3: React Hooks and Live Local-First UX](03-react-hooks-and-live-local-first-ux.md)
