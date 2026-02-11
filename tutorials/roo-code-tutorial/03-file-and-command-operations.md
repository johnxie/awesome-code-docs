---
layout: default
title: "Chapter 3: File and Command Operations"
nav_order: 3
parent: Roo Code Tutorial
---

# Chapter 3: File and Command Operations

Effective Roo workflows combine code edits with runtime verification.

## Operation Loop

1. propose targeted file changes
2. review diffs
3. approve and apply
4. execute validation commands
5. iterate based on output

## Safety Controls

- keep destructive shell actions approval-gated
- scope edits to explicit file sets
- require validation command before task completion

## Reliability Practices

| Practice | Benefit |
|:---------|:--------|
| deterministic test/lint command | consistent verification |
| structured command logs | easier debugging/audit |
| bounded retry policy | avoids runaway loops |

## Summary

You now have a practical edit-and-verify loop for reliable Roo Code operation.

Next: [Chapter 4: Context and Indexing](04-context-and-indexing.md)
