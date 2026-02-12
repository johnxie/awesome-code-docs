---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Claude-Mem Tutorial
---

# Chapter 1: Getting Started

This chapter gets Claude-Mem installed and verifies automatic memory behavior in new sessions.

## Learning Goals

- install Claude-Mem from plugin marketplace
- restart Claude Code and confirm memory hooks are active
- validate baseline context persistence across sessions
- locate primary operating surfaces (viewer, settings, docs)

## Quick Install

Inside Claude Code, run:

```text
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

Then restart Claude Code and begin a new session.

## First Validation Loop

- perform a short task with tool usage
- start a new session
- confirm previous context appears via memory priming
- open web viewer (`http://localhost:37777`) to inspect stored activity

## Baseline Checks

- plugin appears in installed plugin list
- worker service responds and logs activity
- context survives session boundary

## Source References

- [README Quick Start](https://github.com/thedotmack/claude-mem/blob/main/README.md#quick-start)
- [Installation Guide](https://docs.claude-mem.ai/installation)
- [Usage Getting Started](https://docs.claude-mem.ai/usage/getting-started)

## Summary

You now have a working Claude-Mem baseline with persistent session memory.

Next: [Chapter 2: Architecture, Hooks, and Worker Flow](02-architecture-hooks-and-worker-flow.md)
