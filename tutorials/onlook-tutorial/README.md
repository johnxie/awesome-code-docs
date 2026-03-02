---
layout: default
title: "Onlook Tutorial"
nav_order: 124
has_children: true
format_version: v2
---

# Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind

> Learn how to use `onlook-dev/onlook` to design and edit production-grade React apps visually while keeping generated code in your repository.

[![GitHub Repo](https://img.shields.io/badge/GitHub-onlook--dev%2Fonlook-black?logo=github)](https://github.com/onlook-dev/onlook)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/onlook-dev/onlook/blob/main/LICENSE.md)
[![Docs](https://img.shields.io/badge/docs-docs.onlook.com-blue)](https://docs.onlook.com)

## Why This Track Matters

Onlook is a leading open-source visual-first coding environment that combines AI chat, live DOM editing, and direct code updates for Next.js + Tailwind projects.

This track focuses on:

- starting projects in hosted or local Onlook environments
- understanding visual edit -> code writeback architecture
- using AI/chat workflows while preserving code ownership
- contributing to and operating Onlook in team contexts

## Current Snapshot (auto-updated)

- repository: [`onlook-dev/onlook`](https://github.com/onlook-dev/onlook)
- stars: about **24.7k**
- latest release: [`v0.2.32`](https://github.com/onlook-dev/onlook/releases/tag/v0.2.32)
- recent activity: updates on **January 21, 2026**
- project positioning: open-source visual-first code editor for React/Next.js workflows

## Mental Model

```mermaid
flowchart LR
    A[Prompt or Visual Edit] --> B[Onlook Editor]
    B --> C[Live App Preview iFrame]
    C --> D[Element-to-Code Mapping]
    D --> E[AST/Code Writeback]
    E --> F[Versioned Changes in Repo]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I start using Onlook quickly? | Working baseline |
| [02 - Product and Architecture Foundations](02-product-and-architecture-foundations.md) | How does Onlook connect visual editing to real code? | Strong architecture understanding |
| [03 - Visual Editing and Code Mapping](03-visual-editing-and-code-mapping.md) | How are visual changes translated into source code? | Better editing confidence |
| [04 - AI Chat, Branching, and Iteration](04-ai-chat-branching-and-iteration.md) | How should I run prompt-driven workflows safely? | Reliable iteration flow |
| [05 - Local Development and Runtime Setup](05-local-development-and-runtime-setup.md) | How do I run and debug Onlook locally? | Contributor baseline setup |
| [06 - Deployment and Team Collaboration](06-deployment-and-team-collaboration.md) | How do teams ship and share projects built in Onlook? | Delivery workflow model |
| [07 - Contributing and Quality Workflow](07-contributing-and-quality-workflow.md) | How do I contribute safely to Onlook itself? | OSS contribution readiness |
| [08 - Production Operations and Governance](08-production-operations-and-governance.md) | How do organizations adopt Onlook responsibly? | Adoption and governance runbook |

## What You Will Learn

- how to use Onlook as a visual coding interface without code lock-in
- how visual interactions are mapped and written back to source code
- how to run local development and contribute to the project
- how to adopt Onlook with reliable team workflows and controls

## Source References

- [Onlook Repository](https://github.com/onlook-dev/onlook)
- [Onlook README](https://github.com/onlook-dev/onlook/blob/main/README.md)
- [Onlook Docs](https://docs.onlook.com)
- [Onlook Architecture Docs](https://docs.onlook.com/developers/architecture)
- [Onlook Running Locally](https://docs.onlook.com/developers/running-locally)
- [Onlook Developer Docs](https://docs.onlook.com/developers)

## Related Tutorials

- [Dyad Tutorial](../dyad-tutorial/)
- [Bolt.diy Tutorial](../bolt-diy-tutorial/)
- [Vercel AI Tutorial](../vercel-ai-tutorial/)
- [Serena Tutorial](../serena-tutorial/)

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
2. [Chapter 2: Product and Architecture Foundations](02-product-and-architecture-foundations.md)
3. [Chapter 3: Visual Editing and Code Mapping](03-visual-editing-and-code-mapping.md)
4. [Chapter 4: AI Chat, Branching, and Iteration](04-ai-chat-branching-and-iteration.md)
5. [Chapter 5: Local Development and Runtime Setup](05-local-development-and-runtime-setup.md)
6. [Chapter 6: Deployment and Team Collaboration](06-deployment-and-team-collaboration.md)
7. [Chapter 7: Contributing and Quality Workflow](07-contributing-and-quality-workflow.md)
8. [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
