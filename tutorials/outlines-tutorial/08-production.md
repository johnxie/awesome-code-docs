---
layout: default
title: "Outlines Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Outlines Tutorial
---

# Chapter 8: Production Deployment & Scaling

> Deploy Outlines constrained generation systems at enterprise scale with high availability, monitoring, and performance optimization.

## Production Architecture

### Scalable Microservices Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │  Load Balancer  │
│  (Kong/Traefik) │    │   (NGINX)       │
└─────────────────┘    └─────────────────┘
           │                       │
           └───────────────────────┘
                    │
          ┌─────────────────┐
          │  Outlines API   │
          │   Services      │
          │ (Kubernetes)    │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Model Cache   │
          │    (Redis)      │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Vector DB     │
          │ (Qdrant/Pinecone│
          │   for RAG)      │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Monitoring    │
          │ (Prometheus/    │
          │  Grafana)       │
          └─────────────────┘
```

## Kubernetes Deployment

### Complete Outlines Service Deployment

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: outlines
  labels:
    name: outlines

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: outlines-config
  namespace: outlines
data:
  MODEL_NAME: "microsoft/DialoGPT-small"
  MAX_CONCURRENT_REQUESTS: "10"
  CACHE_TTL: "3600"
  LOG_LEVEL: "INFO"
  METRICS_ENABLED: "true"
  HEALTH_CHECK_INTERVAL: "30"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: outlines-secrets
  namespace: outlines
type: Opaque
stringData:
  REDIS_PASSWORD: "your-secure-redis-password"
  API_KEY: "your-api-key-for-authentication"
  MODEL_API_KEY: "your-openai-or-other-api-key"

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: outlines-api
  namespace: outlines
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: outlines-api
  template:
    metadata:
      labels:
        app: outlines-api
    spec:
      containers:
      - name: outlines-api
        image: outlines-api:latest  # Your container image
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: outlines-config
        - secretRef:
            name: outlines-secrets
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
        # Startup probe for slow model loading
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 120
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 6
      volumes:
      - name: model-cache
        emptyDir: {}
      # Enable if you want persistent model cache
      # persistentVolumeClaim:
      #   claimName: model-cache-pvc

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: outlines-service
  namespace: outlines
spec:
  selector:
    app: outlines-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: outlines-hpa
  namespace: outlines
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: outlines-api
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
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "10"

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: outlines-ingress
  namespace: outlines
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
spec:
  tls:
  - hosts:
    - outlines-api.company.com
    secretName: outlines-tls
  rules:
  - host: outlines-api.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: outlines-service
            port:
              number: 80
```

## Docker Production Setup

### Multi-Stage Production Dockerfile

```dockerfile
# Dockerfile.production
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=app:app . .

# Create necessary directories
RUN mkdir -p /app/logs /app/models /app/cache

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "main.py"]
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Outlines API Service
  outlines-api:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: outlines-api-prod
    restart: unless-stopped
    environment:
      - MODEL_NAME=microsoft/DialoGPT-small
      - REDIS_URL=redis://redis:6379
      - MAX_CONCURRENT_REQUESTS=20
      - CACHE_TTL=3600
      - LOG_LEVEL=INFO
      - METRICS_ENABLED=true
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
      - model_cache:/app/models
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: outlines-redis-prod
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Vector Database (Optional, for RAG)
  qdrant:
    image: qdrant/qdrant:latest
    container_name: outlines-qdrant-prod
    restart: unless-stopped
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: outlines-prometheus
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: outlines-grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
    depends_on:
      - prometheus

volumes:
  redis_data:
  qdrant_data:
  prometheus_data:
  grafana_data:
  model_cache:
```

## Model Optimization for Production

### Model Quantization and Optimization

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from outlines import models
import torch

def load_optimized_model(model_name: str, device: str = "auto"):
    """Load model with production optimizations."""

    print(f"Loading optimized model: {model_name}")

    # 4-bit quantization for memory efficiency
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_quant_scale="fp4"
    )

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True
    )

    # Load model with optimizations
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map=device,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        # Memory optimizations
        use_cache=True,
        max_memory={0: "12GB", "cpu": "8GB"},  # Adjust based on your hardware
        offload_folder="./offload",
        # Performance optimizations
        load_in_8bit=False,  # We're using 4-bit
        low_cpu_mem_usage=True,
    )

    # Enable optimizations
    model.config.use_cache = True
    model.eval()  # Set to evaluation mode

    # Create Outlines model
    outlines_model = models.transformers(model, tokenizer)

    print("Model loaded with optimizations:")
    print(f"- Quantization: 4-bit NF4")
    print(f"- Device: {device}")
    print(f"- Memory usage: {torch.cuda.memory_allocated()/1024**3:.2f}GB")

    return outlines_model

