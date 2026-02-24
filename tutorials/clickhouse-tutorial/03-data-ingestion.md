---
layout: default
title: "Chapter 3: Data Ingestion & ETL"
parent: "ClickHouse Tutorial"
nav_order: 3
---

# Chapter 3: Data Ingestion & ETL

Welcome to **Chapter 3: Data Ingestion & ETL**. In this part of **ClickHouse Tutorial: High-Performance Analytical Database**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Now that you have well-designed schemas, let's explore how to efficiently load data into ClickHouse. Data ingestion is where ClickHouse truly shines, offering multiple methods for getting data into your analytical database quickly and reliably.

## Bulk Data Loading

### INSERT Statements

```sql
-- Single row insert
INSERT INTO events VALUES (1, '2024-01-01 10:00:00', 'user_login', 123);

-- Multiple rows
INSERT INTO events VALUES
(1, '2024-01-01 10:00:00', 'user_login', 123),
(2, '2024-01-01 10:01:00', 'page_view', 456),
(3, '2024-01-01 10:02:00', 'purchase', 789);

-- Insert with column names
INSERT INTO events (id, timestamp, event_type, user_id)
VALUES (4, now(), 'signup', 101);
```

### Bulk INSERT from Files

```bash
# Load data from CSV file
clickhouse-client --query="
    INSERT INTO events
    FORMAT CSV
" < events.csv

# Load from TSV with headers
clickhouse-client --query="
    INSERT INTO events
    FORMAT TSVWithNames
" < events_with_headers.tsv
```

### Using clickhouse-client

```bash
# Connect to ClickHouse
clickhouse-client --host localhost --port 9000 --user default

# Load data with progress
cat large_dataset.csv | clickhouse-client --query="
    INSERT INTO table_name FORMAT CSV
" --progress

# Load compressed data
zcat data.csv.gz | clickhouse-client --query="
    INSERT INTO table_name FORMAT CSV
"
```

## ETL with External Tables

### File-based ETL

```sql
-- Create external table for CSV processing
CREATE TABLE events_raw (
    timestamp String,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = File(CSV, '/data/events.csv');

-- Process and insert into final table
INSERT INTO events
SELECT
    parseDateTimeBestEffort(timestamp) as timestamp,
    user_id,
    event_type,
    value
FROM events_raw
WHERE user_id IS NOT NULL;
```

### URL-based Ingestion

```sql
-- Load data directly from URL
INSERT INTO events
SELECT *
FROM url('https://example.com/data.csv', CSV, '
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
');
```

## Streaming Data Ingestion

### Kafka Integration

```sql
-- Create Kafka engine table
CREATE TABLE events_kafka (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'user_events',
    kafka_group_name = 'clickhouse_consumer',
    kafka_format = 'JSONEachRow';

-- Create materialized view for processing
CREATE MATERIALIZED VIEW events_processed
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id)
AS SELECT
    timestamp,
    user_id,
    event_type,
    value,
    now() as processed_at
FROM events_kafka;
```

### RabbitMQ Integration

```sql
-- RabbitMQ engine table
CREATE TABLE events_rabbitmq (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = RabbitMQ()
SETTINGS
    rabbitmq_host_port = 'localhost:5672',
    rabbitmq_exchange_name = 'events_exchange',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_routing_key_list = 'user.*';
```

## Data Transformation Pipelines

### Basic Transformations

```sql
-- Transform data during ingestion
INSERT INTO user_activity_clean
SELECT
    user_id,
    timestamp,
    event_type,
    CASE
        WHEN event_type = 'login' THEN 1
        WHEN event_type = 'logout' THEN 2
        ELSE 0
    END as event_code,
    JSONExtractString(properties, 'page') as page,
    JSONExtractFloat(properties, 'duration') as duration
FROM user_activity_raw
WHERE timestamp >= '2024-01-01 00:00:00';
```

### Advanced ETL with Dictionaries

