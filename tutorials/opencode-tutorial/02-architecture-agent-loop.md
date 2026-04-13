---
layout: default
title: "Chapter 2: Architecture and Agent Loop"
nav_order: 2
parent: OpenCode Tutorial
---


# Chapter 2: Architecture and Agent Loop

Welcome to **Chapter 2: Architecture and Agent Loop**. In this part of **OpenCode Tutorial: Open-Source Terminal Coding Agent at Scale**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


OpenCode is built around an interactive coding-agent loop optimized for terminal-native development.

## Core Loop

```mermaid
flowchart LR
    A[Task Input] --> B[Reasoning]
    B --> C[Tool Selection]
    C --> D[Execution]
    D --> E[Result Synthesis]
    E --> F[Next Step or Finish]
```

## Key Components

| Component | Role |
|:----------|:-----|
| client UI | terminal interaction and control |
| agent runtime | planning + execution orchestration |
| tool system | file, shell, and search operations |
| provider layer | model routing and inference integration |

## Why This Matters

Understanding this loop helps you tune OpenCode behavior without relying on trial and error.

## Source References

- [OpenCode Repository](https://github.com/anomalyco/opencode)
- [OpenCode Docs](https://opencode.ai/docs)

## Summary

You now have the architecture mental model required for safe customization.

Next: [Chapter 3: Model and Provider Routing](03-model-and-provider-routing.md)

## How These Components Connect

```mermaid
flowchart TD
    A[User Input] --> B[OpenCode Client TUI]
    B --> C[Agent Runtime]
    C --> D[Planning Phase]
    D --> E[Tool Execution]
    E --> F[File Edits / Shell Cmds]
    F --> G[Result Synthesis]
    G --> B
```
