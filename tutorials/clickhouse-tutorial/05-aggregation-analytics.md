---
layout: default
title: "Chapter 5: Aggregation & Analytics"
parent: "ClickHouse Tutorial"
nav_order: 5
---

# Chapter 5: Aggregation & Analytics

Welcome to **Chapter 5: Aggregation & Analytics**. In this part of **ClickHouse Tutorial: High-Performance Analytical Database**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


ClickHouse excels at analytical workloads with its powerful aggregation functions and real-time analytics capabilities. This chapter covers advanced aggregation techniques and analytical patterns for building high-performance analytical applications.

## Advanced Aggregation Functions

### Statistical Aggregations

```sql
-- Statistical analysis functions
SELECT
    category,
    count() as total_count,
    avg(price) as avg_price,
    median(price) as median_price,
    quantile(0.25)(price) as q25_price,
    quantile(0.75)(price) as q75_price,
    stddevPop(price) as std_dev,
    skewnessPop(price) as skewness,
    kurtosisPop(price) as kurtosis
FROM products
GROUP BY category
ORDER BY total_count DESC;

-- Time-series statistical analysis
SELECT
    toStartOfHour(timestamp) as hour,
    count() as events_count,
    avg(response_time) as avg_response,
    quantileExact(0.95)(response_time) as p95_response,
    quantileExact(0.99)(response_time) as p99_response,
    min(response_time) as min_response,
    max(response_time) as max_response
FROM api_logs
WHERE timestamp >= now() - INTERVAL 24 HOUR
GROUP BY hour
ORDER BY hour;
```

### Array and String Aggregations

```sql
-- Array aggregation functions
SELECT
    user_id,
    groupArray(event_type) as event_sequence,
    arrayDistinct(groupArray(event_type)) as unique_events,
    arrayCount(x -> x = 'purchase', groupArray(event_type)) as purchase_count,
    arraySum(groupArray(value)) as total_value
FROM user_events
GROUP BY user_id;

-- String aggregation functions
SELECT
    category,
    groupArrayConcat(',', product_name) as product_list,
    groupArrayConcat('|', tag) as tag_string,
    countDistinct(product_name) as unique_products
FROM products
GROUP BY category;
```

### Custom Aggregation States

```sql
-- Using aggregate state functions
CREATE TABLE user_metrics (
    user_id UInt32,
    date Date,
    page_views UInt32,
    session_duration UInt32
) ENGINE = MergeTree()
ORDER BY (user_id, date);

-- Aggregate states for efficient merging
SELECT
    user_id,
    sumState(page_views) as total_views_state,
    avgState(session_duration) as avg_duration_state,
    countState() as session_count_state
FROM user_metrics
GROUP BY user_id;

-- Merge states across different time periods
SELECT
    user_id,
    sumMerge(total_views_state) as total_views,
    avgMerge(avg_duration_state) as avg_duration,
    countMerge(session_count_state) as total_sessions
FROM (
    SELECT user_id, sumState(page_views) as total_views_state,
           avgState(session_duration) as avg_duration_state,
           countState() as session_count_state
    FROM user_metrics
    WHERE date >= '2024-01-01'
    GROUP BY user_id
) t
GROUP BY user_id;
```

## Real-Time Analytics

### Sliding Window Analytics

```sql
-- Sliding window aggregations
SELECT
    user_id,
    timestamp,
    event_type,
    count() OVER (
        PARTITION BY user_id
        ORDER BY timestamp
        RANGE BETWEEN INTERVAL 1 HOUR PRECEDING AND CURRENT ROW
    ) as events_last_hour,
    sum(value) OVER (
        PARTITION BY user_id
        ORDER BY timestamp
        RANGE BETWEEN INTERVAL 24 HOUR PRECEDING AND CURRENT ROW
    ) as value_last_24h
FROM user_events
ORDER BY user_id, timestamp;

-- Tumbling window analytics
SELECT
    toStartOfHour(timestamp) as hour,
    count() as events_per_hour,
    uniq(user_id) as unique_users,
    sum(value) as total_value,
    avg(value) as avg_value
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY hour
ORDER BY hour DESC;
```

