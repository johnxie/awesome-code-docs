---
layout: default
title: "Chapter 3: Workflow Construction and Deterministic Runtime"
nav_order: 3
parent: Refly Tutorial
---


# Chapter 3: Workflow Construction and Deterministic Runtime

Welcome to **Chapter 3: Workflow Construction and Deterministic Runtime**. In this part of **Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on constructing workflows that remain stable under real operational pressure.

## Learning Goals

- build workflows from intent while preserving deterministic behavior
- validate graph logic before execution
- use state transitions to avoid accidental invalid runs
- design workflows for recovery and reuse

## Builder-Oriented Loop

1. start workflow construction (visual or CLI builder)
2. define nodes, dependencies, and variable contracts
3. validate structure before commit/run
4. run with explicit input and inspect status/output
5. iterate with small deltas and versioned changes

## Determinism Signals

| Signal | Why It Matters |
|:-------|:---------------|
| DAG validation | prevents cycle-based runtime failures |
| explicit state transitions | reduces partial/invalid commits |
| JSON-first outputs | improves machine readability and automation |
| versioned skills | enables safe reuse and rollback |

## Source References

- [README: Core Capabilities](https://github.com/refly-ai/refly/blob/main/README.md#core-capabilities)
- [README: Create Your First Workflow](https://github.com/refly-ai/refly/blob/main/README.md#create-your-first-workflow)
- [CLI README](https://github.com/refly-ai/refly/blob/main/packages/cli/README.md)

## Summary

You now have a practical pattern for building stable workflows and iterating safely.

Next: [Chapter 4: API and Webhook Integrations](04-api-and-webhook-integrations.md)

## Source Code Walkthrough

### `scripts/upload-config.js`

The `main` function in [`scripts/upload-config.js`](https://github.com/refly-ai/refly/blob/HEAD/scripts/upload-config.js) handles a key part of this chapter's functionality:

```js
}

async function main() {
  // upload mcp catalog
  await uploadState('config/mcp-catalog.json', 'mcp-config/mcp-catalog.json');

  await uploadState('config/provider-catalog.json', 'mcp-config/provider-catalog.json');
}

main();

```

This function is important because it defines how Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code implements the patterns covered in this chapter.

### `docs/.vitepress/config.ts`

The `gtag` function in [`docs/.vitepress/config.ts`](https://github.com/refly-ai/refly/blob/HEAD/docs/.vitepress/config.ts) handles a key part of this chapter's functionality:

```ts
      {
        async: '',
        src: 'https://www.googletagmanager.com/gtag/js?id=G-RS0SJYDFJF',
      },
    ],
    [
      'script',
      {},
      `window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-RS0SJYDFJF');`,
    ],
  ],

  // File path rewrites to map /en/* files to root URLs
  rewrites: {
    'en/index.md': 'index.md',
    'en/:path*': ':path*',
  },

  // i18n configuration
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      title: 'Refly Docs',
      description: 'Refly Documentation',
      themeConfig: {
        nav: enNav,
        sidebar: sidebar.en,
        siteTitle: 'Refly Docs',
```

This function is important because it defines how Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[main]
    B[gtag]
    A --> B
```
