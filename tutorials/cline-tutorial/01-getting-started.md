---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Cline Tutorial
---

# Chapter 1: Getting Started

This chapter sets up Cline in VS Code and validates a safe first engineering loop.

## Prerequisites

| Requirement | Why It Matters |
|:------------|:---------------|
| VS Code (or compatible fork) | Cline runs as an editor extension |
| model provider keys | powers reasoning, planning, and tool decisions |
| sandbox repository | lets you validate behavior before real projects |

## Installation and First Configuration

1. install Cline from the VS Code marketplace
2. configure provider/API settings in extension preferences
3. open a small repository with passing tests
4. keep manual approvals enabled for edits and commands

## First Task Pattern

Use a bounded, auditable prompt:

```text
Analyze module X, refactor function Y for readability,
run npm test -- module-z, and summarize changed files.
```

This validates analysis, edit, command execution, and reporting in one pass.

## Initial Verification Checklist

- Cline can read and summarize relevant files
- proposed edits appear in explicit diffs before write
- command output is captured and attached to the task
- final summary includes files changed + validation status

## Common Early Issues

| Symptom | Fix |
|:--------|:----|
| broad, noisy edits | tighten prompt scope and acceptance criteria |
| repeated command retries | specify canonical command and timeout expectations |
| weak summaries | require explicit final format in your prompt |

## Summary

You now have Cline installed with a controlled first-task baseline.

Next: [Chapter 2: Agent Workflow](02-agent-workflow.md)
