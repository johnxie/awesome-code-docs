---
layout: default
title: "Chapter 6: Deployment"
parent: "LLaMA Factory Tutorial"
nav_order: 6
---

# Chapter 6: Deployment

Welcome to the deployment phase! This chapter covers production deployment strategies for your fine-tuned LLaMA models, from model optimization to serving infrastructure and scaling considerations.

## Model Optimization for Production

### Quantization and Compression

```python
from transformers import BitsAndBytesConfig, AutoModelForCausalLM
import torch
from optimum.onnxruntime import ORTModelForCausalLM

def optimize_model_for_deployment(model_path: str, optimization_type: str = "quantization"):
    """Optimize model for production deployment"""

    if optimization_type == "quantization":
        # 4-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=quantization_config,
            device_map="auto"
        )

    elif optimization_type == "onnx":
        # Convert to ONNX for better performance
        model = ORTModelForCausalLM.from_pretrained(
            model_path,
            export=True
        )

    elif optimization_type == "tensorrt":
        # TensorRT optimization (for NVIDIA GPUs)
        from optimum.onnxruntime import ORTModelForCausalLM
        model = ORTModelForCausalLM.from_pretrained(
            model_path,
            provider="TensorrtExecutionProvider"
        )

    return model

# Usage
optimized_model = optimize_model_for_deployment(
    "path/to/fine-tuned-model",
    optimization_type="quantization"
)
```

## API Development

### FastAPI Server Setup

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI(title="LLaMA Model API", version="1.0.0")

class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt for generation")
    max_length: Optional[int] = Field(100, description="Maximum generation length")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    top_p: Optional[float] = Field(0.9, description="Top-p sampling")
    do_sample: Optional[bool] = Field(True, description="Enable sampling")

class GenerationResponse(BaseModel):
    generated_text: str
    prompt: str
    generation_time: float
    model_name: str

class ModelManager:
    """Manages model loading and inference"""

    def __init__(self, model_path: str, device: str = "auto"):
        self.device = device
        self.model_path = model_path
        self.model = None
        self.tokenizer = None

    async def load_model(self):
        """Load model asynchronously"""
        if self.model is None:
            print(f"Loading model from {self.model_path}")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map=self.device,
                load_in_8bit=True,  # Memory optimization
                trust_remote_code=True
            )

            print("Model loaded successfully")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate text from prompt"""
        if self.model is None:
            await self.load_model()

        start_time = time.time()

        # Tokenize input
        inputs = self.tokenizer(
            request.prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.model.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=request.max_length or 100,
                temperature=request.temperature or 0.7,
                top_p=request.top_p or 0.9,
                do_sample=request.do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        # Decode output
        generated_text = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )

        generation_time = time.time() - start_time

        return GenerationResponse(
            generated_text=generated_text,
            prompt=request.prompt,
            generation_time=generation_time,
            model_name=self.model_path.split('/')[-1]
        )

# Global model manager
model_manager = ModelManager("path/to/your/model")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    await model_manager.load_model()

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    """Generate text endpoint"""
    try:
        response = await model_manager.generate(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model_manager.model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Containerization

### Docker Setup for GPU Support

```dockerfile
# Dockerfile for GPU-enabled LLaMA deployment
FROM nvidia/cuda:11.8-runtime-ubuntu20.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
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
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "main.py"]
```

### Docker Compose for Complete Stack

```yaml
# docker-compose.yml
version: '3.8'

services:
  llama-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - MODEL_PATH=/app/models
    volumes:
      - ./models:/app/models:ro
      - ./logs:/app/logs
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - llama-api

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
```

## Scaling and Load Balancing

### Multi-Instance Deployment

```python
from fastapi import Request
import redis
import hashlib

class LoadBalancer:
    """Simple load balancer for multiple model instances"""

    def __init__(self, instances: List[str]):
        self.instances = instances
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_instance(self, request: Request) -> str:
        """Get appropriate instance for request"""

        # Use consistent hashing for session affinity
        client_ip = request.client.host
        instance_index = int(hashlib.md5(client_ip.encode()).hexdigest(), 16) % len(self.instances)

        return self.instances[instance_index]

    def get_health_status(self) -> Dict[str, bool]:
        """Get health status of all instances"""
        status = {}
        for instance in self.instances:
            # Check Redis cache for health status
            health_key = f"health:{instance}"
            status[instance] = self.redis.get(health_key) == b"healthy"
        return status

# Usage in FastAPI
load_balancer = LoadBalancer([
    "http://instance1:8000",
    "http://instance2:8000",
    "http://instance3:8000"
])

@app.middleware("http")
async def load_balancing_middleware(request: Request, call_next):
    """Route requests to appropriate instance"""

    if request.url.path.startswith("/generate"):
        target_instance = load_balancer.get_instance(request)

        # Proxy request to target instance
        # Implementation would forward the request

    response = await call_next(request)
    return response
```

## Monitoring and Observability

### Production Monitoring Setup

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Prometheus metrics
REQUEST_COUNT = Counter('llama_requests_total', 'Total number of requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('llama_request_duration_seconds', 'Request duration in seconds', ['method', 'endpoint'])
ACTIVE_REQUESTS = Gauge('llama_active_requests', 'Number of active requests')
MODEL_LOAD_TIME = Gauge('llama_model_load_time_seconds', 'Time taken to load model')

class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring requests"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        ACTIVE_REQUESTS.inc()

        try:
            response = await call_next(request)

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()

            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(time.time() - start_time)

            return response

        finally:
            ACTIVE_REQUESTS.dec()

# Initialize monitoring
def setup_monitoring():
    """Setup monitoring server"""
    start_http_server(8001)  # Prometheus metrics on port 8001

    # Custom metrics
    MODEL_LOAD_TIME.set(time.time())  # Would be set when model loads

    print("Monitoring server started on port 8001")

# Usage
app.add_middleware(MonitoringMiddleware)

@app.on_event("startup")
async def startup_event():
    setup_monitoring()
    await model_manager.load_model()
```

## Caching and Performance Optimization

### Redis Caching Layer

```python
import redis
import json
import hashlib
from typing import Optional

class RedisCache:
    """Redis-based caching for model responses"""

    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.ttl = 3600  # 1 hour cache

    def get_cache_key(self, prompt: str, params: dict) -> str:
        """Generate cache key from prompt and parameters"""
        content = f"{prompt}:{json.dumps(params, sort_keys=True)}"
        return f"llama:{hashlib.md5(content.encode()).hexdigest()}"

    def get(self, prompt: str, params: dict) -> Optional[str]:
        """Get cached response"""
        key = self.get_cache_key(prompt, params)
        return self.redis.get(key)

    def set(self, prompt: str, params: dict, response: str):
        """Cache response"""
        key = self.get_cache_key(prompt, params)
        self.redis.setex(key, self.ttl, response)

    def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern"""
        keys = self.redis.keys(f"llama:{pattern}*")
        if keys:
            self.redis.delete(*keys)

