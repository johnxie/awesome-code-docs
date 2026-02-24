---
layout: default
title: "LiteLLM Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy LiteLLM applications to production with monitoring, scaling, security, and operational best practices.

## Overview

Production deployment of LiteLLM requires careful consideration of performance, reliability, security, and cost management. This chapter covers comprehensive production patterns for both direct LiteLLM usage and proxy deployments.

## Production Architecture

Recommended production setup:

```
┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │  Load Balancer  │
│  (Kong/AWS ALB) │    │   (Nginx/HAProxy)│
└─────────────────┘    └─────────────────┘
           │                       │
           └───────────────────────┘
                    │
          ┌─────────────────┐
          │  LiteLLM Proxy  │
          │   (Docker/K8s)  │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Database      │
          │ (PostgreSQL)    │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Redis Cache   │
          │   (Optional)    │
          └─────────────────┘
```

## Environment Configuration

Secure production environment variables:

```bash
# .env.production
# API Keys (use secret management in production)
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_API_KEY="..."
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."

# Database
DATABASE_URL="postgresql://user:secure_password@db.host:5432/litellm"

# Redis
REDIS_URL="redis://redis.host:6379"
REDIS_PASSWORD="secure_redis_password"

# Application Settings
LITELLM_LOG_LEVEL="INFO"
LITELLM_MASTER_KEY="sk-production-master-key"
LITELLM_GLOBAL_MAX_RPM=10000
LITELLM_GLOBAL_MAX_TPM=10000000

# Monitoring
DD_API_KEY="datadog-api-key"
SENTRY_DSN="sentry-dsn"
```

## Database Setup

Use PostgreSQL for production data persistence:

```sql
-- Production database schema
CREATE DATABASE litellm_prod;

-- Create application user
CREATE USER litellm_app WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE litellm_prod TO litellm_app;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

## Redis Configuration

Set up Redis for caching and rate limiting:

```yaml
# redis.conf (production settings)
maxmemory 256mb
maxmemory-policy allkeys-lru
tcp-keepalive 300
timeout 300
databases 16

# Security
requirepass your_secure_redis_password
rename-command FLUSHDB ""
rename-command FLUSHALL ""

# Persistence
save 900 1
save 300 10
save 60 10000
```

## Docker Production Deployment

Optimized production Docker setup:

```dockerfile
# Dockerfile.prod
FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r litellm && useradd -r -g litellm litellm

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=litellm:litellm . .

# Create data directory
RUN mkdir -p /app/data && chown litellm:litellm /app/data

# Switch to non-root user
USER litellm

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "-m", "litellm.proxy", "--config", "/app/config.yaml"]
```

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  litellm:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=litellm_prod
      - POSTGRES_USER=litellm_app
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U litellm_app -d litellm_prod"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  redis:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis.conf:/etc/redis/redis.conf:ro
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:
```

## Kubernetes Production Deployment

Enterprise-grade Kubernetes deployment:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm-proxy
  labels:
    app: litellm-proxy
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: litellm-proxy
  template:
    metadata:
      labels:
        app: litellm-proxy
        version: v1.0.0
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
      containers:
      - name: litellm
        image: your-registry/litellm:v1.0.0
        ports:
        - containerPort: 8000
          name: http
        envFrom:
        - configMapRef:
            name: litellm-config
        - secretRef:
            name: litellm-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: http
            scheme: HTTP
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: config-volume
          mountPath: /app/config.yaml
          subPath: config.yaml
          readOnly: true
      volumes:
      - name: config-volume
        configMap:
          name: litellm-config
          items:
          - key: config.yaml
            path: config.yaml

---
apiVersion: v1
kind: Service
metadata:
  name: litellm-service
  labels:
    app: litellm-proxy
spec:
  selector:
    app: litellm-proxy
  ports:
  - name: http
    port: 80
    targetPort: http
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: litellm-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - api.yourcompany.com
    secretName: litellm-tls
  rules:
  - host: api.yourcompany.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: litellm-service
            port:
              number: 80
```

## Horizontal Pod Autoscaling

Scale based on CPU and custom metrics:

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: litellm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: litellm-proxy
  minReplicas: 2
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
        averageValue: "50"
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

## Monitoring and Observability

Comprehensive monitoring setup:

```yaml
# Prometheus metrics collection
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: litellm-servicemonitor
  labels:
    team: backend
