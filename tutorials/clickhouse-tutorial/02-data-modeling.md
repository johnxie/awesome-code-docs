---
layout: default
title: "Chapter 2: Data Modeling & Schemas"
parent: "ClickHouse Tutorial"
nav_order: 2
---

# Chapter 2: Data Modeling & Schemas

Welcome to **Chapter 2: Data Modeling & Schemas**. In this part of **ClickHouse Tutorial: High-Performance Analytical Database**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! Now that you have ClickHouse up and running, let's explore how to design efficient data schemas that take advantage of ClickHouse's unique architecture. Proper data modeling is crucial for achieving the lightning-fast query performance that ClickHouse is known for.

## Understanding ClickHouse Storage Engine

### MergeTree Family

ClickHouse's primary storage engine is the MergeTree family, designed specifically for analytical workloads:

```sql
-- Basic MergeTree table
CREATE TABLE events (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id);

-- Optimized for time-series data
CREATE TABLE metrics (
    timestamp DateTime,
    metric_name String,
    value Float64,
    tags Map(String, String)
) ENGINE = MergeTree()
ORDER BY (timestamp, metric_name)
TTL timestamp + INTERVAL 30 DAY; -- Automatic data cleanup
```

### Table Engines Overview

```sql
-- ReplacingMergeTree for deduplication
CREATE TABLE user_sessions (
    user_id UInt32,
    session_id String,
    start_time DateTime,
    end_time DateTime,
    events Array(String)
) ENGINE = ReplacingMergeTree()
ORDER BY (user_id, session_id);

-- SummingMergeTree for pre-aggregated data
CREATE TABLE hourly_stats (
    hour DateTime,
    category String,
    count UInt64,
    sum_value Float64
) ENGINE = SummingMergeTree()
ORDER BY (hour, category);

-- AggregatingMergeTree for complex aggregations
CREATE TABLE user_aggregates (
    user_id UInt32,
    date Date,
    visits UInt64,
    page_views UInt64,
    unique_pages UInt32
) ENGINE = AggregatingMergeTree()
ORDER BY (user_id, date);
```

## Data Types in ClickHouse

### Numeric Types

```sql
-- Integer types
CREATE TABLE measurements (
    id UInt32,           -- Unsigned 32-bit integer
    sensor_id Int16,     -- Signed 16-bit integer
    reading Float32,     -- 32-bit float
    precision Float64    -- 64-bit float (double)
) ENGINE = MergeTree()
ORDER BY id;

-- Fixed-point decimals
CREATE TABLE financial (
    account_id UInt32,
    balance Decimal(18, 4),  -- 18 digits total, 4 after decimal
    interest_rate Decimal(5, 4) -- 5 digits total, 4 after decimal
) ENGINE = MergeTree()
ORDER BY account_id;
```

### String and Text Types

```sql
-- String types
CREATE TABLE logs (
    timestamp DateTime,
    level Enum('DEBUG' = 1, 'INFO' = 2, 'WARN' = 3, 'ERROR' = 4),
    message String,
    source LowCardinality(String),  -- Optimized for low-cardinality strings
    tags Array(String)
) ENGINE = MergeTree()
ORDER BY (timestamp, level);

-- Fixed-length strings
CREATE TABLE codes (
    id UInt32,
    country_code FixedString(2),  -- Always 2 characters
    postal_code FixedString(10)   -- Always 10 characters
) ENGINE = MergeTree()
ORDER BY id;
```

### Date and Time Types

```sql
-- Date and time types
CREATE TABLE events (
    id UInt32,
    event_date Date,
    event_time DateTime,
    created_at DateTime64(3),  -- With millisecond precision
    duration UInt32
) ENGINE = MergeTree()
ORDER BY (event_date, event_time);

-- Time zone handling
CREATE TABLE global_events (
    id UInt32,
    timestamp DateTime('UTC'),
    local_time DateTime,
    timezone String
) ENGINE = MergeTree()
ORDER BY timestamp;
```

### Complex Data Types

```sql
-- Arrays and nested structures
CREATE TABLE products (
    product_id UInt32,
    name String,
    categories Array(String),
    attributes Map(String, String),
    variants Nested(
        variant_id UInt32,
        price Float64,
        stock UInt32
    )
) ENGINE = MergeTree()
ORDER BY product_id;

-- Tuples for structured data
CREATE TABLE coordinates (
    id UInt32,
    location Tuple(Float64, Float64),  -- (latitude, longitude)
    metadata Tuple(String, UInt32)     -- (description, accuracy)
) ENGINE = MergeTree()
ORDER BY id;
```

