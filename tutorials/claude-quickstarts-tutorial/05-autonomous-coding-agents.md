---
layout: default
title: "Chapter 5: Autonomous Coding Agents"
nav_order: 5
parent: Claude Quickstarts Tutorial
---

# Chapter 5: Autonomous Coding Agents

Coding quickstarts show how to combine planning, execution, and persistence across sessions.

## Two-Agent Pattern

- **Initializer agent**: clarifies goals and constraints.
- **Coding agent**: implements changes and tests them.

## Persistence Strategy

- Store progress in git commits/branches.
- Keep machine-readable task state.
- Resume work from explicit checkpoints.

## Quality Controls

- run tests before each checkpoint
- require diff summaries
- block merges on failing validations

## Summary

You can now design persistent coding-agent flows with practical guardrails.

Next: [Chapter 6: Production Patterns](06-production-patterns.md)