```sql
-- Create external dictionary for lookups
CREATE DICTIONARY user_attributes (
    user_id UInt32,
    country LowCardinality(String),
    age_group LowCardinality(String),
    subscription_type LowCardinality(String)
)
PRIMARY KEY user_id
SOURCE(HTTP(URL 'http://api.example.com/users' FORMAT 'JSON'))
LIFETIME(MIN 300 MAX 3600)
LAYOUT(HASHED());

-- Use dictionary in transformations
INSERT INTO enriched_events
SELECT
    e.timestamp,
    e.user_id,
    e.event_type,
    e.value,
    dictGet('user_attributes', 'country', e.user_id) as country,
    dictGet('user_attributes', 'subscription_type', e.user_id) as subscription_type
FROM events e;
```

## Incremental Loading

### Change Data Capture

```sql
-- Track last processed timestamp
CREATE TABLE ingestion_state (
    table_name String,
    last_timestamp DateTime,
    last_id UInt64
) ENGINE = MergeTree()
ORDER BY table_name;

-- Incremental load with state tracking
INSERT INTO events
SELECT
    timestamp,
    user_id,
    event_type,
    value
FROM events_source
WHERE timestamp > (
    SELECT last_timestamp
    FROM ingestion_state
    WHERE table_name = 'events'
);

-- Update state
INSERT INTO ingestion_state
SELECT
    'events' as table_name,
    max(timestamp) as last_timestamp,
    max(id) as last_id
FROM events_source;
```

### Watermark-based Loading

```sql
-- Use watermarks for incremental processing
CREATE TABLE events_watermark (
    watermark DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY watermark;

-- Incremental load
INSERT INTO events
SELECT *
FROM events_source
WHERE timestamp > (SELECT max(watermark) FROM events_watermark);

-- Update watermark
INSERT INTO events_watermark SELECT now();
```

## Data Quality and Validation

### Pre-ingestion Validation

```sql
-- Validate data before insertion
CREATE TABLE events_staging (
    timestamp String,
    user_id String,
    event_type String,
    value String
) ENGINE = MergeTree()
ORDER BY tuple();

-- Validation query
SELECT
    count() as total_rows,
    countIf(length(timestamp) > 0) as valid_timestamps,
    countIf(user_id != '') as valid_user_ids,
    countIf(event_type IN ('login', 'logout', 'purchase')) as valid_event_types
FROM events_staging;

-- Insert only valid data
INSERT INTO events
SELECT
    parseDateTimeBestEffort(timestamp),
    toUInt32OrNull(user_id),
    event_type,
    toFloat64OrNull(value)
FROM events_staging
WHERE
    length(timestamp) > 0
    AND user_id != ''
    AND event_type IN ('login', 'logout', 'purchase');
```

### Post-ingestion Validation

```sql
-- Data quality checks
SELECT
    'Duplicate events' as check_name,
    count() as count
FROM (
    SELECT user_id, timestamp, event_type, count() as cnt
    FROM events
    GROUP BY user_id, timestamp, event_type
    HAVING cnt > 1
);

-- Missing data validation
SELECT
    'Missing timestamps' as check_name,
    countIf(timestamp IS NULL) as count
FROM events;

-- Outlier detection
SELECT
    'Value outliers' as check_name,
    countIf(value < 0 OR value > 1000000) as count
FROM events;
```

## Performance Optimization

### Parallel Loading

```bash
# Parallel loading with multiple clients
for i in {1..4}; do
    clickhouse-client --query="
        INSERT INTO events
        SELECT * FROM events_source
        WHERE cityHash64(id) % 4 = $i
    " &
done
wait
```

### Batch Optimization

```sql
-- Optimize batch sizes
INSERT INTO events
SELECT *
FROM events_source
SETTINGS
    max_insert_threads = 8,
    max_insert_block_size = 1000000,
    min_insert_block_size_rows = 100000;
```

### Memory Management

```sql
-- Control memory usage during ingestion
INSERT INTO large_table
SELECT *
FROM source_table
SETTINGS
    max_memory_usage = 10000000000,  -- 10GB
    max_threads = 4,
    max_insert_threads = 4;
```

## Monitoring Ingestion

### Ingestion Metrics

