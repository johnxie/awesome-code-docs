---
layout: default
title: "Chapter 6: Testing and Debugging"
nav_order: 6
has_children: false
parent: "Obsidian Outliner Plugin"
---

# Chapter 6: Testing and Debugging

Editor plugins require strong mutation-focused testing because small command bugs can corrupt note structure.

## High-Value Test Areas

- indent/outdent in nested hierarchies
- move up/down with mixed sibling depths
- fold/unfold state persistence across reloads
- multi-cursor and selection edge cases
- undo/redo across structural + text mutations

## Test Layering Strategy

1. unit tests for pure tree-transform helpers
2. integration tests for command execution in editor context
3. fixture-based regression tests for known bug patterns

## Debugging Workflow

- instrument command entry/exit with structured logs
- snapshot outline tree before and after each command
- isolate parser/selection issues with minimal markdown fixtures
- add deterministic reproduction scripts for flaky failures

## Observability Tips

| Signal | Use |
|:-------|:----|
| command failure rate | catches regressions quickly |
| unexpected selection states | identifies cursor logic bugs |
| mutation latency | reveals slow tree operations |

## Summary

You can now implement a practical quality system for reliable outliner command behavior.

Next: [Chapter 7: Plugin Packaging](07-plugin-packaging.md)
