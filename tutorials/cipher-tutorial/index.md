---
layout: default
title: "Cipher Tutorial"
nav_order: 118
has_children: true
format_version: v2
---

# Cipher Tutorial: Shared Memory Layer for Coding Agents

> Learn how to use `campfirein/cipher` as a memory-centric MCP-enabled layer that preserves and shares coding context across IDEs, agents, and teams.

[![GitHub Repo](https://img.shields.io/badge/GitHub-campfirein%2Fcipher-black?logo=github)](https://github.com/campfirein/cipher)
[![License](https://img.shields.io/badge/license-Elastic--2.0-blue.svg)](https://github.com/campfirein/cipher/blob/main/LICENSE)
[![Release](https://img.shields.io/badge/release-v0.3.0-blue)](https://github.com/campfirein/cipher/releases/tag/v0.3.0)

## Why This Track Matters

As teams use multiple coding agents, memory continuity becomes a bottleneck. Cipher provides a memory layer with MCP integration, vector stores, and workspace memory for cross-tool continuity.

This track focuses on:

- Cipher modes (CLI, API, MCP, UI)
- dual-memory and reasoning-memory workflows
- vector store and embedding configuration
- MCP server modes and production deployment controls

## Current Snapshot (auto-updated)

- repository: [`campfirein/cipher`](https://github.com/campfirein/cipher)
- stars: about **3.5k**
- latest release: [`v0.3.0`](https://github.com/campfirein/cipher/releases/tag/v0.3.0)
- recent activity: updates on **January 25, 2026**
- project positioning: MCP-compatible memory layer for coding agents

## Mental Model

```mermaid
flowchart LR
    A[Agent Request] --> B[Cipher MCP/API Layer]
    B --> C[Memory Extraction and Search]
    C --> D[Vector Store + Workspace Memory]
    D --> E[Context Returned to Agent]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started](01-getting-started.md) | How do I install and run Cipher quickly? | Working baseline |
| [02 - Core Modes and Session Workflow](02-core-modes-and-session-workflow.md) | How do CLI/API/MCP/UI modes differ? | Correct mode selection |
| [03 - Memory Architecture and Data Model](03-memory-architecture-and-data-model.md) | How does Cipher store knowledge and reasoning memory? | Strong memory mental model |
| [04 - Configuration, Providers, and Embeddings](04-configuration-providers-and-embeddings.md) | How do I configure LLM and embedding stacks? | Reliable config strategy |
| [05 - Vector Stores and Workspace Memory](05-vector-stores-and-workspace-memory.md) | How do persistence and team memory layers work? | Scalable storage architecture |
| [06 - MCP Integration Patterns](06-mcp-integration-patterns.md) | How do I connect Cipher to MCP clients and IDEs? | Cross-tool integration model |
| [07 - Deployment and Operations Modes](07-deployment-and-operations-modes.md) | How do I run Cipher in local/dev/prod setups? | Deployment baseline |
| [08 - Security and Team Governance](08-security-and-team-governance.md) | How do I govern memory operations safely? | Production governance model |

## What You Will Learn

- how to run Cipher as a shared memory service across coding tools
- how to configure embeddings, vector stores, and transport modes
- how to connect and secure MCP integrations across IDEs
- how to govern team memory usage and deployment operations

## Source References

- [Cipher Repository](https://github.com/campfirein/cipher)
- [Cipher README](https://github.com/campfirein/cipher/blob/main/README.md)
- [Configuration guide](https://github.com/campfirein/cipher/blob/main/docs/configuration.md)
- [MCP integration guide](https://github.com/campfirein/cipher/blob/main/docs/mcp-integration.md)
- [CLI reference](https://github.com/campfirein/cipher/blob/main/docs/cli-reference.md)

## Related Tutorials

- [gptme Tutorial](../gptme-tutorial/)
- [OpenSkills Tutorial](../openskills-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [MCP Servers Tutorial](../mcp-servers-tutorial/)

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
2. [Chapter 2: Core Modes and Session Workflow](02-core-modes-and-session-workflow.md)
3. [Chapter 3: Memory Architecture and Data Model](03-memory-architecture-and-data-model.md)
4. [Chapter 4: Configuration, Providers, and Embeddings](04-configuration-providers-and-embeddings.md)
5. [Chapter 5: Vector Stores and Workspace Memory](05-vector-stores-and-workspace-memory.md)
6. [Chapter 6: MCP Integration Patterns](06-mcp-integration-patterns.md)
7. [Chapter 7: Deployment and Operations Modes](07-deployment-and-operations-modes.md)
8. [Chapter 8: Security and Team Governance](08-security-and-team-governance.md)

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
