---
layout: default
title: "Chapter 1: Query Planning Fundamentals"
parent: "PostgreSQL Query Planner"
nav_order: 1
---

# Chapter 1: Query Planning Fundamentals

Welcome to **Chapter 1: Query Planning Fundamentals**. In this part of **PostgreSQL Query Planner Deep Dive**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understand how PostgreSQL transforms SQL into execution plans and learn to read EXPLAIN output effectively.

## Overview

Every SQL query goes through a sophisticated pipeline before returning results. This chapter introduces PostgreSQL's query processing architecture and teaches you to read and understand execution plans.

## Query Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     Query Processing Stages                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PARSER                                                      │
│     ├── Lexical Analysis (tokenization)                         │
│     ├── Syntax Analysis (grammar checking)                      │
│     └── Output: Parse Tree                                      │
│                                                                 │
│  2. ANALYZER                                                    │
│     ├── Semantic Analysis                                       │
│     ├── Name Resolution (tables, columns)                       │
│     └── Output: Query Tree                                      │
│                                                                 │
│  3. REWRITER                                                    │
│     ├── Rule Application                                        │
│     ├── View Expansion                                          │
│     └── Output: Rewritten Query Tree                            │
│                                                                 │
│  4. PLANNER/OPTIMIZER                                           │
│     ├── Generate Possible Plans                                 │
│     ├── Estimate Costs                                          │
│     ├── Choose Cheapest Plan                                    │
│     └── Output: Execution Plan                                  │
│                                                                 │
│  5. EXECUTOR                                                    │
│     ├── Execute Plan Nodes                                      │
│     ├── Fetch/Process Data                                      │
│     └── Output: Query Results                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Understanding EXPLAIN

### Basic EXPLAIN

```sql
-- Basic execution plan
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
```

Output:
```
                        QUERY PLAN
-----------------------------------------------------------
 Seq Scan on users  (cost=0.00..25.00 rows=1 width=100)
   Filter: (email = 'john@example.com'::text)
```

### Reading Plan Output

```sql
-- Breaking down the components:
--
-- Seq Scan on users     <- Operation type and target table
-- cost=0.00..25.00      <- Startup cost..Total cost
-- rows=1                <- Estimated rows returned
-- width=100             <- Estimated average row width in bytes
-- Filter: ...           <- Conditions applied during scan
```

### EXPLAIN ANALYZE

```sql
-- Execute the query and show actual timing
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';
```

Output:
```
                                              QUERY PLAN
------------------------------------------------------------------------------------------------------
 Seq Scan on users  (cost=0.00..25.00 rows=1 width=100) (actual time=0.015..0.234 rows=1 loops=1)
   Filter: (email = 'john@example.com'::text)
   Rows Removed by Filter: 999
 Planning Time: 0.085 ms
 Execution Time: 0.256 ms
```

### EXPLAIN Options

```sql
-- Comprehensive analysis
EXPLAIN (
    ANALYZE,          -- Execute and show actual times
    BUFFERS,          -- Show buffer usage
    COSTS,            -- Show cost estimates (default)
    TIMING,           -- Show actual timing (default with ANALYZE)
    VERBOSE,          -- Show additional details
    FORMAT TEXT       -- Output format (TEXT, XML, JSON, YAML)
)
SELECT * FROM orders WHERE total > 100;
```

## Plan Node Types

### Scan Nodes

```sql
-- Sequential Scan: reads entire table
EXPLAIN SELECT * FROM small_table;
-- Result: Seq Scan on small_table

-- Index Scan: uses index to find rows
EXPLAIN SELECT * FROM users WHERE id = 42;
-- Result: Index Scan using users_pkey on users

-- Index Only Scan: satisfies query from index alone
EXPLAIN SELECT id FROM users WHERE id = 42;
-- Result: Index Only Scan using users_pkey on users

-- Bitmap Index Scan + Bitmap Heap Scan: for multiple index conditions
EXPLAIN SELECT * FROM users WHERE age > 30 AND city = 'NYC';
-- Result: Bitmap Heap Scan + Bitmap Index Scans
```

### Join Nodes

```sql
-- Nested Loop: for small datasets or indexed lookups
EXPLAIN SELECT * FROM orders o JOIN customers c ON o.customer_id = c.id
WHERE c.id = 42;

-- Hash Join: builds hash table, probes with other table
EXPLAIN SELECT * FROM orders o JOIN customers c ON o.customer_id = c.id;

-- Merge Join: for sorted inputs
EXPLAIN SELECT * FROM orders o JOIN customers c ON o.customer_id = c.id
ORDER BY c.id;
```

### Aggregate Nodes

```sql
-- Aggregate: computes aggregate functions
EXPLAIN SELECT COUNT(*), SUM(total) FROM orders;

-- HashAggregate: uses hash table for grouping
EXPLAIN SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id;

-- GroupAggregate: groups pre-sorted input
EXPLAIN SELECT customer_id, COUNT(*) FROM orders
GROUP BY customer_id ORDER BY customer_id;
```

## Understanding Costs

### Cost Components

```sql
-- Cost formula components:
-- seq_page_cost = 1.0       -- cost of sequential page read
-- random_page_cost = 4.0    -- cost of random page read
-- cpu_tuple_cost = 0.01     -- cost to process each row
-- cpu_index_tuple_cost = 0.005
-- cpu_operator_cost = 0.0025

-- Example cost calculation for sequential scan:
-- Total cost = (pages * seq_page_cost) + (rows * cpu_tuple_cost)
```

### Startup vs Total Cost

