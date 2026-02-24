---
layout: default
title: "Letta Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Letta Tutorial
---

# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **Letta Tutorial: Stateful LLM Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy Letta agents to production with scaling, monitoring, security, and operational best practices.

## Overview

Deploying Letta agents to production requires careful consideration of scaling, data persistence, security, and monitoring. This chapter covers production deployment patterns and operational practices.

## Production Architecture

Recommended production setup:

```
┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   API Gateway   │
│   (Nginx/HAProxy)│    │  (Kong/KrakenD)│
└─────────────────┘    └─────────────────┘
           │                       │
           └───────────────────────┘
                    │
          ┌─────────────────┐
          │  Letta Instances │
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

## Database Setup

Use PostgreSQL for production data persistence:

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=letta
      - POSTGRES_USER=letta
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U letta"]
      interval: 30s
      timeout: 10s
      retries: 3

  letta:
    image: letta/letta:latest
    environment:
      - LETTA_DB_URL=postgresql://letta:${DB_PASSWORD}@postgres:5432/letta
      - LETTA_REDIS_URL=redis://redis:6379
      - LETTA_API_KEY=${API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8283:8283"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Environment Configuration

Secure environment variables:

```bash
# .env.production
# Database
LETTA_DB_URL=postgresql://letta:secure_password@db.host:5432/letta

# Redis (optional)
LETTA_REDIS_URL=redis://redis.host:6379

# API Security
LETTA_API_KEY=your-secure-api-key-here
LETTA_JWT_SECRET=another-secure-random-string

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Logging
LOG_LEVEL=info
LOG_FORMAT=json

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

## Docker Production Build

Optimized Docker image for production:

```dockerfile
# Dockerfile.prod
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash letta

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership
RUN chown -R letta:letta /app

# Switch to non-root user
USER letta

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8283/health')"

EXPOSE 8283

CMD ["letta", "server", "--host", "0.0.0.0", "--port", "8283"]
```

## Kubernetes Deployment

Production Kubernetes manifest:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: letta
  labels:
    app: letta
spec:
  replicas: 3
  selector:
    matchLabels:
      app: letta
  template:
    metadata:
      labels:
        app: letta
    spec:
      containers:
      - name: letta
        image: your-registry/letta:latest
        ports:
        - containerPort: 8283
        envFrom:
        - secretRef:
            name: letta-secrets
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
            port: 8283
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8283
          initialDelaySeconds: 5
          periodSeconds: 5
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000

---
apiVersion: v1
kind: Service
metadata:
  name: letta-service
spec:
  selector:
    app: letta
  ports:
    - port: 80
      targetPort: 8283
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: letta-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: letta-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: letta-service
            port:
              number: 80
```

## Horizontal Scaling

Scale Letta instances based on load:

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: letta-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: letta
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
```

## Database Scaling

Handle database growth:

```sql
-- PostgreSQL optimization queries

-- Create indexes for performance
CREATE INDEX CONCURRENTLY idx_messages_agent_id ON messages(agent_id);
CREATE INDEX CONCURRENTLY idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX CONCURRENTLY idx_conversations_agent_id ON conversations(agent_id);

-- Partition large tables by month
CREATE TABLE messages_y2024m01 PARTITION OF messages
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Set up automated maintenance
ALTER SYSTEM SET autovacuum = on;
ALTER SYSTEM SET autovacuum_vacuum_scale_factor = 0.02;
ALTER SYSTEM SET autovacuum_analyze_scale_factor = 0.01;
```

## Backup Strategy

Comprehensive backup solution:

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Database backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/db_$DATE.sql.gz s3://letta-backups/

# Clean old backups (keep last 30 days)
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

# Verify backup
if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
else
    echo "Backup failed!" >&2
    exit 1
fi
```

## Security Hardening

Production security measures:

```yaml
# Security context for pods
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL

# Network policies
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: letta-network-policy
spec:
  podSelector:
    matchLabels:
      app: letta
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8283
  egress:
  - to:
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
  - to: []  # Allow external access for LLM APIs
```

## Monitoring and Observability

Comprehensive monitoring setup:

```yaml
# Prometheus metrics
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'letta'
      static_configs:
      - targets: ['letta-service:8283']
      metrics_path: '/metrics'

# Grafana dashboard for Letta metrics
# Key metrics to monitor:
# - Request latency (p50, p95, p99)
# - Error rate by endpoint
# - Active agents and conversations
# - Memory usage per agent
# - Token usage and costs
# - Database connection pool utilization
```

## Logging

Structured logging for production:

```python
# logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'agent_name'):
            log_entry['agent_name'] = record.agent_name
        if hasattr(record, 'conversation_id'):
            log_entry['conversation_id'] = record.conversation_id

        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('/app/logs/letta.log'),  # File output
    ]
)

