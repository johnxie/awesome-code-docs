---
layout: default
title: "Chapter 8: Production Scaling"
parent: "BentoML Tutorial"
nav_order: 8
---

# Chapter 8: Production Scaling

Welcome to **Chapter 8: Production Scaling**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This final chapter covers production scaling strategies for BentoML services. We'll explore horizontal scaling, load balancing, auto-scaling, high availability, and enterprise deployment patterns to handle production workloads effectively.

## Horizontal Scaling

### Docker Compose for Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  bentoml-service:
    build: .
    ports:
      - "3000-3009:3000"  # Port range for multiple instances
    environment:
      - BENTOML_PORT=3000
      - MODEL_PATH=/app/model
    volumes:
      - ./models:/app/model:ro
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  load-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - bentoml-service
```

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream bentoml_backend {
        least_conn;
        server bentoml-service:3000;
        server bentoml-service:3001;
        server bentoml-service:3002;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://bentoml_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeout settings
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### Kubernetes Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-service
  labels:
    app: bentoml-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bentoml-service
  template:
    metadata:
      labels:
        app: bentoml-service
    spec:
      containers:
      - name: bentoml
        image: my-bentoml-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: BENTOML_PORT
          value: "3000"
        resources:
          limits:
            cpu: "1000m"
            memory: "2Gi"
          requests:
            cpu: "500m"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/model
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
```

```yaml
# kubernetes/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: bentoml-service
  labels:
    app: bentoml-service
spec:
  selector:
    app: bentoml-service
  ports:
  - name: http
    port: 80
    targetPort: 3000
  type: ClusterIP
```

```yaml
# kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bentoml-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bentoml-service
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

## Load Balancing Strategies

### Advanced Load Balancing

```python
from typing import List, Dict, Any
import asyncio
import aiohttp
from dataclasses import dataclass
from collections import defaultdict
import time

@dataclass
class BackendServer:
    url: str
    weight: int = 1
    current_weight: int = 0
    active_requests: int = 0
    total_requests: int = 0
    response_time: float = 0.0
    failures: int = 0

class LoadBalancer:
    def __init__(self):
        self.backends: List[BackendServer] = []
        self.health_check_interval = 30
        self.max_failures = 3

    def add_backend(self, url: str, weight: int = 1):
        """Add backend server"""
        backend = BackendServer(url=url, weight=weight)
        self.backends.append(backend)

    async def health_check(self):
        """Perform health checks on all backends"""
        while True:
            for backend in self.backends:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{backend.url}/health") as response:
                            if response.status == 200:
                                backend.failures = 0
                            else:
                                backend.failures += 1
                except Exception:
                    backend.failures += 1

            await asyncio.sleep(self.health_check_interval)

    def get_healthy_backends(self) -> List[BackendServer]:
        """Get list of healthy backends"""
        return [b for b in self.backends if b.failures < self.max_failures]

    def select_backend_weighted_round_robin(self) -> BackendServer:
        """Select backend using weighted round-robin"""
        healthy_backends = self.get_healthy_backends()
        if not healthy_backends:
            raise Exception("No healthy backends available")

        total_weight = sum(b.weight for b in healthy_backends)
        max_weight = max(b.weight for b in healthy_backends)

        while True:
            for backend in healthy_backends:
                backend.current_weight += backend.weight
                if backend.current_weight >= max_weight:
                    backend.current_weight -= total_weight
                    return backend

    def select_backend_least_connections(self) -> BackendServer:
        """Select backend with least active connections"""
        healthy_backends = self.get_healthy_backends()
        if not healthy_backends:
            raise Exception("No healthy backends available")

        return min(healthy_backends, key=lambda b: b.active_requests)

    def select_backend_adaptive(self) -> BackendServer:
        """Select backend using adaptive algorithm"""
        healthy_backends = self.get_healthy_backends()
        if not healthy_backends:
            raise Exception("No healthy backends available")

        # Score based on response time and active connections
        def score_backend(backend):
            # Lower response time and fewer connections = better score
            response_score = backend.response_time if backend.response_time > 0 else 1.0
            connection_score = backend.active_requests
            return response_score * (1 + connection_score * 0.1)

        return min(healthy_backends, key=score_backend)

