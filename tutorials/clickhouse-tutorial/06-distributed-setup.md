---
layout: default
title: "Chapter 6: Distributed ClickHouse"
parent: "ClickHouse Tutorial"
nav_order: 6
---

# Chapter 6: Distributed ClickHouse

Welcome to **Chapter 6: Distributed ClickHouse**. In this part of **ClickHouse Tutorial: High-Performance Analytical Database**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


ClickHouse's true power emerges in distributed deployments. This chapter covers clustering, sharding, replication, and scaling strategies for enterprise-grade analytical workloads.

## Distributed Architecture Overview

### Cluster Components

```xml
<!-- ClickHouse cluster configuration -->
<clickhouse>
    <remote_servers>
        <analytics_cluster>
            <shard>
                <replica>
                    <host>ch-node-1</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>ch-node-2</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <replica>
                    <host>ch-node-3</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>ch-node-4</host>
                    <port>9000</port>
                </replica>
            </shard>
        </analytics_cluster>
    </remote_servers>
</clickhouse>
```

### Distributed Table Engine

```sql
-- Create distributed table
CREATE TABLE events_distributed (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = Distributed(
    'analytics_cluster',  -- Cluster name
    'events_local',       -- Local table name
    cityHash64(user_id)   -- Sharding key
);

-- Local table on each shard
CREATE TABLE events_local (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id);
```

## Sharding Strategies

### Hash-Based Sharding

```sql
-- User-based sharding (good for user analytics)
CREATE TABLE user_events_distributed (
    user_id UInt32,
    timestamp DateTime,
    event_type String,
    data String
) ENGINE = Distributed(
    'analytics_cluster',
    'user_events_local',
    cityHash64(user_id)  -- Shard by user_id hash
);

-- Time-based sharding with hash
CREATE TABLE time_events_distributed (
    timestamp DateTime,
    event_type String,
    data String
) ENGINE = Distributed(
    'analytics_cluster',
    'time_events_local',
    cityHash64(toYYYYMM(timestamp))  -- Shard by month hash
);
```

### Custom Sharding Functions

```sql
-- Geographic sharding
CREATE TABLE geo_events (
    country String,
    city String,
    timestamp DateTime,
    data String
) ENGINE = Distributed(
    'analytics_cluster',
    'geo_events_local',
    cityHash64(country)  -- Shard by country
);

-- Category-based sharding
CREATE TABLE category_events (
    category String,
    subcategory String,
    timestamp DateTime,
    data String
) ENGINE = Distributed(
    'analytics_cluster',
    'category_events_local',
    cityHash64(category)  -- Shard by category
);
```

## Replication and High Availability

### ReplicatedMergeTree Engine

```sql
-- Create replicated table
CREATE TABLE events_replicated (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{cluster}/events',  -- ZooKeeper path
    '{replica}'                             -- Replica name
)
ORDER BY (timestamp, user_id)
SETTINGS
    index_granularity = 8192,
    merge_max_block_size = 8192;

-- With replication settings
CREATE TABLE events_replicated_advanced (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{cluster}/events_advanced',
    '{replica}'
)
ORDER BY (timestamp, user_id)
TTL timestamp + INTERVAL 90 DAY
SETTINGS
    index_granularity = 8192,
    merge_max_block_size = 8192,
    replication_alter_partitions_sync = 1;  -- Sync DDL operations
```

### Replication Monitoring

```sql
-- Monitor replication status
SELECT
    database,
    table,
    is_readonly,
    absolute_delay,
    queue_size,
    inserts_in_queue,
    merges_in_queue
FROM system.replicas
WHERE database = 'your_database';

-- Replication queue details
SELECT
    database,
    table,
    create_time,
    last_attempt_time,
    last_exception,
    num_tries
FROM system.replication_queue
ORDER BY create_time DESC;

-- Check replica synchronization
SELECT
    database,
    table,
    total_replicas,
    active_replicas,
    lost_partitions
FROM system.replicas
WHERE lost_partitions > 0;
```

## Distributed Query Execution

### Global Query Distribution

```sql
-- Query distributed table (automatic distribution)
SELECT
    toDate(timestamp) as date,
    count() as events,
    uniq(user_id) as unique_users,
    sum(value) as total_value
FROM events_distributed
WHERE timestamp >= '2024-01-01'
GROUP BY date
ORDER BY date DESC;

-- Force global distribution
SELECT
    shardNum() as shard_id,
    count() as local_count
FROM events_distributed
GROUP BY shardNum();

-- Distributed subqueries
SELECT user_id, count()
FROM events_distributed
WHERE user_id IN (
    SELECT user_id
    FROM user_attributes_distributed
    WHERE status = 'active'
)
GROUP BY user_id;
```

