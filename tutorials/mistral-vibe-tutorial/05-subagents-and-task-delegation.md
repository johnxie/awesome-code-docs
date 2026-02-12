---
layout: default
title: "Chapter 5: Subagents and Task Delegation"
nav_order: 5
parent: Mistral Vibe Tutorial
---

# Chapter 5: Subagents and Task Delegation

Vibe supports task delegation to subagents, allowing specialized work to run with isolated context.

## Delegation Model

- main agent handles top-level coordination
- subagents perform scoped tasks
- outputs flow back into the primary conversation

## Practical Uses

- codebase exploration in parallel
- focused refactor analysis versus implementation split
- staged task decomposition without overloading main context

## Source References

- [Mistral Vibe README: subagents and task delegation](https://github.com/mistralai/mistral-vibe/blob/main/README.md)

## Summary

You now know how to use subagents to scale complex coding tasks.

Next: [Chapter 6: Programmatic and Non-Interactive Modes](06-programmatic-and-non-interactive-modes.md)
