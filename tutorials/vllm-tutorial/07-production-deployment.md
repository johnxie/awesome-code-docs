---
layout: default
title: "vLLM Tutorial - Chapter 7: Production Deployment"
nav_order: 7
has_children: false
parent: vLLM Tutorial
---

# Chapter 7: Production Deployment - Serving vLLM at Scale

> Deploy vLLM in production with FastAPI, Docker, Kubernetes, and enterprise-grade operational practices.

## Overview

Production deployment requires robust serving infrastructure, monitoring, security, and scalability. This chapter covers deploying vLLM with FastAPI, containerization, orchestration, and production best practices.

## FastAPI Integration

### Basic FastAPI Server

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from vllm import LLM, SamplingParams
import asyncio
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="vLLM API Server",
    description="Production-ready vLLM inference API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vLLM instance
llm: Optional[LLM] = None

# Request/Response models
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Input text prompt")
    max_tokens: int = Field(100, description="Maximum tokens to generate")
    temperature: float = Field(0.7, description="Sampling temperature")
    top_p: float = Field(0.9, description="Top-p sampling parameter")
    top_k: int = Field(-1, description="Top-k sampling parameter")
    stop: Optional[List[str]] = Field(None, description="Stop sequences")
    stream: bool = Field(False, description="Enable streaming response")

class GenerateResponse(BaseModel):
    text: str
    tokens_generated: int
    generation_time: float
    model_name: str

class BatchRequest(BaseModel):
    prompts: List[str] = Field(..., description="List of input prompts")
    max_tokens: int = Field(100, description="Maximum tokens per response")
    temperature: float = Field(0.7, description="Sampling temperature")
    top_p: float = Field(0.9, description="Top-p sampling parameter")

class BatchResponse(BaseModel):
    responses: List[GenerateResponse]
    total_tokens: int
    batch_time: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    gpu_memory_used: float
    gpu_memory_total: float

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize vLLM on startup"""
    global llm
    try:
        logger.info("Initializing vLLM...")
        llm = LLM(
            model="microsoft/DialoGPT-medium",
            gpu_memory_utilization=0.9,
            max_model_len=1024,
            dtype="half"
        )
        logger.info("vLLM initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vLLM: {e}")
        raise

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if llm is None:
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            gpu_memory_used=0.0,
            gpu_memory_total=0.0
        )

    try:
        import torch
        memory_used = torch.cuda.memory_allocated() / (1024**3) if torch.cuda.is_available() else 0
        memory_total = torch.cuda.get_device_properties(0).total_memory / (1024**3) if torch.cuda.is_available() else 0

        return HealthResponse(
            status="healthy",
            model_loaded=True,
            gpu_memory_used=memory_used,
            gpu_memory_total=memory_total
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="error",
            model_loaded=llm is not None,
            gpu_memory_used=0.0,
            gpu_memory_total=0.0
        )

# Single generation endpoint
@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text from a single prompt"""
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Create sampling parameters
        sampling_params = SamplingParams(
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            stop=request.stop
        )

        # Generate text
        start_time = time.time()
        outputs = llm.generate([request.prompt], sampling_params)
        generation_time = time.time() - start_time

        result = outputs[0]
        response_text = result.outputs[0].text
        tokens_generated = len(result.outputs[0].token_ids)

        logger.info(f"Generated {tokens_generated} tokens in {generation_time:.3f}s")

        return GenerateResponse(
            text=response_text,
            tokens_generated=tokens_generated,
            generation_time=generation_time,
            model_name="microsoft/DialoGPT-medium"
        )

    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

