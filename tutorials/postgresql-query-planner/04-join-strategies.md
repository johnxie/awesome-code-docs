---
layout: default
title: "Chapter 4: Join Strategies"
parent: "PostgreSQL Query Planner"
nav_order: 4
---

# Chapter 4: Join Strategies

Welcome to **Chapter 4: Join Strategies**. In this part of **PostgreSQL Query Planner Deep Dive**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master nested loop, hash join, and merge join operations, including when each is optimal.

## Overview

Join operations combine rows from multiple tables based on related columns. PostgreSQL implements three primary join algorithms, each optimized for different scenarios.

## Join Algorithm Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    Join Algorithm Summary                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Nested Loop                                                    │
│  • Best for: Small outer table, indexed inner table             │
│  • Complexity: O(N × M) worst case, O(N × log M) with index     │
│  • Memory: Minimal                                              │
│                                                                 │
│  Hash Join                                                      │
│  • Best for: Larger tables, equality joins                      │
│  • Complexity: O(N + M)                                         │
│  • Memory: Builds hash table (work_mem dependent)               │
│                                                                 │
│  Merge Join                                                     │
│  • Best for: Pre-sorted data, merge operations                  │
│  • Complexity: O(N log N + M log M) with sort, O(N + M) if sorted│
│  • Memory: Moderate (for sorting)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Nested Loop Join

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     Nested Loop Join                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Outer Table (N rows)      Inner Table (M rows)                 │
│  ┌─────────────┐           ┌─────────────┐                      │
│  │ Row 1 ──────┼──────────▶│ Scan all    │                      │
│  │ Row 2 ──────┼──────────▶│ Scan all    │                      │
│  │ Row 3 ──────┼──────────▶│ Scan all    │                      │
│  │ ...         │           │ ...         │                      │
│  │ Row N ──────┼──────────▶│ Scan all    │                      │
│  └─────────────┘           └─────────────┘                      │
│                                                                 │
│  Pseudocode:                                                    │
│  FOR each row in outer_table:                                   │
│      FOR each row in inner_table:                               │
│          IF join_condition matches:                             │
│              output combined row                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Basic Nested Loop

```sql
-- Setup
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    total DECIMAL,
    created_at TIMESTAMP
);

-- Small outer, indexed inner = Nested Loop
EXPLAIN ANALYZE
SELECT c.name, o.total
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.id = 42;

-- Nested Loop  (cost=0.57..16.61 rows=5 width=40)
--   ->  Index Scan using customers_pkey on customers c
--         Index Cond: (id = 42)
--   ->  Index Scan using idx_orders_customer on orders o
--         Index Cond: (customer_id = c.id)
```

### Nested Loop Variants

```sql
-- Nested Loop with inner sequential scan
-- (when inner table is small or no useful index)
EXPLAIN ANALYZE
SELECT c.name, o.total
FROM (SELECT * FROM customers LIMIT 5) c
JOIN orders o ON c.id = o.customer_id;

-- Nested Loop with materialized inner
-- (inner is scanned multiple times, so materialized)
EXPLAIN ANALYZE
SELECT c.name, s.total
FROM customers c
JOIN (SELECT customer_id, SUM(total) as total
      FROM orders GROUP BY customer_id) s
ON c.id = s.customer_id;
```

### When Nested Loop is Chosen

```sql
-- 1. Very selective outer table
EXPLAIN SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.id = 12345;

-- 2. Index available on inner table's join column
-- 3. LIMIT clause (early termination)
EXPLAIN SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
LIMIT 10;

-- 4. Non-equality joins (only option)
EXPLAIN SELECT * FROM events e1
JOIN events e2 ON e1.timestamp < e2.timestamp
WHERE e1.type = 'start' AND e2.type = 'end';
```

