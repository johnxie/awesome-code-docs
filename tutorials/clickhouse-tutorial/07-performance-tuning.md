---
layout: default
title: "Chapter 7: Performance Tuning"
parent: "ClickHouse Tutorial"
nav_order: 7
---

# Chapter 7: Performance Tuning

Welcome to **Chapter 7: Performance Tuning**. In this part of **ClickHouse Tutorial: High-Performance Analytical Database**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Performance tuning is critical for maximizing ClickHouse's analytical capabilities. This chapter covers advanced optimization techniques, memory management, and system-level tuning for production workloads.

## System-Level Optimization

### Server Configuration Tuning

```xml
<!-- Optimized ClickHouse server configuration -->
<clickhouse>
    <!-- Memory Settings -->
    <max_memory_usage>107374182400</max_memory_usage>  <!-- 100GB -->
    <max_memory_usage_for_user>85899345920</max_memory_usage_for_user>  <!-- 80GB -->
    <max_memory_usage_for_all_queries>64424509440</max_memory_usage_for_all_queries>  <!-- 60GB -->

    <!-- Thread Settings -->
    <max_threads>32</max_threads>
    <max_insert_threads>8</max_insert_threads>
    <background_pool_size>16</background_pool_size>

    <!-- Cache Settings -->
    <uncompressed_cache_size>2147483648</uncompressed_cache_size>  <!-- 2GB -->
    <mark_cache_size>2147483648</mark_cache_size>  <!-- 2GB -->
    <mmap_cache_size>1073741824</mmap_cache_size>  <!-- 1GB -->

    <!-- Merge Settings -->
    <merge_max_block_size>8192</merge_max_block_size>
    <merge_threads>8</merge_threads>
    <merge_tree>
        <max_parts_in_total>10000</max_parts_in_total>
        <max_parts_to_merge_at_once>100</max_parts_to_merge_at_once>
    </merge_tree>
</clickhouse>
```

### Hardware Optimization

```bash
# CPU optimization
echo "performance" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Memory optimization
echo "always" > /sys/kernel/mm/transparent_hugepage/enabled
echo "madvise" > /sys/kernel/mm/transparent_hugepage/defrag

# Disk optimization
echo "deadline" > /sys/block/sda/queue/scheduler
echo "1024" > /sys/block/sda/queue/nr_requests
echo "1024" > /sys/block/sda/queue/read_ahead_kb

# Network optimization
echo "4096 87380 6291456" > /proc/sys/net/ipv4/tcp_rmem
echo "4096 87380 6291456" > /proc/sys/net/ipv4/tcp_wmem
```

## Query-Level Optimizations

### Advanced Query Settings

```sql
-- Global query optimization settings
SET max_threads = 16;
SET max_memory_usage = 10000000000;  -- 10GB
SET max_bytes_before_external_group_by = 5000000000;  -- 5GB
SET max_bytes_before_external_sort = 5000000000;  -- 5GB
SET max_result_rows = 1000000;
SET max_result_bytes = 100000000;  -- 100MB

-- Execute optimized query
SELECT
    toDate(timestamp) as date,
    count() as events,
    uniq(user_id) as unique_users,
    sum(value) as total_value
FROM events
WHERE timestamp >= '2024-01-01'
    AND event_type IN ('login', 'purchase')
GROUP BY date
ORDER BY date DESC
SETTINGS
    optimize_read_in_order = 1,
    optimize_aggregation_in_order = 1,
    optimize_move_to_prewhere = 1,
    read_overflow_mode = 'break';
```

### Prewhere Optimization

```sql
-- Prewhere for selective filtering
SELECT
    user_id,
    count() as actions,
    sum(value) as total_value
FROM user_events
PREWHERE timestamp >= '2024-01-01'  -- Filters applied before reading columns
    AND event_type = 'purchase'
WHERE user_id IN (SELECT user_id FROM active_users)  -- Additional filtering
GROUP BY user_id
ORDER BY total_value DESC;

-- Prewhere with multiple conditions
SELECT
    user_id,
    event_type,
    count() as count,
    avg(value) as avg_value
FROM events
PREWHERE timestamp >= '2024-01-01'
    AND user_id % 100 = 0  -- Selective user sampling
WHERE event_type IN ('view', 'click', 'purchase')
GROUP BY user_id, event_type;
```

## Memory Management

### Memory-Efficient Aggregations

