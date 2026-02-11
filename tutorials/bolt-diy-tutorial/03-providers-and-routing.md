---
layout: default
title: "Chapter 3: Providers and Model Routing"
nav_order: 3
parent: Bolt.diy Tutorial
---

# Chapter 3: Providers and Model Routing

Provider flexibility is a core bolt.diy advantage, but it needs explicit policy.

## Routing Strategy by Task Class

| Task Type | Preferred Model Tier |
|:----------|:---------------------|
| scaffolding and low-risk refactor | fast/low-cost models |
| architecture or complex debugging | stronger reasoning models |
| privacy-sensitive iteration | local/self-hosted models |

## Configuration Modes

- environment-based secrets for CI and production
- UI-based key switching for local exploration
- hybrid mode with explicit default + fallback paths

## Guardrails

| Risk | Control |
|:-----|:--------|
| credential leakage | secrets management and no hardcoded keys |
| wrong fallback behavior | explicit provider priority rules |
| cost spikes | per-session budgets and usage review |

## Operational Tip

Standardize one team default provider profile, then allow opt-in overrides for special workloads.

## Fallback Planning

Keep an explicit fallback order documented and tested:

1. preferred primary provider/model
2. lower-cost secondary for non-critical tasks
3. local/self-hosted fallback for outage or policy events

This avoids emergency reconfiguration during incidents.

## Summary

You can now treat model routing as a managed engineering policy rather than ad hoc settings changes.

Next: [Chapter 4: Prompt-to-App Workflow](04-prompt-to-app-workflow.md)
