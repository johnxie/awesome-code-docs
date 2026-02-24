---
layout: default
title: "Chapter 7: Advanced Analytics"
parent: "PostHog Tutorial"
nav_order: 7
---

# Chapter 7: Advanced Analytics

Welcome to **Chapter 7: Advanced Analytics**. In this part of **PostHog Tutorial: Open Source Product Analytics Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In [Chapter 6](06-dashboards-insights.md), you built dashboards that communicate metrics to stakeholders. Those dashboards use PostHog's built-in insight types -- trends, funnels, retention -- which cover the majority of product analytics questions. But some questions require more power: custom SQL queries, advanced cohort logic, computed metrics, and data warehouse integrations.

This chapter covers PostHog's advanced analytics capabilities: HogQL (PostHog's SQL dialect), programmatic cohort management, data pipelines for warehouse synchronization, and techniques for building metrics like LTV, churn prediction, and attribution modeling that go beyond what point-and-click insights can deliver.

## What You Will Learn

- Write HogQL queries for custom metrics and ad-hoc analysis
- Build and manage advanced cohorts programmatically
- Export PostHog data to external warehouses (BigQuery, Snowflake, Redshift)
- Import external data into PostHog for enrichment
- Compute derived metrics like LTV, churn rate, and attribution

## HogQL: PostHog's SQL Engine

HogQL is a SQL dialect that lets you query PostHog's ClickHouse-backed data store directly. It gives you full access to the raw events, persons, and groups tables without leaving the PostHog interface.

### Architecture

```mermaid
flowchart LR
    A[PostHog SDK] --> B[Event Ingestion]
    B --> C[ClickHouse]
    C --> D[HogQL Engine]
    D --> E["SQL Insights<br/>(UI or API)"]
    D --> F["Notebooks"]
    D --> G["API Queries"]

    classDef ingest fill:#e1f5fe,stroke:#01579b
    classDef storage fill:#f3e5f5,stroke:#4a148c
    classDef query fill:#e8f5e8,stroke:#1b5e20

    class A,B ingest
    class C,D storage
    class E,F,G query
```

### Available Tables

| Table | Contents | Common Columns |
|-------|----------|---------------|
| `events` | All captured events | `event`, `distinct_id`, `timestamp`, `properties` |
| `persons` | User profiles | `id`, `properties`, `created_at` |
| `person_distinct_ids` | ID mapping | `distinct_id`, `person_id` |
| `groups` | Group profiles | `group_type_index`, `group_key`, `group_properties` |
| `session_replay_events` | Recording metadata | `session_id`, `distinct_id`, `first_timestamp` |
| `cohort_people` | Cohort memberships | `cohort_id`, `person_id` |

### Basic HogQL Queries

```sql
-- Weekly active users (WAU)
SELECT
    toStartOfWeek(timestamp) AS week,
    count(DISTINCT distinct_id) AS wau
FROM events
WHERE event = 'app_opened'
    AND timestamp >= now() - INTERVAL 12 WEEK
GROUP BY week
ORDER BY week DESC
```

```sql
-- Top events by volume in the last 30 days
SELECT
    event,
    count() AS event_count,
    count(DISTINCT distinct_id) AS unique_users,
    round(event_count / unique_users, 2) AS events_per_user
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
    AND event NOT LIKE '$%'  -- exclude system events
GROUP BY event
ORDER BY event_count DESC
LIMIT 20
```

```sql
-- Signup-to-activation time distribution
SELECT
    date_diff(
        'hour',
        signup_time,
        activation_time
    ) AS hours_to_activate,
    count() AS user_count
FROM (
    SELECT
        e1.distinct_id,
        min(e1.timestamp) AS signup_time,
        min(e2.timestamp) AS activation_time
    FROM events e1
    INNER JOIN events e2
        ON e1.distinct_id = e2.distinct_id
        AND e2.event = 'onboarding_completed'
        AND e2.timestamp > e1.timestamp
    WHERE e1.event = 'signed_up'
        AND e1.timestamp >= now() - INTERVAL 30 DAY
    GROUP BY e1.distinct_id
)
GROUP BY hours_to_activate
ORDER BY hours_to_activate
```

