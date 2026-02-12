---
layout: default
title: "Chapter 5: Agents, Skills, and Model Tier Strategy"
nav_order: 5
parent: Wshobson Agents Tutorial
---

# Chapter 5: Agents, Skills, and Model Tier Strategy

This chapter explains how specialists, skill packs, and model assignment combine to shape output quality and cost.

## Learning Goals

- understand agent category coverage and specialization
- use skills for progressive-disclosure knowledge loading
- reason about model-tier assignment tradeoffs
- tune workflows for quality/cost targets

## Agent + Skill Interaction

- agents provide execution persona and task behavior
- skills inject narrow, high-value domain knowledge on demand
- plugin boundaries keep activation surfaces focused

## Model Tier Strategy

The project documents tiered model use across high-criticality and fast operational tasks.

Practical heuristic:

- critical architecture/security decisions: strongest model tier
- implementation-heavy but bounded tasks: balanced tier
- deterministic operational tasks: cost-efficient tier

## Operational Checklist

- verify agent choice before long runs
- ensure relevant skill triggers are present in prompts
- re-run sensitive workflows with review-oriented agents
- track token/cost patterns by plugin profile

## Source References

- [Agent Reference](https://github.com/wshobson/agents/blob/main/docs/agents.md)
- [Agent Skills Guide](https://github.com/wshobson/agents/blob/main/docs/agent-skills.md)
- [README Model Strategy](https://github.com/wshobson/agents/blob/main/README.md#three-tier-model-strategy)

## Summary

You now understand how to combine specialists, skills, and model strategy for better outcomes.

Next: [Chapter 6: Multi-Agent Team Patterns and Production Workflows](06-multi-agent-team-patterns-and-production-workflows.md)
