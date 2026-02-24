---
layout: default
title: "Pydantic AI Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 8: Production Deployment & Scaling Pydantic AI Systems

Welcome to **Chapter 8: Production Deployment & Scaling Pydantic AI Systems**. In this part of **Pydantic AI Tutorial: Type-Safe AI Agent Development**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy type-safe AI agent systems at enterprise scale with high availability, monitoring, and production best practices.

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
          │  Pydantic AI    │
          │   Services      │
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
          │   Task Queue    │
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

### Complete Pydantic AI Agent Deployment

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pydantic-ai
  labels:
    name: pydantic-ai

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pydantic-ai-config
  namespace: pydantic-ai
data:
  MODEL_NAME: "gpt-4"
  MAX_CONCURRENT_AGENTS: "10"
  AGENT_TIMEOUT: "300"
  CACHE_TTL: "3600"
  LOG_LEVEL: "INFO"
  ENABLE_METRICS: "true"
  DATABASE_URL: "postgresql://user:password@postgres:5432/pydanticai"
  REDIS_URL: "redis://redis:6379"
  VECTOR_DB_URL: "http://qdrant:6333"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: pydantic-ai-secrets
  namespace: pydantic-ai
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-your-openai-key"
  ANTHROPIC_API_KEY: "sk-ant-your-anthropic-key"
  DATABASE_PASSWORD: "your-db-password"
  REDIS_PASSWORD: "your-redis-password"
  API_SECRET_KEY: "your-api-secret"

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pydantic-ai-agents
  namespace: pydantic-ai
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 2
      maxSurge: 2
  selector:
    matchLabels:
      app: pydantic-ai-agent
  template:
    metadata:
      labels:
        app: pydantic-ai-agent
    spec:
      containers:
      - name: pydantic-ai-agent
        image: pydantic-ai/agents:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: pydantic-ai-config
        - secretRef:
            name: pydantic-ai-secrets
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
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: pydantic-ai-service
  namespace: pydantic-ai
spec:
  selector:
    app: pydantic-ai-agent
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pydantic-ai-hpa
  namespace: pydantic-ai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pydantic-ai-agents
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
  name: pydantic-ai-ingress
  namespace: pydantic-ai
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
    secretName: pydantic-ai-tls
  rules:
  - host: agents.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: pydantic-ai-service
            port:
              number: 80
```

## Docker Production Setup

### Multi-Service Production Stack

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Pydantic AI API Service
  pydantic-ai-api:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: pydantic-ai-api-prod
    restart: unless-stopped
    environment:
      - MODEL_NAME=gpt-4
      - MAX_CONCURRENT_AGENTS=20
      - AGENT_TIMEOUT=300
      - CACHE_TTL=3600
      - DATABASE_URL=postgresql://user:password@postgres:5432/pydanticai
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
    container_name: pydantic-ai-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=pydanticai
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d pydanticai"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    container_name: pydantic-ai-redis
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
    container_name: pydantic-ai-qdrant
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
    container_name: pydantic-ai-rabbitmq
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
    container_name: pydantic-ai-prometheus
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
    container_name: pydantic-ai-grafana
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

## Model Optimization for Production

### Advanced Model Configuration

```python
from pydantic_ai import Agent
from typing import Dict, Any, Optional
import torch
from transformers import BitsAndBytesConfig

