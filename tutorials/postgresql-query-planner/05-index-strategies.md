---
layout: default
title: "Chapter 5: Index Deep Dive"
parent: "PostgreSQL Query Planner"
nav_order: 5
---

# Chapter 5: Index Deep Dive

> Advanced indexing strategies including B-tree internals, partial indexes, expression indexes, and covering indexes.

## Overview

Indexes are fundamental to query performance. This chapter explores PostgreSQL index types in depth, when to use each, and advanced indexing strategies for complex scenarios.

## B-Tree Index Internals

### Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                     B-Tree Structure                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         Root Node                               │
│                    ┌────────────────┐                           │
│                    │ 50 │ 100 │ 150 │                           │
│                    └──┬────┬────┬───┘                           │
│           ┌──────────┘    │    └──────────┐                     │
│           ▼               ▼               ▼                     │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐                │
│    │ 20 │ 35  │    │ 70 │ 85  │    │120 │ 135 │   Internal     │
│    └──┬───┬───┘    └──┬───┬───┘    └──┬───┬───┘   Nodes        │
│       │   │           │   │           │   │                     │
│       ▼   ▼           ▼   ▼           ▼   ▼                     │
│    ┌─────────────────────────────────────────┐                  │
│    │  Leaf Nodes (contain TIDs to heap)      │                  │
│    │  [5→(0,1)] [20→(2,3)] [35→(1,2)] ...   │                  │
│    └─────────────────────────────────────────┘                  │
│                                                                 │
│  Leaf nodes are linked for range scans:                         │
│  [5,10,15] ←→ [20,25,30] ←→ [35,40,45] ←→ ...                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### B-Tree Operations

```sql
-- Equality search: O(log N)
-- Traverse from root to leaf

-- Range search: O(log N + K)
-- Find start, scan linked leaves

-- Supported operators: <, <=, =, >=, >, BETWEEN, IN
-- Pattern matching: LIKE 'prefix%' (not '%suffix')

-- Check index usage
EXPLAIN SELECT * FROM users WHERE id = 42;      -- Equality
EXPLAIN SELECT * FROM users WHERE id > 100;     -- Range
EXPLAIN SELECT * FROM users WHERE id IN (1,2,3); -- IN list
```

### Multi-Column B-Tree

```sql
-- Column order matters!
CREATE INDEX idx_multi ON orders(customer_id, created_at, status);

-- Can use index (left-to-right prefix)
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
EXPLAIN SELECT * FROM orders WHERE customer_id = 42 AND created_at > '2024-01-01';
EXPLAIN SELECT * FROM orders WHERE customer_id = 42 AND created_at > '2024-01-01' AND status = 'pending';

-- Cannot efficiently use index
EXPLAIN SELECT * FROM orders WHERE status = 'pending';  -- Skip first columns
EXPLAIN SELECT * FROM orders WHERE created_at > '2024-01-01';  -- Skip first column

-- Index skip scan (PostgreSQL 14+) can help in some cases
```

## Index Types

### Hash Index

```sql
-- Only supports equality comparisons
CREATE INDEX idx_users_email_hash ON users USING hash(email);

-- Use case: exact match only, no range queries
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';

-- Hash vs B-tree:
-- Hash: Slightly faster for equality, smaller for long keys
-- B-tree: More versatile, supports ranges and sorting
```

### GiST Index

```sql
-- Generalized Search Tree: extensible for custom types
-- Used for: geometric, full-text, range types

-- Geometric example
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    coords POINT
);

CREATE INDEX idx_locations_coords ON locations USING gist(coords);

-- Find points within a box
EXPLAIN SELECT * FROM locations
WHERE coords <@ box '((0,0),(10,10))';

-- Full-text search
CREATE INDEX idx_documents_content ON documents
USING gist(to_tsvector('english', content));
```

### GIN Index

```sql
-- Generalized Inverted Index: for composite values
-- Used for: arrays, JSONB, full-text search

-- Array containment
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    tags TEXT[]
);

CREATE INDEX idx_articles_tags ON articles USING gin(tags);

EXPLAIN SELECT * FROM articles WHERE tags @> ARRAY['postgresql'];

-- JSONB
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB
);

CREATE INDEX idx_events_data ON events USING gin(data);

EXPLAIN SELECT * FROM events WHERE data @> '{"type": "click"}';

-- Full-text with GIN (faster queries, slower updates than GiST)
CREATE INDEX idx_docs_fts ON documents
USING gin(to_tsvector('english', content));
```

### BRIN Index

```sql
-- Block Range Index: for naturally ordered data
-- Very small, summarizes page ranges

CREATE TABLE sensor_data (
    id SERIAL,
    sensor_id INT,
    timestamp TIMESTAMPTZ,
    value DECIMAL
);

-- Data naturally ordered by time (append-only)
CREATE INDEX idx_sensor_time_brin ON sensor_data
USING brin(timestamp);

-- Much smaller than B-tree for large tables
-- Works well when data is physically ordered by index column

-- Check correlation
SELECT correlation FROM pg_stats
WHERE tablename = 'sensor_data' AND attname = 'timestamp';
-- Should be close to 1.0 for BRIN to be effective
```

