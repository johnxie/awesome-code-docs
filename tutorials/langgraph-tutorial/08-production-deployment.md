---
layout: default
title: "Chapter 8: Production Deployment"
parent: "LangGraph Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Congratulations! You've made it to the final chapter of our LangGraph journey. By now, you understand how to build stateful multi-actor applications with graphs, nodes, edges, conditional logic, tool integration, and persistence. Now it's time to take your applications from development to **production deployment**!

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `state`, `time`, `request` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment` as an operating subsystem inside **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `user_id`, `langgraph`, `session_id` as your checklist when adapting these patterns to your own repository.

## Understanding Production Deployment

Production deployment means your LangGraph applications are:
- **Reliable**: They handle failures gracefully and recover automatically
- **Scalable**: They can handle increased load without performance degradation
- **Monitorable**: You can track performance, errors, and usage patterns
- **Secure**: They protect user data and API keys
- **Cost-effective**: They optimize resource usage and AI model costs

### Production Architecture Overview

```mermaid
graph TB
    A[User Request] --> B[Load Balancer]
    B --> C[API Gateway]
    C --> D[Application Server]
    D --> E[LangGraph Application]
    E --> F[Checkpoint Storage]
    E --> G[External APIs/Tools]
    E --> H[Vector Databases]
    E --> I[Cache Layer]

    J[Monitoring] --> D
    K[Logging] --> D
    L[Metrics] --> D

    classDef infrastructure fill:#e1f5fe,stroke:#01579b
    classDef application fill:#f3e5f5,stroke:#4a148c
    classDef external fill:#fff3e0,stroke:#ef6c00
    classDef monitoring fill:#e8f5e8,stroke:#1b5e20

    class A,B,C infrastructure
    class D,E application
    class F,G,H,I external
    class J,K,L monitoring
```

## Building Production-Ready LangGraph Applications

### 1. Application Structure

```python
# production_app.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import logging
import time
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production state with validation
class ProductionState(BaseModel):
    messages: list
    current_step: str
    user_id: str
    session_id: str
    request_id: Optional[str] = None
    start_time: float = time.time()
    error_count: int = 0

    class Config:
        arbitrary_types_allowed = True

# FastAPI models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    processing_time: float

# Initialize components
app = FastAPI(title="LangGraph Production API", version="1.0.0")

# Production checkpoint saver
checkpoint_saver = PostgresSaver.from_conn_string(
    "postgresql://user:pass@prod-db:5432/langgraph"
)

# Global graph instance
production_graph = None

@app.on_event("startup")
async def startup_event():
    """Initialize production components."""
    global production_graph
    production_graph = create_production_graph()
    logger.info("Production LangGraph application started")

def create_production_graph():
    """Create the main production graph."""

    def validate_request(state: dict) -> dict:
        """Validate incoming request."""
        if not state.get("user_id"):
            raise ValueError("user_id is required")
        if not state.get("messages"):
            raise ValueError("messages cannot be empty")

        return {
            **state,
            "validated": True,
            "request_id": f"req_{int(time.time())}_{state['user_id']}"
        }

    def process_message(state: dict) -> dict:
        """Process the user message."""
        try:
            # Your message processing logic here
            response = generate_ai_response(state["messages"])

            return {
                **state,
                "response": response,
                "current_step": "completed",
                "processing_time": time.time() - state["start_time"]
            }

        except Exception as e:
            logger.error(f"Processing failed for user {state['user_id']}: {str(e)}")
            return {
                **state,
                "error": str(e),
                "current_step": "failed",
                "error_count": state.get("error_count", 0) + 1
            }

    # Build graph
    graph = StateGraph(dict)
    graph.add_node("validate", validate_request)
    graph.add_node("process", process_message)

    graph.set_entry_point("validate")
    graph.add_edge("validate", "process")
    graph.add_edge("process", END)

    # Compile with production checkpoint saver
    return graph.compile(checkpointer=checkpoint_saver)
