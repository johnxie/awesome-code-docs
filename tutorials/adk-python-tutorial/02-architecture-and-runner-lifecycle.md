---
layout: default
title: "Chapter 2: Architecture and Runner Lifecycle"
nav_order: 2
parent: ADK Python Tutorial
---

# Chapter 2: Architecture and Runner Lifecycle

This chapter explains ADK's execution model so you can reason about behavior under load and during failures.

## Learning Goals

- understand the stateless runner model
- map invocation lifecycle steps end-to-end
- see where sessions, artifacts, and memory fit
- design around event persistence and compaction

## Runner Lifecycle (Mental Model)

1. retrieve session state from session service
2. build invocation context for current turn
3. run agent reason-act loop
4. stream and persist events
5. optionally compact historical events

## Design Implications

- keep agent code deterministic per invocation
- treat persistence services as system boundaries
- design event schemas for observability and replay

## Source References

- [ADK AGENTS Context](https://github.com/google/adk-python/blob/main/AGENTS.md)
- [ADK Architecture Overview](https://github.com/google/adk-python/blob/main/contributing/adk_project_overview_and_architecture.md)
- [ADK Agents Docs](https://google.github.io/adk-docs/agents/)

## Summary

You now understand why ADK runner behavior is reliable when state is externalized and lifecycle boundaries are explicit.

Next: [Chapter 3: Agent Design and Multi-Agent Composition](03-agent-design-and-multi-agent-composition.md)
