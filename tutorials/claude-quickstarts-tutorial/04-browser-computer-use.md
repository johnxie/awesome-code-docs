---
layout: default
title: "Chapter 4: Browser and Computer Use"
nav_order: 4
parent: Claude Quickstarts Tutorial
---

# Chapter 4: Browser and Computer Use

Browser and desktop control quickstarts are high leverage, but they require explicit safety boundaries.

## Execution Loop

A reliable automation loop is:

1. inspect state (DOM snapshot, screenshot, focused window)
2. plan a single concrete action
3. execute action
4. verify resulting state
5. repeat until goal or stop condition

This keeps errors localized and makes debugging straightforward.

## Browser Automation Pattern

Use short, verifiable actions:

- navigate to known URL
- wait for explicit selectors
- fill one field at a time
- verify expected text/state before continuing

Avoid monolithic "do everything" instructions that hide failure points.

## Computer-Use Risk Model

Desktop automation should classify actions into risk tiers:

| Tier | Example | Required Control |
|:-----|:--------|:-----------------|
| Low | read visible state | none or lightweight logging |
| Medium | non-destructive clicks/type | confirmation on first use |
| High | file deletion/send/submit | explicit human approval per action |

## Guardrails

- strict domain and application allowlists
- denylist destructive shortcuts by default
- short action timeouts with retry limits
- full action log with screenshots for audit

## Failure Recovery

When state diverges from expectations:

- stop action sequence
- capture current state artifacts
- ask for user confirmation or corrected target

## Summary

You can now run browser/computer-use workflows with a deterministic control loop and practical safety gates.

Next: [Chapter 5: Autonomous Coding Agents](05-autonomous-coding-agents.md)
