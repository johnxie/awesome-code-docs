---
layout: default
title: "Chapter 8: Production Operations and Scaling"
nav_order: 8
parent: VibeSDK Tutorial
---

# Chapter 8: Production Operations and Scaling

This chapter turns VibeSDK from a functional deployment into an operated platform.

## Production Readiness Checklist

- observability enabled for worker and agent paths
- migration and rollback playbook tested
- preview sandbox quotas tuned for expected concurrency
- authentication and secret rotation documented
- incident ownership and escalation paths assigned

## Validation Commands

```bash
bun run lint
bun run typecheck
bun run test
bun run db:migrate:remote
```

## Scaling Focus Areas

| Area | Metric to Track |
|:-----|:----------------|
| Generation pipeline | phase success rate and median completion time |
| Sandbox runtime | startup latency and failure/restart rate |
| Storage layer | D1 query latency and migration error rate |
| Cost profile | per-generated-app compute and token spend |

## Rollout Strategy

1. harden staging with production-like bindings
2. enable gradual tenant/team onboarding
3. capture failure archetypes and automate mitigations
4. iterate model strategy based on observed quality/cost

## Summary

You now have an operations framework for running VibeSDK as a reliable, governed platform at team scale.

Next: return to the [VibeSDK Tutorial index](index.md).
