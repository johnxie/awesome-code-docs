---
layout: default
title: "DSPy Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: DSPy Tutorial
---

# Chapter 8: Production Deployment - Scaling DSPy Systems

> Deploy optimized DSPy programs to production with proper scaling, monitoring, and operational best practices.

## Overview

Production deployment requires careful consideration of performance, reliability, cost, and maintenance. DSPy programs need robust infrastructure to handle real-world workloads while maintaining the quality improvements achieved through optimization.

## Model Selection and Optimization for Production

### Cost-Effective Model Selection

```python
import dspy

# Define models with different cost/performance profiles
model_configs = {
    "gpt-4": {
        "model": "gpt-4",
        "cost_per_1k_tokens": 0.03,  # Input cost
        "quality_score": 0.95,
        "latency_ms": 2000
    },
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo",
        "cost_per_1k_tokens": 0.002,
        "quality_score": 0.85,
        "latency_ms": 800
    },
    "claude-3-haiku": {
        "model": "claude-3-haiku-20240307",
        "cost_per_1k_tokens": 0.00025,
        "quality_score": 0.82,
        "latency_ms": 600
    }
}

class CostOptimizedDSPy:
    def __init__(self, model_configs):
        self.model_configs = model_configs
        self.models = {}

        # Initialize models
        for name, config in model_configs.items():
            if name.startswith("gpt"):
                self.models[name] = dspy.OpenAI(model=config["model"])
            elif name.startswith("claude"):
                self.models[name] = dspy.Claude(model=config["model"])

    def select_model(self, task_complexity, budget_constraint=None):
        """Select optimal model based on requirements"""

        candidates = []

        for name, config in self.model_configs.items():
            # Filter by quality requirements
            if task_complexity == "high" and config["quality_score"] < 0.9:
                continue
            elif task_complexity == "medium" and config["quality_score"] < 0.8:
                continue

            # Filter by budget if specified
            if budget_constraint and config["cost_per_1k_tokens"] > budget_constraint:
                continue

            candidates.append((name, config))

        if not candidates:
            return "gpt-3.5-turbo"  # Fallback

        # Select best candidate (highest quality within constraints)
        best_candidate = max(candidates, key=lambda x: x[1]["quality_score"])
        return best_candidate[0]

    def get_model(self, model_name):
        """Get configured model instance"""
        return self.models.get(model_name)

# Usage
cost_optimizer = CostOptimizedDSPy(model_configs)

# Select model for different scenarios
high_quality_model = cost_optimizer.select_model("high")
budget_model = cost_optimizer.select_model("medium", budget_constraint=0.005)

print(f"High quality: {high_quality_model}")
print(f"Budget constrained: {budget_model}")
```

### Model Routing and Fallback

```python
class ModelRouter:
    def __init__(self, primary_model, fallback_models):
        self.primary_model = primary_model
        self.fallback_models = fallback_models
        self.failure_counts = {model: 0 for model in [primary_model] + fallback_models}

    async def execute_with_fallback(self, program_func, *args, **kwargs):
        """Execute with automatic fallback on failures"""

        models_to_try = [self.primary_model] + self.fallback_models

        for model_name in models_to_try:
            try:
                # Configure DSPy with current model
                model = self.get_model(model_name)
                dspy.settings.configure(lm=model)

                # Execute program
                result = await program_func(*args, **kwargs)

                # Reset failure count on success
                self.failure_counts[model_name] = 0

                return result, model_name

            except Exception as e:
                # Increment failure count
                self.failure_counts[model_name] += 1

                print(f"Model {model_name} failed: {e}")

                # If this is the last model, re-raise the exception
                if model_name == models_to_try[-1]:
                    raise e

                continue

    def get_model(self, model_name):
        """Get model instance by name"""
        # This would integrate with your CostOptimizedDSPy
        return cost_optimizer.get_model(model_name)

    def get_health_status(self):
        """Get health status of all models"""
        return {
            model: {
                "failure_count": count,
                "healthy": count < 5  # Consider unhealthy after 5 failures
            }
            for model, count in self.failure_counts.items()
        }

# Usage
router = ModelRouter(
    primary_model="gpt-4",
    fallback_models=["gpt-3.5-turbo", "claude-3-haiku"]
)

# Define program function
async def run_qa(question):
    qa_program = dspy.Predict(BasicQA)
    return qa_program(question=question)

# Execute with automatic fallback
result, used_model = await router.execute_with_fallback(run_qa, "What is AI?")
print(f"Result: {result.answer}, Used model: {used_model}")
```

