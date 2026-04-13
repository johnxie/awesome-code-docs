---
layout: default
title: "Chapter 2: Section Design and Instruction Quality"
nav_order: 2
parent: AGENTS.md Tutorial
---


# Chapter 2: Section Design and Instruction Quality

Welcome to **Chapter 2: Section Design and Instruction Quality**. In this part of **AGENTS.md Tutorial: Open Standard for Coding-Agent Guidance in Repositories**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers how to write instructions that agents can execute reliably.

## Learning Goals

- choose high-impact section categories
- write deterministic operational instructions
- avoid ambiguous language and hidden assumptions
- make tradeoffs explicit for better agent choices

## High-Signal Sections

- environment/tooling setup expectations
- build/test/lint command requirements
- PR and branching conventions
- safety constraints and prohibited actions

## Source References

- [AGENTS.md README Example](https://github.com/agentsmd/agents.md/blob/main/README.md)
- [AGENTS.md Project Site](https://agents.md)

## Summary

You now understand how section quality directly impacts agent behavior quality.

Next: [Chapter 3: Tool-Agnostic Portability Patterns](03-tool-agnostic-portability-patterns.md)

## Source Code Walkthrough

### `AGENTS.md`

The [`AGENTS.md`](https://github.com/agentsmd/agents.md/blob/HEAD/AGENTS.md) file in the upstream repository is the primary reference for section design. It demonstrates which top-level sections provide the most signal to coding agents — build commands, test commands, code-style rules, and security notes.

Study the section headings and instruction patterns in that file to understand what makes instructions high-quality. The [`README.md`](https://github.com/agentsmd/agents.md/blob/HEAD/README.md) lists common section choices that tool vendors and the community have converged on.
