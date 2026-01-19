---
layout: default
title: "Chapter 2: Statistics and Cost Estimation"
parent: "PostgreSQL Query Planner"
nav_order: 2
---

# Chapter 2: Statistics and Cost Estimation

> Deep dive into PostgreSQL statistics, how the planner estimates costs, and the impact of accurate statistics on query performance.

## Overview

The query planner's effectiveness depends entirely on accurate statistics about your data. This chapter explores how PostgreSQL collects, stores, and uses statistics to make planning decisions.

## Statistics Collection

### ANALYZE Command

```sql
-- Analyze a single table
ANALYZE users;

-- Analyze specific columns
ANALYZE users (email, created_at);

-- Analyze entire database
ANALYZE;

-- Verbose output
ANALYZE VERBOSE users;
```

### Autovacuum and Statistics

```sql
-- Check autovacuum settings
SHOW autovacuum;
SHOW autovacuum_analyze_threshold;
SHOW autovacuum_analyze_scale_factor;

-- Default: Analyze when changed_rows > threshold + scale_factor * table_rows
-- With defaults: 50 + 0.1 * table_rows

-- Adjust for specific table
ALTER TABLE high_churn_table
SET (autovacuum_analyze_threshold = 100,
     autovacuum_analyze_scale_factor = 0.02);
```

## Understanding pg_stats

### Core Statistics

```sql
-- View statistics for a table
SELECT
    attname,
    n_distinct,
    most_common_vals,
    most_common_freqs,
    histogram_bounds,
    correlation
FROM pg_stats
WHERE tablename = 'orders';
```

### Column Statistics Breakdown

```sql
-- n_distinct: Number of distinct values
-- > 0: Actual count
-- < 0: Negative fraction of rows (e.g., -0.5 means 50% unique)

SELECT attname, n_distinct,
    CASE
        WHEN n_distinct > 0 THEN n_distinct::text
        ELSE 'Fraction: ' || abs(n_distinct)::text
    END as interpretation
FROM pg_stats
WHERE tablename = 'users';
```

### Most Common Values (MCV)

```sql
-- Most common values and their frequencies
SELECT
    attname,
    most_common_vals,
    most_common_freqs
FROM pg_stats
WHERE tablename = 'orders'
  AND attname = 'status';

-- Example output:
-- status | {pending,shipped,delivered} | {0.45,0.35,0.20}
-- Interpretation: 45% pending, 35% shipped, 20% delivered
```

### Histogram Bounds

```sql
-- For columns without MCVs or remaining values
SELECT
    attname,
    histogram_bounds
FROM pg_stats
WHERE tablename = 'orders'
  AND attname = 'total';

-- Example: {0.00,25.50,75.20,150.00,500.00,1000.00}
-- Divides non-MCV values into roughly equal-sized buckets
```

### Correlation

```sql
-- Physical vs logical order correlation
-- 1.0 = perfectly correlated (good for range scans)
-- 0.0 = random (index scan may cause random I/O)

SELECT attname, correlation
FROM pg_stats
WHERE tablename = 'orders';

-- High correlation on 'created_at' suggests time-ordered inserts
```

## Statistics Target

### Adjusting Statistics Precision

```sql
-- Default statistics target
SHOW default_statistics_target;  -- Default: 100

-- Increase for important columns
ALTER TABLE orders
ALTER COLUMN customer_id SET STATISTICS 500;

-- Must re-analyze to take effect
ANALYZE orders (customer_id);

-- View current setting
SELECT attname, attstattarget
FROM pg_attribute
WHERE attrelid = 'orders'::regclass
  AND attname = 'customer_id';
```

### When to Increase Statistics

```sql
-- Highly skewed data distributions
-- Frequently filtered columns
-- Join columns

-- Example: Column with many distinct values used in filtering
ALTER TABLE products ALTER COLUMN sku SET STATISTICS 1000;
ANALYZE products (sku);
```

## Extended Statistics

### Multi-Column Statistics

```sql
-- For correlated columns that are filtered together
CREATE STATISTICS orders_customer_status
ON customer_id, status
FROM orders;

ANALYZE orders;

-- View extended statistics
SELECT * FROM pg_statistic_ext;

-- Example use case: city and zip code are correlated
CREATE STATISTICS location_stats (dependencies)
ON city, zip_code
FROM addresses;
```

### Types of Extended Statistics

```sql
-- Functional dependencies
CREATE STATISTICS deps_stats (dependencies)
ON col_a, col_b FROM my_table;

-- N-distinct for combinations
CREATE STATISTICS ndist_stats (ndistinct)
ON col_a, col_b FROM my_table;

-- MCV lists for combinations
CREATE STATISTICS mcv_stats (mcv)
ON col_a, col_b FROM my_table;

-- All types
CREATE STATISTICS full_stats (dependencies, ndistinct, mcv)
ON col_a, col_b, col_c FROM my_table;
```

## Cost Estimation

### Cost Model Parameters

```sql
-- Examine current settings
SELECT name, setting, unit, short_desc
FROM pg_settings
WHERE name LIKE '%cost%' OR name LIKE '%page%';

-- Key parameters:
-- seq_page_cost = 1.0           Base cost for sequential page read
-- random_page_cost = 4.0        Base cost for random page read
-- cpu_tuple_cost = 0.01         Cost to process each row
-- cpu_index_tuple_cost = 0.005  Cost to process index entry
-- cpu_operator_cost = 0.0025    Cost for operator evaluation
-- effective_cache_size = 4GB    Planner's assumption of disk cache
```