spec:
  selector:
    matchLabels:
      app: litellm-proxy
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

Key metrics to monitor:

- **Request Rate**: Requests per second by endpoint and model
- **Latency**: P95 response times
- **Error Rate**: 4xx and 5xx error percentages
- **Cost Tracking**: Spend by user, model, and time period
- **Token Usage**: Input/output tokens per request
- **Rate Limiting**: Throttled requests percentage
- **Cache Hit Rate**: Cache effectiveness
- **Database Connections**: Pool utilization

## Logging Configuration

Structured logging for production:

```python
# logging_config.py
import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['service'] = 'litellm-proxy'
        log_record['version'] = '1.0.0'

        # Add contextual fields if available
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'model'):
            log_record['model'] = record.model
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler for development
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomJsonFormatter())
logger.addHandler(console_handler)

# File handler for production
file_handler = logging.FileHandler('/app/logs/litellm.log')
file_handler.setFormatter(CustomJsonFormatter())
logger.addHandler(file_handler)

# Error file handler
error_handler = logging.FileHandler('/app/logs/error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(CustomJsonFormatter())
logger.addHandler(error_handler)
```

## Security Hardening

Production security measures:

```yaml
# Network policies
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: litellm-network-policy
spec:
  podSelector:
    matchLabels:
      app: litellm-proxy
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
  - to: []  # Allow external access for LLM APIs
    ports:
    - protocol: TCP
      port: 443
```

## Backup and Recovery

Automated backup strategy:

```yaml
# k8s/backup-job.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: litellm-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: litellm-secrets
                  key: db-password
            command:
            - /bin/sh
            - -c
            - |
              # Database backup
              pg_dump -h postgres -U litellm_app litellm_prod > /backup/daily_backup.sql

              # Compress
              gzip /backup/daily_backup.sql

              # Upload to S3
              aws s3 cp /backup/daily_backup.sql.gz s3://litellm-backups/$(date +%Y%m%d).sql.gz

              # Clean old local backups
              find /backup -name "*.sql.gz" -mtime +7 -delete
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
          restartPolicy: OnFailure
          volumes:
          - name: backup-volume
            emptyDir: {}
```

## Cost Optimization

Production cost management:

```python
# cost_optimization.py
import litellm
from typing import Dict, List
import time

class ProductionCostOptimizer:
    def __init__(self):
        self.model_costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
            "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
        }

    def select_optimal_model(self, messages: List[Dict], task_complexity: str = "medium") -> str:
        """Select cost-optimal model for task complexity."""

        # Estimate token count
        text = " ".join([msg["content"] for msg in messages])
        estimated_tokens = len(text.split()) * 1.3

        # Adjust for task complexity
        complexity_multipliers = {
            "low": 0.5,      # Simple tasks
            "medium": 1.0,   # Standard tasks
            "high": 2.0,     # Complex reasoning
            "creative": 1.5  # Creative tasks
        }

        multiplier = complexity_multipliers.get(task_complexity, 1.0)
        estimated_output_tokens = min(1000, estimated_tokens * multiplier * 0.3)

        # Find best model within constraints
        candidates = []
        for model, costs in self.model_costs.items():
            estimated_cost = (
                (estimated_tokens / 1000) * costs["input"] +
                (estimated_output_tokens / 1000) * costs["output"]
            )

            # Skip expensive models for simple tasks
            if task_complexity == "low" and estimated_cost > 0.005:
                continue

            candidates.append((model, estimated_cost))

        if not candidates:
            return "gpt-3.5-turbo"  # Safe fallback

        # Return cheapest suitable model
        return min(candidates, key=lambda x: x[1])[0]

    def completion_with_cost_control(self, messages: List[Dict], user_budget: float = None, **kwargs):
        """Completion with cost control and optimization."""

        # Select optimal model
        task_complexity = kwargs.pop("task_complexity", "medium")
        model = self.select_optimal_model(messages, task_complexity)

        # Check budget if provided
        if user_budget is not None:
            estimated_cost = self.estimate_cost(model, messages)
            if estimated_cost > user_budget:
                # Try cheaper model
                model = "gpt-3.5-turbo"
                estimated_cost = self.estimate_cost(model, messages)
                if estimated_cost > user_budget:
                    raise ValueError(f"Estimated cost ${estimated_cost:.4f} exceeds budget ${user_budget:.2f}")

        # Make request with timeout and retries
        start_time = time.time()
        response = litellm.completion(
            model=model,
            messages=messages,
            timeout=30,
            **kwargs
        )

        # Log cost and performance
        duration = time.time() - start_time
        actual_cost = getattr(response, '_hidden_params', {}).get('response_cost', 0)

        print(f"Model: {model}, Cost: ${actual_cost:.4f}, Duration: {duration:.2f}s")

        return response, model, actual_cost

# Usage
optimizer = ProductionCostOptimizer()

response, model_used, cost = optimizer.completion_with_cost_control(
    messages=[{"role": "user", "content": "Write a Python function to sort a list"}],
    task_complexity="low",
    user_budget=0.01
)
```

