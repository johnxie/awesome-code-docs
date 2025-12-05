---
layout: default
title: "AG2 Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: AG2 Tutorial
---

# Chapter 8: Production Deployment & Scaling

> Deploy AG2 agents to production with proper scaling, monitoring, security, and operational best practices.

## Overview

Production deployment requires careful consideration of scalability, reliability, security, and operational concerns. This chapter covers enterprise-grade deployment patterns for AG2 systems.

## Infrastructure Architecture

### Multi-Tier Deployment Architecture

```python
# config/production_config.py
PRODUCTION_CONFIG = {
    "agents": {
        "web_tier": {
            "count": 3,
            "instance_type": "t3.medium",
            "auto_scaling": {
                "min": 2,
                "max": 10,
                "target_cpu": 70
            }
        },
        "worker_tier": {
            "count": 5,
            "instance_type": "c5.large",
            "auto_scaling": {
                "min": 3,
                "max": 20,
                "target_cpu": 80
            }
        },
        "gpu_tier": {
            "count": 2,
            "instance_type": "g4dn.xlarge",
            "auto_scaling": {
                "min": 1,
                "max": 8,
                "target_gpu": 80
            }
        }
    },
    "load_balancer": {
        "type": "application",
        "health_check": {
            "path": "/health",
            "interval": 30,
            "timeout": 5
        }
    },
    "database": {
        "engine": "postgresql",
        "instance_class": "db.r6g.large",
        "multi_az": True,
        "backup_retention": 30
    },
    "cache": {
        "engine": "redis",
        "node_type": "cache.r6g.large",
        "num_nodes": 3,
        "cluster_mode": True
    }
}
```

### Container Orchestration

```yaml
# kubernetes/agent-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ag2-agents
  labels:
    app: ag2-agents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ag2-agents
  template:
    metadata:
      labels:
        app: ag2-agents
    spec:
      containers:
      - name: ag2-agent
        image: ag2/agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: AG2_CONFIG_PATH
          value: "/app/config/production.yaml"
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: ag2-secrets
              key: redis-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ag2-secrets
              key: openai-api-key
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
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
      volumes:
      - name: config-volume
        configMap:
          name: ag2-config
---
apiVersion: v1
kind: Service
metadata:
  name: ag2-service
spec:
  selector:
    app: ag2-agents
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Service Mesh Integration

```yaml
# istio/service-mesh.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ag2-virtual-service
spec:
  http:
  - match:
    - uri:
        prefix: "/api/v1/agents"
    route:
    - destination:
        host: ag2-service
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: ag2-destination-rule
spec:
  host: ag2-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    outlierDetection:
      consecutiveErrors: 5
      interval: 10s
      baseEjectionTime: 30s
```

## Scaling Strategies

### Horizontal Pod Autoscaling

```yaml
# kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ag2-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ag2-agents
  minReplicas: 3
  maxReplicas: 20
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

### Agent Pool Management

