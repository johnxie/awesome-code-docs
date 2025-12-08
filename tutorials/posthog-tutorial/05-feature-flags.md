---
layout: default
title: "Chapter 5: Feature Flags & Experiments"
parent: "PostHog Tutorial"
nav_order: 5
---

# Chapter 5: Feature Flags & Experiments

Roll out features safely and run A/B tests with PostHog flags and experiments.

## Objectives
- Create and evaluate feature flags
- Target cohorts and percentages
- Run experiments and measure lift

## Create a Feature Flag (JS)
```javascript
const newLayout = posthog.isFeatureEnabled('new-layout')
if (newLayout) {
  // render new UI
}
```

- In the UI: Feature Flags → create `new-layout`, rollout 25%, add filter `plan = pro`.

## Experiments
- Define primary metric (e.g., `completed_purchase`)
- Choose exposure (flag) and variants (A/B)
- Run until significance or a minimum sample size

## Guardrails
- Track negative metrics (errors, latency)
- Add kill switch flag for rapid rollback

## Troubleshooting
- Users stuck on old flag: ensure distinct_id stable; clear local cache
- Variant imbalance: check rollout percentages and targeting filters
- Metrics not moving: verify events tied to primary metric

## Performance Notes
- Avoid flag checks inside tight loops
- Cache flag evaluations per session when possible

## Security/Privacy
- Do not expose sensitive logic solely via flags; enforce backend checks for access

## Next Steps
Proceed to Chapter 6 to build dashboards and insights for stakeholders.
