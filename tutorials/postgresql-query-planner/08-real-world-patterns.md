---
layout: default
title: "Chapter 8: Real-World Patterns"
parent: "PostgreSQL Query Planner"
nav_order: 8
---

# Chapter 8: Real-World Patterns

Welcome to **Chapter 8: Real-World Patterns**. In this part of **PostgreSQL Query Planner Deep Dive**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Common anti-patterns, production debugging techniques, and optimization case studies.

## Overview

This chapter presents real-world scenarios, common mistakes, and proven solutions. Learn from practical examples and case studies to become proficient at diagnosing and fixing query performance issues.

## Common Anti-Patterns

### Anti-Pattern 1: SELECT *

```sql
-- Problem: Fetching unnecessary columns
SELECT * FROM orders WHERE customer_id = 42;

-- Issues:
-- 1. Prevents index-only scans
-- 2. Increases I/O and memory usage
-- 3. Network transfer overhead

-- Solution: Select only needed columns
SELECT id, total, created_at FROM orders WHERE customer_id = 42;

-- With covering index for index-only scan
CREATE INDEX idx_orders_customer_covering
ON orders(customer_id) INCLUDE (id, total, created_at);
```

### Anti-Pattern 2: Functions on Indexed Columns

```sql
-- Problem: Function prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
-- Forces Seq Scan even with index on email

-- Solution 1: Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Solution 2: Store normalized data
ALTER TABLE users ADD COLUMN email_normalized TEXT
    GENERATED ALWAYS AS (LOWER(email)) STORED;
CREATE INDEX idx_users_email_normalized ON users(email_normalized);

-- Solution 3: Avoid function in query
SELECT * FROM users WHERE email = 'john@example.com';
-- If email is always stored lowercase
```

### Anti-Pattern 3: OR Conditions

```sql
-- Problem: OR can prevent index usage
SELECT * FROM orders
WHERE customer_id = 42 OR status = 'pending';

-- May result in Seq Scan even with indexes on both columns

-- Solution 1: UNION ALL
SELECT * FROM orders WHERE customer_id = 42
UNION ALL
SELECT * FROM orders WHERE status = 'pending' AND customer_id != 42;

-- Solution 2: Separate queries in application
-- Query 1: SELECT * FROM orders WHERE customer_id = 42;
-- Query 2: SELECT * FROM orders WHERE status = 'pending';
-- Merge results in application
```

### Anti-Pattern 4: Implicit Type Conversion

```sql
-- Problem: Type mismatch forces conversion
-- Column is INTEGER, but comparing with TEXT
SELECT * FROM orders WHERE customer_id = '42';

-- PostgreSQL converts column: customer_id::text = '42'
-- Index on customer_id cannot be used!

-- Solution: Use matching types
SELECT * FROM orders WHERE customer_id = 42;

-- Check for implicit conversions
EXPLAIN SELECT * FROM orders WHERE customer_id = '42';
-- Look for "Filter" with type cast
```

### Anti-Pattern 5: OFFSET for Pagination

```sql
-- Problem: OFFSET is slow for large offsets
SELECT * FROM orders ORDER BY created_at DESC OFFSET 100000 LIMIT 10;
-- Must scan and skip 100,000 rows!

-- Solution: Keyset pagination
-- First page:
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
-- Returns last created_at = '2024-01-15 10:30:00'

-- Next page:
SELECT * FROM orders
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC
LIMIT 10;

-- Much faster with index on created_at
```

### Anti-Pattern 6: N+1 Query Problem

```sql
-- Problem: Separate query for each related record
-- Application code:
-- customers = SELECT * FROM customers;
-- for each customer:
--     orders = SELECT * FROM orders WHERE customer_id = ?;

-- Solution: Join in single query
SELECT c.*, o.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.region = 'US';

-- Or use array aggregation
SELECT c.*,
       array_agg(row_to_json(o.*)) as orders
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.region = 'US'
GROUP BY c.id;
```

## Debugging Techniques

### Isolating the Problem

```sql
-- Step 1: Get the slow query
-- From pg_stat_statements or application logs

-- Step 2: Test in isolation
\timing on
SELECT ...your query...;

-- Step 3: Get execution plan
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT ...your query...;

-- Step 4: Identify slow nodes
-- Look for nodes with high "actual time"
-- Compare "rows" (estimate) vs "actual rows"
```

