---
layout: default
title: "Chapter 8: Production Operations"
nav_order: 8
parent: Bolt.diy Tutorial
---

# Chapter 8: Production Operations

This chapter closes with the controls needed to run bolt.diy as a production service.

## Production Baseline

- environment-specific config and secret rotation
- provider usage and token-cost observability
- incident runbooks for provider/tool failures
- staged rollout plus rollback procedures

## Key Metrics

| Metric | Operational Value |
|:-------|:------------------|
| generation success rate | platform reliability trend |
| retry/failure distribution | weak provider or prompt patterns |
| diff acceptance ratio | output quality signal |
| median task completion time | user experience and throughput |

## Governance Controls

- mandatory review for high-risk files
- retention/redaction policy for logs and prompts
- role-scoped admin access for provider settings
- regular disaster-recovery and failover drills

## Incident Playbook Essentials

| Incident Type | First Response |
|:--------------|:---------------|
| provider outage | force fallback provider profile |
| malformed generation spike | tighten prompt policy and review gates |
| cost anomaly | cap usage and inspect model routing logs |
| deployment failure | revert to last known good release artifact |

## Final Summary

You now have end-to-end coverage for operating bolt.diy from local iteration to production governance.

Related:
- [Dyad Tutorial](../dyad-tutorial/)
- [Vercel AI SDK Tutorial](../vercel-ai-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