## Hash Join

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                       Hash Join                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Build Hash Table (from smaller table)                 │
│  ┌─────────────┐         ┌─────────────────────┐                │
│  │ Inner Table │────────▶│ Hash Table          │                │
│  │ (build)     │         │ ┌───┬───────────┐   │                │
│  │             │         │ │ h1│ rows...   │   │                │
│  │             │         │ │ h2│ rows...   │   │                │
│  └─────────────┘         │ │ h3│ rows...   │   │                │
│                          │ └───┴───────────┘   │                │
│                          └─────────────────────┘                │
│                                                                 │
│  Phase 2: Probe (scan outer table)                              │
│  ┌─────────────┐         ┌─────────────────────┐                │
│  │ Outer Table │         │ Hash Table          │                │
│  │ (probe)     │         │                     │                │
│  │  Row 1 ─────┼────────▶│ hash(key) → lookup  │                │
│  │  Row 2 ─────┼────────▶│ hash(key) → lookup  │                │
│  │  ...        │         │                     │                │
│  └─────────────┘         └─────────────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Hash Join Example

```sql
-- Typical hash join scenario
EXPLAIN ANALYZE
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;

-- Hash Join  (cost=20.00..150.00 rows=1000 width=48)
--   Hash Cond: (o.customer_id = c.id)
--   ->  Seq Scan on orders o
--   ->  Hash
--         ->  Seq Scan on customers c
--         Buckets: 1024  Batches: 1  Memory Usage: 64kB
```

### Hash Join Memory

```sql
-- work_mem controls hash table size
SHOW work_mem;

-- If hash table exceeds work_mem, spills to disk (batches)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_table1 l1
JOIN large_table2 l2 ON l1.key = l2.key;

-- Hash  (Batches: 4 means 4 passes due to memory pressure)

-- Increase work_mem for large joins
SET work_mem = '256MB';
```

### Parallel Hash Join

```sql
-- PostgreSQL can parallelize hash joins
SET max_parallel_workers_per_gather = 4;

EXPLAIN ANALYZE
SELECT c.region, SUM(o.total)
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.region;

-- Gather
--   Workers Planned: 2
--   ->  Parallel Hash Join
--         ->  Parallel Seq Scan on orders o
--         ->  Parallel Hash
--               ->  Parallel Seq Scan on customers c
```

## Merge Join

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                       Merge Join                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Pre-sorted Inputs (or sort first)                              │
│                                                                 │
│  Outer (sorted)    Inner (sorted)                               │
│  ┌─────────┐       ┌─────────┐                                  │
│  │ 1 ──────┼───────┼── 1     │  Match!                         │
│  │ 2 ──────┼───────┼── 2     │  Match!                         │
│  │ 3       │       │   2     │  (same key, continue inner)     │
│  │ 4 ──────┼───────┼── 4     │  Match!                         │
│  │ 5       │       │   6     │  (advance outer)                │
│  │ 6 ──────┼───────┼── 6     │  Match!                         │
│  └─────────┘       └─────────┘                                  │
│                                                                 │
│  Process: Advance pointers in sorted order                      │
│  - If outer < inner: advance outer                              │
│  - If outer > inner: advance inner                              │
│  - If equal: output match, advance both                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Merge Join Example

```sql
-- Create indexes that provide sorted input
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Query that can use merge join
EXPLAIN ANALYZE
SELECT c.name, o.total
FROM customers c
JOIN orders o ON c.id = o.customer_id
ORDER BY c.id;

-- Merge Join  (cost=0.56..500.00 rows=10000 width=48)
--   Merge Cond: (c.id = o.customer_id)
--   ->  Index Scan using customers_pkey on customers c
--   ->  Index Scan using idx_orders_customer on orders o
```

### Merge Join with Sort

```sql
-- When no index provides order, must sort first
EXPLAIN ANALYZE
SELECT * FROM table1 t1
JOIN table2 t2 ON t1.key = t2.key
ORDER BY t1.key;

-- Merge Join
--   ->  Sort
--         Sort Key: t1.key
--         ->  Seq Scan on table1 t1
--   ->  Sort
--         Sort Key: t2.key
--         ->  Seq Scan on table2 t2
```

## Join Selection Factors

### Planner Decision Criteria

