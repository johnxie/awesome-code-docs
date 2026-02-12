---
layout: default
title: "Chapter 6: Timeline, Checkpoints, and Recovery"
nav_order: 6
parent: Opcode Tutorial
---

# Chapter 6: Timeline, Checkpoints, and Recovery

This chapter focuses on versioned session control and rollback safety.

## Learning Goals

- use checkpoints to protect long-running sessions
- restore and fork from prior states quickly
- inspect diffs between checkpoints
- design safer experimentation workflows

## Checkpoint Strategy

| Pattern | When to Use |
|:--------|:------------|
| checkpoint before big prompt | any high-impact refactor/design change |
| branch from checkpoint | exploring alternative implementations |
| restore previous state | output drift or regressions |

## Source References

- [Opcode README: Timeline & Checkpoints](https://github.com/winfunc/opcode/blob/main/README.md#-timeline--checkpoints)
- [Opcode README: Diff Viewer mentions](https://github.com/winfunc/opcode/blob/main/README.md#-timeline--checkpoints)

## Summary

You now know how to use checkpointing as a first-class safety primitive in Opcode.

Next: [Chapter 7: Development Workflow and Build from Source](07-development-workflow-and-build-from-source.md)
