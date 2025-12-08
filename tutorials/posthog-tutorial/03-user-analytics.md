---
layout: default
title: "Chapter 3: User Analytics & Funnels"
parent: "PostHog Tutorial"
nav_order: 3
---

# Chapter 3: User Analytics & Funnels

Understand user behavior, conversion, and retention with PostHog insights.

## Objectives
- Build funnels for core flows
- Analyze cohorts and retention
- Track user journeys end-to-end

## Funnels
- Define steps as ordered events (e.g., `visited_pricing` → `started_checkout` → `completed_purchase`)
- Segment by plan, device, referrer
- Use breakdowns to spot drop-off by cohort

## Journeys (Paths)
- Visualize paths users take before/after key events
- Filter by cohort or property (e.g., `plan = pro`)

## Retention
- Choose returning event (e.g., `app_opened`)
- View retention curves by week/month
- Tag experiments/flags to compare cohorts

## Example: Create a Funnel (UI steps)
1) Insights → Funnels → New funnel
2) Add steps: `signed_up`, `created_project`, `invited_teammate`
3) Breakdown by `plan` and `referrer`
4) Save and add to dashboard

## Troubleshooting
- Sparse funnels: ensure events fire on all platforms; verify distinct_id consistency
- Retention flat: double-check returning event definition
- Paths noisy: add minimum edge weights; filter internal traffic

## Performance Notes
- Keep event/property cardinality reasonable
- Use sampling only for exploratory analysis, not critical funnels

## Security/Privacy
- Anonymize IP if required; respect regional data policies
- Exclude internal traffic via filters

## Next Steps
In Chapter 4, capture session recordings for qualitative insights.
