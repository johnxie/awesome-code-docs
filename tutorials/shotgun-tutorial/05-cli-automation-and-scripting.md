---
layout: default
title: "Chapter 5: CLI Automation and Scripting"
nav_order: 5
parent: Shotgun Tutorial
---

# Chapter 5: CLI Automation and Scripting

Shotgun includes CLI commands for non-interactive and automation-friendly usage.

## Key Commands

```bash
shotgun run "Research auth architecture and produce implementation plan"
shotgun run -n "Analyze current retry strategy"
shotgun run -p anthropic "Generate staged refactor plan"
```

## Utility Commands

- `shotgun context` for token usage visibility
- `shotgun compact` for conversation compaction
- `shotgun codebase index` and `shotgun codebase info` for graph lifecycle

## CI Pattern

Use `shotgun run -n` in controlled environments where deterministic prompt templates and post-run validation steps are in place.

## Source References

- [Shotgun CLI Docs](https://github.com/shotgun-sh/shotgun/blob/main/docs/CLI.md)

## Summary

You can now run Shotgun workflows both interactively and in scripted pipelines.

Next: [Chapter 6: Context7 MCP and Local Models](06-context7-mcp-and-local-models.md)