### Plan Comparison

```sql
-- Compare plans before and after changes
-- Save original plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT ...original query...;
\g original_plan.json

-- Make change (add index, rewrite query, etc.)

-- Save new plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT ...modified query...;
\g new_plan.json

-- Compare execution times and buffer usage
```

### Finding Missing Indexes

```sql
-- Queries doing Seq Scans on large tables
SELECT
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > 0
  AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;

-- Look at actual queries hitting these tables
-- Use pg_stat_statements to find patterns
```

### Lock Contention

```sql
-- Find blocking queries
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks
    ON blocked_locks.locktype = blocking_locks.locktype
    AND blocked_locks.relation = blocking_locks.relation
    AND blocked_locks.pid != blocking_locks.pid
    AND NOT blocked_locks.granted
    AND blocking_locks.granted
JOIN pg_stat_activity blocking ON blocking_locks.pid = blocking.pid;
```

## Case Studies

### Case Study 1: Dashboard Query Optimization

```sql
-- Original query (15 seconds)
SELECT
    d.date,
    COUNT(DISTINCT o.customer_id) as customers,
    SUM(o.total) as revenue,
    COUNT(o.id) as order_count
FROM dates d
LEFT JOIN orders o ON d.date = DATE(o.created_at)
WHERE d.date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY d.date
ORDER BY d.date;

-- Problem identified: DATE() function on indexed column
-- Plus join on computed value

-- Solution 1: Expression index
CREATE INDEX idx_orders_date ON orders(DATE(created_at));

-- Solution 2: Materialized column
ALTER TABLE orders ADD COLUMN created_date DATE
    GENERATED ALWAYS AS (DATE(created_at)) STORED;
CREATE INDEX idx_orders_created_date ON orders(created_date);

-- Solution 3: Pre-aggregated table for dashboards
CREATE TABLE daily_stats AS
SELECT
    DATE(created_at) as date,
    COUNT(DISTINCT customer_id) as customers,
    SUM(total) as revenue,
    COUNT(*) as order_count
FROM orders
GROUP BY DATE(created_at);

-- Refresh daily with incremental update
-- Query now runs in < 100ms
```

### Case Study 2: Search Query with Multiple Filters

```sql
-- Original query (variable performance, sometimes 30+ seconds)
SELECT *
FROM products
WHERE
    ($1 IS NULL OR category = $1)
    AND ($2 IS NULL OR brand = $2)
    AND ($3 IS NULL OR price BETWEEN $3 AND $4)
    AND ($5 IS NULL OR name ILIKE '%' || $5 || '%')
ORDER BY created_at DESC
LIMIT 20;

-- Problem: Planner can't optimize for optional conditions
-- Gets different plans based on which params are NULL

-- Solution: Dynamic SQL with only active conditions
-- In application:
sql = "SELECT * FROM products WHERE 1=1"
params = []
if category:
    sql += " AND category = $" + str(len(params)+1)
    params.append(category)
if brand:
    sql += " AND brand = $" + str(len(params)+1)
    params.append(brand)
# ... etc

-- Or use partial indexes for common patterns
CREATE INDEX idx_products_active_electronics
ON products(created_at DESC)
WHERE category = 'Electronics' AND status = 'active';
```

### Case Study 3: Report with Complex Aggregations

