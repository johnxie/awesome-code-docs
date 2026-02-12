---
layout: default
title: "Chapter 2: Architecture and Data Model"
nav_order: 2
parent: Beads Tutorial
---

# Chapter 2: Architecture and Data Model

This chapter explains Beads internals for durable agent memory.

## Learning Goals

- understand git-backed graph tracking model
- interpret hash-based IDs and issue relationships
- map status, assignee, and audit semantics
- reason about portability and merge behavior

## Model Highlights

- graph issues with typed relationships
- hash IDs to avoid merge collisions
- structured output for machine-driven workflows

## Source References

- [Beads README Features](https://github.com/steveyegge/beads/blob/main/README.md)
- [Beads Agent Instructions](https://github.com/steveyegge/beads/blob/main/AGENT_INSTRUCTIONS.md)

## Summary

You now understand how Beads persists and structures long-horizon task state.

Next: [Chapter 3: Core Workflow Commands](03-core-workflow-commands.md)
