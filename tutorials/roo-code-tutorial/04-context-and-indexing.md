---
layout: default
title: "Chapter 4: Context and Indexing"
nav_order: 4
parent: Roo Code Tutorial
---

# Chapter 4: Context and Indexing

In large repositories, quality depends on context precision. This chapter covers how to manage context and indexing strategy in Roo workflows.

## Core Principle

Relevance beats volume.

Passing too much context increases token cost and decreases reasoning quality.

## Context Pipeline

```mermaid
flowchart LR
    A[Task Goal] --> B[Index or Search Relevant Areas]
    B --> C[Curated Context Set]
    C --> D[Mode Execution]
    D --> E[Validation Results]
    E --> F[Next Context Slice]
```

## Context Slicing Strategy

| Situation | Recommended Slice |
|:----------|:------------------|
| single bugfix | one module + failing tests/logs |
| feature iteration | active files + adjacent interfaces |
| migration | architecture map + staged module batches |
| production incident | runtime logs + impacted service paths |

## Indexing Practical Guidance

Use indexing/search to discover candidates, then manually constrain final context set.

Good pattern:

1. broad discovery
2. narrow target selection
3. bounded execution
4. evidence-driven expansion if needed

## Context Mentions and Grounding

Roo docs include context and tool usage surfaces. Regardless of mechanism, include:

- exact files
- concrete errors/logs
- expected behavior
- validation command

This prevents speculative edits.

## Cost and Latency Impact

Context discipline improves:

- response latency
- token spend
- patch accuracy
- reviewer confidence

Treat context selection as an engineering activity, not a UI action.

## Failure Patterns

### Over-contexting

Symptom: unrelated edits and slow loops.

Fix: remove low-relevance files and enforce explicit scope.

### Under-contexting

Symptom: shallow fixes that ignore true root cause.

Fix: add targeted interface/dependency files and concrete error traces.

### Stale context between mode changes

Symptom: mode transitions lose constraints.

Fix: include concise state summary when switching modes.

## Chapter Summary

You now have a context/indexing model for large repos:

- discover broadly, execute narrowly
- tie context to validation evidence
- maintain continuity across mode transitions

Next: [Chapter 5: Checkpoints and Recovery](05-checkpoints-and-recovery.md)