```sql
-- Monitor ingestion performance
SELECT
    database,
    table,
    metric,
    value
FROM system.metrics
WHERE metric LIKE '%insert%'
    OR metric LIKE '%merge%';

-- Query ingestion statistics
SELECT
    query_id,
    query,
    read_rows,
    written_rows,
    memory_usage,
    query_duration_ms
FROM system.query_log
WHERE query LIKE '%INSERT%'
    AND type = 'QueryFinish'
ORDER BY query_duration_ms DESC
LIMIT 10;
```

### Performance Troubleshooting

```sql
-- Identify slow insertions
SELECT
    query,
    query_duration_ms,
    read_bytes,
    written_bytes,
    memory_usage
FROM system.query_log
WHERE query LIKE '%INSERT%'
    AND query_duration_ms > 5000  -- > 5 seconds
ORDER BY query_duration_ms DESC;

-- Monitor merge performance
SELECT
    database,
    table,
    elapsed,
    progress,
    num_parts,
    result_part_name
FROM system.merges
WHERE is_mutation = 0
ORDER BY elapsed DESC;
```

## Real-world ETL Patterns

### Data Warehouse Loading

```sql
-- Fact table loading
INSERT INTO fact_sales
SELECT
    s.sale_id,
    d.date_key,
    p.product_key,
    c.customer_key,
    s.quantity,
    s.unit_price,
    s.total_amount,
    s.discount_amount
FROM staging_sales s
JOIN dim_date d ON s.sale_date = d.full_date
JOIN dim_product p ON s.product_id = p.product_id
JOIN dim_customer c ON s.customer_id = c.customer_id;

-- Dimension updates
INSERT INTO dim_customer
SELECT
    customer_id,
    customer_name,
    email,
    phone,
    address,
    now() as updated_at
FROM staging_customers
WHERE customer_id NOT IN (SELECT customer_id FROM dim_customer);
```

### Log Processing Pipeline

```sql
-- Parse and enrich log data
INSERT INTO processed_logs
SELECT
    timestamp,
    parseDateTimeBestEffort(timestamp_str) as parsed_timestamp,
    level,
    message,
    JSONExtractString(metadata, 'user_id') as user_id,
    JSONExtractString(metadata, 'session_id') as session_id,
    arrayMap(x -> JSONExtractString(x, 'tag'), JSONExtractArrayRaw(metadata, 'tags')) as tags,
    cityHash64(concat(user_id, session_id)) as session_hash
FROM raw_logs
WHERE length(timestamp_str) > 0
    AND level IN ('INFO', 'WARN', 'ERROR');
```

## What We've Accomplished

Excellent! 🎉 You've mastered ClickHouse data ingestion:

1. **Bulk Loading** - Efficiently loading large datasets
2. **Streaming Ingestion** - Real-time data from Kafka/RabbitMQ
3. **ETL Pipelines** - Data transformation and enrichment
4. **Incremental Loading** - Change data capture and watermarks
5. **Data Quality** - Validation and error handling
6. **Performance Optimization** - Parallel loading and memory management
7. **Monitoring** - Tracking ingestion performance and troubleshooting

## Next Steps

With data flowing into ClickHouse efficiently, let's focus on writing high-performance analytical queries. In [Chapter 4: Query Optimization](04-query-optimization.md), we'll explore ClickHouse's query engine and optimization techniques.

---

**Practice what you've learned:**
1. Set up a Kafka consumer for real-time data ingestion
2. Create an ETL pipeline with data validation
3. Implement incremental loading for a large dataset
4. Monitor and optimize the performance of your ingestion pipeline

*What type of data source are you planning to ingest into ClickHouse?* 📥

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `timestamp`, `user_id` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Data Ingestion & ETL` as an operating subsystem inside **ClickHouse Tutorial: High-Performance Analytical Database**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `INSERT`, `INTO`, `events` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Data Ingestion & ETL` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `timestamp` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `user_id`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ClickHouse/ClickHouse)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `SELECT` and `timestamp` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Data Modeling & Schemas](02-data-modeling.md)
- [Next Chapter: Chapter 4: Query Optimization](04-query-optimization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
