---
layout: default
title: "Chapter 3: Agent Design and Multi-Agent Composition"
nav_order: 3
parent: ADK Python Tutorial
---

# Chapter 3: Agent Design and Multi-Agent Composition

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
