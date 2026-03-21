---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: Onlook Tutorial
---


# Chapter 8: Production Operations and Governance

Welcome to **Chapter 8: Production Operations and Governance**. In this part of **Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter provides a practical adoption model for using Onlook in production teams.

## Learning Goals

- define governance boundaries for AI-assisted visual editing
- keep generated code quality high over time
- align Onlook workflows with enterprise delivery controls
- create a sustainable rollout roadmap

## Governance Baseline

| Area | Recommended Baseline |
|:-----|:---------------------|
| repository control | all generated changes through PR review |
| quality gates | enforce lint/test/build before merge |
| branch strategy | isolate large design experiments |
| security/compliance | manage provider keys and secrets centrally |
| training | publish prompt and visual-edit playbooks |

## Rollout Stages

1. pilot with a single product team and clear metrics
2. compare throughput/quality vs existing UI workflow
3. standardize branch and review conventions
4. expand gradually to additional teams and repositories

## Source References

- [Onlook Documentation](https://docs.onlook.com)
- [Onlook Architecture Docs](https://docs.onlook.com/developers/architecture)
- [Onlook Repository](https://github.com/onlook-dev/onlook)

## Summary

You now have a complete model for operationalizing Onlook in real product-engineering environments.

Compare semantic agent augmentation in the [Serena Tutorial](../serena-tutorial/).

## Depth Expansion Playbook

## Source Code Walkthrough

### `docker-compose.yml`

The `docker-compose` module in [`docker-compose.yml`](https://github.com/onlook-dev/onlook/blob/HEAD/docker-compose.yml) handles a key part of this chapter's functionality:

```yml
name: onlook

services:
  web-client:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - apps/web/client/.env
    ports:
      - "3000:3000"
    restart: unless-stopped
    network_mode: host

networks:
  supabase_network_onlook-web:
    external: true

```

This module is important because it defines how Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind implements the patterns covered in this chapter.

### `docs/next.config.ts`

The `next.config` module in [`docs/next.config.ts`](https://github.com/onlook-dev/onlook/blob/HEAD/docs/next.config.ts) handles a key part of this chapter's functionality:

```ts
/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
import { createMDX } from 'fumadocs-mdx/next';
import { NextConfig } from 'next';
import path from 'node:path';

const withMDX = createMDX();

const nextConfig: NextConfig = {
    reactStrictMode: true,
};

if (process.env.NODE_ENV === 'development') {
    nextConfig.outputFileTracingRoot = path.join(__dirname, '../../..');
}

export default withMDX(nextConfig);

```

This module is important because it defines how Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind implements the patterns covered in this chapter.

### `eslint.config.js`

The `eslint.config` module in [`eslint.config.js`](https://github.com/onlook-dev/onlook/blob/HEAD/eslint.config.js) handles a key part of this chapter's functionality:

```js
import baseConfig from "@onlook/eslint/base";

/** @type {import('typescript-eslint').Config} */
export default [
  ...baseConfig,
  {
    files: ["tooling/**/*.js"],
  },
];

```

This module is important because it defines how Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[docker-compose]
    B[next.config]
    C[eslint.config]
    A --> B
    B --> C
```
