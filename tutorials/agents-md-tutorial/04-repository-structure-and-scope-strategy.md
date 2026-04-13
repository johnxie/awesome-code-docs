---
layout: default
title: "Chapter 4: Repository Structure and Scope Strategy"
nav_order: 4
parent: AGENTS.md Tutorial
---


# Chapter 4: Repository Structure and Scope Strategy

Welcome to **Chapter 4: Repository Structure and Scope Strategy**. In this part of **AGENTS.md Tutorial: Open Standard for Coding-Agent Guidance in Repositories**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on scoping AGENTS.md guidance in complex repositories.

## Learning Goals

- define root-level guidance clearly
- handle subproject-specific overrides safely
- reduce conflicts in monorepos
- keep ownership boundaries explicit

## Scope Patterns

- root AGENTS.md for global policies
- subdirectory AGENTS.md where workflows diverge
- explicit precedence and conflict-resolution rules

## Source References

- [AGENTS.md Standard Repository](https://github.com/agentsmd/agents.md)
- [AGENTS.md Website](https://agents.md)

## Summary

You now can scale AGENTS.md patterns from small repos to monorepos.

Next: [Chapter 5: Testing, Linting, and CI Alignment](05-testing-linting-and-ci-alignment.md)

## Source Code Walkthrough

### `AGENTS.md`

Repository structure and scope decisions are visible in the [`AGENTS.md`](https://github.com/agentsmd/agents.md/blob/HEAD/AGENTS.md) specification itself. The file lives at the repository root, which is the standard location agents look for first. The specification notes that sub-directory AGENTS.md files override or extend the root file for narrower scopes — observe how the root file deliberately keeps scope broad enough to serve the whole project.

Cross-reference the upstream repo’s directory layout with the guidance in the root `AGENTS.md` to see how structure and scope choices interact in a real project.
