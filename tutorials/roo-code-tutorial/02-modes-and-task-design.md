---
layout: default
title: "Chapter 2: Modes and Task Design"
nav_order: 2
parent: Roo Code Tutorial
---

# Chapter 2: Modes and Task Design

Roo Code’s mode system is a core differentiator for workflow control.

## Mode Semantics

- **Code**: direct implementation and edits
- **Architect**: planning, system design, migration maps
- **Ask**: fast explanations and scoped Q&A
- **Debug**: failure diagnosis and remediation loops
- **Custom**: team-specific specialist behavior

## Mode Selection Heuristic

| Task Type | Recommended Mode |
|:----------|:-----------------|
| implement feature | Code |
| design refactor plan | Architect |
| explain unfamiliar subsystem | Ask |
| reproduce and fix failures | Debug |
| repeated domain workflow | Custom |

## Prompt Design by Mode

Define inputs and acceptance criteria differently per mode so the model does not overreach.

## Summary

You can now choose and apply modes deliberately to improve output quality and reduce wasted cycles.

Next: [Chapter 3: File and Command Operations](03-file-and-command-operations.md)
