---
layout: default
title: "Chapter 6: Performance"
parent: "LanceDB Tutorial"
nav_order: 6
---

# Chapter 6: Performance

Welcome to **Chapter 6: Performance**. In this part of **LanceDB Tutorial: Serverless Vector Database for AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Optimize LanceDB for speed, memory efficiency, and throughput with indexing strategies and query tuning.

## Overview

Performance optimization is crucial for production deployments. This chapter covers indexing strategies, query optimization, memory management, and benchmarking techniques for LanceDB.

## Index Optimization

### Choosing Index Parameters

```python
import lancedb
import numpy as np

db = lancedb.connect("./perf_lancedb")

# Create table with 1M vectors
data = [
    {"id": i, "vector": np.random.rand(384).tolist()}
    for i in range(1_000_000)
]
table = db.create_table("large_table", data)

# Index for balanced performance
table.create_index(
    metric="cosine",
    num_partitions=256,      # sqrt(n) is a good starting point
    num_sub_vectors=96,      # dimension / 4 is reasonable
)

# Index for high recall (accuracy)
table.create_index(
    metric="cosine",
    num_partitions=512,      # More partitions
    num_sub_vectors=128,     # More sub-vectors
    replace=True
)

# Index for high throughput (speed)
table.create_index(
    metric="cosine",
    num_partitions=128,      # Fewer partitions
    num_sub_vectors=48,      # Fewer sub-vectors
    replace=True
)
```

### Index Selection Guidelines

```python
def recommend_index_params(num_vectors: int, dimension: int, priority: str) -> dict:
    """Recommend index parameters based on dataset and priority."""

    # Base calculations
    sqrt_n = int(np.sqrt(num_vectors))

    if priority == "accuracy":
        return {
            "num_partitions": min(sqrt_n * 2, 4096),
            "num_sub_vectors": min(dimension // 2, 256),
            "nprobes_recommendation": sqrt_n // 2
        }
    elif priority == "speed":
        return {
            "num_partitions": max(sqrt_n // 2, 64),
            "num_sub_vectors": max(dimension // 8, 16),
            "nprobes_recommendation": 10
        }
    else:  # balanced
        return {
            "num_partitions": sqrt_n,
            "num_sub_vectors": dimension // 4,
            "nprobes_recommendation": sqrt_n // 4
        }

# Usage
params = recommend_index_params(
    num_vectors=1_000_000,
    dimension=384,
    priority="balanced"
)
print(params)
```

### Index Types Comparison

```python
import time

def benchmark_index_type(table, query_vectors, index_config):
    """Benchmark an index configuration."""

    # Create index
    start = time.time()
    table.create_index(**index_config, replace=True)
    index_time = time.time() - start

    # Benchmark queries
    latencies = []
    for query in query_vectors[:100]:
        start = time.time()
        table.search(query).limit(10).to_list()
        latencies.append(time.time() - start)

    return {
        "index_time": index_time,
        "avg_latency": np.mean(latencies),
        "p99_latency": np.percentile(latencies, 99)
    }

# Compare configurations
configs = [
    {"metric": "cosine", "num_partitions": 128, "num_sub_vectors": 48},
    {"metric": "cosine", "num_partitions": 256, "num_sub_vectors": 96},
    {"metric": "cosine", "num_partitions": 512, "num_sub_vectors": 128},
]

for config in configs:
    results = benchmark_index_type(table, query_vectors, config)
    print(f"Config: {config}")
    print(f"  Index time: {results['index_time']:.2f}s")
    print(f"  Avg latency: {results['avg_latency']*1000:.2f}ms")
    print(f"  P99 latency: {results['p99_latency']*1000:.2f}ms")
```

## Query Optimization

### nprobes Tuning

```python
# nprobes controls accuracy vs speed tradeoff
# More probes = higher accuracy, slower search

# Fast search (lower accuracy)
results = table.search(query) \
    .nprobes(5) \
    .limit(10) \
    .to_list()

# Balanced
results = table.search(query) \
    .nprobes(20) \
    .limit(10) \
    .to_list()

# High accuracy (slower)
results = table.search(query) \
    .nprobes(100) \
    .limit(10) \
    .to_list()

# Benchmark different nprobes values
def find_optimal_nprobes(table, query, ground_truth, target_recall=0.95):
    """Find minimum nprobes for target recall."""

    for nprobes in [5, 10, 20, 50, 100, 200]:
        results = table.search(query).nprobes(nprobes).limit(10).to_list()
        result_ids = set(r['id'] for r in results)
        recall = len(result_ids & ground_truth) / len(ground_truth)

        if recall >= target_recall:
            return nprobes

    return 200  # Maximum
```

### Refine Factor

```python
# refine_factor fetches more candidates and reranks
# Improves accuracy at cost of latency

# No refinement (fastest)
results = table.search(query).limit(10).to_list()

# With refinement (more accurate)
results = table.search(query) \
    .refine_factor(5) \  # Fetch 5x candidates
    .limit(10) \
    .to_list()

# Higher refinement (most accurate)
results = table.search(query) \
    .refine_factor(20) \
    .limit(10) \
    .to_list()
```