### Accessing Event Properties in HogQL

PostHog stores event properties as JSON. HogQL provides accessor syntax to extract values.

```sql
-- Revenue by plan and payment method
SELECT
    properties.$set.plan AS plan,
    properties.payment_method AS payment_method,
    count() AS transactions,
    sum(toFloat64OrZero(properties.amount_cents)) / 100 AS total_revenue_usd
FROM events
WHERE event = 'invoice_paid'
    AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY plan, payment_method
ORDER BY total_revenue_usd DESC
```

```sql
-- Feature usage by browser
SELECT
    properties.$browser AS browser,
    count() AS uses,
    count(DISTINCT distinct_id) AS unique_users
FROM events
WHERE event = 'insight_saved'
    AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY browser
ORDER BY uses DESC
```

### Querying Person Properties

```sql
-- Users by plan and country
SELECT
    person.properties.plan AS plan,
    person.properties.$geoip_country_code AS country,
    count() AS user_count
FROM persons person
WHERE person.properties.plan IS NOT NULL
GROUP BY plan, country
ORDER BY user_count DESC
LIMIT 20
```

### Running HogQL via the API

```typescript
// Execute a HogQL query via the PostHog API
async function runHogQLQuery(query: string) {
  const response = await fetch(
    'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/query/',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
      },
      body: JSON.stringify({
        kind: 'HogQLQuery',
        query: query
      })
    }
  )

  const result = await response.json()
  return {
    columns: result.columns,
    rows: result.results,
    types: result.types
  }
}

// Example: fetch WAU for the last 12 weeks
const wauData = await runHogQLQuery(`
  SELECT
      toStartOfWeek(timestamp) AS week,
      count(DISTINCT distinct_id) AS wau
  FROM events
  WHERE event = 'app_opened'
      AND timestamp >= now() - INTERVAL 12 WEEK
  GROUP BY week
  ORDER BY week DESC
`)

for (const [week, wau] of wauData.rows) {
  console.log(`${week}: ${wau} weekly active users`)
}
```

```python
import requests

def run_hogql_query(project_id: str, api_key: str, query: str) -> dict:
    """Execute a HogQL query against PostHog."""
    response = requests.post(
        f'https://app.posthog.com/api/projects/{project_id}/query/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        json={
            'kind': 'HogQLQuery',
            'query': query,
        }
    )
    result = response.json()
    return {
        'columns': result['columns'],
        'rows': result['results'],
    }

# Calculate churn rate by cohort week
churn_data = run_hogql_query(
    project_id='YOUR_PROJECT_ID',
    api_key='YOUR_API_KEY',
    query='''
        SELECT
            toStartOfWeek(signup_time) AS cohort_week,
            count() AS cohort_size,
            countIf(last_seen < now() - INTERVAL 30 DAY) AS churned,
            round(churned / cohort_size * 100, 2) AS churn_rate_pct
        FROM (
            SELECT
                distinct_id,
                min(timestamp) AS signup_time,
                max(timestamp) AS last_seen
            FROM events
            WHERE event IN ('signed_up', 'app_opened')
            GROUP BY distinct_id
            HAVING signup_time >= now() - INTERVAL 90 DAY
        )
        GROUP BY cohort_week
        ORDER BY cohort_week
    '''
)

for row in churn_data['rows']:
    print(f"Cohort {row[0]}: {row[1]} users, {row[3]}% churned")
```

## Advanced Cohort Management

### Dynamic vs. Static Cohorts

```mermaid
flowchart TD
    C[Cohort Types]
    C --> D["Dynamic Cohort"]
    C --> S["Static Cohort"]

    D --> D1["Auto-updates as users<br/>match criteria"]
    D --> D2["Example: Users who<br/>signed up in last 30 days"]
    D --> D3["Use for: ongoing analysis,<br/>feature targeting"]

    S --> S1["Fixed list of users,<br/>never changes"]
    S --> S2["Example: Users in a<br/>specific beta program"]
    S --> S3["Use for: one-time campaigns,<br/>experiment holdouts"]

    classDef type fill:#e1f5fe,stroke:#01579b
    classDef detail fill:#fff3e0,stroke:#ef6c00

    class C type
    class D,S type
    class D1,D2,D3,S1,S2,S3 detail
```