```sql
-- Original query (45 seconds)
WITH monthly_sales AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', created_at) as month,
        SUM(total) as monthly_total
    FROM orders
    WHERE created_at >= '2023-01-01'
    GROUP BY customer_id, DATE_TRUNC('month', created_at)
),
customer_stats AS (
    SELECT
        customer_id,
        AVG(monthly_total) as avg_monthly,
        MAX(monthly_total) as max_monthly,
        COUNT(*) as active_months
    FROM monthly_sales
    GROUP BY customer_id
)
SELECT
    c.name,
    cs.avg_monthly,
    cs.max_monthly,
    cs.active_months
FROM customers c
JOIN customer_stats cs ON c.id = cs.customer_id
WHERE cs.avg_monthly > 1000
ORDER BY cs.avg_monthly DESC;

-- Analysis:
-- 1. CTEs are materialized (lots of data)
-- 2. DATE_TRUNC on every row
-- 3. Multiple passes over orders table

-- Solution:
-- 1. Index for date range
CREATE INDEX idx_orders_created_customer
ON orders(created_at, customer_id);

-- 2. Single-pass aggregation
SELECT
    c.name,
    AVG(monthly_total) as avg_monthly,
    MAX(monthly_total) as max_monthly,
    COUNT(*) as active_months
FROM customers c
JOIN (
    SELECT
        customer_id,
        DATE_TRUNC('month', created_at) as month,
        SUM(total) as monthly_total
    FROM orders
    WHERE created_at >= '2023-01-01'
    GROUP BY customer_id, DATE_TRUNC('month', created_at)
) ms ON c.id = ms.customer_id
GROUP BY c.id, c.name
HAVING AVG(monthly_total) > 1000
ORDER BY AVG(monthly_total) DESC;

-- Result: 3 seconds (15x faster)
```

### Case Study 4: Inventory Check with Locks

```sql
-- Original approach (causes deadlocks)
BEGIN;
SELECT quantity FROM inventory WHERE product_id = 123 FOR UPDATE;
-- Application checks if quantity >= requested
UPDATE inventory SET quantity = quantity - 5 WHERE product_id = 123;
COMMIT;

-- Problem: Long lock hold time, deadlocks with concurrent requests

-- Solution: Single atomic operation
UPDATE inventory
SET quantity = quantity - 5
WHERE product_id = 123
  AND quantity >= 5
RETURNING quantity;

-- If returns row, success
-- If no row returned, insufficient inventory
-- No explicit locks, no deadlocks
```

## Production Checklist

### Before Deployment

```sql
-- 1. Run EXPLAIN ANALYZE on new queries
-- 2. Check for Seq Scans on large tables
-- 3. Verify indexes exist for WHERE/JOIN columns
-- 4. Test with production-like data volume
-- 5. Check for estimate mismatches
```

### Monitoring Setup

```sql
-- Enable essential extensions
CREATE EXTENSION pg_stat_statements;

-- Configure logging
-- log_min_duration_statement = '100ms'
-- auto_explain.log_min_duration = '1s'

-- Set up regular statistics collection
-- Schedule: ANALYZE every hour
-- Schedule: VACUUM ANALYZE nightly
```

### Emergency Response

```sql
-- Kill long-running query
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE duration > interval '5 minutes'
  AND state = 'active';

-- Quick win: Increase work_mem for session
SET work_mem = '512MB';

-- Disable problematic plan choices temporarily
SET enable_seqscan = off;  -- Force index usage
SET enable_nestloop = off; -- Avoid nested loops
```

## Summary

In this chapter, you've learned:

- **Anti-Patterns**: Common mistakes and their solutions
- **Debugging**: Systematic approach to finding issues
- **Case Studies**: Real-world optimization examples
- **Production**: Checklists and emergency procedures

## Key Takeaways

1. **Avoid SELECT ***: Always specify needed columns
2. **Watch for Function Wrapping**: Use expression indexes or normalized columns
3. **Keyset > OFFSET**: For pagination at scale
4. **Test with Real Data**: Query plans change with data volume
5. **Monitor Continuously**: Catch regressions early

## Tutorial Complete

Congratulations! You've completed the PostgreSQL Query Planner tutorial. You now have the knowledge to:

- Read and understand EXPLAIN output
- Identify and fix common performance issues
- Design effective indexing strategies
- Tune PostgreSQL for your workload
- Debug production query problems

## Further Resources

- [PostgreSQL Documentation: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL Documentation: Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [pgMustard](https://www.pgmustard.com/) - EXPLAIN visualization tool
- [Dalibo explain.depesz.com](https://explain.depesz.com/) - Plan analysis

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `WHERE`, `orders` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Real-World Patterns` as an operating subsystem inside **PostgreSQL Query Planner Deep Dive**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `customer_id`, `created_at`, `Solution` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Real-World Patterns` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `WHERE` receives stable contracts.
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
- search upstream code for `SELECT` and `WHERE` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Performance Tuning](07-performance-tuning.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