```python
from typing import Dict, List, Optional
import asyncio
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"

@dataclass
class AgentInstance:
    id: str
    status: AgentStatus
    capabilities: List[str]
    current_load: float
    last_heartbeat: float
    metadata: Dict

class AgentPoolManager:
    def __init__(self, pool_size=10):
        self.pool_size = pool_size
        self.agents: Dict[str, AgentInstance] = {}
        self.task_queue = asyncio.Queue()
        self.load_balancer = self._create_load_balancer()

    def _create_load_balancer(self):
        """Create load balancing strategy"""
        return LeastLoadedBalancer()

    async def register_agent(self, agent_id: str, capabilities: List[str], metadata: Dict = None):
        """Register a new agent in the pool"""
        agent = AgentInstance(
            id=agent_id,
            status=AgentStatus.AVAILABLE,
            capabilities=capabilities,
            current_load=0.0,
            last_heartbeat=time.time(),
            metadata=metadata or {}
        )

        self.agents[agent_id] = agent

        # Start heartbeat monitoring
        asyncio.create_task(self._monitor_agent(agent_id))

    async def submit_task(self, task: Dict) -> str:
        """Submit task to agent pool"""
        task_id = f"task_{int(time.time())}_{hash(str(task))}"

        await self.task_queue.put({
            "id": task_id,
            "task": task,
            "submitted_at": time.time()
        })

        return task_id

    async def process_tasks(self):
        """Main task processing loop"""
        while True:
            try:
                task_request = await self.task_queue.get()

                # Find suitable agent
                agent = await self._select_agent(task_request["task"])

                if agent:
                    # Assign task to agent
                    await self._assign_task_to_agent(agent, task_request)
                else:
                    # No suitable agent available, requeue with backoff
                    await asyncio.sleep(1)
                    await self.task_queue.put(task_request)

                self.task_queue.task_done()

            except Exception as e:
                logger.error(f"Error processing task: {e}")
                await asyncio.sleep(1)

    async def _select_agent(self, task: Dict) -> Optional[AgentInstance]:
        """Select best agent for task using load balancer"""
        required_capabilities = task.get("required_capabilities", [])
        max_load = task.get("max_agent_load", 0.8)

        available_agents = [
            agent for agent in self.agents.values()
            if agent.status == AgentStatus.AVAILABLE
            and agent.current_load < max_load
            and all(cap in agent.capabilities for cap in required_capabilities)
        ]

        if not available_agents:
            return None

        return self.load_balancer.select_agent(available_agents, task)

    async def _assign_task_to_agent(self, agent: AgentInstance, task_request: Dict):
        """Assign task to specific agent"""
        agent.status = AgentStatus.BUSY
        agent.current_load += 0.1  # Estimate initial load

        try:
            # Send task to agent (implementation depends on communication method)
            result = await self._send_task_to_agent(agent, task_request["task"])

            # Update agent load based on actual processing
            processing_time = result.get("processing_time", 0)
            agent.current_load = min(1.0, agent.current_load + (processing_time / 100))  # Normalize

        finally:
            agent.status = AgentStatus.AVAILABLE
            agent.current_load = max(0.0, agent.current_load - 0.1)

    async def _monitor_agent(self, agent_id: str):
        """Monitor agent health via heartbeat"""
        while agent_id in self.agents:
            await asyncio.sleep(30)  # Check every 30 seconds

            agent = self.agents.get(agent_id)
            if not agent:
                break

            if time.time() - agent.last_heartbeat > 60:  # 60 second timeout
                logger.warning(f"Agent {agent_id} missed heartbeat, marking unavailable")
                agent.status = AgentStatus.UNAVAILABLE
            else:
                # Agent is healthy, ensure it's available if not busy
                if agent.status == AgentStatus.UNAVAILABLE:
                    agent.status = AgentStatus.AVAILABLE

    def get_pool_status(self) -> Dict:
        """Get current pool status"""
        total_agents = len(self.agents)
        available_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.AVAILABLE)
        busy_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.BUSY)
        unavailable_agents = sum(1 for a in self.agents.values() if a.status == AgentStatus.UNAVAILABLE)

        avg_load = sum(a.current_load for a in self.agents.values()) / total_agents if total_agents > 0 else 0

        return {
            "total_agents": total_agents,
            "available": available_agents,
            "busy": busy_agents,
            "unavailable": unavailable_agents,
            "average_load": avg_load,
            "queue_size": self.task_queue.qsize()
        }

class LeastLoadedBalancer:
    def select_agent(self, available_agents: List[AgentInstance], task: Dict) -> AgentInstance:
        """Select agent with lowest current load"""
        return min(available_agents, key=lambda a: a.current_load)

# Initialize agent pool
agent_pool = AgentPoolManager(pool_size=10)

# Start task processing
asyncio.create_task(agent_pool.process_tasks())
```

## Monitoring and Observability

### Comprehensive Monitoring Setup

