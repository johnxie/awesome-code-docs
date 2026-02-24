---
layout: default
title: "Chapter 7: Production Deployment"
parent: "LlamaIndex Tutorial"
nav_order: 7
---

# Chapter 7: Production Deployment

Welcome to **Chapter 7: Production Deployment**. In this part of **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy LlamaIndex applications at scale with enterprise-grade reliability and performance.

## 🎯 Overview

This chapter covers production deployment strategies for LlamaIndex applications, including containerization, orchestration, scaling, and operational best practices for running RAG systems in production environments.

## 🐳 Containerization

### Docker Deployment

```yaml
# Dockerfile for LlamaIndex application
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

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
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# requirements.txt
llama-index==0.9.45
llama-index-vector-stores-chroma==0.1.6
llama-index-embeddings-openai==0.1.7
llama-index-llms-openai==0.1.12
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
chromadb==0.4.18
openai==1.3.7
sentence-transformers==2.2.2
numpy==1.24.3
pandas==2.1.4
```

```python
# app.py - FastAPI application
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import time
from contextlib import asynccontextmanager

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import chromadb

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
index = None
query_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await initialize_app()
    yield
    # Shutdown
    await cleanup_app()

app = FastAPI(
    title="LlamaIndex RAG API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = None

class IndexRequest(BaseModel):
    documents: List[Dict[str, Any]]
    collection_name: Optional[str] = "default"

class QueryResponse(BaseModel):
    response: str
    source_nodes: List[Dict[str, Any]]
    metadata: Dict[str, Any]

async def initialize_app():
    """Initialize LlamaIndex components"""
    global index, query_engine

    try:
        logger.info("Initializing LlamaIndex application...")

        # Configure LlamaIndex settings
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        Settings.llm = OpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = chroma_client.get_or_create_collection("documents")

        # Create vector store
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # Create index (will be populated via API if empty)
        index = VectorStoreIndex.from_vector_store(vector_store)

        # Create query engine
        query_engine = index.as_query_engine(similarity_top_k=5)

        logger.info("LlamaIndex application initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

async def cleanup_app():
    """Cleanup resources"""
    logger.info("Cleaning up application resources...")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "index_ready": index is not None,
        "query_engine_ready": query_engine is not None
    }

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the document collection"""
    if not query_engine:
        raise HTTPException(status_code=503, detail="Query engine not ready")

    try:
        # Execute query
        response = query_engine.query(
            request.query,
            similarity_top_k=request.top_k
        )

        # Format source nodes
        source_nodes = []
        for node in response.source_nodes:
            source_nodes.append({
                "id": node.node.id_,
                "text": node.node.text[:500] + "..." if len(node.node.text) > 500 else node.node.text,
                "score": node.score,
                "metadata": node.node.metadata
            })

        return QueryResponse(
            response=str(response),
            source_nodes=source_nodes,
            metadata={
                "query_time": time.time(),
                "total_sources": len(source_nodes)
            }
        )

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.post("/index")
async def index_documents(request: IndexRequest, background_tasks: BackgroundTasks):
    """Index new documents"""
    if not index:
        raise HTTPException(status_code=503, detail="Index not ready")

    try:
        # Add documents in background for large operations
        background_tasks.add_task(process_documents, request.documents, request.collection_name)

        return {
            "status": "indexing_started",
            "message": f"Started indexing {len(request.documents)} documents",
            "collection": request.collection_name
        }

    except Exception as e:
        logger.error(f"Indexing error: {e}")
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

def process_documents(documents_data: List[Dict[str, Any]], collection_name: str):
    """Process and index documents"""
    try:
        from llama_index.core import Document

        # Convert to LlamaIndex documents
        documents = []
        for doc_data in documents_data:
            doc = Document(
                text=doc_data["text"],
                metadata=doc_data.get("metadata", {}),
                id_=doc_data.get("id")
            )
            documents.append(doc)

        # Add to index
        global index
        for doc in documents:
            index.insert(doc)

        # Refresh index
        index.refresh_reflectors()

        logger.info(f"Successfully indexed {len(documents)} documents to {collection_name}")

    except Exception as e:
        logger.error(f"Document processing error: {e}")

@app.get("/stats")
async def get_stats():
    """Get index statistics"""
    if not index:
        raise HTTPException(status_code=503, detail="Index not ready")

    try:
        # Get basic stats
        stats = {
            "total_documents": len(index.docstore.docs) if hasattr(index, 'docstore') else 0,
            "index_type": type(index).__name__,
            "timestamp": time.time()
        }

        return stats

    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Multi-Stage Docker Build

```dockerfile
# Multi-stage Dockerfile for optimized production image
FROM python:3.11-slim as builder

