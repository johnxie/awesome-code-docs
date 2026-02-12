---
layout: default
title: "Chapter 2: Architecture and Package Topology"
nav_order: 2
parent: Claude Code Router Tutorial
---

# Chapter 2: Architecture and Package Topology

This chapter maps CCR components and request flow boundaries.

## Learning Goals

- understand roles of CLI, server, and shared packages
- trace route selection through transformer pipelines
- identify extension points for custom behavior
- reduce debugging ambiguity in multi-layer flows

## Topology Overview

| Layer | Responsibility |
|:------|:---------------|
| CLI | user commands, model/preset/status operations |
| Server | request routing, API handling, streaming |
| Shared | config utilities, preset support, constants |
| `@musistudio/llms` | provider adaptation and transformation |

## Source References

- [Project CLAUDE.md](https://github.com/musistudio/claude-code-router/blob/main/CLAUDE.md)
- [Server Intro](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/intro.md)

## Summary

You now have a system-level map for CCR operations.

Next: [Chapter 3: Provider Configuration and Transformer Strategy](03-provider-configuration-and-transformer-strategy.md)
