---
layout: default
title: "Chapter 3: Session Lifecycle and Task Parallelism"
nav_order: 3
parent: Claude Squad Tutorial
---

# Chapter 3: Session Lifecycle and Task Parallelism

Claude Squad session controls support task creation, pause/resume, and deletion within one terminal workflow.

## Key Session Actions

- create session (`n` / `N`)
- attach/detach (`enter`/`o`, `ctrl-q`)
- pause/resume (`c`, `r`)
- delete session (`D`)

## Parallelism Pattern

Run multiple sessions in parallel for independent features or bug fixes, each on its own worktree branch.

## Source References

- [Claude Squad README: menu and session controls](https://github.com/smtg-ai/claude-squad/blob/main/README.md)

## Summary

You now have a session lifecycle model for high-throughput parallel task execution.

Next: [Chapter 4: Multi-Agent Program Integration](04-multi-agent-program-integration.md)
