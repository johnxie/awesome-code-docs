---
layout: default
title: "LocalAI Tutorial - Chapter 7: Configuration"
nav_order: 7
has_children: false
parent: LocalAI Tutorial
---

# Chapter 7: Advanced Configuration and Tuning

> Optimize LocalAI performance with advanced configuration options, hardware tuning, and production settings.

## Overview

LocalAI offers extensive configuration options for performance tuning, hardware optimization, and production deployment.

## Configuration File Structure

### Main Configuration

```yaml
# config.yaml - Main LocalAI configuration
debug: true
threads: 8
context_size: 4096
f16: false
mlock: true
mmap: true

# Model library
model_library:
  - url: "https://raw.githubusercontent.com/mudler/LocalAI/master/gallery/index.yaml"
    name: "model-gallery"

# Preload models
preload_models:
  - name: phi-2
    parameters:
      model: phi-2.Q4_K_M.gguf
      temperature: 0.7
  - name: stablediffusion
    parameters:
      height: 512
      width: 512

# API settings
api_keys:
  - sk-local-key-1
  - sk-local-key-2

rate_limits:
  requests_per_minute: 60
  tokens_per_minute: 40000
```

## Hardware-Specific Optimization

### CPU Optimization

```yaml
# CPU-optimized configuration
cpu_optimization:
  threads: 8                    # Match CPU cores
  batch_size: 512              # Batch processing
  ubatch_size: 512             # Micro batch size
  context_size: 4096           # Context window
  f16: false                   # Use f32 for compatibility
  mlock: true                  # Lock model in RAM
  mmap: true                   # Memory mapping
  numa: false                  # NUMA awareness

# AVX instruction sets
instruction_sets:
  avx: true
  avx2: true
  avx512: true
  fma: true
  f16c: true
```

### GPU Optimization

```yaml
# GPU configuration for different backends
gpu_config:
  # CUDA (NVIDIA)
  cuda:
    gpu_layers: 35             # Layers to offload
    main_gpu: 0                # Primary GPU
    tensor_split: "0.5,0.5"    # Multi-GPU split
    low_vram: false            # Low VRAM mode

  # Metal (Apple Silicon)
  metal:
    gpu_layers: 35
    mlock: true
    mmap: true

  # ROCm (AMD)
  rocm:
    gpu_layers: 35
    main_gpu: 0
    tensor_split: "0.7,0.3"
```

## Model-Specific Tuning

### LLM Configuration

```yaml
# Advanced LLM settings
llm_config:
  # Generation parameters
  temperature: 0.8
  top_p: 0.9
  top_k: 40
  min_p: 0.0
  tfs_z: 1.0
  typical_p: 1.0
  repeat_penalty: 1.1
  repeat_last_n: 64
  presence_penalty: 0.0
  frequency_penalty: 0.0

  # Mirostat sampling
  mirostat: 0
  mirostat_lr: 0.1
  mirostat_ent: 5.0

  # Context and memory
  context_size: 4096
  rope_scaling: "yarn"
  rope_scale: 2.0
  yarn_ext_factor: 1.0
  yarn_attn_factor: 1.0
  yarn_beta_fast: 32
  yarn_beta_slow: 1

  # Performance
  flash_attn: true
  cache_type_k: "f16"
  cache_type_v: "f16"
```

### Image Generation Tuning

```yaml
# Stable Diffusion optimization
stablediffusion_config:
  # Quality settings
  steps: 25
  guidance_scale: 7.5
  height: 512
  width: 512

  # Performance
  batch_size: 1
  vae_slicing: true
  attention_slicing: true
  cpu_offload: false

  # Memory optimization
  enable_model_cpu_offload: false
  enable_sequential_cpu_offload: false
  low_vram_mode: false

  # Advanced
  denoising_strength: 1.0
  negative_prompt_strength: 1.0
```

### Audio Processing Settings

```yaml
# Whisper configuration
whisper_config:
  model: "large-v3"
  language: "auto"
  translate: false
  threads: 4
  processors: 1
  offset_ms: 0
  duration_ms: 0
  no_context: false
  suppress_blank: true
  suppress_non_speech_tokens: true

# TTS configuration
tts_config:
  model: "tts-1"
  voice: "alloy"
  speed: 1.0
  response_format: "mp3"
  length_penalty: 1.0
  repetition_penalty: 1.0
  top_k: 50
  top_p: 0.9
  temperature: 0.8
```

## Production Configuration

### Docker Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  localai:
    image: localai/localai:latest-gpu-nvidia-cuda-12
    ports:
      - "8080:8080"
    environment:
      - DEBUG=false
      - THREADS=16
      - MODELS_PATH=/models
      - GALLERY_MODELS_PATH=/models/gallery
    volumes:
      - ./models:/models:cached
      - ./config.yaml:/config.yaml:ro
    deploy:
      resources:
        limits:
          cpus: '16.0'
          memory: 32G
        reservations:
          cpus: '8.0'
          memory: 16G
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/readyz"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis for caching (optional)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  redis_data:
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: localai
  labels:
    app: localai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: localai
  template:
    metadata:
      labels:
        app: localai
    spec:
      containers:
      - name: localai
        image: localai/localai:latest-cpu
        ports:
        - containerPort: 8080
        env:
        - name: THREADS
          value: "8"
        - name: MODELS_PATH
          value: "/models"
        resources:
          requests:
            memory: "8Gi"
            cpu: "4"
          limits:
            memory: "16Gi"
            cpu: "8"
        volumeMounts:
        - name: models-volume
          mountPath: /models
        - name: config-volume
          mountPath: /config.yaml
          subPath: config.yaml
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: models-volume
        persistentVolumeClaim:
          claimName: localai-models-pvc
      - name: config-volume
        configMap:
          name: localai-config

