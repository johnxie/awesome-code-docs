---
layout: default
title: "Chapter 2: Architecture and Package Topology"
nav_order: 2
parent: Claude Code Router Tutorial
---

# Chapter 2: Architecture and Package Topology

This chapter maps CCR's monorepo structure and runtime boundaries.

## Learning Goals

- understand responsibilities of CLI, server, and shared packages
- trace request flow across router and transformer layers
- identify extension points for custom routing/transformers
- reduce confusion when debugging multi-layer behavior

## Core Package Roles

| Package | Responsibility |
|:--------|:---------------|
| CLI | command orchestration, model/preset/status workflows |
| Server | request routing, API handling, stream processing |
| Shared | common config, constants, preset utilities |
| external `@musistudio/llms` | provider transformation framework |

## Source References

- [CLAUDE.md Architecture Notes](https://github.com/musistudio/claude-code-router/blob/main/CLAUDE.md)
- [Server Intro](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/intro.md)

## Summary

You now have a clear component model for reasoning about CCR behavior.

Next: [Chapter 3: Provider Configuration and Transformer Strategy](03-provider-configuration-and-transformer-strategy.md)