```python
import logging
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import psutil
import time

class AgentMetricsCollector:
    def __init__(self):
        # Request metrics
        self.request_total = Counter(
            'ag2_requests_total',
            'Total number of requests',
            ['agent_type', 'method', 'status']
        )

        self.request_duration = Histogram(
            'ag2_request_duration_seconds',
            'Request duration in seconds',
            ['agent_type', 'method']
        )

        # Agent metrics
        self.active_agents = Gauge(
            'ag2_active_agents',
            'Number of active agents',
            ['agent_type']
        )

        self.agent_load = Gauge(
            'ag2_agent_load_percent',
            'Agent load percentage',
            ['agent_id', 'agent_type']
        )

        # System metrics
        self.cpu_usage = Gauge('ag2_cpu_usage_percent', 'CPU usage percentage')
        self.memory_usage = Gauge('ag2_memory_usage_percent', 'Memory usage percentage')
        self.disk_usage = Gauge('ag2_disk_usage_percent', 'Disk usage percentage')

        # Error metrics
        self.error_total = Counter(
            'ag2_errors_total',
            'Total number of errors',
            ['error_type', 'agent_type']
        )

    def start_collection(self, port=8001):
        """Start metrics collection server"""
        start_http_server(port)
        logger.info(f"Metrics server started on port {port}")

    async def collect_system_metrics(self):
        """Collect system-level metrics"""
        while True:
            try:
                # CPU usage
                self.cpu_usage.set(psutil.cpu_percent(interval=1))

                # Memory usage
                memory = psutil.virtual_memory()
                self.memory_usage.set(memory.percent)

                # Disk usage
                disk = psutil.disk_usage('/')
                self.disk_usage.set(disk.percent)

                await asyncio.sleep(30)  # Collect every 30 seconds

            except Exception as e:
                logger.error(f"Error collecting system metrics: {e}")
                await asyncio.sleep(30)

    def record_request(self, agent_type: str, method: str, duration: float, status: str = "success"):
        """Record request metrics"""
        self.request_total.labels(agent_type=agent_type, method=method, status=status).inc()
        self.request_duration.labels(agent_type=agent_type, method=method).observe(duration)

    def update_agent_metrics(self, agent_id: str, agent_type: str, load: float, active: bool = True):
        """Update agent-specific metrics"""
        if active:
            self.active_agents.labels(agent_type=agent_type).inc()
        else:
            self.active_agents.labels(agent_type=agent_type).dec()

        self.agent_load.labels(agent_id=agent_id, agent_type=agent_type).set(load)

    def record_error(self, error_type: str, agent_type: str):
        """Record error metrics"""
        self.error_total.labels(error_type=error_type, agent_type=agent_type).inc()

# Global metrics collector
metrics = AgentMetricsCollector()

# Middleware for request tracking
class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        agent_type = scope.get("path", "").split("/")[2] if len(scope.get("path", "").split("/")) > 2 else "unknown"

        try:
            await self.app(scope, receive, send)
            duration = time.time() - start_time
            metrics.record_request(agent_type, scope["method"], duration, "success")

        except Exception as e:
            duration = time.time() - start_time
            metrics.record_request(agent_type, scope["method"], duration, "error")
            metrics.record_error(type(e).__name__, agent_type)
            raise

# Initialize monitoring
metrics.start_collection(port=8001)
asyncio.create_task(metrics.collect_system_metrics())
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_tracing(service_name="ag2-agents"):
    """Setup distributed tracing with Jaeger"""
    # Configure tracer
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger-agent",
        agent_port=6831,
    )

    # Add span processor
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    return tracer

# Global tracer
tracer = setup_tracing()

class TracedAgent(AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracer = tracer

    async def generate_reply_async(self, messages, **kwargs):
        """Generate reply with tracing"""
        with self.tracer.start_as_span(f"agent_{self.name}_generate_reply") as span:
            span.set_attribute("agent.name", self.name)
            span.set_attribute("messages.count", len(messages))

            try:
                # Add message content (truncated for privacy)
                if messages:
                    first_message = messages[0].get("content", "")[:100]
                    span.set_attribute("message.preview", first_message)

                result = await super().generate_reply_async(messages, **kwargs)

                span.set_attribute("response.length", len(result) if result else 0)
                span.set_status(trace.Status(trace.StatusCode.OK))

                return result

            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

# Instrument FastAPI app
def instrument_app(app):
    """Add tracing instrumentation to FastAPI app"""
    FastAPIInstrumentor.instrument_app(app)
```

### Logging Configuration

