---
layout: default
title: "Chapter 8: Production Operations"
nav_order: 8
parent: Bolt.diy Tutorial
---

# Chapter 8: Production Operations

This chapter finalizes bolt.diy with production reliability, security, and governance patterns.

## Operations Baseline

- environment-specific configuration profiles
- centralized secrets and key rotation
- usage monitoring (token/cost/provider mix)
- incident runbooks for provider outages or malformed generations

## Observability Baseline

Track:

- request latency by provider/model
- generation failure and retry rates
- diff rejection vs acceptance rates
- deployment and integration error classes

## Governance Baseline

| Area | Control |
|:-----|:--------|
| change safety | mandatory diff review for high-risk files |
| data security | redaction and retention policy for logs |
| access | role-scoped admin/provider controls |
| release | staged rollout and rollback procedures |

## Final Summary

You now have end-to-end coverage for running bolt.diy from local experiments to production-grade operations.

Related:
- [Dyad Tutorial](../dyad-tutorial/)
- [Vercel AI SDK Tutorial](../vercel-ai-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
