---
layout: default
title: "Chapter 4: Agents and Assistants"
nav_order: 4
parent: OpenAI Python SDK Tutorial
---

# Chapter 4: Agents and Assistants

This chapter focuses on transition strategy: operate existing assistants safely while moving toward current agent-platform patterns.

## Current State

- Assistants API is still usable in many systems.
- OpenAI platform docs indicate a target sunset timeline around **August 26, 2026**.
- New projects should evaluate Responses API + Agents patterns first.

## Existing Assistants Workflow (Legacy/Transition)

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    model="gpt-5.2",
    name="Ops Assistant",
    instructions="Help with reliability planning and incident response."
)

thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Draft a rollback checklist for a risky deployment."
)
```

## Migration Playbook

1. catalog Assistants API usage and tool dependencies
2. extract shared prompt/tool contracts
3. rebuild core flows on Responses/Agents primitives
4. run side-by-side output comparisons
5. cut over service by service

## Risk Controls During Migration

- avoid broad rewrites in one release
- pin SDK versions per service
- keep rollback path to known-good behavior
- monitor quality regressions with fixed eval sets

## Summary

You can now manage assistant-era systems while executing a controlled migration plan.

Next: [Chapter 5: Batch Processing](05-batch-processing.md)
