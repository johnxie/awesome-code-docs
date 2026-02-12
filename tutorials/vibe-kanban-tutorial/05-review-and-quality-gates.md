---
layout: default
title: "Chapter 5: Review and Quality Gates"
nav_order: 5
parent: Vibe Kanban Tutorial
---

# Chapter 5: Review and Quality Gates

This chapter defines the human-in-the-loop controls that keep multi-agent output production-ready.

## Learning Goals

- run fast review loops across many agent tasks
- use dev-server checks during handoff
- standardize merge-readiness criteria
- reduce regressions in parallel agent workflows

## Suggested Gate Sequence

1. agent task completion signal on board
2. quick diff and intent review
3. run project validation checks
4. promote to merge-ready state

## Merge-Readiness Checklist

- scope matches original task request
- no hidden destructive changes
- tests/lint/build pass
- reviewer notes are captured for future prompts

## Source References

- [Vibe Kanban README: review and dev server workflow](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#overview)
- [Vibe Kanban Discussions](https://github.com/BloopAI/vibe-kanban/discussions)

## Summary

You now have a high-throughput review model for multi-agent task output.

Next: [Chapter 6: Remote Access and Self-Hosting](06-remote-access-and-self-hosting.md)