| Feature | Dynamic Cohort | Static Cohort |
|---------|:-------------:|:------------:|
| Auto-updates | Yes | No |
| API-creatable | Yes | Yes (via CSV upload) |
| Use in feature flags | Yes | Yes |
| Use in insights | Yes | Yes |
| Membership based on events | Yes | No |
| Membership based on properties | Yes | No |
| Fixed user list | No | Yes |

### Creating Complex Cohorts

```python
import requests

def create_behavioral_cohort(
    project_id: str,
    api_key: str,
    name: str,
    event_conditions: list,
    property_conditions: list
) -> dict:
    """Create a cohort with both event and property conditions."""
    groups = []

    # Add event-based conditions
    for condition in event_conditions:
        groups.append({
            'properties': [{
                'key': condition['event'],
                'value': condition.get('count', 1),
                'type': 'behavioral',
                'operator': condition.get('operator', 'gte'),
                'time_value': condition.get('days', 30),
                'time_interval': 'day',
            }]
        })

    # Add property-based conditions
    if property_conditions:
        groups.append({
            'properties': [
                {
                    'key': prop['key'],
                    'value': prop['value'],
                    'type': 'person',
                    'operator': prop.get('operator', 'exact'),
                }
                for prop in property_conditions
            ]
        })

    response = requests.post(
        f'https://app.posthog.com/api/projects/{project_id}/cohorts/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        json={
            'name': name,
            'groups': groups,
            'is_static': False,
        }
    )

    return response.json()

# Example: "Power users" - used the app 10+ times in 7 days AND are on growth plan
power_users = create_behavioral_cohort(
    project_id='YOUR_PROJECT_ID',
    api_key='YOUR_API_KEY',
    name='Power Users',
    event_conditions=[
        {'event': 'app_opened', 'count': 10, 'days': 7, 'operator': 'gte'},
    ],
    property_conditions=[
        {'key': 'plan', 'value': 'growth', 'operator': 'exact'},
    ]
)

print(f"Created cohort: {power_users['name']} (ID: {power_users['id']})")
```

### Cohort Comparison with HogQL

```sql
-- Compare conversion rates between two cohorts
SELECT
    CASE
        WHEN distinct_id IN (SELECT distinct_id FROM cohort_people WHERE cohort_id = 1)
            THEN 'Power Users'
        WHEN distinct_id IN (SELECT distinct_id FROM cohort_people WHERE cohort_id = 2)
            THEN 'Casual Users'
        ELSE 'Other'
    END AS cohort_name,
    count(DISTINCT distinct_id) AS users,
    countIf(event = 'subscription_upgraded') AS upgrades,
    round(upgrades / users * 100, 2) AS upgrade_rate_pct
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
    AND event IN ('app_opened', 'subscription_upgraded')
GROUP BY cohort_name
ORDER BY upgrade_rate_pct DESC
```

## Data Pipelines and Warehouse Integration

PostHog can both export data to and import data from external systems. This enables advanced modeling, machine learning, and joining PostHog data with business data from your CRM, billing system, or data warehouse.

### Export Architecture

```mermaid
flowchart LR
    PH[PostHog]
    PH --> E1["Batch Export<br/>(S3, GCS)"]
    PH --> E2["Streaming Export<br/>(Webhook, Kafka)"]
    PH --> E3["Warehouse Sync<br/>(BigQuery, Snowflake,<br/>Redshift)"]

    E1 --> W1["Data Lake"]
    E2 --> W2["Real-time Pipeline"]
    E3 --> W3["Data Warehouse"]

    W1 --> M["dbt / SQL Models"]
    W3 --> M
    M --> D["BI Dashboards<br/>(Looker, Metabase)"]
    M --> ML["ML Models"]

    classDef ph fill:#e1f5fe,stroke:#01579b
    classDef export fill:#fff3e0,stroke:#ef6c00
    classDef dest fill:#f3e5f5,stroke:#4a148c
    classDef output fill:#e8f5e8,stroke:#1b5e20

    class PH ph
    class E1,E2,E3 export
    class W1,W2,W3 dest
    class M,D,ML output
```