```sql
-- Memory-efficient group by
SELECT
    category,
    count() as total,
    sum(amount) as total_amount,
    avg(amount) as avg_amount
FROM transactions
GROUP BY category
SETTINGS
    max_bytes_before_external_group_by = 1000000000,  -- 1GB
    group_by_two_level_threshold = 100000,
    group_by_two_level_threshold_bytes = 100000000;   -- 100MB

-- External aggregation for large datasets
SELECT
    user_id,
    count() as events,
    sum(value) as total_value
FROM large_events_table
GROUP BY user_id
SETTINGS
    max_memory_usage = 2000000000,  -- 2GB limit
    max_bytes_before_external_group_by = 500000000;  -- 500MB
```

### Memory Monitoring

```sql
-- Monitor memory usage
SELECT
    query_id,
    query,
    memory_usage,
    peak_memory_usage,
    ProfileEvents['MemoryTrackerAlloc'] as memory_allocated,
    ProfileEvents['MemoryTrackerFree'] as memory_freed
FROM system.query_log
WHERE type = 'QueryFinish'
    AND peak_memory_usage > 1000000000  -- > 1GB
ORDER BY peak_memory_usage DESC;

-- Real-time memory statistics
SELECT
    metric,
    value,
    description
FROM system.metrics
WHERE metric LIKE '%memory%'
    OR metric LIKE '%alloc%';
```

## Storage Optimization

### Compression Tuning

```sql
-- Optimize compression for different data types
CREATE TABLE optimized_events (
    timestamp DateTime CODEC(Delta, ZSTD(6)),
    user_id UInt32 CODEC(LZ4),
    event_type LowCardinality(String) CODEC(ZSTD(3)),
    message String CODEC(ZSTD(9)),  -- Higher compression for text
    value Nullable(Float64) CODEC(Gorilla)
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id)
SETTINGS
    min_rows_for_wide_part = 0,      -- Force wide parts
    min_bytes_for_wide_part = 0,
    index_granularity = 8192;

-- Compression ratio analysis
SELECT
    database,
    table,
    sum(bytes) as uncompressed_bytes,
    sum(compressed_bytes) as compressed_bytes,
    sum(compressed_bytes) / sum(bytes) as compression_ratio
FROM system.columns
WHERE database = 'your_db'
GROUP BY database, table
ORDER BY compression_ratio;
```

### Index Optimization

```sql
-- Granular indexing strategy
CREATE TABLE indexed_events (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    category LowCardinality(String),
    value Float64,
    metadata String
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id, category)
SETTINGS
    index_granularity = 8192,        -- Smaller granules = faster queries
    merge_max_block_size = 8192,
    min_rows_for_wide_part = 0;

-- Skip indexes for selective queries
CREATE TABLE skip_index_events (
    timestamp DateTime,
    user_id UInt32,
    event_type LowCardinality(String),
    status LowCardinality(String),
    value Float64
) ENGINE = MergeTree()
ORDER BY timestamp
SETTINGS
    index_granularity = 8192;

-- Analyze index effectiveness
SELECT
    database,
    table,
    name,
    type,
    granularity,
    num_parts,
    marks_count
FROM system.columns
WHERE database = 'your_db'
    AND type LIKE '%Index%';
```

## Query Result Caching

### Query Cache Configuration

```xml
<!-- Enable query result cache -->
<clickhouse>
    <query_cache>
        <max_size_in_bytes>1073741824</max_size_in_bytes>  <!-- 1GB -->
        <max_entries>10000</max_entries>
        <max_entry_size_in_bytes>104857600</max_entry_size_in_bytes>  <!-- 100MB -->
        <ttl>3600000</ttl>  <!-- 1 hour -->
    </query_cache>
</clickhouse>
```

### Cache Usage

```sql
-- Enable query caching
SET query_cache_store_results = 1;
SET query_cache_ttl = 3600;  -- 1 hour TTL

-- Cache expensive aggregations
SELECT
    toDate(timestamp) as date,
    count() as daily_events,
    uniq(user_id) as daily_users,
    sum(value) as daily_value
FROM events
WHERE timestamp >= '2024-01-01'
GROUP BY date
SETTINGS
    use_query_cache = 1,
    query_cache_min_query_duration = 5000;  -- Cache queries > 5s

-- Monitor cache performance
SELECT
    ProfileEvents['QueryCacheHits'] as cache_hits,
    ProfileEvents['QueryCacheMisses'] as cache_misses,
    ProfileEvents['QueryCacheHits'] / (ProfileEvents['QueryCacheHits'] + ProfileEvents['QueryCacheMisses']) as hit_rate
FROM system.query_log
WHERE query_id = 'your_query_id';
```

## Advanced Optimization Techniques

### Parallel Processing

