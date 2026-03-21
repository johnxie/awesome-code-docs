---
layout: default
title: "Chapter 6: Deployment and Team Collaboration"
nav_order: 6
parent: Onlook Tutorial
---


# Chapter 6: Deployment and Team Collaboration

Welcome to **Chapter 6: Deployment and Team Collaboration**. In this part of **Onlook Tutorial: Visual-First AI Coding for Next.js and Tailwind**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on shipping workflows and collaboration patterns around Onlook-generated code.

## Learning Goals

- move from local edits to deployable outputs
- use sharable links and branch workflows for reviews
- avoid collaboration bottlenecks in UI-heavy projects
- align design iteration with engineering quality gates

## Delivery Pattern

| Phase | Practice |
|:------|:---------|
| draft | rapid visual/prompt edits in isolated branch |
| review | share previews, run code review on diffs |
| validate | lint/tests/build checks |
| release | merge branch and deploy |

## Collaboration Guidance

- require code review for major generated UI changes
- keep prompt context and design goals in PR descriptions
- pair design and engineering reviewers for high-impact pages

## Source References

- [Onlook README: deployment/collaboration capabilities](https://github.com/onlook-dev/onlook/blob/main/README.md#what-you-can-do-with-onlook)
- [Onlook Docs](https://docs.onlook.com)

## Summary

You now have a workflow for turning Onlook edits into team-reviewed deployable changes.

Next: [Chapter 7: Contributing and Quality Workflow](07-contributing-and-quality-workflow.md)

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
