---
layout: default
title: "Chapter 2: Architecture and Component Topology"
nav_order: 2
parent: Refly Tutorial
---

# Chapter 2: Architecture and Component Topology

This chapter maps Refly's monorepo into runtime responsibilities.

## Learning Goals

- identify the role of `apps/api`, `apps/web`, and shared packages
- understand where skill logic and workflow orchestration live
- trace how shared types/utilities reduce drift across surfaces
- decide where to customize first for your use case

## Core Topology

| Layer | Key Paths | Primary Responsibility |
|:------|:----------|:-----------------------|
| API backend | `apps/api/` | workflow execution, skills, tool integrations |
| web app | `apps/web/` | visual builder and runtime interaction UX |
| CLI | `packages/cli/` | deterministic command-line orchestration |
| skill runtime libs | `packages/skill-template/`, `packages/providers/` | reusable execution and provider abstractions |
| shared foundations | `packages/common-types/`, `packages/stores/`, `packages/utils/` | cross-surface consistency |

## Source References

- [Contributing: Code Structure](https://github.com/refly-ai/refly/blob/main/CONTRIBUTING.md#code-structure)
- [Repository Tree](https://github.com/refly-ai/refly)

## Summary

You now understand the architectural boundaries and extension points in Refly.

Next: [Chapter 3: Workflow Construction and Deterministic Runtime](03-workflow-construction-and-deterministic-runtime.md)
