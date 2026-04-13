---
layout: default
title: "Chapter 2: Architecture and Runner Lifecycle"
nav_order: 2
parent: ADK Python Tutorial
---


# Chapter 2: Architecture and Runner Lifecycle

Welcome to **Chapter 2: Architecture and Runner Lifecycle**. In this part of **ADK Python Tutorial: Production-Grade Agent Engineering with Google's ADK**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Source Code Walkthrough

### `google/adk/runners.py`

The Runner class in [`google/adk/runners.py`](https://github.com/google/adk-python/blob/HEAD/google/adk/runners.py) is the entry point for the architecture covered in this chapter. It wires together the agent, session service, and memory service into the request/response lifecycle. Tracing the `run_async` method shows how events flow from user input through the agent graph and back to the caller, which is the central architectural pattern this chapter explains.