### Setting Up a BigQuery Export

1. Navigate to **Data pipelines** in PostHog
2. Click **New destination**
3. Select **BigQuery**
4. Configure the connection:
   - GCP Project ID
   - Dataset name
   - Service account JSON key
5. Choose which data to export:
   - Events
   - Persons
   - Groups
6. Set the sync frequency (hourly, daily)
7. Click **Create**

### Exporting Events via the API

```typescript
// Batch export events to your own system
async function exportEvents(
  projectId: string,
  apiKey: string,
  dateFrom: string,
  dateTo: string
) {
  let url = `https://app.posthog.com/api/projects/${projectId}/events/?` +
    `after=${dateFrom}&before=${dateTo}&limit=1000`

  const allEvents: any[] = []

  while (url) {
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    })
    const data = await response.json()

    allEvents.push(...data.results)
    url = data.next  // pagination

    console.log(`Fetched ${allEvents.length} events...`)
  }

  return allEvents
}

// Export last 7 days of events
const events = await exportEvents(
  'YOUR_PROJECT_ID',
  'YOUR_API_KEY',
  '2025-01-20',
  '2025-01-27'
)
console.log(`Total events exported: ${events.length}`)
```

```python
import requests
from typing import List, Dict

def export_events(
    project_id: str,
    api_key: str,
    date_from: str,
    date_to: str,
) -> List[Dict]:
    """Export events from PostHog within a date range."""
    all_events = []
    url = (
        f'https://app.posthog.com/api/projects/{project_id}/events/'
        f'?after={date_from}&before={date_to}&limit=1000'
    )

    while url:
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        data = response.json()
        all_events.extend(data['results'])
        url = data.get('next')
        print(f'Fetched {len(all_events)} events...')

    return all_events

# Export events for LTV modeling
events = export_events(
    project_id='YOUR_PROJECT_ID',
    api_key='YOUR_API_KEY',
    date_from='2025-01-01',
    date_to='2025-01-31',
)

# Save to a file for warehouse loading
import json
with open('posthog_events_jan.json', 'w') as f:
    json.dump(events, f)

print(f'Exported {len(events)} events')
```

### Importing External Data

PostHog can ingest data from external sources to enrich your analytics.

| Source | Method | Use Case |
|--------|--------|----------|
| Stripe | PostHog integration | Revenue data, subscription status |
| HubSpot / Salesforce | PostHog integration | CRM data, deal stage |
| Custom database | Batch API import | Product data, user metadata |
| CSV upload | Static cohort | One-time user lists |

```python
# Import Stripe subscription data as person properties
import stripe
from posthog import Posthog

stripe.api_key = 'sk_...'
posthog_client = Posthog(api_key='YOUR_API_KEY', host='https://app.posthog.com')

def sync_stripe_to_posthog():
    """Sync Stripe customer data to PostHog person properties."""
    customers = stripe.Customer.list(limit=100)

    for customer in customers.auto_paging_iter():
        subscriptions = stripe.Subscription.list(customer=customer.id, limit=1)

        if subscriptions.data:
            sub = subscriptions.data[0]
            posthog_client.identify(
                distinct_id=customer.metadata.get('posthog_id', customer.id),
                properties={
                    'stripe_customer_id': customer.id,
                    'subscription_status': sub.status,
                    'subscription_plan': sub.items.data[0].price.lookup_key,
                    'mrr_cents': sub.items.data[0].price.unit_amount,
                    'subscription_start': sub.start_date,
                    'trial_end': sub.trial_end,
                }
            )

    posthog_client.flush()

sync_stripe_to_posthog()
```

## Computed Metrics

### Customer Lifetime Value (LTV)

```sql
-- Calculate LTV by signup cohort
SELECT
    toStartOfMonth(signup_time) AS cohort_month,
    count() AS cohort_size,
    round(sum(total_revenue) / cohort_size, 2) AS avg_ltv_usd,
    round(avg(months_active), 1) AS avg_lifetime_months