```

### 2. API Endpoints

```python
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint with production features."""

    start_time = time.time()
    request_id = f"req_{int(start_time)}_{request.user_id}"

    try:
        # Get or create session
        session_id = request.session_id or f"session_{request.user_id}_{int(start_time)}"
        config = {"configurable": {"thread_id": session_id}}

        # Get existing state for session
        existing_state = production_graph.get_state(config)

        if existing_state:
            # Resume existing session
            state = existing_state.values
            state["messages"].append({"role": "user", "content": request.message})
        else:
            # Start new session
            state = {
                "messages": [{"role": "user", "content": request.message}],
                "current_step": "start",
                "user_id": request.user_id,
                "session_id": session_id,
                "request_id": request_id,
                "start_time": start_time
            }

        # Execute graph
        result = production_graph.invoke(state, config)

        # Log successful request
        processing_time = time.time() - start_time
        logger.info(f"Request {request_id} completed in {processing_time:.2f}s")

        return ChatResponse(
            response=result.get("response", "Sorry, I encountered an error."),
            session_id=session_id,
            processing_time=processing_time
        )

    except Exception as e:
        # Log error
        processing_time = time.time() - start_time
        logger.error(f"Request {request_id} failed after {processing_time:.2f}s: {str(e)}")

        # Return error response
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/session/{session_id}")
async def get_session_state(session_id: str):
    """Get session state for debugging."""
    config = {"configurable": {"thread_id": session_id}}
    state = production_graph.get_state(config)

    if state:
        return {
            "session_id": session_id,
            "current_step": state.values.get("current_step"),
            "message_count": len(state.values.get("messages", [])),
            "last_updated": state.metadata.get("timestamp")
        }
    else:
        raise HTTPException(status_code=404, detail="Session not found")
```

## Scaling and Performance Optimization

### 1. Horizontal Scaling

```python
# docker-compose.yml for scaling
version: '3.8'
services:
  langgraph-app:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/langgraph
      - REDIS_URL=redis://redis:6379
    deploy:
      replicas: 3  # Scale to 3 instances
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=langgraph
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 2. Caching Layer

```python
import redis
from functools import lru_cache

# Redis for distributed caching
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

def cache_response(func):
    """Decorator to cache function responses."""
    def wrapper(*args, **kwargs):
        # Create cache key
        key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

        # Check cache
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)

        # Execute function
        result = func(*args, **kwargs)

        # Cache result (expire in 1 hour)
        redis_client.setex(key, 3600, json.dumps(result))

        return result
    return wrapper

@lru_cache(maxsize=1000)
def cached_ai_response(messages_hash: str):
    """Cache AI responses based on message content hash."""
    # Your AI response generation logic
    pass
```

### 3. Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Production database connection pool
engine = create_engine(
    "postgresql://user:pass@prod-db:5432/langgraph",
    poolclass=QueuePool,
    pool_size=10,          # Maximum connections
    max_overflow=20,       # Additional connections when pool is full
    pool_timeout=30,       # Timeout for getting connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    echo=False
)

# Use connection pool in your graph nodes
def database_operation(state):
    """Perform database operation with pooled connection."""
    with engine.connect() as conn:
        # Your database operations here
        result = conn.execute("SELECT * FROM user_data WHERE user_id = %s",
                            (state["user_id"],))
        return {**state, "db_result": result.fetchall()}
```

## Monitoring and Observability

### 1. Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
REQUEST_COUNT = Counter('langgraph_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('langgraph_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
ACTIVE_SESSIONS = Gauge('langgraph_active_sessions', 'Active sessions')
ERROR_COUNT = Counter('langgraph_errors_total', 'Total errors', ['type'])

# Middleware for metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    # Record metrics
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(
        time.time() - start_time
    )

    if response.status_code >= 400:
        ERROR_COUNT.labels(type="http_error").inc()

    return response

# Start metrics server
start_http_server(8001)  # Metrics available at /metrics
```

### 2. Structured Logging

```python
import structlog
from pythonjsonlogger import jsonlogger

# Configure structured logging
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
        jsonlogger.JsonFormatter()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage in your application
def process_with_logging(state):
    """Process with comprehensive logging."""
    logger.info(
        "Processing request",
        user_id=state.get("user_id"),
        session_id=state.get("session_id"),
        message_count=len(state.get("messages", [])),
        request_id=state.get("request_id")
    )

    try:
        result = process_message(state)

        logger.info(
            "Request completed successfully",
            request_id=state.get("request_id"),
            processing_time=result.get("processing_time", 0),
            current_step=result.get("current_step")
        )

        return result

    except Exception as e:
        logger.error(
            "Request processing failed",
            request_id=state.get("request_id"),
            error=str(e),
            exc_info=True
        )
        raise
```

### 3. Health Checks and Alerts

```python
from fastapi import APIRouter
import psutil
import time

router = APIRouter()

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics."""

    # Database health
    db_healthy = check_database_health()

    # Redis health
    redis_healthy = check_redis_health()

    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    health_status = {
        "timestamp": time.time(),
        "database": "healthy" if db_healthy else "unhealthy",
        "redis": "healthy" if redis_healthy else "unhealthy",
        "cpu_usage": f"{cpu_percent}%",
        "memory_usage": f"{memory.percent}%",
        "disk_usage": f"{disk.percent}%",
        "active_connections": get_active_connection_count()
    }

    # Determine overall health
    overall_healthy = all([
        db_healthy,
        redis_healthy,
        cpu_percent < 90,
        memory.percent < 90,
        disk.percent < 90
    ])

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "details": health_status
    }

