---
layout: default
title: "Chapter 5: Agent Integration and AGENTS.md Patterns"
nav_order: 5
parent: Beads Tutorial
---

# Chapter 5: Agent Integration and AGENTS.md Patterns

This chapter explains how to standardize Beads usage in coding-agent instructions.

## Learning Goals

- declare Beads expectations in AGENTS.md
- define when agents must read/write Beads tasks
- align task updates with PR and CI workflows
- prevent drift between work and planning state

## Integration Strategy

- include explicit `bd` command expectations
- require status updates on major execution transitions
- pair task state with PR references where possible

## Source References

- [Beads README AGENTS.md Tip](https://github.com/steveyegge/beads/blob/main/README.md)
- [AGENTS.md Tutorial](../agents-md-tutorial/)

## Summary

You now have an integration baseline for predictable agent behavior with Beads.

Next: [Chapter 6: Multi-Branch Collaboration and Protected Flows](06-multi-branch-collaboration-and-protected-flows.md)
