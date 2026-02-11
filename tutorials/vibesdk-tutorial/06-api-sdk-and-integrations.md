---
layout: default
title: "Chapter 6: API, SDK, and Integrations"
nav_order: 6
parent: VibeSDK Tutorial
---

# Chapter 6: API, SDK, and Integrations

Beyond the web UI, VibeSDK exposes programmable workflows through APIs and an official TypeScript SDK.

## SDK Quick Start

```bash
npm install @cf-vibesdk/sdk
```

```ts
import { PhasicClient } from '@cf-vibesdk/sdk';

const client = new PhasicClient({
  baseUrl: 'https://build.cloudflare.dev',
  apiKey: process.env.VIBESDK_API_KEY!,
});

const session = await client.build('Build a simple hello world page.', {
  projectType: 'app',
  autoGenerate: true,
});

await session.wait.deployable();
session.close();
```

## Integration Surfaces

| Surface | Use Case |
|:--------|:---------|
| REST/API routes | internal platform and automation hooks |
| SDK (`@cf-vibesdk/sdk`) | CI-driven app generation and lifecycle orchestration |
| GitHub export flow | move generated code into external repos |
| Postman collections in `docs/` | team onboarding and API exploration |

## Practical Integration Pattern

1. trigger generation from CI or an internal portal
2. stream state until deployable
3. auto-run policy checks
4. export code and open PR in target repo

## Summary

You now have the building blocks to automate VibeSDK workflows outside the default chat interface.

Next: [Chapter 7: Security, Auth, and Governance](07-security-auth-and-governance.md)
