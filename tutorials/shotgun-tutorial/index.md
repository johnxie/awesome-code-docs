---
layout: default
title: "Shotgun Tutorial"
nav_order: 110
has_children: true
format_version: v2
---

# Shotgun Tutorial: Spec-Driven Development for Coding Agents

> Learn how to use `shotgun-sh/shotgun` to plan, specify, and execute large code changes with structured agent workflows and stronger delivery control.

[![GitHub Repo](https://img.shields.io/badge/GitHub-shotgun--sh%2Fshotgun-black?logo=github)](https://github.com/shotgun-sh/shotgun)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/shotgun-sh/shotgun/blob/main/LICENSE)
[![Website](https://img.shields.io/badge/site-shotgun.sh-blue)](https://shotgun.sh/)

## Why This Track Matters

When coding agents work on larger features, they often drift from architecture and produce hard-to-review output. Shotgun uses a structured flow to keep planning, scoping, and execution aligned with your codebase.

This track focuses on:

- router-driven multi-agent lifecycle (research to export)
- planning and drafting execution modes
- codebase indexing, context retrieval, and operations
- production concerns across CI, observability, and security

## Current Snapshot (Verified February 12, 2026)

- repository: [`shotgun-sh/shotgun`](https://github.com/shotgun-sh/shotgun)
- stars: about **585**
- latest release: [`0.9.0`](https://github.com/shotgun-sh/shotgun/releases/tag/0.9.0)
- recent activity: updates on **February 11, 2026**
- project positioning: spec-driven development system for AI coding agents

## Mental Model

```mermaid
flowchart LR
    A[Prompt] --> B[Router]
    B --> C[Research]
    C --> D[Specify]
    D --> E[Plan]
    E --> F[Tasks]
    F --> G[Export]
    G --> H[Agent Execution]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I install and run Shotgun quickly? | Working local baseline |
| [02 - Router Architecture and Agent Lifecycle](02-router-architecture-and-agent-lifecycle.md) | How does Shotgun break work into specialized agents? | Clear orchestration model |
| [03 - Planning vs Drafting Execution Modes](03-planning-vs-drafting-execution-modes.md) | When should I use checkpoints versus full-speed runs? | Better control and throughput |
| [04 - Codebase Indexing and Context Retrieval](04-codebase-indexing-and-context-retrieval.md) | How does Shotgun build code awareness before writing changes? | Stronger context quality |
| [05 - CLI Automation and Scripting](05-cli-automation-and-scripting.md) | How do I run Shotgun in scripts and CI flows? | Repeatable automation patterns |
| [06 - Context7 MCP and Local Models](06-context7-mcp-and-local-models.md) | How do docs lookup and local model support work? | Practical integration strategy |
| [07 - Spec Sharing and Collaboration Workflows](07-spec-sharing-and-collaboration-workflows.md) | How do teams share and iterate specs safely? | Better collaboration lifecycle |
| [08 - Production Operations, Observability, and Security](08-production-operations-observability-and-security.md) | How do I run Shotgun in production environments? | Ops and governance baseline |

## What You Will Learn

- how to structure large coding-agent tasks into staged execution
- how to use router modes for safer implementation flow
- how to automate Shotgun in CI and team workflows
- how to harden operations with telemetry, secrets hygiene, and deployment controls

## Source References

- [Shotgun Repository](https://github.com/shotgun-sh/shotgun)
- [Shotgun CLI Docs](https://github.com/shotgun-sh/shotgun/blob/main/docs/CLI.md)
- [Context7 Integration Architecture](https://github.com/shotgun-sh/shotgun/blob/main/docs/architecture/context7-mcp-integration.md)
- [Ollama/Local Models Architecture](https://github.com/shotgun-sh/shotgun/blob/main/docs/architecture/ollama-local-models.md)
- [CI/CD Docs](https://github.com/shotgun-sh/shotgun/blob/main/docs/CI_CD.md)

## Related Tutorials

- [OpenCode Tutorial](../opencode-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [Plandex Tutorial](../plandex-tutorial/)
- [HumanLayer Tutorial](../humanlayer-tutorial/)

---

Start with [Chapter 1: Getting Started](01-getting-started.md).