def check_database_health():
    """Check database connectivity."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False

def check_redis_health():
    """Check Redis connectivity."""
    try:
        redis_client.ping()
        return True
    except Exception:
        return False
```

## Security and Compliance

### 1. API Security

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

security = HTTPBearer()

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/chat")
async def secure_chat_endpoint(
    request: ChatRequest,
    user_id: str = Depends(verify_token)
):
    """Secure chat endpoint with authentication."""
    # User is now authenticated
    request.user_id = user_id
    return await chat_endpoint(request)
```

### 2. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Add rate limiting to FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.post("/chat")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def rate_limited_chat(request: ChatRequest):
    """Rate limited chat endpoint."""
    return await chat_endpoint(request)
```

### 3. Data Encryption

```python
from cryptography.fernet import Fernet
import base64
import os

# Generate encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data before storage."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data when needed."""
    return cipher.decrypt(encrypted_data.encode()).decode()

# Use in your graph
def process_sensitive_data(state):
    """Process data with encryption."""
    sensitive_info = state.get("api_key", "")

    # Encrypt before storing in checkpoint
    encrypted_key = encrypt_sensitive_data(sensitive_info)

    return {
        **state,
        "encrypted_api_key": encrypted_key,
        "api_key": None  # Remove from state
    }
```

## Cost Optimization

### 1. Model Selection and Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_model_inference(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Cache model inferences to reduce API costs."""

    # Create cache key from prompt
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    cache_key = f"{model}:{prompt_hash}"

    # Check Redis cache first
    cached_response = redis_client.get(cache_key)
    if cached_response:
        return cached_response

    # Make API call
    response = call_openai_api(prompt, model)

    # Cache response (expire in 1 hour)
    redis_client.setex(cache_key, 3600, response)

    return response

def select_model_based_on_complexity(prompt: str) -> str:
    """Select appropriate model based on prompt complexity."""

    # Simple prompts use cheaper model
    if len(prompt.split()) < 50:
        return "gpt-3.5-turbo"

    # Complex prompts use more capable model
    return "gpt-4"
```

### 2. Usage Monitoring

```python
class CostTracker:
    """Track and monitor API usage costs."""

    def __init__(self):
        self.usage = {
            "gpt-3.5-turbo": {"tokens": 0, "cost": 0.0},
            "gpt-4": {"tokens": 0, "cost": 0.0}
        }

    def track_usage(self, model: str, tokens: int):
        """Track token usage and calculate costs."""

        # Pricing per 1K tokens (example rates)
        rates = {
            "gpt-3.5-turbo": 0.002,
            "gpt-4": 0.03
        }

        cost = (tokens / 1000) * rates.get(model, 0)

        self.usage[model]["tokens"] += tokens
        self.usage[model]["cost"] += cost

        # Log cost information
        logger.info(f"Model usage: {model}, tokens: {tokens}, cost: ${cost:.4f}")

        # Alert if cost exceeds threshold
        if self.usage[model]["cost"] > 100:  # $100 daily limit
            alert_admin(f"High cost alert for {model}: ${self.usage[model]['cost']:.2f}")

cost_tracker = CostTracker()
```

