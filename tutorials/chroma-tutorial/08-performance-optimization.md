---
layout: default
title: "Chapter 8: Performance Optimization"
parent: "Chroma Tutorial"
nav_order: 8
---

# Chapter 8: Performance Optimization

Welcome to **Chapter 8: Performance Optimization**. In this part of **ChromaDB Tutorial: Building AI-Native Vector Databases**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Master Chroma performance tuning! This final chapter covers advanced optimization techniques, benchmarking, and performance best practices for maximum efficiency.

## Performance Profiling

### Query Performance Analysis

```python
import time
import statistics

class ChromaProfiler:
    def __init__(self, collection):
        self.collection = collection
        self.query_times = []

    def profile_query(self, query_texts, n_results=10, iterations=100):
        times = []

        for _ in range(iterations):
            start_time = time.time()
            self.collection.query(
                query_texts=query_texts,
                n_results=n_results
            )
            end_time = time.time()
            times.append(end_time - start_time)

        self.query_times = times
        return self.analyze_performance(times)

    def analyze_performance(self, times):
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times),
            'min': min(times),
            'max': max(times),
            'p95': sorted(times)[int(len(times) * 0.95)],
            'p99': sorted(times)[int(len(times) * 0.99)]
        }

# Usage
profiler = ChromaProfiler(collection)
performance = profiler.profile_query(["machine learning"], n_results=5)

print("Query Performance:")
for metric, value in performance.items():
    print(f"{metric}: {value:.4f}s")
```

## Indexing Optimization

### HNSW Parameter Tuning

```python
# Optimize HNSW parameters for your dataset
def optimize_hnsw_parameters(collection, sample_queries, target_recall=0.95):
    best_params = None
    best_performance = float('inf')

    # Test different parameter combinations
    param_grid = [
        {'M': 16, 'ef_construction': 100, 'ef': 64},
        {'M': 32, 'ef_construction': 200, 'ef': 128},
        {'M': 64, 'ef_construction': 400, 'ef': 256}
    ]

    for params in param_grid:
        # Create collection with test parameters
        test_collection = client.create_collection(
            name=f"test_hnsw_{params['M']}",
            metadata={
                'hnsw:M': params['M'],
                'hnsw:ef_construction': params['ef_construction'],
                'hnsw:search_ef': params['ef']
            }
        )

        # Add sample data
        test_collection.add(
            documents=["Sample document " + str(i) for i in range(1000)],
            ids=[f"doc_{i}" for i in range(1000)]
        )

        # Test performance
        profiler = ChromaProfiler(test_collection)
        performance = profiler.profile_query(sample_queries, iterations=10)

        # Calculate score (balance speed vs accuracy)
        score = performance['mean'] / target_recall

        if score < best_performance:
            best_performance = score
            best_params = params

    return best_params

# Usage
optimal_params = optimize_hnsw_parameters(
    collection,
    ["machine learning", "artificial intelligence"],
    target_recall=0.95
)
print(f"Optimal HNSW parameters: {optimal_params}")
```

## Memory Optimization

### Batch Processing

```python
# Optimize memory usage with batch processing
def batch_add_documents(collection, documents, batch_size=100):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]

        # Process batch
        batch_texts = [doc['text'] for doc in batch]
        batch_metadatas = [doc.get('metadata', {}) for doc in batch]
        batch_ids = [doc['id'] for doc in batch]

        collection.add(
            documents=batch_texts,
            metadatas=batch_metadatas,
            ids=batch_ids
        )

        # Force garbage collection
        import gc
        gc.collect()

# Usage
large_document_set = [
    {'id': f'doc_{i}', 'text': f'Document content {i}', 'metadata': {'category': 'test'}}
    for i in range(10000)
]

batch_add_documents(collection, large_document_set, batch_size=500)
```

### Memory-Mapped Storage