```sql
-- Maximize parallel execution
SELECT
    category,
    count() as total,
    sum(amount) as total_amount,
    avg(amount) as avg_amount
FROM large_transactions
GROUP BY category
SETTINGS
    max_threads = 32,
    max_distributed_connections = 8,
    distributed_group_by_no_merge = 0,
    optimize_distributed_group_by_sharding_key = 1;

-- Parallel aggregation
SELECT
    toStartOfHour(timestamp) as hour,
    count() as events_per_hour,
    uniq(user_id) as unique_users_per_hour
FROM distributed_events
GROUP BY hour
SETTINGS
    max_parallel_replicas = 3,
    cluster = 'analytics_cluster';
```

### Pre-computed Views

```sql
-- Materialized view for real-time analytics
CREATE MATERIALIZED VIEW realtime_user_stats
ENGINE = AggregatingMergeTree()
ORDER BY (user_id, minute)
AS SELECT
    user_id,
    toStartOfMinute(timestamp) as minute,
    countState() as events_count,
    sumState(value) as total_value,
    avgState(value) as avg_value
FROM user_events
GROUP BY user_id, minute;

-- Query pre-computed stats
SELECT
    user_id,
    countMerge(events_count) as total_events,
    sumMerge(total_value) as total_value,
    avgMerge(avg_value) as avg_value
FROM realtime_user_stats
WHERE minute >= now() - INTERVAL 1 HOUR
GROUP BY user_id
ORDER BY total_events DESC;
```

### Approximate Query Processing

```sql
-- Approximate distinct counts
SELECT
    approx_count_distinct(user_id) as approx_unique_users,
    uniqCombined(user_id) as exact_unique_users
FROM events
SAMPLE 0.1;  -- Sample 10% of data

-- Approximate quantiles
SELECT
    quantileTDigest(0.5)(response_time) as median_response,
    quantileTDigest(0.95)(response_time) as p95_response,
    quantileTDigest(0.99)(response_time) as p99_response
FROM api_logs
WHERE timestamp >= now() - INTERVAL 1 HOUR;

-- Approximate top-k
SELECT
    topK(10)(product_name) as top_products,
    topKWeighted(10)(product_name, sales) as top_by_sales
FROM product_sales;
```

## Performance Monitoring and Troubleshooting

### System Performance Metrics

```sql
-- Comprehensive performance monitoring
SELECT
    query_id,
    query_duration_ms,
    read_rows,
    read_bytes,
    written_rows,
    written_bytes,
    memory_usage,
    peak_memory_usage,
    ProfileEvents['OSCPUVirtualTimeMicroseconds'] as cpu_time,
    ProfileEvents['OSReadBytes'] as disk_read,
    ProfileEvents['OSWriteBytes'] as disk_write
FROM system.query_log
WHERE type = 'QueryFinish'
    AND query_duration_ms > 1000
ORDER BY query_duration_ms DESC;

-- System resource usage
SELECT
    metric,
    value,
    description
FROM system.metrics
WHERE metric LIKE '%thread%'
    OR metric LIKE '%memory%'
    OR metric LIKE '%cpu%';
```

### Query Profiling

```sql
-- Enable query profiling
SET send_logs_level = 'trace';

-- Profile specific query
SELECT
    toDate(timestamp) as date,
    count() as events
FROM events
WHERE timestamp >= '2024-01-01'
GROUP BY date
SETTINGS
    log_queries = 1,
    log_queries_min_type = 'QUERY_FINISH';

-- Analyze query execution details
SELECT
    query_id,
    query,
    event_time,
    event_type,
    message
FROM system.query_log
WHERE query_id = 'your_query_id'
ORDER BY event_time;
```

### Performance Diagnostics

```sql
-- Identify slow queries
SELECT
    query,
    query_duration_ms,
    read_rows,
    memory_usage,
    ProfileEvents['MergeTreeDataSelectExecutorThreads'] as threads_used
FROM system.query_log
WHERE type = 'QueryFinish'
    AND query_duration_ms > 5000
ORDER BY query_duration_ms DESC;

-- Analyze merge performance
SELECT
    database,
    table,
    elapsed,
    progress,
    num_parts,
    source_part_names,
    result_part_name
FROM system.merges
WHERE database = 'your_db'
ORDER BY elapsed DESC;

-- Disk I/O analysis
SELECT
    ProfileEvents['OSReadBytes'] as total_read,
    ProfileEvents['OSWriteBytes'] as total_write,
    ProfileEvents['OSReadChars'] as read_operations,
    ProfileEvents['OSWriteChars'] as write_operations
FROM system.query_log
WHERE query_id = 'your_query_id';
```

