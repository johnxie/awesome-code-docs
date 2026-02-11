---
layout: default
title: "Chapter 3: File and Command Operations"
nav_order: 3
parent: Roo Code Tutorial
---

# Chapter 3: File and Command Operations

Roo Code is most effective when edits and runtime validation are tightly coupled.

## Controlled Edit-and-Verify Loop

1. generate a targeted patch
2. review diff scope and semantics
3. approve apply step
4. run lint/test/build command
5. iterate until deterministic pass

## Review Rubric

| Dimension | Check |
|:----------|:------|
| scope | only intended files changed |
| correctness | logic matches requested behavior |
| risk | no hidden config/security regressions |
| compatibility | public interfaces remain valid |

## Command Safety Controls

- keep destructive commands approval-gated
- use canonical repo commands where possible
- set retry/timeout boundaries for noisy commands

## Summary

You now have a repeatable patch-validation loop for dependable Roo Code outcomes.

Next: [Chapter 4: Context and Indexing](04-context-and-indexing.md)