### Column Selection

```python
import time

# Slow: Fetching all columns including vectors
start = time.time()
results = table.search(query).limit(100).to_pandas()
print(f"All columns: {time.time() - start:.3f}s")

# Fast: Selecting only needed columns
start = time.time()
results = table.search(query) \
    .select(["id", "title"]) \
    .limit(100) \
    .to_pandas()
print(f"Selected columns: {time.time() - start:.3f}s")

# Avoid fetching vector column unless needed
```

### Filter Optimization

```python
# Pre-filter (applied before vector search) - use for selective filters
results = table.search(query) \
    .where("category = 'technology'") \  # Filters out 90% of data
    .limit(10) \
    .to_list()

# Post-filter (applied after vector search) - use for less selective filters
results = table.search(query) \
    .where("is_active = true", prefilter=False) \  # Most rows match
    .limit(10) \
    .to_list()

# Indexed filters (faster)
# Create scalar index for frequently filtered columns
table.create_scalar_index("category")

results = table.search(query) \
    .where("category = 'technology'") \
    .limit(10) \
    .to_list()
```

## Memory Management

### Memory-Mapped Access

```python
import lancedb

# LanceDB uses memory-mapped files by default
# This allows working with datasets larger than RAM

db = lancedb.connect("./large_dataset")
table = db.open_table("big_table")

# Only accessed data is loaded into memory
results = table.search(query).limit(10).to_list()
```

### Batch Processing

```python
def process_large_dataset(table, queries, batch_size=100):
    """Process queries in batches to manage memory."""

    all_results = []

    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]

        batch_results = []
        for query in batch:
            results = table.search(query).limit(10).to_list()
            batch_results.append(results)

        all_results.extend(batch_results)

        # Optional: Force garbage collection
        import gc
        gc.collect()

    return all_results
```

### Streaming Results

```python
# For very large result sets, use iteration
def stream_results(table, query, total_limit=10000, batch_size=1000):
    """Stream results in batches."""

    offset = 0
    while offset < total_limit:
        results = table.search(query) \
            .limit(batch_size) \
            .offset(offset) \
            .to_list()

        if not results:
            break

        for result in results:
            yield result

        offset += batch_size

# Usage
for result in stream_results(table, query):
    process_result(result)
```

## Concurrent Access

### Thread Safety

```python
import lancedb
from concurrent.futures import ThreadPoolExecutor
import threading

# LanceDB connections are thread-safe
db = lancedb.connect("./concurrent_lancedb")

def search_worker(query, table_name="my_table"):
    """Worker function for concurrent search."""
    table = db.open_table(table_name)
    return table.search(query).limit(10).to_list()

# Concurrent searches
with ThreadPoolExecutor(max_workers=8) as executor:
    queries = [np.random.rand(384).tolist() for _ in range(100)]
    futures = [executor.submit(search_worker, q) for q in queries]
    results = [f.result() for f in futures]
```

### Connection Pooling

```python
class LanceDBPool:
    """Simple connection pool for LanceDB."""

    def __init__(self, uri: str, pool_size: int = 5):
        self.uri = uri
        self.pool_size = pool_size
        self._connections = []
        self._lock = threading.Lock()

        # Pre-create connections
        for _ in range(pool_size):
            self._connections.append(lancedb.connect(uri))

    def get_connection(self):
        """Get a connection from the pool."""
        with self._lock:
            if self._connections:
                return self._connections.pop()
        # Create new if pool exhausted
        return lancedb.connect(self.uri)

    def return_connection(self, conn):
        """Return connection to pool."""
        with self._lock:
            if len(self._connections) < self.pool_size:
                self._connections.append(conn)

# Usage
pool = LanceDBPool("./my_lancedb", pool_size=10)

def search_with_pool(query):
    conn = pool.get_connection()
    try:
        table = conn.open_table("my_table")
        return table.search(query).limit(10).to_list()
    finally:
        pool.return_connection(conn)
```

## Benchmarking

### Basic Benchmark

```python
import time
import numpy as np
from statistics import mean, stdev

def benchmark_search(table, num_queries=100, limit=10):
    """Benchmark search performance."""

    # Generate random queries
    queries = [np.random.rand(384).tolist() for _ in range(num_queries)]

    # Warm up
    for query in queries[:10]:
        table.search(query).limit(limit).to_list()

    # Benchmark
    latencies = []
    for query in queries:
        start = time.perf_counter()
        table.search(query).limit(limit).to_list()
        latencies.append(time.perf_counter() - start)

    return {
        "num_queries": num_queries,
        "avg_latency_ms": mean(latencies) * 1000,
        "std_latency_ms": stdev(latencies) * 1000,
        "p50_latency_ms": np.percentile(latencies, 50) * 1000,
        "p95_latency_ms": np.percentile(latencies, 95) * 1000,
        "p99_latency_ms": np.percentile(latencies, 99) * 1000,
        "qps": num_queries / sum(latencies)
    }

results = benchmark_search(table)
print(f"Average latency: {results['avg_latency_ms']:.2f}ms")
print(f"P99 latency: {results['p99_latency_ms']:.2f}ms")
print(f"QPS: {results['qps']:.1f}")
```

