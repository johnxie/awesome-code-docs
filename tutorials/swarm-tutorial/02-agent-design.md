---
layout: default
title: "Chapter 2: Agent Design"
parent: "OpenAI Swarm Tutorial"
nav_order: 2
---

# Chapter 2: Agent Design

Define Swarm agents with clear instructions, behaviors, and tools.

## Objectives
- Create agents with personas and goals
- Attach tools and routines
- Control verbosity and style

## Basic Agent
```python
from swarm import Agent

triage = Agent(
    name="Triage",
    instructions="Route requests to the right specialist; be concise.",
)
```

## Adding Tools
```python
def lookup_customer(name: str):
    return {"name": name, "status": "gold"}

support = Agent(
    name="Support",
    instructions="Resolve product issues.",
    functions=[lookup_customer],
)
```

## Tips
- Keep instructions short; add examples
- Limit tools per agent to reduce misuse

## Next Steps
Proceed to Chapter 3 for function calling and tool wiring.
