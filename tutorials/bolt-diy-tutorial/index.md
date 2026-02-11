---
layout: default
title: "Bolt.diy Tutorial"
nav_order: 96
has_children: true
---

# bolt.diy Tutorial: Open-Source AI Full-Stack Builder

> Learn how to run, extend, and operate `stackblitz-labs/bolt.diy`, the open-source version of Bolt-style AI app building with provider flexibility.

[![Stars](https://img.shields.io/github/stars/stackblitz-labs/bolt.diy?style=social)](https://github.com/stackblitz-labs/bolt.diy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stack](https://img.shields.io/badge/Stack-Remix%20%2B%20Vite-blue)](https://github.com/stackblitz-labs/bolt.diy)

## What is bolt.diy?

`bolt.diy` is an open-source AI coding and app-building environment inspired by Bolt-style workflows, with support for many model providers and local/self-hosted deployment options. It combines chat-driven code generation with an editable workspace, terminal execution, diffing, file locking, and deployment integrations.

## Current Snapshot (February 11, 2026)

- repository: `stackblitz-labs/bolt.diy`
- stars: ~19K
- latest stable release in GitHub Releases: `v1.0.0` (published May 12, 2025)
- active development continues on `main` with frequent updates

## Tutorial Chapters

1. **[Chapter 1: Getting Started](01-getting-started.md)** - Local setup, Docker path, and first run
2. **[Chapter 2: Architecture Overview](02-architecture-overview.md)** - Remix/Vite app structure and execution model
3. **[Chapter 3: Providers and Model Routing](03-providers-and-routing.md)** - Multi-provider strategy and key management
4. **[Chapter 4: Prompt-to-App Workflow](04-prompt-to-app-workflow.md)** - How prompt loops become code changes
5. **[Chapter 5: Files, Diff, and Locking](05-files-diff-locking.md)** - Safety controls for generated edits
6. **[Chapter 6: Integrations and MCP](06-integrations-and-mcp.md)** - External services, MCP, and extension pathways
7. **[Chapter 7: Deployment and Distribution](07-deployment-distribution.md)** - Netlify/Vercel/GitHub Pages and desktop packaging
8. **[Chapter 8: Production Operations](08-production-operations.md)** - Security, observability, and governance patterns

## What You Will Learn

- operate bolt.diy locally and in containerized environments
- configure cloud and local model providers safely
- manage generated code changes with diff/locking workflows
- integrate MCP and external services responsibly
- deploy and run bolt.diy in team/production settings

## Related Tutorials

- [Dyad Tutorial](../dyad-tutorial/)
- [Vercel AI SDK Tutorial](../vercel-ai-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [Continue Tutorial](../continue-tutorial/)

---

Ready to start? Open [Chapter 1: Getting Started](01-getting-started.md).
