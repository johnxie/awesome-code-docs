---
layout: default
title: "Chapter 6: Dashboards & Insights"
parent: "PostHog Tutorial"
nav_order: 6
---

# Chapter 6: Dashboards & Insights

Welcome to **Chapter 6: Dashboards & Insights**. In this part of **PostHog Tutorial: Open Source Product Analytics Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In the previous chapters you built the entire analytics pipeline: event tracking (Chapter 2), user analytics (Chapter 3), session recordings (Chapter 4), and feature flags (Chapter 5). Each of those tools produces individual insights. Dashboards are where you bring them together into a coherent story that your team, your managers, and your stakeholders can understand at a glance.

A well-designed dashboard answers a specific question for a specific audience. A poorly designed one is a wall of charts that nobody reads. This chapter teaches you how to design dashboards that people actually use, how to create and configure insights in PostHog, and how to set up automated reports and alerts so the data comes to you.

## What You Will Learn

- Design dashboards for different audiences (executive, product, engineering)
- Create and configure all PostHog insight types
- Organize dashboards with layouts, descriptions, and sections
- Set up scheduled reports and anomaly alerts
- Use the PostHog API to build custom reporting

## Dashboard Design Principles

### Audience-Driven Design

Every dashboard should have a clear owner and a clear question it answers. If you cannot state the question in one sentence, the dashboard is too broad.

```mermaid
flowchart TD
    A["Who is the audience?"] --> B{"Executive"}
    A --> C{"Product"}
    A --> D{"Engineering"}
    A --> E{"Growth"}

    B --> B1["Revenue, activation,<br/>churn, high-level KPIs"]
    C --> C1["Funnels, retention,<br/>feature adoption, experiments"]
    D --> D1["Error rates, latency,<br/>ingestion health, uptime"]
    E --> E1["Acquisition channels,<br/>campaigns, referrals, CAC"]

    classDef audience fill:#e1f5fe,stroke:#01579b
    classDef content fill:#e8f5e8,stroke:#1b5e20

    class A audience
    class B,C,D,E audience
    class B1,C1,D1,E1 content
```

### Dashboard Templates

| Dashboard | Audience | Key Insights | Refresh |
|-----------|----------|-------------|---------|
| **Company KPIs** | Executive / All-hands | ARR, DAU/MAU, activation rate, churn | Weekly |
| **Product Health** | Product team | Core funnel, retention, feature adoption | Daily |
| **Growth & Acquisition** | Growth / Marketing | Signups by channel, CAC, campaign performance | Daily |
| **Engineering Health** | Engineering | Error rate, p95 latency, ingestion volume | Hourly |
| **Experiment Results** | Product + Data | Active experiments, significance, lift | Real-time |
| **Customer Success** | CS / Support | NPS trend, support tickets, churn risk | Weekly |

### Layout Best Practices

| Principle | Why | How |
|-----------|-----|-----|
| Limit to 8-12 insights per dashboard | Prevents information overload | Split by audience if you have more |
| Put the most important metric top-left | Users read left-to-right, top-to-bottom | Use a large "number" insight for the hero metric |
| Group related insights together | Creates a visual narrative | Use description text between sections |
| Use consistent time ranges | Avoids confusion when comparing | Set a dashboard-level date filter |
| Add text descriptions | Provides context for non-analysts | Use PostHog's text cards |

## Creating Insights

### Insight Types Reference

PostHog offers several insight types, each suited to a different question.

```mermaid
flowchart LR
    subgraph Quantitative
        A[Trends]
        B[Funnels]
        C[Retention]
        D[Stickiness]
        E[Lifecycle]
    end
    subgraph Exploratory
        F[Paths]
        G[SQL / HogQL]
    end
    subgraph Display
        H[Number]
        I[Table]
        J[World Map]
    end

    classDef quant fill:#e1f5fe,stroke:#01579b
    classDef explore fill:#f3e5f5,stroke:#4a148c
    classDef display fill:#e8f5e8,stroke:#1b5e20

    class A,B,C,D,E quant
    class F,G explore
    class H,I,J display
```

