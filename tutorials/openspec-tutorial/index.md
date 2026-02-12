---
layout: default
title: "OpenSpec Tutorial"
nav_order: 181
has_children: true
format_version: v2
---

# OpenSpec Tutorial: Spec-Driven Workflows for AI Coding Agents

> Learn how to use `Fission-AI/OpenSpec` to make AI-assisted software delivery more predictable with artifact-driven planning, implementation, and archival workflows.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Fission--AI%2FOpenSpec-black?logo=github)](https://github.com/Fission-AI/OpenSpec)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Fission-AI/OpenSpec/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-OpenSpec-blue)](https://github.com/Fission-AI/OpenSpec/tree/main/docs)
[![Latest Release](https://img.shields.io/github/v/release/Fission-AI/OpenSpec)](https://github.com/Fission-AI/OpenSpec/releases)

## Why This Track Matters

OpenSpec adds a strong specification layer on top of coding agents, reducing ambiguity between intent, design, and implementation.

This track focuses on:

- using OPSX commands to move from idea to implemented change
- managing proposal/spec/design/tasks artifacts as a connected graph
- customizing schemas and rules for team-specific standards
- operating validation, migration, and governance in real repositories

## Current Snapshot (Verified February 12, 2026)

- repository: [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec)
- stars: about **23.8k**
- latest release: [`v1.1.1`](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.1.1) (**January 30, 2026**)
- recent activity: updated on **February 12, 2026**
- positioning: tool-agnostic spec workflow system spanning 20+ coding assistants

## Mental Model

```mermaid
flowchart LR
    A[Idea] --> B[/opsx:new]
    B --> C[proposal, specs, design, tasks]
    C --> D[/opsx:apply]
    D --> E[/opsx:verify]
    E --> F[/opsx:archive]
    F --> G[Updated source-of-truth specs]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started and OPSX Basics](01-getting-started-and-opsx-basics.md) | How do I install and initialize OpenSpec safely? | Clean project bootstrap |
| [02 - Artifact Graph and Change Lifecycle](02-artifact-graph-and-change-lifecycle.md) | How do specs and change artifacts interact over time? | Strong lifecycle model |
| [03 - Command Surface and Agent Workflows](03-command-surface-and-agent-workflows.md) | Which commands belong to humans vs agents? | Better execution discipline |
| [04 - Spec Authoring, Delta Patterns, and Quality](04-spec-authoring-delta-patterns-and-quality.md) | How do you write robust ADDED/MODIFIED/REMOVED specs? | Higher artifact quality |
| [05 - Customization, Schemas, and Project Rules](05-customization-schemas-and-project-rules.md) | How do teams adapt OpenSpec to their delivery model? | Tailored workflows |
| [06 - Tool Integrations and Multi-Agent Portability](06-tool-integrations-and-multi-agent-portability.md) | How does OpenSpec span many coding assistants? | Cross-tool consistency |
| [07 - Validation, Automation, and CI Operations](07-validation-automation-and-ci-operations.md) | How do we enforce quality gates continuously? | Repeatable validation |
| [08 - Migration, Governance, and Team Adoption](08-migration-governance-and-team-adoption.md) | How do teams migrate and scale OpenSpec usage safely? | Sustainable adoption plan |

## What You Will Learn

- how to run an end-to-end spec-driven workflow with coding agents
- how to separate planning artifacts from implementation execution
- how to customize OpenSpec behavior with config and schema controls
- how to enforce validation and governance as part of CI/CD

## Source References

- [OpenSpec Repository](https://github.com/Fission-AI/OpenSpec)
- [README](https://github.com/Fission-AI/OpenSpec/blob/main/README.md)
- [Getting Started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)
- [Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)
- [Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)
- [Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [CLI Reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)
- [Migration Guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/migration-guide.md)
- [Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)

## Related Tutorials

- [Claude Task Master Tutorial](../claude-task-master-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [Codex CLI Tutorial](../codex-cli-tutorial/)
- [Continue Tutorial](../continue-tutorial/)

---

Start with [Chapter 1: Getting Started and OPSX Basics](01-getting-started-and-opsx-basics.md).
