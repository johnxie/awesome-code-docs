---
layout: default
title: "Chapter 6: Context Variables"
parent: "OpenAI Swarm Tutorial"
nav_order: 6
---

# Chapter 6: Context Variables

Manage shared state across agents to keep conversations coherent.

## Objectives
- Define and update context variables
- Avoid stale or oversized context
- Share only what downstream agents need

## Example
```python
context = {
  "user_intent": "billing",
  "account_id": "123",
  "summary": "User needs invoice copy"
}
```

- Pass context with handoffs
- Prune unused keys regularly

## Troubleshooting
- Oversized context: trim histories; keep summaries short
- Missing data: validate required keys before handoff

## Next Steps
Chapter 7 explores multi-agent orchestration patterns.
