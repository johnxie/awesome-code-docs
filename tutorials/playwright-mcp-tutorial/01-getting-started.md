---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Playwright MCP Tutorial
---

# Chapter 1: Getting Started

This chapter gets Playwright MCP installed and validated with a minimal host configuration.

## Learning Goals

- add Playwright MCP with standard `npx` config
- verify browser tool availability in your host
- run first navigation/snapshot actions successfully
- establish a clean baseline for deeper configuration

## Standard Config Baseline

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## First Validation Loop

1. connect server in your host client
2. run `browser_navigate` to a known URL
3. run `browser_snapshot`
4. run one simple interaction (click or fill)

## Source References

- [README: Getting Started](https://github.com/microsoft/playwright-mcp/blob/main/README.md#getting-started)

## Summary

You now have Playwright MCP connected and executing basic browser tasks.

Next: [Chapter 2: Operating Model: Accessibility Snapshots](02-operating-model-accessibility-snapshots.md)
