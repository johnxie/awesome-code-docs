---
layout: default
title: "Chapter 4: Prompt-to-App Workflow"
nav_order: 4
parent: Bolt.diy Tutorial
---

# Chapter 4: Prompt-to-App Workflow

This chapter covers how prompts become concrete, reviewable application changes.

## Workflow Stages

1. define target outcome (feature, fix, refactor)
2. generate proposed edits
3. inspect diffs and workspace impacts
4. run or validate changes
5. iterate with focused follow-up prompts

## Prompting Pattern That Works

Use constrained prompts:

- requested files/components
- acceptance criteria
- non-goals and constraints
- validation command to run

This significantly reduces oversized or misdirected edits.

## Effective Iteration Loop

```text
goal -> scoped prompt -> diff review -> run checks -> refine
```

Treat each loop as a bounded change set, not an open-ended generation session.

## Common Failure Modes

- vague prompts leading to broad edits
- skipped diff review before applying
- no validation command after major modifications

## Summary

You can now drive bolt.diy like a controlled development workflow instead of a one-shot code generator.

Next: [Chapter 5: Files, Diff, and Locking](05-files-diff-locking.md)
