---
layout: default
title: "Chapter 6: Daily Operations and Quality Gates"
nav_order: 6
parent: Compound Engineering Plugin Tutorial
---

# Chapter 6: Daily Operations and Quality Gates

This chapter covers daily workflow discipline for teams using compound engineering loops.

## Learning Goals

- run standardized daily workflows with low drift
- apply quality gates at plan, work, and review stages
- capture learnings that improve future cycles
- avoid workflow shortcuts that create long-term regressions

## Daily Runbook

- start with scoped `/workflows:plan`
- execute via `/workflows:work` with explicit task boundaries
- run `/workflows:review` before merge decisions
- close with `/workflows:compound` to retain learnings

## Quality Gate Anchors

- architectural clarity before implementation
- test/behavior confidence before review close
- documented patterns and anti-patterns after each cycle

## Source References

- [Workflow Commands](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md#workflow)
- [Compound Plugin Commands](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/commands)
- [Compounding Plugin README](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md)

## Summary

You now have a repeatable operations loop with built-in quality controls.

Next: [Chapter 7: Troubleshooting and Runtime Maintenance](07-troubleshooting-and-runtime-maintenance.md)
