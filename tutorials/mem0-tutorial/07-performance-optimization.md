---
layout: default
title: "Chapter 7: Performance Optimization"
parent: "Mem0 Tutorial"
nav_order: 7
---

# Chapter 7: Performance Optimization

> Optimize Mem0 memory systems for high-performance, scalable AI applications.

## 🎯 Overview

This chapter covers performance optimization techniques for Mem0 memory systems, including indexing strategies, caching mechanisms, batch processing, and scaling approaches to handle enterprise-level workloads efficiently.

## 🚀 Memory Indexing Strategies

### Advanced Indexing Techniques

```python
from mem0 import Memory
from typing import Dict, List, Any, Optional
import numpy as np
import faiss
import time

class OptimizedMemoryIndex:
    """High-performance memory indexing system"""

    def __init__(self, dimension: int = 384, index_type: str = "IVF"):
        self.dimension = dimension
        self.index_type = index_type
        self.memory = Memory()
        self.vector_index = self._initialize_vector_index()
        self.metadata_index = {}
        self.performance_stats = {
            "index_operations": 0,
            "search_operations": 0,
            "avg_index_time": 0,
            "avg_search_time": 0
        }

    def _initialize_vector_index(self):
        """Initialize optimized vector index"""

        if self.index_type == "IVF":
            # IVF (Inverted File) index for large datasets
            quantizer = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine
            index = faiss.IndexIVFFlat(quantizer, self.dimension, 100)  # 100 clusters
            index.train(np.random.random((1000, self.dimension)).astype('float32'))

        elif self.index_type == "HNSW":
            # HNSW for high-dimensional data
            index = faiss.IndexHNSWFlat(self.dimension, 32)  # 32 neighbors

        elif self.index_type == "PQ":
            # Product Quantization for memory efficiency
            m = self.dimension // 4  # Number of sub-quantizers
            index = faiss.IndexPQ(self.dimension, m, 8)  # 8 bits per sub-vector
            index.train(np.random.random((10000, self.dimension)).astype('float32'))

        else:
            # Flat index for small datasets
            index = faiss.IndexFlatIP(self.dimension)

        return index

    def add_memories_batch(self, memories: List[Dict[str, Any]], batch_size: int = 100):
        """Add memories in optimized batches"""

        start_time = time.time()

        for i in range(0, len(memories), batch_size):
            batch = memories[i:i + batch_size]

            # Prepare batch data
            vectors = []
            metadata_batch = []

            for memory in batch:
                # Generate or get embedding (simplified)
                vector = self._get_embedding(memory["content"])
                vectors.append(vector)

                # Prepare metadata
                metadata = {
                    "content": memory["content"],
                    "user_id": memory.get("user_id"),
                    "timestamp": memory.get("timestamp", time.time()),
                    "importance": memory.get("importance", 0.5)
                }
                metadata_batch.append(metadata)

            # Add to vector index
            vectors_array = np.array(vectors).astype('float32')
            self.vector_index.add(vectors_array)

            # Update metadata index
            base_idx = len(self.metadata_index)
            for j, metadata in enumerate(metadata_batch):
                self.metadata_index[base_idx + j] = metadata

        # Update performance stats
        total_time = time.time() - start_time
        self.performance_stats["index_operations"] += len(memories)
        self.performance_stats["avg_index_time"] = (
            (self.performance_stats["avg_index_time"] * (self.performance_stats["index_operations"] - len(memories))) +
            total_time
        ) / self.performance_stats["index_operations"]

        print(f"Indexed {len(memories)} memories in {total_time:.3f}s")

    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text (simplified)"""
        # In practice, use a proper embedding model
        # This is a placeholder
        return np.random.random(self.dimension).astype('float32')

    def search_memories_optimized(self, query: str, top_k: int = 5,
                                search_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Optimized memory search with performance monitoring"""

        start_time = time.time()

        # Get query embedding
        query_vector = self._get_embedding(query).reshape(1, -1).astype('float32')

        # Configure search parameters
        if search_params:
            if hasattr(self.vector_index, 'nprobe'):
                self.vector_index.nprobe = search_params.get('nprobe', 10)
            if hasattr(self.vector_index, 'efSearch'):
                self.vector_index.efSearch = search_params.get('efSearch', 64)

        # Perform vector search
        scores, indices = self.vector_index.search(query_vector, top_k)

        # Retrieve results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.metadata_index):
                metadata = self.metadata_index[idx]
                result = {
                    "content": metadata["content"],
                    "score": float(score),
                    "metadata": metadata
                }
                results.append(result)

        # Update performance stats
        search_time = time.time() - start_time
        self.performance_stats["search_operations"] += 1
        self.performance_stats["avg_search_time"] = (
            (self.performance_stats["avg_search_time"] * (self.performance_stats["search_operations"] - 1)) +
            search_time
        ) / self.performance_stats["search_operations"]

        return results

    def optimize_index(self):
        """Optimize index for better performance"""

        if hasattr(self.vector_index, 'make_direct_map'):
            # For IVF indexes
            self.vector_index.make_direct_map()

        # Additional optimizations based on index type
        if self.index_type == "HNSW":
            # Optimize HNSW parameters
            pass
        elif self.index_type == "PQ":
            # Product quantization specific optimizations
            pass

        print("Index optimization completed")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""

        metrics = self.performance_stats.copy()

        # Add index-specific metrics
        metrics.update({
            "index_type": self.index_type,
            "dimension": self.dimension,
            "total_memories": len(self.metadata_index),
            "index_size_mb": self._calculate_index_size(),
            "queries_per_second": (
                self.performance_stats["search_operations"] /
                max(self.performance_stats["avg_search_time"], 0.001)
            ) if self.performance_stats["search_operations"] > 0 else 0
        })

        return metrics

    def _calculate_index_size(self) -> float:
        """Calculate approximate index size in MB"""

        # Rough estimation
        vector_size = len(self.metadata_index) * self.dimension * 4  # 4 bytes per float32
        metadata_size = sum(len(str(metadata)) for metadata in self.metadata_index.values())

        total_bytes = vector_size + metadata_size
        return total_bytes / (1024 * 1024)  # Convert to MB

# Usage
optimized_index = OptimizedMemoryIndex(dimension=384, index_type="IVF")

# Add memories in batches
sample_memories = [
    {"content": f"Sample memory {i}", "user_id": f"user_{i%10}", "importance": 0.5 + (i % 5) * 0.1}
    for i in range(1000)
]

optimized_index.add_memories_batch(sample_memories, batch_size=100)

# Search with optimization
results = optimized_index.search_memories_optimized(
    "sample query",
    search_params={"nprobe": 20}
)

print(f"Search returned {len(results)} results")
for result in results[:3]:
    print(f"  Score: {result['score']:.3f} - {result['content'][:50]}...")

# Get performance metrics
metrics = optimized_index.get_performance_metrics()
print(f"Performance Metrics: {metrics}")
```

