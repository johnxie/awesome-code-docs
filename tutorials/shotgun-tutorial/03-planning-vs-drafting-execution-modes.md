---
layout: default
title: "Chapter 3: Planning vs Drafting Execution Modes"
nav_order: 3
parent: Shotgun Tutorial
---

# Chapter 3: Planning vs Drafting Execution Modes

Shotgun exposes two user-facing execution modes with different tradeoffs.

## Mode Comparison

| Mode | Behavior | Best For |
|:-----|:---------|:---------|
| Planning | step-by-step confirmations and checkpoints | high-risk or high-complexity work |
| Drafting | continuous execution with fewer interruptions | well-scoped work where speed matters |

## Practical Guidance

Use Planning when:

- requirements are still evolving
- cross-cutting changes affect many files
- you need signoff checkpoints for team review

Use Drafting when:

- plan is already validated
- workflow is repetitive
- you are optimizing for cycle time

## Operator Controls

- mode switching is available in TUI
- planner checkpoints help catch drift early
- drafting reduces manual overhead for mature flows

## Source References

- [Shotgun README: Planning vs Drafting](https://github.com/shotgun-sh/shotgun#planning-vs-drafting)

## Summary

You can now choose execution mode based on risk, ambiguity, and throughput needs.

Next: [Chapter 4: Codebase Indexing and Context Retrieval](04-codebase-indexing-and-context-retrieval.md)
