---
layout: default
title: "Wshobson Agents Tutorial"
nav_order: 142
has_children: true
format_version: v2
---

# Wshobson Agents Tutorial: Pluginized Multi-Agent Workflows for Claude Code

> Learn how to use `wshobson/agents` to install focused Claude Code plugins, coordinate specialist agents, and run scalable multi-agent workflows with clear model and skill boundaries.

[![GitHub Repo](https://img.shields.io/badge/GitHub-wshobson%2Fagents-black?logo=github)](https://github.com/wshobson/agents)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wshobson/agents/blob/main/LICENSE)
[![Marketplace](https://img.shields.io/badge/marketplace-.claude--plugin-blue)](https://github.com/wshobson/agents/tree/main/.claude-plugin)

## Why This Track Matters

`wshobson/agents` is one of the largest pluginized Claude Code ecosystems and a practical reference for composable agent operations at scale.

This track focuses on:

- installing only the plugins you need for token-efficient operation
- understanding how plugins, agents, commands, and skills interact
- using command workflows and natural-language orchestration together
- extending the ecosystem with maintainable plugin authoring practices

## Current Snapshot (auto-updated)

- repository: [`wshobson/agents`](https://github.com/wshobson/agents)
- stars: about **28.4k**
- latest release: **none tagged** (rolling `main`)
- recent push activity: **February 7, 2026**
- project positioning: large Claude Code plugin marketplace for multi-agent automation

## Mental Model

```mermaid
flowchart LR
    A[Install plugin] --> B[Load focused agents and commands]
    B --> C[Optional skill activation]
    C --> D[Slash command or NL invocation]
    D --> E[Multi-agent orchestration]
    E --> F[Iterative output and review]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I start with the marketplace and first plugins? | Working baseline |
| [02 - Marketplace Architecture and Plugin Structure](02-marketplace-architecture-and-plugin-structure.md) | How is the repo organized for composability? | Strong architecture model |
| [03 - Installation and Plugin Selection Strategy](03-installation-and-plugin-selection-strategy.md) | How do I choose plugin sets without context bloat? | Better plugin portfolio |
| [04 - Commands, Natural Language, and Workflow Orchestration](04-commands-natural-language-and-workflow-orchestration.md) | When should I use slash commands vs NL prompts? | Higher operator throughput |
| [05 - Agents, Skills, and Model Tier Strategy](05-agents-skills-and-model-tier-strategy.md) | How do specialists, skills, and model tiers fit together? | Better quality/cost control |
| [06 - Multi-Agent Team Patterns and Production Workflows](06-multi-agent-team-patterns-and-production-workflows.md) | How do I run complex team workflows safely? | Operational confidence |
| [07 - Governance, Safety, and Operational Best Practices](07-governance-safety-and-operational-best-practices.md) | How do teams keep usage secure and maintainable? | Governance baseline |
| [08 - Contribution Workflow and Plugin Authoring Patterns](08-contribution-workflow-and-plugin-authoring-patterns.md) | How do I contribute high-quality plugins and docs? | Contributor readiness |

## What You Will Learn

- how to operationalize pluginized agent systems at scale
- how to manage command-driven and NL-driven flows together
- how to tune capability/cost through selective plugin + model strategy
- how to contribute cleanly to a fast-moving multi-plugin ecosystem

## Source References

- [Repository README](https://github.com/wshobson/agents/blob/main/README.md)
- [Plugin Reference](https://github.com/wshobson/agents/blob/main/docs/plugins.md)
- [Usage Guide](https://github.com/wshobson/agents/blob/main/docs/usage.md)
- [Agent Reference](https://github.com/wshobson/agents/blob/main/docs/agents.md)
- [Agent Skills](https://github.com/wshobson/agents/blob/main/docs/agent-skills.md)
- [Architecture Guide](https://github.com/wshobson/agents/blob/main/docs/architecture.md)

## Related Tutorials

- [Claude Code Tutorial](../claude-code-tutorial/)
- [AGENTS.md Tutorial](../agents-md-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [Codex CLI Tutorial](../codex-cli-tutorial/)

---

Start with [Chapter 1: Getting Started](01-getting-started.md).

## Navigation & Backlinks

- [Start Here: Chapter 1: Getting Started](01-getting-started.md)
- [Back to Main Catalog](../../README.md#-tutorial-catalog)
- [Browse A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
- [Search by Intent](../../discoverability/query-hub.md)
- [Explore Category Hubs](../../README.md#category-hubs)

## Full Chapter Map

1. [Chapter 1: Getting Started](01-getting-started.md)
2. [Chapter 2: Marketplace Architecture and Plugin Structure](02-marketplace-architecture-and-plugin-structure.md)
3. [Chapter 3: Installation and Plugin Selection Strategy](03-installation-and-plugin-selection-strategy.md)
4. [Chapter 4: Commands, Natural Language, and Workflow Orchestration](04-commands-natural-language-and-workflow-orchestration.md)
5. [Chapter 5: Agents, Skills, and Model Tier Strategy](05-agents-skills-and-model-tier-strategy.md)
6. [Chapter 6: Multi-Agent Team Patterns and Production Workflows](06-multi-agent-team-patterns-and-production-workflows.md)
7. [Chapter 7: Governance, Safety, and Operational Best Practices](07-governance-safety-and-operational-best-practices.md)
8. [Chapter 8: Contribution Workflow and Plugin Authoring Patterns](08-contribution-workflow-and-plugin-authoring-patterns.md)

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