### Continuous Aggregation

```sql
-- Continuous aggregation with materialized views
CREATE MATERIALIZED VIEW hourly_user_stats
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, user_id)
AS SELECT
    toStartOfHour(timestamp) as hour,
    user_id,
    countState() as events_count,
    sumState(value) as total_value,
    avgState(value) as avg_value,
    minState(timestamp) as first_event,
    maxState(timestamp) as last_event
FROM user_events
GROUP BY hour, user_id;

-- Query real-time stats
SELECT
    user_id,
    countMerge(events_count) as total_events,
    sumMerge(total_value) as total_value,
    avgMerge(avg_value) as avg_value,
    minMerge(first_event) as first_event_time,
    maxMerge(last_event) as last_event_time
FROM hourly_user_stats
WHERE hour >= now() - INTERVAL 24 HOUR
GROUP BY user_id
ORDER BY total_events DESC;
```

## Complex Analytical Queries

### Cohort Analysis

```sql
-- User cohort analysis
WITH user_first_events AS (
    SELECT
        user_id,
        min(toDate(timestamp)) as first_date,
        max(toDate(timestamp)) as last_date
    FROM events
    GROUP BY user_id
),
cohorts AS (
    SELECT
        user_id,
        first_date,
        dateDiff('month', first_date, last_date) as cohort_month
    FROM user_first_events
)
SELECT
    toYear(first_date) as cohort_year,
    toMonth(first_date) as cohort_month,
    cohort_month,
    count() as users_in_cohort,
    countIf(cohort_month >= 0) as active_month_0,
    countIf(cohort_month >= 1) as active_month_1,
    countIf(cohort_month >= 2) as active_month_2
FROM cohorts
GROUP BY cohort_year, cohort_month, cohort_month
ORDER BY cohort_year DESC, cohort_month DESC;
```

### Funnel Analysis

```sql
-- Conversion funnel analysis
WITH user_steps AS (
    SELECT
        user_id,
        groupArray(event_type) as event_sequence,
        arrayCount(x -> x = 'page_view', event_sequence) > 0 as step1_page_view,
        arrayCount(x -> x = 'add_to_cart', event_sequence) > 0 as step2_add_to_cart,
        arrayCount(x -> x = 'checkout', event_sequence) > 0 as step3_checkout,
        arrayCount(x -> x = 'purchase', event_sequence) > 0 as step4_purchase
    FROM (
        SELECT user_id, event_type
        FROM user_events
        WHERE timestamp >= '2024-01-01'
        ORDER BY timestamp
    )
    GROUP BY user_id
)
SELECT
    count() as total_users,
    countIf(step1_page_view) as step1_count,
    countIf(step2_add_to_cart) as step2_count,
    countIf(step3_checkout) as step3_count,
    countIf(step4_purchase) as step4_count,
    round(step1_count / total_users * 100, 2) as step1_conversion,
    round(step2_count / step1_count * 100, 2) as step2_conversion,
    round(step3_count / step2_count * 100, 2) as step3_conversion,
    round(step4_count / step3_count * 100, 2) as step4_conversion
FROM user_steps;
```

### Time-Series Forecasting

```sql
-- Simple trend analysis
SELECT
    date,
    sales,
    avg(sales) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d,
    sales - lag(sales) OVER (ORDER BY date) as daily_change,
    (sales - lag(sales, 7) OVER (ORDER BY date)) / lag(sales, 7) OVER (ORDER BY date) * 100 as weekly_change_pct
FROM daily_sales
WHERE date >= '2024-01-01'
ORDER BY date;

-- Seasonal decomposition
SELECT
    toYear(date) as year,
    toMonth(date) as month,
    avg(sales) as monthly_avg,
    avg(sales) OVER (PARTITION BY toMonth(date)) as seasonal_avg,
    avg(sales) - avg(sales) OVER (PARTITION BY toMonth(date)) as seasonal_adjusted
FROM daily_sales
GROUP BY year, month, date
ORDER BY year, month;
```