## Schema Design Principles

### Primary Key and Sorting Key

The ORDER BY clause defines both the primary key and sorting order:

```sql
-- Good: Optimized for time-range queries
CREATE TABLE user_activity (
    user_id UInt32,
    timestamp DateTime,
    activity_type String,
    metadata String
) ENGINE = MergeTree()
ORDER BY (user_id, timestamp);

-- Better: Include query predicates in sorting key
CREATE TABLE user_activity_optimized (
    user_id UInt32,
    timestamp DateTime,
    activity_type LowCardinality(String),
    metadata String
) ENGINE = MergeTree()
ORDER BY (user_id, timestamp, activity_type);
```

### Partitioning Strategy

```sql
-- Monthly partitioning for time-series data
CREATE TABLE logs_partitioned (
    timestamp DateTime,
    level String,
    message String,
    source String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, level);

-- Custom partitioning for categorical data
CREATE TABLE sales_partitioned (
    date Date,
    region LowCardinality(String),
    product_id UInt32,
    quantity UInt32,
    revenue Float64
) ENGINE = MergeTree()
PARTITION BY (toYear(date), region)
ORDER BY (date, product_id);
```

### Index Optimization

```sql
-- Granular indexes for fast queries
CREATE TABLE events_indexed (
    timestamp DateTime,
    user_id UInt32,
    event_type LowCardinality(String),
    properties String
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id)
SETTINGS index_granularity = 8192;  -- Smaller granules = faster queries

-- Skipping indexes for selective queries
CREATE TABLE large_table (
    id UInt32,
    category LowCardinality(String),
    data String
) ENGINE = MergeTree()
ORDER BY id
SETTINGS
    index_granularity = 8192,
    merge_max_block_size = 8192;
```

## Materialized Views

### Basic Materialized Views

```sql
-- Create a summary table
CREATE MATERIALIZED VIEW daily_user_stats
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, user_id)
AS SELECT
    toDate(timestamp) as date,
    user_id,
    count() as events_count,
    sum(value) as total_value
FROM events
GROUP BY date, user_id;

-- Query the materialized view
SELECT user_id, events_count, total_value
FROM daily_user_stats
WHERE date >= '2024-01-01'
ORDER BY total_value DESC
LIMIT 10;
```

### Advanced Materialized Views

```sql
-- Complex aggregations
CREATE MATERIALIZED VIEW user_session_summary
ENGINE = AggregatingMergeTree()
ORDER BY (user_id, session_date)
AS SELECT
    user_id,
    toDate(min(timestamp)) as session_date,
    count() as total_events,
    sum(value) as total_value,
    avg(value) as avg_value,
    min(timestamp) as first_event,
    max(timestamp) as last_event
FROM user_events
GROUP BY user_id, toDate(timestamp);

-- Real-time aggregations
CREATE MATERIALIZED VIEW realtime_metrics
ENGINE = AggregatingMergeTree()
ORDER BY (minute, metric_name)
AS SELECT
    toStartOfMinute(timestamp) as minute,
    metric_name,
    count() as count,
    avg(value) as avg_value,
    max(value) as max_value
FROM metrics
GROUP BY minute, metric_name;
```

## Schema Evolution

### Adding Columns

```sql
-- Add new columns
ALTER TABLE users ADD COLUMN email String AFTER name;
ALTER TABLE users ADD COLUMN preferences Map(String, String);

-- Add columns with defaults
ALTER TABLE products ADD COLUMN discontinued UInt8 DEFAULT 0;
ALTER TABLE products ADD COLUMN discontinued_date Nullable(Date);
```

### Modifying Columns

```sql
-- Change column types (careful with data loss)
ALTER TABLE users MODIFY COLUMN age UInt8;  -- Downcast Int32 to UInt8

-- Change column order
ALTER TABLE users MODIFY COLUMN email String AFTER phone;

-- Add constraints
ALTER TABLE users ADD CONSTRAINT check_age CHECK age >= 0 AND age <= 150;
```

### Data Migration

