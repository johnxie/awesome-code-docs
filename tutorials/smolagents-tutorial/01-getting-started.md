---
layout: default
title: "Smolagents Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Smolagents Tutorial
---

# Chapter 1: Getting Started with Smolagents

> Install smolagents, configure your model, and run your first lightweight agent.

## Installation

```bash
pip install smolagents            # core
pip install smolagents[all]       # extras: web tools, code exec helpers
```

Environment variables (example):

```bash
HF_API_TOKEN=your-hf-token            # for Hugging Face Inference API
OPENAI_API_KEY=sk-your-key            # if using OpenAI
ANTHROPIC_API_KEY=your-anthropic-key  # if using Anthropic
```

## Your First Agent (CodeAgent)

```python
from smolagents import CodeAgent, HfApiModel

# Default: uses Hugging Face Inference API credentials
model = HfApiModel(model_id="meta-llama/Llama-3.1-8B-Instruct")

agent = CodeAgent(
    tools=[],          # no tools yet
    model=model,
    max_steps=6,       # cap iterations
    verbose=True,      # show reasoning
)

print(agent.run("Calculate 37 * 42, then divide by 7."))
```

## Minimal ToolCallingAgent

```python
from smolagents import ToolCallingAgent, OpenAIServerModel, tool


@tool
def get_greeting(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"


agent = ToolCallingAgent(
    tools=[get_greeting],
    model=OpenAIServerModel(model_id="gpt-4o"),
    max_steps=4,
)

print(agent.run("Greet Alex warmly."))
```

## Quick Tips

- Prefer **CodeAgent** when you want maximum flexibility (the agent can write Python).
- Prefer **ToolCallingAgent** when you need stricter, structured tool calls.
- Set `max_steps` to control cost and runaway loops.
- Use `verbose=True` during development to inspect reasoning.

## Checklist

- [ ] Install smolagents (core or `[all]`)
- [ ] Configure a model provider (HF, OpenAI, Anthropic, LiteLLM)
- [ ] Run a CodeAgent example
- [ ] Enable `verbose` and tune `max_steps`

Next: **[Chapter 2: Understanding Agents](02-understanding-agents.md)** to compare agent types and configurations. 🧠
