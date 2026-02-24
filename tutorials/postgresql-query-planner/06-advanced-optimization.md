---
layout: default
title: "Chapter 6: Advanced Optimization"
parent: "PostgreSQL Query Planner"
nav_order: 6
---

# Chapter 6: Advanced Optimization

Welcome to **Chapter 6: Advanced Optimization**. In this part of **PostgreSQL Query Planner Deep Dive**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> CTEs, window functions, subquery optimization, and parallel query execution.

## Overview

Beyond basic scan and join optimization, PostgreSQL offers advanced features that require specific optimization knowledge. This chapter covers CTEs, window functions, subqueries, and parallel execution.

## Common Table Expressions (CTEs)

### CTE Materialization

```sql
-- Before PostgreSQL 12: CTEs were always materialized
-- PostgreSQL 12+: Planner can inline CTEs

-- Explicit materialization (forces separate execution)
WITH orders_summary AS MATERIALIZED (
    SELECT customer_id, SUM(total) as total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT c.name, os.total_spent
FROM customers c
JOIN orders_summary os ON c.id = os.customer_id;

-- Inline (allows optimization as subquery)
WITH orders_summary AS NOT MATERIALIZED (
    SELECT customer_id, SUM(total) as total_spent
    FROM orders
    GROUP BY customer_id
)
SELECT c.name, os.total_spent
FROM customers c
JOIN orders_summary os ON c.id = os.customer_id;
```

### When to Materialize

```sql
-- Materialize when:
-- 1. CTE is referenced multiple times
WITH stats AS MATERIALIZED (
    SELECT AVG(total) as avg_total, STDDEV(total) as std_total
    FROM orders
)
SELECT o.*, s.avg_total, s.std_total,
       (o.total - s.avg_total) / s.std_total as z_score
FROM orders o, stats s;

-- 2. CTE result is small and expensive to compute
WITH expensive_calc AS MATERIALIZED (
    SELECT id, complex_function(data) as result
    FROM large_table
    WHERE complex_condition
)
SELECT * FROM expensive_calc;

-- Don't materialize when:
-- CTE is used once and planner can optimize together
WITH recent_orders AS (
    SELECT * FROM orders WHERE created_at > CURRENT_DATE - 7
)
SELECT * FROM recent_orders WHERE customer_id = 42;
-- Better as inline - filter pushdown possible
```

### Recursive CTEs

```sql
-- Recursive CTEs are always materialized
WITH RECURSIVE subordinates AS (
    -- Base case
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;

-- Optimization: Add termination conditions
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE id = 1  -- Start from specific manager

    UNION ALL

    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
    WHERE s.level < 10  -- Limit depth
)
SELECT * FROM subordinates;
```

## Window Functions

### Window Function Execution

```sql
-- Window functions require sorted data
-- Planner adds Sort node if needed

EXPLAIN ANALYZE
SELECT
    id,
    customer_id,
    total,
    SUM(total) OVER (PARTITION BY customer_id ORDER BY created_at) as running_total
FROM orders;

-- WindowAgg
--   ->  Sort
--         Sort Key: customer_id, created_at
--         ->  Seq Scan on orders
```

### Optimizing Window Functions

```sql
-- Index for window function ordering
CREATE INDEX idx_orders_customer_created
ON orders(customer_id, created_at);

-- Now can avoid sort
EXPLAIN ANALYZE
SELECT
    id,
    customer_id,
    total,
    SUM(total) OVER (PARTITION BY customer_id ORDER BY created_at) as running_total
FROM orders;

-- WindowAgg
--   ->  Index Scan using idx_orders_customer_created
```

### Multiple Window Functions

```sql
-- Same window specification shares one sort
SELECT
    id,
    SUM(total) OVER w as running_sum,
    AVG(total) OVER w as running_avg,
    COUNT(*) OVER w as running_count
FROM orders
WINDOW w AS (PARTITION BY customer_id ORDER BY created_at);

-- Different partitions require separate sorts
SELECT
    id,
    SUM(total) OVER (PARTITION BY customer_id ORDER BY created_at),
    SUM(total) OVER (PARTITION BY region ORDER BY created_at)
FROM orders;
-- Two separate WindowAgg operations
```

### Frame Optimization

```sql
-- Default frame: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
-- For running totals, ROWS is more efficient

SELECT
    id,
    -- Uses RANGE (slower for ties)
    SUM(total) OVER (ORDER BY created_at) as range_sum,
    -- Uses ROWS (faster)
    SUM(total) OVER (ORDER BY created_at ROWS UNBOUNDED PRECEDING) as rows_sum
FROM orders;
```

## Subquery Optimization

### Subquery Flattening

```sql
-- PostgreSQL flattens simple subqueries
SELECT * FROM (
    SELECT * FROM orders WHERE total > 100
) sub
WHERE sub.customer_id = 42;

-- Becomes:
SELECT * FROM orders WHERE total > 100 AND customer_id = 42;

-- Check with EXPLAIN - single Seq Scan, not SubPlan
```

### EXISTS vs IN vs JOIN

```sql
-- All three can be equivalent
-- EXISTS (semi-join)
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- IN (can be converted to semi-join)
SELECT * FROM customers
WHERE id IN (SELECT customer_id FROM orders);

-- JOIN with DISTINCT (often slower)
SELECT DISTINCT c.*
FROM customers c
JOIN orders o ON c.id = o.customer_id;

-- Check execution plans - EXISTS and IN often produce same plan
EXPLAIN SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

### Correlated Subqueries

```sql
-- Correlated subquery in SELECT
EXPLAIN ANALYZE
SELECT
    c.name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) as order_count