## Automated Performance Tuning

### Adaptive Query Optimization

```sql
-- Adaptive settings based on query characteristics
SELECT
    CASE
        WHEN read_rows > 100000000 THEN 'large_dataset'
        WHEN memory_usage > 1000000000 THEN 'high_memory'
        WHEN query_duration_ms > 30000 THEN 'slow_query'
        ELSE 'normal'
    END as query_type,
    *
FROM (
    SELECT
        query_id,
        query,
        read_rows,
        memory_usage,
        query_duration_ms
    FROM system.query_log
    WHERE type = 'QueryFinish'
) t;
```

### Automated Tuning Recommendations

```sql
-- Generate tuning recommendations
WITH query_stats AS (
    SELECT
        query_id,
        query_duration_ms,
        read_rows,
        memory_usage,
        peak_memory_usage
    FROM system.query_log
    WHERE type = 'QueryFinish'
        AND query_duration_ms > 1000
)
SELECT
    CASE
        WHEN memory_usage > peak_memory_usage * 0.8 THEN 'Consider increasing max_memory_usage'
        WHEN read_rows > 10000000 THEN 'Consider adding more indexes or sampling'
        WHEN query_duration_ms > 30000 THEN 'Consider query optimization or caching'
        ELSE 'Query performance is good'
    END as recommendation,
    count() as query_count,
    avg(query_duration_ms) as avg_duration
FROM query_stats
GROUP BY recommendation;
```

## Production Deployment Optimization

### Resource Management

```xml
<!-- Production resource configuration -->
<clickhouse>
    <!-- CPU Optimization -->
    <max_threads>64</max_threads>
    <background_pool_size>32</background_pool_size>

    <!-- Memory Management -->
    <max_memory_usage>274877906944</max_memory_usage>  <!-- 256GB -->
    <max_memory_usage_for_user>219902325555</max_memory_usage_for_user>  <!-- 200GB -->

    <!-- Storage Optimization -->
    <merge_tree>
        <max_parts_in_total>50000</max_parts_in_total>
        <max_parts_to_merge_at_once>300</max_parts_to_merge_at_once>
    </merge_tree>

    <!-- Network Optimization -->
    <max_distributed_connections>32</max_distributed_connections>
    <distributed_connections_pool_size>16</distributed_connections_pool_size>
</clickhouse>
```

### Monitoring Integration

```sql
-- Export metrics to monitoring system
SELECT
    toUnixTimestamp(now()) as timestamp,
    'clickhouse_performance' as metric_type,
    arrayJoin([
        ('query_count', toString(count())),
        ('avg_query_time', toString(avg(query_duration_ms))),
        ('max_memory_usage', toString(max(memory_usage))),
        ('total_read_bytes', toString(sum(read_bytes)))
    ]) as metric
FROM system.query_log
WHERE type = 'QueryFinish'
    AND event_time >= now() - INTERVAL 1 MINUTE
GROUP BY metric_type;
```

## What We've Accomplished

Brilliant! ⚡ You've mastered ClickHouse performance tuning:

1. **System-Level Optimization** - Server config and hardware tuning
2. **Query-Level Optimizations** - Advanced query settings and prewhere
3. **Memory Management** - Efficient aggregations and monitoring
4. **Storage Optimization** - Compression and indexing strategies
5. **Query Result Caching** - Cache configuration and usage
6. **Advanced Techniques** - Parallel processing and pre-computed views
7. **Performance Monitoring** - Comprehensive diagnostics and profiling
8. **Automated Tuning** - Adaptive optimization and recommendations
9. **Production Deployment** - Resource management and monitoring integration

## Next Steps

With your ClickHouse deployment fully optimized, let's focus on enterprise features and production deployment strategies. In [Chapter 8: Production Deployment](08-production-deployment.md), we'll cover backup strategies, security, monitoring, and enterprise-grade deployment patterns.

---

**Practice what you've learned:**
1. Tune a slow query using the techniques from this chapter
2. Set up comprehensive performance monitoring
3. Implement query result caching for your workload
4. Create an automated performance tuning system

*What's the biggest performance bottleneck you're currently facing?* 🚀

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `user_id`, `WHERE` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Performance Tuning` as an operating subsystem inside **ClickHouse Tutorial: High-Performance Analytical Database**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `timestamp`, `system`, `ProfileEvents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Performance Tuning` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `user_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `WHERE`.
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
- [Previous Chapter: Chapter 6: Distributed ClickHouse](06-distributed-setup.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
