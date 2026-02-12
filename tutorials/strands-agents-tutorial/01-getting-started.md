---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Strands Agents Tutorial
---

# Chapter 1: Getting Started

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
