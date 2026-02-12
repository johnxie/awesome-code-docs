---
layout: default
title: "Chapter 8: Contribution Workflow and Ecosystem Evolution"
nav_order: 8
parent: Stagewise Tutorial
---

# Chapter 8: Contribution Workflow and Ecosystem Evolution

Stagewise is an active monorepo with clear contribution mechanics and a growing frontend-agent ecosystem.

## Learning Goals

- understand contribution flow and monorepo structure
- run development commands for local contribution
- align roadmap decisions with plugin and agent ecosystem growth

## Contribution Baseline

```bash
pnpm install
pnpm dev
pnpm build
pnpm lint
pnpm test
```

## Monorepo Contribution Areas

| Area | Focus |
|:-----|:------|
| `apps/` | website, CLI, and VS Code extension surfaces |
| `plugins/` and `toolbar/` | framework adapters and UI runtime |
| `agent/` | integration interfaces and runtime components |
| `examples/` | reference implementations across frameworks |

## Source References

- [Contributing Guide](https://github.com/stagewise-io/stagewise/blob/main/CONTRIBUTING.md)
- [Developer Contribution Guidelines](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/developer-guides/contribution-guidelines.mdx)
- [Repository](https://github.com/stagewise-io/stagewise)

## Summary

You now have an end-to-end model for adopting, extending, and contributing to Stagewise in production frontend environments.

Next: connect this flow with [VibeSDK](../vibesdk-tutorial/) and [OpenCode](../opencode-tutorial/).
