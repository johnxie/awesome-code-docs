---
layout: default
title: "Chapter 2: System Architecture"
nav_order: 2
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 2: System Architecture

This chapter maps Logseq's architecture from desktop runtime to graph-level services.

## Core Architecture Layers

- **Desktop shell**: Electron runtime and native integration boundary
- **Application core**: ClojureScript state, commands, and domain logic
- **Persistence/index**: plain-text files plus in-memory/query index
- **UI layer**: block editor, page views, graph view, search surfaces

## Data Flow Model

```text
user action -> command/event -> state transition -> file sync/index update -> UI re-render
```

## Module Responsibilities

| Module | Responsibility |
|:-------|:---------------|
| parser | convert markdown/org into block structures |
| block graph manager | maintain parent/child and reference edges |
| query engine | execute page/block graph queries |
| plugin bridge | expose extension hooks safely |

## Architectural Tradeoffs

- local-first responsiveness vs cross-device consistency complexity
- plain-text durability vs richer schema constraints
- extensibility power vs plugin isolation/security overhead

## Summary

You can now reason about where Logseq behavior originates and where to debug architectural issues.

Next: [Chapter 3: Local-First Data](03-local-first-data.md)