## Caching and Performance Optimization

### Multi-Level Caching

```python
import asyncio
import hashlib
import json
from typing import Dict, Any
import time

class MultiLevelCache:
    def __init__(self, redis_client=None, local_cache_size=1000):
        self.redis = redis_client
        self.local_cache = {}
        self.local_cache_size = local_cache_size
        self.stats = {"hits": 0, "misses": 0, "redis_hits": 0, "local_hits": 0}

    def _get_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate deterministic cache key"""
        key_data = {
            "func": func_name,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    async def get(self, func_name: str, args: tuple, kwargs: dict) -> Any:
        """Get from cache with fallback"""
        cache_key = self._get_cache_key(func_name, args, kwargs)

        # Check local cache first
        if cache_key in self.local_cache:
            entry = self.local_cache[cache_key]
            if time.time() - entry["timestamp"] < entry["ttl"]:
                self.stats["hits"] += 1
                self.stats["local_hits"] += 1
                return entry["value"]

        # Check Redis cache
        if self.redis:
            try:
                redis_data = await self.redis.get(cache_key)
                if redis_data:
                    data = json.loads(redis_data)
                    if time.time() - data["timestamp"] < data["ttl"]:
                        # Update local cache
                        self.local_cache[cache_key] = data
                        self._evict_if_needed()

                        self.stats["hits"] += 1
                        self.stats["redis_hits"] += 1
                        return data["value"]
            except Exception as e:
                print(f"Redis cache error: {e}")

        self.stats["misses"] += 1
        return None

    async def set(self, func_name: str, args: tuple, kwargs: dict, value: Any, ttl: int = 3600):
        """Set in cache"""
        cache_key = self._get_cache_key(func_name, args, kwargs)

        cache_entry = {
            "value": value,
            "timestamp": time.time(),
            "ttl": ttl
        }

        # Set in local cache
        self.local_cache[cache_key] = cache_entry
        self._evict_if_needed()

        # Set in Redis if available
        if self.redis:
            try:
                await self.redis.set(cache_key, json.dumps(cache_entry), ex=ttl)
            except Exception as e:
                print(f"Redis cache set error: {e}")

    def _evict_if_needed(self):
        """Evict old entries if cache is full"""
        if len(self.local_cache) > self.local_cache_size:
            # Remove oldest entries (simple LRU)
            sorted_entries = sorted(
                self.local_cache.items(),
                key=lambda x: x[1]["timestamp"]
            )
            to_remove = sorted_entries[:len(sorted_entries) - self.local_cache_size + 1]
            for key, _ in to_remove:
                del self.local_cache[key]

    def get_stats(self):
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0

        return {
            **self.stats,
            "hit_rate": hit_rate,
            "local_cache_size": len(self.local_cache)
        }

# Global cache instance
cache = MultiLevelCache()

class CachedDSPyProgram:
    def __init__(self, program_class, cache_instance=None):
        self.program_class = program_class
        self.cache = cache_instance or cache

    async def execute(self, **kwargs):
        """Execute with caching"""
        # Try cache first
        cached_result = await self.cache.get(
            self.program_class.__name__,
            (),  # No positional args
            kwargs
        )

        if cached_result is not None:
            return cached_result

        # Execute program
        program = self.program_class()
        result = program(**kwargs)

        # Cache result (TTL based on result type)
        ttl = 1800  # 30 minutes default
        if hasattr(result, 'confidence') and result.confidence < 0.7:
            ttl = 300  # 5 minutes for low confidence results

        await self.cache.set(
            self.program_class.__name__,
            (),
            kwargs,
            result,
            ttl=ttl
        )

        return result

# Usage
cached_qa = CachedDSPyProgram(dspy.Predict(BasicQA))

# First call (cache miss)
result1 = await cached_qa.execute(question="What is Python?")
print(f"Result: {result1.answer}")

# Second call (cache hit)
result2 = await cached_qa.execute(question="What is Python?")
print(f"Cached result: {result2.answer}")

print("Cache stats:", cache.get_stats())
```

