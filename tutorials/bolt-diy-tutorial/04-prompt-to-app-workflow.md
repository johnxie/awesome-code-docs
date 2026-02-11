---
layout: default
title: "Chapter 4: Prompt-to-App Workflow"
nav_order: 4
parent: Bolt.diy Tutorial
---

# Chapter 4: Prompt-to-App Workflow

Effective bolt.diy usage depends on bounded prompt loops and explicit acceptance criteria.

## Prompt-to-Change Loop

```mermaid
graph LR
    A[Goal Definition] --> B[Scoped Prompt]
    B --> C[Generated Patch]
    C --> D[Diff Review]
    D --> E[Validation Command]
    E --> F[Refine or Accept]
```

## Prompt Structure That Works

Include:

- target files/components
- expected behavior and non-goals
- validation command to run
- completion condition

## Failure Patterns to Avoid

- broad prompts with no file scope
- accepting large diffs without review
- skipping runtime validation after major edits

## Iteration Playbook

For larger features, split the request into milestone prompts:

1. scaffold base structure
2. implement one subsystem
3. validate and fix
4. only then move to the next subsystem

This keeps each generation step reviewable and reversible.

## Summary

You now have a deterministic pattern for converting intent into controlled code changes.

Next: [Chapter 5: Files, Diff, and Locking](05-files-diff-locking.md)
