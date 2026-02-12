---
layout: default
title: "Chapter 4: Commands, Natural Language, and Workflow Orchestration"
nav_order: 4
parent: Wshobson Agents Tutorial
---

# Chapter 4: Commands, Natural Language, and Workflow Orchestration

This chapter covers the two primary interfaces and when to use each.

## Learning Goals

- apply slash commands for deterministic task execution
- use natural language when agent reasoning is more useful
- compose multi-step workflows safely
- improve reproducibility of complex runs

## Command-First Pattern

Use commands when you need explicit behavior and arguments:

```bash
/full-stack-orchestration:full-stack-feature "user dashboard with analytics"
/security-scanning:security-hardening --level comprehensive
```

Benefits:

- predictable execution path
- clear argument contract
- easier runbook reuse across team members

## Natural-Language Pattern

Use NL when you want dynamic agent selection:

- "Use backend-architect and security-auditor to review this auth flow."

Benefits:

- faster ideation for exploratory tasks
- less command memorization overhead

## Hybrid Workflow

- start with command scaffold
- refine with natural-language follow-ups
- finish with explicit review command for quality gates

## Source References

- [Usage Guide](https://github.com/wshobson/agents/blob/main/docs/usage.md)
- [README Popular Use Cases](https://github.com/wshobson/agents/blob/main/README.md#popular-use-cases)

## Summary

You now have a balanced command/NL operating model for reliable multi-agent workflows.

Next: [Chapter 5: Agents, Skills, and Model Tier Strategy](05-agents-skills-and-model-tier-strategy.md)
