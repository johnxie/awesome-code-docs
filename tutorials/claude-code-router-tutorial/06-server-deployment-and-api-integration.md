---
layout: default
title: "Chapter 6: Server Deployment and API Integration"
nav_order: 6
parent: Claude Code Router Tutorial
---


# Chapter 6: Server Deployment and API Integration

Welcome to **Chapter 6: Server Deployment and API Integration**. In this part of **Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers deploying CCR server for local teams and service-oriented usage.

## Learning Goals

- choose local vs Docker deployment modes
- mount and manage configuration safely in containers
- expose and monitor core API surfaces
- apply production deployment hygiene

## Deployment Building Blocks

| Area | Key Artifact |
|:-----|:-------------|
| container deployment | Docker image / compose patterns |
| configuration management | mounted `config.json` and env interpolation |
| API surface | config and log endpoints |
| production hardening | reverse proxy + HTTPS + health checks |

## Source References

- [Server Deployment Guide](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/deployment.md)
- [Server API Overview](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/api/overview.md)
- [README](https://github.com/musistudio/claude-code-router/blob/main/README.md)

## Summary

You now have a baseline for running CCR as an operational service.

Next: [Chapter 7: GitHub Actions, Non-Interactive Mode, and Team Ops](07-github-actions-non-interactive-mode-and-team-ops.md)

## Source Code Walkthrough

### `docs/sidebars.ts`

The `sidebars` module in [`docs/sidebars.ts`](https://github.com/musistudio/claude-code-router/blob/HEAD/docs/sidebars.ts) handles a key part of this chapter's functionality:

```ts
import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'CLI',
      link: {
        type: 'generated-index',
        title: 'Claude Code Router CLI',
        description: 'Command-line tool usage guide',
        slug: 'category/cli',
      },
      items: [
        'cli/intro',
        'cli/installation',
        'cli/quick-start',
        {
          type: 'category',
          label: 'Commands',
          link: {
            type: 'generated-index',
            title: 'CLI Commands',
            description: 'Complete command reference',
            slug: 'category/cli-commands',
          },
          items: [
            'cli/commands/start',
            'cli/commands/model',
            'cli/commands/status',
            'cli/commands/statusline',
            'cli/commands/preset',
            'cli/commands/other',
          ],
        },
```

This module is important because it defines how Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code implements the patterns covered in this chapter.

### `tsconfig.base.json`

The `tsconfig.base` module in [`tsconfig.base.json`](https://github.com/musistudio/claude-code-router/blob/HEAD/tsconfig.base.json) handles a key part of this chapter's functionality:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "CommonJS",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "noImplicitAny": true,
    "allowSyntheticDefaultImports": true,
    "sourceMap": true,
    "declaration": true,
    "typeRoots": ["./node_modules/@types", "./packages/*/node_modules/@types"]
  }
}

```

This module is important because it defines how Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code implements the patterns covered in this chapter.

### `package.json`

The `package` module in [`package.json`](https://github.com/musistudio/claude-code-router/blob/HEAD/package.json) handles a key part of this chapter's functionality:

```json
{
  "name": "@musistudio/claude-code-router",
  "version": "2.0.0",
  "description": "Use Claude Code without an Anthropics account and route it to another LLM provider",
  "scripts": {
    "build": "pnpm build:shared && pnpm build:core && pnpm build:server && pnpm build:cli && pnpm build:ui",
    "build:core": "pnpm --filter @musistudio/llms build",
    "build:shared": "pnpm --filter @CCR/shared build",
    "build:cli": "pnpm --filter @CCR/cli build",
    "build:server": "pnpm --filter @CCR/server build",
    "build:ui": "pnpm --filter @CCR/ui build",
    "build:docs": "pnpm --filter claude-code-router-docs build",
    "release": "pnpm build && bash scripts/release.sh all",
    "release:npm": "bash scripts/release.sh npm",
    "release:docker": "bash scripts/release.sh docker",
    "dev:cli": "pnpm --filter @CCR/cli dev",
    "dev:server": "pnpm --filter @CCR/server dev",
    "dev:ui": "pnpm --filter @CCR/ui dev",
    "dev:core": "pnpm --filter @musistudio/llms dev",
    "dev:docs": "pnpm --filter claude-code-router-docs start",
    "serve:docs": "pnpm --filter claude-code-router-docs serve"
  },
  "bin": {
    "ccr": "dist/cli.js"
  },
  "keywords": [
    "claude",
    "code",
    "router",
    "llm",
    "anthropic"
  ],
  "author": "musistudio",
  "license": "MIT",
  "devDependencies": {
```

This module is important because it defines how Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[sidebars]
    B[tsconfig.base]
    C[package]
    A --> B
    B --> C
```
