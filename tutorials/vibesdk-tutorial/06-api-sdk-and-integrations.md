---
layout: default
title: "Chapter 6: API, SDK, and Integrations"
nav_order: 6
parent: VibeSDK Tutorial
---

# Chapter 6: API, SDK, and Integrations

VibeSDK can be embedded into workflows beyond the chat UI through APIs, the official TypeScript SDK, and automated handoff flows.

## Learning Goals

By the end of this chapter, you should be able to:

- use `@cf-vibesdk/sdk` for programmatic app generation
- choose between phasic and agentic behavior modes
- automate build, wait, preview, and export workflows
- integrate VibeSDK into CI and internal platform operations

## SDK Installation

```bash
npm install @cf-vibesdk/sdk
```

## Minimal SDK Flow

```ts
import { PhasicClient } from '@cf-vibesdk/sdk';

const client = new PhasicClient({
  baseUrl: 'https://build.cloudflare.dev',
  apiKey: process.env.VIBESDK_API_KEY!,
});

const session = await client.build('Build a landing page with auth', {
  projectType: 'app',
  autoGenerate: true,
});

await session.wait.deployable();
session.deployPreview();
await session.wait.previewDeployed();
session.close();
```

## Integration Surfaces

| Surface | Primary Use Case |
|:--------|:-----------------|
| SDK (`PhasicClient`, `AgenticClient`) | scriptable generation and lifecycle automation |
| API routes/controllers | internal governance and operational controls |
| deploy/export tooling | repository handoff and developer workflow integration |
| Postman docs assets | quick API validation and team onboarding |

## Behavior Mode Selection

| Mode | Best For | Risk Profile |
|:-----|:---------|:-------------|
| phasic | controlled enterprise pipelines | slower iteration, higher predictability |
| agentic | exploratory generation and rapid iteration | higher variability, needs stronger guardrails |

## CI-Friendly Automation Pattern

1. trigger build from internal service or pipeline job
2. wait for deployable milestone
3. run policy checks (security, quality, ownership)
4. deploy preview and run smoke tests
5. export/handoff to repo with traceable metadata

## Reliability Practices for Integrations

- always implement timeout and retry handling around wait helpers
- close sessions explicitly to avoid resource leaks
- persist build session metadata for debugging and audit
- separate API keys for automation workloads vs human UI usage

## Source References

- [VibeSDK SDK README](https://github.com/cloudflare/vibesdk/blob/main/sdk/README.md)
- [Postman Collection README](https://github.com/cloudflare/vibesdk/blob/main/docs/POSTMAN_COLLECTION_README.md)
- [VibeSDK Repository](https://github.com/cloudflare/vibesdk)

## Summary

You now have a practical integration model for embedding VibeSDK into programmatic workflows and CI paths.

Next: [Chapter 7: Security, Auth, and Governance](07-security-auth-and-governance.md)