## Deployment Strategies

### 1. Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
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

# Run application
CMD ["uvicorn", "production_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langgraph-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: langgraph-app
  template:
    metadata:
      labels:
        app: langgraph-app
    spec:
      containers:
      - name: langgraph-app
        image: your-registry/langgraph-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: database-url
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
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
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 3. CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: |
        pip install -r requirements.txt
        python -m pytest tests/ -v

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Build Docker image
      run: |
        docker build -t your-registry/langgraph-app:${{ github.sha }} .
        docker push your-registry/langgraph-app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/langgraph-app langgraph-app=your-registry/langgraph-app:${{ github.sha }}
        kubectl rollout status deployment/langgraph-app
```

## Production Monitoring Dashboard

```python
# monitoring_dashboard.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import prometheus_client
from prometheus_client import Gauge, Counter, Histogram
import time

monitoring_app = FastAPI()

# Production metrics
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration in seconds', ['endpoint'])
ERROR_RATE = Counter('errors_total', 'Total errors', ['type'])

@monitoring_app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return HTMLResponse(prometheus_client.generate_latest())

@monitoring_app.get("/dashboard")
async def dashboard():
    """Simple monitoring dashboard."""
    # Get current metrics
    active_users = ACTIVE_USERS._value
    error_count = ERROR_RATE._value

    html = f"""
    <html>
    <head><title>LangGraph Production Dashboard</title></head>
    <body>
        <h1>LangGraph Production Dashboard</h1>
        <div>
            <h2>Current Metrics</h2>
            <p>Active Users: {active_users}</p>
            <p>Total Errors: {error_count}</p>
            <p>System Health: <span style="color: green;">Healthy</span></p>
        </div>
        <div>
            <h2>Recent Activity</h2>
            <p>Last deployment: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html)
```

## Best Practices Summary

### 1. **Infrastructure**
- Use managed databases (RDS, Cloud SQL) for production
- Implement proper load balancing
- Set up auto-scaling based on CPU/memory usage
- Use CDN for static assets

### 2. **Security**
- Always use HTTPS in production
- Implement proper authentication and authorization
- Store secrets in environment variables or secret managers
- Regularly update dependencies for security patches

### 3. **Monitoring**
- Set up alerts for key metrics (error rate, response time, resource usage)
- Implement distributed tracing for complex requests
- Log structured data for easy analysis
- Monitor costs and set up budget alerts

### 4. **Performance**
- Implement caching at multiple levels (application, database, CDN)
- Optimize database queries and connection pooling
- Use async/await for I/O operations
- Profile and optimize memory usage

### 5. **Reliability**
- Implement proper error handling and recovery
- Use circuit breakers for external service calls
- Set up proper backup and disaster recovery
- Test failure scenarios regularly

## Congratulations!

🎉 **You've successfully completed the LangGraph tutorial!** 🎉

You've learned how to:
- **Build stateful multi-actor applications** with LangGraph
- **Implement complex workflows** with nodes and edges
- **Add conditional logic** for dynamic behavior
- **Integrate external tools and APIs**
- **Implement persistence and checkpoints** for reliability
- **Deploy production-ready applications** with monitoring and scaling

Your LangGraph applications are now ready to handle real-world production workloads with confidence!

## What's Next?

Now that you have production deployment skills, consider:
- **Exploring advanced LangGraph features** like streaming and custom node types
- **Building multi-agent systems** with specialized agents
- **Integrating with other AI frameworks** like LangChain, LlamaIndex
- **Contributing to the LangGraph ecosystem** with your own tools and patterns

Remember, the journey doesn't end here. AI development is an exciting, ever-evolving field. Keep building, keep learning, and keep pushing the boundaries of what's possible with AI!

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `state`.
2. **Input normalization**: shape incoming data so `time` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `request`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `state` and `time` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Persistence and Checkpoints](07-persistence-checkpoints.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
