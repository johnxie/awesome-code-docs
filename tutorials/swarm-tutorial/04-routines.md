---
layout: default
title: "Chapter 4: Routines"
parent: "OpenAI Swarm Tutorial"
nav_order: 4
---

# Chapter 4: Routines

Create reusable sequences of actions that agents can execute.

## Objectives
- Define routines for common tasks
- Reuse routines across agents
- Manage inputs/outputs

## Example Routine
```python
from swarm import Routine

collect_info = Routine(
    name="collect_info",
    description="Gather user context before handoff",
    steps=["ask_issue", "ask_account", "summarize"],
)
```

## Using Routines
```python
triage.routines = [collect_info]
```

## Tips
- Keep routines small and composable
- Include summaries for downstream agents

## Next Steps
Chapter 5 covers handoffs between agents.