FROM customers c;

-- Often transformed to join
-- If not, appears as SubPlan (slower)

-- Manual optimization using lateral join
SELECT c.name, o.order_count
FROM customers c
LEFT JOIN LATERAL (
    SELECT COUNT(*) as order_count
    FROM orders o
    WHERE o.customer_id = c.id
) o ON true;
```

### NOT IN vs NOT EXISTS

```sql
-- NOT IN has NULL-handling issues
SELECT * FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
-- If any customer_id is NULL, returns no rows!

-- NOT EXISTS is NULL-safe
SELECT * FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- Left join anti-pattern
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

## Parallel Query Execution

### Parallel Scan

```sql
-- Enable parallel query
SET max_parallel_workers_per_gather = 4;
SET parallel_tuple_cost = 0.01;
SET parallel_setup_cost = 1000;

-- Parallel sequential scan
EXPLAIN ANALYZE
SELECT COUNT(*) FROM large_table WHERE status = 'active';

-- Gather
--   Workers Planned: 2
--   ->  Partial Aggregate
--         ->  Parallel Seq Scan on large_table
--               Filter: (status = 'active')
```

### Parallel Join

```sql
-- Parallel hash join
EXPLAIN ANALYZE
SELECT c.name, SUM(o.total)
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;

-- Gather
--   ->  Parallel Hash Join
--         ->  Parallel Seq Scan on orders
--         ->  Parallel Hash
--               ->  Parallel Seq Scan on customers
```

### Parallel Index Scan

```sql
-- PostgreSQL 13+ supports parallel index scans
EXPLAIN ANALYZE
SELECT * FROM orders WHERE total > 1000;

-- Index-only scans can be parallel too
CREATE INDEX idx_orders_total ON orders(total) INCLUDE (customer_id);

EXPLAIN ANALYZE
SELECT total, customer_id FROM orders WHERE total > 1000;
```

### Parallel Aggregation

```sql
-- Two-phase aggregation
EXPLAIN ANALYZE
SELECT customer_id, COUNT(*), SUM(total)
FROM orders
GROUP BY customer_id;

-- Finalize GroupAggregate
--   ->  Gather Merge
--         ->  Partial GroupAggregate
--               ->  Parallel Index Scan
```

### Parallel Safety

```sql
-- Some functions prevent parallelism
-- Check function parallel safety:
SELECT proname, proparallel
FROM pg_proc
WHERE proname = 'my_function';

-- proparallel values:
-- 's' = safe
-- 'r' = restricted (can run in parallel worker but not leader)
-- 'u' = unsafe (prevents parallelism)

-- Mark function as parallel safe
CREATE OR REPLACE FUNCTION my_safe_function(x INT)
RETURNS INT
LANGUAGE sql
PARALLEL SAFE
AS $$ SELECT x * 2 $$;
```

## Query Rewriting

### JIT Compilation

```sql
-- Just-in-time compilation for complex queries
SET jit = on;
SET jit_above_cost = 100000;

EXPLAIN (ANALYZE, BUFFERS)
SELECT SUM(total), AVG(total), COUNT(DISTINCT customer_id)
FROM orders
WHERE created_at > '2024-01-01';

-- JIT:
--   Functions: 10
--   Options: Inlining true, Optimization true, Expressions true, Deforming true
--   Timing: Generation 1.234 ms, Inlining 5.678 ms, Optimization 12.345 ms, Emission 23.456 ms, Total 42.713 ms
```

### Query Simplification

```sql
-- PostgreSQL simplifies constant expressions
EXPLAIN SELECT * FROM orders WHERE 1 = 1 AND customer_id = 42;
-- Simplified to: customer_id = 42

-- Dead code elimination
EXPLAIN SELECT * FROM orders WHERE 1 = 0;
-- Result (never executed scan)

-- Constraint exclusion
CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

EXPLAIN SELECT * FROM orders WHERE created_at = '2023-01-15';
-- Excludes 2024 partitions
```

## Summary

In this chapter, you've learned:

- **CTEs**: Materialization control and recursive optimization
- **Window Functions**: Index optimization and frame selection
- **Subqueries**: Flattening, EXISTS vs IN, correlated subquery handling
- **Parallel Execution**: Parallel scans, joins, and aggregation
- **Advanced**: JIT compilation and query rewriting

## Key Takeaways

1. **CTE Materialization**: Use MATERIALIZED/NOT MATERIALIZED explicitly when it matters
2. **Window Function Indexes**: Create indexes matching PARTITION BY and ORDER BY
3. **Prefer EXISTS**: Over IN for NULL-safe anti-joins
4. **Enable Parallelism**: For large analytical queries
5. **Check Parallel Safety**: Custom functions may need PARALLEL SAFE

## Next Steps

With advanced optimization knowledge, let's move to performance tuning configuration in Chapter 7.

---

**Ready for Chapter 7?** [Performance Tuning](07-performance-tuning.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `customer_id`, `orders` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Advanced Optimization` as an operating subsystem inside **PostgreSQL Query Planner Deep Dive**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `WHERE`, `total`, `EXPLAIN` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Advanced Optimization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `customer_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `orders`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `SELECT` and `customer_id` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Index Deep Dive](05-index-strategies.md)
- [Next Chapter: Chapter 7: Performance Tuning](07-performance-tuning.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
