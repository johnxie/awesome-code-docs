---
layout: default
title: "MCP Python SDK Tutorial - Chapter 6: Production Deployment"
nav_order: 6
parent: MCP Python SDK Tutorial
---

# Chapter 6: Production Deployment

> Deploy MCP servers to production with Docker, monitoring, error handling, and scaling strategies.

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY . .

# Non-root user
RUN useradd -m mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import sys; sys.exit(0)"

CMD ["python", "server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    container_name: mcp-server
    restart: unless-stopped
    environment:
      - LOG_LEVEL=INFO
      - MAX_CONNECTIONS=100
    volumes:
      - ./data:/app/data:ro
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Monitoring

### Logging

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("mcp")
    logger.setLevel(logging.INFO)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        "logs/server.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(file_handler)
    return logger

logger = setup_logging()
```

### Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
tool_calls = Counter('mcp_tool_calls_total', 'Total tool calls', ['tool_name'])
tool_duration = Histogram('mcp_tool_duration_seconds', 'Tool execution time', ['tool_name'])

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    start_time = time.time()

    try:
        result = await execute_tool(name, arguments)
        tool_calls.labels(tool_name=name).inc()
        return result
    finally:
        duration = time.time() - start_time
        tool_duration.labels(tool_name=name).observe(duration)

# Start Prometheus metrics server
start_http_server(9090)
```

## Error Handling

```python
from mcp.types import TextContent
import traceback

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        return await execute_tool(name, arguments)
    except ValueError as e:
        logger.warning(f"Validation error in {name}: {e}")
        return [TextContent(type="text", text=f"❌ Invalid input: {e}")]
    except ConnectionError as e:
        logger.error(f"Connection error in {name}: {e}")
        return [TextContent(type="text", text="🔌 Service temporarily unavailable")]
    except Exception as e:
        logger.exception(f"Unexpected error in {name}")
        return [TextContent(type="text", text="⚠️ Internal server error")]
```

## Health Checks

```python
from datetime import datetime

class HealthMonitor:
    def __init__(self):
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0

    async def check_health(self) -> dict:
        uptime = (datetime.now() - self.start_time).total_seconds()
        error_rate = self.error_count / max(self.request_count, 1)

        return {
            "status": "healthy" if error_rate < 0.1 else "degraded",
            "uptime_seconds": uptime,
            "total_requests": self.request_count,
            "error_rate": error_rate
        }

health = HealthMonitor()

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    health.request_count += 1

    if name == "health":
        status = await health.check_health()
        return [TextContent(type="text", text=json.dumps(status))]
```

## Scaling Strategies

### Horizontal Scaling

```python
# Use Redis for shared state across instances
import redis.asyncio as redis

class SharedCache:
    def __init__(self):
        self.redis = redis.from_url("redis://localhost:6379")

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ttl: int = 3600):
        await self.redis.setex(key, ttl, value)

cache = SharedCache()
```

### Load Balancing (nginx)

```nginx
upstream mcp_servers {
    least_conn;
    server mcp1:8000;
    server mcp2:8000;
    server mcp3:8000;
}

server {
    listen 80;

    location / {
        proxy_pass http://mcp_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Configuration

```python
from pydantic_settings import BaseSettings

class ProductionConfig(BaseSettings):
    # Server
    server_name: str = "mcp-prod"
    max_connections: int = 1000
    timeout_seconds: int = 30

    # Security
    api_key_required: bool = True
    allowed_origins: list[str] = ["https://app.example.com"]

    # Monitoring
    log_level: str = "INFO"
    metrics_port: int = 9090

    # Database
    database_url: str

    class Config:
        env_file = ".env.production"

config = ProductionConfig()
```

## Deployment Checklist

- ✅ Docker image built and tested
- ✅ Environment variables configured
- ✅ Logging configured with rotation
- ✅ Monitoring and metrics enabled
- ✅ Health checks implemented
- ✅ Error handling comprehensive
- ✅ Security hardened (no secrets in code)
- ✅ Rate limiting configured
- ✅ Backups configured for stateful data
- ✅ CI/CD pipeline set up

## Next Steps

Chapter 7 covers client integration with Claude Code, Claude.ai, and custom applications.

**Continue to:** [Chapter 7: Client Integration](07-client-integration.md)

---

*Previous: [← Chapter 5: Authentication & Security](05-authentication-security.md)*
