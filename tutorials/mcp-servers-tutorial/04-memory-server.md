---
layout: default
title: "Chapter 4: Memory Server"
nav_order: 4
parent: MCP Servers Tutorial
---

# Chapter 4: Memory Server

The memory server is a clean reference for persistent, structured memory using a local knowledge graph.

## Data Model

The official model uses three primitives:

- **Entities**: named nodes with types and observations
- **Relations**: directed edges between entities
- **Observations**: atomic facts attached to entities

This encourages explicit memory structure instead of opaque long-context accumulation.

## Tool Groups

The server groups operations into:

- create: entities and relations
- update: add observations
- delete: entities/relations/observations
- query: search nodes, open nodes, read entire graph

This surface is small but expressive enough for many memory patterns.

## Design Advantages

- easy to inspect and debug state
- selective deletion and correction
- relation-based retrieval beyond plain text search
- portable JSON-like structures for external storage

## Operational Caveats

Memory quality degrades quickly without governance.

Add controls for:

- duplicate entities and alias handling
- contradictory observations
- stale relations
- source attribution and confidence labels

## Prompting Pattern

A practical pattern is:

1. retrieve relevant nodes first
2. reason with retrieved memory
3. apply bounded updates only when confidence is high

Avoid writing memory for every interaction. Quality beats quantity.

## Summary

You now understand how graph-based memory differs from ad-hoc conversation history and why it can be productionized more safely.

Next: [Chapter 5: Multi-Language Servers](05-multi-language-servers.md)
