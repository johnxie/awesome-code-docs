---
layout: default
title: "Chapter 5: Browser Automation"
nav_order: 5
parent: Cline Tutorial
---

# Chapter 5: Browser Automation

Browser tooling lets Cline verify behavior in the running application, closing the gap between source edits and user-facing outcomes.

## UI Validation Loop

1. launch app/runtime target
2. navigate to target view
3. execute user-like interactions
4. capture errors/screenshots/DOM observations
5. apply and verify fixes

## Best-Fit Use Cases

| Use Case | Why Browser Tooling Helps |
|:---------|:--------------------------|
| regression checks | validates actual rendered behavior |
| form/flow breakages | reproduces interaction bugs faster |
| runtime JS errors | captures failures not visible in static code |
| accessibility smoke checks | verifies baseline navigation/readability issues |

## Reliability Controls

- whitelist domains and environments
- keep action loops bounded by max steps
- require artifacts (screenshots/logs) for bug claims
- separate exploratory browsing from release validation

## Summary

You can now combine Cline edits with browser-grounded evidence before accepting changes.

Next: [Chapter 6: MCP and Custom Tools](06-mcp-and-custom-tools.md)