## 💾 Caching and Memory Management

### Multi-Level Caching System

```python
from cachetools import TTLCache, LRUCache
import asyncio
import hashlib
from typing import Dict, List, Any, Optional
import time

class MemoryCacheSystem:
    """Sophisticated caching system for memory operations"""

    def __init__(self, l1_ttl: int = 300, l2_maxsize: int = 10000, l3_path: str = "./memory_cache"):
        # L1: Fast in-memory cache with TTL
        self.l1_cache = TTLCache(maxsize=1000, ttl=l1_ttl)

        # L2: Larger LRU cache
        self.l2_cache = LRUCache(maxsize=l2_maxsize)

        # L3: Persistent disk cache (simplified)
        self.l3_cache = {}
        self.l3_path = l3_path

        # Cache statistics
        self.stats = {
            "l1_hits": 0, "l1_misses": 0,
            "l2_hits": 0, "l2_misses": 0,
            "l3_hits": 0, "l3_misses": 0,
            "total_requests": 0
        }

        # Semantic caching for similar queries
        self.semantic_cache = TTLCache(maxsize=500, ttl=1800)  # 30 minutes
        self.semantic_threshold = 0.85

    def generate_cache_key(self, operation: str, *args, **kwargs) -> str:
        """Generate deterministic cache key"""

        # Sort kwargs for consistency
        sorted_kwargs = {k: kwargs[k] for k in sorted(kwargs.keys())}

        # Create cache data
        cache_data = {
            "operation": operation,
            "args": args,
            "kwargs": sorted_kwargs
        }

        # Generate hash
        cache_str = str(cache_data).encode()
        return hashlib.md5(cache_str).hexdigest()

    async def get_or_compute(self, key: str, compute_func, use_semantic: bool = False):
        """Get from cache or compute with semantic fallback"""

        # Check L1 cache
        if key in self.l1_cache:
            self.stats["l1_hits"] += 1
            self.stats["total_requests"] += 1
            return self.l1_cache[key], True

        self.stats["l1_misses"] += 1

        # Check L2 cache
        if key in self.l2_cache:
            self.stats["l2_hits"] += 1
            value = self.l2_cache[key]
            self.l1_cache[key] = value  # Promote to L1
            self.stats["total_requests"] += 1
            return value, True

        self.stats["l2_misses"] += 1

        # Check semantic cache if enabled
        if use_semantic:
            semantic_key = self._find_semantic_match(key)
            if semantic_key and semantic_key in self.semantic_cache:
                self.stats["l3_hits"] += 1
                value = self.semantic_cache[semantic_key]
                # Store in higher levels
                self.l2_cache[key] = value
                self.l1_cache[key] = value
                self.stats["total_requests"] += 1
                return value, True

        # Compute value
        value = await compute_func()

        # Cache the result
        await self.set(key, value, use_semantic)

        self.stats["total_requests"] += 1
        return value, False

    async def set(self, key: str, value: Any, use_semantic: bool = False):
        """Set value in cache hierarchy"""

        # Always set in L1 and L2
        self.l1_cache[key] = value
        self.l2_cache[key] = value

        # Set in semantic cache if enabled
        if use_semantic:
            self.semantic_cache[key] = value

        # Optional: Persist to L3 (disk) for important data
        if self._is_important_value(value):
            self.l3_cache[key] = value

    def _find_semantic_match(self, key: str) -> Optional[str]:
        """Find semantically similar cached key"""

        # Extract operation and parameters from key
        # This is a simplified implementation
        for cached_key in self.semantic_cache.keys():
            if self._calculate_similarity(key, cached_key) > self.semantic_threshold:
                return cached_key

        return None

    def _calculate_similarity(self, key1: str, key2: str) -> float:
        """Calculate similarity between cache keys"""

        # Simple similarity based on common substrings
        # In practice, use embeddings or more sophisticated similarity
        words1 = set(key1.split('_'))
        words2 = set(key2.split('_'))

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0

    def _is_important_value(self, value: Any) -> bool:
        """Determine if value should be persisted to disk"""

        # Simple heuristics for importance
        if isinstance(value, dict):
            return len(value) > 5  # Large results
        elif isinstance(value, list):
            return len(value) > 10  # Many items

        return False

    def get_cache_performance(self) -> Dict[str, Any]:
        """Get comprehensive cache performance metrics"""

        total_requests = self.stats["total_requests"]

        if total_requests == 0:
            return {"error": "No cache requests yet"}

        performance = {
            "total_requests": total_requests,
            "overall_hit_rate": (
                self.stats["l1_hits"] + self.stats["l2_hits"] + self.stats["l3_hits"]
            ) / total_requests,
            "l1_hit_rate": self.stats["l1_hits"] / (self.stats["l1_hits"] + self.stats["l1_misses"]) if (self.stats["l1_hits"] + self.stats["l1_misses"]) > 0 else 0,
            "l2_hit_rate": self.stats["l2_hits"] / (self.stats["l2_hits"] + self.stats["l2_misses"]) if (self.stats["l2_hits"] + self.stats["l2_misses"]) > 0 else 0,
            "semantic_hit_rate": self.stats["l3_hits"] / (self.stats["l3_hits"] + self.stats["l3_misses"]) if (self.stats["l3_hits"] + self.stats["l3_misses"]) > 0 else 0,
            "cache_sizes": {
                "l1": len(self.l1_cache),
                "l2": len(self.l2_cache),
                "semantic": len(self.semantic_cache),
                "persistent": len(self.l3_cache)
            }
        }

        return performance

    def optimize_cache_strategy(self):
        """Optimize cache strategy based on usage patterns"""

        performance = self.get_cache_performance()

        # Adjust cache sizes based on hit rates
        l1_hit_rate = performance["l1_hit_rate"]
        l2_hit_rate = performance["l2_hit_rate"]

        if l1_hit_rate > 0.8:
            # L1 is very effective, consider increasing size
            print("L1 cache performing well, consider increasing size")
        elif l1_hit_rate < 0.5:
            # L1 not effective, consider reducing size or TTL
            print("L1 cache underperforming, consider optimization")

        if l2_hit_rate < 0.3:
            # L2 not effective, consider different eviction policy
            print("L2 cache needs optimization")

    def clear_cache(self, level: str = "all"):
        """Clear cache at specified level"""

        if level in ["all", "l1"]:
            self.l1_cache.clear()
        if level in ["all", "l2"]:
            self.l2_cache.clear()
        if level in ["all", "semantic"]:
            self.semantic_cache.clear()
        if level in ["all", "l3"]:
            self.l3_cache.clear()

        print(f"Cleared {level} cache level(s)")

# Usage
cache_system = MemoryCacheSystem()

# Example async memory operation
async def get_user_memories(user_id: str):
    """Simulated memory retrieval operation"""
    await asyncio.sleep(0.1)  # Simulate I/O delay
    return [f"Memory {i} for {user_id}" for i in range(5)]

# Cached memory retrieval
async def cached_memory_retrieval(user_id: str):
    cache_key = cache_system.generate_cache_key("user_memories", user_id=user_id)

    async def compute_memories():
        return await get_user_memories(user_id)

    memories, was_cached = await cache_system.get_or_compute(
        cache_key,
        compute_memories,
        use_semantic=True
    )

    return memories, was_cached

# Test caching
results = []
for user_id in ["user1", "user2", "user1"]:  # Repeat user1 to test cache hit
    memories, cached = await cached_memory_retrieval(user_id)
    results.append((user_id, len(memories), cached))

print("Cache Test Results:")
for user_id, count, cached in results:
    print(f"  {user_id}: {count} memories, cached: {cached}")

# Get performance metrics
performance = cache_system.get_cache_performance()
print(f"Cache Performance: {performance}")
```