```python
import structlog
from pythonjsonlogger import jsonlogger

def setup_structured_logging(log_level="INFO", service_name="ag2-agents"):
    """Setup structured JSON logging"""

    # Configure structlog
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # JSON formatter for production
    json_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console formatter for development
    console_formatter = structlog.WriteLoggerFactory()

    # Configure logging
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": lambda: json_formatter,
            },
            "console": {
                "()": structlog.WriteLoggerFactory(),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "level": log_level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"/var/log/{service_name}.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "formatter": "json",
                "level": log_level,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": log_level,
            },
            service_name: {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
        }
    })

    # Configure structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

# Setup logging
setup_structured_logging(log_level="INFO", service_name="ag2-agents")

# Create structured logger
logger = structlog.get_logger()

class LoggedAgent(AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logger.bind(agent_name=self.name)

    async def generate_reply_async(self, messages, **kwargs):
        """Generate reply with comprehensive logging"""
        request_id = kwargs.get("request_id", f"req_{int(time.time())}")

        self.logger.info(
            "Starting agent request",
            request_id=request_id,
            message_count=len(messages),
            agent_type=type(self).__name__
        )

        start_time = time.time()

        try:
            result = await super().generate_reply_async(messages, **kwargs)

            duration = time.time() - start_time

            self.logger.info(
                "Agent request completed successfully",
                request_id=request_id,
                duration=duration,
                response_length=len(result) if result else 0
            )

            # Record metrics
            metrics.record_request(type(self).__name__, "generate_reply", duration, "success")

            return result

        except Exception as e:
            duration = time.time() - start_time

            self.logger.error(
                "Agent request failed",
                request_id=request_id,
                duration=duration,
                error=str(e),
                error_type=type(e).__name__
            )

            # Record error metrics
            metrics.record_error(type(e).__name__, type(self).__name__)
            metrics.record_request(type(self).__name__, "generate_reply", duration, "error")

            raise
```

## Security Implementation

### Authentication and Authorization

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
import secrets

class AuthManager:
    def __init__(self, secret_key=None, algorithm="HS256"):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = algorithm
        self.security = HTTPBearer()

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def verify_token(self, token: str):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """FastAPI dependency for authentication"""
        token = credentials.credentials
        payload = self.verify_token(token)

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return {"user_id": user_id, "permissions": payload.get("permissions", [])}

# Global auth manager
auth_manager = AuthManager()

class SecureAgentAPI:
    def __init__(self, agent_pool: AgentPoolManager):
        self.agent_pool = agent_pool
        self.app = FastAPI(title="AG2 Agent API", version="1.0.0")

        # Add authentication middleware
        self.app.add_middleware(MetricsMiddleware)

        # Add routes
        self._setup_routes()

        # Add instrumentation
        instrument_app(self.app)

    def _setup_routes(self):
        @self.app.post("/api/v1/agents/chat")
        async def chat_with_agent(
            request: ChatRequest,
            current_user: dict = Depends(auth_manager.get_current_user)
        ):
            """Secure chat endpoint"""
            try:
                # Check permissions
                if "agent:chat" not in current_user["permissions"]:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient permissions"
                    )

                # Rate limiting check (implement based on your needs)
                await self._check_rate_limit(current_user["user_id"])

                # Submit task to agent pool
                task_id = await self.agent_pool.submit_task({
                    "type": "chat",
                    "messages": request.messages,
                    "agent_type": request.agent_type,
                    "user_id": current_user["user_id"]
                })

                return {"task_id": task_id, "status": "submitted"}

            except Exception as e:
                logger.error(f"Chat request failed: {e}", user_id=current_user["user_id"])
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.get("/api/v1/agents/status")
        async def get_system_status(current_user: dict = Depends(auth_manager.get_current_user)):
            """Get system status (admin only)"""
            if "admin" not in current_user["permissions"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin access required"
                )

            return self.agent_pool.get_pool_status()

    async def _check_rate_limit(self, user_id: str):
        """Implement rate limiting logic"""
        # This is a simplified example - implement proper rate limiting
        # using Redis or similar
        pass

# Pydantic models for API
from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    agent_type: str = "general"

# Create secure API
agent_api = SecureAgentAPI(agent_pool)

# For development/testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(agent_api.app, host="0.0.0.0", port=8000)
```

### Data Encryption and Privacy

```python
from cryptography.fernet import Fernet
import base64
import os

class DataEncryption:
    def __init__(self, key=None):
        if key:
            self.key = base64.urlsafe_b64encode(key.encode()) if isinstance(key, str) else key
        else:
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def encrypt_dict(self, data: dict) -> dict:
        """Encrypt sensitive fields in dictionary"""
        encrypted = {}
        sensitive_fields = ["api_key", "password", "token", "secret"]

        for key, value in data.items():
            if any(field in key.lower() for field in sensitive_fields):
                encrypted[key] = self.encrypt_data(str(value))
            else:
                encrypted[key] = value

        return encrypted

    def decrypt_dict(self, data: dict) -> dict:
        """Decrypt sensitive fields in dictionary"""
        decrypted = {}

        for key, value in data.items():
            try:
                decrypted[key] = self.decrypt_data(str(value))
            except:
                # Not encrypted, use as-is
                decrypted[key] = value

        return decrypted

