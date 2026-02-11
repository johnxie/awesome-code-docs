---
layout: default
title: "Chapter 8: Production Operations and Scaling"
nav_order: 8
parent: VibeSDK Tutorial
---

# Chapter 8: Production Operations and Scaling

This chapter turns VibeSDK from a demo deployment into an operated platform.

## Production Readiness Checklist

- worker and agent observability enabled
- migration rollback path tested
- sandbox capacity tuned for expected concurrency
- auth/token rotation process documented
- incident ownership and paging defined

## Validation Commands

```bash
bun run lint
bun run typecheck
bun run test
bun run db:migrate:remote
```

## Scaling Metrics

| Area | Track |
|:-----|:------|
| generation pipeline | completion rate and median end-to-end time |
| sandbox runtime | startup latency and restart/failure rate |
| storage | D1 query latency and migration error rate |
| cost | compute + model spend per generated app |

## Rollout Strategy

1. validate in staging with production-like bindings
2. onboard teams gradually by policy tier
3. automate mitigation for top recurring failure classes
4. tune model routing from observed quality/cost outcomes

## Incident Taxonomy

| Incident Class | First Action |
|:---------------|:-------------|
| provider outage | fail over to validated backup model route |
| sandbox instability | lower concurrency and isolate bad workloads |
| migration regression | stop rollout and restore last known good schema |
| auth/policy failure | revoke exposed tokens and reapply baseline policy |

## Summary

You now have an operational model for running VibeSDK at team and enterprise scale.

Next: return to the [VibeSDK Tutorial index](index.md).
