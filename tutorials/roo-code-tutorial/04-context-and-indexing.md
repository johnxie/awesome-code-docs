---
layout: default
title: "Chapter 4: Context and Indexing"
nav_order: 4
parent: Roo Code Tutorial
---

# Chapter 4: Context and Indexing

Large-codebase performance depends on disciplined context management.

## Context Strategy

- include only task-relevant files and traces
- use indexing/search features for targeted retrieval
- avoid context flooding with entire repositories

## Indexing Benefits

Good indexing enables faster retrieval of symbols, references, and related files, which improves agent grounding and reduces hallucinated edits.

## Context Governance

| Rule | Purpose |
|:-----|:--------|
| explicit include set | lower token cost |
| relevance-first retrieval | higher answer precision |
| stale context refresh | prevent outdated assumptions |

## Summary

You can now manage context as a resource with quality, latency, and cost impact.

Next: [Chapter 5: Checkpoints and Recovery](05-checkpoints-and-recovery.md)
