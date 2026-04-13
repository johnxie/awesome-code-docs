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

## Source Code Walkthrough

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

### `docs/tsconfig.json`

The `tsconfig` module in [`docs/tsconfig.json`](https://github.com/onlook-dev/onlook/blob/HEAD/docs/tsconfig.json) handles a key part of this chapter's functionality:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "target": "ESNext",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "paths": {
      "@/.source": [
        "./.source/index.ts"
      ],
      "@/*": [
        "./src/*"
      ]
    },
    "plugins": [
      {
        "name": "next"
      }
    ]
  },
```

This module is important because it defines how Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[next.config]
    B[tsconfig]
    A --> B
```
