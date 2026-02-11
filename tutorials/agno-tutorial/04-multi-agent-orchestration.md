---
layout: default
title: "Chapter 4: Multi-Agent Orchestration"
nav_order: 4
parent: Agno Tutorial
---

# Chapter 4: Multi-Agent Orchestration

Multi-agent systems need explicit role and handoff boundaries to remain reliable.

## Orchestration Pattern

| Role | Responsibility |
|:-----|:---------------|
| coordinator | route tasks and manage execution state |
| specialist agents | domain-specific reasoning and tool usage |
| reviewer/guard | quality and policy enforcement |

## Handoff Guidance

- pass only required context to each specialist
- log handoff reason and result
- enforce max handoff depth per request

## Source References

- [Agno First Multi-Agent System](https://docs.agno.com/first-multi-agent-system)
- [Agno Docs](https://docs.agno.com)

## Summary

You now have a practical pattern for building coherent Agno multi-agent teams.

Next: [Chapter 5: Knowledge, RAG, and Tools](05-knowledge-rag-and-tools.md)