### Query Optimization for Distributed

```sql
-- Optimize distributed queries
SELECT
    toDate(timestamp) as date,
    count() as events,
    sum(value) as total_value
FROM events_distributed
WHERE timestamp >= '2024-01-01'
    AND user_id % 100 = 0  -- Selective filter
GROUP BY date
ORDER BY date DESC
SETTINGS
    max_distributed_connections = 8,
    distributed_group_by_no_merge = 0,
    optimize_distributed_group_by_sharding_key = 1;
```

## Load Balancing and Failover

### Connection Pooling

```xml
<!-- ClickHouse connection configuration -->
<clickhouse>
    <distributed_ddl>
        <pool_size>4</pool_size>
        <max_connections>100</max_connections>
    </distributed_ddl>
</clickhouse>
```

### Failover Configuration

```sql
-- Create table with failover settings
CREATE TABLE events_failover (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = Distributed(
    'analytics_cluster',
    'events_local',
    cityHash64(user_id)
)
SETTINGS
    max_replicas_to_choose = 3,      -- Use up to 3 replicas
    load_balancing = 'random',       -- Load balancing strategy
    connections_with_failover = 1;   -- Enable failover
```

## Cluster Management

### Adding New Shards

```sql
-- Add new shard configuration
ALTER TABLE events_distributed
ADD SHARD 'ch-node-5:9000', 'ch-node-6:9000';

-- Rebalance data across shards
OPTIMIZE TABLE events_distributed
ON CLUSTER analytics_cluster
FINAL;
```

### Replica Management

```sql
-- Check replica health
SELECT
    database,
    table,
    replica_name,
    is_readonly,
    is_session_expired,
    future_parts,
    parts_to_check
FROM system.replicas;

-- Force replica synchronization
SYSTEM SYNC REPLICA events_replicated;

-- Detach unhealthy replica
ALTER TABLE events_replicated
DETACH PARTITION 202401
ON CLUSTER analytics_cluster;
```

## Performance Optimization

### Distributed Query Settings

```sql
-- Optimize distributed performance
SET max_distributed_connections = 8;
SET distributed_group_by_no_merge = 0;
SET optimize_distributed_group_by_sharding_key = 1;
SET distributed_push_down_limit = 1;

-- Query with optimized settings
SELECT
    toDate(timestamp) as date,
    count() as events,
    uniq(user_id) as unique_users
FROM events_distributed
WHERE timestamp >= '2024-01-01'
GROUP BY date
ORDER BY date DESC
SETTINGS
    max_threads = 16,
    max_memory_usage = 10000000000,
    distributed_aggregation_memory_efficient = 1;
```

### Sharding Optimization

```sql
-- Analyze sharding distribution
SELECT
    shardNum() as shard,
    count() as rows_in_shard,
    uniq(user_id) as unique_users_in_shard
FROM events_distributed
GROUP BY shardNum()
ORDER BY shard;

-- Rebalance if needed
OPTIMIZE TABLE events_distributed
ON CLUSTER analytics_cluster
FINAL SETTINGS
    cleanup_delay_period = 0,
    cleanup_delay_period_random_add = 0;
```

## Monitoring and Troubleshooting

### Cluster Health Monitoring

```sql
-- Monitor cluster status
SELECT
    host,
    port,
    status,
    error,
    num_queries,
    uptime
FROM system.clusters
WHERE cluster = 'analytics_cluster';

-- Check distributed DDL queue
SELECT
    entry,
    host,
    port,
    status,
    query,
    exception
FROM system.distributed_ddl_queue
ORDER BY entry DESC;

-- Monitor replication lag
SELECT
    database,
    table,
    replica_name,
    absolute_delay,
    total_replicas,
    active_replicas
FROM system.replicas
WHERE absolute_delay > 60;  -- > 1 minute lag
```

### Performance Diagnostics

```sql
-- Analyze distributed query performance
SELECT
    query_id,
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage,
    ProfileEvents['DistributedConnectionsUsed'] as distributed_connections,
    ProfileEvents['DistributedConnectionsTotal'] as total_connections
FROM system.query_log
WHERE query LIKE '%events_distributed%'
    AND type = 'QueryFinish'
ORDER BY query_duration_ms DESC;

-- Check network traffic
SELECT
    ProfileEvents['NetworkSendBytes'] as sent_bytes,
    ProfileEvents['NetworkReceiveBytes'] as received_bytes,
    ProfileEvents['DistributedConnectionsUsed'] as connections_used
FROM system.query_log
WHERE query_id = 'your_query_id';
```