FROM (
    SELECT
        e_signup.distinct_id,
        min(e_signup.timestamp) AS signup_time,
        coalesce(sum(toFloat64OrZero(e_pay.properties.amount_cents)) / 100, 0) AS total_revenue,
        date_diff('month', min(e_signup.timestamp), max(e_any.timestamp)) AS months_active
    FROM events e_signup
    LEFT JOIN events e_pay
        ON e_signup.distinct_id = e_pay.distinct_id
        AND e_pay.event = 'invoice_paid'
    LEFT JOIN events e_any
        ON e_signup.distinct_id = e_any.distinct_id
    WHERE e_signup.event = 'signed_up'
        AND e_signup.timestamp >= now() - INTERVAL 12 MONTH
    GROUP BY e_signup.distinct_id
)
GROUP BY cohort_month
ORDER BY cohort_month
```

### Churn Rate

```sql
-- Monthly churn rate
SELECT
    toStartOfMonth(period) AS month,
    active_start,
    active_end,
    churned,
    round(churned / active_start * 100, 2) AS churn_rate_pct
FROM (
    SELECT
        toStartOfMonth(now() - INTERVAL number MONTH) AS period,
        (
            SELECT count(DISTINCT distinct_id)
            FROM events
            WHERE timestamp >= period - INTERVAL 30 DAY
                AND timestamp < period
                AND event = 'app_opened'
        ) AS active_start,
        (
            SELECT count(DISTINCT distinct_id)
            FROM events
            WHERE timestamp >= period
                AND timestamp < period + INTERVAL 30 DAY
                AND event = 'app_opened'
        ) AS active_end,
        active_start - active_end AS churned
    FROM numbers(6)
)
ORDER BY month DESC
```

### Attribution Modeling

```sql
-- First-touch attribution: which channels drive signups that convert?
SELECT
    first_touch_source,
    signups,
    conversions,
    round(conversions / signups * 100, 2) AS conversion_rate_pct,
    round(total_revenue, 2) AS revenue_usd
FROM (
    SELECT
        properties.$initial_referrer AS first_touch_source,
        count(DISTINCT e1.distinct_id) AS signups,
        count(DISTINCT e2.distinct_id) AS conversions,
        coalesce(sum(toFloat64OrZero(e3.properties.amount_cents)) / 100, 0) AS total_revenue
    FROM events e1
    LEFT JOIN events e2
        ON e1.distinct_id = e2.distinct_id
        AND e2.event = 'subscription_upgraded'
    LEFT JOIN events e3
        ON e1.distinct_id = e3.distinct_id
        AND e3.event = 'invoice_paid'
    WHERE e1.event = 'signed_up'
        AND e1.timestamp >= now() - INTERVAL 90 DAY
    GROUP BY first_touch_source
)
WHERE signups > 10
ORDER BY revenue_usd DESC
LIMIT 15
```

## PostHog Notebooks

Notebooks combine text, HogQL queries, insights, and recordings in a single interactive document. They are ideal for ad-hoc investigations and sharing analyses with your team.

### Notebook Use Cases

| Use Case | Contents | Audience |
|----------|----------|----------|
| **Incident investigation** | Timeline, HogQL queries, session recordings | Engineering |
| **Feature launch review** | Experiment results, funnel before/after, cohort comparison | Product |
| **Quarterly business review** | KPI trends, cohort LTV, churn analysis | Executive |
| **User research synthesis** | Session recording playlists, survey data, quotes | Design |

### Creating a Notebook

1. Navigate to **Notebooks** in PostHog
2. Click **New Notebook**
3. Add content blocks:
   - **Text**: Markdown-formatted narrative
   - **Query**: HogQL query with inline results
   - **Insight**: Embed an existing saved insight
   - **Recording**: Link to a specific session recording
   - **Image**: Screenshots or diagrams
4. Share the notebook link with your team

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| HogQL query times out | Query too broad or joins too large | Add date filters; reduce LIMIT; avoid cross-joins |
| Wrong results from property access | Property name has special characters | Use bracket notation: `properties['my-prop']` |
| Cohort shows unexpected size | Event condition too broad or narrow | Verify event names and time windows |
| Export missing recent events | Batch export has not run yet | Wait for next sync cycle; check pipeline status |
| Warehouse data stale | Sync frequency too low | Increase sync frequency; use streaming export |
| HogQL cannot find table | Wrong table name or schema | Use `SHOW TABLES` to list available tables |

## Performance Considerations

- **Date filters first**: Always include a date range in HogQL queries. Without one, ClickHouse scans the entire events table.
- **Avoid SELECT ***: Specify only the columns you need. Fewer columns means less data to scan.
- **Use LIMIT**: During exploration, always add `LIMIT 100` to avoid downloading millions of rows.
- **Pre-aggregate**: For dashboards, create materialized views or save computed results rather than re-running expensive queries.
- **Cohort size**: Very large cohorts (1M+ users) can slow down queries that filter by cohort membership. Consider property-based filters instead.

```sql
-- GOOD: specific columns, date filter, limit
SELECT event, count() AS cnt
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY event
ORDER BY cnt DESC
LIMIT 20