# Batch generation endpoint
@app.post("/generate/batch", response_model=BatchResponse)
async def generate_batch(request: BatchRequest):
    """Generate text for multiple prompts"""
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if len(request.prompts) > 32:  # Limit batch size
        raise HTTPException(status_code=400, detail="Batch size too large (max 32)")

    try:
        sampling_params = SamplingParams(
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )

        start_time = time.time()
        outputs = llm.generate(request.prompts, sampling_params)
        batch_time = time.time() - start_time

        responses = []
        total_tokens = 0

        for i, result in enumerate(outputs):
            response_text = result.outputs[0].text
            tokens_generated = len(result.outputs[0].token_ids)
            total_tokens += tokens_generated

            responses.append(GenerateResponse(
                text=response_text,
                tokens_generated=tokens_generated,
                generation_time=batch_time,  # Total batch time
                model_name="microsoft/DialoGPT-medium"
            ))

        logger.info(f"Batch processed {len(request.prompts)} prompts, {total_tokens} total tokens in {batch_time:.3f}s")

        return BatchResponse(
            responses=responses,
            total_tokens=total_tokens,
            batch_time=batch_time
        )

    except Exception as e:
        logger.error(f"Batch generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch generation failed: {str(e)}")

# Streaming generation endpoint
@app.post("/generate/stream")
async def generate_stream(request: GenerateRequest):
    """Streaming text generation"""
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not request.stream:
        # Fall back to regular generation
        return await generate_text(request)

    async def generate_stream():
        """Generator for streaming response"""
        try:
            sampling_params = SamplingParams(
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
                stop=request.stop
            )

            stream = llm.generate(request.prompt, sampling_params, stream=True)

            async for output in stream:
                if output.outputs:
                    # Send new text since last update
                    new_text = output.outputs[0].text
                    yield f"data: {new_text}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### Advanced FastAPI Features

```python
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import redis

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Authentication
security = HTTPBearer()

# Redis for caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class AuthenticatedUser:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # In production, validate against database
        self.is_valid = api_key.startswith("sk-")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Authenticate user"""
    token = credentials.credentials

    # Simple validation (replace with proper auth)
    if not token or not token.startswith("sk-"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return AuthenticatedUser(token)

# Cached generation with authentication
@app.post("/generate/cached")
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute
async def generate_cached(
    request: GenerateRequest,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Cached generation with authentication and rate limiting"""
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Create cache key
    cache_key = f"generate:{hash(request.prompt + str(request.max_tokens))}"

    # Check cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        import json
        return json.loads(cached_result)

    try:
        # Generate new result
        sampling_params = SamplingParams(
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )

        start_time = time.time()
        outputs = llm.generate([request.prompt], sampling_params)
        generation_time = time.time() - start_time

        result = outputs[0]
        response = GenerateResponse(
            text=result.outputs[0].text,
            tokens_generated=len(result.outputs[0].token_ids),
            generation_time=generation_time,
            model_name="microsoft/DialoGPT-medium"
        )

        # Cache result for 5 minutes
        redis_client.setex(cache_key, 300, response.json())

        return response

    except Exception as e:
        logger.error(f"Cached generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Get service metrics"""
    # In production, integrate with Prometheus
    return {
        "uptime": time.time() - app.startup_time if hasattr(app, 'startup_time') else 0,
        "requests_processed": getattr(app, 'request_count', 0),
        "model_loaded": llm is not None,
        "gpu_memory_used": torch.cuda.memory_allocated() / (1024**3) if torch.cuda.is_available() else 0
    }

# Middleware for request counting
@app.middleware("http")
async def count_requests(request: Request, call_next):
    """Count total requests"""
    if not hasattr(app, 'request_count'):
        app.request_count = 0
    app.request_count += 1

    response = await call_next(request)
    return response

# Startup time tracking
@app.on_event("startup")
async def track_startup():
    """Track application startup time"""
    app.startup_time = time.time()
```

## Docker Containerization

### Dockerfile for vLLM

```dockerfile
# Dockerfile for vLLM production deployment
FROM nvidia/cuda:12.0-runtime-ubuntu20.04

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "main.py"]
```

### Multi-Stage Docker Build