# Usage
cache = RedisCache()

@app.post("/generate")
async def generate_text(request: GenerationRequest):
    # Check cache first
    cached_response = cache.get(request.prompt, request.dict())
    if cached_response:
        return GenerationResponse(
            generated_text=cached_response,
            prompt=request.prompt,
            generation_time=0.0,
            model_name="cached"
        )

    # Generate new response
    response = await model_manager.generate(request)

    # Cache the result
    cache.set(request.prompt, request.dict(), response.generated_text)

    return response
```

## Security and Rate Limiting

### Production Security Setup

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import jwt
from datetime import datetime, timedelta

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Authentication
security = HTTPBearer()

SECRET_KEY = "your-secret-key"  # Would come from environment
ALGORITHM = "HS256"

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
async def login(username: str, password: str):
    """Simple login endpoint (in production, verify against database)"""
    if username == "admin" and password == "password":  # Demo only!
        access_token = create_access_token({"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/generate")
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute
async def generate_text(
    request: GenerationRequest,
    username: str = Depends(verify_token)
):
    """Protected generation endpoint"""
    # Add user context to request
    request.user_id = username

    response = await model_manager.generate(request)
    return response
```

## Cloud Deployment Options

### AWS SageMaker Deployment

```python
import boto3
from sagemaker import Model, Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

def deploy_to_sagemaker(model_path: str, role_arn: str):
    """Deploy model to AWS SageMaker"""

    # Create SageMaker model
    model = Model(
        image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.12.0-gpu-py38",
        model_data=model_path,
        role=role_arn,
        env={
            'MODEL_PATH': '/opt/ml/model',
            'SAGEMAKER_PROGRAM': 'inference.py'
        }
    )

    # Deploy endpoint
    predictor = model.deploy(
        initial_instance_count=1,
        instance_type='ml.g4dn.xlarge',  # GPU instance
        endpoint_name='llama-endpoint',
        serializer=JSONSerializer(),
        deserializer=JSONDeserializer()
    )

    return predictor

# Usage
sagemaker_predictor = deploy_to_sagemaker(
    model_path="s3://your-bucket/model.tar.gz",
    role_arn="arn:aws:iam::123456789012:role/SageMakerRole"
)

# Make prediction
response = sagemaker_predictor.predict({
    "prompt": "Hello, how are you?",
    "max_length": 50
})
```

## What We've Accomplished

Excellent! 🚀 You've mastered model deployment for LLaMA Factory:

1. **Model optimization** - Quantization and compression techniques
2. **API development** - FastAPI server with proper error handling
3. **Containerization** - Docker setup with GPU support
4. **Scaling strategies** - Load balancing and multi-instance deployment
5. **Monitoring setup** - Prometheus metrics and observability
6. **Caching layer** - Redis-based response caching
7. **Security measures** - Authentication and rate limiting
8. **Cloud deployment** - AWS SageMaker and other cloud options

## Next Steps

Ready for advanced techniques? In [Chapter 7: Advanced Techniques](07-advanced-techniques.md), we'll explore cutting-edge methods for even better performance!

---

**Practice what you've learned:**
1. Deploy your fine-tuned model as a REST API
2. Set up monitoring and alerting for your model service
3. Implement caching to improve response times
4. Add authentication and rate limiting to your API
5. Containerize your model for easy deployment

*What's your preferred deployment strategy?* ☁️

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `request`, `model` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Deployment` as an operating subsystem inside **LLaMA-Factory Tutorial: Unified Framework for LLM Training and Fine-tuning**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `prompt`, `response`, `model_path` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `request` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/hiyouga/LLaMA-Factory)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `request` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Model Evaluation](05-model-evaluation.md)
- [Next Chapter: Chapter 7: Advanced Techniques](07-advanced-techniques.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