class BentoLoadBalancer:
    def __init__(self):
        self.lb = LoadBalancer()
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def add_service(self, url: str):
        """Add BentoML service"""
        self.lb.add_backend(url)

    async def predict(self, input_data: Any, strategy: str = "adaptive") -> Dict:
        """Make prediction using load balancing"""
        if strategy == "round_robin":
            backend = self.lb.select_backend_weighted_round_robin()
        elif strategy == "least_conn":
            backend = self.lb.select_backend_least_connections()
        else:  # adaptive
            backend = self.lb.select_backend_adaptive()

        backend.active_requests += 1
        start_time = time.time()

        try:
            async with self.session.post(
                f"{backend.url}/predict",
                json={"input": input_data}
            ) as response:
                result = await response.json()

            response_time = time.time() - start_time
            backend.response_time = response_time
            backend.total_requests += 1

            return result

        finally:
            backend.active_requests -= 1
```

## Auto-Scaling

### CPU/Memory-Based Auto-Scaling

```python
import psutil
import time
from typing import Dict, List
import threading

class AutoScaler:
    def __init__(self, min_instances=1, max_instances=10):
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.current_instances = min_instances
        self.cpu_threshold = 70.0
        self.memory_threshold = 80.0
        self.scale_up_cooldown = 60
        self.scale_down_cooldown = 120
        self.last_scale_up = 0
        self.last_scale_down = 0

    def get_system_metrics(self) -> Dict[str, float]:
        """Get current system metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }

    def should_scale_up(self, metrics: Dict[str, float]) -> bool:
        """Check if we should scale up"""
        current_time = time.time()

        if current_time - self.last_scale_up < self.scale_up_cooldown:
            return False

        if (metrics["cpu_percent"] > self.cpu_threshold or
            metrics["memory_percent"] > self.memory_threshold):
            return True

        return False

    def should_scale_down(self, metrics: Dict[str, float]) -> bool:
        """Check if we should scale down"""
        current_time = time.time()

        if current_time - self.last_scale_down < self.scale_down_cooldown:
            return False

        if self.current_instances <= self.min_instances:
            return False

        if (metrics["cpu_percent"] < self.cpu_threshold * 0.5 and
            metrics["memory_percent"] < self.memory_threshold * 0.5):
            return True

        return False

    def scale_up(self):
        """Scale up by adding instances"""
        if self.current_instances < self.max_instances:
            self.current_instances += 1
            self.last_scale_up = time.time()
            print(f"Scaled up to {self.current_instances} instances")
            return True
        return False

    def scale_down(self):
        """Scale down by removing instances"""
        if self.current_instances > self.min_instances:
            self.current_instances -= 1
            self.last_scale_down = time.time()
            print(f"Scaled down to {self.current_instances} instances")
            return True
        return False

class AdaptiveAutoScaler(AutoScaler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_history = []
        self.history_window = 300  # 5 minutes

    def record_request(self, response_time: float):
        """Record request metrics"""
        current_time = time.time()
        self.request_history.append((current_time, response_time))

        # Keep only recent history
        cutoff_time = current_time - self.history_window
        self.request_history = [
            (t, rt) for t, rt in self.request_history if t > cutoff_time
        ]

    def get_request_metrics(self) -> Dict[str, float]:
        """Calculate request-based metrics"""
        if not self.request_history:
            return {"avg_response_time": 0, "requests_per_second": 0}

        recent_requests = [
            rt for t, rt in self.request_history
            if time.time() - t < 60  # Last minute
        ]

        avg_response_time = sum(recent_requests) / len(recent_requests) if recent_requests else 0
        requests_per_second = len(recent_requests) / 60

        return {
            "avg_response_time": avg_response_time,
            "requests_per_second": requests_per_second
        }

    def should_scale_up(self, metrics: Dict[str, float]) -> bool:
        """Enhanced scale-up decision"""
        if super().should_scale_up(metrics):
            return True

        request_metrics = self.get_request_metrics()

        # Scale up if response time is too high
        if request_metrics["avg_response_time"] > 2.0:  # 2 seconds
            return True

        # Scale up if request rate is high
        if request_metrics["requests_per_second"] > 50:
            return True

        return False
```

### Kubernetes Auto-Scaling

```yaml
# kubernetes/advanced-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bentoml-advanced-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bentoml-service
  minReplicas: 3
  maxReplicas: 20
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
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
  - type: Pods
    pods:
      metric:
        name: packets-per-second
      target:
        type: AverageValue
        averageValue: 1000
```

## High Availability

### Multi-Region Deployment

```yaml
# kubernetes/multi-region-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-service-us-east
  labels:
    app: bentoml-service
    region: us-east
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bentoml-service
      region: us-east
  template:
    metadata:
      labels:
        app: bentoml-service
        region: us-east
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: topology.kubernetes.io/region
                operator: In
                values:
                - us-east-1
      containers:
      - name: bentoml
        image: my-bentoml-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: REGION
          value: "us-east"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# kubernetes/global-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: bentoml-global-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  selector:
    app: bentoml-service
  ports:
  - name: http
    port: 80
    targetPort: 3000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: bentoml-global-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.example.com
    secretName: tls-secret
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: bentoml-global-service
            port:
              number: 80
```

### Circuit Breaker Pattern

```python
import asyncio
from enum import Enum
from typing import Optional
import time

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def can_execute(self) -> bool:
        """Check if request can be executed"""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        else:  # HALF_OPEN
            return True

    def record_success(self):
        """Record successful execution"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        """Record failed execution"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

