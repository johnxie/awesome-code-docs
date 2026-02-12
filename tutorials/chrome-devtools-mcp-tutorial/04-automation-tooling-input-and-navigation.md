---
layout: default
title: "Chapter 4: Automation Tooling: Input and Navigation"
nav_order: 4
parent: Chrome DevTools MCP Tutorial
---

# Chapter 4: Automation Tooling: Input and Navigation

This chapter maps the core automation toolset used in browser control loops.

## Learning Goals

- use input tools (`click`, `fill`, `press_key`) effectively
- manage page lifecycle and navigation safely
- sequence tool calls for deterministic outcomes
- capture snapshots when state verification is needed

## Tooling Strategy

- keep actions small and verifiable
- read snapshots before destructive inputs
- use explicit waits and page selection to avoid race conditions

## Source References

- [Tool Reference: Input Tools](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md#input-automation)
- [Tool Reference: Navigation Tools](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md#navigation-automation)

## Summary

You now have a repeatable automation pattern for browser interactions.

Next: [Chapter 5: Performance and Debugging Workflows](05-performance-and-debugging-workflows.md)
