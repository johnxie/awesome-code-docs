---
layout: default
title: "Chapter 5: Autonomous Coding Agents"
nav_order: 5
parent: Claude Quickstarts Tutorial
---

# Chapter 5: Autonomous Coding Agents

Autonomous coding quickstarts work best when planning and execution are separated.

## Two-Agent Baseline

- **Planner/Initializer**: clarifies objective, constraints, acceptance criteria
- **Executor/Coder**: performs edits, runs tests, reports concrete outcomes

This split reduces context confusion and improves handoff quality.

## Checkpointed Workflow

Use explicit checkpoints after meaningful work units:

1. expected outcome
2. files changed
3. tests run and result
4. unresolved risks
5. next step

Store checkpoints in version control or task state files so runs can resume reliably.

## Autonomous Loop Pattern

```text
plan -> edit -> test -> summarize diff -> checkpoint -> continue or stop
```

Stop conditions should be explicit:

- acceptance criteria met
- blocking test failures
- unsafe/conflicting instructions

## Quality Controls

| Control | Purpose |
|:--------|:--------|
| Required tests per checkpoint | Prevent hidden regressions |
| Diff summary requirement | Improve reviewability |
| Policy checks before merge | Enforce org standards |
| Max iteration budget | Prevent runaway loops |

## Common Failure Modes

- planning omitted, leading to aimless edits
- too many edits before first test run
- missing rollback strategy for failed experiments

## Summary

You can now design autonomous coding flows that are resumable, test-driven, and reviewable.

Next: [Chapter 6: Production Patterns](06-production-patterns.md)