| Type | Best For | Configuration |
|------|----------|---------------|
| **Trends** | Metrics over time | Events, math (total, DAU, avg), interval, breakdown |
| **Funnels** | Conversion analysis | Ordered steps, window, breakdown, exclusions |
| **Retention** | User return rate | Start event, return event, period (day/week/month) |
| **Stickiness** | Engagement depth | Event, time window, breakdown |
| **Lifecycle** | User composition | Event, period, shows new/returning/resurrecting/dormant |
| **Paths** | Navigation patterns | Start/end point, step limit, edge weight |
| **Number** | Single KPI display | Event, math, comparison period |
| **Table** | Tabular breakdown | Event, breakdown, multiple columns |
| **SQL (HogQL)** | Custom queries | Raw SQL against PostHog's ClickHouse data |
| **World Map** | Geographic distribution | Event, breakdown by `$geoip_country_code` |

### Building a Trends Insight

```typescript
// Create a trends insight via the API
const response = await fetch(
  'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      name: 'Daily Active Users (DAU)',
      description: 'Unique users who opened the app each day',
      filters: {
        insight: 'TRENDS',
        events: [
          {
            id: 'app_opened',
            math: 'dau',
            name: 'DAU'
          }
        ],
        date_from: '-30d',
        interval: 'day',
        display: 'ActionsLineGraph'
      },
      saved: true
    })
  }
)

const insight = await response.json()
console.log(`Created insight: ${insight.name} (ID: ${insight.id})`)
```

### Building a Number Insight

Number insights are perfect for hero metrics at the top of a dashboard.

```typescript
// Create a "number" insight showing total signups this week
const numberInsight = await fetch(
  'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      name: 'Signups This Week',
      filters: {
        insight: 'TRENDS',
        events: [
          {
            id: 'signed_up',
            math: 'total',
            name: 'Signups'
          }
        ],
        date_from: '-7d',
        display: 'BoldNumber',
        compare: true  // show comparison to previous period
      },
      saved: true
    })
  }
)
```

### Building a Funnel Insight

```python
import requests

# Create a funnel insight for the onboarding flow
response = requests.post(
    'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY',
    },
    json={
        'name': 'Onboarding Funnel',
        'description': 'Signup → Create Project → Invite Team → First Insight',
        'filters': {
            'insight': 'FUNNELS',
            'events': [
                {'id': 'signed_up', 'order': 0},
                {'id': 'project_created', 'order': 1},
                {'id': 'teammate_invited', 'order': 2},
                {'id': 'insight_saved', 'order': 3},
            ],
            'funnel_window_days': 14,
            'breakdown': 'plan',
            'date_from': '-30d',
        },
        'saved': True,
    }
)

insight = response.json()
print(f"Created funnel: {insight['name']}")
```

## Building Dashboards

### Creating a Dashboard in the UI

1. Navigate to **Dashboards** and click **New Dashboard**
2. Choose a template or start from blank
3. Name the dashboard (e.g., "Product Health - Q1 2025")
4. Add a description explaining the audience and purpose
5. Click **Add Insight** to add existing saved insights, or create new ones inline
6. Drag and resize insights to arrange the layout
7. Add text cards between sections for context

### Creating a Dashboard via the API

```typescript
// Create a dashboard and add insights
const dashboardResponse = await fetch(
  'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/dashboards/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      name: 'Product Health Dashboard',
      description: 'Daily overview of product metrics for the product team',
      filters: {
        date_from: '-30d'  // dashboard-level date filter
      },
      tags: ['product', 'daily']
    })
  }
)

const dashboard = await dashboardResponse.json()
console.log(`Dashboard created: ${dashboard.id}`)

// Add an insight to the dashboard
await fetch(
  `https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      name: 'Core Funnel Conversion',
      dashboards: [dashboard.id],
      filters: {
        insight: 'FUNNELS',
        events: [
          { id: 'signed_up', order: 0 },
          { id: 'onboarding_completed', order: 1 },
          { id: 'project_created', order: 2 }
        ],
        funnel_window_days: 7,
        date_from: '-30d'
      },
      saved: true
    })
  }
)
```

```python
import requests

# Create a dashboard via the API
response = requests.post(
    'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/dashboards/',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY',
    },
    json={
        'name': 'Executive KPIs',
        'description': 'Weekly executive review: ARR, activation, churn',
        'filters': {'date_from': '-90d'},
        'tags': ['executive', 'weekly'],
    }
)

