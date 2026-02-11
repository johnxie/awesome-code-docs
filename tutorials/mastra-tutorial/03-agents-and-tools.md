---
layout: default
title: "Chapter 3: Agents and Tools"
nav_order: 3
parent: Mastra Tutorial
---

# Chapter 3: Agents and Tools

Agents are most useful when tool boundaries are explicit and observable.

## Agent Design Pattern

| Step | Action |
|:-----|:-------|
| define objective | clear role and expected output |
| constrain tools | only required tools per agent |
| enforce schema | typed input/output contracts |
| log behavior | action-level traces for debugging |

## Tool Safety Practices

- validate inputs and authorization before execution
- return structured results instead of free-form text
- classify tools by side-effect risk
- enforce timeout and retry policy

## Source References

- [Mastra Agents Docs](https://mastra.ai/docs/agents/overview)
- [Mastra Model Routing](https://mastra.ai/models)

## Summary

You now have a practical framework for building strong, bounded agents in Mastra.

Next: [Chapter 4: Workflows and Control Flow](04-workflows-and-control-flow.md)
