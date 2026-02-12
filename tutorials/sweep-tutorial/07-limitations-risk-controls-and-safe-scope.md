---
layout: default
title: "Chapter 7: Limitations, Risk Controls, and Safe Scope"
nav_order: 7
parent: Sweep Tutorial
---

# Chapter 7: Limitations, Risk Controls, and Safe Scope

Sweep reliability is highly sensitive to task size and ambiguity. This chapter operationalizes safe scope boundaries.

## Learning Goals

- recognize official limitations before assigning work
- define scope constraints for predictable runs
- establish escalation paths when tasks exceed limits

## Practical Limits to Respect

| Constraint | Operational Implication |
|:-----------|:------------------------|
| large multi-file refactors | split into smaller issues |
| very large files/context | reduce scope and include explicit anchors |
| non-code assets | route to manual workflow |

## Risk Controls

1. gate large tasks with human decomposition first
2. require human review for every generated PR
3. keep strong CI checks and protected-branch rules

## Source References

- [Limitations](https://github.com/sweepai/sweep/blob/main/docs/pages/about/limitations.mdx)
- [Advanced Usage](https://github.com/sweepai/sweep/blob/main/docs/pages/usage/advanced.mdx)

## Summary

You now have a guardrail framework for assigning tasks Sweep can complete with high confidence.

Next: [Chapter 8: Migration Strategy and Long-Term Operations](08-migration-strategy-and-long-term-operations.md)
