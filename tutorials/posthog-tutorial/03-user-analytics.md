---
layout: default
title: "Chapter 3: User Analytics & Funnels"
parent: "PostHog Tutorial"
nav_order: 3
---

# Chapter 3: User Analytics & Funnels

Welcome to **Chapter 3: User Analytics & Funnels**. In this part of **PostHog Tutorial: Open Source Product Analytics Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In [Chapter 2](02-event-tracking.md), you built a solid event tracking layer with clean naming conventions, rich properties, and identity resolution. Raw events are the ingredients; analytics is the recipe. This chapter shows you how to turn those ingredients into funnels, retention curves, user paths, and trend analyses that drive real product decisions.

By the end of this chapter you will be able to answer questions like "Where do users drop off during onboarding?", "How many users come back after week one?", and "Which acquisition channel produces the most paying customers?"

## What You Will Learn

- Build conversion funnels and diagnose drop-offs
- Measure retention with cohort-based tables
- Map user journeys with the Paths visualization
- Create trend insights for KPIs like DAU, WAU, and MAU
- Segment every analysis by cohort, property, or experiment variant

## The PostHog Insights Engine

PostHog provides five core insight types. Each answers a different class of question.

```mermaid
flowchart TD
    Q[Product Question]
    Q --> T["How is metric X changing over time?"]
    Q --> F["Where do users drop off?"]
    Q --> R["Do users come back?"]
    Q --> P["What paths do users take?"]
    Q --> L["What does the distribution look like?"]

    T --> Trends
    F --> Funnels
    R --> Retention
    P --> Paths
    L --> Stickiness

    classDef question fill:#e1f5fe,stroke:#01579b
    classDef insight fill:#e8f5e8,stroke:#1b5e20

    class Q,T,F,R,P,L question
    class Trends,Funnels,Retention,Paths,Stickiness insight
```

| Insight Type | Primary Question | Example |
|-------------|-----------------|---------|
| **Trends** | How does a metric change over time? | Daily signups this month |
| **Funnels** | Where do users drop off in a sequence? | Signup-to-first-project conversion |
| **Retention** | Do users come back after an initial action? | Week-over-week app opens |
| **Paths** | What do users do before/after an event? | Pages visited before checkout |
| **Stickiness** | How many days/weeks do users perform an action? | Days per week a user opens the app |

## Building Conversion Funnels

Funnels are the most actionable insight type for product teams. They show exactly where users abandon a multi-step flow.

### Designing Funnel Steps

A funnel is a sequence of events that represents a desired user journey. Each step narrows the population to users who completed that action.

```mermaid
flowchart LR
    A["visited_pricing<br/>100%"] --> B["started_checkout<br/>42%"]
    B --> C["entered_payment<br/>31%"]
    C --> D["completed_purchase<br/>24%"]

    classDef full fill:#e8f5e8,stroke:#1b5e20
    classDef mid fill:#fff3e0,stroke:#ef6c00
    classDef low fill:#ffebee,stroke:#c62828

    class A full
    class B mid
    class C,D low
```

### Creating a Funnel in the UI

1. Navigate to **Insights** and click **New Insight**
2. Select **Funnels** as the insight type
3. Add steps in order:
   - Step 1: `visited_pricing`
   - Step 2: `started_checkout`
   - Step 3: `entered_payment`
   - Step 4: `completed_purchase`
4. Set the **conversion window** (e.g., 7 days)
5. Add **breakdowns** by `plan`, `$browser`, or `utm_source`
6. Save and add to a dashboard

### Creating a Funnel via the API

```typescript
import { PostHog } from 'posthog-node'

const client = new PostHog('YOUR_API_KEY', {
  host: 'https://app.posthog.com'
})

// Query a funnel programmatically via the PostHog API
const response = await fetch('https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/funnel/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
  },
  body: JSON.stringify({
    events: [
      { id: 'visited_pricing', order: 0 },
      { id: 'started_checkout', order: 1 },
      { id: 'entered_payment', order: 2 },
      { id: 'completed_purchase', order: 3 }
    ],
    funnel_window_days: 7,
    breakdown: 'plan',
    date_from: '-30d'
  })
})

const funnelData = await response.json()
console.log('Overall conversion:', funnelData.result)
```

```python
import requests

response = requests.post(
    'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/funnel/',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    json={
        'events': [
            {'id': 'visited_pricing', 'order': 0},
            {'id': 'started_checkout', 'order': 1},
            {'id': 'entered_payment', 'order': 2},
            {'id': 'completed_purchase', 'order': 3},
        ],
        'funnel_window_days': 7,
        'breakdown': 'plan',
        'date_from': '-30d',
    }
)

funnel_data = response.json()
for step in funnel_data['result']:
    print(f"Step {step['order']}: {step['name']} - {step['count']} users")
```