### Batch Processing

```python
class BatchProcessor:
    def __init__(self, batch_size=10, max_wait_time=5.0):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.batch_queue = []
        self.results = {}
        self.processing = False

    async def submit_request(self, request_id: str, program_func, *args, **kwargs):
        """Submit request for batch processing"""
        self.batch_queue.append({
            "id": request_id,
            "func": program_func,
            "args": args,
            "kwargs": kwargs,
            "timestamp": time.time()
        })

        # Start processing if batch is full or if we should start now
        if len(self.batch_queue) >= self.batch_size:
            await self._process_batch()
        elif not self.processing:
            asyncio.create_task(self._delayed_process())

        # Return future for result
        return self._get_result_future(request_id)

    async def _delayed_process(self):
        """Process batch after waiting"""
        await asyncio.sleep(self.max_wait_time)
        if self.batch_queue:
            await self._process_batch()

    async def _process_batch(self):
        """Process accumulated batch"""
        if not self.batch_queue or self.processing:
            return

        self.processing = True
        current_batch = self.batch_queue[:self.batch_size]
        self.batch_queue = self.batch_queue[self.batch_size:]

        try:
            # Process batch in parallel
            tasks = []
            for request in current_batch:
                task = asyncio.create_task(
                    self._execute_request(request)
                )
                tasks.append(task)

            # Wait for all to complete
            batch_results = await asyncio.gather(*tasks)

            # Store results
            for request, result in zip(current_batch, batch_results):
                self.results[request["id"]] = result

        finally:
            self.processing = False

    async def _execute_request(self, request):
        """Execute individual request"""
        try:
            result = await request["func"](*request["args"], **request["kwargs"])
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _get_result_future(self, request_id):
        """Get future for request result"""
        async def get_result():
            while request_id not in self.results:
                await asyncio.sleep(0.1)

            result = self.results.pop(request_id)  # Remove after retrieval
            if result["status"] == "error":
                raise Exception(result["error"])
            return result["result"]

        return get_result()

# Usage
batch_processor = BatchProcessor(batch_size=5, max_wait_time=2.0)

# Submit multiple requests
futures = []
for i in range(7):
    future = await batch_processor.submit_request(
        f"request_{i}",
        run_qa,
        f"What is example question {i}?"
    )
    futures.append(future)

# Get results
for i, future in enumerate(futures):
    try:
        result = await future()
        print(f"Request {i}: {result.answer}")
    except Exception as e:
        print(f"Request {i} failed: {e}")
```

## Monitoring and Observability

### Comprehensive Monitoring

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import psutil
import time