# Usage
optimized_model = load_optimized_model("microsoft/DialoGPT-large")

# Test generation
generator = generate.text(optimized_model, max_tokens=50)
result = generator("Hello, this is a test of")
print(f"Optimized model output: {result}")
```

### Model Caching and Warm-up

```python
import asyncio
import time
from typing import Dict, List, Any
import redis
import json

class ProductionModelManager:
    """Production-ready model manager with caching and warm-up."""

    def __init__(self, redis_client=None):
        self.models: Dict[str, Any] = {}
        self.generators: Dict[str, Any] = {}
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour

    def load_model(self, model_name: str, **kwargs):
        """Load and cache model."""
        if model_name in self.models:
            return self.models[model_name]

        print(f"Loading model: {model_name}")
        start_time = time.time()

        model = load_optimized_model(model_name, **kwargs)
        load_time = time.time() - start_time

        self.models[model_name] = model

        # Cache metadata
        metadata = {
            "name": model_name,
            "load_time": load_time,
            "loaded_at": time.time(),
            "device": str(next(model.model.parameters()).device)
        }

        if self.redis:
            self.redis.setex(f"model:{model_name}:metadata", self.cache_ttl, json.dumps(metadata))

        print(f"Model {model_name} loaded in {load_time:.2f}s")
        return model

    def get_generator(self, model_name: str, constraint_type: str, constraint_config: Any):
        """Get cached generator."""
        cache_key = f"{model_name}:{constraint_type}:{hash(str(constraint_config))}"

        if cache_key in self.generators:
            return self.generators[cache_key]

        # Load model if needed
        model = self.load_model(model_name)

        # Create generator
        if constraint_type == "text":
            generator = generate.text(model, **constraint_config)
        elif constraint_type == "choice":
            generator = generate.choice(model, constraint_config)
        elif constraint_type == "json":
            generator = generate.json(model, constraint_config)
        elif constraint_type == "pydantic":
            generator = generate.pydantic(model, constraint_config)
        else:
            raise ValueError(f"Unsupported constraint type: {constraint_type}")

        self.generators[cache_key] = generator
        return generator

    async def warmup_models(self, model_configs: List[Dict[str, Any]]):
        """Warm up models with sample generations."""
        print("Starting model warm-up...")

        for config in model_configs:
            model_name = config["name"]
            warmup_prompts = config.get("warmup_prompts", ["Hello, how are you?"])

            print(f"Warming up {model_name}...")

            # Load model
            model = self.load_model(model_name)

            # Create sample generators
            text_gen = generate.text(model, max_tokens=10)

            # Generate warmup samples
            for prompt in warmup_prompts:
                try:
                    result = text_gen(prompt)
                    print(f"  ✓ Warmup: '{prompt}' -> '{result[:30]}...'")
                except Exception as e:
                    print(f"  ✗ Warmup failed: {e}")

        print("Model warm-up completed")

    def get_stats(self) -> Dict[str, Any]:
        """Get model manager statistics."""
        stats = {
            "loaded_models": len(self.models),
            "cached_generators": len(self.generators),
            "model_names": list(self.models.keys())
        }

        if self.redis:
            # Get Redis stats
            redis_keys = self.redis.keys("model:*:metadata")
            stats["redis_cached_models"] = len(redis_keys)

        return stats

# Usage
model_manager = ProductionModelManager()

# Warm up models
warmup_configs = [
    {
        "name": "microsoft/DialoGPT-small",
        "warmup_prompts": [
            "Hello, how are you?",
            "What is the weather like?",
            "Tell me a joke."
        ]
    }
]

await model_manager.warmup_models(warmup_configs)

# Use warmed up model
generator = model_manager.get_generator(
    "microsoft/DialoGPT-small",
    "choice",
    ["yes", "no", "maybe"]
)

result = generator("Should I continue?")
print(f"Generation result: {result}")