# Install build dependencies
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
FROM python:3.11-slim as production

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Copy application code
WORKDIR /app
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "app:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## ☸️ Kubernetes Deployment

### Complete Kubernetes Manifests

```yaml
# llmaindex-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llamaindex-api
  namespace: ai-production
  labels:
    app: llamaindex-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llamaindex-api
  template:
    metadata:
      labels:
        app: llamaindex-api
    spec:
      containers:
      - name: llamaindex
        image: llamaindex-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: CHROMA_HOST
          value: "chroma-service.ai-production.svc.cluster.local"
        - name: REDIS_URL
          value: "redis://redis-service.ai-production.svc.cluster.local:6379"
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
            nvidia.com/gpu: 1  # GPU request if available
          limits:
            cpu: 2000m
            memory: 4Gi
            nvidia.com/gpu: 1
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
        - name: chroma-storage
          mountPath: /app/chroma_db
      volumes:
      - name: model-cache
        emptyDir: {}
      - name: chroma-storage
        persistentVolumeClaim:
          claimName: chroma-pvc
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: accelerator
                operator: In
                values:
                - nvidia-tesla-k80
                - nvidia-tesla-p100
      tolerations:
      - key: "nvidia.com/gpu"
        operator: "Exists"
        effect: "NoSchedule"

---
apiVersion: v1
kind: Service
metadata:
  name: llamaindex-service
  namespace: ai-production
spec:
  selector:
    app: llamaindex-api
  ports:
  - port: 80
    targetPort: 8000
    name: http
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: llamaindex-ingress
  namespace: ai-production
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - rag-api.yourcompany.com
    secretName: llamaindex-tls
  rules:
  - host: rag-api.yourcompany.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: llamaindex-service
            port:
              number: 80
```

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llamaindex-hpa
  namespace: ai-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llamaindex-api
  minReplicas: 2
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
        averageValue: "100"  # Requests per second per pod
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 20
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
```

## 📊 Monitoring and Observability

### Prometheus Metrics

```python
# monitoring.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import psutil
import threading