```dockerfile
# Multi-stage build for optimized production image
FROM nvidia/cuda:12.0-devel-ubuntu20.04 AS builder

# Build stage for installing dependencies
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-pip \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM nvidia/cuda:12.0-runtime-ubuntu20.04

# Install Python and runtime dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Change ownership
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "main.py"]
```

### Docker Compose for Development

```yaml
# docker-compose.yml for development
version: '3.8'

services:
  vllm-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - CUDA_VISIBLE_DEVICES=0  # Use first GPU
      - MODEL_NAME=microsoft/DialoGPT-medium
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
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
    restart: unless-stopped

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  redis_data:
  prometheus_data:
  grafana_data:
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml for production
version: '3.8'

services:
  vllm-api:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - CUDA_VISIBLE_DEVICES=all
      - MODEL_NAME=microsoft/DialoGPT-large
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models:ro
      - ./logs:/app/logs
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 32G
        reservations:
          memory: 16G

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - vllm-api
    restart: always

volumes:
  redis_data:
    driver: local
```

## Kubernetes Deployment

### Basic Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-deployment
  labels:
    app: vllm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
    spec:
      containers:
      - name: vllm
        image: myregistry/vllm-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_NAME
          value: "microsoft/DialoGPT-medium"
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            memory: "8Gi"
            cpu: "2"
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
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
      volumes:
      - name: model-cache
        persistentVolumeClaim:
          claimName: vllm-model-cache-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vllm-model-cache-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
spec:
  selector:
    app: vllm
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vllm-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: vllm.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: vllm-service
            port:
              number: 80
```

### Horizontal Pod Autoscaling

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-deployment
  minReplicas: 1
  maxReplicas: 5
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
        name: vllm_requests_per_second
      target:
        type: AverageValue
        averageValue: 10
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

### GPU Resource Management

```yaml
# k8s/gpu-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-gpu-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-gpu
  template:
    metadata:
      labels:
        app: vllm-gpu
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: nvidia.com/gpu.present
                operator: In
                values:
                - "true"
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
      containers:
      - name: vllm
        image: myregistry/vllm-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: NVIDIA_VISIBLE_DEVICES
          value: "all"
        - name: MODEL_NAME
          value: "microsoft/DialoGPT-large"
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "16Gi"
            cpu: "4"
          requests:
            nvidia.com/gpu: 1
            memory: "8Gi"
            cpu: "2"
        securityContext:
          privileged: true  # Required for GPU access
        volumeMounts:
        - name: dshm
          mountPath: /dev/shm
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory
          sizeLimit: "1Gi"
```

## Monitoring and Observability

### Prometheus Metrics

```python
# metrics.py - Prometheus metrics for vLLM
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class VLLMMetrics:
    def __init__(self):
        # Request metrics
        self.requests_total = Counter(
            'vllm_requests_total',
            'Total number of requests',
            ['method', 'endpoint', 'status']
        )

        self.request_duration = Histogram(
            'vllm_request_duration_seconds',
            'Request duration in seconds',
            ['method', 'endpoint']
        )

        # Generation metrics
        self.tokens_generated = Counter(
            'vllm_tokens_generated_total',
            'Total number of tokens generated'
        )

        self.generation_time = Histogram(
            'vllm_generation_time_seconds',
            'Time spent generating tokens'
        )

        # Model metrics
        self.model_loaded = Gauge(
            'vllm_model_loaded',
            'Whether the model is loaded (1) or not (0)'
        )

        # Resource metrics
        self.gpu_memory_used = Gauge(
            'vllm_gpu_memory_used_bytes',
            'GPU memory used in bytes'
        )

        self.cpu_usage = Gauge(
            'vllm_cpu_usage_percent',
            'CPU usage percentage'
        )

    def start_metrics_server(self, port=8001):
        """Start Prometheus metrics server"""
        start_http_server(port)
        print(f"Metrics server started on port {port}")

    def record_request(self, method: str, endpoint: str, duration: float, status: str = "success"):
        """Record request metrics"""
        self.requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
        self.request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    def record_generation(self, tokens_count: int, generation_time: float):
        """Record generation metrics"""
        self.tokens_generated.inc(tokens_count)
        self.generation_time.observe(generation_time)

    def update_model_status(self, loaded: bool):
        """Update model loaded status"""
        self.model_loaded.set(1 if loaded else 0)

    def update_resource_usage(self):
        """Update resource usage metrics"""
        try:
            import torch
            if torch.cuda.is_available():
                memory_used = torch.cuda.memory_allocated()
                self.gpu_memory_used.set(memory_used)

            import psutil
            cpu_percent = psutil.cpu_percent()
            self.cpu_usage.set(cpu_percent)

        except ImportError:
            pass  # Optional dependencies

