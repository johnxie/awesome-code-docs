---
layout: default
title: "Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic"
nav_order: 4
parent: Claude Code Router Tutorial
---

# Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic

This chapter focuses on resilient route policy design.

## Learning Goals

- configure scenario-specific routing decisions
- define fallback model chains for degraded conditions
- use project-level overrides responsibly
- route subagent workloads explicitly when needed

## Routing Layers

1. global default router
2. scenario routes (`background`, `think`, `longContext`, `webSearch`, `image`)
3. project-level override file
4. optional custom router script
5. fallback list on provider/model failure

## Source References

- [Routing Config Docs](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/config/routing.md)
- [README: Router](https://github.com/musistudio/claude-code-router/blob/main/README.md#router)
- [README: Subagent Routing](https://github.com/musistudio/claude-code-router/blob/main/README.md#subagent-routing)

## Summary

You now know how to design routing for both performance and resilience.

Next: [Chapter 5: CLI Operations: Model, Preset, and Statusline Workflows](05-cli-operations-model-preset-and-statusline-workflows.md)