```python
# Use memory-mapped files for large datasets
import mmap
import os

class MemoryMappedChroma:
    def __init__(self, data_file, index_file):
        self.data_file = data_file
        self.index_file = index_file

    def create_memory_mapped_storage(self):
        # Create memory-mapped data file
        with open(self.data_file, 'wb') as f:
            f.write(b'\x00' * 1024 * 1024 * 1024)  # 1GB initial size

        # Memory map the file
        with open(self.data_file, 'r+b') as f:
            self.data_mmap = mmap.mmap(f.fileno(), 0)

        # Create memory-mapped index
        with open(self.index_file, 'wb') as f:
            f.write(b'\x00' * 100 * 1024 * 1024)  # 100MB for index

        with open(self.index_file, 'r+b') as f:
            self.index_mmap = mmap.mmap(f.fileno(), 0)

    def store_embedding(self, embedding_id, embedding_vector):
        # Store embedding in memory-mapped file
        offset = embedding_id * len(embedding_vector) * 4  # 4 bytes per float
        for i, value in enumerate(embedding_vector):
            self.data_mmap[offset + i*4:offset + (i+1)*4] = \
                struct.pack('f', value)

    def load_embedding(self, embedding_id, vector_size=768):
        # Load embedding from memory-mapped file
        offset = embedding_id * vector_size * 4
        data = self.data_mmap[offset:offset + vector_size * 4]
        return [struct.unpack('f', data[i:i+4])[0]
                for i in range(0, len(data), 4)]
```

## Query Optimization

### Approximate vs Exact Search

```python
# Choose between approximate and exact search based on requirements
def adaptive_search(collection, query_texts, accuracy_requirement=0.9):
    if accuracy_requirement > 0.95:
        # Use exact search for high accuracy requirements
        return collection.query(
            query_texts=query_texts,
            n_results=10,
            search_params={'exact': True}
        )
    else:
        # Use approximate search for speed
        return collection.query(
            query_texts=query_texts,
            n_results=10,
            search_params={'ef': 64}
        )

# Usage
high_accuracy_results = adaptive_search(collection, ["critical query"], accuracy_requirement=0.98)
fast_results = adaptive_search(collection, ["speed query"], accuracy_requirement=0.8)
```

### Query Result Caching

```python
from functools import lru_cache
import hashlib

class QueryCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size

    def get_cache_key(self, query_texts, n_results, where_clause=None):
        # Create deterministic cache key
        key_data = {
            'query_texts': sorted(query_texts),
            'n_results': n_results,
            'where': where_clause
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, cache_key):
        return self.cache.get(cache_key)

    def set(self, cache_key, results):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[cache_key] = results

# Usage
cache = QueryCache(max_size=500)

def cached_query(collection, query_texts, n_results=10, where=None):
    cache_key = cache.get_cache_key(query_texts, n_results, where)

    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    # Execute query
    result = collection.query(
        query_texts=query_texts,
        n_results=n_results,
        where=where
    )

    # Cache result
    cache.set(cache_key, result)
    return result
```

## Hardware Optimization

### GPU Acceleration

```python
# Use GPU for embedding generation and similarity search
import torch
from sentence_transformers import SentenceTransformer

class GPUOptimizedChroma:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)

    def generate_embeddings_gpu(self, texts):
        # Generate embeddings on GPU
        embeddings = self.model.encode(texts, batch_size=32, show_progress_bar=True)

        # Move to CPU for Chroma compatibility
        return embeddings.cpu().numpy()

    def batch_encode(self, texts, batch_size=64):
        # Process in batches to avoid GPU memory issues
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.generate_embeddings_gpu(batch_texts)
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

# Usage
gpu_chroma = GPUOptimizedChroma()
embeddings = gpu_chroma.batch_encode(large_text_dataset)
```

## Scaling Optimization

### Distributed Chroma

