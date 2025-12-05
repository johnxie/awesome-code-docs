---
layout: default
title: "Langfuse Tutorial - Chapter 5: Analytics & Metrics"
nav_order: 5
has_children: false
parent: Langfuse Tutorial
---

# Chapter 5: Analytics & Metrics

> Track costs, latency, usage patterns, and ROI of your LLM applications.

## Overview

Langfuse analytics help you understand usage patterns, control costs, and identify optimization opportunities. The dashboard provides real-time metrics and historical trends.

## Cost Tracking

Monitor spending across providers and models:

```python
# Costs are automatically captured from usage metadata
trace.span(
    name="llm-call",
    usage={
        "input": 150,
        "output": 50,
        "total": 200,
        "model": "gpt-4o-mini",
        "cost": 0.003,  # $0.003 for this call
    }
)
```

## Key Metrics Dashboard

In the Langfuse UI, monitor:

- **Total Traces**: Request volume over time
- **Latency**: P95 response times by span type
- **Cost**: Daily/weekly spending with breakdowns
- **Token Usage**: Input vs output tokens
- **Error Rate**: Failed traces percentage
- **User Activity**: Active users and sessions

## Custom Analytics

Create custom charts and alerts:

```python
# Query traces for custom analytics
traces = langfuse.get_traces(
    limit=1000,
    filters={
        "tags": ["production"],
        "date_range": {"gte": "2024-01-01"},
        "scores": {"helpfulness": {"gte": 0.8}},
    }
)

# Calculate custom metrics
total_cost = sum(t.cost for t in traces)
avg_latency = sum(t.latency for t in traces) / len(traces)
```

## Cost Optimization Insights

Identify high-cost patterns:

- **Model Usage**: Which models consume the most budget
- **Prompt Efficiency**: Cost per quality score
- **User Segments**: High-spending users or features
- **Time Patterns**: Peak usage hours for scaling decisions

## Performance Monitoring

Set up alerts for:

- Cost thresholds (e.g., $100/day)
- Latency spikes (p95 > 5s)
- Error rate increases (>5%)
- Token usage anomalies

## ROI Analysis

Track business impact:

```python
# Correlate with business metrics
trace = langfuse.trace(
    name="customer-support",
    metadata={
        "ticket_id": "12345",
        "resolution_time": 15,  # minutes
        "customer_satisfaction": 4.5,
    }
)
```

Use external data sources to correlate LLM performance with KPIs.

## Exporting Data

Export metrics for external analysis:

```python
# Export to CSV/JSON
langfuse.export_traces(
    format="csv",
    filters={"date_range": {"gte": "2024-12-01"}},
    destination="s3://my-bucket/analytics.csv"
)
```

Integrate with BI tools (Tableau, Looker) or custom dashboards.

## Tips

- Set budgets and alerts early.
- Track cost per user/feature to identify optimization targets.
- Compare A/B test variants by cost and quality.
- Archive old traces to control storage costs.

Next: create test datasets from production traces. 