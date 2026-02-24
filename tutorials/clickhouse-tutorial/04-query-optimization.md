---
layout: default
title: "Chapter 4: Query Optimization"
parent: "ClickHouse Tutorial"
nav_order: 4
---

# Chapter 4: Query Optimization

Welcome to **Chapter 4: Query Optimization**. In this part of **ClickHouse Tutorial: High-Performance Analytical Database**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


ClickHouse is renowned for its blazing-fast analytical queries, but writing optimal queries requires understanding its query execution engine. This chapter covers the techniques and best practices for maximizing query performance.

## Understanding ClickHouse Query Execution

### Query Processing Pipeline

```sql
-- ClickHouse query execution flow
SELECT
    toDate(timestamp) as date,
    count() as events,
    sum(value) as total_value
FROM events
WHERE timestamp >= '2024-01-01'
    AND event_type = 'purchase'
GROUP BY date
ORDER BY date DESC;

-- Execution steps:
-- 1. Parse query and validate syntax
-- 2. Analyze table structure and indexes
-- 3. Generate execution plan
-- 4. Optimize plan based on statistics
-- 5. Execute in parallel across shards
-- 6. Merge and return results
```

### Index Utilization

```sql
-- Primary key index usage
EXPLAIN SELECT *
FROM events
WHERE timestamp >= '2024-01-01'
    AND timestamp < '2024-02-01';

-- Sparse index for selective queries
EXPLAIN SELECT count()
FROM large_table
WHERE category = 'electronics'
    AND price > 100;

-- Index statistics
SELECT
    database,
    table,
    primary_key,
    sorting_key,
    partition_key
FROM system.tables
WHERE database = 'your_db';
```

## Query Optimization Techniques

### Predicate Pushdown

```sql
-- Good: Filters applied early
SELECT user_id, count() as orders
FROM orders
WHERE created_at >= '2024-01-01'
    AND status = 'completed'
    AND total > 50
GROUP BY user_id;

-- Better: Pre-filter with subquery
SELECT user_id, orders_count
FROM (
    SELECT user_id, count() as orders_count
    FROM orders
    WHERE created_at >= '2024-01-01'
        AND status = 'completed'
    GROUP BY user_id
) t
WHERE orders_count > 10;
```

### Join Optimization

```sql
-- Optimize join order
SELECT u.name, count(o.id) as orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name;

-- Use IN instead of JOIN for small datasets
SELECT user_id, count() as orders
FROM orders
WHERE user_id IN (
    SELECT id FROM users
    WHERE created_at >= '2024-01-01'
);

-- Pre-compute aggregations
CREATE MATERIALIZED VIEW user_stats
ENGINE = AggregatingMergeTree()
ORDER BY user_id
AS SELECT
    user_id,
    countState() as orders_count,
    sumState(total) as total_sum
FROM orders
GROUP BY user_id;
```

### Aggregation Optimization

```sql
-- Use aggregate functions efficiently
SELECT
    toDate(timestamp) as date,
    argMax(event_type, timestamp) as last_event,
    countIf(event_type = 'login') as logins,
    sumIf(value, event_type = 'purchase') as revenue
FROM events
GROUP BY date;

-- Combine aggregations
SELECT
    user_id,
    count() as total_events,
    countIf(event_type = 'login') as logins,
    countIf(event_type = 'purchase') as purchases,
    sumIf(value, event_type = 'purchase') as total_spent
FROM user_events
GROUP BY user_id;
```

## Advanced Query Patterns

### Window Functions

```sql
-- Running totals and rankings
SELECT
    user_id,
    timestamp,
    value,
    sum(value) OVER (PARTITION BY user_id ORDER BY timestamp) as running_total,
    row_number() OVER (PARTITION BY user_id ORDER BY timestamp DESC) as recency_rank
FROM user_transactions
ORDER BY user_id, timestamp;

-- Moving averages
SELECT
    date,
    revenue,
    avg(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as weekly_avg,
    avg(revenue) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as monthly_avg
FROM daily_revenue
ORDER BY date;
```