-- BAD: no date filter, select *, no limit
SELECT * FROM events WHERE event = 'app_opened'
```

## Security and Privacy

- **HogQL access control**: Only users with project access can run HogQL queries. Restrict project membership to authorized analysts.
- **Data exports**: When exporting to a warehouse, ensure the warehouse has equivalent access controls and encryption.
- **PII in queries**: HogQL queries can access person properties including email and name. Do not share query results containing PII.
- **Pseudonymization**: When exporting for machine learning or external analysis, hash or pseudonymize distinct_id and person properties.
- **Data retention**: Set retention policies for both PostHog and your external warehouse to comply with regulations.

```python
import hashlib

def pseudonymize_export(events: list) -> list:
    """Remove PII from exported events."""
    sanitized = []
    for event in events:
        sanitized_event = {
            'event': event['event'],
            'timestamp': event['timestamp'],
            'distinct_id': hashlib.sha256(
                event['distinct_id'].encode()
            ).hexdigest()[:16],
            'properties': {
                k: v for k, v in event.get('properties', {}).items()
                if k not in ('email', 'name', 'phone', 'ip')
            }
        }
        sanitized.append(sanitized_event)
    return sanitized
```

## Summary

Advanced analytics in PostHog extends your capabilities beyond the standard insight types. HogQL gives you the power of SQL directly against your event data. Cohorts let you segment users by complex behavioral and property criteria. Data pipelines connect PostHog to your warehouse for derived metrics like LTV and churn. Notebooks bring it all together in a shareable, narrative format. These tools transform PostHog from a product analytics dashboard into a full-featured analytics platform.

## Key Takeaways

1. **HogQL unlocks custom metrics** -- when the built-in insights do not answer your question, write SQL directly against the events table.
2. **Cohorts are reusable segments** -- define them once with behavioral and property criteria, then use them across funnels, experiments, and dashboards.
3. **Export to your warehouse for derived metrics** -- LTV, churn prediction, and attribution modeling are best done in a warehouse with dbt or similar tools.
4. **Import external data to enrich PostHog** -- connect Stripe, CRM, and product data to create a unified view of user behavior.
5. **Notebooks document your analysis** -- use them for investigations, reviews, and sharing findings with non-technical stakeholders.

## Next Steps

You now have the analytical tools to answer virtually any product question. The final step is making it all work reliably at scale. In [Chapter 8: Production Deployment](08-production-deployment.md), you will learn how to deploy PostHog for production workloads, secure your analytics infrastructure, monitor ingestion health, and plan for growth.

---

*Built with insights from the [PostHog](https://github.com/PostHog/posthog) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `events`, `event`, `distinct_id` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Advanced Analytics` as an operating subsystem inside **PostHog Tutorial: Open Source Product Analytics Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `timestamp`, `SELECT`, `count` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Advanced Analytics` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `events`.
2. **Input normalization**: shape incoming data so `event` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `distinct_id`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/PostHog/posthog)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `events` and `event` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Dashboards & Insights](06-dashboards-insights.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
