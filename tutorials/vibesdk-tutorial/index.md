---
layout: default
title: "VibeSDK Tutorial"
nav_order: 99
has_children: true
---

# VibeSDK Tutorial: Build Your Own Vibe-Coding Platform on Cloudflare

> Learn `cloudflare/vibesdk`, an open-source platform that turns natural-language product prompts into deployable full-stack apps.

[![Stars](https://img.shields.io/github/stars/cloudflare/vibesdk?style=social)](https://github.com/cloudflare/vibesdk)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/Demo-build.cloudflare.dev-orange)](https://build.cloudflare.dev)

## What is VibeSDK?

VibeSDK is Cloudflare's reference implementation for a full-stack AI app generation platform. It combines a React frontend, Workers backend, Durable Object agent orchestration, sandboxed preview containers, and one-click deployment.

## Current Snapshot (February 11, 2026)

- repository: `cloudflare/vibesdk`
- stars: ~4.7K
- stable release line: `v1.5.x` (`v1.5.0` published February 6, 2026)
- license: MIT
- core platform: Cloudflare Workers, Durable Objects, D1, KV, R2, Containers

## Tutorial Chapters

1. **[Chapter 1: Getting Started and Deployment Paths](01-getting-started-and-deployment-paths.md)** - local setup, deploy button flow, and first-run checks
2. **[Chapter 2: System Architecture](02-system-architecture.md)** - frontend/backend/agent topology and runtime boundaries
3. **[Chapter 3: AI Pipeline and Phase Engine](03-ai-pipeline-and-phase-engine.md)** - blueprinting, phased generation, review, and correction loops
4. **[Chapter 4: Sandbox and Preview Runtime](04-sandbox-and-preview-runtime.md)** - container lifecycle, preview routing, and execution isolation
5. **[Chapter 5: Data Layer and Persistence](05-data-layer-and-persistence.md)** - D1, KV, R2, Durable Object state, and migration patterns
6. **[Chapter 6: API, SDK, and Integrations](06-api-sdk-and-integrations.md)** - platform APIs, TypeScript SDK usage, GitHub export, and automation
7. **[Chapter 7: Security, Auth, and Governance](07-security-auth-and-governance.md)** - identity, secrets, rate limits, and tenant controls
8. **[Chapter 8: Production Operations and Scaling](08-production-operations-and-scaling.md)** - observability, rollout strategy, cost/perf controls, and runbooks

## What You Will Learn

- how VibeSDK orchestrates an end-to-end prompt-to-app lifecycle
- how to tune AI routing and phase behaviors safely
- how to operate preview sandboxes at scale
- how to secure and govern a multi-user deployment

## Related Tutorials

- [bolt.diy Tutorial](../bolt-diy-tutorial/)
- [Dyad Tutorial](../dyad-tutorial/)
- [Vercel AI SDK Tutorial](../vercel-ai-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)

---

Ready to begin? Continue to [Chapter 1: Getting Started and Deployment Paths](01-getting-started-and-deployment-paths.md).