### Array and Nested Operations

```sql
-- Array operations
SELECT
    user_id,
    arrayDistinct(arrayConcat(events, new_events)) as all_events,
    arrayCount(x -> x = 'login', events) as login_count,
    arraySum(arrayMap(x -> if(x = 'purchase', 1, 0), events)) as purchase_count
FROM user_sessions;

-- Nested structure queries
SELECT
    product_id,
    variants.variant_id,
    variants.price,
    variants.stock
FROM products
ARRAY JOIN variants;
```

### Time-Series Analysis

```sql
-- Time bucketing and analysis
SELECT
    toStartOfHour(timestamp) as hour,
    count() as events_per_hour,
    quantile(0.95)(response_time) as p95_response_time,
    avg(response_time) as avg_response_time
FROM api_logs
WHERE timestamp >= now() - INTERVAL 24 HOUR
GROUP BY hour
ORDER BY hour;

-- Gap analysis
SELECT
    user_id,
    timestamp as current_time,
    lag(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as prev_time,
    timestamp - lag(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as time_gap
FROM user_actions
ORDER BY user_id, timestamp;
```

## Query Performance Monitoring

### EXPLAIN Analysis

```sql
-- Analyze query execution plan
EXPLAIN SELECT
    toDate(timestamp) as date,
    count() as events,
    uniq(user_id) as unique_users
FROM events
WHERE timestamp >= '2024-01-01'
GROUP BY date;

-- Index usage analysis
EXPLAIN INDEXES = 1
SELECT * FROM large_table
WHERE category = 'electronics'
    AND price BETWEEN 100 AND 1000;

-- Pipeline analysis
EXPLAIN PIPELINE
SELECT count()
FROM events
WHERE event_type = 'login';
```

### Performance Metrics

```sql
-- Query performance statistics
SELECT
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    result_rows,
    result_bytes,
    memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
    AND query_duration_ms > 100
ORDER BY query_duration_ms DESC
LIMIT 20;

-- System resource usage
SELECT
    metric,
    value,
    description
FROM system.metrics
WHERE metric LIKE '%query%'
    OR metric LIKE '%memory%'
    OR metric LIKE '%cpu%';
```

## Query Optimization Best Practices

### Data Type Optimization

```sql
-- Use appropriate data types
CREATE TABLE optimized_events (
    timestamp DateTime CODEC(Delta, ZSTD),  -- Compress timestamps
    user_id UInt32,                         -- Unsigned for IDs
    event_type LowCardinality(String),      -- Low cardinality strings
    value Nullable(Float32),               -- Nullable for optional values
    metadata String CODEC(ZSTD)            -- Compress large strings
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id);

-- Optimize numeric precision
SELECT
    user_id,
    toUInt8(ceil(rating)) as rating_int,   -- Reduce precision
    toFloat32(average_score) as score_float -- Use 32-bit floats
FROM user_ratings;
```

### Query Refactoring

```sql
-- Avoid full table scans
SELECT count()
FROM large_table
WHERE date_column >= '2024-01-01';  -- Uses index

-- Use sampling for approximate results
SELECT count()
FROM large_table
SAMPLE 0.1;  -- Sample 10% of data

-- Pre-compute expensive calculations
CREATE MATERIALIZED VIEW daily_stats
ENGINE = AggregatingMergeTree()
ORDER BY date
AS SELECT
    date,
    uniqState(user_id) as unique_users,
    sumState(amount) as total_amount
FROM transactions
GROUP BY date;
```

### Distributed Query Optimization

```sql
-- Optimize distributed queries
SELECT
    shardNum() as shard,
    count() as local_count,
    sum(amount) as local_sum
FROM distributed_table
GROUP BY shardNum();

-- Use distributed subqueries
SELECT user_id, count()
FROM distributed_events
WHERE user_id IN (
    SELECT user_id
    FROM distributed_users
    WHERE status = 'active'
)
GROUP BY user_id;
```

## Performance Troubleshooting

