---
layout: default
title: "Chapter 3: Scan Operations"
parent: "PostgreSQL Query Planner"
nav_order: 3
---

# Chapter 3: Scan Operations

> Explore sequential scans, index scans, bitmap scans, and understand when PostgreSQL chooses each method.

## Overview

Scan operations are the fundamental building blocks of query execution. Understanding when and why PostgreSQL chooses different scan methods is crucial for query optimization.

## Sequential Scan

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     Sequential Scan                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Table Pages: [1] → [2] → [3] → [4] → [5] → ...                │
│                                                                 │
│  Process:                                                       │
│  1. Read pages sequentially from disk                          │
│  2. Examine each tuple                                          │
│  3. Apply WHERE conditions                                      │
│  4. Return matching rows                                        │
│                                                                 │
│  Advantages:                                                    │
│  • Efficient sequential I/O                                     │
│  • No index lookup overhead                                     │
│  • Best for non-selective queries                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### When PostgreSQL Chooses Seq Scan

```sql
-- 1. No suitable index exists
EXPLAIN SELECT * FROM users WHERE bio LIKE '%developer%';
-- No index can help with middle wildcard

-- 2. Query returns large portion of table
EXPLAIN SELECT * FROM orders WHERE status IN ('pending', 'processing', 'shipped');
-- If these cover 80% of rows, seq scan is cheaper

-- 3. Table is very small
EXPLAIN SELECT * FROM countries WHERE code = 'US';
-- Few pages = seq scan overhead is minimal

-- 4. Planner estimates seq scan is cheaper
-- Even with index, if selectivity is low
```

### Forcing or Avoiding Seq Scan

```sql
-- Disable seq scan (for testing only!)
SET enable_seqscan = off;
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
-- Now forced to use index

-- Re-enable
SET enable_seqscan = on;

-- Better approach: understand WHY seq scan was chosen
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 42;
```

## Index Scan

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                       Index Scan                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  B-tree Index          Heap Table                               │
│  ┌─────────┐          ┌─────────────────┐                       │
│  │ Root    │          │ Page 1: □ □ □   │                       │
│  └────┬────┘          │ Page 2: □ □ □   │                       │
│       │               │ Page 3: □ ■ □   │ ← Found!              │
│  ┌────┴────┐          │ Page 4: □ □ □   │                       │
│  │ Branch  │          │ Page 5: □ ■ □   │ ← Found!              │
│  └────┬────┘          └─────────────────┘                       │
│       │                     ↑   ↑                               │
│  ┌────┴────┐                │   │                               │
│  │ Leaf    │────────────────┘   │                               │
│  │ (TIDs)  │────────────────────┘                               │
│  └─────────┘                                                    │
│                                                                 │
│  Process:                                                       │
│  1. Traverse index to find matching entries                     │
│  2. For each match, fetch heap tuple using TID                  │
│  3. Recheck visibility and conditions                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Index Scan Example

```sql
-- Create index
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Query using index
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42;

-- Output:
-- Index Scan using idx_orders_customer on orders
--   (cost=0.43..8.45 rows=5 width=100)
--   (actual time=0.015..0.020 rows=5 loops=1)
--   Index Cond: (customer_id = 42)
```

### Index Scan Cost Factors

```sql
-- Cost depends on:
-- 1. Index depth (typically 3-4 levels for B-tree)
-- 2. Number of matching index entries
-- 3. Number of heap pages to fetch
-- 4. Correlation between index order and heap order

-- Check correlation
SELECT correlation
FROM pg_stats
WHERE tablename = 'orders' AND attname = 'customer_id';

-- High correlation (close to 1 or -1): mostly sequential heap access
-- Low correlation (close to 0): random heap access
```

## Index Only Scan

### How It Works

```sql
-- When all needed columns are in the index
CREATE INDEX idx_users_email_name ON users(email, name);

-- This can use index-only scan
EXPLAIN ANALYZE
SELECT email, name FROM users WHERE email = 'john@example.com';

-- Index Only Scan using idx_users_email_name on users
--   Index Cond: (email = 'john@example.com')
--   Heap Fetches: 0  -- No heap access needed!
```

### Visibility Map Requirement

```sql
-- Index Only Scan still needs to check visibility
-- Uses visibility map to avoid heap fetches

-- View visibility map coverage
SELECT
    relname,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
WHERE relname = 'users';

-- VACUUM updates visibility map
VACUUM users;

-- After vacuum, Heap Fetches should decrease
```

### Covering Indexes (INCLUDE)

```sql
-- Include non-key columns for index-only scans
CREATE INDEX idx_orders_customer_covering
ON orders(customer_id)
INCLUDE (total, created_at);

-- Now this can use index-only scan
EXPLAIN ANALYZE
SELECT customer_id, total, created_at
FROM orders
WHERE customer_id = 42;
```

## Bitmap Scans

### Two-Phase Process

