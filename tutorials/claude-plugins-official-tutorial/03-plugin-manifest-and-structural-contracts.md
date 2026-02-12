---
layout: default
title: "Chapter 3: Plugin Manifest and Structural Contracts"
nav_order: 3
parent: Claude Plugins Official Tutorial
---

# Chapter 3: Plugin Manifest and Structural Contracts

This chapter covers mandatory and optional plugin structure expectations.

## Learning Goals

- identify required plugin metadata files
- understand optional capability directories and when to use them
- apply consistent plugin scaffolding for maintainability
- avoid structural anti-patterns that reduce discoverability

## Standard Plugin Contract

Typical structure includes:

- `.claude-plugin/plugin.json` (required)
- `.mcp.json` (optional)
- `commands/` (optional)
- `agents/` (optional)
- `skills/` (optional)
- `README.md` (strongly recommended)

## Structural Quality Heuristics

- keep command names clear and scoped
- keep agent definitions task-specific
- keep skills modular with explicit activation intent
- document setup and constraints in README

## Source References

- [Directory README Plugin Structure](https://github.com/anthropics/claude-plugins-official/blob/main/README.md#plugin-structure)
- [Example Plugin Reference](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/example-plugin)
- [Plugin Dev Toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev)

## Summary

You now have a clear contract for authoring structurally compliant plugins.

Next: [Chapter 4: Commands, Agents, Skills, Hooks, and MCP Composition](04-commands-agents-skills-hooks-and-mcp-composition.md)
