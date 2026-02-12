---
layout: default
title: "Chapter 5: Session, History, and Context Persistence"
nav_order: 5
parent: Kilo Code Tutorial
---

# Chapter 5: Session, History, and Context Persistence

Kilo persists CLI state such as history and settings to maintain continuity across runs.

## Persistence Artifacts

| Artifact | Purpose |
|:---------|:--------|
| settings | onboarding/provider mode preferences |
| history | prompt/input recall across sessions |
| credentials | authentication tokens/session identity |

## Source References

- [Storage settings module](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/src/lib/storage/settings.ts)
- [History persistence module](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/src/lib/storage/history.ts)

## Summary

You now have a clear model for how Kilo preserves user context over time.

Next: [Chapter 6: Extensions, MCP, and Custom Modes](06-extensions-mcp-and-custom-modes.md)
