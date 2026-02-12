---
layout: default
title: "Chapter 2: Architecture and Session Model"
nav_order: 2
parent: Crush Tutorial
---

# Chapter 2: Architecture and Session Model

This chapter explains the core operating model behind Crush's terminal workflows.

## Learning Goals

- understand how Crush structures project and session context
- use session boundaries intentionally across tasks
- apply config precedence correctly for local vs global behavior
- avoid cross-project context leakage

## Core Runtime Concepts

| Concept | Description | Why It Matters |
|:--------|:------------|:---------------|
| session-based operation | multiple work sessions per project | isolate tasks and maintain history |
| project-local config | `.crush.json` or `crush.json` in repo | task- and repo-specific behavior |
| global config | `$HOME/.config/crush/crush.json` | personal defaults across projects |
| global data store | platform-specific data path | state persistence and diagnostics |

## Config Precedence

Crush applies configuration from highest to lowest priority:

1. `.crush.json`
2. `crush.json`
3. `$HOME/.config/crush/crush.json`

This lets teams enforce repo-level conventions while preserving personal defaults.

## Session Isolation Pattern

- keep each major task in a dedicated session
- prefer explicit project-local config for team repositories
- reset session when switching architecture contexts

## Source References

- [Crush README: Configuration](https://github.com/charmbracelet/crush/blob/main/README.md#configuration)
- [Crush README: Features](https://github.com/charmbracelet/crush/blob/main/README.md#features)

## Summary

You now understand how Crush organizes context and configuration across sessions and projects.

Next: [Chapter 3: Providers and Model Configuration](03-providers-and-model-configuration.md)