## Performance Optimization for Analytics

### Pre-computed Aggregations

```sql
-- Pre-compute common aggregations
CREATE MATERIALIZED VIEW product_analytics
ENGINE = SummingMergeTree()
ORDER BY (product_id, date)
AS SELECT
    product_id,
    toDate(timestamp) as date,
    count() as views,
    countIf(event_type = 'purchase') as purchases,
    sumIf(value, event_type = 'purchase') as revenue,
    uniq(user_id) as unique_viewers
FROM product_events
GROUP BY product_id, date;

-- Query optimized analytics
SELECT
    product_id,
    sum(views) as total_views,
    sum(purchases) as total_purchases,
    sum(revenue) as total_revenue,
    sum(unique_viewers) as total_unique_viewers,
    sum(purchases) / sum(views) as conversion_rate
FROM product_analytics
WHERE date >= '2024-01-01'
GROUP BY product_id
ORDER BY total_revenue DESC;
```

### Approximate Aggregations

```sql
-- Approximate distinct counts for large datasets
SELECT
    category,
    count() as total_products,
    uniq(product_id) as exact_unique,
    uniqCombined(product_id) as approx_unique,
    uniqHLL12(product_id) as hll_unique,
    topK(10)(product_name) as top_products
FROM products
GROUP BY category;

-- Approximate quantiles for performance
SELECT
    category,
    quantile(0.5)(price) as median_price,
    quantiles(0.25, 0.75)(price) as quartiles,
    quantileExact(0.95)(price) as exact_p95,
    quantileTDigest(0.95)(price) as approx_p95
FROM products
GROUP BY category;
```

## Advanced Analytical Patterns

### Customer Lifetime Value

```sql
-- Calculate CLV with cohort analysis
WITH user_cohorts AS (
    SELECT
        user_id,
        min(toDate(timestamp)) as cohort_date,
        max(toDate(timestamp)) as last_active_date,
        dateDiff('month', min(toDate(timestamp)), max(toDate(timestamp))) as lifetime_months
    FROM user_events
    GROUP BY user_id
),
user_revenue AS (
    SELECT
        user_id,
        sum(value) as total_revenue,
        countIf(event_type = 'purchase') as total_purchases,
        avg(value) as avg_order_value
    FROM user_events
    WHERE event_type = 'purchase'
    GROUP BY user_id
)
SELECT
    c.cohort_date,
    count() as cohort_size,
    avg(r.total_revenue) as avg_clv,
    quantile(0.5)(r.total_revenue) as median_clv,
    sum(r.total_revenue) as total_cohort_revenue,
    avg(c.lifetime_months) as avg_lifetime_months
FROM user_cohorts c
LEFT JOIN user_revenue r ON c.user_id = r.user_id
GROUP BY c.cohort_date
ORDER BY c.cohort_date DESC;
```

### Product Affinity Analysis

```sql
-- Market basket analysis
WITH user_purchases AS (
    SELECT
        user_id,
        groupArray(product_id) as purchased_products,
        arrayDistinct(groupArray(product_id)) as unique_products
    FROM purchase_events
    WHERE timestamp >= '2024-01-01'
    GROUP BY user_id
),
product_pairs AS (
    SELECT
        arrayJoin(arrayDistinct(
            arrayMap(x -> (x, y), purchased_products, purchased_products)
        )) as product_pair,
        count() as frequency
    FROM user_purchases
    WHERE length(purchased_products) > 1
    GROUP BY product_pair
)
SELECT
    product_pair.1 as product_a,
    product_pair.2 as product_b,
    frequency,
    frequency / (SELECT count() FROM user_purchases) as support
FROM product_pairs
WHERE product_pair.1 < product_pair.2  -- Avoid duplicates
ORDER BY frequency DESC
LIMIT 20;
```

