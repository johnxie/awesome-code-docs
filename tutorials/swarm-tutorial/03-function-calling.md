---
layout: default
title: "Chapter 3: Function Calling & Tools"
parent: "OpenAI Swarm Tutorial"
nav_order: 3
---

# Chapter 3: Function Calling & Tools

Equip agents with tools using OpenAI function calling.

## Objectives
- Register tools/functions
- Route calls via Swarm
- Handle tool errors safely

## Define Functions
```python
def get_order_status(order_id: str):
    return {"order_id": order_id, "status": "shipped"}
```

## Wire into Agent
```python
from swarm import Agent

support = Agent(
    name="Support",
    instructions="Help users with orders.",
    functions=[get_order_status],
)
```

## Error Handling Tips
- Validate inputs inside functions
- Return structured JSON; avoid free text
- Add retries around flaky APIs

## Next Steps
Chapter 4 introduces routines for reusable sequences.
