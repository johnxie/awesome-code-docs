---
layout: default
title: "Chapter 7: CLI/TUI Architecture for Contributors"
nav_order: 7
parent: Kilo Code Tutorial
---

# Chapter 7: CLI/TUI Architecture for Contributors

Kilo's CLI stack separates extension-host runtime, state client, ask dispatch, and UI rendering concerns.

## Architecture Blocks

| Component | Responsibility |
|:----------|:---------------|
| extension host | load/activate extension runtime |
| extension client | single source of truth for agent state |
| ask dispatcher | route interactive asks and approvals |
| output/prompt managers | terminal output and input orchestration |

## Source References

- [Extension host implementation](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/src/agent/extension-host.ts)
- [Agent module tree](https://github.com/Kilo-Org/kilocode/tree/main/apps/cli/src/agent)

## Summary

You now have a contributor-level map for Kilo CLI internals.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
