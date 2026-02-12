---
layout: default
title: "Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic"
nav_order: 4
parent: Claude Code Router Tutorial
---

# Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic

This chapter covers how to shape model routing behavior by scenario and failure mode.

## Learning Goals

- configure scenario-based routes (`background`, `think`, `longContext`, etc.)
- apply fallback chains for resilience
- use project-level and custom router overrides responsibly
- route subagent workloads to explicit models where needed

## Routing Layers

1. global `Router.default` baseline
2. scenario-specific route overrides
3. project-level route files
4. optional custom router function
5. fallback model chains on failure

## Source References

- [Routing Config Docs](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/config/routing.md)
- [README: Router and Custom Router](https://github.com/musistudio/claude-code-router/blob/main/README.md#router)
- [README: Subagent Routing](https://github.com/musistudio/claude-code-router/blob/main/README.md#subagent-routing)

## Summary

You now know how to build robust routing logic with graceful degradation paths.

Next: [Chapter 5: CLI Operations: Model, Preset, and Statusline Workflows](05-cli-operations-model-preset-and-statusline-workflows.md)