dashboard = response.json()
print(f"Created dashboard: {dashboard['name']} (ID: {dashboard['id']})")
```

## Dashboard Patterns by Audience

### Executive Dashboard

Focus on business outcomes. Minimize detail; maximize clarity.

| Position | Insight | Type | Metric |
|----------|---------|------|--------|
| Top-left (hero) | MRR / ARR | Number | Sum of `invoice_paid.amount_cents` |
| Top-center | Activation Rate | Number | `onboarding_completed` / `signed_up` |
| Top-right | Churn Rate | Number | Churned users / total users |
| Middle-left | Revenue Trend | Trend | Weekly revenue over 12 weeks |
| Middle-right | Signup Trend | Trend | Daily signups over 30 days |
| Bottom | Onboarding Funnel | Funnel | Signup to first value moment |

### Product Dashboard

Focus on user behavior and feature adoption.

| Position | Insight | Type | Metric |
|----------|---------|------|--------|
| Top row | DAU, WAU, MAU | Number (x3) | Unique users of `app_opened` |
| Middle-left | Core Funnel | Funnel | Key user flow conversion |
| Middle-right | Weekly Retention | Retention | `signed_up` to `app_opened` |
| Bottom-left | Feature Adoption | Trend | New feature events over time |
| Bottom-right | Stickiness | Stickiness | Days per week users engage |

### Engineering Dashboard

Focus on reliability, performance, and infrastructure health.

| Position | Insight | Type | Metric |
|----------|---------|------|--------|
| Top-left | Error Rate | Number | `api_error_occurred` count / hour |
| Top-center | p95 Latency | Number | `api_response_time` 95th percentile |
| Top-right | Events Ingested | Number | Total events / minute |
| Middle | Error Trend | Trend | Errors by endpoint, hourly |
| Bottom-left | Status Code Distribution | Table | Breakdown by `status_code` |
| Bottom-right | Slow Queries | Table | Endpoints with highest latency |

## Scheduled Reports and Alerts

### Email and Slack Subscriptions

PostHog can send dashboard snapshots on a schedule.

1. Open a dashboard
2. Click the **Share** button
3. Select **Subscribe**
4. Choose delivery method:
   - **Email**: add recipient email addresses
   - **Slack**: select a Slack channel (requires Slack integration)
5. Set frequency: daily, weekly, or monthly
6. Set delivery time (e.g., Monday 9:00 AM)
7. Save the subscription

### Subscription Configuration

| Setting | Options | Recommendation |
|---------|---------|---------------|
| Frequency | Daily, Weekly, Monthly | Weekly for executive; daily for product |
| Day of week | Mon-Sun | Monday for weekly reviews |
| Time | Any time | Morning before standup |
| Format | Image snapshot | Default; works in all email clients |
| Recipients | Email, Slack channel | Use a team channel, not individuals |

### Anomaly Alerts

Alerts notify you when a metric crosses a threshold or deviates from its baseline.

```mermaid
flowchart TD
    A["Define alert:<br/>Error rate > 5%"] --> B["PostHog monitors<br/>metric continuously"]
    B --> C{"Threshold<br/>breached?"}
    C -->|Yes| D["Send notification<br/>via Slack/Email"]
    C -->|No| B
    D --> E["Team investigates"]

    classDef config fill:#e1f5fe,stroke:#01579b
    classDef monitor fill:#fff3e0,stroke:#ef6c00
    classDef alert fill:#ffebee,stroke:#c62828
    classDef action fill:#e8f5e8,stroke:#1b5e20

    class A config
    class B,C monitor
    class D alert
    class E action