class MetricsCollector:
    def __init__(self):
        # HTTP metrics
        self.http_requests_total = Counter(
            'llamaindex_http_requests_total',
            'Total number of HTTP requests',
            ['method', 'endpoint', 'status_code']
        )

        self.http_request_duration_seconds = Histogram(
            'llamaindex_http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )

        # Application metrics
        self.index_size = Gauge(
            'llamaindex_index_size',
            'Number of documents in index'
        )

        self.query_count = Counter(
            'llamaindex_queries_total',
            'Total number of queries processed',
            ['query_type', 'status']
        )

        self.query_duration = Histogram(
            'llamaindex_query_duration_seconds',
            'Query processing duration',
            ['query_type'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )

        # System metrics
        self.memory_usage = Gauge(
            'llamaindex_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.cpu_usage = Gauge(
            'llamaindex_cpu_usage_percent',
            'CPU usage percentage'
        )

        # Start metrics collection
        self._start_metrics_collection()

    def _start_metrics_collection(self):
        """Start background metrics collection"""
        def collect_metrics():
            while True:
                # Update system metrics
                self.memory_usage.set(psutil.Process().memory_info().rss)
                self.cpu_usage.set(psutil.cpu_percent(interval=1))

                # Update application metrics
                if 'index' in globals() and index:
                    try:
                        self.index_size.set(len(index.docstore.docs))
                    except:
                        pass

                time.sleep(30)  # Update every 30 seconds

        thread = threading.Thread(target=collect_metrics, daemon=True)
        thread.start()

    def record_query(self, query_type: str, duration: float, status: str = "success"):
        """Record query metrics"""
        self.query_count.labels(query_type=query_type, status=status).inc()
        self.query_duration.labels(query_type=query_type).observe(duration)

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, metrics_collector: MetricsCollector):
        super().__init__(app)
        self.metrics = metrics_collector

    async def dispatch(self, request: Request, call_next):
        # Record request start
        start_time = time.time()
        method = request.method
        path = request.url.path

        try:
            # Process request
            response = await call_next(request)

            # Record metrics
            duration = time.time() - start_time
            status_code = response.status_code

            self.metrics.http_requests_total.labels(
                method=method, endpoint=path, status_code=status_code
            ).inc()

            self.metrics.http_request_duration_seconds.labels(
                method=method, endpoint=path
            ).observe(duration)

            return response

        except Exception as e:
            # Record error metrics
            duration = time.time() - start_time
            self.metrics.http_requests_total.labels(
                method=method, endpoint=path, status_code=500
            ).inc()
            raise

# Initialize metrics
metrics_collector = MetricsCollector()

# Add to FastAPI app
app.add_middleware(MetricsMiddleware, metrics_collector=metrics_collector)

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

# Enhanced query endpoint with metrics
@app.post("/query")
async def query_documents(request: QueryRequest):
    if not query_engine:
        raise HTTPException(status_code=503, detail="Query engine not ready")

    start_time = time.time()

    try:
        # Execute query
        response = query_engine.query(
            request.query,
            similarity_top_k=request.top_k
        )

        # Record success metrics
        duration = time.time() - start_time
        metrics_collector.record_query("rag_query", duration, "success")

        # Format response...
        return QueryResponse(...)

    except Exception as e:
        # Record error metrics
        duration = time.time() - start_time
        metrics_collector.record_query("rag_query", duration, "error")

        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
```

### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "LlamaIndex RAG System",
    "tags": ["llamaindex", "rag", "ai"],
    "timezone": "browser",
    "panels": [
      {
        "title": "HTTP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(llamaindex_http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Query Performance",
        "type": "heatmap",
        "targets": [
          {
            "expr": "llamaindex_query_duration_seconds",
            "legendFormat": "{{query_type}}"
          }
        ]
      },
      {
        "title": "System Resources",
        "type": "gauge",
        "targets": [
          {
            "expr": "llamaindex_memory_usage_bytes / 1024 / 1024",
            "legendFormat": "Memory Usage (MB)"
          },
          {
            "expr": "llamaindex_cpu_usage_percent",
            "legendFormat": "CPU Usage (%)"
          }
        ]
      },
      {
        "title": "Index Health",
        "type": "stat",
        "targets": [
          {
            "expr": "llamaindex_index_size",
            "legendFormat": "Documents Indexed"
          }
        ]
      }
    ]
  }
}
```

## 🔒 Security Best Practices

### API Security

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKeyHeader
from fastapi import Depends, Security, HTTPException
import jwt
from datetime import datetime, timedelta
import secrets
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Security configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

class AuthManager:
    def __init__(self):
        self.users_db = {}  # In production, use proper database
        self.api_keys = {}  # API key storage

    def create_access_token(self, data: dict):
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def hash_password(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)

    def create_api_key(self, user_id: str) -> str:
        """Create API key for user"""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "active": True
        }
        return api_key

    def verify_api_key(self, api_key: str):
        """Verify API key"""
        if api_key not in self.api_keys:
            return None

        key_data = self.api_keys[api_key]
        if not key_data["active"]:
            return None

        return key_data

# Initialize auth manager
auth_manager = AuthManager()

# Security schemes
token_scheme = HTTPBearer()
api_key_scheme = APIKeyHeader(name="X-API-Key")

# Add rate limiting to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Authentication dependencies
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(token_scheme)
):
    """Get current user from JWT token"""
    return auth_manager.verify_token(credentials.credentials)

async def get_current_user_from_api_key(
    api_key: str = Security(api_key_scheme)
):
    """Get current user from API key"""
    key_data = auth_manager.verify_api_key(api_key)
    if not key_data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key_data

# Protected endpoints
@app.post("/login")
async def login(username: str, password: str):
    """User login endpoint"""
    # Verify credentials (implement proper user database)
    if username == "admin" and auth_manager.verify_password(password, stored_hash):
        access_token = auth_manager.create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@app.post("/query")
