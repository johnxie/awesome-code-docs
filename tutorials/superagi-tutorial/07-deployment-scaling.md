---
layout: default
title: "Chapter 7: Deployment & Scaling"
parent: "SuperAGI Tutorial"
nav_order: 7
---

# Chapter 7: Deployment & Scaling

> Deploy SuperAGI to production with containerization, orchestration, monitoring, and horizontal scaling strategies.

## Overview

This chapter covers production deployment of SuperAGI systems, including containerization with Docker, orchestration with Kubernetes, performance optimization, monitoring, and scaling strategies for handling increased workloads.

## Docker Deployment

### Production Dockerfile

```dockerfile
# Multi-stage build for SuperAGI
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production image
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 superagi && \
    chown -R superagi:superagi /app

USER superagi

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["python", "-m", "superagi.main"]
```

### Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  superagi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://superagi:password@postgres:5432/superagi
      - REDIS_URL=redis://redis:6379/0
      - VECTOR_DB_URL=http://qdrant:6333
    depends_on:
      - postgres
      - redis
      - qdrant
    volumes:
      - ./workspace:/app/workspace
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=superagi
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=superagi
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U superagi"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"

  worker:
    build: .
    command: python -m superagi.worker
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://superagi:password@postgres:5432/superagi
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    deploy:
      replicas: 3

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
```

## Kubernetes Deployment

### Namespace and ConfigMap

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: superagi
  labels:
    app: superagi
---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: superagi-config
  namespace: superagi
data:
  LOG_LEVEL: "INFO"
  MAX_ITERATIONS: "25"
  AGENT_TIMEOUT: "3600"
  WORKER_CONCURRENCY: "4"
```

### Secrets Management

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: superagi-secrets
  namespace: superagi
type: Opaque
stringData:
  OPENAI_API_KEY: "${OPENAI_API_KEY}"
  DATABASE_URL: "postgresql://superagi:password@postgres:5432/superagi"
  REDIS_URL: "redis://redis:6379/0"
---
# External Secrets (recommended for production)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: superagi-external-secrets
  namespace: superagi
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-secrets-manager
  target:
    name: superagi-secrets
  data:
    - secretKey: OPENAI_API_KEY
      remoteRef:
        key: superagi/openai
        property: api_key
```

### Main Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: superagi-api
  namespace: superagi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: superagi
      component: api
  template:
    metadata:
      labels:
        app: superagi
        component: api
    spec:
      serviceAccountName: superagi-sa
      containers:
        - name: api
          image: superagi/superagi:latest
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: superagi-config
            - secretRef:
                name: superagi-secrets
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
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
          volumeMounts:
            - name: workspace
              mountPath: /app/workspace
      volumes:
        - name: workspace
          persistentVolumeClaim:
            claimName: superagi-workspace-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: superagi-api
  namespace: superagi
spec:
  selector:
    app: superagi
    component: api
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

### Worker Deployment with Autoscaling

```yaml
# k8s/worker-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: superagi-worker
  namespace: superagi
spec:
  replicas: 2
  selector:
    matchLabels:
      app: superagi
      component: worker
  template:
    metadata:
      labels:
        app: superagi
        component: worker
    spec:
      containers:
        - name: worker
          image: superagi/superagi:latest
          command: ["python", "-m", "superagi.worker"]
          envFrom:
            - configMapRef:
                name: superagi-config
            - secretRef:
                name: superagi-secrets
          resources:
            requests:
              memory: "1Gi"
              cpu: "500m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: superagi-worker-hpa
  namespace: superagi
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: superagi-worker
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: External
      external:
        metric:
          name: redis_queue_length
          selector:
            matchLabels:
              queue: superagi-tasks
        target:
          type: AverageValue
          averageValue: "10"
```

### Ingress Configuration

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: superagi-ingress
  namespace: superagi
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
    - hosts:
        - api.superagi.example.com
      secretName: superagi-tls
  rules:
    - host: api.superagi.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: superagi-api
                port:
                  number: 80
```

## Performance Optimization

### Agent Execution Pool

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Dict, Any, List
import multiprocessing

