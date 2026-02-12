---
layout: default
title: "Chapter 6: Search, Planning, and Execution Patterns"
nav_order: 6
parent: Sweep Tutorial
---

# Chapter 6: Search, Planning, and Execution Patterns

Sweep performance depends on a consistent internal pattern: search, plan, implement, validate, and revise.

## Learning Goals

- map the fixed-flow execution philosophy
- align prompt structure with search and planning strengths
- minimize failures from under-specified tasks

## Execution Philosophy

From project docs and FAQ, Sweep emphasizes a bounded workflow instead of open-domain tool execution:

1. search and identify relevant code context
2. plan changes from issue instructions
3. write and update code in PR form
4. validate through CI and user feedback

## Prompting Patterns That Help

| Pattern | Benefit |
|:--------|:--------|
| mention target files/functions | better retrieval precision |
| include desired behavior and constraints | clearer planning output |
| provide reference implementation files | stronger stylistic alignment |

## Source References

- [Advanced Usage](https://github.com/sweepai/sweep/blob/main/docs/pages/usage/advanced.mdx)
- [FAQ](https://github.com/sweepai/sweep/blob/main/docs/pages/faq.mdx)

## Summary

You now understand the core behavioral pattern that drives Sweep output quality.

Next: [Chapter 7: Limitations, Risk Controls, and Safe Scope](07-limitations-risk-controls-and-safe-scope.md)
