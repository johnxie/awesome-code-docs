---
layout: default
title: "Compound Engineering Plugin Tutorial"
nav_order: 146
has_children: true
format_version: v2
---

# Compound Engineering Plugin Tutorial: Compounding Agent Workflows Across Toolchains

> Learn how to use `EveryInc/compound-engineering-plugin` to run compound engineering workflows in Claude Code and convert plugin assets for other coding-agent ecosystems.

[![GitHub Repo](https://img.shields.io/badge/GitHub-EveryInc%2Fcompound--engineering--plugin-black?logo=github)](https://github.com/EveryInc/compound-engineering-plugin)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/EveryInc/compound-engineering-plugin/blob/main/LICENSE)
[![NPM Registry](https://img.shields.io/badge/npm-@every--env%2Fcompound--plugin-red)](https://registry.npmjs.org/%40every-env%2Fcompound-plugin)

## Why This Track Matters

Compound Engineering Plugin combines workflow discipline, reusable agent assets, and cross-toolchain conversion support for teams running mixed coding-agent environments.

This track focuses on:

- installing and operating the core `compound-engineering` plugin
- understanding how workflows, agents, commands, and skills compound over time
- using conversion/sync tooling for OpenCode, Codex, and Droid targets
- applying quality and governance controls to compound engineering loops

## Current Snapshot (Verified February 12, 2026)

- repository: [`EveryInc/compound-engineering-plugin`](https://github.com/EveryInc/compound-engineering-plugin)
- stars: about **8.5k**
- latest release: [`v0.4.0`](https://github.com/EveryInc/compound-engineering-plugin/releases/tag/v0.4.0)
- recent activity: updates on **February 11, 2026**
- project positioning: Claude Code marketplace with compound-engineering workflow system and cross-provider conversion CLI

## Mental Model

```mermaid
flowchart LR
    A[Feature idea] --> B[Plan workflow]
    B --> C[Work execution]
    C --> D[Multi-agent review]
    D --> E[Compound learnings]
    E --> F[Future cycles become faster]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I install and run the core plugin quickly? | Working baseline |
| [02 - Compound Engineering Philosophy and Workflow Loop](02-compound-engineering-philosophy-and-workflow-loop.md) | How does plan/work/review/compound create leverage? | Strong workflow model |
| [03 - Architecture of Agents, Commands, and Skills](03-architecture-of-agents-commands-and-skills.md) | How are components organized and selected? | Better capability mapping |
| [04 - Multi-Provider Conversion and Config Sync](04-multi-provider-conversion-and-config-sync.md) | How do I target OpenCode, Codex, and Droid from same source? | Cross-toolchain portability |
| [05 - MCP Integrations and Browser Automation](05-mcp-integrations-and-browser-automation.md) | How do Context7/Playwright integrations fit into workflows? | Strong integration strategy |
| [06 - Daily Operations and Quality Gates](06-daily-operations-and-quality-gates.md) | How do teams run compound workflows consistently? | Operational reliability |
| [07 - Troubleshooting and Runtime Maintenance](07-troubleshooting-and-runtime-maintenance.md) | How do I recover from plugin/runtime failures quickly? | Faster recovery loops |
| [08 - Contribution Workflow and Versioning Discipline](08-contribution-workflow-and-versioning-discipline.md) | How do contributors evolve the plugin safely? | Contributor readiness |

## What You Will Learn

- how to operationalize compound engineering principles in real coding loops
- how to exploit reusable agents/commands/skills for quality and speed
- how to synchronize capabilities across Claude Code and other agent platforms
- how to govern plugin evolution with versioning and validation discipline

## Source References

- [Repository README](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md)
- [Compound Engineering Plugin README](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md)
- [Marketplace Catalog](https://github.com/EveryInc/compound-engineering-plugin/blob/main/.claude-plugin/marketplace.json)
- [Claude Code Spec Notes](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/specs/claude-code.md)
- [Codex Spec Notes](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/specs/codex.md)
- [OpenCode Spec Notes](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/specs/opencode.md)

## Related Tutorials

- [Codex CLI Tutorial](../codex-cli-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [Wshobson Agents Tutorial](../wshobson-agents-tutorial/)

---

Start with [Chapter 1: Getting Started](01-getting-started.md).