class AgentExecutionPool:
    """Optimized agent execution with process and thread pools."""

    def __init__(
        self,
        max_workers: int = None,
        use_processes: bool = False
    ):
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.use_processes = use_processes

        if use_processes:
            self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        self._active_tasks: Dict[str, asyncio.Task] = {}
        self._semaphore = asyncio.Semaphore(self.max_workers * 2)

    async def execute_agent(
        self,
        agent_id: str,
        agent_config: Dict[str, Any],
        task: str
    ) -> Dict[str, Any]:
        """Execute agent with resource management."""
        async with self._semaphore:
            loop = asyncio.get_event_loop()

            # Run CPU-intensive work in executor
            result = await loop.run_in_executor(
                self.executor,
                self._run_agent_sync,
                agent_id,
                agent_config,
                task
            )

            return result

    def _run_agent_sync(
        self,
        agent_id: str,
        agent_config: Dict[str, Any],
        task: str
    ) -> Dict[str, Any]:
        """Synchronous agent execution for process pool."""
        from superagi import Agent

        agent = Agent.from_config(agent_config)
        return agent.run(task)

    async def execute_batch(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute multiple agents concurrently."""
        coroutines = [
            self.execute_agent(
                task['agent_id'],
                task['config'],
                task['task']
            )
            for task in tasks
        ]

        return await asyncio.gather(*coroutines, return_exceptions=True)

    def shutdown(self):
        """Clean shutdown of executor."""
        self.executor.shutdown(wait=True)
```

### Caching Layer

```python
import redis
import json
import hashlib
from typing import Optional, Any
from functools import wraps
import pickle

class AgentCache:
    """Multi-level caching for agent operations."""

    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self._local_cache: Dict[str, Any] = {}
        self._local_cache_size = 1000

    def _make_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get from cache with local fallback."""
        # Check local cache first
        if key in self._local_cache:
            return self._local_cache[key]

        # Check Redis
        data = self.redis.get(key)
        if data:
            value = pickle.loads(data)
            self._update_local_cache(key, value)
            return value

        return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ):
        """Set cache value with TTL."""
        self._update_local_cache(key, value)
        self.redis.setex(key, ttl, pickle.dumps(value))

    def _update_local_cache(self, key: str, value: Any):
        """Update local cache with LRU eviction."""
        if len(self._local_cache) >= self._local_cache_size:
            # Simple eviction - remove first item
            self._local_cache.pop(next(iter(self._local_cache)))
        self._local_cache[key] = value

    def cached(self, ttl: int = 3600):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                key = f"{func.__name__}:{self._make_key(*args, **kwargs)}"

                cached_value = self.get(key)
                if cached_value is not None:
                    return cached_value

                result = await func(*args, **kwargs)
                self.set(key, result, ttl)
                return result
            return wrapper
        return decorator


# Usage with agent operations
cache = AgentCache("redis://localhost:6379/0")

@cache.cached(ttl=300)
async def get_agent_response(agent_id: str, prompt: str) -> str:
    """Cached agent response for repeated queries."""
    agent = await load_agent(agent_id)
    return await agent.generate_response(prompt)
```

### Memory-Efficient Processing

```python
from typing import Generator, Iterator
import gc

