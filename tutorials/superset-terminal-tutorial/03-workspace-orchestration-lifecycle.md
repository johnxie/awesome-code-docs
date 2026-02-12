---
layout: default
title: "Chapter 3: Workspace Orchestration Lifecycle"
nav_order: 3
parent: Superset Terminal Tutorial
---

# Chapter 3: Workspace Orchestration Lifecycle

Superset orchestrates workspace CRUD and related cascade operations for processes and diffs.

## Lifecycle Responsibilities

| Operation | Behavior |
|:----------|:---------|
| create | initialize workspace metadata and select active workspace |
| list/get/update | read and mutate workspace state |
| delete | cascade cleanup of process and diff artifacts |

## Source References

- [Workspace orchestrator implementation](https://github.com/superset-sh/superset/blob/main/apps/cli/src/lib/orchestrators/workspace-orchestrator.ts)
- [Workspace init manager](https://github.com/superset-sh/superset/blob/main/apps/desktop/src/main/lib/workspace-init-manager.ts)

## Summary

You now have a concrete lifecycle model for Superset workspace management.

Next: [Chapter 4: Multi-Agent Program Compatibility](04-multi-agent-program-compatibility.md)
