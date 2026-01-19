---
layout: default
title: "Chapter 7: Performance Tuning"
parent: "PostgreSQL Query Planner"
nav_order: 7
---

# Chapter 7: Performance Tuning

> Configuration parameters, memory settings, and systematic approaches to query optimization.

## Overview

Query performance depends on both the planner's decisions and PostgreSQL's configuration. This chapter covers essential parameters, memory tuning, and systematic optimization approaches.

## Memory Configuration

### Shared Buffers

```sql
-- Shared memory for caching data pages
-- Recommended: 25% of system RAM (up to ~8GB)

SHOW shared_buffers;

-- Set in postgresql.conf
-- shared_buffers = '4GB'

-- Monitor buffer usage
SELECT
    c.relname,
    pg_size_pretty(count(*) * 8192) as buffered,
    round(100.0 * count(*) / (
        SELECT setting::integer FROM pg_settings WHERE name = 'shared_buffers'
    ), 2) as buffer_percent
FROM pg_class c
JOIN pg_buffercache b ON b.relfilenode = c.relfilenode
GROUP BY c.relname
ORDER BY count(*) DESC
LIMIT 10;
```

### Work Mem

```sql
-- Memory for sorting and hashing PER OPERATION
-- Each query can use multiple work_mem allocations

SHOW work_mem;  -- Default: 4MB

-- Increase for complex queries
SET work_mem = '256MB';

-- Signs you need more work_mem:
-- 1. "Sort Method: external merge" in EXPLAIN
-- 2. "Batches: N" > 1 in Hash operations

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders ORDER BY total DESC;
-- Sort Method: external merge  Disk: 12345kB  <- needs more work_mem
-- Sort Method: quicksort  Memory: 1234kB     <- fits in memory

-- Calculate work_mem needs
-- Estimate: expected_rows * row_width / 1024 (KB)
```

### Maintenance Work Mem

```sql
-- Memory for maintenance operations
-- Used by: VACUUM, CREATE INDEX, ALTER TABLE ADD FOREIGN KEY

SHOW maintenance_work_mem;  -- Default: 64MB

-- Increase for faster maintenance (up to 1-2GB)
SET maintenance_work_mem = '1GB';

-- Then run maintenance
CREATE INDEX CONCURRENTLY idx_large_table_col ON large_table(column);
```

### Effective Cache Size

```sql
-- Planner's estimate of OS disk cache
-- Affects cost estimates for index scans

SHOW effective_cache_size;

-- Set to ~75% of total system RAM
-- effective_cache_size = '12GB'

-- Higher value makes index scans more attractive
-- (assumes more data will be cached)
```

## Planner Configuration

### Cost Parameters

```sql
-- Tune for your storage
-- SSD storage
SET random_page_cost = 1.1;  -- Default 4.0, lower for SSD
SET seq_page_cost = 1.0;

-- Networked/cloud storage
SET random_page_cost = 2.0;  -- Might be faster than local HDD

-- Check current settings
SELECT name, setting, unit, short_desc
FROM pg_settings
WHERE name LIKE '%cost%';
```

### Parallelism Settings

```sql
-- Maximum parallel workers globally
SHOW max_parallel_workers;  -- Default: 8

-- Maximum per gather operation
SHOW max_parallel_workers_per_gather;  -- Default: 2

-- Minimum table size for parallel scan
SHOW min_parallel_table_scan_size;  -- Default: 8MB

-- Cost thresholds
SHOW parallel_setup_cost;  -- Default: 1000
SHOW parallel_tuple_cost;  -- Default: 0.1

-- For analytical workloads, increase parallelism
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
SELECT pg_reload_conf();
```

### Join Settings

```sql
-- Control join planning complexity
SHOW join_collapse_limit;     -- Default: 8
SHOW from_collapse_limit;     -- Default: 8
SHOW geqo_threshold;          -- Default: 12 (genetic query optimizer kicks in)

-- For complex queries with many tables
-- Lower limits = faster planning, potentially worse plans
SET join_collapse_limit = 1;  -- Force written join order

-- Higher limits = slower planning, better plans
SET join_collapse_limit = 12;
```

## Analyzing Slow Queries

### pg_stat_statements

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slowest queries
SELECT
    round(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    round(mean_exec_time::numeric, 2) as mean_ms,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) as percent,
    substring(query, 1, 100) as query_preview
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Find queries with high I/O
SELECT
    query,
    calls,
    shared_blks_read,
    shared_blks_hit,
    round(100.0 * shared_blks_hit / nullif(shared_blks_read + shared_blks_hit, 0), 2) as hit_rate
FROM pg_stat_statements
WHERE calls > 100
ORDER BY shared_blks_read DESC
LIMIT 10;
```

### Auto-Explain

```sql
-- Enable auto-explain for slow queries
LOAD 'auto_explain';
SET auto_explain.log_min_duration = '100ms';
SET auto_explain.log_analyze = on;
SET auto_explain.log_buffers = on;
SET auto_explain.log_timing = on;

-- Queries over 100ms will log their execution plan
-- Check PostgreSQL log for plans
```

### Log Analysis

```sql
-- Configure query logging in postgresql.conf
-- log_min_duration_statement = '100ms'  -- Log slow queries
-- log_statement = 'all'                  -- Log all statements (verbose!)
-- log_line_prefix = '%t [%p]: '         -- Add timestamp and PID

