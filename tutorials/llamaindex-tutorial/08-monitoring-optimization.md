---
layout: default
title: "Chapter 8: Monitoring & Optimization"
parent: "LlamaIndex Tutorial"
nav_order: 8
---

# Chapter 8: Monitoring & Optimization

Welcome to **Chapter 8: Monitoring & Optimization**. In this part of **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master advanced performance tuning, observability, and optimization techniques for production LlamaIndex applications.

## 🎯 Overview

This final chapter covers advanced monitoring, performance optimization, and operational excellence for LlamaIndex RAG systems. You'll learn to identify bottlenecks, implement advanced caching strategies, optimize for specific use cases, and maintain high-performance production deployments.

## 📊 Advanced Monitoring

### Distributed Tracing

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import time

class DistributedTracer:
    def __init__(self, service_name="llamaindex-rag"):
        self.service_name = service_name
        self._setup_tracing()

    def _setup_tracing(self):
        """Setup OpenTelemetry distributed tracing"""

        # Create tracer provider
        trace.set_tracer_provider(TracerProvider())
        tracer_provider = trace.get_tracer_provider()

        # Jaeger exporter for trace collection
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
        )

        # Batch span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        tracer_provider.add_span_processor(span_processor)

        # Get tracer
        self.tracer = trace.get_tracer(__name__)

    def instrument_app(self, app):
        """Instrument FastAPI application"""
        FastAPIInstrumentor.instrument_app(app)
        RequestsInstrumentor().instrument()

    def trace_query_operation(self, func_name="query"):
        """Decorator for tracing query operations"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                with self.tracer.start_as_current_span(func_name) as span:
                    # Add span attributes
                    span.set_attribute("operation.type", "query")
                    span.set_attribute("service.name", self.service_name)

                    try:
                        start_time = time.time()
                        result = func(*args, **kwargs)
                        duration = time.time() - start_time

                        # Add metrics to span
                        span.set_attribute("operation.duration", duration)
                        span.set_attribute("operation.success", True)

                        if hasattr(result, 'source_nodes'):
                            span.set_attribute("result.nodes_count", len(result.source_nodes))

                        return result

                    except Exception as e:
                        span.set_attribute("operation.success", False)
                        span.set_attribute("error.message", str(e))
                        span.record_exception(e)
                        raise

            return wrapper
        return decorator

    def create_custom_span(self, span_name, attributes=None):
        """Context manager for custom spans"""
        return self.tracer.start_as_current_span(span_name, attributes=attributes or {})

# Usage
tracer = DistributedTracer()

# Instrument FastAPI app
tracer.instrument_app(app)

# Trace query operations
@tracer.trace_query_operation("rag_query")
def perform_rag_query(query, top_k=5):
    """Traced RAG query operation"""
    # Your query logic here
    result = query_engine.query(query)
    return result

# Custom spans for complex operations
def complex_indexing_operation(documents):
    """Complex operation with detailed tracing"""
    with tracer.create_custom_span("document_processing") as span:
        span.set_attribute("documents.count", len(documents))

        with tracer.create_custom_span("text_extraction") as child_span:
            # Text extraction logic
            texts = [doc.text for doc in documents]
            child_span.set_attribute("extraction.method", "direct")

        with tracer.create_custom_span("embedding_generation") as child_span:
            # Embedding generation
            embeddings = generate_embeddings(texts)
            child_span.set_attribute("embeddings.count", len(embeddings))
            child_span.set_attribute("embeddings.dimension", len(embeddings[0]) if embeddings else 0)

        with tracer.create_custom_span("index_update") as child_span:
            # Index update
            update_index(embeddings, documents)
            child_span.set_attribute("index.operation", "batch_update")

        span.set_attribute("operation.status", "completed")
```

### Custom Metrics and Alerts

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
from prometheus_client import generate_latest, CollectorRegistry
import time
import threading
import psutil
import GPUtil

class AdvancedMetricsCollector:
    def __init__(self, service_name="llamaindex-rag"):
        self.service_name = service_name
        self.registry = CollectorRegistry()

        # Query metrics
        self.query_total = Counter(
            'llamaindex_query_total',
            'Total number of queries',
            ['query_type', 'status', 'model'],
            registry=self.registry
        )

        self.query_duration = Histogram(
            'llamaindex_query_duration_seconds',
            'Query duration distribution',
            ['query_type', 'model'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
            registry=self.registry
        )

        self.query_tokens = Summary(
            'llamaindex_query_tokens_total',
            'Tokens used in queries',
            ['operation', 'model'],
            registry=self.registry
        )

        # Index metrics
        self.index_size = Gauge(
            'llamaindex_index_size',
            'Number of documents/chunks in index',
            ['index_type'],
            registry=self.registry
        )

        self.index_operations = Counter(
            'llamaindex_index_operations_total',
            'Index operations performed',
            ['operation_type', 'status'],
            registry=self.registry
        )

        # Cache metrics
        self.cache_hits = Counter(
            'llamaindex_cache_hits_total',
            'Cache hit operations',
            ['cache_type'],
            registry=self.registry
        )

        self.cache_misses = Counter(
            'llamaindex_cache_misses_total',
            'Cache miss operations',
            ['cache_type'],
            registry=self.registry
        )

        # Resource metrics
        self.memory_usage = Gauge(
            'llamaindex_memory_usage_bytes',
            'Memory usage in bytes',
            ['type'],
            registry=self.registry
        )

        self.gpu_memory_usage = Gauge(
            'llamaindex_gpu_memory_usage_bytes',
            'GPU memory usage in bytes',
            ['device'],
            registry=self.registry
        )

        self.cpu_usage = Gauge(
            'llamaindex_cpu_usage_percent',
            'CPU usage percentage',
            registry=self.registry
        )

        # Custom business metrics
        self.user_satisfaction = Histogram(
            'llamaindex_user_satisfaction_score',
            'User satisfaction scores',
            buckets=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
            registry=self.registry
        )

        self.response_quality = Gauge(
            'llamaindex_response_quality_score',
            'Average response quality score',
            registry=self.registry
        )

        # Start background monitoring
        self._start_background_monitoring()

    def _start_background_monitoring(self):
        """Start background resource monitoring"""
        def monitor_resources():
            while True:
                try:
                    # System resources
                    memory = psutil.virtual_memory()
                    self.memory_usage.labels(type='system').set(memory.used)
                    self.memory_usage.labels(type='available').set(memory.available)
                    self.cpu_usage.set(psutil.cpu_percent(interval=1))

                    # GPU resources
                    try:
                        gpus = GPUtil.getGPUs()
                        for i, gpu in enumerate(gpus):
                            self.gpu_memory_usage.labels(device=f'gpu_{i}').set(
                                gpu.memoryUsed * 1024 * 1024  # Convert to bytes
                            )
                    except:
                        pass  # GPU monitoring not available

                    # Index metrics (if available)
                    try:
                        if 'index' in globals():
                            doc_count = len(index.docstore.docs)
                            self.index_size.labels(index_type='vector').set(doc_count)
                    except:
                        pass

                except Exception as e:
                    print(f"Monitoring error: {e}")

                time.sleep(30)  # Update every 30 seconds

        thread = threading.Thread(target=monitor_resources, daemon=True)
        thread.start()

    def record_query_metrics(self, query_type, model, duration, tokens_used=None, status="success"):
        """Record query-related metrics"""
        self.query_total.labels(
            query_type=query_type,
            status=status,
            model=model
        ).inc()

        self.query_duration.labels(
            query_type=query_type,
            model=model
        ).observe(duration)

        if tokens_used:
            self.query_tokens.labels(
                operation="query",
                model=model
            ).observe(tokens_used)

    def record_cache_metrics(self, cache_type, hit=True):
        """Record cache performance metrics"""
        if hit:
            self.cache_hits.labels(cache_type=cache_type).inc()
        else:
            self.cache_misses.labels(cache_type=cache_type).inc()

    def record_index_operation(self, operation_type, status="success"):
        """Record index operation metrics"""
        self.index_operations.labels(
            operation_type=operation_type,
            status=status
        ).inc()

    def record_user_feedback(self, satisfaction_score, quality_score=None):
        """Record user feedback metrics"""
        self.user_satisfaction.observe(satisfaction_score)

        if quality_score is not None:
            # Update rolling average (simplified)
            current_avg = self.response_quality._value
            if current_avg == 0:
                self.response_quality.set(quality_score)
            else:
                # Simple moving average
                new_avg = (current_avg + quality_score) / 2
                self.response_quality.set(new_avg)

    def get_cache_hit_ratio(self, cache_type):
        """Calculate cache hit ratio"""
        hits = self.cache_hits.labels(cache_type=cache_type)._value
        misses = self.cache_misses.labels(cache_type=cache_type)._value

        total = hits + misses
        return hits / total if total > 0 else 0

    def generate_report(self):
        """Generate comprehensive metrics report"""
        cache_hit_ratio = self.get_cache_hit_ratio("query_cache")

        report = {
            "timestamp": time.time(),
            "cache_performance": {
                "hit_ratio": cache_hit_ratio,
                "total_requests": self.cache_hits._value + self.cache_misses._value
            },
            "system_resources": {
                "memory_usage_mb": self.memory_usage.labels(type='system')._value / (1024 * 1024),
                "cpu_usage_percent": self.cpu_usage._value
            },
            "query_performance": {
                "total_queries": self.query_total._value,
                "avg_duration": self.query_duration._sum / self.query_total._value if self.query_total._value > 0 else 0
            }
        }

        return report

    def start_metrics_server(self, port=8001):
        """Start Prometheus metrics server"""
        start_http_server(port, registry=self.registry)
        print(f"Metrics server started on port {port}")

# Usage
metrics = AdvancedMetricsCollector()

# Record metrics in query endpoint
@app.post("/query")
@tracer.trace_query_operation("api_query")
async def query_endpoint(request: QueryRequest):
    start_time = time.time()

    try:
        # Your query logic
        result = await perform_query(request)

        # Record success metrics
        duration = time.time() - start_time
        metrics.record_query_metrics(
            query_type="rag_query",
            model="gpt-4",
            duration=duration,
            tokens_used=getattr(result, 'tokens_used', None),
            status="success"
        )

        return result

    except Exception as e:
        # Record error metrics
        duration = time.time() - start_time
        metrics.record_query_metrics(
            query_type="rag_query",
            model="gpt-4",
            duration=duration,
            status="error"
        )
        raise

# User feedback endpoint
@app.post("/feedback")
async def submit_feedback(feedback: dict):
    """Collect user feedback"""
    satisfaction = feedback.get("satisfaction", 0.5)
    quality = feedback.get("quality", None)

    metrics.record_user_feedback(satisfaction, quality)

    return {"status": "feedback recorded"}

# Metrics endpoint
@app.get("/advanced-metrics")
async def get_advanced_metrics():
    """Get comprehensive metrics report"""
    report = metrics.generate_report()
    return report
```

## 🚀 Advanced Caching Strategies

### Multi-Level Caching

```python
# caching.py
from cachetools import TTLCache, LRUCache
from diskcache import Cache as DiskCache
import hashlib
import json
import asyncio
from typing import Any, Optional

class MultiLevelCache:
    """Multi-level caching system with L1, L2, and disk caching"""

    def __init__(self, l1_ttl=300, l2_maxsize=10000, disk_cache_dir="./cache"):
        # L1: Fast in-memory cache with TTL
        self.l1_cache = TTLCache(maxsize=1000, ttl=l1_ttl)

        # L2: Larger in-memory cache with LRU eviction
        self.l2_cache = LRUCache(maxsize=l2_maxsize)

        # L3: Disk-based persistent cache
        self.disk_cache = DiskCache(disk_cache_dir)

        # Cache statistics
        self.stats = {
            "l1_hits": 0, "l1_misses": 0,
            "l2_hits": 0, "l2_misses": 0,
            "disk_hits": 0, "disk_misses": 0
        }

    def generate_key(self, *args, **kwargs) -> str:
        """Generate deterministic cache key"""
        # Convert args and kwargs to sorted string
        cache_data = {
            "args": args,
            "kwargs": dict(sorted(kwargs.items()))
        }
        cache_str = json.dumps(cache_data, sort_keys=True, default=str)
        return hashlib.md5(cache_str.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from multi-level cache"""

        # Check L1 cache
        if key in self.l1_cache:
            self.stats["l1_hits"] += 1
            return self.l1_cache[key]

        self.stats["l1_misses"] += 1

        # Check L2 cache
        if key in self.l2_cache:
            self.stats["l2_hits"] += 1
            # Promote to L1
            value = self.l2_cache[key]
            self.l1_cache[key] = value
            return value

        self.stats["l2_misses"] += 1

        # Check disk cache
        try:
            value = self.disk_cache.get(key)
            if value is not None:
                self.stats["disk_hits"] += 1
                # Promote to higher levels
                self.l2_cache[key] = value
                self.l1_cache[key] = value
                return value
        except Exception:
            pass

        self.stats["disk_misses"] += 1
        return None

    async def set(self, key: str, value: Any, persist_to_disk: bool = True):
        """Set value in multi-level cache"""

        # Always set in L1 and L2
        self.l1_cache[key] = value
        self.l2_cache[key] = value

        # Optionally persist to disk
        if persist_to_disk:
            try:
                self.disk_cache[key] = value
            except Exception as e:
                print(f"Disk cache write error: {e}")

    async def get_or_compute(self, key: str, compute_func, persist_to_disk: bool = True):
        """Get from cache or compute and cache"""

        # Try to get from cache
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value, True  # Return cached value and hit flag

        # Compute value
        value = await compute_func()

        # Cache the result
        await self.set(key, value, persist_to_disk)

        return value, False  # Return computed value and miss flag

    def get_cache_stats(self):
        """Get cache performance statistics"""
        total_requests = sum(self.stats.values())

        return {
            "total_requests": total_requests,
            "l1_hit_rate": self.stats["l1_hits"] / (self.stats["l1_hits"] + self.stats["l1_misses"]) if (self.stats["l1_hits"] + self.stats["l1_misses"]) > 0 else 0,
            "l2_hit_rate": self.stats["l2_hits"] / (self.stats["l2_hits"] + self.stats["l2_misses"]) if (self.stats["l2_hits"] + self.stats["l2_misses"]) > 0 else 0,
            "disk_hit_rate": self.stats["disk_hits"] / (self.stats["disk_hits"] + self.stats["disk_misses"]) if (self.stats["disk_hits"] + self.stats["disk_misses"]) > 0 else 0,
            "overall_hit_rate": (self.stats["l1_hits"] + self.stats["l2_hits"] + self.stats["disk_hits"]) / total_requests if total_requests > 0 else 0,
            "raw_stats": self.stats.copy()
        }

    def clear_cache(self, level: str = "all"):
        """Clear cache at specified level"""

        if level in ["all", "l1"]:
            self.l1_cache.clear()

        if level in ["all", "l2"]:
            self.l2_cache.clear()

        if level in ["all", "disk"]:
            self.disk_cache.clear()

    def warmup_cache(self, common_queries: list, compute_func):
        """Warm up cache with common queries"""

        async def warmup():
            tasks = []
            for query in common_queries:
                key = self.generate_key(query)
                task = self.get_or_compute(key, lambda q=query: compute_func(q), persist_to_disk=True)
                tasks.append(task)

            await asyncio.gather(*tasks)

        asyncio.run(warmup())
        print(f"Cache warmed up with {len(common_queries)} queries")