```sql
-- cost=startup..total
--
-- Startup cost: Cost before first row can be returned
--   - Building hash tables
--   - Sorting data
--   - Index positioning
--
-- Total cost: Cost to return all rows

EXPLAIN SELECT * FROM users ORDER BY name;
-- Sort  (cost=150.00..155.00 rows=1000 width=100)
--       startup=150 (must sort before returning first row)
--       total=155 (5 additional to return all rows)
```

## Practical Examples

### Simple Query Analysis

```sql
-- Create sample table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INT
);

-- Insert sample data
INSERT INTO products (name, category, price, stock)
SELECT
    'Product ' || i,
    CASE i % 5
        WHEN 0 THEN 'Electronics'
        WHEN 1 THEN 'Clothing'
        WHEN 2 THEN 'Books'
        WHEN 3 THEN 'Home'
        ELSE 'Sports'
    END,
    (random() * 1000)::decimal(10,2),
    (random() * 100)::int
FROM generate_series(1, 10000) i;

-- Analyze the table
ANALYZE products;

-- Examine different queries
EXPLAIN ANALYZE SELECT * FROM products WHERE id = 500;
-- Index Scan (using primary key)

EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics';
-- Seq Scan (no index on category)

-- Add index and compare
CREATE INDEX idx_products_category ON products(category);
EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'Electronics';
-- Now uses Index Scan or Bitmap Scan
```

### Join Query Analysis

```sql
-- Create related tables
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

INSERT INTO categories (name)
VALUES ('Electronics'), ('Clothing'), ('Books'), ('Home'), ('Sports');

-- Analyze join query
EXPLAIN ANALYZE
SELECT p.name, c.name as category_name, p.price
FROM products p
JOIN categories c ON p.category = c.name
WHERE p.price > 500;
```

### Subquery Analysis

```sql
-- Subquery in WHERE
EXPLAIN ANALYZE
SELECT * FROM products
WHERE category IN (
    SELECT name FROM categories WHERE id IN (1, 2)
);

-- Correlated subquery
EXPLAIN ANALYZE
SELECT p.*,
       (SELECT COUNT(*) FROM products p2 WHERE p2.category = p.category) as category_count
FROM products p
WHERE p.price > 500;
```

## Reading Complex Plans

### Plan Tree Structure

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, COUNT(o.id), SUM(o.total)
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.created_at > '2024-01-01'
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 5
ORDER BY SUM(o.total) DESC
LIMIT 10;
```

Understanding the output:
```
Limit  (actual rows=10)                           -- Final limit
  ->  Sort  (actual rows=10)                      -- Sort for ORDER BY
        Sort Key: (sum(o.total)) DESC
        ->  HashAggregate  (actual rows=100)      -- GROUP BY using hash
              Filter: (count(o.id) > 5)           -- HAVING clause
              ->  Hash Left Join                   -- JOIN operation
                    Hash Cond: (c.id = o.customer_id)
                    ->  Seq Scan on customers c   -- Scan customers
                          Filter: (created_at > '2024-01-01')
                    ->  Hash                       -- Build hash table
                          ->  Seq Scan on orders o -- Scan orders
```

### Execution Order

```
Execution proceeds BOTTOM-UP and INSIDE-OUT:

1. Seq Scan on orders (build input for hash)
2. Hash (create hash table from orders)
3. Seq Scan on customers (with filter)
4. Hash Left Join (join using hash table)
5. HashAggregate (group and filter with HAVING)
6. Sort (order by sum)
7. Limit (return top 10)
```

## Common Plan Issues

### Missing Index

```sql
-- Symptom: Seq Scan on large table with selective filter
EXPLAIN ANALYZE SELECT * FROM products WHERE name = 'Product 500';
-- Seq Scan with high actual time

-- Solution: Add appropriate index
CREATE INDEX idx_products_name ON products(name);
```

### Wrong Join Order

```sql
-- Symptom: Hash Join building huge hash table
-- The planner might choose suboptimal join order

-- Solution: Check statistics, consider join_collapse_limit
SET join_collapse_limit = 1;  -- Forces explicit join order
```

### Estimate Mismatch

```sql
-- Symptom: rows=1000 but actual rows=100000
-- Planner chose wrong strategy based on bad estimates

-- Solution: Update statistics
ANALYZE table_name;
-- Or adjust statistics target
ALTER TABLE products ALTER COLUMN category SET STATISTICS 1000;
ANALYZE products;
```

## Summary

In this chapter, you've learned:

- **Query Pipeline**: Parser, Analyzer, Rewriter, Planner, Executor
- **EXPLAIN Basics**: Reading cost estimates and actual execution data
- **Plan Nodes**: Scan, Join, and Aggregate operations
- **Cost Model**: Understanding startup and total costs
- **Practical Analysis**: Reading and interpreting complex plans

## Key Takeaways

1. **Always Use ANALYZE**: Estimates without execution can be misleading
2. **Read Bottom-Up**: Plans execute from leaf nodes upward
3. **Compare Estimates vs Actuals**: Large mismatches indicate problems
4. **Consider BUFFERS**: I/O is often the real bottleneck
5. **Understand Costs**: They're relative, not absolute time

## Next Steps

Now that you understand the basics, let's dive into how PostgreSQL collects and uses statistics in Chapter 2.

---

**Ready for Chapter 2?** [Statistics and Cost Estimation](02-statistics.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `SELECT`, `Scan`, `EXPLAIN` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Query Planning Fundamentals` as an operating subsystem inside **PostgreSQL Query Planner Deep Dive**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `WHERE`, `cost`, `rows` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Query Planning Fundamentals` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `SELECT`.
2. **Input normalization**: shape incoming data so `Scan` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `EXPLAIN`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `SELECT` and `Scan` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Statistics and Cost Estimation](02-statistics.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
