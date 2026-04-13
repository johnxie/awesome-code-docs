---
layout: default
title: "Chapter 2: Modes and Task Design"
nav_order: 2
parent: Roo Code Tutorial
---


# Chapter 2: Modes and Task Design

Welcome to **Chapter 2: Modes and Task Design**. In this part of **Roo Code Tutorial: Run an AI Dev Team in Your Editor**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Roo Code's mode system is its core quality-control mechanism. This chapter shows how to choose and sequence modes deliberately.

## Mode Landscape

Roo documentation and project materials cover modes including:

- Code
- Ask
- Architect
- Debug
- Orchestrator
- Custom modes (team-specific)

## Mode Selection Matrix

| Mode | Best For | Avoid Using It For |
|:-----|:---------|:-------------------|
| Ask | quick understanding and codebase questions | large multi-file implementation |
| Architect | decomposition, design proposals, migration planning | immediate low-level patching |
| Code | implementation and scoped refactors | broad strategy decisions |
| Debug | reproduction and root-cause loops | greenfield architecture |
| Orchestrator | coordinating multi-step tasks | low-complexity one-file edits |
| Custom | team/domain workflows | unvalidated generic tasks |

## Mode Transition Pattern

```mermaid
flowchart TD
    A[Ask or Architect] --> B[Plan Approved]
    B --> C[Code Mode Execution]
    C --> D{Failure?}
    D -- Yes --> E[Debug Mode]
    E --> C
    D -- No --> F[Finalize and Summarize]
```

This prevents premature implementation.

## Task Contract Template

Use the same structure in every mode:

```text
Goal:
Mode:
Allowed files:
Forbidden changes:
Validation command:
Definition of done:
```

Mode selection should be explicit in the prompt.

## Designing Custom Modes

Use custom modes when you need repeated domain behavior such as:

- backend API triage
- migration planning
- documentation enforcement
- release note synthesis

Custom mode quality improves when you define:

- narrow responsibilities
- required output format
- prohibited actions
- mandatory validation steps

## Common Mode Anti-Patterns

- using Code mode for unresolved architecture tasks
- running Debug mode without reproducible failing evidence
- switching modes mid-task without preserving constraints
- one custom mode trying to do everything

## Team Mode Policy

Define a simple team policy table:

| Task Class | Allowed Mode(s) | Required Validation |
|:-----------|:----------------|:--------------------|
| bugfix | Debug -> Code | failing + passing test |
| feature | Architect -> Code | unit + integration check |
| refactor | Code | regression-focused tests |
| doc updates | Ask/Custom | link and formatting checks |

This reduces random mode usage.

## Chapter Summary

You now have a mode-driven execution framework that supports:

- deliberate mode choice
- safer transitions between planning and implementation
- reusable custom-mode behavior for teams

Next: [Chapter 3: File and Command Operations](03-file-and-command-operations.md)

## Source Code Walkthrough

Use the following upstream sources to verify mode-related implementation details while reading this chapter:

- [`src/shared/modes.ts`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/src/shared/modes.ts) — defines mode identifiers, slug constants, and the mode registry that drives mode selection behavior in Roo Code.
- [`src/core/prompts/system.ts`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/src/core/prompts/system.ts) — contains the system prompt construction logic used for each mode, showing how mode context shapes agent behavior.

Suggested trace strategy:
- search the `src/shared/modes.ts` file for mode slug definitions and the `ModeConfig` type to understand mode attributes
- compare system prompt differences across modes in `system.ts` to understand capability boundaries
- check `src/extension.ts` for mode-switching entry points triggered from the VS Code UI

## How These Components Connect

```mermaid
flowchart LR
    A[User selects mode] --> B[modes.ts registry]
    B --> C[system.ts prompt builder]
    C --> D[Agent receives mode-scoped context]
```
