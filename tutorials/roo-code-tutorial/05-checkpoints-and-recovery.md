---
layout: default
title: "Chapter 5: Checkpoints and Recovery"
nav_order: 5
parent: Roo Code Tutorial
---

# Chapter 5: Checkpoints and Recovery

Checkpoints let teams experiment quickly without accepting irreversible drift.

## Checkpoint Lifecycle

1. capture baseline before risky edits
2. execute candidate patch set
3. compare behavior and diff against checkpoint
4. restore and branch another strategy when needed

## When to Checkpoint

| Situation | Why Snapshot First |
|:----------|:-------------------|
| multi-file refactor | rollback cost is otherwise high |
| dependency/config shifts | blast radius can be broad |
| uncertain bug root cause | enables parallel repair paths |

## Recovery Rules

- annotate checkpoint intent before execution
- always rerun validation after restore
- record winning vs rejected approaches for future prompts

## Summary

You now have a rollback discipline that supports fast experimentation with lower operational risk.

Next: [Chapter 6: MCP and Tool Extensions](06-mcp-and-tool-extensions.md)