## Real-Time Dashboards

### Live Metrics Aggregation

```sql
-- Real-time dashboard queries
CREATE TABLE dashboard_metrics (
    metric_name String,
    value Float64,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (metric_name, timestamp);

-- Live aggregation view
CREATE MATERIALIZED VIEW live_metrics
ENGINE = AggregatingMergeTree()
ORDER BY (metric_name, minute)
AS SELECT
    metric_name,
    toStartOfMinute(timestamp) as minute,
    countState() as count,
    avgState(value) as avg_value,
    maxState(value) as max_value,
    minState(value) as min_value
FROM dashboard_metrics
GROUP BY metric_name, minute;

-- Real-time queries
SELECT
    metric_name,
    countMerge(count) as events_count,
    avgMerge(avg_value) as current_avg,
    maxMerge(max_value) as peak_value,
    minMerge(min_value) as min_value
FROM live_metrics
WHERE minute >= now() - INTERVAL 5 MINUTE
GROUP BY metric_name;
```

### Anomaly Detection

```sql
-- Statistical anomaly detection
WITH baseline_stats AS (
    SELECT
        metric_name,
        avg(value) as baseline_avg,
        stddevPop(value) as baseline_std
    FROM dashboard_metrics
    WHERE timestamp >= now() - INTERVAL 7 DAY
        AND timestamp < now() - INTERVAL 1 HOUR
    GROUP BY metric_name
),
current_values AS (
    SELECT
        metric_name,
        toStartOfMinute(timestamp) as minute,
        avg(value) as current_avg
    FROM dashboard_metrics
    WHERE timestamp >= now() - INTERVAL 1 HOUR
    GROUP BY metric_name, minute
)
SELECT
    c.metric_name,
    c.minute,
    c.current_avg,
    b.baseline_avg,
    b.baseline_std,
    abs(c.current_avg - b.baseline_avg) / b.baseline_std as z_score,
    if(abs(c.current_avg - b.baseline_avg) / b.baseline_std > 3, 'ANOMALY', 'NORMAL') as status
FROM current_values c
JOIN baseline_stats b ON c.metric_name = b.metric_name
ORDER BY z_score DESC;
```

## What We've Accomplished

Outstanding! 🎯 You've mastered ClickHouse analytics:

1. **Advanced Aggregations** - Statistical and array functions
2. **Real-Time Analytics** - Sliding windows and continuous aggregation
3. **Complex Analytics** - Cohort, funnel, and forecasting analysis
4. **Performance Optimization** - Pre-computed and approximate aggregations
5. **Advanced Patterns** - CLV, affinity analysis, and real-time dashboards
6. **Anomaly Detection** - Statistical monitoring and alerting

## Next Steps

With powerful analytics capabilities in place, let's explore how to scale ClickHouse across multiple servers. In [Chapter 6: Distributed ClickHouse](06-distributed-setup.md), we'll cover clustering, sharding, and high availability configurations.

---

**Practice what you've learned:**
1. Implement a real-time dashboard for user behavior analytics
2. Create cohort analysis for user engagement metrics
3. Set up anomaly detection for key business metrics
4. Build a product recommendation system using affinity analysis

*What analytical challenge are you most excited to tackle with ClickHouse?* 📈

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `user_id`, `timestamp` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Aggregation & Analytics` as an operating subsystem inside **ClickHouse Tutorial: High-Performance Analytical Database**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `GROUP`, `ORDER`, `date` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Aggregation & Analytics` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `user_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `timestamp`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ClickHouse/ClickHouse)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `SELECT` and `user_id` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Query Optimization](04-query-optimization.md)
- [Next Chapter: Chapter 6: Distributed ClickHouse](06-distributed-setup.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
