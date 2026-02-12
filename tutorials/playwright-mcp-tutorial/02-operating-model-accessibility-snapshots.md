---
layout: default
title: "Chapter 2: Operating Model: Accessibility Snapshots"
nav_order: 2
parent: Playwright MCP Tutorial
---

# Chapter 2: Operating Model: Accessibility Snapshots

This chapter explains why Playwright MCP emphasizes structured accessibility snapshots instead of image-first control.

## Learning Goals

- understand snapshot-first interaction mechanics
- map snapshot references to deterministic tool inputs
- reduce fragile visual automation behaviors
- decide when screenshots are diagnostic vs operational

## Core Principle

Use `browser_snapshot` as the primary interaction surface, then reference exact nodes for actions. This reduces ambiguity and improves reproducibility.

## Practical Guidance

| Situation | Preferred Approach |
|:----------|:-------------------|
| planning an interaction | snapshot and inspect references |
| executing click/type/select | pass exact `ref` from snapshot |
| debugging layout issues | use screenshot as supplemental artifact |

## Source References

- [README: Playwright MCP vs Playwright CLI](https://github.com/microsoft/playwright-mcp/blob/main/README.md#playwright-mcp-vs-playwright-cli)
- [README: Tools](https://github.com/microsoft/playwright-mcp/blob/main/README.md#tools)

## Summary

You now have the core interaction model for deterministic browser automation.

Next: [Chapter 3: Installation Across Host Clients](03-installation-across-host-clients.md)