# Global metrics instance
metrics = VLLMMetrics()

# Integration with FastAPI
def setup_metrics_integration(app: FastAPI):
    """Integrate metrics with FastAPI app"""

    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time
        metrics.record_request(
            method=request.method,
            endpoint=request.url.path,
            duration=duration,
            status="success" if response.status_code < 400 else "error"
        )

        return response

    return app
```

### Structured Logging

```python
# logging_config.py - Structured logging configuration
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredFormatter(logging.Formatter):
    """JSON structured logging formatter"""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add extra fields
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        # Add exception info
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

def setup_structured_logging(log_level=logging.INFO, log_file=None):
    """Setup structured logging"""

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

    return logger

# Custom logger for vLLM operations
class VLLMLogger:
    def __init__(self):
        self.logger = logging.getLogger('vllm')

    def log_request(self, request_id: str, method: str, endpoint: str, user_id: str = None):
        """Log API request"""
        self.logger.info(
            f"API request: {method} {endpoint}",
            extra={
                'extra_fields': {
                    'request_id': request_id,
                    'user_id': user_id,
                    'event_type': 'api_request'
                }
            }
        )

    def log_generation(self, request_id: str, prompt_length: int, response_length: int, duration: float):
        """Log generation completion"""
        self.logger.info(
            f"Generation completed: {response_length} tokens in {duration:.3f}s",
            extra={
                'extra_fields': {
                    'request_id': request_id,
                    'prompt_length': prompt_length,
                    'response_length': response_length,
                    'duration': duration,
                    'tokens_per_second': response_length / duration if duration > 0 else 0,
                    'event_type': 'generation_complete'
                }
            }
        )

    def log_error(self, request_id: str, error_type: str, error_message: str):
        """Log error"""
        self.logger.error(
            f"Error: {error_type} - {error_message}",
            extra={
                'extra_fields': {
                    'request_id': request_id,
                    'error_type': error_type,
                    'event_type': 'error'
                }
            }
        )

# Global logger instance
vllm_logger = VLLMLogger()
```

## Security and Compliance

### API Security

```python
# security.py - Security middleware and utilities
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib
import hmac