## ⚡ Batch Processing and Parallelization

### High-Throughput Memory Operations

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from typing import List, Dict, Any
import time

class BatchMemoryProcessor:
    """High-throughput batch processing for memory operations"""

    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, multiprocessing.cpu_count() * 2)
        self.thread_executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_executor = ProcessPoolExecutor(max_workers=min(4, multiprocessing.cpu_count()))

        # Performance tracking
        self.performance_stats = {
            "batches_processed": 0,
            "total_items_processed": 0,
            "avg_batch_time": 0,
            "throughput_items_per_sec": 0
        }

    async def batch_add_memories(self, memory_batches: List[List[Dict[str, Any]]],
                               batch_size: int = 100) -> Dict[str, Any]:
        """Add multiple batches of memories concurrently"""

        start_time = time.time()

        # Process batches concurrently
        tasks = []
        for batch in memory_batches:
            # Split large batches
            for i in range(0, len(batch), batch_size):
                sub_batch = batch[i:i + batch_size]
                task = self._process_memory_batch(sub_batch)
                tasks.append(task)

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        total_processed = 0
        errors = []

        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
            else:
                total_processed += result

        processing_time = time.time() - start_time

        # Update performance stats
        self.performance_stats["batches_processed"] += len(memory_batches)
        self.performance_stats["total_items_processed"] += total_processed
        self.performance_stats["avg_batch_time"] = (
            (self.performance_stats["avg_batch_time"] * (self.performance_stats["batches_processed"] - len(memory_batches))) +
            processing_time
        ) / self.performance_stats["batches_processed"]

        self.performance_stats["throughput_items_per_sec"] = (
            self.performance_stats["total_items_processed"] / processing_time
        ) if processing_time > 0 else 0

        return {
            "total_processed": total_processed,
            "processing_time": processing_time,
            "throughput": total_processed / processing_time if processing_time > 0 else 0,
            "errors": errors,
            "batches_completed": len([r for r in results if not isinstance(r, Exception)])
        }

    async def _process_memory_batch(self, batch: List[Dict[str, Any]]) -> int:
        """Process a single batch of memories"""

        # Use thread pool for I/O operations
        loop = asyncio.get_running_loop()

        def process_batch_sync():
            processed_count = 0
            for memory_data in batch:
                try:
                    # Simulate memory addition (replace with actual Mem0 call)
                    self._add_memory_sync(memory_data)
                    processed_count += 1
                except Exception as e:
                    print(f"Error processing memory: {e}")
                    continue

            return processed_count

        result = await loop.run_in_executor(self.thread_executor, process_batch_sync)
        return result

    def _add_memory_sync(self, memory_data: Dict[str, Any]):
        """Synchronous memory addition (placeholder)"""
        # In practice, this would call Mem0's add method
        time.sleep(0.01)  # Simulate processing time

    async def parallel_memory_search(self, queries: List[str], user_ids: List[str] = None,
                                   max_concurrent: int = 10) -> List[List[Dict[str, Any]]]:
        """Execute multiple memory searches in parallel"""

        if user_ids is None:
            user_ids = [None] * len(queries)

        # Create search tasks
        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = []

        async def limited_search(query: str, user_id: str = None):
            async with semaphore:
                return await self._single_memory_search(query, user_id)

        for query, user_id in zip(queries, user_ids):
            task = limited_search(query, user_id)
            tasks.append(task)

        # Execute searches concurrently
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        performance = {
            "total_queries": len(queries),
            "total_time": total_time,
            "avg_time_per_query": total_time / len(queries),
            "queries_per_second": len(queries) / total_time
        }

        return results, performance

    async def _single_memory_search(self, query: str, user_id: str = None) -> List[Dict[str, Any]]:
        """Execute single memory search"""

        # Simulate search operation
        await asyncio.sleep(0.05)  # Simulate I/O delay

        # Return mock results
        return [
            {
                "content": f"Memory result for '{query}'",
                "score": 0.85,
                "metadata": {"user_id": user_id, "relevance": "high"}
            }
        ]

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""

        return {
            "batch_processing": self.performance_stats,
            "system_info": {
                "max_workers": self.max_workers,
                "cpu_count": multiprocessing.cpu_count(),
                "thread_pool_active": len(self.thread_executor._threads) if hasattr(self.thread_executor, '_threads') else 0
            },
            "throughput_analysis": {
                "items_per_second": self.performance_stats["throughput_items_per_sec"],
                "estimated_hourly_capacity": self.performance_stats["throughput_items_per_sec"] * 3600,
                "estimated_daily_capacity": self.performance_stats["throughput_items_per_sec"] * 3600 * 24
            }
        }

    def optimize_batch_size(self, sample_batches: List[List[Dict[str, Any]]]) -> int:
        """Dynamically determine optimal batch size"""

        # Test different batch sizes
        test_sizes = [10, 50, 100, 200, 500]
        results = {}

        async def test_batch_size(batch_size: int):
            # Create test batches
            test_data = sample_batches[0][:batch_size] if sample_batches else []
            if not test_data:
                return batch_size, 0

            start_time = time.time()
            result = await self._process_memory_batch(test_data)
            processing_time = time.time() - start_time

            throughput = len(test_data) / processing_time if processing_time > 0 else 0
            return batch_size, throughput

        # Test all sizes
        for batch_size in test_sizes:
            _, throughput = asyncio.run(test_batch_size(batch_size))
            results[batch_size] = throughput

        # Find optimal size (balance between throughput and memory usage)
        optimal_size = max(results.items(), key=lambda x: x[1])[0]

        print(f"Optimal batch size determined: {optimal_size}")
        print(f"Throughput by size: {results}")

        return optimal_size

