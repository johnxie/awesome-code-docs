---
layout: default
title: "Chapter 4: AI Chat, Branching, and Iteration"
nav_order: 4
parent: Onlook Tutorial
---


# Chapter 4: AI Chat, Branching, and Iteration

Welcome to **Chapter 4: AI Chat, Branching, and Iteration**. In this part of **Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers prompt-driven workflows and branch-first experimentation in Onlook.

## Learning Goals

- use AI chat prompts with bounded task scope
- combine prompt edits with manual visual refinement
- use branch/checkpoint workflows to limit risk
- converge faster on production-ready UI outcomes

## Prompt Strategy Baseline

1. start with concise intent + explicit target page/component
2. request one change class at a time (layout, typography, interaction)
3. review generated code after each prompt batch
4. checkpoint/branch before broad UI rewrites

## Iteration Loop

- prompt for draft changes
- inspect visual output
- correct with direct visual edits
- validate code diff and behavior
- commit to branch

## Source References

- [Onlook README](https://github.com/onlook-dev/onlook/blob/main/README.md)
- [Onlook Docs](https://docs.onlook.com)

## Summary

You now have a practical pattern for controlled, high-speed AI-assisted UI iteration.

Next: [Chapter 5: Local Development and Runtime Setup](05-local-development-and-runtime-setup.md)

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
