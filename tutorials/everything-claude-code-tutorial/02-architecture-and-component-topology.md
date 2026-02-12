---
layout: default
title: "Chapter 2: Architecture and Component Topology"
nav_order: 2
parent: Everything Claude Code Tutorial
---

# Chapter 2: Architecture and Component Topology

This chapter maps the system into manageable component groups.

## Learning Goals

- understand role boundaries between agents, skills, hooks, commands, and rules
- map critical files and folders to runtime behavior
- identify where to customize without breaking portability
- reason about orchestration paths from command to output

## Core Topology

- `agents/`: specialist delegations (planning, review, security, docs, etc.)
- `skills/`: reusable workflow and domain modules
- `commands/`: high-level task entrypoints
- `hooks/`: automated lifecycle enforcement and reminders
- `rules/`: persistent project and language guidance
- MCP configs: external capability integrations

## Architectural Principle

Keep each layer focused and composable; avoid collapsing all behavior into one layer.

## Source References

- [README What's Inside](https://github.com/affaan-m/everything-claude-code/blob/main/README.md#-whats-inside)
- [Agents Directory](https://github.com/affaan-m/everything-claude-code/tree/main/agents)
- [Skills Directory](https://github.com/affaan-m/everything-claude-code/tree/main/skills)

## Summary

You now understand the component architecture and boundaries.

Next: [Chapter 3: Installation Modes and Rules Strategy](03-installation-modes-and-rules-strategy.md)