print("Model manager stats:", model_manager.get_stats())
```

## Monitoring and Observability

### Comprehensive Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import psutil

class ProductionMetrics:
    """Production monitoring metrics for Outlines."""

    def __init__(self):
        # Request metrics
        self.requests_total = Counter(
            'outlines_requests_total',
            'Total number of requests',
            ['model_name', 'constraint_type', 'status']
        )

        self.request_duration = Histogram(
            'outlines_request_duration_seconds',
            'Request duration in seconds',
            ['model_name', 'constraint_type']
        )

        # Model metrics
        self.model_load_duration = Histogram(
            'outlines_model_load_duration_seconds',
            'Model loading duration',
            ['model_name']
        )

        self.active_models = Gauge(
            'outlines_active_models',
            'Number of active models'
        )

        # Cache metrics
        self.cache_hits = Counter(
            'outlines_cache_hits_total',
            'Total cache hits'
        )

        self.cache_misses = Counter(
            'outlines_cache_misses_total',
            'Total cache misses'
        )

        # System metrics
        self.memory_usage = Gauge(
            'outlines_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.cpu_usage = Gauge(
            'outlines_cpu_usage_percent',
            'CPU usage percentage'
        )

        self.gpu_memory_usage = Gauge(
            'outlines_gpu_memory_usage_bytes',
            'GPU memory usage in bytes'
        )

    def record_request(self, model_name: str, constraint_type: str, duration: float, status: str = "success"):
        """Record request metrics."""
        self.requests_total.labels(model_name, constraint_type, status).inc()
        self.request_duration.labels(model_name, constraint_type).observe(duration)

    def record_model_load(self, model_name: str, duration: float):
        """Record model loading metrics."""
        self.model_load_duration.labels(model_name).observe(duration)

    def update_model_count(self, count: int):
        """Update active model count."""
        self.active_models.set(count)

    def record_cache_access(self, hit: bool):
        """Record cache access."""
        if hit:
            self.cache_hits.inc()
        else:
            self.cache_misses.inc()

    def update_system_metrics(self):
        """Update system resource metrics."""
        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_usage.set(cpu_percent)

        # GPU memory (if available)
        try:
            import torch
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.memory_allocated()
                self.gpu_memory_usage.set(gpu_memory)
        except:
            pass

    def get_metrics_text(self) -> str:
        """Get metrics in Prometheus format."""
        return generate_latest().decode('utf-8')

# Global metrics instance
metrics = ProductionMetrics()

class MonitoredOutlinesAPI:
    """Outlines API with comprehensive monitoring."""

    def __init__(self, model_manager: ProductionModelManager, metrics: ProductionMetrics):
        self.model_manager = model_manager
        self.metrics = metrics

    async def generate(self, model_name: str, constraint_type: str, constraint_config: Any, prompt: str) -> Dict[str, Any]:
        """Generate with monitoring."""
        start_time = time.time()

        try:
            # Get generator
            generator = self.model_manager.get_generator(model_name, constraint_type, constraint_config)

            # Record cache miss (generator creation)
            self.metrics.record_cache_access(hit=False)

            # Generate
            result = generator(prompt)

            # Record success
            duration = time.time() - start_time
            self.metrics.record_request(model_name, constraint_type, duration, "success")

            # Update system metrics
            self.metrics.update_system_metrics()
            self.metrics.update_model_count(len(self.model_manager.models))

            return {
                "success": True,
                "result": result,
                "duration": duration
            }

        except Exception as e:
            # Record failure
            duration = time.time() - start_time
            self.metrics.record_request(model_name, constraint_type, duration, "error")

            return {
                "success": False,
                "error": str(e),
                "duration": duration
            }

# Usage
monitored_api = MonitoredOutlinesAPI(model_manager, metrics)

# Make monitored request
result = await monitored_api.generate(
    "microsoft/DialoGPT-small",
    "choice",
    ["excellent", "good", "average", "poor"],
    "Rate this tutorial:"
)

print("Generation result:", result)
print("Sample metrics:")
print(metrics.get_metrics_text()[:1000] + "...")
```

### Health Checks and Readiness