```

### Setting Up Alerts

1. Navigate to an insight (e.g., error rate trend)
2. Click the **Alerts** icon
3. Configure the alert:
   - **Condition**: "Value is above 500" or "Value increased by 50%"
   - **Check frequency**: Every hour
   - **Notification**: Slack channel or email
4. Save the alert

### Common Alert Configurations

| Alert | Metric | Condition | Channel |
|-------|--------|-----------|---------|
| Error spike | `api_error_occurred` / hour | > 2x 7-day average | #engineering-alerts |
| Signup drop | `signed_up` / day | < 50% of 7-day average | #growth-team |
| Conversion drop | Funnel step 2 → 3 | < 20% conversion | #product-team |
| Revenue anomaly | `invoice_paid` sum / day | < 70% of 30-day average | #finance-alerts |
| Recording volume spike | Session recording count | > 3x daily average | #platform-team |

## Custom Reporting with the API

### Fetching Dashboard Data

```typescript
// Fetch all insights from a dashboard
async function getDashboardData(dashboardId: number) {
  const response = await fetch(
    `https://app.posthog.com/api/projects/YOUR_PROJECT_ID/dashboards/${dashboardId}/`,
    {
      headers: {
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
      }
    }
  )

  const dashboard = await response.json()

  for (const tile of dashboard.tiles) {
    const insight = tile.insight
    console.log(`${insight.name}: ${JSON.stringify(insight.result)}`)
  }

  return dashboard
}
```

### Building a Custom Weekly Report

```python
import requests
from datetime import datetime

def generate_weekly_report(project_id: str, api_key: str) -> dict:
    """Generate a custom weekly report from PostHog data."""
    base_url = f'https://app.posthog.com/api/projects/{project_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    # Fetch signups trend
    signups = requests.post(
        f'{base_url}/insights/trend/',
        headers=headers,
        json={
            'events': [{'id': 'signed_up', 'math': 'total'}],
            'date_from': '-7d',
            'interval': 'day',
        }
    ).json()

    # Fetch DAU trend
    dau = requests.post(
        f'{base_url}/insights/trend/',
        headers=headers,
        json={
            'events': [{'id': 'app_opened', 'math': 'dau'}],
            'date_from': '-7d',
            'interval': 'day',
        }
    ).json()

    # Fetch onboarding funnel
    funnel = requests.post(
        f'{base_url}/insights/funnel/',
        headers=headers,
        json={
            'events': [
                {'id': 'signed_up', 'order': 0},
                {'id': 'onboarding_completed', 'order': 1},
                {'id': 'project_created', 'order': 2},
            ],
            'funnel_window_days': 7,
            'date_from': '-7d',
        }
    ).json()

    report = {
        'generated_at': datetime.now().isoformat(),
        'period': 'Last 7 days',
        'signups': {
            'total': sum(signups['result'][0]['data']),
            'daily': signups['result'][0]['data'],
        },
        'dau': {
            'average': round(
                sum(dau['result'][0]['data']) / len(dau['result'][0]['data']), 1
            ),
            'daily': dau['result'][0]['data'],
        },
        'onboarding_funnel': {
            'steps': [
                {'name': step['name'], 'count': step['count']}
                for step in funnel['result']
            ],
        },
    }

    return report

# Generate and print the report
report = generate_weekly_report('YOUR_PROJECT_ID', 'YOUR_API_KEY')
print(f"Weekly Report - {report['period']}")
print(f"Total Signups: {report['signups']['total']}")
print(f"Average DAU: {report['dau']['average']}")
```

## Dashboard Sharing and Permissions

### Sharing Options

| Method | Audience | Access Level |
|--------|----------|-------------|
| **Internal link** | Team members with PostHog access | Full interactive access |
| **Shared link** | External stakeholders | Read-only, no login required |
| **Embedded iframe** | Internal tools, wikis | Read-only embed |
| **Scheduled report** | Any email or Slack channel | Static snapshot |
| **API export** | Custom tools and scripts | Raw data access |

### Access Control

```mermaid
flowchart TD
    D[Dashboard]
    D --> P1["Project Members<br/>Full access"]
    D --> P2["Shared Link<br/>Read-only, no PII"]
    D --> P3["API Access<br/>Requires API key"]

    P1 --> R1["Can edit, add insights,<br/>change filters"]
    P2 --> R2["Can view charts,<br/>cannot see person data"]
    P3 --> R3["Can read data,<br/>scoped by key permissions"]

    classDef dash fill:#e1f5fe,stroke:#01579b
    classDef perm fill:#fff3e0,stroke:#ef6c00
    classDef detail fill:#e8f5e8,stroke:#1b5e20

    class D dash
    class P1,P2,P3 perm
    class R1,R2,R3 detail
```

### Creating a Shared Link

```typescript
// Create a sharing link for a dashboard
const sharingResponse = await fetch(
  `https://app.posthog.com/api/projects/YOUR_PROJECT_ID/dashboards/DASHBOARD_ID/sharing/`,
  {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      enabled: true
    })
  }
)

