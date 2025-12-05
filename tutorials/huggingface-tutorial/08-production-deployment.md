---
layout: default
title: "Chapter 8: Production Deployment"
parent: "HuggingFace Transformers Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

> Deploy Transformer models at scale with high performance and reliability.

## 🎯 Overview

This chapter covers production deployment strategies for Transformer models, including optimization techniques, scaling approaches, monitoring, and operational best practices for running AI models in production environments.

## 🚀 Model Optimization for Production

### Model Compression Techniques

#### Quantization

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from torch.quantization import quantize_dynamic

class ModelQuantizer:
    def __init__(self, model_name="bert-base-uncased"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def quantize_model(self, model, quantization_type="dynamic"):
        """Quantize model for reduced size and faster inference"""
        if quantization_type == "dynamic":
            # Dynamic quantization
            quantized_model = quantize_dynamic(
                model,
                {torch.nn.Linear},  # Quantize linear layers
                dtype=torch.qint8
            )
        elif quantization_type == "static":
            # Static quantization requires calibration data
            quantized_model = self._static_quantization(model)
        else:
            raise ValueError(f"Unknown quantization type: {quantization_type}")

        return quantized_model

    def _static_quantization(self, model):
        """Perform static quantization with calibration"""
        model.eval()

        # Fuse layers
        model = torch.quantization.fuse_modules(
            model,
            [['encoder.layer.0.attention.self.query', 'encoder.layer.0.attention.self.key']],
        )

        # Set quantization config
        model.qconfig = torch.quantization.get_default_qconfig('fbgemm')

        # Prepare for quantization
        torch.quantization.prepare(model, inplace=True)

        # Calibrate with sample data
        self._calibrate_model(model)

        # Convert to quantized model
        torch.quantization.convert(model, inplace=True)

        return model

    def _calibrate_model(self, model, num_samples=100):
        """Calibrate quantization with sample data"""
        # Generate sample inputs for calibration
        sample_texts = [
            "This is a sample text for calibration.",
            "Another example sentence for quantization.",
            "Machine learning models need calibration data."
        ] * (num_samples // 3)

        for text in sample_texts:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                model(**inputs)

    def optimize_for_inference(self, model):
        """Apply inference optimizations"""
        # Set to evaluation mode
        model.eval()

        # Enable inference optimizations
        if hasattr(model, "config"):
            model.config.use_cache = True

        # Disable gradient computation
        for param in model.parameters():
            param.requires_grad = False

        return model

    def save_optimized_model(self, model, path="./optimized-model"):
        """Save optimized model with tokenizer"""
        # Save model
        torch.save(model.state_dict(), f"{path}/pytorch_model.bin")

        # Save tokenizer
        self.tokenizer.save_pretrained(path)

        # Save model config
        if hasattr(model, "config"):
            model.config.save_pretrained(path)

        # Create model card
        self._create_model_card(path)

    def _create_model_card(self, path):
        """Create model card for documentation"""
        model_card = f"""
---
language: en
tags:
  - transformers
  - pytorch
  - quantized
license: apache-2.0
---

# Optimized {self.model_name} Model

This is an optimized, quantized version of {self.model_name} for production deployment.

## Model Details
- **Base Model**: {self.model_name}
- **Optimization**: 8-bit quantization
- **Framework**: PyTorch
- **License**: Apache 2.0

## Usage

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load optimized model
model = AutoModelForSequenceClassification.from_pretrained("./optimized-model")
tokenizer = AutoTokenizer.from_pretrained("./optimized-model")

# Use for inference
inputs = tokenizer("Sample text", return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
```
"""

        with open(f"{path}/README.md", "w") as f:
            f.write(model_card)

# Usage
quantizer = ModelQuantizer("microsoft/DialoGPT-medium")

# Load base model
base_model = AutoModelForSequenceClassification.from_pretrained("microsoft/DialoGPT-medium")

# Quantize
quantized_model = quantizer.quantize_model(base_model, "dynamic")

# Optimize for inference
optimized_model = quantizer.optimize_for_inference(quantized_model)

# Save
quantizer.save_optimized_model(optimized_model, "./optimized-dialogpt")
```

### ONNX Conversion

```python
from transformers.onnx import export
from transformers import AutoTokenizer
from pathlib import Path

class ONNXConverter:
    def __init__(self, model_name="bert-base-uncased"):
        self.model_name = model_name

    def convert_to_onnx(self, output_path="./model.onnx"):
        """Convert model to ONNX format for optimized inference"""
        # Export to ONNX
        export(
            preprocessor=AutoTokenizer.from_pretrained(self.model_name),
            model=self.model_name,
            output=Path(output_path),
            opset=13,
            device="cpu"
        )

        print(f"Model exported to {output_path}")

    def optimize_onnx_model(self, onnx_path):
        """Apply ONNX optimizations"""
        import onnxruntime as ort
        from onnxruntime.transformers import optimizer

        # Load model
        model_path = Path(onnx_path)
        model_bytes = model_path.read_bytes()

        # Create optimizer
        opt = optimizer.optimize_model(
            model_path.as_posix(),
            model_type='bert',
            num_heads=12,
            hidden_size=768
        )

        # Save optimized model
        optimized_path = model_path.parent / f"{model_path.stem}_optimized{model_path.suffix}"
        opt.save_model_to_file(optimized_path.as_posix())

        return optimized_path

# Usage
converter = ONNXConverter("bert-base-uncased")
converter.convert_to_onnx("./bert-base-uncased.onnx")
optimized_path = converter.optimize_onnx_model("./bert-base-uncased.onnx")
```

## ⚡ High-Performance Serving

### FastAPI Model Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Transformers API", version="1.0.0")

# Global model cache
model_cache = {}

class PredictionRequest(BaseModel):
    text: str
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
    task: str = "sentiment-analysis"

class PredictionResponse(BaseModel):
    result: dict
    processing_time: float
    model_version: str

def load_model(model_name: str, task: str):
    """Load and cache model"""
    cache_key = f"{model_name}_{task}"

    if cache_key not in model_cache:
        logger.info(f"Loading model: {model_name} for task: {task}")
        model_cache[cache_key] = pipeline(task=task, model=model_name)

    return model_cache[cache_key]

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make prediction with specified model"""
    start_time = asyncio.get_event_loop().time()

    try:
        # Load model (cached)
        model = load_model(request.model_name, request.task)

        # Make prediction in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                model,
                request.text
            )

        processing_time = asyncio.get_event_loop().time() - start_time

        return PredictionResponse(
            result=result[0] if isinstance(result, list) else result,
            processing_time=round(processing_time, 3),
            model_version=request.model_name
        )

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "cached_models": list(model_cache.keys()),
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "available_models": [
            "distilbert-base-uncased-finetuned-sst-2-english",
            "microsoft/DialoGPT-medium",
            "gpt2",
            "bert-base-uncased"
        ],
        "cached_models": list(model_cache.keys())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=4,  # Multiple workers for better concurrency
        access_log=True
    )
```

### GPU-Accelerated Serving

```python
from transformers import pipeline
import torch
from concurrent.futures import ThreadPoolExecutor
import asyncio

class GPUModelServer:
    def __init__(self, model_name="microsoft/DialoGPT-large", device="cuda:0"):
        self.model_name = model_name
        self.device = device

        # Load model on GPU
        self.model = pipeline(
            "text-generation",
            model=model_name,
            device=device,
            torch_dtype=torch.float16,  # Use mixed precision
            max_length=50,
            pad_token_id=50256
        )

        # Create thread pool for concurrent requests
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def generate_async(self, prompt: str, **kwargs):
        """Async text generation with GPU acceleration"""
        loop = asyncio.get_running_loop()

        # Run generation in thread pool
        result = await loop.run_in_executor(
            self.executor,
            self._generate_sync,
            prompt,
            kwargs
        )

        return result

    def _generate_sync(self, prompt: str, kwargs):
        """Synchronous generation (runs in thread pool)"""
        try:
            # Merge default and user kwargs
            generation_kwargs = {
                "max_length": 50,
                "temperature": 0.8,
                "top_p": 0.9,
                "do_sample": True,
                "pad_token_id": 50256,
                "num_return_sequences": 1
            }
            generation_kwargs.update(kwargs)

            # Generate text
            result = self.model(prompt, **generation_kwargs)

            return {
                "generated_text": result[0]["generated_text"],
                "status": "success"
            }

        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    async def batch_generate(self, prompts: list, **kwargs):
        """Batch text generation"""
        tasks = [self.generate_async(prompt, **kwargs) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        return results

    def get_gpu_memory_usage(self):
        """Get GPU memory usage"""
        if torch.cuda.is_available():
            return {
                "allocated": torch.cuda.memory_allocated(self.device) / 1024**3,  # GB
                "reserved": torch.cuda.memory_reserved(self.device) / 1024**3,    # GB
                "total": torch.cuda.get_device_properties(self.device).total_memory / 1024**3  # GB
            }
        return None

# Usage
gpu_server = GPUModelServer("microsoft/DialoGPT-large")

# Single generation
result = await gpu_server.generate_async("Hello, how are you?")
print(result["generated_text"])

# Batch generation
prompts = ["Tell me a joke", "Explain quantum physics", "Write a poem"]
results = await gpu_server.batch_generate(prompts)
for prompt, result in zip(prompts, results):
    print(f"Prompt: {prompt}")
    print(f"Generated: {result['generated_text'][:100]}...")
    print("---")

# Check GPU memory
memory_info = gpu_server.get_gpu_memory_usage()
if memory_info:
    print(f"GPU Memory: {memory_info['allocated']:.2f}GB / {memory_info['total']:.2f}GB")
```

## 📊 Monitoring and Observability

### Comprehensive Monitoring Setup

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import logging
from functools import wraps

class ModelMonitor:
    def __init__(self, service_name="transformers-api"):
        self.service_name = service_name

        # Prometheus metrics
        self.request_count = Counter(
            'requests_total',
            'Total number of requests',
            ['method', 'endpoint', 'status']
        )

        self.request_latency = Histogram(
            'request_duration_seconds',
            'Request duration in seconds',
            ['method', 'endpoint']
        )

        self.active_requests = Gauge(
            'active_requests',
            'Number of active requests'
        )

        self.model_inference_time = Histogram(
            'model_inference_duration_seconds',
            'Model inference time',
            ['model_name', 'task']
        )

        self.memory_usage = Gauge(
            'memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.gpu_memory_usage = Gauge(
            'gpu_memory_usage_bytes',
            'GPU memory usage in bytes',
            ['device']
        )

    def monitor_endpoint(self, method="GET", endpoint="/"):
        """Decorator for monitoring endpoints"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                self.active_requests.inc()

                try:
                    result = await func(*args, **kwargs)
                    self.request_count.labels(method=method, endpoint=endpoint, status="success").inc()
                    return result

                except Exception as e:
                    self.request_count.labels(method=method, endpoint=endpoint, status="error").inc()
                    logging.error(f"Request error: {str(e)}")
                    raise

                finally:
                    duration = time.time() - start_time
                    self.request_latency.labels(method=method, endpoint=endpoint).observe(duration)
                    self.active_requests.dec()

            return wrapper
        return decorator

    def monitor_inference(self, model_name, task):
        """Decorator for monitoring model inference"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    inference_time = time.time() - start_time
                    self.model_inference_time.labels(
                        model_name=model_name, task=task
                    ).observe(inference_time)
                    return result

                except Exception as e:
                    logging.error(f"Inference error for {model_name}: {str(e)}")
                    raise

            return wrapper
        return decorator

    def update_memory_metrics(self):
        """Update memory usage metrics"""
        import psutil
        import torch

        # System memory
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)

        # GPU memory
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                gpu_memory = torch.cuda.memory_allocated(i)
                self.gpu_memory_usage.labels(device=f"cuda:{i}").set(gpu_memory)

    def start_monitoring_server(self, port=8001):
        """Start Prometheus metrics server"""
        start_http_server(port)
        logging.info(f"Monitoring server started on port {port}")

# Usage in FastAPI app
monitor = ModelMonitor()

@app.on_event("startup")
async def startup_event():
    monitor.start_monitoring_server()
    # Update memory metrics every 30 seconds
    asyncio.create_task(monitor._periodic_memory_update())

@app.post("/predict")
@monitor.monitor_endpoint("POST", "/predict")
async def predict(request: PredictionRequest):
    monitor.update_memory_metrics()

    # Monitor inference
    @monitor.monitor_inference(request.model_name, request.task)
    def do_inference():
        model = load_model(request.model_name, request.task)
        return model(request.text)

    result = do_inference()
    return PredictionResponse(
        result=result[0] if isinstance(result, list) else result,
        processing_time=0.0,  # Would track this properly
        model_version=request.model_name
    )
```

### Logging and Alerting

```python
import structlog
import logging
from logging.handlers import RotatingFileHandler
import json

class AdvancedLogger:
    def __init__(self, service_name="transformers-api"):
        self.service_name = service_name
        self._setup_structured_logging()

    def _setup_structured_logging(self):
        """Setup structured JSON logging"""
        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Setup file handler with rotation
        file_handler = RotatingFileHandler(
            f"{self.service_name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )

        # Setup console handler
        console_handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Setup logger
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_request(self, request_id, method, endpoint, user_agent=None, ip_address=None):
        """Log API request"""
        self.logger.info(
            "API Request",
            request_id=request_id,
            method=method,
            endpoint=endpoint,
            user_agent=user_agent,
            ip_address=ip_address
        )

    def log_inference(self, request_id, model_name, input_length, output_length, inference_time):
        """Log model inference"""
        self.logger.info(
            "Model Inference",
            request_id=request_id,
            model_name=model_name,
            input_length=input_length,
            output_length=output_length,
            inference_time=inference_time
        )

    def log_error(self, request_id, error_type, error_message, stack_trace=None):
        """Log errors"""
        self.logger.error(
            "Application Error",
            request_id=request_id,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace
        )

# Alerting system
class AlertManager:
    def __init__(self, slack_webhook_url=None, email_config=None):
        self.slack_webhook = slack_webhook_url
        self.email_config = email_config

    def send_alert(self, alert_type, message, severity="warning"):
        """Send alert via configured channels"""
        alert_data = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": time.time(),
            "service": "transformers-api"
        }

        # Send to Slack
        if self.slack_webhook:
            self._send_slack_alert(alert_data)

        # Send email
        if self.email_config:
            self._send_email_alert(alert_data)

        # Log alert
        logger = logging.getLogger("alerts")
        logger.warning(f"Alert sent: {alert_type} - {message}")

    def _send_slack_alert(self, alert_data):
        """Send alert to Slack"""
        import requests

        color_map = {
            "info": "good",
            "warning": "#ff9900",
            "error": "danger",
            "critical": "#ff0000"
        }

        payload = {
            "attachments": [{
                "color": color_map.get(alert_data["severity"], "warning"),
                "title": f"🚨 {alert_data['type']} Alert",
                "text": alert_data["message"],
                "fields": [
                    {"title": "Service", "value": alert_data["service"], "short": True},
                    {"title": "Severity", "value": alert_data["severity"], "short": True},
                    {"title": "Time", "value": time.ctime(alert_data["timestamp"]), "short": False}
                ]
            }]
        }

        try:
            requests.post(self.slack_webhook, json=payload)
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")

# Usage
logger = AdvancedLogger()
alerter = AlertManager(slack_webhook_url="your-slack-webhook")

# Log events
logger.log_request("req-123", "POST", "/predict", user_agent="TestClient")
logger.log_inference("req-123", "gpt2", 10, 50, 0.234)

# Send alerts for critical issues
if error_rate > 0.1:  # 10% error rate
    alerter.send_alert("High Error Rate", f"Error rate is {error_rate:.1%}", "error")
```

## 🚀 Scaling Strategies

### Horizontal Scaling with Kubernetes

```yaml
# transformers-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: transformers-api
  namespace: ml-production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: transformers-api
  template:
    metadata:
      labels:
        app: transformers-api
    spec:
      containers:
      - name: api
        image: transformers-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
            nvidia.com/gpu: 1  # GPU request
          limits:
            cpu: 2000m
            memory: 4Gi
            nvidia.com/gpu: 1
        env:
        - name: MODEL_CACHE_DIR
          value: "/app/models"
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
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
      volumes:
      - name: model-cache
        persistentVolumeClaim:
          claimName: model-cache-pvc
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: transformers-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: transformers-api
  minReplicas: 1
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
        name: http_requests_total
      target:
        type: AverageValue
        averageValue: "100"  # 100 requests per second per pod
```

### Load Balancing and Service Mesh

```yaml
# service-mesh-config.yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: transformers-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - transformers-api.example.com
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: transformers-api
spec:
  hosts:
  - transformers-api.example.com
  gateways:
  - transformers-gateway
  http:
  - match:
    - uri:
        prefix: "/api/v1"
    route:
    - destination:
        host: transformers-api
        port:
          number: 8000
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
    trafficPolicy:
      loadBalancer:
        simple: LEAST_REQUEST
      outlierDetection:
        consecutive5xxErrors: 3
        interval: 30s
        baseEjectionTime: 60s
```

## 🔒 Security Best Practices

### API Security

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, Security
import jwt
from datetime import datetime, timedelta
import secrets

class SecurityManager:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.security = HTTPBearer()

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        return encoded_jwt

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(security)):
        """Verify JWT token"""
        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def rate_limit(self, requests_per_minute: int = 60):
        """Rate limiting decorator"""
        def decorator(func):
            request_counts = {}

            @wraps(func)
            async def wrapper(*args, **kwargs):
                client_ip = self._get_client_ip()
                current_time = datetime.now().minute

                # Clean old entries
                request_counts[client_ip] = [
                    req_time for req_time in request_counts.get(client_ip, [])
                    if req_time == current_time
                ]

                # Check rate limit
                if len(request_counts[client_ip]) >= requests_per_minute:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")

                request_counts[client_ip].append(current_time)

                return await func(*args, **kwargs)

            return wrapper
        return decorator

    def _get_client_ip(self):
        """Get client IP (simplified)"""
        # In production, use proper IP extraction from request headers
        return "127.0.0.1"

# Usage in FastAPI
security_manager = SecurityManager()

@app.post("/login")
async def login(username: str, password: str):
    # Verify credentials (implement your logic)
    if username == "admin" and password == "password":
        access_token = security_manager.create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/protected")
async def protected_route(username: str = Depends(security_manager.verify_token)):
    return {"message": f"Hello, {username}!"}

@app.post("/predict")
@security_manager.rate_limit(requests_per_minute=100)
async def predict(request: PredictionRequest, username: str = Depends(security_manager.verify_token)):
    # Authenticated and rate-limited prediction
    result = await perform_prediction(request)
    return result
```

## 📈 Performance Benchmarks

### Benchmarking Script

```python
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import requests

class ModelBenchmarker:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url

    def benchmark_endpoint(self, endpoint="/predict", num_requests=100, concurrent_requests=10):
        """Benchmark API endpoint performance"""
        def make_request():
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.api_url}{endpoint}",
                    json={"text": "This is a sample text for benchmarking."},
                    timeout=30
                )
                response_time = time.time() - start_time

                if response.status_code == 200:
                    return {"success": True, "response_time": response_time}
                else:
                    return {"success": False, "response_time": response_time, "error": response.status_code}

            except Exception as e:
                return {"success": False, "response_time": time.time() - start_time, "error": str(e)}

        # Sequential benchmark
        print("Running sequential benchmark...")
        sequential_times = []
        for i in range(min(num_requests, 10)):  # Limit for sequential
            result = make_request()
            if result["success"]:
                sequential_times.append(result["response_time"])

        # Concurrent benchmark
        print("Running concurrent benchmark...")
        concurrent_results = []
        with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            for future in futures:
                result = future.result()
                concurrent_results.append(result)

        # Calculate metrics
        successful_requests = [r for r in concurrent_results if r["success"]]
        response_times = [r["response_time"] for r in successful_requests]

        return {
            "total_requests": num_requests,
            "successful_requests": len(successful_requests),
            "success_rate": len(successful_requests) / num_requests,
            "sequential_avg_time": statistics.mean(sequential_times) if sequential_times else 0,
            "concurrent_avg_time": statistics.mean(response_times) if response_times else 0,
            "concurrent_p95_time": statistics.quantiles(response_times, n=20)[18] if response_times else 0,  # 95th percentile
            "requests_per_second": len(successful_requests) / sum(response_times) if response_times else 0,
            "error_count": num_requests - len(successful_requests)
        }

    def memory_benchmark(self, model_configs):
        """Benchmark memory usage for different model configurations"""
        memory_results = {}

        for config_name, config in model_configs.items():
            print(f"Benchmarking {config_name}...")

            # Load model and measure memory
            initial_memory = self._get_memory_usage()

            # Simulate model loading and inference
            model_memory = self._simulate_model_usage(config)

            peak_memory = self._get_memory_usage()

            memory_results[config_name] = {
                "initial_memory": initial_memory,
                "model_memory": model_memory,
                "peak_memory": peak_memory,
                "memory_increase": peak_memory - initial_memory
            }

        return memory_results

    def _get_memory_usage(self):
        """Get current memory usage"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB

    def _simulate_model_usage(self, config):
        """Simulate model loading and usage"""
        # This would load actual models in production
        time.sleep(2)  # Simulate loading time
        return 500  # MB (placeholder)

# Usage
benchmarker = ModelBenchmarker()

# API performance benchmark
results = benchmarker.benchmark_endpoint(num_requests=100, concurrent_requests=5)
print("Benchmark Results:")
print(".1f")
print(".1f")
print(".1f")
print(".1f")

# Memory benchmark
model_configs = {
    "base_model": {"model": "bert-base", "quantized": False},
    "quantized_model": {"model": "bert-base", "quantized": True},
    "large_model": {"model": "bert-large", "quantized": False}
}

memory_results = benchmarker.memory_benchmark(model_configs)
for config, metrics in memory_results.items():
    print(f"{config}: {metrics['memory_increase']}MB increase")
```

## 🎯 Production Checklist

### Pre-Deployment Checklist

- [ ] **Model Optimization**
  - [ ] Quantization applied for reduced size
  - [ ] ONNX conversion for cross-platform deployment
  - [ ] GPU acceleration configured
  - [ ] Batch processing optimized

- [ ] **Infrastructure**
  - [ ] Load balancer configured
  - [ ] Auto-scaling policies set
  - [ ] Monitoring and alerting enabled
  - [ ] Backup and recovery procedures tested

- [ ] **Security**
  - [ ] API authentication implemented
  - [ ] Rate limiting configured
  - [ ] Input validation enabled
  - [ ] HTTPS/TLS certificates installed

- [ ] **Performance**
  - [ ] Caching strategies implemented
  - [ ] Database connection pooling configured
  - [ ] Response compression enabled
  - [ ] CDN integration for static assets

### Monitoring Checklist

- [ ] **Application Metrics**
  - [ ] Response times tracked
  - [ ] Error rates monitored
  - [ ] Throughput measured
  - [ ] Resource usage logged

- [ ] **Business Metrics**
  - [ ] User satisfaction scores
  - [ ] Feature usage analytics
  - [ ] Conversion rates tracked
  - [ ] SLA compliance monitored

- [ ] **Alerting**
  - [ ] Critical error alerts configured
  - [ ] Performance degradation alerts
  - [ ] Resource exhaustion warnings
  - [ ] Security incident notifications

## 🚀 Congratulations!

You've successfully mastered the deployment of Transformer models in production! 🎉

### Key Achievements

✅ **Model Optimization**: Quantization, ONNX conversion, GPU acceleration
✅ **High-Performance Serving**: FastAPI, GPU acceleration, concurrent processing
✅ **Monitoring & Observability**: Prometheus, Grafana, logging, alerting
✅ **Scaling Strategies**: Kubernetes, load balancing, auto-scaling
✅ **Security**: Authentication, rate limiting, input validation
✅ **Performance Benchmarks**: Comprehensive testing and optimization

### Production-Ready Skills

- **Deploy ML models** at enterprise scale
- **Optimize inference performance** for real-time applications
- **Monitor and maintain** production AI systems
- **Scale horizontally** to handle increasing loads
- **Ensure security** and compliance in AI deployments

### Next Steps

1. **Explore Advanced Topics**: Model versioning, A/B testing, multi-model serving
2. **Specialize in Domains**: Healthcare, finance, content moderation
3. **Contribute to Open Source**: Improve Transformers ecosystem
4. **Start Production Projects**: Build real-world AI applications

---

**You've transformed from AI enthusiast to production AI engineer!** 🚀

*Mastering Transformers deployment opens doors to building the next generation of AI-powered applications that can serve millions of users reliably and efficiently.*