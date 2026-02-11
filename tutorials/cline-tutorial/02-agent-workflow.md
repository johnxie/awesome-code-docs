---
layout: default
title: "Chapter 2: Agent Workflow"
nav_order: 2
parent: Cline Tutorial
---

# Chapter 2: Agent Workflow

Cline’s strength is its structured task loop, not just raw code generation.

## Typical Loop

1. understand request and gather context
2. propose targeted actions
3. request permission for execution/editing
4. apply changes and run validation
5. summarize results and next steps

## Human-in-the-Loop Model

The approval layer is a core safety feature, especially when commands or edits can have broad side effects.

## Prompt Engineering for Workflow Quality

Use prompts with:

- explicit scope (files/modules)
- acceptance criteria
- validation command
- non-goals

This reduces overreach and improves review quality.

## Workflow Anti-Patterns

- large vague tasks with no acceptance test
- skipping approval review under pressure
- no rollback point before risky changes

## Summary

You can now drive Cline through a repeatable and auditable agent workflow.

Next: [Chapter 3: File Editing and Diffs](03-file-editing-and-diffs.md)