```
┌─────────────────────────────────────────────────────────────────┐
│                       Bitmap Scan                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Bitmap Index Scan                                     │
│  ┌──────────────────────────────────────────┐                   │
│  │ Scan index, build bitmap of matching TIDs │                   │
│  │                                          │                   │
│  │ Bitmap: [0,0,1,0,1,1,0,0,1,0,1,...]      │                   │
│  │         (1 = page contains matching row)  │                   │
│  └──────────────────────────────────────────┘                   │
│                                                                 │
│  Phase 2: Bitmap Heap Scan                                      │
│  ┌──────────────────────────────────────────┐                   │
│  │ Read heap pages in physical order         │                   │
│  │ Only visit pages marked in bitmap         │                   │
│  │ Recheck conditions on each tuple          │                   │
│  └──────────────────────────────────────────┘                   │
│                                                                 │
│  Advantages:                                                    │
│  • Avoids repeated random heap access                           │
│  • Sorts page access for sequential I/O                         │
│  • Can combine multiple indexes (BitmapAnd/BitmapOr)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Bitmap Scan Example

```sql
-- Single index bitmap scan
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id BETWEEN 100 AND 200;

-- Bitmap Heap Scan on orders
--   Recheck Cond: (customer_id >= 100 AND customer_id <= 200)
--   Heap Blocks: exact=50
--   ->  Bitmap Index Scan on idx_orders_customer
--         Index Cond: (customer_id >= 100 AND customer_id <= 200)
```

### Combining Multiple Indexes

```sql
-- Create multiple indexes
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(created_at);

-- Query using multiple conditions
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE status = 'pending'
  AND created_at > '2024-01-01';

-- BitmapAnd
--   ->  Bitmap Index Scan on idx_orders_status
--         Index Cond: (status = 'pending')
--   ->  Bitmap Index Scan on idx_orders_date
--         Index Cond: (created_at > '2024-01-01')
```

### Bitmap OR Conditions

```sql
-- OR conditions with bitmap
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 42
   OR customer_id = 43
   OR customer_id = 44;

-- BitmapOr
--   ->  Bitmap Index Scan on idx_orders_customer
--         Index Cond: (customer_id = 42)
--   ->  Bitmap Index Scan on idx_orders_customer
--         Index Cond: (customer_id = 43)
--   ->  Bitmap Index Scan on idx_orders_customer
--         Index Cond: (customer_id = 44)
```

### Lossy Bitmap

```sql
-- When bitmap exceeds work_mem, becomes "lossy"
-- Stores page numbers instead of exact TIDs

-- Check if bitmap was lossy
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_table WHERE category = 'common';

-- Heap Blocks: exact=100 lossy=50
-- "lossy" means page-level bitmap, must recheck all rows

-- Increase work_mem to avoid lossy bitmaps
SET work_mem = '256MB';
```

## TID Scan

### Direct Tuple Access

```sql
-- Scan by tuple ID (rarely used in practice)
EXPLAIN SELECT * FROM users WHERE ctid = '(0,1)';

-- Tid Scan on users
--   TID Cond: (ctid = '(0,1)'::tid)

-- ctid format: (page_number, tuple_number)
SELECT ctid, * FROM users LIMIT 5;
-- (0,1) | 1 | John | ...
-- (0,2) | 2 | Jane | ...
```

## Choosing the Right Scan

### Decision Factors

```sql
-- PostgreSQL considers:
-- 1. Selectivity: What fraction of rows match?
-- 2. Available indexes: Which conditions can use indexes?
-- 3. Table size: Is seq scan overhead acceptable?
-- 4. Correlation: Will index scan cause random I/O?
-- 5. work_mem: Enough for bitmap operations?

-- View planner's estimates
EXPLAIN (VERBOSE, COSTS)
SELECT * FROM orders WHERE customer_id = 42;
```

### Selectivity Thresholds

```sql
-- Rough guidelines (vary by situation):
-- < 1-5% of rows: Index Scan likely
-- 5-20% of rows: Bitmap Scan likely
-- > 20% of rows: Sequential Scan likely

-- Test with different selectivities
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;     -- Very selective
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending';   -- Less selective
EXPLAIN ANALYZE SELECT * FROM orders WHERE total > 0;            -- Not selective
```

### Practical Comparison

```sql
-- Create test scenario
CREATE TABLE scan_test AS
SELECT
    generate_series(1, 1000000) as id,
    (random() * 1000)::int as category_id,
    random() * 10000 as amount,
    md5(random()::text) as data
;

CREATE INDEX idx_scan_test_category ON scan_test(category_id);
ANALYZE scan_test;

-- Compare scan methods at different selectivities
-- 1 row (0.0001%)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM scan_test WHERE category_id = 500 AND id = 12345;

-- ~1000 rows (0.1%)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM scan_test WHERE category_id = 500;

-- ~100000 rows (10%)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM scan_test WHERE category_id < 100;

-- ~500000 rows (50%)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM scan_test WHERE category_id < 500;
```

## Summary

In this chapter, you've learned:

- **Sequential Scan**: Reads entire table, best for unselective queries
- **Index Scan**: Uses index + heap access, best for highly selective queries
- **Index Only Scan**: Satisfies query from index alone when possible
- **Bitmap Scan**: Two-phase scan for medium selectivity, can combine indexes
- **Scan Selection**: Factors influencing planner's choice

## Key Takeaways

1. **Selectivity Matters**: Low selectivity often means seq scan wins
2. **Correlation Affects Index Scans**: Random I/O is expensive
3. **Bitmap for Middle Ground**: Combines index efficiency with sequential heap access
4. **Index Only Scans**: Keep visibility map current with VACUUM
5. **Don't Force Scans**: Understand why the planner chose what it did

## Next Steps

Now that you understand scan operations, let's explore how PostgreSQL joins tables in Chapter 4.

---

**Ready for Chapter 4?** [Join Strategies](04-join-strategies.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