# Usage
batch_processor = BatchMemoryProcessor(max_workers=8)

# Create sample memory batches
memory_batches = [
    [{"content": f"Memory {i} content", "user_id": f"user_{i%10}"} for i in range(batch_size)]
    for batch_size in [50, 75, 100]  # Different batch sizes
]

# Process batches concurrently
async def process_batches():
    results = await batch_processor.batch_add_memories(memory_batches, batch_size=50)

    print("Batch Processing Results:")
    print(f"  Total processed: {results['total_processed']}")
    print(f"  Processing time: {results['processing_time']:.3f}s")
    print(f"  Throughput: {results['throughput']:.1f} items/sec")
    print(f"  Errors: {len(results['errors'])}")

# Execute parallel searches
async def parallel_searches():
    queries = [f"Search query {i}" for i in range(20)]
    user_ids = [f"user_{i%5}" for i in range(20)]

    results, performance = await batch_processor.parallel_memory_search(
        queries, user_ids, max_concurrent=5
    )

    print("Parallel Search Performance:")
    print(f"  Total queries: {performance['total_queries']}")
    print(f"  Total time: {performance['total_time']:.3f}s")
    print(f"  Avg time per query: {performance['avg_time_per_query']:.3f}s")
    print(f"  Queries per second: {performance['queries_per_second']:.1f}")

