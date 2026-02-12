---
layout: default
title: "Chapter 2: Router Architecture and Agent Lifecycle"
nav_order: 2
parent: Shotgun Tutorial
---

# Chapter 2: Router Architecture and Agent Lifecycle

Shotgun routes requests through specialized agents instead of using one generic prompt loop.

## Lifecycle Model

| Stage | Purpose |
|:------|:--------|
| Research | understand codebase and external context |
| Specify | define requirements and boundaries |
| Plan | propose staged implementation roadmap |
| Tasks | decompose into execution-ready units |
| Export | emit agent-ready deliverables |

## Why This Matters

- each stage can use more focused prompts
- outputs stay structured and easier to review
- task handoff quality improves across long features

## Implementation Signals

Shotgun documentation describes a router that orchestrates these phases internally while exposing user-facing mode controls.

## Source References

- [Shotgun README: router flow](https://github.com/shotgun-sh/shotgun#-features)
- [CLI docs](https://github.com/shotgun-sh/shotgun/blob/main/docs/CLI.md)

## Summary

You now understand how Shotgun sequences specialized agents across the delivery lifecycle.

Next: [Chapter 3: Planning vs Drafting Execution Modes](03-planning-vs-drafting-execution-modes.md)