```sql
-- Migrate data with transformation
CREATE TABLE users_new (
    id UInt32,
    name String,
    email String,
    age UInt8,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY id;

-- Insert transformed data
INSERT INTO users_new
SELECT
    id,
    name,
    email,
    if(age < 0, 0, if(age > 150, 150, age)) as age,
    now() as created_at
FROM users_old;

-- Atomic swap
RENAME TABLE users TO users_old, users_new TO users;
```

## Best Practices for Schema Design

### Data Distribution

```sql
-- Ensure even data distribution
CREATE TABLE distributed_events (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    data String
) ENGINE = MergeTree()
ORDER BY (timestamp, cityHash64(user_id))  -- Hash-based distribution
PARTITION BY toYYYYMM(timestamp);

-- Avoid hotspots
CREATE TABLE balanced_table (
    id UInt64,
    category String,
    data String
) ENGINE = MergeTree()
ORDER BY (category, cityHash64(id))  -- Distribute by hash
PARTITION BY category;
```

### Compression Optimization

```sql
-- Choose appropriate compression
CREATE TABLE compressed_logs (
    timestamp DateTime CODEC(Delta, ZSTD),
    level LowCardinality(String),
    message String CODEC(ZSTD(3)),  -- Lower compression for text
    metadata String CODEC(LZ4)      -- Faster compression for metadata
) ENGINE = MergeTree()
ORDER BY (timestamp, level)
SETTINGS
    min_rows_for_wide_part = 0,     -- Force wide parts for better compression
    min_bytes_for_wide_part = 0;
```

### Memory Optimization

```sql
-- Optimize for memory usage
CREATE TABLE memory_efficient (
    id UInt32,
    small_field UInt8,
    medium_field UInt16,
    large_field String
) ENGINE = MergeTree()
ORDER BY id
SETTINGS
    max_parts_in_total = 10000,      -- Limit total parts
    max_memory_usage = 10000000000, -- 10GB memory limit
    merge_max_block_size = 8192;     -- Smaller merge blocks
```

## Performance Monitoring

### Query Analysis

```sql
-- Monitor query performance
SELECT
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    result_rows,
    result_bytes
FROM system.query_log
WHERE type = 'QueryFinish'
    AND query_duration_ms > 1000  -- Queries taking > 1 second
ORDER BY query_duration_ms DESC
LIMIT 10;
```

### Table Statistics

```sql
-- Monitor table performance
SELECT
    database,
    table,
    total_rows,
    total_bytes,
    total_bytes / total_rows as avg_row_size,
    parts_count,
    uncompressed_bytes,
    compressed_bytes
FROM system.tables
WHERE database = 'your_database'
ORDER BY total_bytes DESC;
```

## What We've Accomplished

Congratulations! 🎉 You've learned:

1. **ClickHouse Storage Engines** - Understanding MergeTree and its variants
2. **Data Type Selection** - Choosing the right types for your data
3. **Schema Design** - Creating efficient table structures
4. **Partitioning Strategies** - Optimizing data distribution
5. **Materialized Views** - Pre-computing aggregations
6. **Schema Evolution** - Safely modifying table structures
7. **Performance Optimization** - Tuning for your specific workload

## Next Steps

Now that you understand ClickHouse's data modeling capabilities, let's explore how to efficiently load data from various sources. In [Chapter 3: Data Ingestion & ETL](03-data-ingestion.md), we'll cover bulk loading, streaming ingestion, and ETL pipelines.

---

**Practice what you've learned:**
1. Design a schema for a real-world analytics use case
2. Create materialized views for common query patterns
3. Optimize an existing table structure for better performance
4. Set up partitioning for a large dataset

*What kind of data are you planning to store in ClickHouse?* 📊

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `TABLE`, `ORDER`, `timestamp` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Data Modeling & Schemas` as an operating subsystem inside **ClickHouse Tutorial: High-Performance Analytical Database**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `CREATE`, `ENGINE`, `UInt32` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Data Modeling & Schemas` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `TABLE`.
2. **Input normalization**: shape incoming data so `ORDER` receives stable contracts.
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
- search upstream code for `TABLE` and `ORDER` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with ClickHouse](01-getting-started.md)
- [Next Chapter: Chapter 3: Data Ingestion & ETL](03-data-ingestion.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