-- Parse logs with pgBadger for analysis
-- pgbadger /var/log/postgresql/postgresql-*.log -o report.html
```

## Systematic Optimization Process

### Step 1: Identify Problem Queries

```sql
-- Check pg_stat_statements for high-impact queries
-- Sort by: total_time, calls, mean_time

-- Focus on queries that:
-- 1. Run frequently AND have moderate time
-- 2. Run occasionally BUT are very slow
-- 3. Use significant I/O (shared_blks_read)
```

### Step 2: Analyze Execution Plan

```sql
-- Get detailed execution plan
EXPLAIN (ANALYZE, BUFFERS, TIMING, VERBOSE, FORMAT TEXT)
SELECT ...your query...;

-- Look for:
-- 1. High actual time nodes
-- 2. Large row estimate mismatches (rows vs actual rows)
-- 3. Unexpected scan types (Seq Scan on large table)
-- 4. Disk spills in sorts/hashes
```

### Step 3: Check Statistics

```sql
-- Verify statistics are current
SELECT
    schemaname,
    relname,
    last_analyze,
    last_autoanalyze,
    n_live_tup
FROM pg_stat_user_tables
WHERE relname = 'your_table';

-- Update if needed
ANALYZE your_table;

-- Check column statistics
SELECT
    attname,
    n_distinct,
    most_common_vals,
    correlation
FROM pg_stats
WHERE tablename = 'your_table';
```

### Step 4: Evaluate Indexes

```sql
-- Check if appropriate indexes exist
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'your_table';

-- Check index usage
SELECT
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'your_table';

-- Consider creating new index
CREATE INDEX CONCURRENTLY idx_new ON your_table(column1, column2);
```

### Step 5: Query Rewriting

```sql
-- Simplify complex expressions
-- Before:
SELECT * FROM orders WHERE COALESCE(discount, 0) > 10;
-- After (if discount is rarely NULL):
SELECT * FROM orders WHERE discount > 10;

-- Avoid functions on indexed columns
-- Before:
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
-- After (with expression index):
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Break up OR conditions
-- Before:
SELECT * FROM orders WHERE customer_id = 1 OR customer_id = 2;
-- After (for better index use):
SELECT * FROM orders WHERE customer_id IN (1, 2);
```

## Performance Monitoring

### Key Metrics

```sql
-- Cache hit ratio (should be > 99%)
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit)  as heap_hit,
    round(100.0 * sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0), 2) as hit_ratio
FROM pg_statio_user_tables;

-- Index hit ratio
SELECT
    sum(idx_blks_read) as idx_read,
    sum(idx_blks_hit)  as idx_hit,
    round(100.0 * sum(idx_blks_hit) / nullif(sum(idx_blks_hit) + sum(idx_blks_read), 0), 2) as hit_ratio
FROM pg_statio_user_indexes;

-- Transaction rate
SELECT
    xact_commit + xact_rollback as transactions,
    xact_commit,
    xact_rollback
FROM pg_stat_database
WHERE datname = current_database();
```

### Wait Events

```sql
-- Active queries and what they're waiting on
SELECT
    pid,
    wait_event_type,
    wait_event,
    state,
    query
FROM pg_stat_activity
WHERE state = 'active';

-- Common wait events:
-- LWLock: Internal lock contention
-- Lock: Row/table lock waiting
-- IO: Disk I/O
-- Client: Waiting for client
```

### Table Bloat

```sql
-- Estimate table bloat
SELECT
    schemaname,
    relname,
    n_live_tup,
    n_dead_tup,
    round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Run vacuum if bloated
VACUUM ANALYZE your_table;

-- For severe bloat
VACUUM FULL your_table;  -- Locks table!
-- Or use pg_repack extension
```

## Configuration Recommendations

### OLTP Workload

```sql
-- Typical web application settings
-- shared_buffers = '2GB'
-- effective_cache_size = '6GB'
-- work_mem = '64MB'
-- maintenance_work_mem = '512MB'
-- random_page_cost = 1.1  -- SSD
-- max_parallel_workers_per_gather = 2
-- checkpoint_completion_target = 0.9
```

### OLAP Workload

```sql
-- Analytics/reporting settings
-- shared_buffers = '4GB'
-- effective_cache_size = '12GB'
-- work_mem = '512MB'
-- maintenance_work_mem = '2GB'
-- random_page_cost = 1.1
-- max_parallel_workers_per_gather = 4
-- max_parallel_workers = 8
-- jit = on
```

## Summary

In this chapter, you've learned:

- **Memory Configuration**: shared_buffers, work_mem, effective_cache_size
- **Planner Configuration**: Cost parameters, parallelism, join settings
- **Query Analysis**: pg_stat_statements, auto_explain, log analysis
- **Optimization Process**: Systematic approach to fixing slow queries
- **Monitoring**: Cache ratios, wait events, bloat detection

## Key Takeaways

1. **Memory is Critical**: Tune work_mem to avoid disk sorts
2. **Keep Statistics Fresh**: ANALYZE regularly
3. **Use pg_stat_statements**: Find the queries worth optimizing
4. **Systematic Approach**: Analyze → Understand → Fix → Verify
5. **Monitor Continuously**: Cache hit ratio, wait events, bloat

## Next Steps

With configuration knowledge in hand, let's explore real-world patterns and anti-patterns in Chapter 8.

---

**Ready for Chapter 8?** [Real-World Patterns](08-real-world-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
