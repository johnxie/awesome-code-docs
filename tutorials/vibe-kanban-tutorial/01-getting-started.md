---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Vibe Kanban Tutorial
---

# Chapter 1: Getting Started

This chapter gets Vibe Kanban running with your preferred coding agent environment.

## Learning Goals

- launch Vibe Kanban via the CLI bootstrap path
- connect authenticated coding agents
- create first task board workflow
- verify local baseline and resolve startup issues

## Quick Launch

```bash
npx vibe-kanban
```

## Startup Checklist

1. authenticate at least one supported coding agent first
2. launch Vibe Kanban
3. create/import project context
4. add a few tasks to board columns
5. assign tasks to agent workflows

## Common Startup Issues

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| agent unavailable | missing agent auth state | authenticate agent CLI and retry |
| commands fail to run | environment/toolchain mismatch | verify required runtimes and path settings |
| MCP errors | host/port/origin mismatch | review MCP and origin-related settings |

## Source References

- [Vibe Kanban README: Installation](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#installation)
- [Vibe Kanban Docs](https://vibekanban.com/docs)

## Summary

You now have Vibe Kanban up and ready for multi-agent task orchestration.

Next: [Chapter 2: Orchestration Architecture](02-orchestration-architecture.md)