class ProductionModelManager:
    """Production-ready model manager with optimization."""

    def __init__(self):
        self.models = {}
        self.model_configs = {
            'openai:gpt-4': {
                'cost_per_token': {'input': 0.03, 'output': 0.06},
                'context_window': 8192,
                'max_tokens': 4096
            },
            'openai:gpt-4-turbo': {
                'cost_per_token': {'input': 0.01, 'output': 0.03},
                'context_window': 128000,
                'max_tokens': 4096
            },
            'anthropic:claude-3-opus-20240229': {
                'cost_per_token': {'input': 15, 'output': 75},  # per million
                'context_window': 200000,
                'max_tokens': 4096
            },
            'anthropic:claude-3-haiku-20240307': {
                'cost_per_token': {'input': 0.25, 'output': 1.25},  # per million
                'context_window': 200000,
                'max_tokens': 4096
            },
            'google:gemini-1.5-pro': {
                'cost_per_token': {'input': 0.5, 'output': 1.5},  # per million chars
                'context_window': 1000000,
                'max_tokens': 8192
            },
            'groq:mixtral-8x7b-32768': {
                'cost_per_token': {'input': 0.27, 'output': 0.27},  # per million
                'context_window': 32768,
                'max_tokens': 4096
            }
        }

    def create_optimized_agent(self, model_string: str, task_type: str = "general") -> Agent:
        """Create agent optimized for specific task type."""

        base_config = self.model_configs.get(model_string, {})

        # Task-specific optimizations
        task_optimizations = {
            'creative': {
                'temperature': 0.9,
                'top_p': 0.95,
                'max_tokens': 1000
            },
            'analytical': {
                'temperature': 0.1,
                'top_p': 0.8,
                'max_tokens': 1500
            },
            'coding': {
                'temperature': 0.2,
                'top_p': 0.85,
                'max_tokens': 2000
            },
            'general': {
                'temperature': 0.7,
                'top_p': 0.9,
                'max_tokens': 1000
            }
        }

        model_settings = task_optimizations.get(task_type, task_optimizations['general'])
        model_settings.update(base_config)

        # Create agent with optimized settings
        agent = Agent(
            model_string,
            model_settings=model_settings
        )

        self.models[model_string] = agent
        return agent

    def get_model_stats(self, model_string: str) -> Dict[str, Any]:
        """Get model performance and cost statistics."""

        config = self.model_configs.get(model_string, {})

        return {
            'model': model_string,
            'context_window': config.get('context_window', 'unknown'),
            'max_tokens': config.get('max_tokens', 'unknown'),
            'cost_input_per_1k': config.get('cost_per_token', {}).get('input', 0) * 1000,
            'cost_output_per_1k': config.get('cost_per_token', {}).get('output', 0) * 1000,
            'estimated_latency': self._estimate_latency(model_string)
        }

    def _estimate_latency(self, model_string: str) -> str:
        """Estimate response latency for model."""

        latency_estimates = {
            'groq:mixtral-8x7b-32768': '0.5-2s',
            'anthropic:claude-3-haiku-20240307': '1-3s',
            'openai:gpt-3.5-turbo': '1-4s',
            'openai:gpt-4': '2-8s',
            'openai:gpt-4-turbo': '1-5s',
            'anthropic:claude-3-opus-20240229': '3-10s',
            'google:gemini-1.5-pro': '2-6s'
        }

        return latency_estimates.get(model_string, 'unknown')

    def select_optimal_model(self, requirements: Dict[str, Any]) -> str:
        """Select optimal model based on requirements."""

        candidates = list(self.model_configs.keys())

        # Filter by requirements
        if requirements.get('max_cost'):
            max_cost = requirements['max_cost']
            candidates = [
                model for model in candidates
                if self.model_configs[model]['cost_per_token']['input'] <= max_cost
            ]

        if requirements.get('min_context'):
            min_context = requirements['min_context']
            candidates = [
                model for model in candidates
                if self.model_configs[model]['context_window'] >= min_context
            ]

        if requirements.get('max_latency') == 'fast':
            # Prefer faster models
            fast_models = ['groq:mixtral-8x7b-32768', 'anthropic:claude-3-haiku-20240307']
            candidates = [model for model in candidates if model in fast_models]

        # Return cheapest available (simple strategy)
        if candidates:
            return min(candidates, key=lambda x: self.model_configs[x]['cost_per_token']['input'])

        return 'openai:gpt-4'  # Fallback

# Create production model manager
model_manager = ProductionModelManager()

# Create optimized agents for different tasks
creative_agent = model_manager.create_optimized_agent('openai:gpt-4', 'creative')
analytical_agent = model_manager.create_optimized_agent('anthropic:claude-3-haiku-20240307', 'analytical')
coding_agent = model_manager.create_optimized_agent('groq:mixtral-8x7b-32768', 'coding')

print("🎯 Optimized Agents Created:")
print(f"Creative: {creative_agent.model}")
print(f"Analytical: {analytical_agent.model}")
print(f"Coding: {coding_agent.model}")

