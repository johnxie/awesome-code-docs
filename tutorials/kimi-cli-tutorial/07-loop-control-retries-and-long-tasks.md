---
layout: default
title: "Chapter 7: Loop Control, Retries, and Long Tasks"
nav_order: 7
parent: Kimi CLI Tutorial
---

# Chapter 7: Loop Control, Retries, and Long Tasks

Kimi includes control knobs for multi-step and long-running tasks where bounded execution is critical.

## Key Controls

- `--max-steps-per-turn`
- `--max-retries-per-step`
- `--max-ralph-iterations`

These help teams prevent runaway loops and tune behavior for complex workflows.

## Reliability Pattern

1. start with conservative step/retry limits
2. inspect outcomes and error modes
3. gradually increase limits only where justified

## Source References

- [Kimi command reference: loop control](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/reference/kimi-command.md)
- [Sessions and context guide](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/guides/sessions.md)

## Summary

You now have an execution-bounding strategy for larger autonomous task loops.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
