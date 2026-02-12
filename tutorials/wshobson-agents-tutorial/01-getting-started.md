---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Wshobson Agents Tutorial
---

# Chapter 1: Getting Started

This chapter gets the marketplace connected and installs your first focused plugin set.

## Learning Goals

- add the marketplace to Claude Code
- install a minimal but useful first plugin portfolio
- verify slash-command discovery and invocation
- avoid over-installing plugins in early setup

## Quick Start Commands

```bash
/plugin marketplace add wshobson/agents
/plugin
/plugin install python-development
/plugin install code-review-ai
```

After installation, re-run `/plugin` and verify new commands are available.

## First-Session Operating Pattern

- pick one command workflow, for example test generation or review
- run a small target scope first
- validate output quality before adding more plugins

## Baseline Plugin Starter Set

- `python-development`
- `javascript-typescript`
- `code-review-ai`
- `git-pr-workflows`

This set is enough for many day-one coding loops.

## Source References

- [README Quick Start](https://github.com/wshobson/agents/blob/main/README.md#quick-start)
- [Plugin Reference](https://github.com/wshobson/agents/blob/main/docs/plugins.md)

## Summary

You now have a working baseline installation and first command surface.

Next: [Chapter 2: Marketplace Architecture and Plugin Structure](02-marketplace-architecture-and-plugin-structure.md)