```sql
-- Size of tables
-- Presence of indexes
-- Required output ordering
-- Memory available (work_mem)
-- Statistics accuracy

-- Force specific join method (for testing)
SET enable_hashjoin = off;
SET enable_mergejoin = off;
SET enable_nestloop = off;

-- Check which was chosen
EXPLAIN SELECT * FROM t1 JOIN t2 ON t1.id = t2.id;

-- Reset
RESET enable_hashjoin;
RESET enable_mergejoin;
RESET enable_nestloop;
```

### Join Order

```sql
-- PostgreSQL considers different join orders
-- join_collapse_limit controls optimization depth

SHOW join_collapse_limit;  -- Default: 8

-- For queries with many tables
SET join_collapse_limit = 1;  -- Forces written order

-- Complex join
EXPLAIN
SELECT *
FROM a
JOIN b ON a.id = b.a_id
JOIN c ON b.id = c.b_id
JOIN d ON c.id = d.c_id;
```

## Outer Joins

### Left/Right/Full Joins

```sql
-- Left join: Keep all from left, NULL for non-matches
EXPLAIN ANALYZE
SELECT c.name, o.total
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Full outer join: Keep all from both sides
EXPLAIN ANALYZE
SELECT c.name, o.total
FROM customers c
FULL OUTER JOIN orders o ON c.id = o.customer_id;
```

### Anti-Join Pattern

```sql
-- Find customers with no orders
EXPLAIN ANALYZE
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;

-- Alternative: NOT EXISTS
EXPLAIN ANALYZE
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Anti Join (efficient detection of non-matches)
```

### Semi-Join Pattern

```sql
-- Find customers with at least one order
EXPLAIN ANALYZE
SELECT c.*
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Semi Join (stops after first match)
```

## Join Optimization Tips

### Index Strategy

```sql
-- Index foreign keys for nested loop efficiency
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Covering index for index-only join
CREATE INDEX idx_orders_customer_total
ON orders(customer_id) INCLUDE (total);

EXPLAIN
SELECT c.name, o.total
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.id = 42;
```

### work_mem for Hash Joins

```sql
-- Increase work_mem for better hash join performance
SET work_mem = '256MB';

-- Check hash join batching
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_t1 JOIN large_t2 ON large_t1.key = large_t2.key;

-- Batches: 1 = fits in memory (good)
-- Batches: N > 1 = spilled to disk (might need more work_mem)
```

### Join Condition Optimization

```sql
-- Use equality when possible (enables hash/merge join)
-- Bad: range join
SELECT * FROM t1 JOIN t2 ON t1.val > t2.val;

-- Good: equality join
SELECT * FROM t1 JOIN t2 ON t1.key = t2.key;

-- Filter early
SELECT * FROM t1
JOIN t2 ON t1.id = t2.id
WHERE t1.status = 'active';  -- Filter pushdown
```

## Summary

In this chapter, you've learned:

- **Nested Loop**: Best for small outer + indexed inner, non-equality joins
- **Hash Join**: Best for larger tables with equality conditions
- **Merge Join**: Best for pre-sorted data or when order is needed
- **Join Selection**: Factors affecting planner's choice
- **Optimization**: Indexes, work_mem, and join order tuning

## Key Takeaways

1. **Index Foreign Keys**: Critical for nested loop performance
2. **Increase work_mem**: Prevents hash join spilling to disk
3. **Prefer Equality Joins**: Enables more efficient algorithms
4. **Check Batches**: Hash join batches > 1 indicates memory pressure
5. **Join Order Matters**: For many tables, use join_collapse_limit wisely

## Next Steps

Now that you understand join operations, let's dive deep into indexing strategies in Chapter 5.

---

**Ready for Chapter 5?** [Index Deep Dive](05-index-strategies.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `orders`, `customer_id` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Join Strategies` as an operating subsystem inside **PostgreSQL Query Planner Deep Dive**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `JOIN`, `customers`, `EXPLAIN` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Join Strategies` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `orders` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `customer_id`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `SELECT` and `orders` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Scan Operations](03-scan-operations.md)
- [Next Chapter: Chapter 5: Index Deep Dive](05-index-strategies.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