```python
from typing import Dict, Any
import asyncio
import time

class HealthChecker:
    """Comprehensive health checking for Outlines service."""

    def __init__(self, model_manager: ProductionModelManager, redis_client=None):
        self.model_manager = model_manager
        self.redis = redis_client
        self.last_health_check = 0
        self.health_status = {}

    async def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        health = {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {}
        }

        # Model health check
        try:
            models_loaded = len(self.model_manager.models)
            health["checks"]["models"] = {
                "status": "healthy",
                "models_loaded": models_loaded,
                "model_names": list(self.model_manager.models.keys())
            }
        except Exception as e:
            health["checks"]["models"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health["status"] = "unhealthy"

        # Redis health check
        if self.redis:
            try:
                self.redis.ping()
                health["checks"]["redis"] = {"status": "healthy"}
            except Exception as e:
                health["checks"]["redis"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health["status"] = "unhealthy"
        else:
            health["checks"]["redis"] = {"status": "not_configured"}

        # Generation test
        try:
            # Quick test with loaded model
            if self.model_manager.models:
                model_name = list(self.model_manager.models.keys())[0]
                test_gen = self.model_manager.get_generator(model_name, "text", {"max_tokens": 5})
                test_result = test_gen("Test")

                health["checks"]["generation"] = {
                    "status": "healthy",
                    "test_result_length": len(test_result)
                }
            else:
                health["checks"]["generation"] = {
                    "status": "no_models_loaded"
                }
        except Exception as e:
            health["checks"]["generation"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health["status"] = "unhealthy"

        # System resources
        health["checks"]["system"] = self._check_system_resources()

        self.health_status = health
        self.last_health_check = time.time()

        return health

    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage."""
        try:
            import psutil

            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=0.1)

            system_health = {
                "memory_percent": memory.percent,
                "cpu_percent": cpu,
                "memory_available_gb": memory.available / (1024**3)
            }

            # Determine status based on thresholds
            if memory.percent > 90 or cpu > 95:
                system_health["status"] = "critical"
            elif memory.percent > 80 or cpu > 80:
                system_health["status"] = "warning"
            else:
                system_health["status"] = "healthy"

            return system_health

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def readiness_check(self) -> Dict[str, Any]:
        """Readiness check for Kubernetes."""
        # Minimum requirements for readiness
        health = await self.check_health()

        readiness = {
            "ready": health["status"] == "healthy",
            "checks": health["checks"]
        }

        # Additional readiness criteria
        if len(self.model_manager.models) == 0:
            readiness["ready"] = False
            readiness["reason"] = "no_models_loaded"

        return readiness

    def get_health_status(self) -> Dict[str, Any]:
        """Get last health check status."""
        return self.health_status

# Usage in FastAPI
from fastapi import FastAPI

app = FastAPI()
health_checker = HealthChecker(model_manager)

@app.get("/health")
async def health_endpoint():
    """Health check endpoint."""
    return await health_checker.check_health()

@app.get("/ready")
async def readiness_endpoint():
    """Readiness check endpoint."""
    return await health_checker.readiness_check()

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint."""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(metrics.get_metrics_text())
```

## Security Hardening

### API Authentication and Authorization