class CircuitBreakerService:
    def __init__(self):
        self.circuit_breakers = {}

    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]

    async def call_with_circuit_breaker(self, service_name: str, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        cb = self.get_circuit_breaker(service_name)

        if not cb.can_execute():
            raise Exception(f"Circuit breaker is OPEN for service {service_name}")

        try:
            result = await func(*args, **kwargs)
            cb.record_success()
            return result
        except cb.expected_exception as e:
            cb.record_failure()
            raise e
```

## Enterprise Deployment Patterns

### Blue-Green Deployment

```python
class DeploymentManager:
    def __init__(self):
        self.active_version = "blue"
        self.versions = {
            "blue": {"instances": 3, "healthy": True},
            "green": {"instances": 0, "healthy": False}
        }

    def switch_traffic(self):
        """Switch traffic between blue and green deployments"""
        old_version = self.active_version
        new_version = "green" if old_version == "blue" else "blue"

        # Scale up new version
        self.scale_deployment(new_version, 3)

        # Wait for health checks
        if self.wait_for_healthy(new_version):
            # Switch traffic
            self.active_version = new_version

            # Scale down old version
            self.scale_deployment(old_version, 0)

            print(f"Traffic switched from {old_version} to {new_version}")
            return True
        else:
            # Rollback - scale down new version
            self.scale_deployment(new_version, 0)
            print(f"Deployment failed, rolled back to {old_version}")
            return False

    def scale_deployment(self, version: str, instances: int):
        """Scale deployment to specified number of instances"""
        self.versions[version]["instances"] = instances
        print(f"Scaled {version} to {instances} instances")

    def wait_for_healthy(self, version: str, timeout: int = 300) -> bool:
        """Wait for deployment to become healthy"""
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.check_health(version):
                self.versions[version]["healthy"] = True
                return True
            time.sleep(10)

        return False

    def check_health(self, version: str) -> bool:
        """Check if deployment is healthy"""
        # Simulate health check
        return self.versions[version]["instances"] > 0
```

### Rolling Deployment

```python
class RollingDeployer:
    def __init__(self, total_instances: int = 6):
        self.total_instances = total_instances
        self.batch_size = max(1, total_instances // 3)  # Deploy in thirds

    async def rolling_update(self, new_image: str):
        """Perform rolling update"""
        updated = 0

        while updated < self.total_instances:
            batch_end = min(updated + self.batch_size, self.total_instances)

            # Update batch
            await self.update_batch(updated, batch_end, new_image)

            # Wait for health checks
            if not await self.wait_for_batch_health(updated, batch_end):
                raise Exception("Batch health check failed")

            updated = batch_end

        print("Rolling update completed successfully")

    async def update_batch(self, start: int, end: int, new_image: str):
        """Update a batch of instances"""
        print(f"Updating instances {start} to {end-1} with {new_image}")

        # Simulate update
        await asyncio.sleep(2)

    async def wait_for_batch_health(self, start: int, end: int) -> bool:
        """Wait for batch to become healthy"""
        await asyncio.sleep(5)  # Simulate health check time
        return True  # Simulate success
```

### Canary Deployment

```python
class CanaryDeployer:
    def __init__(self, traffic_distribution: Dict[str, float] = None):
        self.traffic_distribution = traffic_distribution or {"stable": 0.9, "canary": 0.1}
        self.metrics_collector = MetricsCollector()

    async def canary_deployment(self, new_version: str):
        """Perform canary deployment"""
        # Deploy canary version
        await self.deploy_canary(new_version)

        # Monitor performance
        stable_metrics = await self.monitor_version("stable")
        canary_metrics = await self.monitor_version("canary")

        # Compare metrics
        if self.compare_performance(stable_metrics, canary_metrics):
            # Promote canary to full deployment
            await self.promote_canary(new_version)
            print("Canary deployment successful")
        else:
            # Rollback canary
            await self.rollback_canary()
            print("Canary deployment rolled back")

    async def deploy_canary(self, version: str):
        """Deploy canary version"""
        print(f"Deploying canary version: {version}")

    async def monitor_version(self, version: str) -> Dict:
        """Monitor version performance"""
        await asyncio.sleep(10)  # Monitoring period

        # Simulate metrics collection
        return {
            "response_time": 0.5,
            "error_rate": 0.01,
            "throughput": 100
        }

    def compare_performance(self, stable: Dict, canary: Dict) -> bool:
        """Compare performance metrics"""
        # Simple comparison - canary should be within 10% of stable
        rt_threshold = 1.1  # 10% degradation allowed
        error_threshold = 1.5  # 50% error rate increase allowed

        if (canary["response_time"] > stable["response_time"] * rt_threshold or
            canary["error_rate"] > stable["error_rate"] * error_threshold):
            return False

        return True

    async def promote_canary(self, version: str):
        """Promote canary to full deployment"""
        self.traffic_distribution = {"stable": 0.0, "canary": 1.0}
        print(f"Promoted {version} to full deployment")

    async def rollback_canary(self):
        """Rollback canary deployment"""
        self.traffic_distribution = {"stable": 1.0, "canary": 0.0}
        print("Canary deployment rolled back")
```

## Performance Optimization

### Caching Strategies

```python
from typing import Any, Dict
import asyncio
from collections import OrderedDict
import time

class LRUCache:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any:
        """Get item from cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key: str, value: Any):
        """Put item in cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def get_stats(self) -> Dict[str, float]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        return {
            "hit_rate": hit_rate,
            "hits": self.hits,
            "misses": self.misses,
            "size": len(self.cache)
        }

@bentoml.service
class CachedBentoService:
    def __init__(self):
        self.cache = LRUCache(capacity=1000)
        self.cache_ttl = 3600  # 1 hour

    @bentoml.api
    def predict_with_cache(self, input_data):
        # Create cache key from input
        cache_key = str(hash(str(input_data.tobytes())))

        # Check cache
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            return {"prediction": cached_result, "cached": True}

        # Compute prediction
        result = self.model.predict(input_data)

        # Cache result
        self.cache.put(cache_key, result.tolist())

        return {"prediction": result.tolist(), "cached": False}

    @bentoml.api
    def get_cache_stats(self):
        """Get cache performance statistics"""
        return self.cache.get_stats()
```

## What We've Accomplished

Congratulations! 🎉 You've completed the comprehensive BentoML tutorial:

1. **Getting Started** - Basic BentoML concepts and service creation
2. **Model Packaging** - Advanced model packaging and versioning
3. **API Development** - Building robust APIs with validation and error handling
4. **Framework Integration** - Integrating with popular ML frameworks
5. **Testing & Validation** - Comprehensive testing strategies
6. **Deployment Strategies** - Production deployment patterns
7. **Monitoring & Observability** - Metrics, logging, and health checks
8. **Production Scaling** - Horizontal scaling, load balancing, and auto-scaling

## Final Thoughts

You've now mastered BentoML from basic concepts to production-ready deployments! Here's what makes this powerful:

### Key Achievements:
- ✅ Built production-ready ML services
- ✅ Implemented comprehensive monitoring and observability
- ✅ Mastered scaling strategies for high-traffic applications
- ✅ Learned enterprise deployment patterns
- ✅ Integrated with modern infrastructure (Docker, Kubernetes)
- ✅ Implemented performance optimization techniques

### Production Checklist:
- [ ] Model packaged with BentoML
- [ ] APIs with proper validation and error handling
- [ ] Comprehensive testing suite
- [ ] Monitoring and alerting configured
- [ ] Auto-scaling policies in place
- [ ] High availability setup
- [ ] Performance optimization implemented
- [ ] Security best practices applied

### Next Steps:
1. **Deploy your first BentoML service** to production
2. **Set up monitoring** with Prometheus and Grafana
3. **Implement auto-scaling** based on your workload
4. **Explore advanced features** like model serving optimizations
5. **Contribute back** to the BentoML community

Remember: The journey from model to production-ready service is now complete! 🚀

*What's your next BentoML project going to be?* 🤔

---

**Happy deploying!** 🎊

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `time`, `bentoml` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Scaling` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `service`, `backend`, `name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Scaling` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `time` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `bentoml`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/bentoml/BentoML)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `time` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Monitoring & Observability](07-monitoring-observability.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