# Usage
cache = MultiLevelCache()

# Cache query results
async def cached_rag_query(query: str):
    """Perform cached RAG query"""
    cache_key = cache.generate_key("rag_query", query=query, top_k=5)

    async def compute_query():
        # Your actual query computation
        result = await perform_rag_query(query)
        return result

    result, was_cached = await cache.get_or_compute(cache_key, compute_query)

    if was_cached:
        print(f"Cache hit for query: {query}")
    else:
        print(f"Cache miss for query: {query}")

    return result

# Get cache statistics
stats = cache.get_cache_stats()
print(f"Overall cache hit rate: {stats['overall_hit_rate']:.3f}")

# Warm up cache with common queries
common_queries = [
    "What is machine learning?",
    "How do neural networks work?",
    "Explain AI concepts"
]

cache.warmup_cache(common_queries, lambda q: perform_rag_query(q))
```

### Semantic Caching

```python
# semantic_cache.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

class SemanticCache:
    """Semantic caching based on query similarity"""

    def __init__(self, embedding_model="all-MiniLM-L6-v2", similarity_threshold=0.85):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.similarity_threshold = similarity_threshold
        self.cache = {}  # {query_hash: {"embedding": [...], "response": ..., "query": ...}}

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        return self.embedding_model.encode(text, convert_to_numpy=True)

    def find_similar_query(self, query: str) -> Optional[dict]:
        """Find semantically similar cached query"""

        if not self.cache:
            return None

        # Generate embedding for current query
        query_embedding = self.generate_embedding(query)

        # Find most similar cached query
        best_match = None
        best_similarity = 0

        for cache_item in self.cache.values():
            similarity = cosine_similarity(
                [query_embedding],
                [cache_item["embedding"]]
            )[0][0]

            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match = cache_item

        return best_match if best_match else None

    def get(self, query: str) -> Optional[Any]:
        """Get cached response for similar query"""

        similar_item = self.find_similar_query(query)

        if similar_item:
            print(f"Semantic cache hit (similarity: {self.calculate_similarity(query, similar_item['query']):.3f})")
            return similar_item["response"]

        return None

    def set(self, query: str, response: Any):
        """Cache query response"""

        query_embedding = self.generate_embedding(query)

        # Create cache key (simple hash for management)
        cache_key = hash(query) % 10000

        self.cache[cache_key] = {
            "query": query,
            "embedding": query_embedding,
            "response": response,
            "timestamp": time.time()
        }

    def calculate_similarity(self, query1: str, query2: str) -> float:
        """Calculate semantic similarity between two queries"""
        emb1 = self.generate_embedding(query1)
        emb2 = self.generate_embedding(query2)

        return cosine_similarity([emb1], [emb2])[0][0]

    def get_cache_stats(self):
        """Get semantic cache statistics"""
        if not self.cache:
            return {"total_entries": 0}

        similarities = []
        for item in self.cache.values():
            # Calculate similarity to other cached queries (sample)
            other_items = [i for i in self.cache.values() if i != item][:5]  # Sample 5 others
            for other in other_items:
                sim = cosine_similarity([item["embedding"]], [other["embedding"]])[0][0]
                similarities.append(sim)

        return {
            "total_entries": len(self.cache),
            "avg_similarity": np.mean(similarities) if similarities else 0,
            "similarity_std": np.std(similarities) if similarities else 0,
            "similarity_threshold": self.similarity_threshold
        }

    def cleanup_old_entries(self, max_age_hours: int = 24):
        """Remove old cache entries"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600

        keys_to_remove = [
            key for key, item in self.cache.items()
            if current_time - item["timestamp"] > max_age_seconds
        ]

        for key in keys_to_remove:
            del self.cache[key]

        print(f"Cleaned up {len(keys_to_remove)} old cache entries")

# Usage
semantic_cache = SemanticCache(similarity_threshold=0.8)

def semantically_cached_query(query: str):
    """Perform semantically cached query"""

    # Check semantic cache
    cached_response = semantic_cache.get(query)

    if cached_response:
        return cached_response, True  # Return cached response

    # Perform actual query
    response = perform_rag_query(query)

    # Cache the response
    semantic_cache.set(query, response)

    return response, False  # Return fresh response

# Test semantic caching
queries = [
    "What is machine learning?",
    "Explain machine learning",  # Should match first query semantically
    "How do neural networks work?",  # Different topic
    "Tell me about machine learning algorithms"  # Should match first query
]

for query in queries:
    response, was_cached = semantically_cached_query(query)
    print(f"Query: '{query}' -> {'Cached' if was_cached else 'Fresh'}")

# Get cache statistics
stats = semantic_cache.get_cache_stats()
print(f"Cache stats: {stats}")
```

## ⚡ Performance Optimization

### GPU Acceleration and Optimization

```python
# gpu_optimization.py
import torch
from transformers import AutoTokenizer, AutoModel
import psutil
import GPUtil
from concurrent.futures import ThreadPoolExecutor
import asyncio

class GPUOptimizer:
    """GPU optimization and acceleration for LlamaIndex operations"""

    def __init__(self, device="auto"):
        self.device = self._setup_device(device)
        self.executor = ThreadPoolExecutor(max_workers=4)

        # GPU memory management
        self.memory_stats = {}

    def _setup_device(self, device):
        """Setup optimal device configuration"""
        if device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                torch.cuda.empty_cache()  # Clear any existing cache
            elif torch.backends.mps.is_available():
                device = "mps"  # Apple Silicon
            else:
                device = "cpu"

        print(f"Using device: {device}")
        return device

    def optimize_model_for_gpu(self, model):
        """Optimize model for GPU inference"""

        if self.device == "cuda":
            # Move model to GPU
            model = model.to(self.device)

            # Enable CUDA optimizations
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.enabled = True

            # Use mixed precision if supported
            if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 7:
                model = model.half()  # Convert to FP16

        elif self.device == "mps":
            # Apple Silicon optimizations
            model = model.to(self.device)

        return model

    async def batch_process_embeddings(self, texts: list, model_name="sentence-transformers/all-MiniLM-L6-v2", batch_size=32):
        """Batch process embeddings with GPU acceleration"""

        from sentence_transformers import SentenceTransformer

        # Load model on optimal device
        model = SentenceTransformer(model_name, device=self.device)

        # Process in batches
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]

            # Process batch
            loop = asyncio.get_running_loop()
            batch_embeddings = await loop.run_in_executor(
                self.executor,
                model.encode,
                batch_texts
            )

            all_embeddings.extend(batch_embeddings)

            # GPU memory management
            if self.device == "cuda":
                torch.cuda.empty_cache()

        return all_embeddings

    def monitor_gpu_usage(self):
        """Monitor GPU usage and memory"""

        gpu_stats = {}

        try:
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                gpu_stats[f"gpu_{i}"] = {
                    "name": gpu.name,
                    "memory_used": gpu.memoryUsed,
                    "memory_total": gpu.memoryTotal,
                    "memory_free": gpu.memoryFree,
                    "memory_utilization": gpu.memoryUtil,
                    "gpu_utilization": gpu.load * 100
                }

        except Exception as e:
            gpu_stats["error"] = str(e)

        return gpu_stats

    def optimize_batch_size(self, model, sample_texts, target_memory_usage=0.8):
        """Dynamically optimize batch size based on GPU memory"""

        if self.device != "cuda":
            return 16  # Default batch size for CPU

        # Start with small batch size
        batch_size = 1
        max_batch_size = 128

        while batch_size <= max_batch_size:
            try:
                # Test batch processing
                test_batch = sample_texts[:batch_size]

                # Load model and test
                from sentence_transformers import SentenceTransformer
                test_model = SentenceTransformer("all-MiniLM-L6-v2", device=self.device)

                # Process test batch
                embeddings = test_model.encode(test_batch)

                # Check memory usage
                memory_info = torch.cuda.mem_get_info()
                memory_used = 1 - (memory_info[0] / memory_info[1])  # Free / Total

                if memory_used > target_memory_usage:
                    # Too much memory usage, reduce batch size
                    batch_size = max(1, batch_size // 2)
                    break

                # Clean up
                del embeddings
                torch.cuda.empty_cache()

                # Try larger batch size
                batch_size *= 2

            except RuntimeError as e:
                if "out of memory" in str(e).lower():
                    batch_size = max(1, batch_size // 2)
                    break
                else:
                    raise e

        optimal_batch_size = min(batch_size, max_batch_size)
        print(f"Optimal batch size: {optimal_batch_size}")

        return optimal_batch_size

    async def parallel_gpu_inference(self, queries: list, model):
        """Perform parallel GPU inference"""

        # Split queries into batches for parallel processing
        batch_size = len(queries) // torch.cuda.device_count() if torch.cuda.is_available() else len(queries)

        async def process_batch(batch_queries):
            """Process a batch of queries"""
            loop = asyncio.get_running_loop()

            results = await loop.run_in_executor(
                self.executor,
                lambda: [model.generate_text(q) for q in batch_queries]
            )

            return results

        # Process batches in parallel
        batches = [queries[i:i + batch_size] for i in range(0, len(queries), batch_size)]
        tasks = [process_batch(batch) for batch in batches]

        batch_results = await asyncio.gather(*tasks)

        # Flatten results
        all_results = [item for sublist in batch_results for item in sublist]

        return all_results

# Usage
gpu_optimizer = GPUOptimizer()

# Optimize model for GPU
optimized_model = gpu_optimizer.optimize_model_for_gpu(base_model)

# Batch process embeddings
texts = ["Text 1", "Text 2", "Text 3"] * 100  # 300 texts
embeddings = await gpu_optimizer.batch_process_embeddings(texts, batch_size=32)

# Monitor GPU usage
gpu_stats = gpu_optimizer.monitor_gpu_usage()
print(f"GPU Stats: {gpu_stats}")

# Optimize batch size
optimal_batch_size = gpu_optimizer.optimize_batch_size(
    model=None,  # Would pass actual model
    sample_texts=texts[:10]
)

print(f"Optimal batch size determined: {optimal_batch_size}")
```

### Query Optimization Strategies

```python
# query_optimization.py
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.postprocessor import (
    SimilarityPostprocessor,
    KeywordNodePostprocessor,
    MetadataReplacementPostprocessor
)
import re

class QueryOptimizer:
    """Advanced query optimization strategies"""

    def __init__(self):
        self.hyde_transform = HyDEQueryTransform(include_original=True)
        self.optimization_stats = {}

    def optimize_query(self, query: str, optimization_level="standard"):
        """Apply comprehensive query optimization"""

        optimized = {
            "original_query": query,
            "optimizations_applied": []
        }

        # Basic text cleaning
        cleaned_query = self._clean_query_text(query)
        if cleaned_query != query:
            optimized["cleaned_query"] = cleaned_query
            optimized["optimizations_applied"].append("text_cleaning")

        # Query expansion
        if optimization_level in ["standard", "advanced"]:
            expanded_query = self._expand_query(cleaned_query)
            if expanded_query != cleaned_query:
                optimized["expanded_query"] = expanded_query
                optimized["optimizations_applied"].append("query_expansion")

        # Intent classification
        intent = self._classify_query_intent(cleaned_query)
        optimized["detected_intent"] = intent
        optimized["optimizations_applied"].append("intent_classification")

        # Generate HyDE query if appropriate
        if intent in ["explanatory", "comparative"] and optimization_level == "advanced":
            hyde_query = self._generate_hyde_query(cleaned_query)
            optimized["hyde_query"] = hyde_query
            optimized["optimizations_applied"].append("hyde_enhancement")

        # Final optimized query selection
        final_query = optimized.get("hyde_query") or \
                     optimized.get("expanded_query") or \
                     optimized.get("cleaned_query") or \
                     query

        optimized["final_query"] = final_query
        optimized["optimization_level"] = optimization_level

        return optimized

    def _clean_query_text(self, query: str) -> str:
        """Clean and normalize query text"""

        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', query.strip())

        # Fix common typos and abbreviations
        replacements = {
            r'\b(ml|ML)\b': 'machine learning',
            r'\bai\b': 'artificial intelligence',
            r'\bnn\b': 'neural network',
            r'\bapi\b': 'API'
        }

        for pattern, replacement in replacements.items():
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

        return cleaned

    def _expand_query(self, query: str) -> str:
        """Expand query with related terms"""

        expansion_rules = {
            "machine learning": ["algorithms", "data science", "AI"],
            "neural network": ["deep learning", "artificial neural network", "neurons"],
            "artificial intelligence": ["AI", "machine learning", "automation"],
            "data science": ["analytics", "statistics", "machine learning"]
        }

        expanded_terms = []
        query_lower = query.lower()

        for key, terms in expansion_rules.items():
            if key in query_lower:
                # Add 1-2 most relevant terms
                expanded_terms.extend(terms[:2])
                break  # Only expand with one category

        if expanded_terms:
            return f"{query} {' '.join(expanded_terms)}"

        return query

    def _classify_query_intent(self, query: str) -> str:
        """Classify query intent"""

        query_lower = query.lower()

        # Intent patterns
        intents = {
            "factual": ["what is", "how does", "explain", "describe"],
            "comparative": ["compare", "versus", "vs", "difference between"],
            "procedural": ["how to", "steps to", "guide for"],
            "analytical": ["why", "analyze", "evaluate", "assess"],
            "explanatory": ["explain", "meaning of", "what does"]
        }

        for intent, patterns in intents.items():
            if any(pattern in query_lower for pattern in patterns):
                return intent

        return "general"

    def _generate_hyde_query(self, query: str) -> str:
        """Generate hypothetical document embedding query"""
        # This would integrate with HyDE transform
        # Simplified version for demonstration
        hyde_prompt = f"Generate a detailed answer that would be relevant to this question: {query}"

        # In practice, this would use the HyDE transform
        return f"{query} [HyDE enhanced]"

    def create_optimized_postprocessors(self, intent: str):
        """Create optimized post-processing pipeline based on intent"""

        postprocessors = []

        # Base similarity filter
        postprocessors.append(SimilarityPostprocessor(similarity_cutoff=0.7))

        # Intent-specific processors
        if intent == "factual":
            # For factual queries, prioritize exact matches
            postprocessors.append(
                KeywordNodePostprocessor(
                    required_keywords=["definition", "meaning", "explanation"],
                    exclude_keywords=["opinion", "speculation"]
                )
            )

        elif intent == "comparative":
            # For comparisons, include diverse perspectives
            postprocessors.append(
                MetadataReplacementPostprocessor(
                    target_metadata_key="category",
                    new_content_template="Comparison point: {content}"
                )
            )

        elif intent == "procedural":
            # For how-to queries, prioritize step-by-step content
            postprocessors.append(
                KeywordNodePostprocessor(
                    required_keywords=["step", "guide", "tutorial", "process"],
                    mode="OR"
                )
            )

        return postprocessors

    def optimize_index_for_query(self, query: str, index):
        """Optimize index retrieval strategy for specific query"""

        intent = self._classify_query_intent(query)

        # Adjust retrieval parameters based on intent
        if intent == "factual":
            # Precise retrieval for factual queries
            retriever = index.as_retriever(
                similarity_top_k=5,
                vector_store_query_mode="default"
            )

        elif intent == "comparative":
            # Broader retrieval for comparative queries
            retriever = index.as_retriever(
                similarity_top_k=10,
                vector_store_query_mode="hybrid"
            )

        elif intent == "general":
            # Balanced retrieval for general queries
            retriever = index.as_retriever(
                similarity_top_k=7,
                vector_store_query_mode="default"
            )

        else:
            # Default retrieval
            retriever = index.as_retriever(similarity_top_k=5)

        return retriever, intent

# Usage
query_optimizer = QueryOptimizer()

# Optimize a query
query = "how do neural networks learn?"
optimized = query_optimizer.optimize_query(query, optimization_level="advanced")

print("Query Optimization Results:")
for key, value in optimized.items():
    print(f"{key}: {value}")

# Create optimized post-processors
postprocessors = query_optimizer.create_optimized_postprocessors(optimized["detected_intent"])

# Optimize index for query
retriever, intent = query_optimizer.optimize_index_for_query(query, vector_index)

print(f"Using {len(postprocessors)} post-processors for {intent} query")
```

## 🎯 Production Optimization Checklist

### Performance Benchmarks

```python
# benchmark_final.py
import time
import statistics
import asyncio
from typing import Dict, List, Any

class ProductionBenchmarker:
    """Comprehensive benchmarking for production RAG systems"""

    def __init__(self):
        self.baseline_metrics = {}

    async def comprehensive_benchmark(self, system_configs: Dict[str, Any], test_queries: List[str]):
        """Run comprehensive benchmark across different configurations"""

        results = {}

        for config_name, config in system_configs.items():
            print(f"Benchmarking configuration: {config_name}")

            # Setup system with configuration
            system = await self._setup_system(config)

            # Run benchmarks
            config_results = await self._run_full_benchmark(system, test_queries)

            results[config_name] = config_results

            # Cleanup
            await self._cleanup_system(system)

        # Generate comparison report
        comparison = self._generate_comparison_report(results)

        return results, comparison

    async def _setup_system(self, config: Dict[str, Any]):
        """Setup system with specific configuration"""
        # This would initialize your RAG system with specific settings
        system = {
            "index": config.get("index"),
            "retriever": config.get("retriever"),
            "generator": config.get("generator"),
            "cache": config.get("cache"),
            "optimizations": config.get("optimizations", [])
        }

        return system

    async def _run_full_benchmark(self, system, test_queries: List[str]):
        """Run complete benchmark suite"""

        results = {
            "latency": await self._benchmark_latency(system, test_queries),
            "throughput": await self._benchmark_throughput(system, test_queries),
            "accuracy": await self._benchmark_accuracy(system, test_queries),
            "resource_usage": await self._benchmark_resources(system, test_queries),
            "scalability": await self._benchmark_scalability(system)
        }

        return results

    async def _benchmark_latency(self, system, queries: List[str]):
        """Benchmark query latency"""

        latencies = []

        for query in queries:
            start_time = time.time()

            # Execute query
            result = await self._execute_query(system, query)

            latency = time.time() - start_time
            latencies.append(latency)

        return {
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "p95": sorted(latencies)[int(len(latencies) * 0.95)],
            "p99": sorted(latencies)[int(len(latencies) * 0.99)],
            "min": min(latencies),
            "max": max(latencies)
        }

    async def _benchmark_throughput(self, system, queries: List[str]):
        """Benchmark system throughput"""

        # Test different concurrency levels
        concurrency_levels = [1, 5, 10, 20]

        throughput_results = {}

        for concurrency in concurrency_levels:
            start_time = time.time()

            # Run queries concurrently
            tasks = []
            for i in range(min(len(queries) * 2, 100)):  # Repeat queries if needed
                query = queries[i % len(queries)]
                tasks.append(self._execute_query(system, query))

            await asyncio.gather(*tasks)

            total_time = time.time() - start_time
            throughput = len(tasks) / total_time

            throughput_results[concurrency] = {
                "queries_per_second": throughput,
                "total_queries": len(tasks),
                "total_time": total_time
            }

        return throughput_results

    async def _benchmark_accuracy(self, system, queries: List[str]):
        """Benchmark answer accuracy"""

        accuracy_scores = []

        for query in queries:
            result = await self._execute_query(system, query)

            # Calculate accuracy (simplified - would use proper evaluation)
            accuracy = self._calculate_answer_accuracy(result, query)
            accuracy_scores.append(accuracy)

        return {
            "mean_accuracy": statistics.mean(accuracy_scores),
            "accuracy_distribution": self._calculate_distribution(accuracy_scores)
        }

    async def _benchmark_resources(self, system, queries: List[str]):
        """Benchmark resource usage"""

        import psutil
        process = psutil.Process()

        # Baseline measurements
        baseline_cpu = psutil.cpu_percent()
        baseline_memory = process.memory_info().rss

        # Execute queries
        for query in queries:
            await self._execute_query(system, query)

        # Peak measurements
        peak_cpu = psutil.cpu_percent()
        peak_memory = process.memory_info().rss

        return {
            "cpu_usage_percent": peak_cpu - baseline_cpu,
            "memory_usage_mb": (peak_memory - baseline_memory) / (1024 * 1024),
            "baseline_cpu": baseline_cpu,
            "baseline_memory_mb": baseline_memory / (1024 * 1024)
        }

    async def _benchmark_scalability(self, system):
        """Benchmark system scalability"""

        # Test with increasing data sizes
        data_sizes = [100, 500, 1000, 5000]

        scalability_results = {}

        for size in data_sizes:
            # Create index with specific size
            test_index = await self._create_test_index(size)

            # Benchmark performance
            test_queries = [f"test query {i}" for i in range(10)]
            latency_results = await self._benchmark_latency({"index": test_index}, test_queries)

            scalability_results[size] = {
                "latency": latency_results,
                "index_size": size
            }

        return scalability_results

    async def _execute_query(self, system, query: str):
        """Execute a single query"""
        # Implement your query execution logic
        return {"response": f"Mock response for: {query}"}

    def _calculate_answer_accuracy(self, result, query):
        """Calculate answer accuracy (placeholder)"""
        # This would implement proper accuracy calculation
        return 0.85  # Mock accuracy score

    def _calculate_distribution(self, scores):
        """Calculate score distribution"""
        return {
            "excellent": len([s for s in scores if s >= 0.9]),
            "good": len([s for s in scores if 0.7 <= s < 0.9]),
            "fair": len([s for s in scores if 0.5 <= s < 0.7]),
            "poor": len([s for s in scores if s < 0.5])
        }

    async def _create_test_index(self, size: int):
        """Create test index of specific size"""
        # Implement test index creation
        return {"size": size}

    async def _cleanup_system(self, system):
        """Cleanup system resources"""
        pass

    def _generate_comparison_report(self, results):
        """Generate comparison report across configurations"""

        comparison = {
            "best_latency": min(results.keys(), key=lambda k: results[k]["latency"]["mean"]),
            "best_throughput": max(results.keys(), key=lambda k: results[k]["throughput"][10]["queries_per_second"]),
            "best_accuracy": max(results.keys(), key=lambda k: results[k]["accuracy"]["mean_accuracy"]),
            "efficiency_scores": {}
        }

        # Calculate efficiency scores (accuracy / latency)
        for config, metrics in results.items():
            efficiency = metrics["accuracy"]["mean_accuracy"] / metrics["latency"]["mean"]
            comparison["efficiency_scores"][config] = efficiency

        comparison["most_efficient"] = max(comparison["efficiency_scores"].keys(),
                                         key=lambda k: comparison["efficiency_scores"][k])

        return comparison

# Usage
benchmarker = ProductionBenchmarker()

# Define system configurations to test
system_configs = {
    "baseline": {
        "index": "vector_index",
        "retriever": "basic",
        "cache": False,
        "optimizations": []
    },
    "optimized": {
        "index": "vector_index",
        "retriever": "advanced",
        "cache": True,
        "optimizations": ["gpu_acceleration", "batch_processing"]
    },
    "enterprise": {
        "index": "distributed_index",
        "retriever": "ensemble",
        "cache": True,
        "optimizations": ["gpu_acceleration", "distributed_processing", "advanced_cache"]
    }
}

# Test queries
test_queries = [
    "What is machine learning?",
    "How do neural networks work?",
    "Explain the difference between AI and machine learning",
    "What are the applications of deep learning?"
] * 5  # 20 queries total

# Run comprehensive benchmark
results, comparison = await benchmarker.comprehensive_benchmark(system_configs, test_queries)

print("Benchmark Results Summary:")
for config, metrics in results.items():
    print(f"\n{config.upper()}:")
    print(f"  Latency (p95): {metrics['latency']['p95']:.3f}s")
    print(f"  Throughput: {metrics['throughput'][10]['queries_per_second']:.1f} qps")
    print(f"  Accuracy: {metrics['accuracy']['mean_accuracy']:.3f}")

print(f"\nBest Configuration: {comparison['most_efficient']}")
```

## 🎉 Congratulations!

You've mastered advanced monitoring and optimization for LlamaIndex RAG systems! 🎉

### Key Achievements

✅ **Distributed Tracing**: OpenTelemetry integration for request tracking
✅ **Advanced Metrics**: Custom Prometheus metrics and business KPIs
✅ **Multi-Level Caching**: L1/L2/disk caching with semantic similarity
✅ **GPU Optimization**: CUDA acceleration and memory management
✅ **Query Optimization**: Intent classification and dynamic strategies
✅ **Production Benchmarking**: Comprehensive performance evaluation

### Production-Ready Capabilities

- **Full Observability**: End-to-end tracing and comprehensive monitoring
- **Intelligent Caching**: Multi-level caching with semantic understanding
- **GPU Acceleration**: Optimized inference with automatic batching
- **Dynamic Optimization**: Query-aware performance tuning
- **Enterprise Benchmarking**: Production-grade performance evaluation

### Your RAG System is Now:

🚀 **High-Performance**: GPU-accelerated with intelligent caching  
📊 **Fully Monitored**: Complete observability with distributed tracing  
⚡ **Auto-Optimized**: Dynamic query optimization and resource management  
🏢 **Production-Ready**: Enterprise-grade reliability and scalability  
🎯 **Intelligent**: Context-aware processing with advanced RAG patterns  

*You've built a world-class RAG system that can handle enterprise workloads with confidence! The monitoring and optimization techniques you've implemented ensure your system will perform reliably at scale while continuously improving through intelligent caching and dynamic optimization.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `query`, `cache` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Monitoring & Optimization` as an operating subsystem inside **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `queries`, `metrics`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Monitoring & Optimization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `query` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `cache`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/run-llama/llama_index)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `query` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Production Deployment](07-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
