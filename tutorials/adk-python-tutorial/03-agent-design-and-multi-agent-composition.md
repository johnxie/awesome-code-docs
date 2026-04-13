---
layout: default
title: "Chapter 3: Agent Design and Multi-Agent Composition"
nav_order: 3
parent: ADK Python Tutorial
---


# Chapter 3: Agent Design and Multi-Agent Composition

Welcome to **Chapter 3: Agent Design and Multi-Agent Composition**. In this part of **ADK Python Tutorial: Production-Grade Agent Engineering with Google's ADK**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers how to structure ADK agents for maintainability and collaboration.

## Learning Goals

- define clean single-agent boundaries
- compose sub-agents with clear responsibilities
- choose `Agent` vs app pattern intentionally
- design instructions and tool scope for reliability

## Composition Strategies

- use specialist sub-agents for narrow tasks
- keep a coordinator agent focused on routing decisions
- limit tool sets per agent to reduce accidental behavior
- enforce stable directory conventions for discoverability

## Recommended Structure

- `my_agent/__init__.py` exports the agent entry
- `my_agent/agent.py` defines `root_agent` or `app`
- instructions and tool contracts stay modular and testable

## Source References

- [ADK README: Multi-Agent Example](https://github.com/google/adk-python/blob/main/README.md#define-a-multi-agent-system)
- [ADK Multi-Agent Docs](https://google.github.io/adk-docs/agents/multi-agents/)
- [ADK AGENTS.md Structure Convention](https://github.com/google/adk-python/blob/main/AGENTS.md)

## Summary

You can now build multi-agent ADK systems with clearer separation of concerns.

Next: [Chapter 4: Tools, MCP, and Confirmation Flows](04-tools-mcp-and-confirmation-flows.md)

## Source Code Walkthrough

### `google/adk/agents/llm_agent.py`

The [`google/adk/agents/llm_agent.py`](https://github.com/google/adk-python/blob/HEAD/google/adk/agents/llm_agent.py) file defines the core `LlmAgent` class that all LLM-backed agents extend. It shows how agents declare tools, sub-agents, and system instructions — the building blocks of multi-agent composition. The `sub_agents` field and delegation logic are directly relevant to the composition patterns described in this chapter.