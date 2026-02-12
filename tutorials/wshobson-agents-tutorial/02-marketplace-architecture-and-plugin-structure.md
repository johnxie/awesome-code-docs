---
layout: default
title: "Chapter 2: Marketplace Architecture and Plugin Structure"
nav_order: 2
parent: Wshobson Agents Tutorial
---

# Chapter 2: Marketplace Architecture and Plugin Structure

This chapter explains the repository's composable plugin architecture.

## Learning Goals

- understand how plugins isolate capabilities
- map relationships between `agents`, `commands`, and `skills`
- identify where marketplace metadata lives
- evaluate plugin design quality quickly

## Structural Overview

Key paths:

- `.claude-plugin/marketplace.json`: plugin catalog metadata
- `plugins/<plugin-name>/agents/`: specialist agent prompts
- `plugins/<plugin-name>/commands/`: slash-command behavior
- `plugins/<plugin-name>/skills/`: progressive-disclosure skill packs
- `docs/`: operator and contributor documentation

## Design Principles

The project emphasizes:

- single-responsibility plugins
- composability over monolithic bundles
- minimal token footprint by selective installs
- maintainable boundaries for updates and reviews

## Architecture Review Checklist

- is plugin scope focused and clearly named?
- are command names predictable and discoverable?
- do skills have clear activation criteria?
- is there overlap that should be decomposed further?

## Source References

- [Architecture Guide](https://github.com/wshobson/agents/blob/main/docs/architecture.md)
- [Marketplace Directory](https://github.com/wshobson/agents/tree/main/.claude-plugin)
- [Plugins Directory](https://github.com/wshobson/agents/tree/main/plugins)

## Summary

You now understand the composable architecture that powers the ecosystem.

Next: [Chapter 3: Installation and Plugin Selection Strategy](03-installation-and-plugin-selection-strategy.md)
