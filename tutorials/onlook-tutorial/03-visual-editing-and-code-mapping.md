---
layout: default
title: "Chapter 3: Visual Editing and Code Mapping"
nav_order: 3
parent: Onlook Tutorial
---

# Chapter 3: Visual Editing and Code Mapping

This chapter focuses on the core visual editing loop and how to keep changes predictable.

## Learning Goals

- use visual controls for precise layout/styling updates
- understand element-to-code mapping behavior
- avoid destructive or ambiguous bulk edits
- validate generated code efficiently

## Editing Workflow

| Step | Action |
|:-----|:-------|
| inspect | select element in canvas or layer tree |
| modify | change styles/layout through visual controls |
| map | Onlook resolves target code location |
| persist | write updates to source files |
| verify | review code diff and rerun app/tests |

## Safe Iteration Tips

- keep edits scoped to one section at a time
- check generated code after each substantial change
- use branching/checkpoints for large redesigns
- run test/lint passes before merging

## Source References

- [Onlook README: Visual edit capabilities](https://github.com/onlook-dev/onlook/blob/main/README.md#what-you-can-do-with-onlook)
- [Onlook Architecture Docs](https://docs.onlook.com/developers/architecture)

## Summary

You now understand how to run visual editing loops while keeping code quality intact.

Next: [Chapter 4: AI Chat, Branching, and Iteration](04-ai-chat-branching-and-iteration.md)
