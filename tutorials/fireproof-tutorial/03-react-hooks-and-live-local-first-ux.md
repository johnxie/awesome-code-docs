---
layout: default
title: "Chapter 3: React Hooks and Live Local-First UX"
nav_order: 3
parent: Fireproof Tutorial
---

# Chapter 3: React Hooks and Live Local-First UX

Fireproof provides React hooks so local writes and query updates stay synchronized in UI state.

## Hook Roles

| Hook | Role |
|:-----|:-----|
| `useFireproof` | initialize database and expose helper hooks |
| `useDocument` | manage mutable draft + submit flow |
| `useLiveQuery` | live query results with automatic updates |

## Typical Flow

1. create database with `useFireproof("my-ledger")`
2. edit docs through `useDocument`
3. render lists via `useLiveQuery`

This model removes much of the manual cache invalidation and loading-state orchestration common in CRUD apps.

## Source References

- [Fireproof README: React usage](https://github.com/fireproof-storage/fireproof/blob/main/README.md)
- [React tutorial docs](https://use-fireproof.com/docs/react-tutorial)

## Summary

You now have the React mental model for real-time local-first Fireproof UIs.

Next: [Chapter 4: Ledger, CRDT, and Causal Consistency](04-ledger-crdt-and-causal-consistency.md)
