---
layout: default
title: "Claude Flow Tutorial"
nav_order: 160
has_children: true
format_version: v2
---

# Claude Flow Tutorial: Multi-Agent Orchestration, MCP Tooling, and V3 Module Architecture

> Learn how to use `ruvnet/claude-flow` to orchestrate multi-agent workflows, operate MCP/CLI surfaces, and reason about V2-to-V3 architecture and migration tradeoffs.

[![GitHub Repo](https://img.shields.io/badge/GitHub-ruvnet%2Fclaude--flow-black?logo=github)](https://github.com/ruvnet/claude-flow)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ruvnet/claude-flow/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/ruvnet/claude-flow)](https://github.com/ruvnet/claude-flow/releases)

## Why This Track Matters

Claude Flow is a prominent open-source orchestration stack in the coding-agent ecosystem, with broad MCP and multi-agent framing plus active V3 modularization efforts.

This track focuses on:

- understanding core orchestration surfaces across CLI, MCP, and swarm patterns
- mapping V3 module architecture and ADR-driven decisions
- operating memory, security, and performance subsystems with pragmatic expectations
- evaluating migration gaps between V2 and V3 before production rollout

## Current Snapshot (Verified February 12, 2026)

- repository: [`ruvnet/claude-flow`](https://github.com/ruvnet/claude-flow)
- stars: about **14.0k**
- latest release: [`v2.7.1-agentic-flow-1.7.4`](https://github.com/ruvnet/claude-flow/releases/tag/v2.7.1-agentic-flow-1.7.4) (**October 24, 2025**)
- license: MIT
- recent activity: updates on **February 12, 2026**
- project positioning: orchestration layer for Claude-centered multi-agent workflows with V3 modular package split

## Mental Model

```mermaid
flowchart LR
    A[Task request] --> B[CLI or MCP entry]
    B --> C[Routing and swarm coordination]
    C --> D[Agent execution memory and plugins]
    D --> E[Security and performance controls]
    E --> F[Testing migration and operations]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I get Claude Flow running quickly and safely? | First-run baseline |
| [02 - V3 Architecture and ADRs](02-v3-architecture-and-adrs.md) | What changed in V3 and why? | Clear architecture model |
| [03 - Swarm Coordination and Consensus Patterns](03-swarm-coordination-and-consensus-patterns.md) | How do agent teams coordinate work reliably? | Better orchestration decisions |
| [04 - Memory, Learning, and Intelligence Systems](04-memory-learning-and-intelligence-systems.md) | How do memory and learning layers shape behavior? | Stronger memory strategy |
| [05 - MCP Server, CLI, and Runtime Operations](05-mcp-server-cli-and-runtime-operations.md) | How should MCP and CLI surfaces be operated? | More predictable tooling usage |
| [06 - Plugin SDK and Extensibility Patterns](06-plugin-sdk-and-extensibility-patterns.md) | How do I add capabilities without breaking core flows? | Safer extension workflow |
| [07 - Testing, Migration, and Upgrade Strategy](07-testing-migration-and-upgrade-strategy.md) | How do I validate changes across V2/V3 realities? | Lower regression risk |
| [08 - Production Governance, Security, and Performance](08-production-governance-security-and-performance.md) | How do teams operationalize Claude Flow with guardrails? | Long-term operations playbook |

## What You Will Learn

- how to reason about Claude Flow as an orchestration ledger versus execution engine
- how V3 modules map to swarm, MCP, memory, security, and performance concerns
- how to apply extension, testing, and migration practices pragmatically
- how to set production controls around security and runtime performance

## Source References

- [Claude Flow Repository](https://github.com/ruvnet/claude-flow)
- [README](https://github.com/ruvnet/claude-flow/blob/main/README.md)
- [V3 README](https://github.com/ruvnet/claude-flow/blob/main/v3/README.md)
- [V2 README](https://github.com/ruvnet/claude-flow/blob/main/v2/README.md)
- [AGENTS Guide](https://github.com/ruvnet/claude-flow/blob/main/AGENTS.md)
- [V3 ADR Index](https://github.com/ruvnet/claude-flow/blob/main/v3/docs/adr/README.md)
- [@claude-flow/swarm](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/swarm/README.md)
- [@claude-flow/mcp](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/mcp/README.md)
- [@claude-flow/memory](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/memory/README.md)
- [@claude-flow/security](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/security/README.md)
- [@claude-flow/plugins](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/plugins/README.md)
- [@claude-flow/testing](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/testing/README.md)
- [V3 Migration Docs](https://github.com/ruvnet/claude-flow/blob/main/v3/implementation/v3-migration/README.md)

## Related Tutorials

- [Claude Code Tutorial](../claude-code-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [Daytona Tutorial](../daytona-tutorial/)
- [MCP Python SDK Tutorial](../mcp-python-sdk-tutorial/)

---

Start with [Chapter 1: Getting Started](01-getting-started.md).