### Recall Benchmark

```python
def benchmark_recall(table, queries, ground_truth, k=10):
    """Benchmark search recall against ground truth."""

    recalls = []
    for query, truth in zip(queries, ground_truth):
        results = table.search(query).limit(k).to_list()
        result_ids = set(r['id'] for r in results)
        truth_ids = set(truth[:k])

        recall = len(result_ids & truth_ids) / len(truth_ids)
        recalls.append(recall)

    return {
        "avg_recall": mean(recalls),
        "min_recall": min(recalls),
        "max_recall": max(recalls)
    }
```

### Throughput Benchmark

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def benchmark_throughput(table, num_queries=1000, num_workers=8):
    """Benchmark concurrent throughput."""

    queries = [np.random.rand(384).tolist() for _ in range(num_queries)]

    def search_one(query):
        return table.search(query).limit(10).to_list()

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        list(executor.map(search_one, queries))

    duration = time.perf_counter() - start

    return {
        "total_queries": num_queries,
        "duration_s": duration,
        "qps": num_queries / duration,
        "num_workers": num_workers
    }

results = benchmark_throughput(table, num_queries=1000, num_workers=8)
print(f"Throughput: {results['qps']:.1f} QPS with {results['num_workers']} workers")
```

## Performance Monitoring

### Query Logging

```python
import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lancedb.performance")

def log_query_performance(func):
    """Decorator to log query performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start

        logger.info(
            f"Query completed in {duration*1000:.2f}ms, "
            f"results: {len(result) if hasattr(result, '__len__') else 'N/A'}"
        )

        if duration > 0.1:  # Log slow queries
            logger.warning(f"Slow query detected: {duration*1000:.2f}ms")

        return result
    return wrapper

@log_query_performance
def search(table, query, limit=10):
    return table.search(query).limit(limit).to_list()
```

### Metrics Collection

```python
from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class QueryMetrics:
    """Collect query metrics."""
    latencies: List[float] = field(default_factory=list)
    errors: int = 0
    total_results: int = 0

    def record(self, latency: float, num_results: int):
        self.latencies.append(latency)
        self.total_results += num_results

    def record_error(self):
        self.errors += 1

    def summary(self) -> dict:
        if not self.latencies:
            return {}

        return {
            "total_queries": len(self.latencies),
            "avg_latency_ms": np.mean(self.latencies) * 1000,
            "p99_latency_ms": np.percentile(self.latencies, 99) * 1000,
            "errors": self.errors,
            "error_rate": self.errors / (len(self.latencies) + self.errors),
            "avg_results": self.total_results / len(self.latencies)
        }

# Usage
metrics = QueryMetrics()

for query in queries:
    start = time.perf_counter()
    try:
        results = table.search(query).limit(10).to_list()
        metrics.record(time.perf_counter() - start, len(results))
    except Exception:
        metrics.record_error()

print(metrics.summary())
```

## Best Practices

### Index Lifecycle

```python
# 1. Create index after bulk data load
table.add(initial_data)
table.create_index(metric="cosine", num_partitions=256)

# 2. Rebuild index periodically after many updates
if table.count_rows() > last_indexed_count * 1.5:
    table.create_index(metric="cosine", num_partitions=256, replace=True)

# 3. Use appropriate index for query patterns
# - High accuracy needs: more partitions, more sub-vectors
# - High throughput needs: fewer partitions, fewer sub-vectors
```

### Query Patterns

```python
# 1. Always set reasonable limits
results = table.search(query).limit(10).to_list()  # Good
# results = table.search(query).to_list()  # Bad - fetches all

# 2. Select only needed columns
results = table.search(query).select(["id", "title"]).limit(10).to_list()

# 3. Use appropriate nprobes
results = table.search(query).nprobes(20).limit(10).to_list()

# 4. Index frequently filtered columns
table.create_scalar_index("category")
```

## Summary

In this chapter, you've learned:

- **Index Optimization**: Choosing and tuning index parameters
- **Query Optimization**: nprobes, refine factor, and column selection
- **Memory Management**: Efficient handling of large datasets
- **Concurrent Access**: Thread safety and connection pooling
- **Benchmarking**: Measuring latency, throughput, and recall
- **Monitoring**: Query logging and metrics collection

## Key Takeaways

1. **Index Matters**: Proper indexing is crucial for performance
2. **Tune nprobes**: Balance accuracy vs. speed
3. **Select Columns**: Don't fetch what you don't need
4. **Monitor Performance**: Track latency and throughput
5. **Benchmark**: Measure before and after optimizations

## Next Steps

Now that you can optimize performance, let's explore Production Deployment in Chapter 7 for cloud storage and scaling.

---

**Ready for Chapter 7?** [Production Deployment](07-production.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `table`, `query`, `results` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Performance` as an operating subsystem inside **LanceDB Tutorial: Serverless Vector Database for AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `search`, `limit`, `self` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Performance` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `table`.
2. **Input normalization**: shape incoming data so `query` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `results`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `table` and `query` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Integrations](05-integrations.md)
- [Next Chapter: Chapter 7: Production Deployment](07-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
