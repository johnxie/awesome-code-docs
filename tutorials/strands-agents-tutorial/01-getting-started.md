---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Strands Agents Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Strands Agents Tutorial: Model-Driven Agent Systems with Native MCP Support**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gets a first Strands agent running with minimal setup.

## Learning Goals

- install Strands SDK and companion tools package
- run a first tool-enabled agent call
- establish a clean local development loop
- avoid common setup mistakes

## Quick Setup Pattern

```bash
python -m venv .venv
source .venv/bin/activate
pip install strands-agents strands-agents-tools
```

Minimal usage:

```python
from strands import Agent
from strands_tools import calculator

agent = Agent(tools=[calculator])
agent("What is the square root of 1764?")
```

## Source References

- [Strands README: Quick Start](https://github.com/strands-agents/sdk-python#quick-start)
- [Strands Python Quickstart Docs](https://strandsagents.com/latest/documentation/docs/user-guide/quickstart/python/)

## Summary

You now have Strands installed with a working first invocation.

Next: [Chapter 2: Agent Loop and Model-Driven Architecture](02-agent-loop-and-model-driven-architecture.md)

## Source Code Walkthrough

Use the following upstream sources to verify getting started details while reading this chapter:

- [`src/strands/agent/agent.py`](https://github.com/strands-agents/sdk-python/blob/HEAD/src/strands/agent/agent.py) — the primary `Agent` class that developers instantiate to run agent loops; this is the entry point for any Strands agent and the first class to understand when getting started.
- [`examples/`](https://github.com/strands-agents/sdk-python/blob/HEAD/examples/) — the official examples directory with minimal working agents demonstrating tool registration, model selection, and basic invocation patterns.

Suggested trace strategy:
- read the `Agent.__init__` signature to understand required and optional parameters (model, tools, system_prompt)
- trace a simple `agent("hello")` call through `agent.py` to see the full invocation path from user input to model response
- check `examples/` for the simplest possible working example to use as a baseline for first runs

## How These Components Connect

```mermaid
flowchart LR
    A[agent = Agent(model, tools)] --> B[agent.py Agent class]
    B --> C[Agent loop invoked with user input]
    C --> D[Model response returned]
```