## Performance Optimization

Production performance tips:

1. **Connection Pooling**: Reuse HTTP connections to providers
2. **Response Caching**: Cache frequent queries with Redis
3. **Async Processing**: Use async/await for concurrent requests
4. **Batch Processing**: Combine multiple small requests
5. **Model Warm-up**: Pre-warm connections to avoid cold starts
6. **Resource Limits**: Set appropriate CPU/memory limits

## Disaster Recovery

Recovery procedures:

```yaml
# disaster-recovery.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: disaster-recovery
data:
  runbook.md: |
    # Disaster Recovery Procedures

    ## Database Failure
    1. Check database connectivity: `kubectl exec -it postgres-pod -- pg_isready`
    2. If down, scale up replica: `kubectl scale deployment postgres --replicas=1`
    3. Restore from backup if needed
    4. Update DNS if endpoint changed

    ## Application Failure
    1. Check pod status: `kubectl get pods -l app=litellm-proxy`
    2. View logs: `kubectl logs -l app=litellm-proxy --tail=100`
    3. Restart deployment: `kubectl rollout restart deployment/litellm-proxy`
    4. If persistent, rollback: `kubectl rollout undo deployment/litellm-proxy`

    ## Provider Outage
    - Check status pages (OpenAI, Anthropic, etc.)
    - Switch to fallback models in config
    - Notify users of potential delays
    - Monitor error rates and auto-scale if needed

    ## Full System Recovery
    1. Restore database from S3 backup
    2. Redeploy application with latest image
    3. Verify all integrations work
    4. Run smoke tests against all endpoints
```

## Compliance and Governance

Production compliance:

- **Data Encryption**: Encrypt data at rest and in transit
- **Audit Logging**: Log all API access and model usage
- **Access Control**: Implement role-based access with SSO
- **Data Retention**: Automatic cleanup of old logs and data
- **GDPR Compliance**: Handle user data deletion requests
- **Cost Governance**: Department-level budget controls

## Operational Playbook

Daily operations:

1. **Morning Checks**:
   - Verify all services are healthy
   - Check error rates and latency trends
   - Review overnight costs and usage

2. **Performance Monitoring**:
   - Monitor resource utilization
   - Scale services based on load
   - Optimize slow queries

3. **Cost Management**:
   - Review spending by user and model
   - Adjust rate limits and budgets
   - Identify cost optimization opportunities

4. **Security Reviews**:
   - Check for unusual access patterns
   - Review failed authentication attempts
   - Update security patches

5. **Capacity Planning**:
   - Monitor usage trends
   - Plan for seasonal load increases
   - Evaluate new model additions

## Final Production Checklist

Before going live:

- [ ] Environment variables configured securely
- [ ] Database and Redis properly set up
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and alerting configured
- [ ] Load testing completed successfully
- [ ] Security audit passed
- [ ] Backup and recovery tested
- [ ] Team trained on operations
- [ ] Rollback procedures documented
- [ ] Cost budgets and alerts set
- [ ] Performance benchmarks established

This production setup ensures LiteLLM can handle enterprise-scale workloads while maintaining reliability, security, and cost efficiency. The modular architecture allows for easy scaling and maintenance as your AI usage grows.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `litellm`, `name`, `model` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `proxy`, `redis`, `config` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `litellm`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
  Why it matters: authoritative reference on `LiteLLM Repository` (github.com).
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
  Why it matters: authoritative reference on `LiteLLM Releases` (github.com).
- [LiteLLM Docs](https://docs.litellm.ai/)
  Why it matters: authoritative reference on `LiteLLM Docs` (docs.litellm.ai).

Suggested trace strategy:
- search upstream code for `litellm` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: LiteLLM Proxy](07-proxy.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
