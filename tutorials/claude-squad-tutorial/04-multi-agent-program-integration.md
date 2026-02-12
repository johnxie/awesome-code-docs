---
layout: default
title: "Chapter 4: Multi-Agent Program Integration"
nav_order: 4
parent: Claude Squad Tutorial
---

# Chapter 4: Multi-Agent Program Integration

Claude Squad can orchestrate different terminal agents by configuring the program command per session.

## Example Programs

| Agent Program | Launch Example |
|:--------------|:---------------|
| Claude Code | `cs` (default) |
| Codex | `cs -p "codex"` |
| Gemini | `cs -p "gemini"` |
| Aider | `cs -p "aider ..."` |

## Integration Guidance

- keep program-specific environment variables explicit
- validate each program's prompt/approval conventions
- standardize defaults in config for team consistency

## Source References

- [Claude Squad README: multi-agent usage](https://github.com/smtg-ai/claude-squad/blob/main/README.md)

## Summary

You now know how to use Claude Squad as a shared orchestrator across multiple coding agents.

Next: [Chapter 5: Review, Checkout, and Push Workflow](05-review-checkout-and-push-workflow.md)
