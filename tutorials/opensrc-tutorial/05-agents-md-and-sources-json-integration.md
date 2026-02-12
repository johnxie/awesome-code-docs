---
layout: default
title: "Chapter 5: AGENTS.md and sources.json Integration"
nav_order: 5
parent: OpenSrc Tutorial
---

# Chapter 5: AGENTS.md and sources.json Integration

OpenSrc can update project metadata so coding agents know where imported source context lives.

## Integration Outputs

| File | Purpose |
|:-----|:--------|
| `opensrc/sources.json` | machine-readable index of fetched packages/repos |
| `AGENTS.md` | agent-facing guidance that source context exists in `opensrc/` |
| `.gitignore` | ignore imported source cache |
| `tsconfig.json` | exclude `opensrc/` from normal compile scope |

## Permission Model

On first run, OpenSrc asks if file modifications are allowed. The preference is persisted in `opensrc/settings.json`.

## Source References

- [Fetch command integration flow](https://github.com/vercel-labs/opensrc/blob/main/src/commands/fetch.ts)
- [AGENTS.md and index updater](https://github.com/vercel-labs/opensrc/blob/main/src/lib/agents.ts)

## Summary

You now know how OpenSrc surfaces fetched sources to agent workflows without manual file editing.

Next: [Chapter 6: Update, Remove, and Clean Lifecycle](06-update-remove-and-clean-lifecycle.md)