```python
from typing import Optional, Dict, Any
import jwt
import time
import hashlib
import hmac
from functools import wraps

class SecurityManager:
    """Security manager for Outlines API."""

    def __init__(self, jwt_secret: str, api_keys: Dict[str, str] = None):
        self.jwt_secret = jwt_secret
        self.api_keys = api_keys or {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}

    def authenticate_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """Authenticate JWT token."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])

            # Check expiration
            if payload.get('exp', 0) < time.time():
                return None

            return payload

        except jwt.InvalidTokenError:
            return None

    def authenticate_api_key(self, api_key: str) -> Optional[str]:
        """Authenticate API key."""
        # Hash the provided key for comparison
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        for user_id, stored_hash in self.api_keys.items():
            if hmac.compare_digest(key_hash, stored_hash):
                return user_id

        return None

    def authorize_request(self, user_info: Dict[str, Any], required_permission: str) -> bool:
        """Check if user has required permission."""
        user_permissions = user_info.get('permissions', [])
        user_role = user_info.get('role', 'user')

        # Role-based permissions
        role_permissions = {
            'admin': ['*'],  # Admin has all permissions
            'user': ['generate:text', 'generate:choice', 'generate:json'],
            'guest': ['generate:text']
        }

        allowed_permissions = role_permissions.get(user_role, [])

        return required_permission in allowed_permissions or '*' in allowed_permissions

    def check_rate_limit(self, user_id: str, endpoint: str, max_requests: int = 100, window: int = 60) -> bool:
        """Check rate limit for user."""
        key = f"{user_id}:{endpoint}"
        current_time = int(time.time())

        if key not in self.rate_limits:
            self.rate_limits[key] = {
                'requests': [],
                'blocked_until': 0
            }

        limit_data = self.rate_limits[key]

        # Check if still blocked
        if current_time < limit_data['blocked_until']:
            return False

        # Clean old requests
        limit_data['requests'] = [
            req_time for req_time in limit_data['requests']
            if current_time - req_time < window
        ]

        # Check limit
        if len(limit_data['requests']) >= max_requests:
            # Block for the window duration
            limit_data['blocked_until'] = current_time + window
            return False

        # Add current request
        limit_data['requests'].append(current_time)
        return True

# Authentication middleware
def require_auth(permission: str = None):
    """Decorator for authentication and authorization."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from args (FastAPI specific)
            request = kwargs.get('request') or args[0] if args else None

            if not request:
                return {"error": "No request object"}

            # Try JWT authentication
            auth_header = request.headers.get('Authorization', '')
            user_info = None

            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                user_info = security_manager.authenticate_jwt(token)

            # Try API key authentication
            if not user_info:
                api_key = request.headers.get('X-API-Key') or request.query_params.get('api_key')
                if api_key:
                    user_id = security_manager.authenticate_api_key(api_key)
                    if user_id:
                        user_info = {"user_id": user_id, "role": "user"}  # Default role

            if not user_info:
                return {"error": "Authentication required"}

            # Check permission
            if permission and not security_manager.authorize_request(user_info, permission):
                return {"error": "Insufficient permissions"}

            # Check rate limit
            endpoint = request.url.path
            if not security_manager.check_rate_limit(user_info['user_id'], endpoint):
                return {"error": "Rate limit exceeded"}

            # Add user info to request
            request.state.user = user_info

            return await func(*args, **kwargs)

        return wrapper
    return decorator

# Usage in FastAPI
security_manager = SecurityManager(
    jwt_secret="your-jwt-secret",
    api_keys={
        "user123": hashlib.sha256("api-key-123".encode()).hexdigest(),
        "admin456": hashlib.sha256("admin-key-456".encode()).hexdigest()
    }
)

@app.post("/generate")
@require_auth("generate:text")
async def generate_text(request: Request, payload: Dict[str, Any]):
    """Protected generation endpoint."""
    user = request.state.user

    # Generate with user context
    result = await monitored_api.generate(
        payload["model_name"],
        payload["constraint_type"],
        payload["constraint_config"],
        payload["prompt"]
    )

    return result
```

## Performance Benchmarking

### Comprehensive Benchmark Suite

