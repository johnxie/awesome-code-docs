---
layout: default
title: "Chapter 2: Orchestration Architecture"
nav_order: 2
parent: Vibe Kanban Tutorial
---

# Chapter 2: Orchestration Architecture

This chapter explains the core architecture that turns Vibe Kanban into a multi-agent command center.

## Learning Goals

- understand board-driven orchestration flow
- map task state to agent execution lifecycle
- reason about switching and sequencing agent runs
- align architecture with review workflow design

## Core System Model

| Layer | Responsibility |
|:------|:---------------|
| board/task layer | task planning, status tracking, ownership visibility |
| orchestration layer | start/stop/switch coding agents and workflows |
| review layer | quick validation, dev-server checks, handoff control |
| config layer | centralize MCP and runtime settings |

## Why This Matters

Vibe Kanban helps teams avoid context fragmentation by keeping planning, execution, and review in one loop.

## Source References

- [Vibe Kanban README: Overview](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#overview)
- [Vibe Kanban Docs](https://vibekanban.com/docs)

## Summary

You now understand how Vibe Kanban coordinates planning and execution across many coding agents.

Next: [Chapter 3: Multi-Agent Execution Strategies](03-multi-agent-execution-strategies.md)