const sharing = await sharingResponse.json()
console.log(`Shared link: ${sharing.access_token}`)
// Link format: https://app.posthog.com/shared_dashboard/{access_token}
```

## Dashboard Maintenance

### Review Cadence

| Activity | Frequency | Who |
|----------|-----------|-----|
| Review metric definitions | Monthly | Analytics + Product |
| Archive stale dashboards | Quarterly | Dashboard owners |
| Audit shared links | Monthly | Security / Admin |
| Update alert thresholds | After major releases | Engineering |
| Clean up orphaned insights | Quarterly | Analytics |

### Signs a Dashboard Needs Attention

- **Nobody opens it**: Check PostHog's own analytics on dashboard views
- **Too many insights**: If you scroll to see everything, split it
- **Outdated metrics**: Events renamed or deprecated; insights show zero
- **No description**: New team members cannot understand the context
- **Conflicting date ranges**: Individual insights override the dashboard filter

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Dashboard loads slowly | Too many insights or wide date ranges | Reduce to 8-12 insights; narrow date range |
| Data looks stale | Caching or ingestion delay | Refresh the dashboard; check ingestion health |
| Numbers differ from other dashboards | Different date ranges or filters | Align dashboard-level filters |
| Shared link shows no data | Sharing not enabled or expired | Re-enable sharing in dashboard settings |
| Alerts not firing | Threshold set incorrectly or notification misconfigured | Verify condition and Slack/email integration |
| Breakdown shows "Other" | High-cardinality property | Reduce cardinality or use top-N filter |

## Performance Considerations

- **Dashboard-level filters**: Apply a single date range to all insights instead of per-insight filters. This enables query optimization.
- **Caching**: PostHog caches insight results. Dashboards do not re-run queries on every page load. Manual refresh triggers a fresh query.
- **Insight count**: Each insight is a separate query. Keep dashboards under 12-15 insights for fast load times.
- **Breakdowns**: Multi-dimensional breakdowns (e.g., by plan AND by country) multiply query cost. Use sparingly on dashboards.

## Security and Privacy

- **Shared links**: Shared dashboards expose aggregated data. Ensure no PII is visible in insight names, descriptions, or breakdowns.
- **API keys**: Use project-scoped API keys for programmatic access. Do not embed personal API keys in client-side code.
- **Role-based access**: Limit dashboard editing to the owning team. Use viewer roles for stakeholders.
- **Audit trail**: PostHog logs who accessed which dashboard and when. Review access logs periodically.

## Summary

Dashboards are the communication layer of your analytics stack. They transform raw insights into narratives that drive decisions across teams. A well-designed dashboard has a clear audience, a focused set of metrics, and automated delivery so the right people see the right data at the right time.

## Key Takeaways

1. **Design for a specific audience** -- an executive dashboard and an engineering dashboard should look completely different.
2. **Limit insights per dashboard** -- 8-12 well-chosen insights tell a better story than 30 crammed onto one page.
3. **Automate delivery** -- use Slack and email subscriptions so stakeholders see dashboards without logging in.
4. **Set alerts for critical metrics** -- do not rely on manual dashboard checks for error rates and revenue anomalies.
5. **Maintain and retire** -- dashboards have a lifecycle. Archive ones nobody uses and refresh definitions quarterly.

## Next Steps

Your dashboards are now telling the story of your product. But sometimes the standard insight types are not enough. In [Chapter 7: Advanced Analytics](07-advanced-analytics.md), you will learn how to use cohort analysis, custom SQL queries with HogQL, and data warehouse integrations to answer questions that go beyond what the UI provides out of the box.

---

*Built with insights from the [PostHog](https://github.com/PostHog/posthog) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `json`, `insight`, `dashboard` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Dashboards & Insights` as an operating subsystem inside **PostHog Tutorial: Open Source Product Analytics Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `headers`, `name`, `classDef` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Dashboards & Insights` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `json`.
2. **Input normalization**: shape incoming data so `insight` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `dashboard`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/PostHog/posthog)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `json` and `insight` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Feature Flags & Experiments](05-feature-flags.md)
- [Next Chapter: Chapter 7: Advanced Analytics](07-advanced-analytics.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
