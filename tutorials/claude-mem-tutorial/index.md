---
layout: default
title: "Claude-Mem Tutorial"
nav_order: 144
has_children: true
format_version: v2
---

# Claude-Mem Tutorial: Persistent Memory Compression for Claude Code

> Learn how to use `thedotmack/claude-mem` to capture, compress, and retrieve coding-session memory with hook-driven automation, searchable context layers, and operator controls.

[![GitHub Repo](https://img.shields.io/badge/GitHub-thedotmack%2Fclaude--mem-black?logo=github)](https://github.com/thedotmack/claude-mem)
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](https://github.com/thedotmack/claude-mem/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-docs.claude--mem.ai-blue)](https://docs.claude-mem.ai/)

## Why This Track Matters

Claude-Mem is one of the most widely adopted memory plugins for Claude Code and addresses a common pain point in agentic workflows: loss of durable project context across sessions.

This track focuses on:

- setting up Claude-Mem reliably with plugin marketplace workflows
- understanding hooks, worker service, and database architecture
- using search tools with token-efficient progressive disclosure
- operating and troubleshooting memory systems in production-like environments

## Current Snapshot (Verified February 12, 2026)

- repository: [`thedotmack/claude-mem`](https://github.com/thedotmack/claude-mem)
- stars: about **27.4k**
- latest release: [`v10.0.4`](https://github.com/thedotmack/claude-mem/releases/tag/v10.0.4)
- recent activity: updates on **February 12, 2026**
- project positioning: persistent context and memory compression plugin for Claude Code

## Mental Model

```mermaid
flowchart LR
    A[Claude Code session] --> B[Lifecycle hooks]
    B --> C[Worker service + queue]
    C --> D[SQLite and vector search storage]
    D --> E[Progressive-disclosure retrieval]
    E --> F[Context injection into new sessions]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I install and verify Claude-Mem quickly? | Working baseline |
| [02 - Architecture, Hooks, and Worker Flow](02-architecture-hooks-and-worker-flow.md) | How does data move from hooks to searchable memory? | Strong architecture model |
| [03 - Installation, Upgrade, and Runtime Environment](03-installation-upgrade-and-runtime-environment.md) | How do I keep installs and upgrades stable? | Better deployment reliability |
| [04 - Configuration, Modes, and Context Injection](04-configuration-modes-and-context-injection.md) | How do I tune memory behavior safely? | Predictable context behavior |
| [05 - Search Tools and Progressive Disclosure](05-search-tools-and-progressive-disclosure.md) | How do I query memory with strong token discipline? | Better retrieval efficiency |
| [06 - Viewer Operations and Maintenance Workflows](06-viewer-operations-and-maintenance-workflows.md) | How do I run daily operations and maintenance? | Operational confidence |
| [07 - Troubleshooting, Recovery, and Reliability](07-troubleshooting-recovery-and-reliability.md) | How do I recover from failures and data issues quickly? | Incident-response playbook |
| [08 - Contribution Workflow and Governance](08-contribution-workflow-and-governance.md) | How do I contribute safely to memory infrastructure? | Contributor readiness |

## What You Will Learn

- how Claude-Mem preserves context with minimal manual effort
- how to control memory capture and injection behavior safely
- how to query memory with multi-layer, token-efficient search patterns
- how to operate and contribute to Claude-Mem with production discipline

## Source References

- [Claude-Mem Repository](https://github.com/thedotmack/claude-mem)
- [Claude-Mem README](https://github.com/thedotmack/claude-mem/blob/main/README.md)
- [Official Documentation](https://docs.claude-mem.ai/)
- [Configuration Guide](https://docs.claude-mem.ai/configuration)
- [Troubleshooting Guide](https://docs.claude-mem.ai/troubleshooting)

## Related Tutorials

- [Claude Code Tutorial](../claude-code-tutorial/)
- [Agents.md Tutorial](../agents-md-tutorial/)
- [Beads Tutorial](../beads-tutorial/)
- [Context7 Tutorial](../context7-tutorial/)

---

Start with [Chapter 1: Getting Started](01-getting-started.md).
