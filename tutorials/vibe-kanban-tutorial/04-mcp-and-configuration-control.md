---
layout: default
title: "Chapter 4: MCP and Configuration Control"
nav_order: 4
parent: Vibe Kanban Tutorial
---

# Chapter 4: MCP and Configuration Control

This chapter covers how Vibe Kanban centralizes MCP and runtime configuration to reduce agent drift.

## Learning Goals

- manage coding-agent MCP settings from one control surface
- apply host/port/origin settings safely for local and hosted deployments
- troubleshoot common configuration mismatches
- enforce stable team defaults

## Key Config Domains

| Domain | Example Variables |
|:-------|:------------------|
| network/runtime | `HOST`, `PORT`, `BACKEND_PORT`, `FRONTEND_PORT` |
| MCP connectivity | `MCP_HOST`, `MCP_PORT` |
| hosted deployment | `VK_ALLOWED_ORIGINS` |
| operational toggles | `DISABLE_WORKTREE_CLEANUP` |

## Control Practices

- treat configuration as versioned infrastructure
- separate dev defaults from production settings
- validate MCP and origin rules before broad rollout

## Source References

- [Vibe Kanban README: Environment Variables](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#environment-variables)
- [Vibe Kanban Docs: configuration](https://vibekanban.com/docs/configuration-customisation)

## Summary

You now have a practical model for MCP/runtime configuration governance in Vibe Kanban.

Next: [Chapter 5: Review and Quality Gates](05-review-and-quality-gates.md)