## Backup and Recovery

### Distributed Backup

```bash
# Backup distributed tables
clickhouse-backup create \
    --config /etc/clickhouse-server/config.xml \
    --table events_distributed \
    backup_2024_01_15

# Restore distributed tables
clickhouse-backup restore \
    --config /etc/clickhouse-server/config.xml \
    backup_2024_01_15
```

### Point-in-Time Recovery

```sql
-- Create snapshot for recovery
CREATE SNAPSHOT events_snapshot
FOR TABLE events_distributed
ON CLUSTER analytics_cluster;

-- Restore from snapshot
RESTORE SNAPSHOT events_snapshot
FOR TABLE events_distributed
ON CLUSTER analytics_cluster;
```

## Scaling Strategies

### Horizontal Scaling

```sql
-- Add new shard to cluster
ALTER TABLE events_distributed
ADD SHARD 'ch-node-7:9000', 'ch-node-8:9000'
ON CLUSTER analytics_cluster;

-- Redistribute data
SYSTEM RELOAD CONFIG;
OPTIMIZE TABLE events_distributed
ON CLUSTER analytics_cluster FINAL;
```

### Vertical Scaling

```sql
-- Increase resources per node
-- Update server configuration
sudo systemctl stop clickhouse-server

# Edit config.xml
# Increase max_memory_usage, max_threads, etc.

sudo systemctl start clickhouse-server
```

## Cloud Deployment

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: clickhouse-cluster
spec:
  serviceName: clickhouse
  replicas: 4
  selector:
    matchLabels:
      app: clickhouse
  template:
    metadata:
      labels:
        app: clickhouse
    spec:
      containers:
      - name: clickhouse
        image: clickhouse/clickhouse-server:latest
        ports:
        - containerPort: 9000
        - containerPort: 8123
        volumeMounts:
        - name: clickhouse-data
          mountPath: /var/lib/clickhouse
        env:
        - name: CLICKHOUSE_CLUSTER
          value: "analytics_cluster"
  volumeClaimTemplates:
  - metadata:
    name: clickhouse-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### Cloud-Native Features

```sql
-- Cloud storage integration
CREATE TABLE events_cloud (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id)
SETTINGS
    storage_policy = 's3_cold',  -- Use S3 for cold data
    min_bytes_for_wide_part = 0;

-- Multi-cloud deployment
CREATE TABLE events_multi_cloud (
    timestamp DateTime,
    user_id UInt32,
    event_type String,
    value Float64
) ENGINE = Distributed(
    'multi_cloud_cluster',
    'events_local',
    cityHash64(user_id)
);
```

## What We've Accomplished

Excellent! 🌐 You've mastered distributed ClickHouse:

1. **Distributed Architecture** - Cluster setup and configuration
2. **Sharding Strategies** - Hash-based and custom sharding
3. **Replication** - High availability with ReplicatedMergeTree
4. **Distributed Queries** - Global query execution and optimization
5. **Load Balancing** - Connection pooling and failover
6. **Cluster Management** - Adding shards and managing replicas
7. **Performance Optimization** - Distributed query tuning
8. **Monitoring** - Health checks and performance diagnostics
9. **Backup & Recovery** - Distributed backup strategies
10. **Scaling** - Horizontal and vertical scaling approaches

## Next Steps

With your distributed ClickHouse cluster running smoothly, let's focus on performance tuning and optimization. In [Chapter 7: Performance Tuning](07-performance-tuning.md), we'll dive into advanced optimization techniques, memory management, and query performance improvements.

---

**Practice what you've learned:**
1. Set up a 3-node ClickHouse cluster with replication
2. Implement proper sharding for a large dataset
3. Configure monitoring and alerting for cluster health
4. Optimize a distributed query for better performance

*How many nodes are you planning for your ClickHouse cluster?* ⚡

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `user_id`, `timestamp`, `clickhouse` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Distributed ClickHouse` as an operating subsystem inside **ClickHouse Tutorial: High-Performance Analytical Database**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `TABLE`, `analytics_cluster`, `events_distributed` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Distributed ClickHouse` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `user_id`.
2. **Input normalization**: shape incoming data so `timestamp` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `clickhouse`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ClickHouse/ClickHouse)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `user_id` and `timestamp` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Aggregation & Analytics](05-aggregation-analytics.md)
- [Next Chapter: Chapter 7: Performance Tuning](07-performance-tuning.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