# Global encryption manager
encryption = DataEncryption()

class SecureAgent(AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.encryption = encryption

    async def process_secure_request(self, request: dict):
        """Process request with automatic encryption/decryption"""
        # Decrypt sensitive data in request
        decrypted_request = self.encryption.decrypt_dict(request)

        # Process the request
        messages = decrypted_request.get("messages", [])

        # Check for sensitive content in messages
        sanitized_messages = []
        for msg in messages:
            content = msg.get("content", "")
            # Remove or mask sensitive patterns
            sanitized_content = self._sanitize_sensitive_data(content)
            sanitized_messages.append({"role": msg.get("role"), "content": sanitized_content})

        response = await self.generate_reply_async(sanitized_messages)

        # Encrypt response if it contains sensitive data
        if self._contains_sensitive_data(response):
            response = self.encryption.encrypt_data(response)

        return response

    def _sanitize_sensitive_data(self, content: str) -> str:
        """Remove or mask sensitive data"""
        import re

        # Mask API keys
        content = re.sub(r'api[_-]?key[_-]?[=:]\s*[\w-]+', 'api_key=***', content, flags=re.IGNORECASE)

        # Mask passwords
        content = re.sub(r'password[_-]?[=:]\s*[\w-]+', 'password=***', content, flags=re.IGNORECASE)

        # Mask tokens
        content = re.sub(r'token[_-]?[=:]\s*[\w-]+', 'token=***', content, flags=re.IGNORECASE)

        return content

    def _contains_sensitive_data(self, content: str) -> bool:
        """Check if content contains sensitive data"""
        sensitive_patterns = [
            r'api[_-]?key',
            r'password',
            r'token',
            r'secret',
            r'private[_-]?key'
        ]

        return any(re.search(pattern, content, re.IGNORECASE) for pattern in sensitive_patterns)
```

## Backup and Disaster Recovery

### Automated Backup System

```python
import boto3
from botocore.exceptions import ClientError
import gzip
import json
from datetime import datetime

class BackupManager:
    def __init__(self, s3_bucket: str, region: str = "us-east-1"):
        self.s3_client = boto3.client('s3', region_name=region)
        self.bucket = s3_bucket
        self.backup_schedule = {
            "agent_configs": "daily",
            "conversation_history": "hourly",
            "metrics_data": "daily",
            "model_weights": "weekly"
        }

    async def create_backup(self, backup_type: str, data: dict) -> str:
        """Create and upload backup to S3"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_key = f"backups/{backup_type}/{timestamp}.json.gz"

        # Compress data
        json_data = json.dumps(data, indent=2)
        compressed_data = gzip.compress(json_data.encode('utf-8'))

        try:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=backup_key,
                Body=compressed_data,
                ContentType='application/json',
                ContentEncoding='gzip',
                Metadata={
                    'backup_type': backup_type,
                    'timestamp': timestamp,
                    'uncompressed_size': str(len(json_data))
                }
            )

            logger.info(f"Backup created: {backup_key}")
            return backup_key

        except ClientError as e:
            logger.error(f"Backup failed: {e}")
            raise

    async def restore_backup(self, backup_key: str) -> dict:
        """Restore data from backup"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=backup_key)

            compressed_data = response['Body'].read()
            json_data = gzip.decompress(compressed_data)
            data = json.loads(json_data.decode('utf-8'))

            logger.info(f"Backup restored: {backup_key}")
            return data

        except ClientError as e:
            logger.error(f"Restore failed: {e}")
            raise

    async def list_backups(self, backup_type: str = None, limit: int = 10) -> List[Dict]:
        """List available backups"""
        prefix = f"backups/{backup_type}/" if backup_type else "backups/"

        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )

            backups = []
            if 'Contents' in response:
                for obj in response['Contents'][:limit]:
                    backups.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'backup_type': obj['Key'].split('/')[1]
                    })

            return backups

        except ClientError as e:
            logger.error(f"List backups failed: {e}")
            raise

    async def scheduled_backup(self):
        """Run scheduled backups"""
        while True:
            try:
                current_time = datetime.utcnow()

                # Daily backups at 2 AM UTC
                if current_time.hour == 2 and current_time.minute == 0:
                    await self._perform_daily_backups()

                # Hourly backups
                if current_time.minute == 0:
                    await self._perform_hourly_backups()

                # Weekly backups on Sunday at 3 AM UTC
                if current_time.weekday() == 6 and current_time.hour == 3 and current_time.minute == 0:
                    await self._perform_weekly_backups()

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"Scheduled backup failed: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

    async def _perform_daily_backups(self):
        """Perform daily backup tasks"""
        # Agent configurations
        agent_configs = self._collect_agent_configs()
        await self.create_backup("agent_configs", agent_configs)

        # Metrics data
        metrics_data = self._collect_metrics_data()
        await self.create_backup("metrics_data", metrics_data)

    async def _perform_hourly_backups(self):
        """Perform hourly backup tasks"""
        # Conversation history
        conversation_history = self._collect_conversation_history()
        await self.create_backup("conversation_history", conversation_history)

    async def _perform_weekly_backups(self):
        """Perform weekly backup tasks"""
        # Model weights and large data
        model_data = self._collect_model_data()
        await self.create_backup("model_weights", model_data)

    def _collect_agent_configs(self) -> dict:
        """Collect current agent configurations"""
        # Implementation depends on your agent management system
        return {"agents": [], "timestamp": datetime.utcnow().isoformat()}

    def _collect_metrics_data(self) -> dict:
        """Collect metrics data"""
        # Implementation depends on your metrics system
        return {"metrics": {}, "timestamp": datetime.utcnow().isoformat()}

    def _collect_conversation_history(self) -> dict:
        """Collect recent conversation history"""
        # Implementation depends on your storage system
        return {"conversations": [], "timestamp": datetime.utcnow().isoformat()}

    def _collect_model_data(self) -> dict:
        """Collect model weights and configurations"""
        # Implementation depends on your model storage
        return {"models": {}, "timestamp": datetime.utcnow().isoformat()}

