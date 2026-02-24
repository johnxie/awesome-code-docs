---
layout: default
title: "Phidata Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Phidata Tutorial
---

# Chapter 8: Production Deployment & Scaling Phidata Agents

Welcome to **Chapter 8: Production Deployment & Scaling Phidata Agents**. In this part of **Phidata Tutorial: Building Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy autonomous agent systems at enterprise scale with high availability, monitoring, and production best practices.

## Production Architecture

### Scalable Agent Platform Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │  Load Balancer  │
│  (Kong/Traefik) │    │   (NGINX)       │
└─────────────────┘    └─────────────────┘
           │                       │
           └───────────────────────┘
                    │
          ┌─────────────────┐
          │  Agent Router   │
          │  (Phidata API)  │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │  Agent Pool     │
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
          │   for Memory)   │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │  Task Queue     │
          │  (Redis/Rabbit) │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Monitoring    │
          │ (Prometheus/    │
          │  Grafana)       │
          └─────────────────┘
```

## Kubernetes Deployment

### Complete Phidata Agent Deployment

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: phidata
  labels:
    name: phidata

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: phidata-config
  namespace: phidata
data:
  MODEL_NAME: "gpt-4"
  MAX_CONCURRENT_AGENTS: "10"
  AGENT_TIMEOUT: "300"
  CACHE_TTL: "3600"
  LOG_LEVEL: "INFO"
  ENABLE_METRICS: "true"
  DATABASE_URL: "postgresql://user:password@postgres:5432/phidata"
  REDIS_URL: "redis://redis:6379"
  VECTOR_DB_URL: "http://qdrant:6333"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: phidata-secrets
  namespace: phidata
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-your-openai-key"
  ANTHROPIC_API_KEY: "sk-ant-your-anthropic-key"
  DATABASE_PASSWORD: "your-db-password"
  REDIS_PASSWORD: "your-redis-password"
  API_SECRET_KEY: "your-api-secret"

---
# k8s/agent-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: phidata-agents
  namespace: phidata
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 2
      maxSurge: 2
  selector:
    matchLabels:
      app: phidata-agent
  template:
    metadata:
      labels:
        app: phidata-agent
    spec:
      containers:
      - name: phidata-agent
        image: phidata/agents:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: phidata-config
        - secretRef:
            name: phidata-secrets
        volumeMounts:
        - name: agent-logs
          mountPath: /app/logs
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
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 120
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 6
      volumes:
      - name: agent-logs
        emptyDir: {}

---
# k8s/api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: phidata-api
  namespace: phidata
spec:
  selector:
    app: phidata-agent
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: phidata-hpa
  namespace: phidata
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: phidata-agents
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
  name: phidata-ingress
  namespace: phidata
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
spec:
  tls:
  - hosts:
    - agents.company.com
    secretName: phidata-tls
  rules:
  - host: agents.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: phidata-api
            port:
              number: 80
```

## Docker Production Setup