```python
# Scale across multiple machines
class DistributedChroma:
    def __init__(self, node_urls):
        self.nodes = [chromadb.Client(url=url) for url in node_urls]
        self.current_node = 0

    def distribute_collection(self, collection_name):
        # Create collection on all nodes
        for node in self.nodes:
            node.create_collection(name=collection_name)

    def add_documents_distributed(self, collection_name, documents, metadatas, ids):
        # Distribute documents across nodes
        node_index = 0
        batch_size = len(documents) // len(self.nodes)

        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            batch_docs = documents[i:end_idx]
            batch_metadatas = metadatas[i:end_idx]
            batch_ids = ids[i:end_idx]

            self.nodes[node_index].get_collection(collection_name).add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )

            node_index = (node_index + 1) % len(self.nodes)

    def query_distributed(self, collection_name, query_texts, n_results=10):
        # Query all nodes and combine results
        all_results = []
        for node in self.nodes:
            results = node.get_collection(collection_name).query(
                query_texts=query_texts,
                n_results=n_results
            )
            all_results.extend(results['documents'][0])

        # Remove duplicates and return top results
        unique_results = list(set(all_results))
        return unique_results[:n_results]

# Usage
distributed_chroma = DistributedChroma([
    "http://node1:8000",
    "http://node2:8000",
    "http://node3:8000"
])

distributed_chroma.distribute_collection("large_collection")
```

## Monitoring and Alerting

### Performance Monitoring

```python
import time
import threading

class PerformanceMonitor:
    def __init__(self, collection):
        self.collection = collection
        self.metrics = {
            'query_count': 0,
            'total_query_time': 0,
            'slow_queries': 0,
            'errors': 0
        }
        self.alerts = []

    def monitor_query(self, query_func, *args, **kwargs):
        start_time = time.time()
        try:
            result = query_func(*args, **kwargs)
            query_time = time.time() - start_time

            self.metrics['query_count'] += 1
            self.metrics['total_query_time'] += query_time

            if query_time > 1.0:  # Slow query threshold
                self.metrics['slow_queries'] += 1
                self.alerts.append(f"Slow query: {query_time:.2f}s")

            return result
        except Exception as e:
            self.metrics['errors'] += 1
            self.alerts.append(f"Query error: {str(e)}")
            raise

    def get_performance_report(self):
        avg_query_time = (self.metrics['total_query_time'] /
                         max(self.metrics['query_count'], 1))

        return {
            'total_queries': self.metrics['query_count'],
            'average_query_time': avg_query_time,
            'slow_query_percentage': (self.metrics['slow_queries'] /
                                    max(self.metrics['query_count'], 1)) * 100,
            'error_rate': (self.metrics['errors'] /
                          max(self.metrics['query_count'], 1)) * 100,
            'alerts': self.alerts[-10:]  # Last 10 alerts
        }

# Usage
monitor = PerformanceMonitor(collection)

# Monitor a query
results = monitor.monitor_query(
    collection.query,
    query_texts=["test query"],
    n_results=5
)

# Get performance report
report = monitor.get_performance_report()
print("Performance Report:", report)
```

## What We've Accomplished

Congratulations! 🎉 You've mastered Chroma performance optimization:

1. **Performance Profiling** - Query analysis and benchmarking
2. **Indexing Optimization** - HNSW parameter tuning for your data
3. **Memory Optimization** - Batch processing and memory mapping
4. **Query Optimization** - Adaptive search and result caching
5. **Hardware Optimization** - GPU acceleration and distributed scaling
6. **Monitoring** - Real-time performance tracking and alerting

## Final Thoughts

Performance optimization is an ongoing process. Monitor your Chroma deployment regularly, profile queries, and adjust parameters based on your specific use case and data characteristics.

---

**Practice what you've learned:**
1. Profile your Chroma queries and identify bottlenecks
2. Optimize HNSW parameters for your dataset
3. Implement GPU acceleration for embedding generation
4. Set up distributed Chroma for scaling
5. Create monitoring and alerting for production

*What's your biggest performance challenge with Chroma?* ⚡

---

**🎓 Tutorial Complete!**

You've successfully completed the comprehensive Chroma tutorial! You now have the knowledge to:

- Build AI applications with vector databases
- Optimize Chroma for production workloads
- Integrate Chroma with popular AI frameworks
- Scale Chroma deployments across multiple machines
- Monitor and troubleshoot Chroma performance

*Ready to build your next AI application with Chroma?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `collection`, `query_texts` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Performance Optimization` as an operating subsystem inside **ChromaDB Tutorial: Building AI-Native Vector Databases**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `n_results`, `times`, `query` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Performance Optimization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `collection` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `query_texts`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/chroma-core/chroma)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `collection` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Production Deployment](07-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
