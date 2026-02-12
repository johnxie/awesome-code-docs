---
layout: default
title: "Chapter 2: Worktree Isolation and Workspace Model"
nav_order: 2
parent: Superset Terminal Tutorial
---

# Chapter 2: Worktree Isolation and Workspace Model

Superset isolates each active task in its own git worktree and workspace context.

## Isolation Benefits

- avoids branch conflicts between parallel tasks
- preserves clean context per agent run
- enables fast switch/cleanup between active workspaces

## Source References

- [Superset README: worktree isolation](https://github.com/superset-sh/superset/blob/main/README.md)
- [Worktree utility path](https://github.com/superset-sh/superset/blob/main/apps/desktop/src/lib/trpc/routers/workspaces/utils/worktree.ts)

## Summary

You now understand how Superset prevents multi-agent interference through workspace isolation.

Next: [Chapter 3: Workspace Orchestration Lifecycle](03-workspace-orchestration-lifecycle.md)
