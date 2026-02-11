---
layout: default
title: "Chapter 7: Advanced Patterns"
nav_order: 7
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 7: Advanced Patterns

This chapter covers the two flagship patterns demonstrated by the official repository.

## Pattern 1: Chat-Supervisor

**Design:**

- fast realtime chat agent handles greeting, small talk, and quick confirmations
- stronger text model supervisor handles complex reasoning and heavy tool usage

**Why it works:**

- preserves responsiveness for routine turns
- provides stronger reasoning where needed
- reduces full-stack migration risk for existing text-agent systems

## Pattern 2: Sequential Handoff

**Design:**

- specialist realtime agents (for example auth, billing, returns) hand off based on intent
- transfer rules are explicit in agent graph configuration

**Why it works:**

- keeps prompts/tools scoped per agent
- reduces instruction collisions
- improves domain-specific accuracy

## Pattern Selection Heuristic

| Need | Best Pattern |
|:-----|:-------------|
| Fast migration from text agent | Chat-Supervisor |
| Clear multi-domain routing | Sequential Handoff |
| High control over specialist behavior | Sequential Handoff |
| Minimal orchestration complexity | Chat-Supervisor |

## Summary

You can now choose and implement the right orchestration pattern for your voice-agent product.

Next: [Chapter 8: Production Deployment](08-production-deployment.md)
