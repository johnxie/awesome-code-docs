---
layout: default
title: "Chapter 4: Task Planning and Code Generation"
nav_order: 4
parent: Devika Tutorial
---


# Chapter 4: Task Planning and Code Generation

Welcome to **Chapter 4: Task Planning and Code Generation**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter explains how Devika's planner agent decomposes a user prompt into an executable step plan, and how the coder agent transforms each step plus research context into production-ready code files.

## Learning Goals

- understand how the planner agent structures a task into numbered steps with dependencies
- trace how each plan step becomes a coder agent invocation with a bounded context
- identify prompt engineering patterns that improve planning quality and code generation accuracy
- recognize failure modes in task decomposition and apply countermeasures

## Fast Start Checklist

1. submit a small, well-scoped coding task and observe the plan output in the agent log
2. examine the coder prompt template to see how plan steps and research context are assembled
3. review the generated workspace files to verify step-to-file correspondence
4. experiment with prompt phrasing to observe its effect on step count and code quality

## Source References

- [Devika Planner Agent Source](https://github.com/stitionai/devika/tree/main/src/agents/planner)
- [Devika Coder Agent Source](https://github.com/stitionai/devika/tree/main/src/agents/coder)
- [Devika How It Works](https://github.com/stitionai/devika#how-it-works)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)

## Summary

You now understand how Devika converts a natural language task into a structured execution plan and how each plan step drives a focused code generation call with research-enriched context.

Next: [Chapter 5: Web Research and Browser Integration](05-web-research-and-browser-integration.md)

## How These Components Connect

```mermaid
flowchart TD
    A[User task] --> B[Planner agent]
    B --> C[Structured plan with steps]
    C --> D[Coder agent per step]
    D --> E[LLM generates code]
    E --> F[Code written to project workspace]
    F --> G[Action agent runs code]
    G --> H{Success?}
    H -->|Yes| I[Advance to next step]
    H -->|No| J[Debug / retry cycle]
```
