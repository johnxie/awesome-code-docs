---
layout: default
title: "Chapter 6: API, SDK, and Integrations"
nav_order: 6
parent: VibeSDK Tutorial
---

# Chapter 6: API, SDK, and Integrations

VibeSDK can be operated programmatically through APIs and the official TypeScript SDK.

## SDK Starter

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
| REST/API routes | internal platform actions and governance flows |
| SDK | CI-driven generation and lifecycle control |
| GitHub exporter | repository handoff and PR workflows |
| Postman collection in `docs/` | team onboarding and API testing |

## Automation Pattern

1. trigger generation from CI or internal portal
2. wait for deployable state
3. enforce policy checks
4. export and open PR in target repository

## Summary

You now have the integration model to run VibeSDK beyond manual chat usage.

Next: [Chapter 7: Security, Auth, and Governance](07-security-auth-and-governance.md)
