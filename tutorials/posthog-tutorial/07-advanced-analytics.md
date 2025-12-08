---
layout: default
title: "Chapter 7: Advanced Analytics"
parent: "PostHog Tutorial"
nav_order: 7
---

# Chapter 7: Advanced Analytics

Use cohorts, custom SQL, and data pipelines for deeper insights.

## Objectives
- Build cohorts and advanced segments
- Write SQL insights for custom metrics
- Export data to warehouses for modeling

## Cohorts
- Build cohorts from events (e.g., "users who invited teammate")
- Use property-based cohorts (plan, region, device)
- Combine cohorts to analyze experiment impact

## SQL Insights (Example)
```sql
select
  date_trunc('week', timestamp) as week,
  count(distinct distinct_id) as wau
from events
where event = 'app_opened'
group by 1
order by 1 desc;
```

## Warehouse Export
- Use PostHog data pipelines to send events to BigQuery/Snowflake
- Model metrics (LTV, churn) in your warehouse

## Troubleshooting
- Missing data in SQL: ensure event names match; check timezones
- Cohort size off: verify distinct_id consistency; filter internal traffic

## Performance Notes
- Limit date ranges for heavy queries
- Add indexes on frequently filtered columns in warehouse

## Security/Privacy
- Pseudonymize or hash identifiers when exporting if required
- Apply data retention policies

## Next Steps
Finalize with Chapter 8: production deployment, compliance, and reliability.