# Run demonstrations
asyncio.run(process_batches())
asyncio.run(parallel_searches())

# Get performance stats
stats = batch_processor.get_performance_stats()
print(f"Performance Stats: {stats}")

# Optimize batch size
sample_batches = [[{"content": f"Sample {i}"} for i in range(100)]]
optimal_size = batch_processor.optimize_batch_size(sample_batches)
print(f"Optimal batch size: {optimal_size}")
```

## 📊 Memory System Monitoring

### Real-Time Performance Monitoring

```python
import psutil
import GPUtil
from mem0 import Memory
from typing import Dict, Any
import threading
import time
import logging

class MemorySystemMonitor:
    """Comprehensive monitoring for memory systems"""

    def __init__(self, memory_system: Memory, monitoring_interval: int = 30):
        self.memory_system = memory_system
        self.monitoring_interval = monitoring_interval

        # Monitoring data
        self.metrics_history = []
        self.alerts = []
        self.performance_baselines = {}

        # Configure logging
        self.logger = logging.getLogger("MemoryMonitor")
        self.logger.setLevel(logging.INFO)

        # Start monitoring thread
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()

    def _monitoring_loop(self):
        """Continuous monitoring loop"""

        while self.monitoring_active:
            try:
                # Collect metrics
                metrics = self._collect_system_metrics()

                # Store in history
                self.metrics_history.append(metrics)

                # Keep only recent history (last 100 data points)
                if len(self.metrics_history) > 100:
                    self.metrics_history = self.metrics_history[-100:]

                # Check for alerts
                self._check_alerts(metrics)

                # Update baselines
                self._update_baselines(metrics)

            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")

            time.sleep(self.monitoring_interval)

    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""

        metrics = {
            "timestamp": time.time(),
            "memory_system": self._get_memory_metrics(),
            "system_resources": self._get_system_resource_metrics(),
            "performance": self._get_performance_metrics()
        }

        return metrics

    def _get_memory_metrics(self) -> Dict[str, Any]:
        """Get memory system specific metrics"""

        try:
            # These would be actual Mem0 metrics in practice
            memory_metrics = {
                "total_memories": 1000,  # Placeholder
                "active_users": 50,      # Placeholder
                "avg_query_time": 0.15,  # Placeholder
                "cache_hit_rate": 0.85,  # Placeholder
                "memory_usage_mb": 256   # Placeholder
            }

            return memory_metrics

        except Exception as e:
            return {"error": str(e)}

    def _get_system_resource_metrics(self) -> Dict[str, Any]:
        """Get system resource usage metrics"""

        try:
            # CPU metrics
            cpu_metrics = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_count": psutil.cpu_count(),
                "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else None
            }

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_metrics = {
                "memory_total": memory.total,
                "memory_used": memory.used,
                "memory_percent": memory.percent,
                "memory_available": memory.available
            }

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_metrics = {
                "disk_total": disk.total,
                "disk_used": disk.used,
                "disk_percent": disk.percent,
                "disk_free": disk.free
            }

            # GPU metrics (if available)
            gpu_metrics = {}
            try:
                gpus = GPUtil.getGPUs()
                for i, gpu in enumerate(gpus):
                    gpu_metrics[f"gpu_{i}"] = {
                        "name": gpu.name,
                        "memory_used": gpu.memoryUsed,
                        "memory_total": gpu.memoryTotal,
                        "memory_percent": gpu.memoryUtil * 100,
                        "gpu_percent": gpu.load * 100
                    }
            except:
                gpu_metrics["gpu_available"] = False

            return {
                "cpu": cpu_metrics,
                "memory": memory_metrics,
                "disk": disk_metrics,
                "gpu": gpu_metrics
            }

        except Exception as e:
            return {"error": str(e)}

    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance-related metrics"""

        # Calculate trends from recent history
        if len(self.metrics_history) < 2:
            return {"insufficient_data": True}

        recent_metrics = self.metrics_history[-10:]  # Last 10 data points

        # Calculate trends
        memory_usage_trend = self._calculate_trend([
            m["memory_system"].get("memory_usage_mb", 0) for m in recent_metrics
        ])

        query_time_trend = self._calculate_trend([
            m["memory_system"].get("avg_query_time", 0) for m in recent_metrics
        ])

        return {
            "memory_usage_trend": memory_usage_trend,
            "query_time_trend": query_time_trend,
            "avg_response_time": sum([
                m["memory_system"].get("avg_query_time", 0) for m in recent_metrics
            ]) / len(recent_metrics)
        }

    def _calculate_trend(self, values: list) -> str:
        """Calculate trend direction from values"""

        if len(values) < 2:
            return "insufficient_data"

        # Simple linear trend
        n = len(values)
        x = list(range(n))
        y = values

        # Calculate slope (simplified)
        if n > 1:
            slope = (y[-1] - y[0]) / (x[-1] - x[0])
            if slope > 0.01:
                return "increasing"
            elif slope < -0.01:
                return "decreasing"
            else:
                return "stable"

        return "unknown"

    def _check_alerts(self, current_metrics: Dict[str, Any]):
        """Check for alert conditions"""

        alerts = []

        # Memory usage alerts
        memory_percent = current_metrics["system_resources"]["memory"].get("memory_percent", 0)
        if memory_percent > 90:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "critical",
                "message": f"Memory usage is {memory_percent:.1f}%",
                "timestamp": current_metrics["timestamp"]
            })

        # CPU usage alerts
        cpu_percent = current_metrics["system_resources"]["cpu"].get("cpu_percent", 0)
        if cpu_percent > 95:
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning",
                "message": f"CPU usage is {cpu_percent:.1f}%",
                "timestamp": current_metrics["timestamp"]
            })

        # Performance degradation alerts
        if current_metrics["performance"].get("query_time_trend") == "increasing":
            alerts.append({
                "type": "performance_degradation",
                "severity": "warning",
                "message": "Query response times are increasing",
                "timestamp": current_metrics["timestamp"]
            })

        # Add alerts to history
        self.alerts.extend(alerts)

        # Keep only recent alerts (last 100)
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

        # Log critical alerts
        for alert in alerts:
            if alert["severity"] == "critical":
                self.logger.error(f"CRITICAL ALERT: {alert['message']}")

    def _update_baselines(self, metrics: Dict[str, Any]):
        """Update performance baselines"""

        # Update rolling baselines
        for key, value in metrics["memory_system"].items():
            if isinstance(value, (int, float)):
                if key not in self.performance_baselines:
                    self.performance_baselines[key] = []

                self.performance_baselines[key].append(value)

                # Keep only recent values (last 50)
                if len(self.performance_baselines[key]) > 50:
                    self.performance_baselines[key] = self.performance_baselines[key][-50:]

    def get_monitoring_report(self) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""

        if not self.metrics_history:
            return {"error": "No monitoring data available"}

        latest_metrics = self.metrics_history[-1]

        # Calculate baselines
        baselines = {}
        for key, values in self.performance_baselines.items():
            if values:
                baselines[key] = {
                    "current": values[-1],
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                }

        # Get recent alerts
        recent_alerts = self.alerts[-10:] if self.alerts else []

        report = {
            "current_status": latest_metrics,
            "baselines": baselines,
            "recent_alerts": recent_alerts,
            "trends": latest_metrics.get("performance", {}),
            "system_health": self._calculate_system_health(latest_metrics),
            "recommendations": self._generate_recommendations(latest_metrics, baselines)
        }

        return report

    def _calculate_system_health(self, metrics: Dict[str, Any]) -> str:
        """Calculate overall system health score"""

        health_score = 100

        # Memory usage penalty
        memory_percent = metrics["system_resources"]["memory"].get("memory_percent", 0)
        if memory_percent > 80:
            health_score -= (memory_percent - 80) * 0.5

        # CPU usage penalty
        cpu_percent = metrics["system_resources"]["cpu"].get("cpu_percent", 0)
        if cpu_percent > 90:
            health_score -= (cpu_percent - 90) * 2

        # Alert penalties
        recent_alerts = [a for a in self.alerts[-5] if a["timestamp"] > time.time() - 3600]  # Last hour
        health_score -= len(recent_alerts) * 5

        # Performance penalties
        if metrics["performance"].get("query_time_trend") == "increasing":
            health_score -= 10

        health_score = max(0, min(100, health_score))

        if health_score >= 90:
            return "excellent"
        elif health_score >= 75:
            return "good"
        elif health_score >= 60:
            return "fair"
        elif health_score >= 40:
            return "poor"
        else:
            return "critical"

    def _generate_recommendations(self, metrics: Dict[str, Any], baselines: Dict[str, Any]) -> List[str]:
        """Generate system optimization recommendations"""

        recommendations = []

        # Memory recommendations
        memory_percent = metrics["system_resources"]["memory"].get("memory_percent", 0)
        if memory_percent > 85:
            recommendations.append("Consider increasing system memory or implementing memory optimization techniques")

        # Performance recommendations
        if metrics["performance"].get("query_time_trend") == "increasing":
            recommendations.append("Query performance is degrading - consider index optimization or caching improvements")

        # Resource recommendations
        cpu_percent = metrics["system_resources"]["cpu"].get("cpu_percent", 0)
        if cpu_percent > 90:
            recommendations.append("High CPU usage detected - consider scaling or optimizing compute-intensive operations")

        if not recommendations:
            recommendations.append("System is performing well - continue monitoring")

        return recommendations

    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring_active = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

# Usage
memory_system = Memory()  # Your Mem0 instance
monitor = MemorySystemMonitor(memory_system, monitoring_interval=30)

# Let it run for a while to collect data
print("Monitoring system started... (waiting for data collection)")
time.sleep(120)  # Collect data for 2 minutes

# Get monitoring report
report = monitor.get_monitoring_report()
print("Monitoring Report:")
print(f"System Health: {report['system_health']}")
print(f"Recent Alerts: {len(report['recent_alerts'])}")
print(f"Recommendations: {report['recommendations']}")

# Stop monitoring
monitor.stop_monitoring()
print("Monitoring stopped")
```

## 🎯 Best Practices

### Performance Optimization Guidelines

1. **Index Optimization**: Use appropriate indexing strategies for your data patterns
2. **Caching Strategy**: Implement multi-level caching with semantic similarity
3. **Batch Processing**: Process operations in batches for better throughput
4. **Resource Monitoring**: Continuously monitor system resources and performance
5. **Scalable Architecture**: Design for horizontal scaling and load distribution

### Monitoring and Alerting

1. **Comprehensive Metrics**: Track all aspects of system performance
2. **Alert Thresholds**: Set appropriate alert thresholds for different metrics
3. **Trend Analysis**: Monitor performance trends over time
4. **Automated Responses**: Implement automated responses to common issues
5. **Regular Reporting**: Generate regular performance reports

### Production Scaling

1. **Load Balancing**: Distribute load across multiple instances
2. **Data Partitioning**: Partition data for better performance
3. **Async Processing**: Use async operations for better concurrency
4. **Resource Limits**: Set appropriate resource limits and quotas
5. **Backup and Recovery**: Implement robust backup and recovery procedures

## 📈 Next Steps

With performance optimization mastered, you're ready for:

- **[Chapter 8: Deployment & Monitoring](08-production-deployment.md)** - Deploying memory-enabled AI systems at scale

---

**Ready to deploy optimized memory systems? Continue to [Chapter 8: Deployment & Monitoring](08-production-deployment.md)!** 🚀