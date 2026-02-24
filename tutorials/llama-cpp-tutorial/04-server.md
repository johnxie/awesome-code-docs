---
layout: default
title: "llama.cpp Tutorial - Chapter 4: Server Mode"
nav_order: 4
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 4: Server Mode

Welcome to **Chapter 4: Server Mode**. In this part of **llama.cpp Tutorial: Local LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Run llama.cpp as an OpenAI-compatible HTTP server for API access and integration with applications.

## Overview

llama.cpp includes a built-in HTTP server that provides an OpenAI-compatible API. This allows you to use any OpenAI client or library with your local models.

## Starting the Server

### Basic Server Setup

```bash
# Start server with default settings
./llama-server -m model.gguf

# With custom host and port
./llama-server -m model.gguf --host 0.0.0.0 --port 8080

# With verbose logging
./llama-server -m model.gguf --verbose
```

### Advanced Server Configuration

```bash
# Production server configuration
./llama-server -m model.gguf \
    --host 0.0.0.0 \
    --port 8000 \
    --threads $(nproc) \
    --ctx-size 4096 \
    --batch-size 512 \
    --ubatch-size 512 \
    --gpu-layers 0 \
    --flash-attn \
    --mlock \
    --parallel 1 \
    --cont-batching \
    --metrics \
    --log-format json
```

## API Endpoints

The server provides OpenAI-compatible endpoints:

### Chat Completions

```python
import requests

# POST /v1/chat/completions
response = requests.post("http://localhost:8080/v1/chat/completions",
    json={
        "model": "local-model",
        "messages": [
            {"role": "user", "content": "Hello!"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Completions (Legacy)

```python
# POST /v1/completions
response = requests.post("http://localhost:8080/v1/completions",
    json={
        "model": "local-model",
        "prompt": "The capital of France is",
        "max_tokens": 50,
        "temperature": 0.1
    }
)

result = response.json()
print(result["choices"][0]["text"])
```

### Streaming Responses

```python
# Enable streaming
response = requests.post("http://localhost:8080/v1/chat/completions",
    json={
        "model": "local-model",
        "messages": [{"role": "user", "content": "Tell me a story"}],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = line[6:]  # Remove 'data: ' prefix
            if data == '[DONE]':
                break
            try:
                chunk = json.loads(data)
                content = chunk["choices"][0]["delta"].get("content", "")
                print(content, end="", flush=True)
            except json.JSONDecodeError:
                continue
```

## Using OpenAI Client

Drop-in replacement for OpenAI API:

```python
from openai import OpenAI

# Point to your llama.cpp server
client = OpenAI(
    api_key="not-needed",  # Any string works
    base_url="http://localhost:8080/v1"
)

# Use like normal OpenAI API
response = client.chat.completions.create(
    model="local-model",  # Model name doesn't matter
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message.content)
```

## Server Configuration Options

### Performance Tuning

```bash
# High-performance configuration
./llama-server -m model.gguf \
    --threads $(nproc) \
    --ctx-size 4096 \
    --batch-size 2048 \
    --ubatch-size 512 \
    --gpu-layers 35 \     # Use GPU if available
    --flash-attn \        # Flash attention for speed
    --mlock \             # Lock model in RAM
    --no-mmap \          # Alternative memory management
    --numa               # NUMA-aware memory allocation
```

### Multi-Model Support

```bash
# Load multiple models
./llama-server \
    --model models/llama-7b.gguf \
    --model models/mistral-7b.gguf \
    --model models/codellama.gguf \
    --alias llama=llama-7b.gguf \
    --alias mistral=mistral-7b.gguf \
    --alias code=codellama.gguf
```

### Context and Memory

```bash
# Optimize for different use cases
./llama-server -m model.gguf \
    --ctx-size 8192 \     # Large context for analysis
    --rope-scaling yarn \ # YaRN RoPE scaling
    --rope-scale 2.0 \    # Scale factor
    --yarn-ext-factor 1.0 \
    --yarn-attn-factor 1.0 \
    --yarn-beta-fast 32 \
    --yarn-beta-slow 1
```

## Authentication and Security

### API Key Authentication

```bash
# Enable authentication
./llama-server -m model.gguf \
    --api-key sk-your-secret-key

# Use in requests
headers = {"Authorization": "Bearer sk-your-secret-key"}
response = requests.post("http://localhost:8080/v1/chat/completions",
    headers=headers,
    json={...}
)
```

### CORS Configuration

```bash
# Enable CORS for web applications
./llama-server -m model.gguf \
    --cors \
    --cors-origin http://localhost:3000,http://localhost:5173

# Or allow all origins (development only)
./llama-server -m model.gguf --cors
```

## Monitoring and Metrics

### Server Metrics

```bash
# Enable Prometheus metrics
./llama-server -m model.gguf --metrics

# Access metrics at /metrics
curl http://localhost:8080/metrics
```

### Health Checks

```python
# Health endpoint
response = requests.get("http://localhost:8080/health")
if response.status_code == 200:
    print("Server is healthy")
```

### Logging

```bash
# Structured JSON logging
./llama-server -m model.gguf \
    --log-format json \
    --verbose

# Log to file
./llama-server -m model.gguf \
    --log-file server.log \
    --log-verbosity 1
```

## Load Balancing and Scaling

### Multiple Server Instances

```bash
#!/bin/bash
# start_multiple_servers.sh

ports=(8080 8081 8082)
models=("llama-7b.gguf" "mistral-7b.gguf" "codellama.gguf")

for i in "${!ports[@]}"; do
    port=${ports[$i]}
    model=${models[$i]}

    echo "Starting server on port $port with $model"
    ./llama-server -m "models/$model" \
        --port $port \
        --host 0.0.0.0 \
        --threads $(nproc) &
done

wait
```

### Load Balancer Configuration

```yaml
# nginx.conf
upstream llama_backend {
    server localhost:8080;
    server localhost:8081;
    server localhost:8082;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://llama_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Integration Examples

### LangChain Integration

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Use llama.cpp server with LangChain
llm = ChatOpenAI(
    model="local-model",
    openai_api_key="dummy",
    openai_api_base="http://localhost:8080/v1",
    temperature=0.7
)

chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms for a beginner."
    )
)

result = chain.run(topic="quantum computing")
print(result)
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7
    max_tokens: int = 100

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = requests.post("http://localhost:8080/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": request.message}],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return ChatResponse(
                response=result["choices"][0]["message"]["content"]
            )
        else:
            raise HTTPException(status_code=500, detail="LLM server error")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/health")