### Funnel Configuration Options

| Option | Description | Recommended Value |
|--------|-------------|-------------------|
| **Conversion window** | Max time between first and last step | 7-14 days for SaaS onboarding |
| **Breakdown** | Split results by a property | `plan`, `utm_source`, `$browser` |
| **Exclusion steps** | Events that disqualify a user | `account_deleted`, `unsubscribed` |
| **Funnel order** | Strict (exact order) vs. unordered | Strict for checkout flows |
| **Aggregation** | Count unique users or events | Unique users for conversion rates |

### Diagnosing Drop-Offs

When a funnel shows a large drop between steps, investigate with these techniques:

1. **Click the drop-off bar** to see the list of users who did not convert
2. **Watch their session recordings** (covered in Chapter 4) to see what they did instead
3. **Add a breakdown** by device, browser, or geography to find platform-specific issues
4. **Check the median time** between steps -- a very long gap may indicate confusion
5. **Create a Path analysis** starting from the drop-off point to see where users went

## Retention Analysis

Retention answers the question: "After users do X for the first time, how many come back and do Y?" It is the single most important metric for product-market fit.

### Retention Table Structure

A retention table shows cohorts (rows) and time periods (columns). Each cell is the percentage of the cohort that returned.

| Cohort (Week) | Week 0 | Week 1 | Week 2 | Week 3 | Week 4 |
|:--------------|:------:|:------:|:------:|:------:|:------:|
| Jan 6 | 100% | 38% | 29% | 24% | 21% |
| Jan 13 | 100% | 41% | 32% | 26% | -- |
| Jan 20 | 100% | 35% | 27% | -- | -- |
| Jan 27 | 100% | 39% | -- | -- | -- |

### Creating Retention Insights

In the PostHog UI:

1. Navigate to **Insights** and select **Retention**
2. Set the **start event** (e.g., `signed_up`)
3. Set the **return event** (e.g., `app_opened` or `project_created`)
4. Choose the **period** (Day, Week, or Month)
5. Optionally filter by cohort, plan, or experiment variant

### Retention Patterns to Watch For

```mermaid
flowchart TD
    subgraph Healthy
        H1["Week 0: 100%"] --> H2["Week 1: 45%"]
        H2 --> H3["Week 4: 30%"]
        H3 --> H4["Week 8: 28%"]
    end

    subgraph Leaky["Leaky Bucket"]
        L1["Week 0: 100%"] --> L2["Week 1: 20%"]
        L2 --> L3["Week 4: 5%"]
        L3 --> L4["Week 8: 1%"]
    end

    subgraph Improving
        I1["Week 0: 100%"] --> I2["Week 1: 25%"]
        I2 --> I3["Week 4: 22%"]
        I3 --> I4["Week 8: 28%"]
    end

    classDef good fill:#e8f5e8,stroke:#1b5e20
    classDef bad fill:#ffebee,stroke:#c62828
    classDef neutral fill:#fff3e0,stroke:#ef6c00

    class H1,H2,H3,H4 good
    class L1,L2,L3,L4 bad
    class I1,I2,I3,I4 neutral
```

| Pattern | Shape | Action |
|---------|-------|--------|
| **Healthy** | Curve flattens above 20-30% | Maintain; focus on growth |
| **Leaky bucket** | Steep decline, never flattens | Fix activation; improve onboarding |
| **Improving** | Later cohorts retain better | Keep shipping; recent changes are working |
| **Smile curve** | Drops then rises | Users rediscover value; investigate why |

## User Paths (Journey Analysis)

Paths show the actual sequences of pages or events users follow. Unlike funnels, which test a specific hypothesis, paths help you discover unknown patterns.

### Path Analysis Types

| Path Type | Starting Point | Use Case |
|-----------|---------------|----------|
| **Paths after event** | A specific event | What do users do after signing up? |
| **Paths before event** | A specific event | What leads users to upgrade? |
| **Full paths** | Any entry point | General navigation patterns |

### Creating a Path Analysis

```typescript
// Query paths via the API
const response = await fetch(
  'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/path/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      path_type: 'paths_after',          // or 'paths_before'
      start_point: 'signed_up',
      step_limit: 5,                     // max depth
      date_from: '-30d',
      include_event_types: ['custom_event', '$pageview'],
      exclude_events: ['$autocapture'],  // reduce noise
      min_edge_weight: 10                // hide rare paths
    })
  }
)
```

### Reading Path Visualizations

Paths produce a Sankey-style diagram. Focus on:

- **Thick branches**: popular paths most users follow
- **Dead ends**: paths that lead to no further action (possible frustration)
- **Loops**: users going back and forth (possible confusion)
- **Short paths to conversion**: the "happy path" you want to optimize for

## Trend Analysis

Trends are the simplest and most frequently used insight type. They plot a metric over time.

### Common Trend Metrics

| Metric | Event | Aggregation | Use |
|--------|-------|------------|-----|
| DAU | `app_opened` | Unique users / day | Daily engagement |
| WAU | `app_opened` | Unique users / week | Weekly engagement |
| Signups | `signed_up` | Total count / day | Growth rate |
| Revenue events | `invoice_paid` | Sum of `amount_cents` / day | Revenue tracking |
| Errors | `api_error_occurred` | Total count / hour | Reliability monitoring |

### Building a Trend in TypeScript

```typescript
// Fetch a trend from the PostHog API
const trendResponse = await fetch(
  'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/insights/trend/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      events: [
        {
          id: 'signed_up',
          math: 'total',         // count every event
          name: 'Signups'
        },
        {
          id: 'app_opened',
          math: 'dau',           // unique users per day
          name: 'DAU'
        }
      ],
      date_from: '-30d',
      interval: 'day',
      display: 'ActionsLineGraph'
    })
  }
)

const trendData = await trendResponse.json()
for (const series of trendData.result) {
  console.log(`${series.label}: ${series.data}`)
}
```

### Trend Formulas

PostHog supports formulas to create composite metrics:

```
# Activation rate
A / B  where A = "onboarding_completed" and B = "signed_up"

# WAU / MAU ratio (stickiness proxy)
A / B  where A = "app_opened" (unique/week) and B = "app_opened" (unique/month)
```

## Stickiness Analysis

Stickiness measures how frequently users perform an action over a time window. It answers: "Out of the users who did X this month, how many did it on 1 day, 2 days, 3 days ... etc.?"

A healthy product has a stickiness distribution that skews right -- many users engage on multiple days rather than just one.

| Days Active in Month | Users | Percentage |
|:-------------------:|:-----:|:----------:|
| 1 | 2,400 | 30% |
| 2-3 | 1,800 | 22% |
| 4-7 | 1,600 | 20% |
| 8-14 | 1,200 | 15% |
| 15+ | 1,000 | 13% |

## Segmentation and Breakdowns

Every insight type supports breakdowns -- splitting results by a property. Breakdowns transform a single number into an actionable comparison.

### Useful Breakdown Properties

| Property | Type | Reveals |
|----------|------|---------|
| `plan` | Person | Conversion differences by plan |
| `utm_source` | Event | Best acquisition channels |
| `$browser` | System | Platform-specific issues |
| `$country_code` | System | Geographic patterns |
| `experiment_variant` | Person | A/B test impact |
| `company` (group) | Group | B2B account behavior |

### Cohort-Based Segmentation

Cohorts let you define reusable user segments for any analysis.

```mermaid
flowchart LR
    subgraph Definition
        A["Users who signed up<br/>in last 30 days"]
        B["Users on growth plan"]
        C["Users who completed<br/>onboarding"]
    end

    subgraph Usage
        D[Funnel Breakdown]
        E[Retention Filter]
        F[Trend Comparison]
    end

    A --> D
    A --> E
    B --> D
    B --> F
    C --> E
    C --> F

    classDef def fill:#e1f5fe,stroke:#01579b
    classDef use fill:#e8f5e8,stroke:#1b5e20

    class A,B,C def
    class D,E,F use
```

### Creating Cohorts

In the PostHog UI:

1. Navigate to **Persons & Groups** then **Cohorts**
2. Click **New Cohort**
3. Define criteria:
   - "Completed event `onboarding_completed` in the last 30 days"
   - AND "Person property `plan` equals `growth`"
4. Name the cohort (e.g., "Activated Growth Users") and save
5. Use it as a filter or breakdown in any insight

```python
import requests

# Create a cohort via the API
response = requests.post(
    'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/cohorts/',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    json={
        'name': 'Activated Growth Users',
        'groups': [
            {
                'properties': [
                    {
                        'key': 'plan',
                        'value': 'growth',
                        'type': 'person'
                    }
                ]
            }
        ],
        'is_static': False
    }
)

cohort = response.json()
print(f"Created cohort: {cohort['name']} (ID: {cohort['id']})")
```

## Lifecycle Analysis

Lifecycle categorizes your users into four groups for each time period:

