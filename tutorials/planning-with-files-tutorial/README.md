---
layout: default
title: "Planning with Files Tutorial"
nav_order: 148
has_children: true
format_version: v2
---

# Planning with Files Tutorial: Persistent Markdown Workflow Memory for AI Coding Agents

> Learn how to use `OthmanAdi/planning-with-files` to run Manus-style file-based planning workflows across Claude Code and other AI coding environments.

[![GitHub Repo](https://img.shields.io/badge/GitHub-OthmanAdi%2Fplanning--with--files-black?logo=github)](https://github.com/OthmanAdi/planning-with-files)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/OthmanAdi/planning-with-files/blob/master/LICENSE)
[![Release](https://img.shields.io/badge/release-v2.15.0-green)](https://github.com/OthmanAdi/planning-with-files/releases/tag/v2.15.0)

## Why This Track Matters

`planning-with-files` is one of the fastest-growing workflow skills for coding agents and provides a concrete system for durable planning beyond volatile context windows.

This track focuses on:

- setting up the skill quickly in Claude Code
- applying the 3-file planning pattern consistently
- using hooks, templates, and scripts for reliability
- adapting the workflow across multiple IDE/agent runtimes

## Current Snapshot (auto-updated)

- repository: [`OthmanAdi/planning-with-files`](https://github.com/OthmanAdi/planning-with-files)
- stars: about **13.7k**
- latest release: [`v2.15.0`](https://github.com/OthmanAdi/planning-with-files/releases/tag/v2.15.0)
- recent activity: updates on **February 9, 2026**
- project positioning: cross-IDE planning skill emphasizing persistent file-based workflow memory

## Mental Model

```mermaid
flowchart LR
    A[Task request] --> B[task_plan.md]
    B --> C[findings.md]
    C --> D[progress.md]
    D --> E[Hook-driven reminders]
    E --> F[Completion checks and recovery]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I install and launch the workflow quickly? | Working baseline |
| [02 - Core Philosophy and the 3-File Pattern](02-core-philosophy-and-the-3-file-pattern.md) | Why does filesystem memory improve agent reliability? | Strong mental model |
| [03 - Installation Paths Across IDEs and Agents](03-installation-paths-across-ides-and-agents.md) | How do setup paths vary across toolchains? | Better portability |
| [04 - Commands, Hooks, and Workflow Orchestration](04-commands-hooks-and-workflow-orchestration.md) | How do commands and hooks enforce discipline? | Higher consistency |
| [05 - Templates, Scripts, and Session Recovery](05-templates-scripts-and-session-recovery.md) | How do I recover state and keep momentum after context resets? | Better resilience |
| [06 - Multi-IDE Adaptation (Codex, Gemini, OpenCode, Cursor)](06-multi-ide-adaptation-codex-gemini-opencode-cursor.md) | How do I reuse the same planning system across platforms? | Cross-platform fluency |
| [07 - Troubleshooting, Anti-Patterns, and Safety Checks](07-troubleshooting-anti-patterns-and-safety-checks.md) | How do I avoid failure loops and workflow drift? | Reliability playbook |
| [08 - Contribution Workflow and Team Adoption](08-contribution-workflow-and-team-adoption.md) | How do teams standardize and evolve this pattern? | Adoption readiness |

## What You Will Learn

- how to make agent workflows durable with persistent markdown memory
- how to run and recover complex tasks with less context loss
- how to port the planning system across major AI coding IDEs
- how to govern and extend the workflow in team settings

## Source References

- [Planning with Files Repository](https://github.com/OthmanAdi/planning-with-files)
- [README](https://github.com/OthmanAdi/planning-with-files/blob/master/README.md)
- [Installation Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/installation.md)
- [Workflow Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/workflow.md)
- [Troubleshooting Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/troubleshooting.md)

## Related Tutorials

- [Beads Tutorial](../beads-tutorial/)
- [Mini-SWE-Agent Tutorial](../mini-swe-agent-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
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
2. [Chapter 2: Core Philosophy and the 3-File Pattern](02-core-philosophy-and-the-3-file-pattern.md)
3. [Chapter 3: Installation Paths Across IDEs and Agents](03-installation-paths-across-ides-and-agents.md)
4. [Chapter 4: Commands, Hooks, and Workflow Orchestration](04-commands-hooks-and-workflow-orchestration.md)
5. [Chapter 5: Templates, Scripts, and Session Recovery](05-templates-scripts-and-session-recovery.md)
6. [Chapter 6: Multi-IDE Adaptation (Codex, Gemini, OpenCode, Cursor)](06-multi-ide-adaptation-codex-gemini-opencode-cursor.md)
7. [Chapter 7: Troubleshooting, Anti-Patterns, and Safety Checks](07-troubleshooting-anti-patterns-and-safety-checks.md)
8. [Chapter 8: Contribution Workflow and Team Adoption](08-contribution-workflow-and-team-adoption.md)

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