async def health():
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        return {"status": "healthy" if response.status_code == 200 else "unhealthy"}
    except:
        return {"status": "unhealthy"}
```

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  llama-server:
    build:
      context: .
      dockerfile: Dockerfile.server
    ports:
      - "8080:8080"
    environment:
      - LLAMA_MODEL_PATH=/models/model.gguf
    volumes:
      - ./models:/models:ro
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G

  api-gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - llama-server

  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
```

```dockerfile
# Dockerfile.server
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone and build llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) llama-server

WORKDIR /llama.cpp/build/bin

EXPOSE 8080

CMD ["./llama-server", "-m", "/models/model.gguf", "--host", "0.0.0.0", "--port", "8080"]
```

## Production Deployment

### Systemd Service

```ini
# /etc/systemd/system/llama-server.service
[Unit]
Description=llama.cpp Server
After=network.target

[Service]
Type=simple
User=llama
Group=llama
WorkingDirectory=/opt/llama.cpp
ExecStart=/opt/llama.cpp/build/bin/llama-server \
    -m /opt/models/model.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    --threads 8 \
    --ctx-size 4096 \
    --mlock
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Process Management

```bash
# Install service
sudo systemctl daemon-reload
sudo systemctl enable llama-server
sudo systemctl start llama-server

# Monitor service
sudo systemctl status llama-server
sudo journalctl -u llama-server -f
```

## Performance Optimization

### GPU Acceleration

```bash
# NVIDIA CUDA
./llama-server -m model.gguf \
    --gpu-layers 35 \
    --main-gpu 0 \
    --tensor-split 0,1  # Multi-GPU

# AMD ROCm (Linux)
./llama-server -m model.gguf \
    --gpu-layers 35 \
    --main-gpu 0

# Apple Metal
./llama-server -m model.gguf \
    --gpu-layers 35 \
    --metal
```

### Memory Optimization

```bash
# Large model optimization
./llama-server -m model.gguf \
    --ctx-size 4096 \
    --rope-scaling yarn \
    --rope-scale 2.0 \
    --mlock \
    --memory-f32 \
    --flash-attn
```

### Concurrent Requests

```bash
# Handle multiple requests
./llama-server -m model.gguf \
    --parallel 4 \         # Number of parallel requests
    --cont-batching \      # Continuous batching
    --batch-size 2048 \    # Batch size
    --ubatch-size 512      # Micro batch size
```

## Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check model file exists
ls -la model.gguf

# Check port availability
netstat -tlnp | grep 8080

# Run with verbose logging
./llama-server -m model.gguf --verbose
```

**Out of memory:**
```bash
# Reduce context size
./llama-server -m model.gguf --ctx-size 2048

# Use lower quantization
# Try Q3_K or Q2_K models
```

**Slow responses:**
```bash
# Increase threads
./llama-server -m model.gguf --threads $(nproc)

# Enable GPU layers
./llama-server -m model.gguf --gpu-layers 35

# Use flash attention
./llama-server -m model.gguf --flash-attn
```

**Connection refused:**
```bash
# Check server is running
ps aux | grep llama-server

# Check firewall
sudo ufw status
sudo ufw allow 8080
```

## Best Practices

1. **Resource Planning**: Calculate memory requirements before deployment
2. **Health Checks**: Implement proper health checks and monitoring
3. **Security**: Use authentication and restrict network access
4. **Scaling**: Plan for load balancing and horizontal scaling
5. **Monitoring**: Set up comprehensive logging and metrics
6. **Updates**: Keep llama.cpp updated for performance improvements
7. **Testing**: Thoroughly test your API endpoints before production

The server mode makes llama.cpp accessible via standard HTTP APIs, enabling integration with any application that supports OpenAI-compatible endpoints. This is the most practical way to use llama.cpp in production applications.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `llama`, `server`, `model` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Server Mode` as an operating subsystem inside **llama.cpp Tutorial: Local LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `gguf`, `response`, `size` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Server Mode` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `llama`.
2. **Input normalization**: shape incoming data so `server` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ggerganov/llama.cpp)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `llama` and `server` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Command Line Interface](03-cli-usage.md)
- [Next Chapter: Chapter 5: GPU Acceleration](05-gpu.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