## Advanced Index Strategies

### Partial Indexes

```sql
-- Index only a subset of rows
-- Saves space, improves performance for specific queries

-- Index only active users
CREATE INDEX idx_users_active_email
ON users(email)
WHERE status = 'active';

-- Query must match the WHERE clause
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com' AND status = 'active';
-- Uses partial index

EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
-- Cannot use partial index (might include inactive users)

-- Partial index on NULLs
CREATE INDEX idx_orders_pending
ON orders(created_at)
WHERE shipped_at IS NULL;
```

### Expression Indexes

```sql
-- Index on expressions, not just columns
CREATE INDEX idx_users_lower_email
ON users(lower(email));

-- Must use same expression in query
EXPLAIN SELECT * FROM users WHERE lower(email) = 'john@example.com';
-- Uses expression index

-- Date extraction
CREATE INDEX idx_orders_month
ON orders(date_trunc('month', created_at));

EXPLAIN SELECT * FROM orders
WHERE date_trunc('month', created_at) = '2024-01-01';
```

### Covering Indexes (INCLUDE)

```sql
-- Include non-key columns for index-only scans
CREATE INDEX idx_orders_customer_covering
ON orders(customer_id)
INCLUDE (total, status);

-- Index-only scan possible
EXPLAIN SELECT customer_id, total, status
FROM orders
WHERE customer_id = 42;

-- Key columns: used for searching
-- Included columns: stored but not searchable
-- Included columns don't affect index ordering
```

### Unique Indexes

```sql
-- Enforce uniqueness
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Partial unique constraint
CREATE UNIQUE INDEX idx_users_active_email
ON users(email)
WHERE deleted_at IS NULL;

-- Allows duplicate emails for deleted users
-- Only one active user per email
```

## Index Maintenance

### Monitoring Index Health

```sql
-- Index usage statistics
SELECT
    schemaname,
    relname as tablename,
    indexrelname as indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT
    schemaname || '.' || relname as table,
    indexrelname as index,
    pg_size_pretty(pg_relation_size(indexrelid)) as size,
    idx_scan as scans
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Index Bloat

```sql
-- Check for bloated indexes
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    idx_scan,
    idx_tup_read
FROM pg_stat_user_indexes
JOIN pg_index USING (indexrelid)
WHERE NOT indisunique;

-- Rebuild bloated index
REINDEX INDEX idx_orders_customer;

-- Concurrent rebuild (no locks)
REINDEX INDEX CONCURRENTLY idx_orders_customer;
```

### Index-Only Scan Requirements

```sql
-- Check visibility map coverage
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE relname = 'orders';

-- Vacuum to update visibility map
VACUUM orders;

-- Check heap fetches in index-only scan
EXPLAIN (ANALYZE, BUFFERS)
SELECT id FROM orders WHERE customer_id = 42;
-- Heap Fetches: 0 = optimal
-- Heap Fetches: N > 0 = visibility map needs update
```

## Index Selection Guidelines

### When to Create Indexes

```sql
-- 1. Primary keys (automatic)
-- 2. Foreign keys (manual but critical)
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- 3. Frequently filtered columns
CREATE INDEX idx_orders_status ON orders(status);

-- 4. Join columns
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- 5. Sort columns (if ordering without filtering)
CREATE INDEX idx_orders_created ON orders(created_at DESC);
```

### Index Column Order

```sql
-- Most selective column first? Not always!
-- Consider query patterns:

-- If always filtering by status, then optionally by date:
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- If sorting by date after filtering by status:
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- Equality before range
-- WHERE status = 'pending' AND created_at > '2024-01-01'
-- status (equality) first, created_at (range) second
```

### Index Size Considerations

```sql
-- Check index sizes
SELECT
    indexrelname as index,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Consider partial indexes for large tables
-- Full index on status
CREATE INDEX idx_orders_status ON orders(status);

-- Partial index (smaller)
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';
```

## Summary

In this chapter, you've learned:

- **B-Tree Internals**: Structure, operations, multi-column behavior
- **Index Types**: Hash, GiST, GIN, BRIN and their use cases
- **Advanced Strategies**: Partial, expression, covering indexes
- **Maintenance**: Monitoring usage, detecting bloat, reindexing
- **Selection**: When and how to create effective indexes

## Key Takeaways

1. **Column Order Matters**: In multi-column indexes, leftmost columns are critical
2. **Partial Indexes**: Save space and target specific query patterns
3. **Covering Indexes**: Enable index-only scans with INCLUDE
4. **BRIN for Time Series**: Much smaller for naturally ordered data
5. **Monitor Usage**: Remove unused indexes to reduce write overhead

## Next Steps

Now that you understand indexing, let's explore advanced query optimization techniques in Chapter 6.

---

**Ready for Chapter 6?** [Advanced Optimization](06-advanced-optimization.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
