---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Onlook Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gets you productive with Onlook through hosted and local entry points.

## Learning Goals

- choose hosted or local startup path
- initialize a Next.js + Tailwind workflow in Onlook
- understand first edit and preview loop
- avoid common setup friction quickly

## Startup Paths

| Path | Best For | Entry |
|:-----|:---------|:------|
| hosted app | fastest learning path | [onlook.com](https://onlook.com) |
| local development | contributors and advanced customization | [running locally docs](https://docs.onlook.com/developers/running-locally) |

## First-Use Checklist

1. open or create a Next.js + Tailwind project
2. run first visual edit in preview canvas
3. use AI chat for a scoped UI change
4. verify generated code in source panel
5. confirm change persists in your repository files

## Source References

- [Onlook README: Getting Started](https://github.com/onlook-dev/onlook/blob/main/README.md#getting-started)
- [Onlook Running Locally](https://docs.onlook.com/developers/running-locally)

## Summary

You now have a working Onlook baseline for visual and prompt-driven iteration.

Next: [Chapter 2: Product and Architecture Foundations](02-product-and-architecture-foundations.md)

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
