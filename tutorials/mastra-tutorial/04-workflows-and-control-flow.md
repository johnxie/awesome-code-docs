---
layout: default
title: "Chapter 4: Workflows and Control Flow"
nav_order: 4
parent: Mastra Tutorial
---

# Chapter 4: Workflows and Control Flow

Mastra workflows provide deterministic orchestration when autonomous loops are not enough.

## Workflow Controls

| Control | Use Case |
|:--------|:---------|
| `.then()` | linear stage execution |
| `.branch()` | conditional routing |
| `.parallel()` | independent concurrent tasks |
| suspend/resume | human approval or async wait states |

## Decision Rule

Use workflows when you need strict ordering, approvals, or compliance constraints.

## Production Pattern

1. agent drafts plan
2. workflow runs approval gates
3. tools execute with policy checks
4. workflow commits output and telemetry

## Source References

- [Mastra Workflows Docs](https://mastra.ai/docs/workflows/overview)
- [Suspend and Resume](https://mastra.ai/docs/workflows/suspend-and-resume)

## Summary

You now know when and how to move from free-form agents to deterministic workflow control.

Next: [Chapter 5: Memory, RAG, and Context](05-memory-rag-and-context.md)