class StreamingAgentProcessor:
    """Memory-efficient streaming processor for large workloads."""

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size

    def process_tasks_streaming(
        self,
        tasks: Iterator[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Process tasks in streaming fashion to minimize memory."""
        batch = []

        for task in tasks:
            batch.append(task)

            if len(batch) >= self.batch_size:
                yield from self._process_batch(batch)
                batch = []
                gc.collect()  # Force garbage collection

        # Process remaining
        if batch:
            yield from self._process_batch(batch)

    def _process_batch(
        self,
        batch: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Process a batch of tasks."""
        for task in batch:
            try:
                result = self._execute_single(task)
                yield {"status": "success", "result": result, "task_id": task["id"]}
            except Exception as e:
                yield {"status": "error", "error": str(e), "task_id": task["id"]}

    def _execute_single(self, task: Dict[str, Any]) -> Any:
        """Execute single task with resource cleanup."""
        agent = Agent.from_config(task["config"])
        try:
            return agent.run(task["task"])
        finally:
            del agent
```

## Monitoring and Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response
import time

# Define metrics
AGENT_EXECUTIONS = Counter(
    'superagi_agent_executions_total',
    'Total agent executions',
    ['agent_type', 'status']
)

AGENT_EXECUTION_DURATION = Histogram(
    'superagi_agent_execution_duration_seconds',
    'Agent execution duration',
    ['agent_type'],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600]
)

ACTIVE_AGENTS = Gauge(
    'superagi_active_agents',
    'Currently active agents',
    ['agent_type']
)

TASK_QUEUE_SIZE = Gauge(
    'superagi_task_queue_size',
    'Tasks waiting in queue',
    ['queue_name']
)

LLM_TOKENS_USED = Counter(
    'superagi_llm_tokens_total',
    'Total LLM tokens consumed',
    ['model', 'type']
)

app = FastAPI()

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

class MetricsMiddleware:
    """Middleware for automatic metrics collection."""

    def __init__(self, agent):
        self.agent = agent

    async def execute(self, task: str) -> Dict[str, Any]:
        agent_type = self.agent.__class__.__name__

        ACTIVE_AGENTS.labels(agent_type=agent_type).inc()
        start_time = time.time()

        try:
            result = await self.agent.run(task)
            AGENT_EXECUTIONS.labels(
                agent_type=agent_type,
                status="success"
            ).inc()
            return result
        except Exception as e:
            AGENT_EXECUTIONS.labels(
                agent_type=agent_type,
                status="error"
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            AGENT_EXECUTION_DURATION.labels(
                agent_type=agent_type
            ).observe(duration)
            ACTIVE_AGENTS.labels(agent_type=agent_type).dec()
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

class TracedAgent:
    """Agent with distributed tracing support."""

    def __init__(self, agent):
        self.agent = agent
        self.tracer = trace.get_tracer(__name__)

    async def run(self, task: str) -> Dict[str, Any]:
        with self.tracer.start_as_current_span("agent_execution") as span:
            span.set_attribute("agent.type", self.agent.__class__.__name__)
            span.set_attribute("task.preview", task[:100])

            # Trace planning phase
            with self.tracer.start_as_current_span("planning"):
                plan = await self.agent.plan(task)
                span.set_attribute("plan.steps", len(plan.steps))

            # Trace execution phase
            results = []
            for i, step in enumerate(plan.steps):
                with self.tracer.start_as_current_span(f"step_{i}") as step_span:
                    step_span.set_attribute("step.action", step.action)
                    result = await self.agent.execute_step(step)
                    results.append(result)

            return {"plan": plan, "results": results}
```

### Logging Configuration

```python
import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging."""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['service'] = 'superagi'

        if hasattr(record, 'agent_id'):
            log_record['agent_id'] = record.agent_id
        if hasattr(record, 'task_id'):
            log_record['task_id'] = record.task_id

def setup_logging():
    """Configure structured logging."""
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

# Usage
logger = setup_logging()

class LoggingAgent:
    """Agent with comprehensive logging."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)

    async def run(self, task: str) -> Dict[str, Any]:
        self.logger.info(
            "Starting agent execution",
            extra={
                "agent_id": self.agent_id,
                "task_preview": task[:100]
            }
        )

        try:
            result = await self._execute(task)
            self.logger.info(
                "Agent execution completed",
                extra={
                    "agent_id": self.agent_id,
                    "status": "success"
                }
            )
            return result
        except Exception as e:
            self.logger.error(
                "Agent execution failed",
                extra={
                    "agent_id": self.agent_id,
                    "error": str(e)
                },
                exc_info=True
            )
            raise
```

## Scaling Strategies

### Queue-Based Architecture

```python
import redis
from rq import Queue, Worker
from typing import Dict, Any
import uuid

class TaskQueue:
    """Distributed task queue for agent execution."""

    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.queues = {
            "high": Queue("high", connection=self.redis),
            "default": Queue("default", connection=self.redis),
            "low": Queue("low", connection=self.redis)
        }

    def enqueue_task(
        self,
        task: Dict[str, Any],
        priority: str = "default"
    ) -> str:
        """Enqueue task for async processing."""
        task_id = str(uuid.uuid4())

        job = self.queues[priority].enqueue(
            execute_agent_task,
            task_id=task_id,
            agent_config=task["agent_config"],
            task_input=task["input"],
            job_timeout=task.get("timeout", 3600)
        )

        return task_id

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task execution status."""
        for queue in self.queues.values():
            job = queue.fetch_job(task_id)
            if job:
                return {
                    "task_id": task_id,
                    "status": job.get_status(),
                    "result": job.result if job.is_finished else None,
                    "error": str(job.exc_info) if job.is_failed else None
                }

        return {"task_id": task_id, "status": "not_found"}

def execute_agent_task(
    task_id: str,
    agent_config: Dict[str, Any],
    task_input: str
) -> Dict[str, Any]:
    """Worker function for agent execution."""
    from superagi import Agent

    agent = Agent.from_config(agent_config)
    result = agent.run(task_input)

    return {
        "task_id": task_id,
        "result": result,
        "completed_at": datetime.utcnow().isoformat()
    }
```

### Horizontal Scaling with Sharding

```python
from typing import List
import hashlib

class ShardedAgentCluster:
    """Sharded agent cluster for horizontal scaling."""

    def __init__(self, shard_urls: List[str]):
        self.shards = [
            AgentClient(url) for url in shard_urls
        ]
        self.num_shards = len(self.shards)

    def _get_shard(self, key: str) -> 'AgentClient':
        """Consistent hashing for shard selection."""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        shard_index = hash_value % self.num_shards
        return self.shards[shard_index]

    async def execute(
        self,
        agent_id: str,
        task: str
    ) -> Dict[str, Any]:
        """Execute task on appropriate shard."""
        shard = self._get_shard(agent_id)
        return await shard.execute(agent_id, task)

    async def broadcast(
        self,
        message: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Broadcast message to all shards."""
        import asyncio

        tasks = [
            shard.send_message(message)
            for shard in self.shards
        ]

        return await asyncio.gather(*tasks)
```

## Health Checks and Resilience

### Comprehensive Health Checks

```python
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import asyncio

app = FastAPI()

class HealthChecker:
    """Comprehensive health checking system."""

    def __init__(self):
        self.checks = {}

    def register(self, name: str, check_func):
        """Register a health check."""
        self.checks[name] = check_func

    async def run_all(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        overall_healthy = True

        for name, check in self.checks.items():
            try:
                result = await asyncio.wait_for(check(), timeout=5.0)
                results[name] = {"status": "healthy", **result}
            except asyncio.TimeoutError:
                results[name] = {"status": "unhealthy", "error": "timeout"}
                overall_healthy = False
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
                overall_healthy = False

        return {
            "status": "healthy" if overall_healthy else "unhealthy",
            "checks": results
        }

health_checker = HealthChecker()

# Register checks
async def check_database():
    async with get_db_connection() as conn:
        await conn.execute("SELECT 1")
    return {"latency_ms": 5}

async def check_redis():
    redis = get_redis_client()
    await redis.ping()
    return {"latency_ms": 2}

async def check_llm_api():
    # Quick health check to LLM provider
    response = await llm_client.models.list()
    return {"models_available": len(response.data)}

health_checker.register("database", check_database)
health_checker.register("redis", check_redis)
health_checker.register("llm_api", check_llm_api)

@app.get("/health")
async def health():
    """Basic liveness check."""
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    """Readiness check with dependency verification."""
    result = await health_checker.run_all()
    if result["status"] != "healthy":
        raise HTTPException(status_code=503, detail=result)
    return result
```

## Summary

In this chapter, you've learned:

- **Docker Deployment**: Multi-stage builds and compose configurations
- **Kubernetes**: Deployments, services, autoscaling, and ingress
- **Performance**: Execution pools, caching, and memory efficiency
- **Monitoring**: Prometheus metrics, distributed tracing, logging
- **Scaling**: Queue-based architecture and horizontal sharding
- **Resilience**: Health checks and dependency management

## Key Takeaways

1. **Containerize Everything**: Use Docker for consistent deployments
2. **Kubernetes for Scale**: HPA and pod autoscaling for dynamic workloads
3. **Cache Aggressively**: Reduce LLM calls with intelligent caching
4. **Monitor Thoroughly**: Metrics, traces, and logs for observability
5. **Design for Failure**: Health checks and graceful degradation

## Next Steps

Now that you can deploy and scale SuperAGI, let's explore Advanced Features in Chapter 8 for custom agents, plugins, and enterprise integrations.

---

**Ready for Chapter 8?** [Advanced Features](08-advanced-features.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