### Common Issues

```sql
-- Identify slow queries
SELECT
    query_id,
    query,
    query_duration_ms,
    read_rows,
    memory_usage
FROM system.query_log
WHERE query_duration_ms > 10000  -- > 10 seconds
ORDER BY query_duration_ms DESC;

-- Memory usage analysis
SELECT
    query_id,
    peak_memory_usage,
    memory_usage,
    query
FROM system.query_log
WHERE peak_memory_usage > 1000000000  -- > 1GB
ORDER BY peak_memory_usage DESC;

-- Disk I/O analysis
SELECT
    query_id,
    read_bytes,
    written_bytes,
    query
FROM system.query_log
ORDER BY read_bytes DESC;
```

### Optimization Strategies

```sql
-- Query settings optimization
SELECT count()
FROM large_table
SETTINGS
    max_threads = 8,
    max_memory_usage = 10000000000,
    merge_max_block_size = 8192,
    read_overflow_mode = 'break';

-- Use query cache
SELECT *
FROM table_with_cache
SETTINGS
    use_query_cache = 1,
    query_cache_ttl = 3600;  -- 1 hour TTL

-- Optimize for specific workloads
SELECT *
FROM analytics_table
SETTINGS
    optimize_read_in_order = 1,      -- Read in order
    optimize_aggregation_in_order = 1, -- Aggregate in order
    optimize_move_to_prewhere = 1;   -- Move filters to prewhere
```

## Advanced Optimization Techniques

### Query Result Caching

```sql
-- Enable query result cache
SET query_cache_store_results = 1;

-- Cache expensive aggregations
SELECT
    toDate(timestamp) as date,
    count() as daily_count,
    sum(amount) as daily_sum
FROM transactions
WHERE timestamp >= '2024-01-01'
GROUP BY date
SETTINGS
    use_query_cache = 1,
    query_cache_min_query_duration = 1000;  -- Cache queries > 1s
```

### Parallel Query Execution

```sql
-- Force parallel execution
SELECT count()
FROM large_table
SETTINGS
    max_threads = 16,
    max_distributed_connections = 8,
    distributed_group_by_no_merge = 1;

-- Control parallelism per query
SELECT
    group,
    count() as cnt,
    sum(value) as total
FROM distributed_table
GROUP BY group
SETTINGS
    max_threads = 4,
    group_by_two_level_threshold = 100000;
```

## What We've Accomplished

Fantastic! 🚀 You've mastered ClickHouse query optimization:

1. **Query Execution Understanding** - How ClickHouse processes queries
2. **Index Utilization** - Leveraging primary keys and sparse indexes
3. **Predicate Pushdown** - Filtering data early in the pipeline
4. **Join Optimization** - Efficient multi-table queries
5. **Aggregation Techniques** - Fast analytical computations
6. **Advanced Patterns** - Window functions and time-series analysis
7. **Performance Monitoring** - Tracking and troubleshooting queries
8. **Optimization Strategies** - Advanced tuning techniques

## Next Steps

With optimized queries running efficiently, let's explore ClickHouse's powerful aggregation and analytics capabilities. In [Chapter 5: Aggregation & Analytics](05-aggregation-analytics.md), we'll dive into advanced analytical functions and real-time analytics patterns.

---

**Practice what you've learned:**
1. Analyze a slow query using EXPLAIN and optimize it
2. Implement window functions for time-series analysis
3. Create a materialized view for expensive aggregations
4. Set up query performance monitoring for your workload

*What's the most complex analytical query you're planning to optimize?* ⚡

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `user_id`, `timestamp` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Query Optimization` as an operating subsystem inside **ClickHouse Tutorial: High-Performance Analytical Database**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `WHERE`, `count`, `ORDER` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Query Optimization` usually follows a repeatable control path:

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
- [Previous Chapter: Chapter 3: Data Ingestion & ETL](03-data-ingestion.md)
- [Next Chapter: Chapter 5: Aggregation & Analytics](05-aggregation-analytics.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