# Add JSON formatter for structured logs
json_handler = logging.StreamHandler()
json_handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(json_handler)
```

## Performance Optimization

Production performance tips:

```python
# Performance settings
PRODUCTION_CONFIG = {
    # Database connection pooling
    "db_pool_size": 20,
    "db_max_overflow": 30,

    # Redis caching
    "redis_cache_ttl": 3600,  # 1 hour
    "redis_max_connections": 50,

    # Agent memory limits
    "max_core_memory_items": 100,
    "max_archival_memory_items": 10000,
    "max_recall_memory_messages": 50,

    # Rate limiting
    "requests_per_minute": 120,
    "burst_limit": 200,

    # Model settings
    "default_temperature": 0.7,
    "max_tokens_limit": 2000,
    "timeout_seconds": 30,
}

# Apply optimizations
def optimize_for_production():
    """Apply production optimizations."""
    # Connection pooling
    engine = create_engine(
        DATABASE_URL,
        pool_size=PRODUCTION_CONFIG["db_pool_size"],
        max_overflow=PRODUCTION_CONFIG["db_max_overflow"]
    )

    # Redis caching
    cache = Redis.from_url(REDIS_URL, max_connections=50)

    return engine, cache
```

## Cost Management

Monitor and control costs:

```python
# Cost tracking
class CostTracker:
    def __init__(self, redis_client):
        self.redis = redis_client

    def track_token_usage(self, agent_name, model, tokens, cost):
        """Track token usage and costs."""
        key = f"costs:{agent_name}:{datetime.now().strftime('%Y-%m-%d')}"

        self.redis.hincrbyfloat(key, "tokens", tokens)
        self.redis.hincrbyfloat(key, "cost", cost)
        self.redis.hincrby(key, f"model:{model}", tokens)

    def get_daily_costs(self, agent_name, date=None):
        """Get daily cost breakdown."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        key = f"costs:{agent_name}:{date}"
        return self.redis.hgetall(key)

    def alert_high_cost(self, threshold=50.0):
        """Alert on high daily costs."""
        today = datetime.now().strftime('%Y-%m-%d')
        keys = self.redis.keys(f"costs:*:{today}")

        for key in keys:
            cost = float(self.redis.hget(key, "cost") or 0)
            if cost > threshold:
                agent_name = key.split(":")[1]
                send_alert(f"High cost alert: {agent_name} exceeded ${threshold} today")

# Usage
cost_tracker = CostTracker(redis_client)
cost_tracker.track_token_usage("sam", "gpt-4o", 150, 0.003)
```

## Disaster Recovery

Recovery procedures:

```yaml
# Disaster recovery plan
# 1. Database failover (if using RDS/multi-AZ)
# 2. Application rollback to previous version
# 3. Data restoration from backups
# 4. Traffic shifting via load balancer
# 5. Monitoring and validation

# Kubernetes job for recovery
apiVersion: batch/v1
kind: Job
metadata:
  name: letta-recovery
spec:
  template:
    spec:
      containers:
      - name: recovery
        image: your-recovery-image
        command: ["/bin/bash", "-c"]
        args:
        - |
          # Restore from backup
          aws s3 cp s3://letta-backups/latest.sql.gz .
          gunzip latest.sql.gz
          psql -h $DB_HOST -U $DB_USER -d $DB_NAME < latest.sql

          # Validate restoration
          # Send test requests
          # Verify agent functionality
      restartPolicy: Never
```

## Compliance and Governance

Production compliance:

- **Data Retention**: Implement automatic data cleanup policies
- **Audit Logging**: Log all agent interactions for compliance
- **Access Control**: Role-based access control for agent management
- **Data Encryption**: Encrypt sensitive data at rest and in transit
- **Regular Updates**: Keep dependencies and base images updated

## Operational Playbook

Daily operations:

1. **Morning Checks**:
   - Verify all services are healthy
   - Check error rates and latency
   - Review overnight costs

2. **Performance Monitoring**:
   - Monitor resource utilization
   - Scale instances as needed
   - Optimize slow queries

3. **Incident Response**:
   - Automated alerts for failures
   - Runbook for common issues
   - Escalation procedures

4. **Maintenance Windows**:
   - Scheduled updates during low-traffic periods
   - Backup verification
   - Security patching

## Final Checklist

Before going live:

- [ ] Database properly configured and backed up
- [ ] Environment variables secured
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and alerting set up
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Rollback plan documented
- [ ] Team trained on operations
- [ ] Support channels established

With this production setup, Letta agents can reliably serve thousands of users while maintaining performance, security, and cost efficiency.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `letta`, `name`, `redis` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment` as an operating subsystem inside **Letta Tutorial: Stateful LLM Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `record`, `self`, `logging` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `letta`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `redis`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/letta-ai/letta)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `letta` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: REST API](07-api.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