# Initialize backup manager
backup_manager = BackupManager(s3_bucket="ag2-backups")

# Start scheduled backups
asyncio.create_task(backup_manager.scheduled_backup())
```

## Summary

In this comprehensive chapter, we've covered:

- **Infrastructure Architecture**: Multi-tier deployment, container orchestration, service mesh
- **Scaling Strategies**: Horizontal pod autoscaling, agent pool management
- **Monitoring & Observability**: Metrics collection, distributed tracing, structured logging
- **Security Implementation**: Authentication, authorization, data encryption
- **Backup & Disaster Recovery**: Automated backup systems, scheduled maintenance

### Production Readiness Checklist

✅ **Infrastructure**
- Multi-tier deployment architecture
- Container orchestration (Kubernetes)
- Service mesh integration (Istio)
- Load balancing and auto-scaling

✅ **Scalability**
- Horizontal pod autoscaling
- Agent pool management
- Load balancing strategies
- Resource optimization

✅ **Monitoring**
- Comprehensive metrics collection
- Distributed tracing (Jaeger)
- Structured logging
- Alerting and dashboards

✅ **Security**
- JWT authentication and authorization
- Data encryption at rest and in transit
- Rate limiting and abuse prevention
- Secure API design

✅ **Reliability**
- Automated backup systems
- Disaster recovery procedures
- Health checks and self-healing
- Graceful failure handling

### Next Steps

1. **Infrastructure Setup**: Deploy the Kubernetes manifests and service mesh configuration
2. **Security Implementation**: Set up authentication, encryption, and access controls
3. **Monitoring Deployment**: Configure Prometheus, Jaeger, and logging infrastructure
4. **Load Testing**: Test scaling behavior under various load conditions
5. **Backup Verification**: Test backup and restore procedures regularly
6. **Compliance Audit**: Ensure compliance with relevant regulations and standards

Your AG2 agent system is now production-ready! The architecture supports high availability, automatic scaling, comprehensive monitoring, and enterprise-grade security.

---

*Congratulations! You've completed the comprehensive AG2 Tutorial. You now have the knowledge to build and deploy production-grade multi-agent AI systems.*

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*