| Category | Definition | Action |
|----------|-----------|--------|
| **New** | First time performing the event | Optimize acquisition |
| **Returning** | Performed the event this period and the previous period | Celebrate and learn from them |
| **Resurrecting** | Performed the event this period but not the previous period | Understand what brought them back |
| **Dormant** | Performed the event in the previous period but not this period | Win them back with re-engagement |

Lifecycle is especially useful for understanding the composition of your active user base. A growing product has more new and returning users than dormant.

## Putting It All Together: An Analytics Workflow

Here is a practical workflow for investigating a drop in weekly active users:

```mermaid
flowchart TD
    A["WAU dropped 15%<br/>this week"] --> B["Check Trends:<br/>Which event declined?"]
    B --> C["app_opened down<br/>among free users"]
    C --> D["Check Retention:<br/>Is the Jan 20 cohort different?"]
    D --> E["Week-1 retention<br/>dropped from 38% to 25%"]
    E --> F["Check Funnel:<br/>Is onboarding broken?"]
    F --> G["Step 2→3 drop-off<br/>increased 12%"]
    G --> H["Watch Session Recordings<br/>of users who dropped off"]
    H --> I["Users confused by<br/>new onboarding step"]
    I --> J["Fix UX and run<br/>an A/B test"]

    classDef alert fill:#ffebee,stroke:#c62828
    classDef investigate fill:#fff3e0,stroke:#ef6c00
    classDef action fill:#e8f5e8,stroke:#1b5e20

    class A alert
    class B,C,D,E,F,G,H investigate
    class I,J action
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Funnel shows 0% conversion | Events not firing or wrong distinct_id | Verify in Live Events; check ID consistency |
| Retention table is empty | Start event has no matches in date range | Expand date range or check event name |
| Path visualization too noisy | Autocapture events dominating | Exclude `$autocapture`; increase min edge weight |
| Breakdown shows "Other" bucket | Too many unique values | Reduce cardinality; bucket values |
| Numbers don't match other tools | Different attribution or dedup logic | Align on unique-user vs. total-event counting |
| Cohort size seems wrong | Internal/test users included | Filter by `is_test_user != true` |

## Performance Considerations

- **Date range**: Queries over very long date ranges (6+ months) on large datasets can be slow. Use shorter ranges for exploration, then save specific insights.
- **Breakdowns**: Each breakdown multiplies query cost. Limit to 1-2 breakdowns at a time.
- **Sampling**: PostHog supports sampling for exploratory analysis. Enable it in the query builder for faster iteration, then disable for final numbers.
- **Caching**: Saved insights are cached. Dashboards refresh on a schedule rather than on every page load.

## Security and Privacy

- **Filter internal traffic**: Exclude your team's events using an `is_internal` person property or IP-based cohort.
- **Anonymize for sharing**: When sharing insights with external stakeholders, ensure PII is not visible in person lists or recordings.
- **Access controls**: Use PostHog's role-based access to limit who can see person-level data vs. aggregated insights.
- **Data retention**: Set retention policies so old person-level data is purged while aggregated metrics remain.

## Summary

User analytics transforms raw events into product intelligence. Funnels show where users abandon key flows. Retention tables reveal whether your product keeps users coming back. Paths uncover navigation patterns you did not expect. Trends track your KPIs over time. Stickiness and lifecycle round out the picture by showing engagement depth and user composition.

## Key Takeaways

1. **Start with funnels for your core flows** -- onboarding, checkout, and activation are the highest-leverage funnels to build first.
2. **Retention is the ultimate product-market fit metric** -- if Week-4 retention is below 15-20%, focus on activation before growth.
3. **Paths reveal what you did not plan for** -- use them to discover unexpected user behavior and new feature opportunities.
4. **Segment everything** -- a single aggregate number hides the story. Break down by plan, source, and cohort to find the real insight.
5. **Connect quantitative and qualitative** -- when a funnel shows a drop-off, watch the session recordings of those users to understand why.

## Next Steps

You now know how to analyze user behavior quantitatively. But numbers only tell you *what* happened, not *why*. In [Chapter 4: Session Recordings](04-session-recordings.md), you will learn how to watch real user sessions, identify UX friction, and connect qualitative observations to the funnels and retention curves you built here.

---

*Built with insights from the [PostHog](https://github.com/PostHog/posthog) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `classDef`, `fill`, `stroke` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: User Analytics & Funnels` as an operating subsystem inside **PostHog Tutorial: Open Source Product Analytics Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Week`, `json`, `order` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: User Analytics & Funnels` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `classDef`.
2. **Input normalization**: shape incoming data so `fill` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `stroke`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/PostHog/posthog)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `classDef` and `fill` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Event Tracking & Properties](02-event-tracking.md)
- [Next Chapter: Chapter 4: Session Recordings](04-session-recordings.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