class DSPyMonitor:
    def __init__(self):
        # Request metrics
        self.requests_total = Counter(
            'dspy_requests_total',
            'Total DSPy requests',
            ['program', 'model', 'status']
        )

        self.request_duration = Histogram(
            'dspy_request_duration_seconds',
            'Request duration',
            ['program', 'model']
        )

        # Quality metrics
        self.quality_score = Histogram(
            'dspy_quality_score',
            'Quality scores',
            ['program', 'metric_type']
        )

        # Resource metrics
        self.active_requests = Gauge('dspy_active_requests', 'Active requests')
        self.memory_usage = Gauge('dspy_memory_usage_mb', 'Memory usage in MB')

        # Cache metrics
        self.cache_hits = Counter('dspy_cache_hits_total', 'Cache hits')
        self.cache_misses = Counter('dspy_cache_misses_total', 'Cache misses')

    def start_monitoring(self, port=8002):
        """Start Prometheus metrics server"""
        start_http_server(port)
        print(f"DSPy metrics server started on port {port}")

    async def collect_system_metrics(self):
        """Collect system resource metrics"""
        while True:
            self.memory_usage.set(psutil.Process().memory_info().rss / 1024 / 1024)
            await asyncio.sleep(30)

    def record_request(self, program_name: str, model_name: str, duration: float, status: str = "success"):
        """Record request metrics"""
        self.requests_total.labels(
            program=program_name,
            model=model_name,
            status=status
        ).inc()

        self.request_duration.labels(
            program=program_name,
            model=model_name
        ).observe(duration)

    def record_quality(self, program_name: str, metric_type: str, score: float):
        """Record quality metrics"""
        self.quality_score.labels(
            program=program_name,
            metric_type=metric_type
        ).observe(score)

    def update_active_requests(self, count: int):
        """Update active request count"""
        self.active_requests.set(count)

    def record_cache_access(self, hit: bool):
        """Record cache access"""
        if hit:
            self.cache_hits.inc()
        else:
            self.cache_misses.inc()

# Global monitor
monitor = DSPyMonitor()

class MonitoredDSPyProgram:
    def __init__(self, program_class, program_name: str):
        self.program_class = program_class
        self.program_name = program_name

    async def execute(self, **kwargs):
        """Execute with monitoring"""
        start_time = time.time()
        monitor.update_active_requests(1)

        try:
            # Execute program
            program = self.program_class()
            result = program(**kwargs)

            duration = time.time() - start_time

            # Record metrics
            model_name = dspy.settings.lm.model if dspy.settings.lm else "unknown"
            monitor.record_request(self.program_name, model_name, duration, "success")

            # Record quality if available
            if hasattr(result, 'confidence'):
                monitor.record_quality(self.program_name, "confidence", result.confidence)

            return result

        except Exception as e:
            duration = time.time() - start_time
            model_name = dspy.settings.lm.model if dspy.settings.lm else "unknown"
            monitor.record_request(self.program_name, model_name, duration, "error")

            raise e

        finally:
            monitor.update_active_requests(-1)

# Usage
monitored_qa = MonitoredDSPyProgram(dspy.Predict(BasicQA), "basic_qa")

# Start monitoring
monitor.start_monitoring()
asyncio.create_task(monitor.collect_system_metrics())

# Execute monitored program
result = await monitored_qa.execute(question="What is machine learning?")
print(f"Result: {result.answer}")
```

## Error Handling and Resilience

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def _can_attempt(self):
        """Check if request can be attempted"""
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        elif self.state == "HALF_OPEN":
            return True
        return False

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker"""
        if not self._can_attempt():
            raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)

            # Success - reset on half-open
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0

            return result

        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

async def resilient_qa(question):
    """QA with circuit breaker protection"""
    async def execute_qa():
        program = dspy.Predict(BasicQA)
        return program(question=question)

    return await circuit_breaker.call(execute_qa)

# Test circuit breaker
try:
    result = await resilient_qa("What is AI?")
    print(f"Success: {result.answer}")
except Exception as e:
    print(f"Circuit breaker triggered: {e}")
```

### Graceful Degradation

