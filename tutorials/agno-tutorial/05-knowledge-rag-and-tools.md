---
layout: default
title: "Chapter 5: Knowledge, RAG, and Tools"
nav_order: 5
parent: Agno Tutorial
---

# Chapter 5: Knowledge, RAG, and Tools

Agno agents combine tool execution and knowledge retrieval to produce grounded, high-utility outputs.

## Augmentation Surfaces

| Surface | Value |
|:--------|:------|
| vector/RAG retrieval | domain grounding |
| toolkits | external action and system interaction |
| guardrails | safe execution boundaries |

## Operational Rules

- treat tool calls as policy-governed actions
- track retrieval quality and stale context rates
- ensure typed contracts for tool inputs/outputs

## Source References

- [Agno Features](https://github.com/agno-agi/agno)
- [Agno Docs](https://docs.agno.com)

## Summary

You now understand how to combine knowledge and tool layers in Agno without sacrificing reliability.

Next: [Chapter 6: AgentOS Runtime and Control Plane](06-agentos-runtime-and-control-plane.md)
