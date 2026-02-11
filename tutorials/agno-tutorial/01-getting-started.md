---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Agno Tutorial
---

# Chapter 1: Getting Started

This chapter gets your first Agno agent running with persistent storage and learning enabled.

## Learning Goals

- create and run a first Agno agent
- enable storage-backed memory behavior
- validate learning mode and session continuity
- confirm model connectivity

## Minimal Example

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=SqliteDb(db_file="tmp/agents.db"),
    learning=True,
)
```

## First Validation Checklist

1. initial response succeeds
2. follow-up recalls prior context
3. persisted state survives process restart
4. logs show expected execution path

## Source References

- [Agno First Agent](https://docs.agno.com/first-agent)
- [Agno Repository](https://github.com/agno-agi/agno)

## Summary

You now have an Agno baseline with persistent memory and learning enabled.

Next: [Chapter 2: Framework Architecture](02-framework-architecture.md)