@limiter.limit("100/minute")  # Rate limiting
async def secure_query(
    request: QueryRequest,
    current_user: dict = Depends(get_current_user)
):
    """Secure query endpoint with authentication and rate limiting"""

    # Log user activity
    logger.info(f"User {current_user['sub']} queried: {request.query[:50]}...")

    # Implement user-specific logic if needed
    user_id = current_user["sub"]

    # Your query logic here
    result = await perform_secure_query(request, user_id)

    return result

@app.post("/admin/index")
async def admin_index(
    request: IndexRequest,
    current_user: dict = Depends(get_current_user)
):
    """Admin-only indexing endpoint"""
    # Check admin permissions
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Admin indexing logic
    result = await perform_admin_indexing(request)

    return result

@app.post("/apikey/create")
async def create_api_key(current_user: dict = Depends(get_current_user)):
    """Create API key for current user"""
    api_key = auth_manager.create_api_key(current_user["sub"])

    # Store API key securely (don't return in response in production)
    return {
        "message": "API key created",
        "api_key": api_key,  # Remove this in production
        "warning": "Store this key securely - it won't be shown again"
    }
```

## 🚀 Scaling Strategies

### Database Optimization

```python
# scaling.py
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from concurrent.futures import ThreadPoolExecutor
import asyncio

class ScalableRAGSystem:
    def __init__(self, chroma_host: str = "localhost", chroma_port: int = 8000):
        self.chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port
        )
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.query_cache = {}  # Simple in-memory cache

    def create_sharded_index(self, documents, num_shards: int = 4):
        """Create sharded index for better performance"""

        # Split documents into shards
        shard_size = len(documents) // num_shards
        shards = []

        for i in range(num_shards):
            start_idx = i * shard_size
            end_idx = start_idx + shard_size if i < num_shards - 1 else len(documents)
            shard_docs = documents[start_idx:end_idx]

            # Create shard-specific collection
            collection_name = f"documents_shard_{i}"
            collection = self.chroma_client.get_or_create_collection(collection_name)

            # Create vector store for this shard
            vector_store = ChromaVectorStore(chroma_collection=collection)

            # Create index for this shard
            index = VectorStoreIndex.from_documents(
                shard_docs,
                vector_store=vector_store,
                show_progress=True
            )

            shards.append({
                "index": index,
                "collection": collection_name,
                "document_count": len(shard_docs)
            })

        print(f"Created {num_shards} shards with ~{shard_size} documents each")
        return shards

    async def parallel_query(self, shards, query: str, top_k: int = 5):
        """Query across all shards in parallel"""

        async def query_shard(shard):
            """Query a single shard"""
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                self.executor,
                lambda: shard["index"].as_query_engine().query(query)
            )
            return result

        # Query all shards in parallel
        tasks = [query_shard(shard) for shard in shards]
        results = await asyncio.gather(*tasks)

        # Combine and rank results
        combined_nodes = []
        for result in results:
            combined_nodes.extend(result.source_nodes)

        # Sort by score and return top_k
        combined_nodes.sort(key=lambda x: x.score or 0, reverse=True)
        top_nodes = combined_nodes[:top_k]

        # Create combined response
        combined_text = " ".join([node.node.text for node in top_nodes[:3]])
        combined_response = f"Based on multiple sources: {combined_text[:500]}..."

        return {
            "response": combined_response,
            "source_nodes": top_nodes,
            "shards_queried": len(shards)
        }

    def cached_query(self, query: str, ttl_seconds: int = 300):
        """Query with caching"""

        cache_key = hash(query) % 10000  # Simple hash
        current_time = time.time()

        # Check cache
        if cache_key in self.query_cache:
            cached_result, timestamp = self.query_cache[cache_key]
            if current_time - timestamp < ttl_seconds:
                return cached_result, True  # Return cached result

        # Perform query (implement your query logic)
        result = self.perform_query(query)

        # Cache result
        self.query_cache[cache_key] = (result, current_time)

        return result, False  # Return fresh result

    def perform_query(self, query: str):
        """Actual query implementation"""
        # Implement your query logic here
        return {"response": f"Query result for: {query}", "cached": False}

    def batch_query(self, queries: List[str], batch_size: int = 10):
        """Process multiple queries in batches"""

        results = []

        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]

            # Process batch
            batch_results = []
            for query in batch:
                result, cached = self.cached_query(query)
                batch_results.append(result)

            results.extend(batch_results)

            # Small delay between batches to prevent overwhelming
            time.sleep(0.1)

        return results

