---
layout: default
title: "Chapter 5: Browser Automation"
nav_order: 5
parent: Cline Tutorial
---

# Chapter 5: Browser Automation

Browser capabilities allow Cline to validate runtime UI behavior, not just source code.

## Browser Workflow

1. run app locally
2. open target page
3. interact with UI elements
4. capture screenshots/logs
5. propose and apply fixes

## High-Value Use Cases

- visual regression checks
- runtime exception discovery
- form flow validation
- end-to-end smoke tests

## Guardrails

| Guardrail | Why |
|:----------|:----|
| domain allowlist | prevent unintended web actions |
| bounded action loops | avoid runaway autonomous browsing |
| artifact capture | keep proof for debugging and review |

## Summary

You can now incorporate browser-grounded validation into Cline-assisted development tasks.

Next: [Chapter 6: MCP and Custom Tools](06-mcp-and-custom-tools.md)
