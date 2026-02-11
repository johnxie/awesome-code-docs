---
layout: default
title: "HumanLayer Tutorial"
nav_order: 105
has_children: true
format_version: v2
---

# HumanLayer Tutorial: Context Engineering and Human-Governed Coding Agents

> Learn how to use `humanlayer/humanlayer` patterns to orchestrate coding agents with stronger context control, human oversight, and team-scale workflows.

[![GitHub Repo](https://img.shields.io/badge/GitHub-humanlayer%2Fhumanlayer-black?logo=github)](https://github.com/humanlayer/humanlayer)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/humanlayer/humanlayer/blob/main/LICENSE)
[![Site](https://img.shields.io/badge/site-humanlayer.dev-blue)](https://humanlayer.dev/code)

## Why This Track Matters

As coding agents move into high-stakes production tasks, context discipline and human governance become essential. HumanLayer emphasizes battle-tested workflows for difficult codebases and multi-agent execution.

This track focuses on:

- context-engineering patterns for large repositories
- multi-agent orchestration and parallel execution
- deterministic human approval for high-stakes operations
- team adoption and production governance

## Current Snapshot (Verified February 11, 2026)

- repository: [`humanlayer/humanlayer`](https://github.com/humanlayer/humanlayer)
- stars: about **9.3k**
- latest release: [`pro-0.20.0`](https://github.com/humanlayer/humanlayer/releases/tag/pro-0.20.0)
- development activity: active with recent updates
- project positioning: open-source coding-agent orchestration stack with context and human-loop emphasis

## Mental Model

```mermaid
flowchart LR
    A[Complex Task] --> B[Context Engineering]
    B --> C[Agent Orchestration]
    C --> D[Human Approval Gates]
    D --> E[Execution and Review]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I approach HumanLayer's current stack and workflows? | Practical onboarding baseline |
| [02 - Architecture and Monorepo Layout](02-architecture-and-monorepo-layout.md) | How is the project structured for orchestration workflows? | Better navigation and extension speed |
| [03 - Context Engineering Workflows](03-context-engineering-workflows.md) | How do I shape context for hard coding tasks? | Higher success on complex repos |
| [04 - Parallel Agent Orchestration](04-parallel-agent-orchestration.md) | How do multi-session workflows improve throughput? | Safer parallel execution model |
| [05 - Human Approval and High-Stakes Actions](05-human-approval-and-high-stakes-actions.md) | How do I gate risky operations deterministically? | Governance controls for high-impact actions |
| [06 - IDE and CLI Integration Patterns](06-ide-and-cli-integration-patterns.md) | How do teams use these workflows in real development loops? | Integration playbook |
| [07 - Telemetry, Cost, and Team Governance](07-telemetry-cost-and-team-governance.md) | How do I monitor quality/cost and prevent drift? | Sustainable operations model |
| [08 - Production Rollout and Adoption](08-production-rollout-and-adoption.md) | How do I scale HumanLayer-style workflows organization-wide? | Adoption and rollout strategy |

## What You Will Learn

- how to structure context for coding agents in large codebases
- how to orchestrate parallel agent workflows with human controls
- how to apply deterministic oversight to high-stakes operations
- how to scale coding-agent practices across teams and environments

## Source References

- [HumanLayer Repository](https://github.com/humanlayer/humanlayer)
- [HumanLayer Releases](https://github.com/humanlayer/humanlayer/releases)
- [HumanLayer README](https://github.com/humanlayer/humanlayer/blob/main/README.md)
- [Legacy HumanLayer SDK Docs](https://github.com/humanlayer/humanlayer/blob/main/humanlayer.md)

## Related Tutorials

- [OpenCode Tutorial](../opencode-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Aider Tutorial](../aider-tutorial/)

---

Start with [Chapter 1: Getting Started](01-getting-started.md).
