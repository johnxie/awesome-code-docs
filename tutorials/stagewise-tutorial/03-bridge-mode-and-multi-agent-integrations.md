---
layout: default
title: "Chapter 3: Bridge Mode and Multi-Agent Integrations"
nav_order: 3
parent: Stagewise Tutorial
---

# Chapter 3: Bridge Mode and Multi-Agent Integrations

Bridge mode allows Stagewise to route prompts to external IDE agents instead of the built-in Stagewise agent runtime.

## Learning Goals

- decide when to run Stagewise in bridge mode
- map supported external agent integrations
- avoid common bridge-mode misconfiguration

## Bridge Mode Command

```bash
stagewise -b
```

With explicit workspace:

```bash
stagewise -b -w ~/repos/my-dev-app
```

## Supported Agent Examples

| Agent Surface | Status |
|:--------------|:-------|
| Cursor | supported |
| GitHub Copilot | supported |
| Windsurf | supported |
| Cline / Roo Code / Kilo Code / Trae | supported |

## Source References

- [Use Different Agents](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/advanced-usage/use-different-agents.mdx)
- [VS Code Extension README](https://github.com/stagewise-io/stagewise/blob/main/apps/vscode-extension/README.md)

## Summary

You now know how to route Stagewise browser context into external coding-agent ecosystems.

Next: [Chapter 4: Configuration and Plugin Loading](04-configuration-and-plugin-loading.md)
