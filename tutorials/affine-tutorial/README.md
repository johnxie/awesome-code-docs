---
layout: default
title: "AFFiNE Tutorial"
nav_order: 192
has_children: true
format_version: v2
---

# AFFiNE Tutorial: Open-Source AI Workspace with Docs, Whiteboards, and Databases

> Learn how to use `toeverything/AFFiNE` to build, extend, and self-host a modern knowledge workspace combining documents, whiteboards, and databases — powered by BlockSuite, CRDT-based collaboration, and integrated AI copilot features.

[![GitHub Repo](https://img.shields.io/badge/GitHub-toeverything%2FAFFiNE-black?logo=github)](https://github.com/toeverything/AFFiNE)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/toeverything/AFFiNE/blob/canary/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/toeverything/AFFiNE)](https://github.com/toeverything/AFFiNE/releases)

## Why This Track Matters

AFFiNE is one of the most ambitious open-source alternatives to Notion and Miro, combining document editing, whiteboard canvases, and structured databases into a single workspace. With approximately 66,000 GitHub stars, it represents a significant shift in how developers think about collaborative knowledge tools.

This track is particularly relevant for developers who:

- want to understand how modern block-based editors are architected with BlockSuite
- need to learn CRDT-based real-time collaboration patterns using yjs and OctoBase
- are building AI-augmented productivity tools and want to study copilot integration patterns
- plan to self-host a Notion-like workspace with full data ownership and extensibility

This track focuses on:

- understanding the BlockSuite framework and its block-tree content model
- mastering the dual page/edgeless editing modes and their underlying data structures
- learning CRDT synchronization with yjs for conflict-free real-time collaboration
- integrating AI copilot features into document and whiteboard workflows
- building custom blocks and plugins to extend the workspace
- deploying and operating self-hosted AFFiNE instances in production

## Current Snapshot (auto-updated)

- repository: [`toeverything/AFFiNE`](https://github.com/toeverything/AFFiNE)
- stars: about **67k**
- latest release: [`v0.26.3`](https://github.com/toeverything/AFFiNE/releases/tag/v0.26.3) (published 2026-02-25)

## Mental Model

```mermaid
flowchart LR
    A[Knowledge need] --> B[Workspace creation]
    B --> C[Block-based content authoring]
    C --> D[Page and edgeless modes]
    D --> E[CRDT sync and collaboration]
    E --> F[AI copilot augmentation]
    F --> G[Database views and organization]
    G --> H[Plugin extension and deployment]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I set up AFFiNE locally and create my first workspace? | Working dev environment and first workspace |
| [02 - System Architecture](02-system-architecture.md) | How does BlockSuite, OctoBase, and yjs fit together? | Clear mental model of the full stack |
| [03 - Block System](03-block-system.md) | How do blocks, pages, and edgeless canvases work? | Understanding of the content model |
| [04 - Collaborative Editing](04-collaborative-editing.md) | How does real-time CRDT sync and conflict resolution work? | Ability to reason about collaboration |
| [05 - AI Copilot](05-ai-copilot.md) | How are AI features integrated into the workspace? | Understanding of copilot architecture |
| [06 - Database and Views](06-database-and-views.md) | How do database blocks, kanban, and table views work? | Ability to build structured data workflows |
| [07 - Plugin System](07-plugin-system.md) | How do I extend AFFiNE with custom blocks and plugins? | Plugin development readiness |
| [08 - Self-Hosting and Deployment](08-self-hosting-and-deployment.md) | How do I deploy and operate AFFiNE in production? | Production deployment baseline |

## What You Will Learn

- how AFFiNE's BlockSuite framework organizes content into a composable block tree
- how page mode and edgeless (whiteboard) mode share the same underlying data model
- how yjs CRDTs enable real-time conflict-free collaboration across clients
- how the AI copilot integrates with blocks for writing assistance, summarization, and generation
- how database blocks support table, kanban, and filtered views within documents
- how to build custom blocks and plugins using AFFiNE's extension architecture
- how to self-host AFFiNE with Docker and configure storage backends

## Source References

- [AFFiNE Repository](https://github.com/toeverything/AFFiNE)
- [README](https://github.com/toeverything/AFFiNE/blob/canary/README.md)
- [BlockSuite Repository](https://github.com/toeverything/blocksuite)
- [AFFiNE Documentation](https://docs.affine.pro)
- [Self-Hosting Guide](https://docs.affine.pro/docs/self-host-affine)

## Related Tutorials

- [LobeChat Tutorial](../lobechat-tutorial/) — AI chat framework with plugin architecture and multi-model support
- [Dify Tutorial](../dify-tutorial/) — LLM app development platform with visual workflow orchestration
- [SiYuan Tutorial](../siyuan-tutorial/) — Local-first personal knowledge management system

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
2. [Chapter 2: System Architecture](02-system-architecture.md)
3. [Chapter 3: Block System](03-block-system.md)
4. [Chapter 4: Collaborative Editing](04-collaborative-editing.md)
5. [Chapter 5: AI Copilot](05-ai-copilot.md)
6. [Chapter 6: Database and Views](06-database-and-views.md)
7. [Chapter 7: Plugin System](07-plugin-system.md)
8. [Chapter 8: Self-Hosting and Deployment](08-self-hosting-and-deployment.md)

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