```python
import asyncio
import time
import statistics
from typing import List, Dict, Any
import json

class PerformanceBenchmark:
    """Comprehensive benchmarking for Outlines performance."""

    def __init__(self, model_manager: ProductionModelManager):
        self.model_manager = model_manager

    async def benchmark_generation(self, model_name: str, constraint_type: str,
                                 constraint_config: Any, prompts: List[str],
                                 iterations: int = 10) -> Dict[str, Any]:
        """Benchmark generation performance."""

        results = {
            "model_name": model_name,
            "constraint_type": constraint_type,
            "iterations": iterations,
            "prompts_tested": len(prompts),
            "results": []
        }

        # Get generator
        generator = self.model_manager.get_generator(model_name, constraint_type, constraint_config)

        for prompt in prompts:
            prompt_results = {
                "prompt": prompt,
                "durations": [],
                "outputs": [],
                "success_count": 0,
                "error_count": 0
            }

            for i in range(iterations):
                try:
                    start_time = time.time()
                    output = generator(prompt)
                    duration = time.time() - start_time

                    prompt_results["durations"].append(duration)
                    prompt_results["outputs"].append(output)
                    prompt_results["success_count"] += 1

                except Exception as e:
                    prompt_results["durations"].append(0)
                    prompt_results["error_count"] += 1
                    print(f"Error in iteration {i}: {e}")

            # Calculate statistics
            successful_durations = [d for d in prompt_results["durations"] if d > 0]

            if successful_durations:
                prompt_results["stats"] = {
                    "mean_duration": statistics.mean(successful_durations),
                    "median_duration": statistics.median(successful_durations),
                    "min_duration": min(successful_durations),
                    "max_duration": max(successful_durations),
                    "std_duration": statistics.stdev(successful_durations) if len(successful_durations) > 1 else 0,
                    "success_rate": prompt_results["success_count"] / iterations
                }
            else:
                prompt_results["stats"] = {"success_rate": 0}

            results["results"].append(prompt_results)

        # Overall statistics
        all_durations = []
        total_successes = 0
        total_requests = 0

        for prompt_result in results["results"]:
            all_durations.extend([d for d in prompt_result["durations"] if d > 0])
            total_successes += prompt_result["success_count"]
            total_requests += iterations

        results["overall_stats"] = {
            "total_requests": total_requests,
            "total_successes": total_successes,
            "overall_success_rate": total_successes / total_requests if total_requests > 0 else 0,
            "avg_duration": statistics.mean(all_durations) if all_durations else 0,
            "throughput": total_successes / sum(all_durations) if all_durations else 0
        }

        return results

    async def benchmark_memory_usage(self, model_name: str) -> Dict[str, Any]:
        """Benchmark memory usage."""

        import psutil
        import torch

        initial_memory = psutil.virtual_memory().used

        # Load model
        start_time = time.time()
        model = self.model_manager.load_model(model_name)
        load_time = time.time() - start_time

        after_load_memory = psutil.virtual_memory().used

        # GPU memory if available
        gpu_memory = 0
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.memory_allocated()

        return {
            "model_name": model_name,
            "load_time": load_time,
            "memory_increase": after_load_memory - initial_memory,
            "gpu_memory": gpu_memory,
            "total_memory_mb": (after_load_memory - initial_memory) / (1024 * 1024)
        }

    async def run_comprehensive_benchmark(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive benchmark suite."""

        benchmark_results = {
            "timestamp": time.time(),
            "config": config,
            "memory_benchmark": {},
            "generation_benchmarks": []
        }

        # Memory benchmark
        benchmark_results["memory_benchmark"] = await self.benchmark_memory_usage(
            config["model_name"]
        )

        # Generation benchmarks
        for benchmark_config in config["generation_tests"]:
            print(f"Running benchmark: {benchmark_config['name']}")

            result = await self.benchmark_generation(
                config["model_name"],
                benchmark_config["constraint_type"],
                benchmark_config["constraint_config"],
                benchmark_config["prompts"],
                benchmark_config.get("iterations", 5)
            )

            benchmark_results["generation_benchmarks"].append({
                "name": benchmark_config["name"],
                "results": result
            })

        return benchmark_results

# Usage
benchmark = PerformanceBenchmark(model_manager)

# Comprehensive benchmark configuration
benchmark_config = {
    "model_name": "microsoft/DialoGPT-small",
    "generation_tests": [
        {
            "name": "text_generation",
            "constraint_type": "text",
            "constraint_config": {"max_tokens": 20},
            "prompts": ["Hello, how are you?", "What is the weather like?", "Tell me a joke."],
            "iterations": 3
        },
        {
            "name": "choice_generation",
            "constraint_type": "choice",
            "constraint_config": ["red", "blue", "green", "yellow"],
            "prompts": ["Pick a color:", "Choose a color for the logo:"],
            "iterations": 5
        }
    ]
}

# Run comprehensive benchmark
results = await benchmark.run_comprehensive_benchmark(benchmark_config)

# Save results
with open("benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Benchmark completed. Results saved to benchmark_results.json")
print("Overall success rate:", results["generation_benchmarks"][0]["results"]["overall_stats"]["overall_success_rate"])
print("Average generation time:", results["generation_benchmarks"][0]["results"]["overall_stats"]["avg_duration"])
```

This production deployment chapter provides enterprise-ready infrastructure, monitoring, security, and performance optimization for Outlines constrained generation systems. The comprehensive setup ensures reliability, scalability, and maintainability in production environments. 🚀

## Quick Production Setup

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Or use Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Check health
curl https://your-domain.com/health

# Monitor metrics
curl https://your-domain.com/metrics

# Run benchmark
python benchmark.py
```

This completes the comprehensive Outlines production deployment guide! 🎊