---
layout: default
title: "Chapter 7: Runtime and Package Architecture"
nav_order: 7
parent: Superset Terminal Tutorial
---

# Chapter 7: Runtime and Package Architecture

Superset separates desktop runtime concerns and shared agent-execution logic into modular packages.

## Architecture Surfaces

| Surface | Purpose |
|:--------|:--------|
| desktop runtime | workspace/session lifecycle, notifications, terminal hosting |
| CLI orchestration | workspace command and state operations |
| shared `@superset/agent` package | common agent execution logic across environments |

## Source References

- [Shared agent package docs](https://github.com/superset-sh/superset/blob/main/packages/agent/README.md)
- [Desktop main runtime modules](https://github.com/superset-sh/superset/tree/main/apps/desktop/src/main)

## Summary

You now have a contributor-level map of Superset runtime boundaries.

Next: [Chapter 8: Production Team Operations](08-production-team-operations.md)
