---
layout: default
title: "Chapter 7: Advanced Patterns"
nav_order: 7
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 7: Advanced Patterns

This chapter covers the two flagship orchestration patterns from the official repository and when to use each.

## Learning Goals

By the end of this chapter, you should be able to:

- implement chat-supervisor architecture intentionally
- implement sequential specialist handoff architecture
- choose pattern based on operational constraints
- avoid common multi-agent orchestration failures

## Pattern 1: Chat-Supervisor

### Design

- a fast realtime front agent handles immediate user interaction
- a stronger reasoning-focused backend agent handles complex planning/tool decisions

### Benefits

- preserves responsiveness on routine turns
- enables deeper reasoning only when needed
- helps teams migrate from text-agent systems incrementally

### Risks

- cross-agent state drift if context handoff is sloppy
- over-routing to supervisor increases latency and cost

## Pattern 2: Sequential Handoff

### Design

- specialist realtime agents own distinct domains (for example billing, support, auth)
- explicit transfer rules route conversations across specialists

### Benefits

- tighter prompts and tools per domain
- clearer ownership and easier debugging
- lower instruction collisions

### Risks

- too many specialists increase routing complexity
- weak handoff contracts can create repetitive clarification loops

## Decision Matrix

| Constraint | Prefer Chat-Supervisor | Prefer Sequential Handoff |
|:-----------|:-----------------------|:--------------------------|
| migrating from a strong text agent | yes | maybe |
| strict domain boundaries | maybe | yes |
| minimal orchestration complexity | yes | no |
| high specialist compliance requirements | no | yes |

## Operational Guardrails

- define explicit handoff contracts (what context transfers)
- log handoff reasons and outcomes for every transfer
- cap max handoff depth per conversation
- add fallback to a generalist recovery path

## Source References

- [openai/openai-realtime-agents Repository](https://github.com/openai/openai-realtime-agents)
- [OpenAI Agents JavaScript SDK](https://github.com/openai/openai-agents-js)

## Summary

You now have a practical framework for choosing and operating multi-agent realtime orchestration patterns.

Next: [Chapter 8: Production Deployment](08-production-deployment.md)