# Usage
scalable_rag = ScalableRAGSystem()

# Create sharded index
shards = scalable_rag.create_sharded_index(documents, num_shards=4)

# Parallel querying
async def query_example():
    result = await scalable_rag.parallel_query(shards, "What is machine learning?")
    print(f"Parallel query result: {result['response']}")

# Cached querying
result, cached = scalable_rag.cached_query("What is AI?")
print(f"Cached query result: {result['response']}, Cached: {cached}")

# Batch processing
batch_queries = ["Query 1", "Query 2", "Query 3"] * 10
batch_results = scalable_rag.batch_query(batch_queries, batch_size=5)
print(f"Processed {len(batch_results)} queries in batches")
```

## 📈 Performance Benchmarks

### Benchmarking Script

```python
# benchmark.py
import time
import statistics
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
import json

class RAGBenchmarker:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.executor = ThreadPoolExecutor(max_workers=10)

    def benchmark_query_performance(self, queries, concurrent_requests=5):
        """Benchmark query performance under load"""

        print(f"Benchmarking with {len(queries)} queries, {concurrent_requests} concurrent requests")

        # Sequential benchmark
        print("Running sequential benchmark...")
        sequential_times = []
        for query in queries:
            start_time = time.time()
            self._single_query(query)
            sequential_times.append(time.time() - start_time)

        # Concurrent benchmark
        print("Running concurrent benchmark...")
        concurrent_results = []

        async def run_concurrent():
            semaphore = asyncio.Semaphore(concurrent_requests)

            async def limited_query(query):
                async with semaphore:
                    loop = asyncio.get_running_loop()
                    start_time = time.time()
                    result = await loop.run_in_executor(
                        self.executor,
                        self._single_query,
                        query
                    )
                    response_time = time.time() - start_time
                    return response_time

            tasks = [limited_query(query) for query in queries]
            response_times = await asyncio.gather(*tasks)
            return response_times

        # Run concurrent benchmark
        concurrent_times = asyncio.run(run_concurrent())

        # Calculate statistics
        results = {
            "total_queries": len(queries),
            "concurrent_requests": concurrent_requests,
            "sequential": {
                "avg_time": statistics.mean(sequential_times),
                "p95_time": sorted(sequential_times)[int(len(sequential_times) * 0.95)],
                "min_time": min(sequential_times),
                "max_time": max(sequential_times)
            },
            "concurrent": {
                "avg_time": statistics.mean(concurrent_times),
                "p95_time": sorted(concurrent_times)[int(len(concurrent_times) * 0.95)],
                "min_time": min(concurrent_times),
                "max_time": max(concurrent_times),
                "throughput": len(queries) / sum(concurrent_times)
            },
            "speedup": statistics.mean(sequential_times) / statistics.mean(concurrent_times)
        }

        return results

    def _single_query(self, query):
        """Execute single query"""
        try:
            response = requests.post(
                f"{self.api_url}/query",
                json={"query": query, "top_k": 3},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Query failed: {e}")
            return {"error": str(e)}

    def benchmark_indexing_performance(self, document_batches):
        """Benchmark indexing performance"""

        results = []

        for i, batch in enumerate(document_batches):
            print(f"Benchmarking batch {i+1}/{len(document_batches)} ({len(batch)} documents)")

            start_time = time.time()
            result = self._index_documents(batch)
            indexing_time = time.time() - start_time

            batch_result = {
                "batch_size": len(batch),
                "indexing_time": indexing_time,
                "documents_per_second": len(batch) / indexing_time if indexing_time > 0 else 0,
                "success": "error" not in result
            }

            results.append(batch_result)

        # Aggregate results
        total_docs = sum(r["batch_size"] for r in results)
        total_time = sum(r["indexing_time"] for r in results)

        summary = {
            "total_documents": total_docs,
            "total_indexing_time": total_time,
            "overall_docs_per_second": total_docs / total_time if total_time > 0 else 0,
            "batch_results": results
        }

        return summary

    def _index_documents(self, documents):
        """Index batch of documents"""
        try:
            response = requests.post(
                f"{self.api_url}/index",
                json={"documents": documents},
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Indexing failed: {e}")
            return {"error": str(e)}

    def memory_usage_benchmark(self, query_loads):
        """Benchmark memory usage under different loads"""

        import psutil
        process = psutil.Process()

        results = []

        for load_name, queries in query_loads.items():
            print(f"Benchmarking memory usage for {load_name}...")

            # Measure baseline memory
            baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

            # Execute queries
            for query in queries:
                self._single_query(query)

            # Measure peak memory
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB

            results.append({
                "load_type": load_name,
                "query_count": len(queries),
                "baseline_memory": baseline_memory,
                "peak_memory": peak_memory,
                "memory_increase": peak_memory - baseline_memory
            })

        return results

# Usage
benchmarker = RAGBenchmarker()

# Query performance benchmark
test_queries = [
    "What is machine learning?",
    "How do neural networks work?",
    "Explain data science concepts",
    "What are the benefits of AI?"
] * 10  # 40 queries total

performance_results = benchmarker.benchmark_query_performance(
    test_queries,
    concurrent_requests=5
)

print("Query Performance Benchmark Results:")
print(f"Sequential - Avg: {performance_results['sequential']['avg_time']:.3f}s")
print(f"Concurrent - Avg: {performance_results['concurrent']['avg_time']:.3f}s")
print(f"Throughput: {performance_results['concurrent']['throughput']:.2f} queries/sec")
print(f"Speedup: {performance_results['speedup']:.2f}x")

# Memory usage benchmark
query_loads = {
    "light": test_queries[:5],
    "medium": test_queries[:20],
    "heavy": test_queries  # All queries
}

memory_results = benchmarker.memory_usage_benchmark(query_loads)

print("\nMemory Usage Benchmark Results:")
for result in memory_results:
    print(f"{result['load_type']}: {result['memory_increase']:.1f} MB increase")
```

## 🎯 Production Checklist

### Deployment Readiness

- [ ] **Containerization**
  - [ ] Multi-stage Docker builds implemented
  - [ ] Health checks configured
  - [ ] Non-root user setup
  - [ ] Resource limits defined

- [ ] **Orchestration**
  - [ ] Kubernetes manifests created
  - [ ] Horizontal Pod Autoscaling configured
  - [ ] Persistent volumes for data storage
  - [ ] ConfigMaps and Secrets for configuration

- [ ] **Monitoring**
  - [ ] Prometheus metrics exposed
  - [ ] Grafana dashboards created
  - [ ] Alerting rules defined
  - [ ] Log aggregation configured

- [ ] **Security**
  - [ ] Authentication and authorization implemented
  - [ ] API rate limiting configured
  - [ ] HTTPS/TLS certificates installed
  - [ ] Secrets management in place

### Operational Excellence

1. **CI/CD Pipeline**: Automated testing, building, and deployment
2. **Blue-Green Deployments**: Zero-downtime updates
3. **Canary Releases**: Gradual rollout of new features
4. **Rollback Procedures**: Quick recovery from failures
5. **Backup & Recovery**: Regular data backups and tested recovery

### Scaling Considerations

1. **Stateless Design**: Application can be scaled horizontally
2. **Database Sharding**: Data distributed across multiple nodes
3. **Caching Strategy**: Multi-level caching (application, database, CDN)
4. **Load Balancing**: Intelligent request distribution
5. **Auto-scaling**: Automatic scaling based on metrics

## 📈 Next Steps

With production deployment mastered, you're ready for:

- **[Chapter 8: Monitoring & Optimization](08-monitoring-optimization.md)** - Advanced performance tuning and observability

---

**Ready for production deployment? Your LlamaIndex RAG system is now enterprise-ready!** 🚀

*You've successfully deployed a scalable, monitored, and secure RAG system that can handle production workloads with confidence.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `query`, `time` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Production Deployment` as an operating subsystem inside **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `index`, `result`, `documents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `query` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `time`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/run-llama/llama_index)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `query` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Custom Components](06-custom-components.md)
- [Next Chapter: Chapter 8: Monitoring & Optimization](08-monitoring-optimization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