### Sequential Scan Cost

```sql
-- Cost formula:
-- cost = (pages * seq_page_cost) + (rows * cpu_tuple_cost)

-- Example: Table with 100 pages, 10000 rows
-- cost = (100 * 1.0) + (10000 * 0.01) = 100 + 100 = 200

-- Check actual values
SELECT
    relname,
    relpages,
    reltuples,
    (relpages * current_setting('seq_page_cost')::float +
     reltuples * current_setting('cpu_tuple_cost')::float) as estimated_cost
FROM pg_class
WHERE relname = 'orders';
```

### Index Scan Cost

```sql
-- More complex formula including:
-- - Index page reads (some sequential, some random)
-- - Heap page reads (random)
-- - CPU costs for index and tuple processing

-- Factors affecting index scan cost:
-- 1. Index selectivity (how many rows match)
-- 2. Correlation (affects random I/O)
-- 3. effective_cache_size (affects random_page_cost effective value)
```

### Selectivity Estimation

```sql
-- Equality on MCV value
-- selectivity = frequency from most_common_freqs

-- Equality on non-MCV value
-- selectivity = (1 - sum(mcv_freqs)) / num_distinct_non_mcv

-- Range queries use histogram buckets
-- WHERE price > 100 AND price < 500
-- selectivity = fraction of histogram range covered
```

## Practical Selectivity Examples

### Equality Selectivity

```sql
-- Setup
CREATE TABLE demo (
    id SERIAL,
    status TEXT,
    amount DECIMAL
);

INSERT INTO demo (status, amount)
SELECT
    CASE (random() * 100)::int
        WHEN 0 THEN 'rare'      -- 1%
        ELSE 'common'           -- 99%
    END,
    random() * 1000
FROM generate_series(1, 100000);

ANALYZE demo;

-- Check selectivity estimates
EXPLAIN SELECT * FROM demo WHERE status = 'rare';
-- rows=~1000 (1% of 100000)

EXPLAIN SELECT * FROM demo WHERE status = 'common';
-- rows=~99000 (99% of 100000)
```

### Range Selectivity

```sql
-- View histogram for amount column
SELECT histogram_bounds
FROM pg_stats
WHERE tablename = 'demo' AND attname = 'amount';

-- Range query selectivity
EXPLAIN SELECT * FROM demo WHERE amount > 500;
-- Approximately 50% of rows (50000)

EXPLAIN SELECT * FROM demo WHERE amount BETWEEN 200 AND 400;
-- Approximately 20% of rows (20000)
```

## Diagnosing Statistics Issues

### Estimate vs Actual Mismatches

```sql
-- Large mismatches indicate statistics problems
EXPLAIN ANALYZE
SELECT * FROM orders WHERE status = 'archived';

-- If rows=100 but actual rows=50000, statistics are stale
```

### Finding Stale Statistics

```sql
-- Check last analyze time
SELECT
    schemaname,
    relname,
    last_analyze,
    last_autoanalyze,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
WHERE n_live_tup > 10000
ORDER BY last_analyze NULLS FIRST;
```

### Correlation Issues

```sql
-- Poor correlation can cause bad index scan estimates
SELECT
    tablename,
    attname,
    correlation
FROM pg_stats
WHERE abs(correlation) < 0.5
  AND n_distinct > 100;

-- For tables with poor correlation, sequential scans
-- might be preferred even with indexes
```

## Tuning for Specific Scenarios

### SSD Storage

```sql
-- SSDs have lower random I/O penalty
-- Adjust random_page_cost closer to seq_page_cost

SET random_page_cost = 1.1;  -- Default is 4.0

-- Or set globally
ALTER SYSTEM SET random_page_cost = 1.1;
SELECT pg_reload_conf();
```

### Large Memory Systems

```sql
-- Increase effective_cache_size
-- Should be ~75% of available memory

SET effective_cache_size = '12GB';

-- This affects cost estimates for index scans
-- Higher values make index scans more attractive
```

### Specific Table Tuning

```sql
-- For tables that change rapidly
ALTER TABLE events
SET (autovacuum_analyze_threshold = 50,
     autovacuum_analyze_scale_factor = 0.01);

-- For append-only tables
ALTER TABLE audit_log
SET (autovacuum_analyze_scale_factor = 0.001);
```

## Summary

In this chapter, you've learned:

- **Statistics Collection**: ANALYZE command and autovacuum
- **pg_stats**: Understanding MCVs, histograms, and correlation
- **Statistics Target**: Tuning precision for specific columns
- **Extended Statistics**: Multi-column statistics for correlated data
- **Cost Estimation**: How PostgreSQL calculates query costs
- **Selectivity**: How the planner estimates row counts

## Key Takeaways

1. **Fresh Statistics**: Keep statistics updated, especially after bulk operations
2. **Increase Targets**: Use higher statistics for skewed or frequently-filtered columns
3. **Extended Statistics**: Create for correlated column combinations
4. **Tune Cost Parameters**: Adjust for your storage (SSD vs HDD) and memory
5. **Monitor Estimates**: Large estimate mismatches indicate statistics problems

## Next Steps

With a solid understanding of statistics, let's explore how PostgreSQL executes different scan operations in Chapter 3.

---

**Ready for Chapter 3?** [Scan Operations](03-scan-operations.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
