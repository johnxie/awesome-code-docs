---
layout: default
title: "Chapter 3: Learning, Memory, and State"
nav_order: 3
parent: Agno Tutorial
---


# Chapter 3: Learning, Memory, and State

Welcome to **Chapter 3: Learning, Memory, and State**. In this part of **Agno Tutorial: Multi-Agent Systems That Learn Over Time**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Agno's differentiator is persistent learning behavior across sessions and users.

## Memory Model

| Type | Purpose |
|:-----|:--------|
| user profile memory | cross-session personalization |
| conversation memory | current dialogue continuity |
| learned shared knowledge | transferable improvements across users |

## Design Rules

- separate volatile session state from durable memory
- validate memory quality before promotion to shared knowledge
- define retention and deletion policies early

## Source References

- [Agno Docs](https://docs.agno.com)
- [Agno README](https://github.com/agno-agi/agno)

## Summary

You now know how to structure Agno memory for sustainable long-term improvement.

Next: [Chapter 4: Multi-Agent Orchestration](04-multi-agent-orchestration.md)

## Source Code Walkthrough

### `libs/agno/agno/memory/` and storage backends

Memory and state management are implemented in [`libs/agno/agno/memory/`](https://github.com/agno-agi/agno/tree/HEAD/libs/agno/agno/memory). This module contains the memory manager, session storage, and user memory classes that Chapter 3 covers. The storage backends (SQLite, PostgreSQL, Redis) show how Agno persists state across runs — review the base storage interface to understand the abstraction layer before examining specific implementations.