```python
class GracefulDegradationSystem:
    def __init__(self):
        self.degradation_levels = {
            "full": ["primary_model", "full_context", "detailed_response"],
            "degraded": ["fallback_model", "limited_context", "brief_response"],
            "minimal": ["basic_model", "no_context", "simple_response"]
        }
        self.current_level = "full"

    def assess_system_health(self):
        """Assess overall system health"""
        # Check various health indicators
        health_indicators = {
            "memory_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(),
            "error_rate": monitor.requests_total.labels(status="error")._value / max(1, monitor.requests_total._value),
            "response_time": monitor.request_duration._sum / max(1, monitor.request_duration._count)
        }

        # Determine degradation level
        if health_indicators["memory_usage"] > 90 or health_indicators["error_rate"] > 0.1:
            self.current_level = "minimal"
        elif health_indicators["cpu_usage"] > 80 or health_indicators["response_time"] > 5.0:
            self.current_level = "degraded"
        else:
            self.current_level = "full"

        return self.current_level

    def get_degraded_config(self):
        """Get configuration for current degradation level"""
        return self.degradation_levels[self.current_level]

    async def execute_with_degradation(self, program_func, *args, **kwargs):
        """Execute with graceful degradation"""
        current_level = self.assess_system_health()
        config = self.get_degraded_config()

        # Modify execution based on degradation level
        if current_level == "minimal":
            # Use simplest possible execution
            dspy.settings.configure(lm=cost_optimizer.get_model("gpt-3.5-turbo"))
            kwargs["max_tokens"] = 50  # Limit response length

        elif current_level == "degraded":
            # Use medium-quality execution
            dspy.settings.configure(lm=cost_optimizer.get_model("claude-3-haiku"))
            kwargs["max_tokens"] = 100

        # Execute with current configuration
        return await program_func(*args, **kwargs)

# Usage
degradation_system = GracefulDegradationSystem()

async def adaptive_qa(question):
    """QA with graceful degradation"""
    async def execute():
        program = dspy.Predict(BasicQA)
        return program(question=question)

    result = await degradation_system.execute_with_degradation(execute, question)
    degradation_level = degradation_system.current_level

    return result, degradation_level

# Test adaptive execution
result, level = await adaptive_qa("What is the capital of France?")
print(f"Result: {result.answer}, Degradation level: {level}")
```

## Deployment Infrastructure

### Container Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  dspy-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DSPY_ENV=production
      - REDIS_URL=redis://redis:6379
      - PROMETHEUS_MULTIPROC_DIR=/tmp
    depends_on:
      - redis
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    deploy:
      resources:
        limits:
          memory: 512M

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

volumes:
  redis_data:
```

### Kubernetes Deployment

```yaml
# k8s/dspy-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dspy-app
  labels:
    app: dspy-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dspy-app
  template:
    metadata:
      labels:
        app: dspy-app
    spec:
      containers:
      - name: dspy-app
        image: myregistry/dspy-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DSPY_ENV
          value: "production"
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: dspy-service
spec:
  selector:
    app: dspy-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: dspy-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: dspy-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Summary

In this chapter, we've covered:

- **Model Selection**: Cost-effective model routing and fallback strategies
- **Caching**: Multi-level caching for performance optimization
- **Batch Processing**: Efficient handling of multiple requests
- **Monitoring**: Comprehensive metrics and observability
- **Error Handling**: Circuit breakers and graceful degradation
- **Infrastructure**: Container and Kubernetes deployment

DSPy programs can now be deployed to production with enterprise-grade reliability, scalability, and monitoring.

## Key Takeaways

1. **Cost Optimization**: Smart model selection based on requirements and budget
2. **Performance**: Multi-level caching and batch processing for efficiency
3. **Reliability**: Circuit breakers, fallbacks, and graceful degradation
4. **Monitoring**: Comprehensive metrics for operational visibility
5. **Infrastructure**: Container orchestration for scalable deployment

Congratulations! You now have the complete knowledge to build, optimize, and deploy production-ready DSPy systems. The framework's automatic optimization capabilities combined with proper production practices enable you to create AI systems that are both powerful and maintainable.

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*