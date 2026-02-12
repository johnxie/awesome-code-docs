---
layout: default
title: "Chapter 2: Agent Loop and State Model"
nav_order: 2
parent: Kilo Code Tutorial
---

# Chapter 2: Agent Loop and State Model

Kilo's CLI architecture uses message-state analysis to track whether the agent is running, streaming, waiting for input, or idle.

## State Categories

| State | Meaning |
|:------|:--------|
| running | active execution |
| streaming | partial output in progress |
| waiting_for_input | explicit user decision needed |
| idle | task completed or halted |

## Why It Matters

This state model allows reliable coordination of approvals, followups, and automation behavior.

## Source References

- [AGENT_LOOP.md](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/docs/AGENT_LOOP.md)

## Summary

You now understand the core loop-state mechanics that drive Kilo interaction behavior.

Next: [Chapter 3: Modes, Prompts, and Approval Workflow](03-modes-prompts-and-approval-workflow.md)
