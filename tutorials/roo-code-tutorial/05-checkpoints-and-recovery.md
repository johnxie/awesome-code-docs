---
layout: default
title: "Chapter 5: Checkpoints and Recovery"
nav_order: 5
parent: Roo Code Tutorial
---


# Chapter 5: Checkpoints and Recovery

Welcome to **Chapter 5: Checkpoints and Recovery**. In this part of **Roo Code Tutorial: Run an AI Dev Team in Your Editor**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Checkpoints are essential for safe experimentation. This chapter explains when to checkpoint, how to compare states, and how to recover cleanly.

## Why Checkpoints Matter

Agentic workflows increase iteration speed. Without snapshot discipline, rollback cost rises sharply when output quality drops.

Checkpoints let you:

- test alternative fixes quickly
- compare patch strategies
- recover without manual cleanup

## Checkpoint Lifecycle

```mermaid
flowchart TD
    A[Create Checkpoint] --> B[Apply Candidate Patch]
    B --> C[Run Validation]
    C --> D{Pass?}
    D -- Yes --> E[Promote and Continue]
    D -- No --> F[Compare with Checkpoint]
    F --> G[Restore and Try Alternate Path]
```

## When to Checkpoint

| Scenario | Why It Is Required |
|:---------|:-------------------|
| multi-file refactor | rollback blast radius is high |
| dependency updates | hidden compatibility risks |
| config/security changes | potential environment-wide impact |
| uncertain root cause | likely need for competing fix paths |

## Recovery Rules

1. annotate checkpoint intent
2. run validation after every restore
3. keep winning and rejected strategy notes
4. avoid chaining too many unlabelled checkpoints

## Compare Strategy

When comparing checkpoint vs current state, inspect:

- changed file count
- high-risk file involvement
- validation command outcomes
- complexity/readability differences

Choose the path with better evidence, not just fewer lines changed.

## Team Workflow Pattern

For collaborative usage:

- checkpoint before risky branch of work
- share short rationale in task summary
- commit only after post-restore validation pass
- archive key decision notes for later incidents

## Common Pitfalls

- checkpointing too late (after risky edits)
- restoring without revalidation
- no explanation of why restore occurred
- treating restore as failure instead of control mechanism

## Chapter Summary

You now have a checkpoint-driven reliability model:

- proactive snapshot timing
- evidence-based compare/restore decisions
- cleaner recovery during high-velocity iteration

Next: [Chapter 6: MCP and Tool Extensions](06-mcp-and-tool-extensions.md)

## Source Code Walkthrough

Use the following upstream sources to verify checkpoint and recovery implementation details while reading this chapter:

- [`src/integrations/checkpoints/`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/src/integrations/checkpoints/) — contains the checkpoint manager that captures task state snapshots using shadow git commits, enabling diff comparison and rollback between task steps.
- [`src/core/task/index.ts`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/src/core/task/index.ts) — integrates with the checkpoint system to record state before destructive operations and expose restore/compare actions to the user.

Suggested trace strategy:
- trace checkpoint creation calls in `src/integrations/checkpoints/` to understand how shadow commits are structured
- review `src/core/task/index.ts` for the task lifecycle points where checkpoints are triggered
- check `src/shared/WebviewMessage.ts` for the message types that drive checkpoint UI interactions (restore, compare)

## How These Components Connect

```mermaid
flowchart LR
    A[Task step begins] --> B[Checkpoint captured in checkpoints/]
    B --> C[Files modified]
    C --> D[User can compare or restore via task/index.ts]
```
