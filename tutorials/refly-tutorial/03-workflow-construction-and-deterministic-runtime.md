---
layout: default
title: "Chapter 3: Workflow Construction and Deterministic Runtime"
nav_order: 3
parent: Refly Tutorial
---

# Chapter 3: Workflow Construction and Deterministic Runtime

This chapter focuses on constructing workflows that remain stable under real operational pressure.

## Learning Goals

- build workflows from intent while preserving deterministic behavior
- validate graph logic before execution
- use state transitions to avoid accidental invalid runs
- design workflows for recovery and reuse

## Builder-Oriented Loop

1. start workflow construction (visual or CLI builder)
2. define nodes, dependencies, and variable contracts
3. validate structure before commit/run
4. run with explicit input and inspect status/output
5. iterate with small deltas and versioned changes

## Determinism Signals

| Signal | Why It Matters |
|:-------|:---------------|
| DAG validation | prevents cycle-based runtime failures |
| explicit state transitions | reduces partial/invalid commits |
| JSON-first outputs | improves machine readability and automation |
| versioned skills | enables safe reuse and rollback |

## Source References

- [README: Core Capabilities](https://github.com/refly-ai/refly/blob/main/README.md#core-capabilities)
- [README: Create Your First Workflow](https://github.com/refly-ai/refly/blob/main/README.md#create-your-first-workflow)
- [CLI README](https://github.com/refly-ai/refly/blob/main/packages/cli/README.md)

## Summary

You now have a practical pattern for building stable workflows and iterating safely.

Next: [Chapter 4: API and Webhook Integrations](04-api-and-webhook-integrations.md)
