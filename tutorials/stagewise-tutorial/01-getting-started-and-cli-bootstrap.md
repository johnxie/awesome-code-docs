---
layout: default
title: "Chapter 1: Getting Started and CLI Bootstrap"
nav_order: 1
parent: Stagewise Tutorial
---

# Chapter 1: Getting Started and CLI Bootstrap

This chapter gets Stagewise running with the correct workspace assumptions so the agent can safely edit your frontend codebase.

## Learning Goals

- run Stagewise from the correct project root
- start a first toolbar-enabled session
- verify prompt flow from browser to agent

## Quick Bootstrap

```bash
# from your frontend app root (where package.json exists)
npx stagewise@latest
```

Or with pnpm:

```bash
pnpm dlx stagewise@latest
```

## First-Run Checklist

1. dev app is running on its own app port
2. Stagewise CLI starts from app root directory
3. toolbar appears in browser on Stagewise proxy port
4. prompt submission reaches selected agent

## Source References

- [Root README](https://github.com/stagewise-io/stagewise/blob/main/README.md)
- [Docs: Getting Started](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/index.mdx)

## Summary

You now have a working Stagewise baseline and understand the root-directory requirement.

Next: [Chapter 2: Proxy and Toolbar Architecture](02-proxy-and-toolbar-architecture.md)