### Multi-Service Production Stack

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Phidata API Service
  phidata-api:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: phidata-api-prod
    restart: unless-stopped
    environment:
      - MODEL_NAME=gpt-4
      - MAX_CONCURRENT_AGENTS=20
      - AGENT_TIMEOUT=300
      - CACHE_TTL=3600
      - DATABASE_URL=postgresql://user:password@postgres:5432/phidata
      - REDIS_URL=redis://redis:6379
      - VECTOR_DB_URL=http://qdrant:6333
      - LOG_LEVEL=INFO
      - ENABLE_METRICS=true
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
      - agent_data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # PostgreSQL Database
  postgres:
    image: postgres:15
    container_name: phidata-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=phidata
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d phidata"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    container_name: phidata-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Vector Database
  qdrant:
    image: qdrant/qdrant:latest
    container_name: phidata-qdrant
    restart: unless-stopped
    volumes:
      - qdrant_data:/qdrant/storage
      - ./qdrant/config:/qdrant/config
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Message Queue (RabbitMQ)
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: phidata-rabbitmq
    restart: unless-stopped
    environment:
      - RABBITMQ_DEFAULT_USER=${MQ_USER}
      - RABBITMQ_DEFAULT_PASS=${MQ_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Monitoring - Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: phidata-prometheus
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  # Monitoring - Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: phidata-grafana
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
  postgres_data:
  redis_data:
  qdrant_data:
  rabbitmq_data:
  prometheus_data:
  grafana_data:
  agent_data:
```

## Agent Pool Management

### Dynamic Agent Scaling

```python
from typing import Dict, List, Any, Optional
import asyncio
import time
from dataclasses import dataclass
from phidata.agent import Agent

@dataclass
class AgentInstance:
    agent: Agent
    created_at: float
    last_used: float
    active_tasks: int
    total_tasks: int

class AgentPoolManager:
    """Production-ready agent pool with scaling and monitoring."""

    def __init__(self, agent_configs: List[Dict[str, Any]], max_pool_size: int = 50):
        self.agent_configs = agent_configs
        self.max_pool_size = max_pool_size
        self.pool: Dict[str, List[AgentInstance]] = {}
        self.active_agents = 0
        self.task_queue = asyncio.Queue()
        self.metrics = {
            "total_agents_created": 0,
            "total_tasks_processed": 0,
            "avg_task_duration": 0,
            "pool_hit_rate": 0
        }

    async def get_agent(self, agent_type: str) -> Agent:
        """Get an agent from the pool or create a new one."""

        if agent_type not in self.pool:
            self.pool[agent_type] = []

        # Find available agent
        available_agents = [
            instance for instance in self.pool[agent_type]
            if instance.active_tasks == 0
        ]

        if available_agents:
            # Use existing agent
            agent_instance = available_agents[0]
            agent_instance.last_used = time.time()
            agent_instance.active_tasks += 1
            return agent_instance.agent

        # Check if we can create a new agent
        if self.active_agents >= self.max_pool_size:
            # Wait for an agent to become available
            await self._wait_for_available_agent(agent_type)

        # Create new agent
        agent_config = next(
            (config for config in self.agent_configs if config["type"] == agent_type),
            None
        )

        if not agent_config:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent = Agent(
            name=f"{agent_type}_{self.metrics['total_agents_created']}",
            instructions=agent_config["instructions"],
            model=agent_config["model"]
        )

        agent_instance = AgentInstance(
            agent=agent,
            created_at=time.time(),
            last_used=time.time(),
            active_tasks=1,
            total_tasks=0
        )

        self.pool[agent_type].append(agent_instance)
        self.active_agents += 1
        self.metrics["total_agents_created"] += 1

        return agent

    async def release_agent(self, agent: Agent, agent_type: str):
        """Release an agent back to the pool."""

        if agent_type in self.pool:
            for instance in self.pool[agent_type]:
                if instance.agent.name == agent.name:
                    instance.active_tasks = max(0, instance.active_tasks - 1)
                    instance.total_tasks += 1
                    break

    async def _wait_for_available_agent(self, agent_type: str, timeout: float = 30.0):
        """Wait for an agent to become available."""

        start_time = time.time()

        while time.time() - start_time < timeout:
            available_agents = [
                instance for instance in self.pool.get(agent_type, [])
                if instance.active_tasks == 0
            ]

            if available_agents:
                return

            await asyncio.sleep(0.1)  # Small delay

        raise TimeoutError(f"No {agent_type} agent available within {timeout} seconds")

    async def execute_task(self, agent_type: str, task: str) -> Dict[str, Any]:
        """Execute a task using the agent pool."""

        start_time = time.time()

        try:
            # Get agent from pool
            agent = await self.get_agent(agent_type)

            # Execute task
            result = agent.run(task)

            # Calculate duration
            duration = time.time() - start_time

            # Update metrics
            self.metrics["total_tasks_processed"] += 1
            self._update_avg_duration(duration)

            # Release agent
            await self.release_agent(agent, agent_type)

            return {
                "success": True,
                "result": result,
                "duration": duration,
                "agent_name": agent.name
            }

        except Exception as e:
            duration = time.time() - start_time

            return {
                "success": False,
                "error": str(e),
                "duration": duration
            }

    def _update_avg_duration(self, new_duration: float):
        """Update rolling average task duration."""

        current_avg = self.metrics["avg_task_duration"]
        total_tasks = self.metrics["total_tasks_processed"]

        if total_tasks == 1:
            self.metrics["avg_task_duration"] = new_duration
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics["avg_task_duration"] = alpha * new_duration + (1 - alpha) * current_avg

    def get_pool_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""

        stats = {
            "total_agents": self.active_agents,
            "max_pool_size": self.max_pool_size,
            "pool_utilization": self.active_agents / self.max_pool_size if self.max_pool_size > 0 else 0,
            "agent_types": {}
        }

        for agent_type, instances in self.pool.items():
            type_stats = {
                "count": len(instances),
                "active": sum(1 for inst in instances if inst.active_tasks > 0),
                "total_tasks": sum(inst.total_tasks for inst in instances)
            }
            stats["agent_types"][agent_type] = type_stats

        stats.update(self.metrics)
        return stats

    async def cleanup_idle_agents(self, idle_timeout: float = 300.0):
        """Clean up idle agents to free resources."""

        current_time = time.time()
        cleaned_count = 0

        for agent_type, instances in list(self.pool.items()):
            active_instances = []

            for instance in instances:
                # Remove idle agents
                if (instance.active_tasks == 0 and
                    current_time - instance.last_used > idle_timeout):

                    self.active_agents -= 1
                    cleaned_count += 1
                    continue

                active_instances.append(instance)

            self.pool[agent_type] = active_instances

        return cleaned_count

# Define agent configurations
agent_configs = [
    {
        "type": "general",
        "instructions": "You are a helpful general-purpose AI assistant.",
        "model": "gpt-4"
    },
    {
        "type": "coder",
        "instructions": "You are an expert software developer specializing in Python.",
        "model": "gpt-4"
    },
    {
        "type": "analyst",
        "instructions": "You are a data analyst skilled in interpreting data and providing insights.",
        "model": "gpt-4"
    },
    {
        "type": "writer",
        "instructions": "You are a professional content writer creating engaging written material.",
        "model": "gpt-4"
    }
]

# Create agent pool
agent_pool = AgentPoolManager(agent_configs, max_pool_size=20)

# Example usage
async def demonstrate_agent_pool():
    """Demonstrate agent pool functionality."""

    tasks = [
        ("general", "What is the capital of France?"),
        ("coder", "Write a Python function to calculate fibonacci numbers."),
        ("analyst", "Analyze this data: [1, 2, 3, 4, 5]"),
        ("writer", "Write a short paragraph about artificial intelligence."),
        ("general", "Explain quantum computing in simple terms.")
    ]

    print("Agent Pool Demonstration:")
    for agent_type, task in tasks:
        print(f"\nExecuting {agent_type} task: {task[:50]}...")

        result = await agent_pool.execute_task(agent_type, task)

        if result["success"]:
            print(f"✓ Completed in {result['duration']:.2f}s using {result['agent_name']}")
            print(f"Result: {result['result'][:100]}...")
        else:
            print(f"✗ Failed: {result['error']}")

    # Show pool statistics
    stats = agent_pool.get_pool_stats()
    print("
Pool Statistics:")
    print(f"Total agents created: {stats['total_agents_created']}")
    print(f"Tasks processed: {stats['total_tasks_processed']}")
    print(f"Average task duration: {stats['avg_task_duration']:.2f}s")
    print(f"Pool utilization: {stats['pool_utilization']:.1%}")

    for agent_type, type_stats in stats["agent_types"].items():
        print(f"{agent_type}: {type_stats['count']} agents, {type_stats['total_tasks']} tasks")

asyncio.run(demonstrate_agent_pool())
```

## Monitoring and Observability

### Comprehensive Agent Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import psutil

class AgentMetrics:
    """Production monitoring for agent systems."""

    def __init__(self):
        # Agent metrics
        self.agent_requests_total = Counter(
            'phidata_agent_requests_total',
            'Total agent requests',
            ['agent_type', 'model', 'status']
        )

        self.agent_request_duration = Histogram(
            'phidata_agent_request_duration_seconds',
            'Agent request duration',
            ['agent_type', 'model']
        )

        self.active_agents = Gauge(
            'phidata_active_agents',
            'Number of currently active agents',
            ['agent_type']
        )

        # Pool metrics
        self.pool_size = Gauge(
            'phidata_pool_size',
            'Current pool size',
            ['pool_type']
        )

        self.pool_utilization = Gauge(
            'phidata_pool_utilization_percent',
            'Pool utilization percentage',
            ['pool_type']
        )

        # Task metrics
        self.task_queue_size = Gauge(
            'phidata_task_queue_size',
            'Number of tasks in queue'
        )

        self.task_processing_time = Histogram(
            'phidata_task_processing_time_seconds',
            'Task processing time'
        )

        # System metrics
        self.memory_usage = Gauge(
            'phidata_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.cpu_usage = Gauge(
            'phidata_cpu_usage_percent',
            'CPU usage percentage'
        )

        # Error metrics
        self.errors_total = Counter(
            'phidata_errors_total',
            'Total errors',
            ['error_type', 'agent_type']
        )

    def record_agent_request(self, agent_type: str, model: str, duration: float, status: str = "success"):
        """Record agent request metrics."""

        self.agent_requests_total.labels(agent_type, model, status).inc()
        self.agent_request_duration.labels(agent_type, model).observe(duration)

    def set_active_agents(self, agent_type: str, count: int):
        """Set active agent count."""

        self.active_agents.labels(agent_type).set(count)

    def set_pool_metrics(self, pool_type: str, size: int, utilization: float):
        """Set pool metrics."""

        self.pool_size.labels(pool_type).set(size)
        self.pool_utilization.labels(pool_type).set(utilization * 100)

    def set_task_queue_size(self, size: int):
        """Set task queue size."""

        self.task_queue_size.set(size)

    def record_task_processing(self, duration: float):
        """Record task processing time."""

        self.task_processing_time.observe(duration)

    def record_error(self, error_type: str, agent_type: str = "unknown"):
        """Record error."""

        self.errors_total.labels(error_type, agent_type).inc()

    def update_system_metrics(self):
        """Update system resource metrics."""

        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_usage.set(cpu_percent)

    def get_metrics_text(self) -> str:
        """Get metrics in Prometheus format."""

        return generate_latest().decode('utf-8')

# Global metrics instance
agent_metrics = AgentMetrics()

class MonitoredAgentPool(AgentPoolManager):
    """Agent pool with built-in monitoring."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = agent_metrics

    async def execute_task(self, agent_type: str, task: str) -> Dict[str, Any]:
        """Execute task with monitoring."""

        start_time = time.time()

        # Update metrics
        self.metrics.set_task_queue_size(self.task_queue.qsize())
        self.metrics.update_system_metrics()

        try:
            result = await super().execute_task(agent_type, task)

            duration = time.time() - start_time
            status = "success" if result["success"] else "error"

            # Record metrics
            agent_config = next(
                (config for config in self.agent_configs if config["type"] == agent_type),
                {}
            )
            model = agent_config.get("model", "unknown")

            self.metrics.record_agent_request(agent_type, model, duration, status)
            self.metrics.record_task_processing(duration)

            # Update pool metrics
            pool_stats = self.get_pool_stats()
            self.metrics.set_pool_metrics("agent_pool", pool_stats["total_agents"],
                                        pool_stats["pool_utilization"])

            for agent_type_name, type_stats in pool_stats["agent_types"].items():
                self.metrics.set_active_agents(agent_type_name, type_stats["active"])

            if not result["success"]:
                self.metrics.record_error("task_execution_failed", agent_type)

            return result

        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_error("unexpected_error", agent_type)

            return {
                "success": False,
                "error": str(e),
                "duration": duration
            }

# Create monitored agent pool
monitored_pool = MonitoredAgentPool(agent_configs, max_pool_size=20)

# Example monitoring
async def demonstrate_monitoring():
    """Demonstrate monitoring capabilities."""

    # Execute some tasks
    tasks = [
        ("general", "Hello, how are you?"),
        ("coder", "Write a Python hello world function."),
        ("analyst", "Analyze this data: [1, 2, 3, 4, 5]"),
    ]

    print("Executing tasks with monitoring...")
    for agent_type, task in tasks:
        result = await monitored_pool.execute_task(agent_type, task)
        print(f"{agent_type} task: {'✓' if result['success'] else '✗'}")

    # Show metrics
    print("
Monitoring Metrics Sample:")
    metrics_text = agent_metrics.get_metrics_text()
    # Show first few lines
    lines = metrics_text.split('\n')[:20]
    print('\n'.join(lines))
    print("... (truncated)")

asyncio.run(demonstrate_monitoring())
```

## Security and Access Control

### Enterprise Security Implementation

```python
from typing import Dict, List, Any, Optional
import jwt
import time
import hashlib
import hmac
from functools import wraps

class EnterpriseSecurityManager:
    """Enterprise-grade security for agent systems."""

    def __init__(self, jwt_secret: str, api_keys: Dict[str, str] = None):
        self.jwt_secret = jwt_secret
        self.api_keys = api_keys or {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def authenticate_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """Authenticate JWT token with comprehensive validation."""

        try:
            # Decode token
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])

            # Validate required claims
            required_claims = ['user_id', 'exp', 'iat']
            for claim in required_claims:
                if claim not in payload:
                    return None

            # Check expiration
            if payload.get('exp', 0) < time.time():
                self._audit_event("token_expired", {"user_id": payload.get("user_id")})
                return None

            # Check if token was issued recently (not too old)
            max_age = 24 * 60 * 60  # 24 hours
            if time.time() - payload.get('iat', 0) > max_age:
                self._audit_event("token_too_old", {"user_id": payload.get("user_id")})
                return None

            # Log successful authentication
            self._audit_event("authentication_success", {
                "user_id": payload.get("user_id"),
                "roles": payload.get("roles", [])
            })

            return payload

        except jwt.ExpiredSignatureError:
            self._audit_event("token_expired_signature", {})
            return None
        except jwt.InvalidTokenError:
            self._audit_event("token_invalid", {})
            return None

    def authenticate_api_key(self, api_key: str) -> Optional[str]:
        """Authenticate API key with rate limiting."""

        # Hash the provided key for comparison
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        for user_id, stored_hash in self.api_keys.items():
            if hmac.compare_digest(key_hash, stored_hash):
                self._audit_event("api_key_auth_success", {"user_id": user_id})
                return user_id

        self._audit_event("api_key_auth_failed", {"key_hash": key_hash[:8]})
        return None

    def authorize_request(self, user_info: Dict[str, Any], required_permission: str,
                         resource: str = None) -> bool:
        """Advanced authorization with role-based and attribute-based access control."""

        user_permissions = user_info.get('permissions', [])
        user_roles = user_info.get('roles', [])
        user_attributes = user_info.get('attributes', {})

        # Role-based permissions
        role_permissions = {
            'admin': ['*'],  # Admin has all permissions
            'developer': ['agent:create', 'agent:execute', 'agent:read'],
            'analyst': ['agent:execute', 'agent:read', 'data:read'],
            'user': ['agent:execute:basic', 'agent:read:own']
        }

        # Collect all permissions
        allowed_permissions = set(user_permissions)

        for role in user_roles:
            if role in role_permissions:
                allowed_permissions.update(role_permissions[role])

        # Check if user has required permission
        if required_permission in allowed_permissions or '*' in allowed_permissions:
            self._audit_event("authorization_success", {
                "user_id": user_info.get("user_id"),
                "permission": required_permission,
                "resource": resource
            })
            return True

        # Attribute-based access control (ABAC)
        if self._check_abac(user_attributes, required_permission, resource):
            self._audit_event("abac_authorization_success", {
                "user_id": user_info.get("user_id"),
                "permission": required_permission,
                "resource": resource
            })
            return True

        self._audit_event("authorization_denied", {
            "user_id": user_info.get("user_id"),
            "permission": required_permission,
            "resource": resource
        })
        return False

    def _check_abac(self, user_attributes: Dict[str, Any], permission: str, resource: str) -> bool:
        """Check attribute-based access control rules."""

        # Example ABAC rules
        department = user_attributes.get('department')
        clearance_level = user_attributes.get('clearance_level', 0)

        # Analysts can only access their department's data
        if permission.startswith('data:read') and department:
            if resource and f"dept:{department}" not in resource:
                return False

        # Higher clearance levels get more permissions
        if permission == 'agent:execute:advanced' and clearance_level < 2:
            return False

        return True

    def check_rate_limit(self, user_id: str, endpoint: str, max_requests: int = 100,
                        window: int = 60) -> bool:
        """Advanced rate limiting with burst handling."""

        key = f"{user_id}:{endpoint}"
        current_time = int(time.time())

        if key not in self.rate_limits:
            self.rate_limits[key] = {
                'requests': [],
                'blocked_until': 0,
                'burst_count': 0
            }

        limit_data = self.rate_limits[key]

        # Check if still blocked
        if current_time < limit_data['blocked_until']:
            self._audit_event("rate_limit_blocked", {"user_id": user_id, "endpoint": endpoint})
            return False

        # Clean old requests
        window_start = current_time - window
        limit_data['requests'] = [
            req_time for req_time in limit_data['requests']
            if req_time > window_start
        ]

        # Check burst protection (allow short bursts)
        burst_limit = max_requests // 10  # 10% of normal limit for bursts
        recent_requests = [req for req in limit_data['requests'] if current_time - req < 10]

        if len(recent_requests) >= burst_limit:
            # Temporary block for burst protection
            limit_data['blocked_until'] = current_time + 10
            self._audit_event("burst_limit_triggered", {"user_id": user_id, "endpoint": endpoint})
            return False

        # Check normal rate limit
        if len(limit_data['requests']) >= max_requests:
            # Block for the window duration
            limit_data['blocked_until'] = current_time + window
            self._audit_event("rate_limit_exceeded", {"user_id": user_id, "endpoint": endpoint})
            return False

        # Add current request
        limit_data['requests'].append(current_time)
        return True

    def _audit_event(self, event_type: str, details: Dict[str, Any]):
        """Log security audit event."""

        audit_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details,
            "ip_address": "system"  # In production, get from request
        }

        self.audit_log.append(audit_entry)

        # Keep only last 10000 entries
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-10000:]

    def get_audit_log(self, user_id: Optional[str] = None, event_type: Optional[str] = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries with filtering."""

        filtered_log = self.audit_log

        if user_id:
            filtered_log = [entry for entry in filtered_log
                          if entry["details"].get("user_id") == user_id]

        if event_type:
            filtered_log = [entry for entry in filtered_log
                          if entry["event_type"] == event_type]

        return filtered_log[-limit:]

# Create enterprise security manager
security_manager = EnterpriseSecurityManager(
    jwt_secret="your-super-secure-jwt-secret-change-in-production",
    api_keys={
        "user123": hashlib.sha256("prod-api-key-123".encode()).hexdigest(),
        "admin456": hashlib.sha256("admin-key-456".encode()).hexdigest()
    }
)

# Secure API endpoint decorator
def require_security(permission: str, rate_limit: bool = True):
    """Decorator for secure API endpoints."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request (FastAPI pattern)
            request = kwargs.get('request') or args[0] if args else None

            if not request:
                return {"error": "No request object"}

            # Authenticate user
            user_info = None
            auth_header = request.headers.get('Authorization', '')
            api_key = request.headers.get('X-API-Key')

            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                user_info = security_manager.authenticate_jwt(token)
            elif api_key:
                user_id = security_manager.authenticate_api_key(api_key)
                if user_id:
                    user_info = {"user_id": user_id, "roles": ["user"]}

            if not user_info:
                return {"error": "Authentication failed"}

            # Check rate limit
            if rate_limit:
                endpoint = request.url.path
                if not security_manager.check_rate_limit(user_info['user_id'], endpoint):
                    return {"error": "Rate limit exceeded"}

            # Authorize request
            if not security_manager.authorize_request(user_info, permission):
                return {"error": "Insufficient permissions"}

            # Add user info to request
            request.state.user = user_info

            return await func(*args, **kwargs)

        return wrapper
    return decorator

# Example secure FastAPI endpoint
from fastapi import FastAPI, Request

app = FastAPI(title="Secure Phidata API", version="1.0.0")

@app.post("/agent/execute")
@require_security("agent:execute")
async def execute_agent(request: Request, payload: Dict[str, Any]):
    """Secure agent execution endpoint."""

    user = request.state.user

    # Execute agent with user context
    result = await monitored_pool.execute_task(
        payload["agent_type"],
        payload["task"]
    )

    # Log the execution
    security_manager._audit_event("agent_execution", {
        "user_id": user["user_id"],
        "agent_type": payload["agent_type"],
        "task_length": len(payload["task"])
    })

    return result

@app.get("/audit/log")
@require_security("audit:read")
async def get_audit_log(request: Request, user_id: Optional[str] = None, limit: int = 50):
    """Secure audit log access."""

    user = request.state.user

    # Only admins can see all logs, users can only see their own
    if "admin" not in user.get("roles", []) and user_id != user["user_id"]:
        user_id = user["user_id"]

    audit_log = security_manager.get_audit_log(user_id=user_id, limit=limit)

    return {"audit_log": audit_log}

@app.get("/security/status")
@require_security("security:read")
async def security_status(request: Request):
    """Security system status."""

    user = request.state.user

    # Only admins can see security status
    if "admin" not in user.get("roles", []):
        return {"error": "Admin access required"}

    recent_audit = security_manager.get_audit_log(limit=10)

    return {
        "total_audit_entries": len(security_manager.audit_log),
        "recent_events": len(recent_audit),
        "rate_limits_active": len(security_manager.rate_limits)
    }
```

## Performance Benchmarking

### Production Performance Testing

```python
import asyncio
import time
import statistics
from typing import List, Dict, Any
import json

class ProductionBenchmarkSuite:
    """Comprehensive benchmarking for production agent systems."""

    def __init__(self, agent_pool: AgentPoolManager):
        self.agent_pool = agent_pool

    async def run_comprehensive_benchmark(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive production benchmark suite."""

        benchmark_results = {
            "timestamp": time.time(),
            "config": config,
            "results": {},
            "summary": {}
        }

        print("Starting Production Benchmark Suite...")

        # 1. Latency Benchmark
        print("Running latency benchmark...")
        latency_results = await self.benchmark_latency(config.get("latency_tests", []))
        benchmark_results["results"]["latency"] = latency_results

        # 2. Throughput Benchmark
        print("Running throughput benchmark...")
        throughput_results = await self.benchmark_throughput(config.get("throughput_tests", []))
        benchmark_results["results"]["throughput"] = throughput_results

        # 3. Memory Usage Benchmark
        print("Running memory benchmark...")
        memory_results = await self.benchmark_memory_usage(config.get("memory_tests", []))
        benchmark_results["results"]["memory"] = memory_results

        # 4. Concurrent Load Test
        print("Running concurrent load test...")
        load_results = await self.benchmark_concurrent_load(config.get("load_tests", {}))
        benchmark_results["results"]["load"] = load_results

        # 5. Error Handling Benchmark
        print("Running error handling benchmark...")
        error_results = await self.benchmark_error_handling(config.get("error_tests", []))
        benchmark_results["results"]["errors"] = error_results

        # Generate summary
        benchmark_results["summary"] = self.generate_summary(benchmark_results["results"])

        print("Benchmark suite completed!")
        return benchmark_results

    async def benchmark_latency(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Benchmark response latency."""

        results = {}

        for test_case in test_cases:
            agent_type = test_case["agent_type"]
            prompt = test_case["prompt"]
            iterations = test_case.get("iterations", 10)

            print(f"  Testing {agent_type} latency...")

            latencies = []

            for i in range(iterations):
                start_time = time.time()
                result = await self.agent_pool.execute_task(agent_type, prompt)
                end_time = time.time()

                if result["success"]:
                    latencies.append(end_time - start_time)

            if latencies:
                results[agent_type] = {
                    "mean_latency": statistics.mean(latencies),
                    "median_latency": statistics.median(latencies),
                    "min_latency": min(latencies),
                    "max_latency": max(latencies),
                    "std_dev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
                    "success_rate": len(latencies) / iterations,
                    "iterations": iterations
                }

        return results

    async def benchmark_throughput(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Benchmark system throughput."""

        results = {}

        for test_case in test_cases:
            agent_type = test_case["agent_type"]
            prompts = test_case["prompts"]
            duration = test_case.get("duration", 60)  # seconds

            print(f"  Testing {agent_type} throughput for {duration}s...")

            start_time = time.time()
            completed_tasks = 0
            errors = 0

            while time.time() - start_time < duration:
                for prompt in prompts:
                    try:
                        result = await self.agent_pool.execute_task(agent_type, prompt)
                        if result["success"]:
                            completed_tasks += 1
                        else:
                            errors += 1
                    except:
                        errors += 1

            total_time = time.time() - start_time
            throughput = completed_tasks / total_time

            results[agent_type] = {
                "total_tasks": completed_tasks,
                "errors": errors,
                "duration": total_time,
                "throughput_tps": throughput,  # tasks per second
                "error_rate": errors / (completed_tasks + errors) if (completed_tasks + errors) > 0 else 0
            }

        return results

    async def benchmark_memory_usage(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Benchmark memory usage patterns."""

        import psutil
        import os

        results = {}

        for test_case in test_cases:
            agent_type = test_case["agent_type"]
            prompts = test_case["prompts"]

            print(f"  Testing {agent_type} memory usage...")

            # Get baseline memory
            process = psutil.Process(os.getpid())
            baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

            memory_readings = []

            for prompt in prompts:
                result = await self.agent_pool.execute_task(agent_type, prompt)
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_readings.append(current_memory)

            final_memory = process.memory_info().rss / 1024 / 1024

            results[agent_type] = {
                "baseline_memory_mb": baseline_memory,
                "peak_memory_mb": max(memory_readings) if memory_readings else baseline_memory,
                "final_memory_mb": final_memory,
                "memory_increase_mb": final_memory - baseline_memory,
                "memory_growth_percent": ((final_memory - baseline_memory) / baseline_memory * 100) if baseline_memory > 0 else 0
            }

        return results

    async def benchmark_concurrent_load(self, load_config: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark concurrent load handling."""

        num_concurrent = load_config.get("concurrent_users", 10)
        duration = load_config.get("duration", 30)
        agent_type = load_config.get("agent_type", "general")
        prompt = load_config.get("prompt", "Hello, how are you?")

        print(f"  Testing {num_concurrent} concurrent users for {duration}s...")

        async def simulate_user(user_id: int):
            """Simulate a single user making requests."""
            user_results = {
                "requests_made": 0,
                "successful_requests": 0,
                "total_latency": 0,
                "errors": 0
            }

            start_time = time.time()

            while time.time() - start_time < duration:
                try:
                    result = await self.agent_pool.execute_task(agent_type, f"{prompt} (User {user_id})")

                    user_results["requests_made"] += 1
                    if result["success"]:
                        user_results["successful_requests"] += 1
                        user_results["total_latency"] += result.get("duration", 0)
                    else:
                        user_results["errors"] += 1

                except Exception as e:
                    user_results["errors"] += 1
                    break

            return user_results

        # Run concurrent users
        tasks = [simulate_user(i) for i in range(num_concurrent)]
        user_results = await asyncio.gather(*tasks)

        # Aggregate results
        total_requests = sum(r["requests_made"] for r in user_results)
        successful_requests = sum(r["successful_requests"] for r in user_results)
        total_errors = sum(r["errors"] for r in user_results)
        total_latency = sum(r["total_latency"] for r in user_results)

        avg_latency = total_latency / successful_requests if successful_requests > 0 else 0

        return {
            "concurrent_users": num_concurrent,
            "duration": duration,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "errors": total_errors,
            "success_rate": successful_requests / total_requests if total_requests > 0 else 0,
            "avg_latency": avg_latency,
            "requests_per_second": total_requests / duration,
            "user_results": user_results
        }

    async def benchmark_error_handling(self, error_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Benchmark error handling and recovery."""

        results = {}

        for test_case in error_tests:
            test_name = test_case["name"]
            agent_type = test_case["agent_type"]
            error_prompts = test_case["error_prompts"]
            iterations = test_case.get("iterations", 5)

            print(f"  Testing {test_name} error handling...")

            error_stats = {
                "total_tests": iterations * len(error_prompts),
                "successful_handling": 0,
                "error_types": {},
                "recovery_times": []
            }

            for _ in range(iterations):
                for error_prompt in error_prompts:
                    start_time = time.time()

                    try:
                        result = await self.agent_pool.execute_task(agent_type, error_prompt)

                        if not result["success"]:
                            # Check if error was handled gracefully
                            if "error" in result and len(result["error"]) > 0:
                                error_stats["successful_handling"] += 1

                            # Categorize error
                            error_msg = result.get("error", "unknown")
                            error_type = self.categorize_error(error_msg)
                            error_stats["error_types"][error_type] = error_stats["error_types"].get(error_type, 0) + 1

                    except Exception as e:
                        error_type = self.categorize_error(str(e))
                        error_stats["error_types"][error_type] = error_stats["error_types"].get(error_type, 0) + 1

                    recovery_time = time.time() - start_time
                    error_stats["recovery_times"].append(recovery_time)

            error_stats["avg_recovery_time"] = statistics.mean(error_stats["recovery_times"])
            error_stats["error_handling_rate"] = error_stats["successful_handling"] / error_stats["total_tests"]

            results[test_name] = error_stats

        return results

    def categorize_error(self, error_msg: str) -> str:
        """Categorize error types."""

        error_msg = error_msg.lower()

        if "timeout" in error_msg or "time" in error_msg:
            return "timeout"
        elif "rate limit" in error_msg or "quota" in error_msg:
            return "rate_limit"
        elif "authentication" in error_msg or "authorization" in error_msg:
            return "auth"
        elif "network" in error_msg or "connection" in error_msg:
            return "network"
        elif "memory" in error_msg or "out of memory" in error_msg:
            return "resource"
        else:
            return "other"

    def generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive benchmark summary."""

        summary = {
            "overall_health": "unknown",
            "performance_score": 0,
            "recommendations": []
        }

        # Analyze latency
        if "latency" in results:
            avg_latencies = [
                agent_results["mean_latency"]
                for agent_results in results["latency"].values()
            ]

            if avg_latencies:
                overall_avg_latency = statistics.mean(avg_latencies)
                summary["avg_latency"] = overall_avg_latency

                if overall_avg_latency < 2.0:
                    summary["latency_score"] = "excellent"
                elif overall_avg_latency < 5.0:
                    summary["latency_score"] = "good"
                elif overall_avg_latency < 10.0:
                    summary["latency_score"] = "acceptable"
                else:
                    summary["latency_score"] = "poor"
                    summary["recommendations"].append("High latency detected. Consider optimizing model or infrastructure.")

        # Analyze throughput
        if "throughput" in results:
            throughputs = [
                agent_results["throughput_tps"]
                for agent_results in results["throughput"].values()
            ]

            if throughputs:
                avg_throughput = statistics.mean(throughputs)
                summary["avg_throughput"] = avg_throughput

                if avg_throughput > 10:
                    summary["throughput_score"] = "excellent"
                elif avg_throughput > 5:
                    summary["throughput_score"] = "good"
                elif avg_throughput > 1:
                    summary["throughput_score"] = "acceptable"
                else:
                    summary["throughput_score"] = "poor"
                    summary["recommendations"].append("Low throughput detected. Consider scaling infrastructure.")

        # Analyze errors
        if "errors" in results:
            error_rates = []
            for test_results in results["errors"].values():
                error_handling_rate = test_results["error_handling_rate"]
                error_rates.append(error_handling_rate)

            if error_rates:
                avg_error_handling = statistics.mean(error_rates)
                summary["error_handling_rate"] = avg_error_handling

                if avg_error_handling > 0.9:
                    summary["error_score"] = "excellent"
                elif avg_error_handling > 0.7:
                    summary["error_score"] = "good"
                else:
                    summary["error_score"] = "needs_improvement"
                    summary["recommendations"].append("Error handling could be improved. Consider adding more robust error recovery.")

        # Overall health assessment
        scores = []
        if "latency_score" in summary:
            score_map = {"excellent": 4, "good": 3, "acceptable": 2, "poor": 1}
            scores.append(score_map.get(summary["latency_score"], 2))

        if "throughput_score" in summary:
            scores.append(score_map.get(summary["throughput_score"], 2))

        if "error_score" in summary:
            scores.append(score_map.get(summary["error_score"], 2))

        if scores:
            avg_score = statistics.mean(scores)
            summary["performance_score"] = avg_score

            if avg_score >= 3.5:
                summary["overall_health"] = "excellent"
            elif avg_score >= 2.5:
                summary["overall_health"] = "good"
            elif avg_score >= 1.5:
                summary["overall_health"] = "acceptable"
            else:
                summary["overall_health"] = "needs_attention"

        return summary

# Run comprehensive benchmark
benchmark_config = {
    "latency_tests": [
        {"agent_type": "general", "prompt": "Hello!", "iterations": 5},
        {"agent_type": "coder", "prompt": "Write a function", "iterations": 5}
    ],
    "throughput_tests": [
        {
            "agent_type": "general",
            "prompts": ["Hi", "Hello", "Hey"],
            "duration": 10
        }
    ],
    "memory_tests": [
        {"agent_type": "general", "prompts": ["Test"] * 10}
    ],
    "load_tests": {
        "concurrent_users": 5,
        "duration": 15,
        "agent_type": "general",
        "prompt": "Quick test"
    },
    "error_tests": [
        {
            "name": "invalid_requests",
            "agent_type": "general",
            "error_prompts": ["", "This prompt is way too long" * 1000],
            "iterations": 3
        }
    ]
}

benchmark_suite = ProductionBenchmarkSuite(monitored_pool)

# Run benchmarks
async def run_benchmarks():
    results = await benchmark_suite.run_comprehensive_benchmark(benchmark_config)

    print(f"\nBenchmark Summary:")
    print(f"Overall Health: {results['summary']['overall_health']}")
    print(f"Performance Score: {results['summary']['performance_score']:.2f}")

    if results['summary']['recommendations']:
        print("Recommendations:")
        for rec in results['summary']['recommendations']:
            print(f"  - {rec}")

    # Save detailed results
    with open("production_benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("Detailed results saved to production_benchmark_results.json")

asyncio.run(run_benchmarks())
```

This comprehensive production deployment chapter covers enterprise-scale infrastructure, monitoring, security, and performance optimization for Phidata agent systems. The implementation provides production-ready scalability and reliability. 🚀

## Quick Production Setup

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Or use Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Check health
curl https://agents.company.com/health

# Monitor metrics
curl https://agents.company.com/metrics

# Run benchmarks
python production_benchmarks.py
```

This completes the comprehensive Phidata production deployment guide.

## Operational Handoff

Treat this chapter as the production baseline for agent workloads:

- pin model/provider configs by environment and rotate keys on schedule
- enforce per-tenant rate limits and workload isolation for shared clusters
- alert on token-cost spikes, latency regressions, and downstream tool failures
- run disaster recovery drills for vector stores, session stores, and agent memory backends
- maintain benchmark baselines and rerun after runtime, model, or prompt-stack changes

With these operational controls, Phidata deployments stay predictable under real production load.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `agent_type`, `time` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment & Scaling Phidata Agents` as an operating subsystem inside **Phidata Tutorial: Building Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `agent`, `user_id`, `duration` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment & Scaling Phidata Agents` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `agent_type` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `time`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/phidatahq/phidata)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `agent_type` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Integrations - Connecting Phidata Agents to External Systems](07-integrations.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