class SecurityManager:
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = "HS256"
        self.security = HTTPBearer()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def create_api_key(self, user_id: str, scopes: list = None) -> str:
        """Create API key for user"""
        api_key = secrets.token_urlsafe(32)
        # In production, store hashed version in database
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Store key_hash, user_id, scopes in database
        # self.store_api_key(key_hash, user_id, scopes)

        return api_key

    def verify_api_key(self, api_key: str) -> Optional[dict]:
        """Verify API key"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        # Look up key_hash in database and return user info
        # return self.lookup_api_key(key_hash)
        return None  # Placeholder

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(Security(HTTPBearer()))):
        """FastAPI dependency for authentication"""
        token = credentials.credentials

        # Try JWT first
        try:
            payload = self.verify_token(token)
            return payload
        except:
            pass

        # Try API key
        user_info = self.verify_api_key(token)
        if user_info:
            return user_info

        raise HTTPException(status_code=401, detail="Invalid authentication")

class RateLimiter:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.requests = {}  # In-memory fallback

    async def check_rate_limit(self, user_id: str, limit: int = 60, window: int = 60) -> bool:
        """Check if user is within rate limit"""
        current_time = int(datetime.utcnow().timestamp())
        window_start = current_time - window

        if self.redis:
            # Redis-based rate limiting
            key = f"ratelimit:{user_id}"
            # Use Redis sorted set to track requests
            self.redis.zremrangebyscore(key, '-inf', window_start)
            request_count = self.redis.zcard(key)

            if request_count >= limit:
                return False

            self.redis.zadd(key, {str(current_time): current_time})
            self.redis.expire(key, window)
            return True
        else:
            # Simple in-memory rate limiting
            if user_id not in self.requests:
                self.requests[user_id] = []

            # Clean old requests
            self.requests[user_id] = [
                ts for ts in self.requests[user_id] if ts > window_start
            ]

            if len(self.requests[user_id]) >= limit:
                return False

            self.requests[user_id].append(current_time)
            return True

# Global security instances
security_manager = SecurityManager()
rate_limiter = RateLimiter()

# Rate limited endpoint decorator
def rate_limited(limit: int = 60, window: int = 60):
    """Decorator for rate limiting"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract user from kwargs (depends on your auth setup)
            user = kwargs.get('current_user', {})
            user_id = user.get('sub', 'anonymous')

            if not await rate_limiter.check_rate_limit(user_id, limit, window):
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. {limit} requests per {window} seconds."
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### Production Configuration

```python
# config/production.py - Production configuration
import os
from typing import List

class ProductionConfig:
    """Production configuration for vLLM API"""

    # Model configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "microsoft/DialoGPT-medium")
    MODEL_DTYPE = os.getenv("MODEL_DTYPE", "half")
    GPU_MEMORY_UTILIZATION = float(os.getenv("GPU_MEMORY_UTILIZATION", "0.9"))
    MAX_MODEL_LEN = int(os.getenv("MAX_MODEL_LEN", "1024"))

    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    WORKERS = int(os.getenv("WORKERS", "1"))

    # Security configuration
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "true").lower() == "true"

    # Rate limiting
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

    # CORS configuration
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:8080"
    ).split(",")

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "/app/logs/vllm.log")

    # Redis configuration (optional)
    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_ENABLED = bool(REDIS_URL)

    # Metrics configuration
    METRICS_ENABLED = os.getenv("METRICS_ENABLED", "true").lower() == "true"
    METRICS_PORT = int(os.getenv("METRICS_PORT", "8001"))

    # Health check configuration
    HEALTH_CHECK_ENABLED = True
    HEALTH_CHECK_INTERVAL = 30  # seconds

# Configuration instance
config = ProductionConfig()
```

## Summary

In this chapter, we've covered comprehensive production deployment:

- **FastAPI Integration**: REST API with authentication, rate limiting, and caching
- **Docker Containerization**: Multi-stage builds and production-optimized images
- **Kubernetes Deployment**: Auto-scaling, resource management, and high availability
- **Monitoring**: Prometheus metrics and structured logging
- **Security**: JWT authentication, API keys, and rate limiting
- **Production Configuration**: Environment-based configuration management

These practices enable deploying vLLM in production with enterprise-grade reliability, security, and observability.

## Key Takeaways

1. **API Design**: RESTful endpoints with proper error handling and documentation
2. **Containerization**: Optimized Docker images for production deployment
3. **Orchestration**: Kubernetes manifests for scalable, reliable deployment
4. **Monitoring**: Comprehensive metrics and logging for operational visibility
5. **Security**: Authentication, authorization, and rate limiting for production safety

Next, we'll explore **monitoring and scaling** - performance monitoring and auto-scaling strategies.

---

**Ready for the next chapter?** [Chapter 8: Monitoring & Scaling](08-monitoring-scaling.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*