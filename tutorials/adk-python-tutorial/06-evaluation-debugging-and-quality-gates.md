---
layout: default
title: "Chapter 6: Evaluation, Debugging, and Quality Gates"
nav_order: 6
parent: ADK Python Tutorial
---


# Chapter 6: Evaluation, Debugging, and Quality Gates

Welcome to **Chapter 6: Evaluation, Debugging, and Quality Gates**. In this part of **ADK Python Tutorial: Production-Grade Agent Engineering with Google's ADK**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter shows how to harden ADK behavior with repeatable evaluation workflows.

## Learning Goals

- run ADK evaluation commands against test sets
- instrument debugging in runner and tool paths
- detect regressions before release
- define release gates for agent quality

## Evaluation Workflow

1. create representative evaluation sets
2. run `adk eval` in CI and locally
3. inspect failures by event trace and tool outputs
4. block release when quality thresholds fail

## Source References

- [ADK README: Evaluate Agents](https://github.com/google/adk-python/blob/main/README.md#--evaluate-agents)
- [ADK Evaluate Docs](https://google.github.io/adk-docs/evaluate/)
- [ADK Testing Guidance](https://github.com/google/adk-python/blob/main/CONTRIBUTING.md)

## Summary

You now have a quality loop that makes ADK systems safer to evolve.

Next: [Chapter 7: Deployment and Production Operations](07-deployment-and-production-operations.md)

## Source Code Walkthrough

### `google/adk/evaluation/`

The evaluation framework lives in [`google/adk/evaluation/`](https://github.com/google/adk-python/tree/HEAD/google/adk/evaluation). This module contains the evaluator classes and dataset formats used for agent quality testing. Reviewing the evaluation module alongside the `contributing/samples/runner_debug_example/` sample shows how to run an agent against a test set and validate its outputs — the core quality gate workflow described in Chapter 6.