---
apiVersion: v1
kind: Service
metadata:
  name: localai-service
spec:
  selector:
    app: localai
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## Caching and Performance

### Response Caching

```yaml
# Enable caching
cache_config:
  enabled: true
  type: redis
  host: localhost
  port: 6379
  password: ""
  ttl: 3600  # 1 hour

  # Semantic caching
  semantic_cache:
    enabled: true
    threshold: 0.8  # Similarity threshold
    max_size: 10000

# Model caching
model_cache:
  enabled: true
  preload_models: true
  unload_models_after: 3600  # Unload after 1 hour of inactivity
```

### Connection Pooling

```yaml
# HTTP client configuration
http_config:
  max_connections: 100
  max_keepalive_connections: 20
  keepalive_timeout: 30
  timeout: 300

# Database configuration (if using external DB)
database_config:
  type: sqlite  # or postgresql
  path: /tmp/localai.db
  max_connections: 10
  connection_timeout: 30
```

## Security Configuration

### API Security

```yaml
# Security settings
security_config:
  # API keys
  api_keys:
    - sk-production-key-1
    - sk-production-key-2

  # CORS settings
  cors:
    enabled: true
    allowed_origins:
      - "https://yourapp.com"
      - "http://localhost:3000"
    allowed_methods: ["GET", "POST", "PUT", "DELETE"]
    allowed_headers: ["*"]
    allow_credentials: true

  # Rate limiting
  rate_limiting:
    enabled: true
    requests_per_minute: 100
    tokens_per_minute: 100000
    burst_limit: 20

  # Request validation
  validation:
    max_request_size: "10MB"
    max_prompt_length: 10000
    allowed_file_types: ["wav", "mp3", "png", "jpg"]
```

### Model Security

```yaml
# Model security settings
model_security:
  # Disable dangerous models
  disabled_models: []
  
  # Sandboxing
  sandbox:
    enabled: true
    max_memory: "4GB"
    max_cpu_time: 300  # seconds
    allowed_syscalls: ["read", "write", "open", "close"]
  
  # Content filtering
  content_filter:
    enabled: true
    blocked_words: ["inappropriate", "harmful"]
    prompt_injection_detection: true
```

## Monitoring and Observability

### Logging Configuration

```yaml
# Logging settings
logging_config:
  level: INFO
  format: json
  output: stderr
  
  # File logging
  file_logging:
    enabled: true
    path: /var/log/localai.log
    max_size: "100MB"
    max_files: 5
  
  # External logging
  external_logging:
    sentry:
      enabled: false
      dsn: "your-sentry-dsn"
    datadog:
      enabled: false
      api_key: "your-datadog-key"
```

### Metrics Collection

```yaml
# Metrics configuration
metrics_config:
  enabled: true
  path: /metrics
  
  # Prometheus format
  prometheus:
    enabled: true
    namespace: localai
    
  # Custom metrics
  custom_metrics:
    - name: requests_total
      type: counter
      help: Total number of requests
    - name: request_duration_seconds
      type: histogram
      help: Request duration in seconds
      buckets: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
```

## Scaling Configuration

### Horizontal Scaling

```yaml
# Load balancer configuration
load_balancer:
  algorithm: round_robin
  health_check:
    enabled: true
    path: /health
    interval: 30
    timeout: 10
    unhealthy_threshold: 3
    healthy_threshold: 2

# Auto-scaling
auto_scaling:
  enabled: true
  min_instances: 2
  max_instances: 10
  cpu_threshold: 70
  memory_threshold: 80
  scale_up_cooldown: 300
  scale_down_cooldown: 600
```

### Model Distribution

```yaml
# Multi-model deployment
model_distribution:
  # Assign models to specific instances
  instance_1:
    models: ["phi-2", "mistral-7b"]
    gpu_required: false
  
  instance_2:
    models: ["llama-70b", "stablediffusion"]
    gpu_required: true
  
  # Load balancing
  routing:
    llm: round_robin
    image: least_loaded
    audio: fastest_response
```

## Troubleshooting Configuration

### Debug Mode

```yaml
# Enable detailed debugging
debug_config:
  enabled: true
  verbose: true
  log_level: DEBUG
  
  # Component debugging
  components:
    llama: true
    stablediffusion: true
    whisper: true
    tts: true
    
  # Performance profiling
  profiling:
    enabled: true
    profile_cpu: true
    profile_memory: true
    profile_gpu: true
```

### Health Checks

```yaml
# Comprehensive health checks
health_checks:
  enabled: true
  
  # Basic health
  basic:
    path: /health
    interval: 30
    
  # Model health
  models:
    enabled: true
    path: /models/health
    interval: 60
    
  # Resource health
  resources:
    enabled: true
    cpu_threshold: 90
    memory_threshold: 90
    disk_threshold: 90
```

## Best Practices

1. **Resource Planning**: Calculate memory requirements before deployment
2. **Configuration Management**: Use version control for configuration files
3. **Environment Separation**: Different configs for dev/staging/prod
4. **Monitoring**: Implement comprehensive logging and metrics
5. **Security**: Enable authentication and rate limiting in production
6. **Backup**: Regular configuration and model backups
7. **Testing**: Validate configurations before deployment
8. **Documentation**: Document custom configurations and tuning decisions

Next: Build production applications integrating LocalAI with web services and APIs. 