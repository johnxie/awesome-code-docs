---
layout: default
title: "Chapter 7: Development and Source Build Workflow"
nav_order: 7
parent: Vibe Kanban Tutorial
---

# Chapter 7: Development and Source Build Workflow

This chapter targets contributors building and extending Vibe Kanban from source.

## Learning Goals

- set up prerequisite toolchain for development
- run local dev server reliably
- build frontend/source artifacts for release testing
- understand contributor expectations before submitting changes

## Development Prerequisites

From README:

- Rust (stable)
- Node.js >= 18
- pnpm >= 8
- optional dev tools: `cargo-watch`, `sqlx-cli`

## Common Commands

```bash
pnpm i
pnpm run dev
```

## Build and Debug Paths

- frontend-only build through `frontend` workspace
- macOS local build script for source test workflows

## Source References

- [Vibe Kanban README: Development](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#development)
- [Vibe Kanban README: Build from source](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#build-from-source-macos)

## Summary

You now have a contributor-ready workflow for iterating on Vibe Kanban itself.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