# Get model statistics
stats = model_manager.get_model_stats('openai:gpt-4')
print("
📊 GPT-4 Stats:")
for key, value in stats.items():
    print(f"  {key}: {value}")

# Select optimal model
optimal = model_manager.select_optimal_model({
    'max_cost': 0.02,
    'min_context': 50000,
    'max_latency': 'fast'
})
print(f"\n🎯 Optimal model for requirements: {optimal}")
```

## Monitoring and Observability

### Comprehensive Agent Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import psutil

class ProductionAgentMetrics:
    """Production monitoring for Pydantic AI systems."""

    def __init__(self):
        # Agent metrics
        self.agent_requests_total = Counter(
            'pydantic_ai_agent_requests_total',
            'Total agent requests',
            ['agent_type', 'model', 'status']
        )

        self.agent_request_duration = Histogram(
            'pydantic_ai_agent_request_duration_seconds',
            'Agent request duration',
            ['agent_type', 'model']
        )

        self.active_agents = Gauge(
            'pydantic_ai_active_agents',
            'Number of currently active agents',
            ['agent_type']
        )

        # Model metrics
        self.model_tokens_total = Counter(
            'pydantic_ai_model_tokens_total',
            'Total tokens used by models',
            ['model', 'token_type']
        )

        self.model_cost_total = Counter(
            'pydantic_ai_model_cost_total',
            'Total cost by model',
            ['model']
        )

        # Validation metrics
        self.validation_errors_total = Counter(
            'pydantic_ai_validation_errors_total',
            'Total validation errors',
            ['error_type']
        )

        # System metrics
        self.memory_usage = Gauge(
            'pydantic_ai_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.cpu_usage = Gauge(
            'pydantic_ai_cpu_usage_percent',
            'CPU usage percentage'
        )

    def record_agent_request(self, agent_type: str, model: str, duration: float, status: str = "success"):
        """Record agent request metrics."""

        self.agent_requests_total.labels(agent_type, model, status).inc()
        self.agent_request_duration.labels(agent_type, model).observe(duration)

    def record_model_usage(self, model: str, prompt_tokens: int, completion_tokens: int, cost: float = 0):
        """Record model usage metrics."""

        self.model_tokens_total.labels(model, 'prompt').inc(prompt_tokens)
        self.model_tokens_total.labels(model, 'completion').inc(completion_tokens)

        if cost > 0:
            self.model_cost_total.labels(model).inc(cost)

    def record_validation_error(self, error_type: str):
        """Record validation error."""

        self.validation_errors_total.labels(error_type).inc()

    def set_active_agents(self, agent_type: str, count: int):
        """Set active agent count."""

        self.active_agents.labels(agent_type).set(count)

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
agent_metrics = ProductionAgentMetrics()

class MonitoredAgent(Agent):
    """Agent with built-in monitoring."""

    def __init__(self, agent_type: str = "general", **kwargs):
        super().__init__(**kwargs)
        self.agent_type = agent_type
        self.metrics = agent_metrics

    async def run_monitored(self, prompt: str, **kwargs):
        """Run agent with monitoring."""

        start_time = time.time()
        self.metrics.set_active_agents(self.agent_type, 1)
        self.metrics.update_system_metrics()

        try:
            result = await self.run(prompt, **kwargs)

            duration = time.time() - start_time

            # Record metrics
            self.metrics.record_agent_request(
                self.agent_type,
                self.model.model_name if hasattr(self.model, 'model_name') else str(self.model),
                duration,
                "success"
            )

            # Record token usage if available
            if hasattr(result, 'usage') and result.usage:
                self.metrics.record_model_usage(
                    str(self.model),
                    result.usage.prompt_tokens,
                    result.usage.completion_tokens
                )

            return result

        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_agent_request(self.agent_type, str(self.model), duration, "error")
            raise e

        finally:
            self.metrics.set_active_agents(self.agent_type, 0)

# Create monitored agents
monitored_creative = MonitoredAgent('creative', model='openai:gpt-4')
monitored_analytical = MonitoredAgent('analytical', model='anthropic:claude-3-haiku-20240307')

async def test_monitored_agents():
    """Test monitored agent functionality."""

    print("📊 Testing Monitored Agents:")

    # Test creative agent
    result1 = await monitored_creative.run_monitored("Write a haiku about AI")
    print(f"Creative agent: {len(result1.data)} chars")

    # Test analytical agent
    result2 = await monitored_analytical.run_monitored("Analyze the number 42")
    print(f"Analytical agent: {len(result2.data)} chars")

    # Show metrics
    print("
📈 Metrics Sample:")
    metrics_text = agent_metrics.get_metrics_text()
    # Show first few lines
    lines = metrics_text.split('\n')[:15]
    print('\n'.join(lines))
    print("... (truncated)")

asyncio.run(test_monitored_agents())
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
    """Enterprise-grade security for Pydantic AI systems."""

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

app = FastAPI(title="Secure Pydantic AI API", version="1.0.0")

@app.post("/agent/execute")
@require_security("agent:execute")
async def execute_agent(request: Request, payload: Dict[str, Any]):
    """Secure agent execution endpoint."""

    user = request.state.user

    # Execute agent with user context
    agent = MonitoredAgent(user.get("preferred_agent_type", "general"), model='openai:gpt-4')
    result = await agent.run_monitored(payload["prompt"])

    # Log the execution
    security_manager._audit_event("agent_execution", {
        "user_id": user["user_id"],
        "agent_type": payload.get("agent_type", "general"),
        "prompt_length": len(payload["prompt"])
    })

    return {
        "result": result.data,
        "user_id": user["user_id"],
        "execution_time": time.time()
    }

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
    """Comprehensive benchmarking for production Pydantic AI systems."""

    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    async def run_comprehensive_benchmark(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive production benchmark suite."""

        benchmark_results = {
            "timestamp": time.time(),
            "config": config,
            "results": {},
            "summary": {}
        }

        print("🚀 Starting Production Benchmark Suite...")

        # 1. Latency Benchmark
        print("📊 Running latency benchmark...")
        latency_results = await self.benchmark_latency(config.get("latency_tests", []))
        benchmark_results["results"]["latency"] = latency_results

        # 2. Throughput Benchmark
        print("⚡ Running throughput benchmark...")
        throughput_results = await self.benchmark_throughput(config.get("throughput_tests", []))
        benchmark_results["results"]["throughput"] = throughput_results

        # 3. Memory Usage Benchmark
        print("🧠 Running memory benchmark...")
        memory_results = await self.benchmark_memory_usage(config.get("memory_tests", []))
        benchmark_results["results"]["memory"] = memory_results

        # 4. Concurrent Load Test
        print("🎯 Running concurrent load test...")
        load_results = await self.benchmark_concurrent_load(config.get("load_tests", {}))
        benchmark_results["results"]["load"] = load_results

        # 5. Validation Performance Benchmark
        print("✅ Running validation benchmark...")
        validation_results = await self.benchmark_validation_performance(config.get("validation_tests", []))
        benchmark_results["results"]["validation"] = validation_results

        # Generate summary
        benchmark_results["summary"] = self.generate_summary(benchmark_results["results"])

        print("✅ Benchmark suite completed!")
        return benchmark_results

    async def benchmark_latency(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Benchmark response latency."""

        results = {}

        for test_case in test_cases:
            agent_template = test_case["agent_template"]
            prompt = test_case["prompt"]
            iterations = test_case.get("iterations", 10)

            print(f"  Testing {agent_template} latency...")

            agent = self.agent_factory.create_agent(agent_template)
            latencies = []

            for i in range(iterations):
                start_time = time.time()
                result = await agent.run(prompt)
                end_time = time.time()

                if hasattr(result, 'data'):
                    latencies.append(end_time - start_time)

            if latencies:
                results[agent_template] = {
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
            agent_template = test_case["agent_template"]
            prompts = test_case["prompts"]
            duration = test_case.get("duration", 60)  # seconds

            print(f"  Testing {agent_template} throughput for {duration}s...")

            agent = self.agent_factory.create_agent(agent_template)
            start_time = time.time()
            completed_tasks = 0
            errors = 0

            while time.time() - start_time < duration:
                for prompt in prompts:
                    try:
                        result = await agent.run(prompt)
                        if hasattr(result, 'data'):
                            completed_tasks += 1
                        else:
                            errors += 1
                    except:
                        errors += 1

            total_time = time.time() - start_time
            throughput = completed_tasks / total_time

            results[agent_template] = {
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
            agent_template = test_case["agent_template"]
            prompts = test_case["prompts"]

            print(f"  Testing {agent_template} memory usage...")

            # Get baseline memory
            process = psutil.Process(os.getpid())
            baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

            memory_readings = []

            agent = self.agent_factory.create_agent(agent_template)
            for prompt in prompts:
                result = await agent.run(prompt)
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_readings.append(current_memory)

            final_memory = process.memory_info().rss / 1024 / 1024

            results[agent_template] = {
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
        agent_template = load_config.get("agent_template", "general")
        prompt = load_config.get("prompt", "Hello, how are you?")

        print(f"  Testing {num_concurrent} concurrent users for {duration}s...")

        async def simulate_user(user_id: int):
            """Simulate a single user making requests."""
            agent = self.agent_factory.create_agent(agent_template)
            user_results = {
                "requests_made": 0,
                "successful_requests": 0,
                "total_latency": 0,
                "errors": 0
            }

            start_time = time.time()

            while time.time() - start_time < duration:
                try:
                    result = await agent.run(f"{prompt} (User {user_id})")

                    user_results["requests_made"] += 1
                    if hasattr(result, 'data'):
                        user_results["successful_requests"] += 1
                        user_results["total_latency"] += time.time() - time.time()  # Simplified
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

    async def benchmark_validation_performance(self, validation_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Benchmark validation performance."""

        results = {}

        for test_case in validation_tests:
            test_name = test_case["name"]
            model_class = test_case["model_class"]
            prompts = test_case["prompts"]
            iterations = test_case.get("iterations", 5)

            print(f"  Testing {test_name} validation performance...")

            agent = Agent('openai:gpt-4', result_type=model_class)
            validation_times = []
            success_count = 0

            for _ in range(iterations):
                for prompt in prompts:
                    start_time = time.time()
                    try:
                        result = await agent.run(prompt)
                        if hasattr(result, 'data'):
                            success_count += 1
                    except:
                        pass
                    validation_times.append(time.time() - start_time)

            results[test_name] = {
                "iterations": iterations,
                "prompts_per_iteration": len(prompts),
                "total_validations": iterations * len(prompts),
                "successful_validations": success_count,
                "success_rate": success_count / (iterations * len(prompts)),
                "avg_validation_time": statistics.mean(validation_times),
                "min_validation_time": min(validation_times),
                "max_validation_time": max(validation_times)
            }

        return results

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

        # Analyze validation performance
        if "validation" in results:
            success_rates = [
                test_results["success_rate"]
                for test_results in results["validation"].values()
            ]

            if success_rates:
                avg_success_rate = statistics.mean(success_rates)
                summary["validation_success_rate"] = avg_success_rate

                if avg_success_rate > 0.95:
                    summary["validation_score"] = "excellent"
                elif avg_success_rate > 0.85:
                    summary["validation_score"] = "good"
                else:
                    summary["validation_score"] = "needs_improvement"
                    summary["recommendations"].append("Validation success rate could be improved. Check model outputs and schemas.")

        # Overall health assessment
        scores = []
        score_map = {"excellent": 4, "good": 3, "acceptable": 2, "poor": 1}

        if "latency_score" in summary:
            scores.append(score_map.get(summary["latency_score"], 2))

        if "throughput_score" in summary:
            scores.append(score_map.get(summary["throughput_score"], 2))

        if "validation_score" in summary:
            scores.append(score_map.get(summary["validation_score"], 2))

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
        {"agent_template": "creative", "prompt": "Write a haiku", "iterations": 5},
        {"agent_template": "analytical", "prompt": "Analyze data", "iterations": 5}
    ],
    "throughput_tests": [
        {
            "agent_template": "general",
            "prompts": ["Hello", "Hi there", "Greetings"],
            "duration": 20
        }
    ],
    "memory_tests": [
        {"agent_template": "general", "prompts": ["Test memory"] * 10}
    ],
    "load_tests": {
        "concurrent_users": 5,
        "duration": 15,
        "agent_template": "general",
        "prompt": "Quick test"
    },
    "validation_tests": [
        {
            "name": "basic_validation",
            "model_class": Person,  # Assuming Person model is defined
            "prompts": ["Create a person profile"],
            "iterations": 3
        }
    ]
}

benchmark_suite = ProductionBenchmarkSuite(factory)

async def run_benchmarks():
    results = await benchmark_suite.run_comprehensive_benchmark(benchmark_config)

    print(f"\n🏆 Benchmark Summary:")
    print(f"Overall Health: {results['summary']['overall_health']}")
    print(f"Performance Score: {results['summary']['performance_score']:.2f}")

    if results['summary']['recommendations']:
        print("Recommendations:")
        for rec in results['summary']['recommendations']:
            print(f"  - {rec}")

    # Save detailed results
    with open("pydantic_ai_production_benchmark.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("Detailed results saved to pydantic_ai_production_benchmark.json")

asyncio.run(run_benchmarks())
```

This comprehensive production deployment chapter covers enterprise-scale infrastructure, monitoring, security, and performance optimization for Pydantic AI systems. The implementation provides production-ready scalability and reliability. 🚀

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

This completes the comprehensive Pydantic AI production deployment guide! 🎊

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `user_id`, `model` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment & Scaling Pydantic AI Systems` as an operating subsystem inside **Pydantic AI Tutorial: Type-Safe AI Agent Development**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `agent`, `time`, `summary` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment & Scaling Pydantic AI Systems` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `user_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/pydantic/pydantic-ai)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `user_id` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Advanced Patterns & Multi-Step Workflows](07-advanced-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
