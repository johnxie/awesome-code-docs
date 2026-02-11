---
layout: default
title: "Chapter 2: System Architecture"
nav_order: 2
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 2: System Architecture

This chapter maps Logseq's desktop architecture and data flow.

## Architecture Layers

- Electron shell for desktop runtime and native integrations.
- ClojureScript core for state + domain logic.
- Datascript + filesystem for local-first persistence.

## Data Flow

```text
user action -> event handler -> state update -> markdown write/sync
```

## Core Modules

- parser and block index
- page/link graph manager
- search and query execution
- plugin runtime bridge

## Summary

You can now identify where Logseq responsibilities are split across runtime layers.

Next: [Chapter 3: Local-First Data](03-local-first-data.md)
