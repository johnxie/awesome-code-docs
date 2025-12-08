---
layout: default
title: "Chapter 5: Agent Handoffs"
parent: "OpenAI Swarm Tutorial"
nav_order: 5
---

# Chapter 5: Agent Handoffs

Transfer control between agents seamlessly with context.

## Objectives
- Trigger handoffs based on intent
- Preserve context variables
- Confirm ownership after handoff

## Example Handoff
```python
from swarm import Swarm

client = Swarm()
conversation = client.run(
    agent=triage,
    messages=[{"role": "user", "content": "I need billing help"}],
)
# triage hands off to billing agent based on intent
```

## Context Variables
- Include user info, latest summary, relevant tool outputs
- Keep context small; drop stale keys

## Tips
- Log handoff reasons; audit later
- Provide brief recap when handing off

## Next Steps
Chapter 6 manages shared state with context variables.
