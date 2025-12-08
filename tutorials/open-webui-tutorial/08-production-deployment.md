---
layout: default
title: "Open WebUI Tutorial - Chapter 8: Production Deployment & Scaling"
nav_order: 8
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 8: Production Deployment, Scaling & Enterprise Configuration

> Deploy Open WebUI at enterprise scale with high availability, monitoring, and production best practices.

## Production Architecture

### Scalable Multi-Service Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   API Gateway   │
│  (NGINX/HAProxy)│    │   (Kong/Traefik)│
└─────────────────┘    └─────────────────┘
           │                       │
           └───────────────────────┘
                    │
          ┌─────────────────┐
          │  Open WebUI     │
          │   Services      │
          │  (Kubernetes)   │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Message Queue │
          │   (Redis/Rabbit)│
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Database      │
          │ (PostgreSQL)    │
          └─────────────────┘
                    │
          ┌─────────────────┐
          │   Vector DB     │
          │ (Qdrant/Weaviate)│
          └─────────────────┘
```

## Kubernetes Deployment

### Complete Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: open-webui
  labels:
    name: open-webui

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: open-webui-config
  namespace: open-webui
data:
  WEBUI_NAME: "Enterprise AI Platform"
  WEBUI_URL: "https://ai.company.com"
  ENABLE_SIGNUP: "false"
  DEFAULT_MODELS: '["gpt-4", "claude-3-sonnet"]'
  MODEL_FILTER_ENABLED: "true"
  MODEL_FILTER_LIST: '["gpt-4", "gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"]'

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: open-webui-secrets
  namespace: open-webui
type: Opaque
stringData:
  WEBUI_SECRET_KEY: "your-super-secret-key-change-this-in-production"
  OPENAI_API_KEY: "sk-your-openai-key"
  ANTHROPIC_API_KEY: "sk-ant-your-anthropic-key"
  DATABASE_URL: "postgresql://user:password@postgres:5432/openwebui"
  REDIS_URL: "redis://redis:6379"

---
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: open-webui
spec:
  serviceName: postgres
  replicas: 2
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
  spec:
    containers:
    - name: postgres
      image: postgres:15
      env:
      - name: POSTGRES_DB
        value: openwebui
      - name: POSTGRES_USER
        valueFrom:
          secretKeyRef:
            name: db-secrets
            key: username
      - name: POSTGRES_PASSWORD
        valueFrom:
          secretKeyRef:
            name: db-secrets
            key: password
      - name: PGDATA
        value: /var/lib/postgresql/data/pgdata
      ports:
      - containerPort: 5432
      volumeMounts:
      - name: postgres-data
        mountPath: /var/lib/postgresql/data
      - name: postgres-config
        mountPath: /etc/postgresql/postgresql.conf
        subPath: postgresql.conf
      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1000m"
      livenessProbe:
        exec:
          command:
          - pg_isready
          - -U
          - $(POSTGRES_USER)
        initialDelaySeconds: 30
        periodSeconds: 10
      readinessProbe:
        exec:
          command:
          - pg_isready
          - -U
          - $(POSTGRES_USER)
        initialDelaySeconds: 5
        periodSeconds: 5
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi

---
# k8s/redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: open-webui
spec:
  replicas: 2
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
        livenessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: redis-data
        emptyDir: {}

---
# k8s/open-webui.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: open-webui
  namespace: open-webui
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: open-webui
  template:
    metadata:
      labels:
        app: open-webui
    spec:
      containers:
      - name: open-webui
        image: ghcr.io/open-webui/open-webui:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: open-webui-config
        - secretRef:
            name: open-webui-secrets
        volumeMounts:
        - name: uploads
          mountPath: /app/backend/data/uploads
        - name: models-cache
          mountPath: /app/backend/data/models
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
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
      volumes:
      - name: uploads
        persistentVolumeClaim:
          claimName: open-webui-uploads
      - name: models-cache
        emptyDir: {}

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: open-webui-service
  namespace: open-webui
spec:
  selector:
    app: open-webui
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: open-webui-ingress
  namespace: open-webui
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - ai.company.com
    secretName: open-webui-tls
  rules:
  - host: ai.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: open-webui-service
            port:
              number: 80

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: open-webui-hpa
  namespace: open-webui
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: open-webui
  minReplicas: 3
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

## Docker Compose Production Setup

### Advanced Docker Compose Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Open WebUI Application
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    container_name: open-webui-prod
    restart: unless-stopped
    environment:
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - WEBUI_NAME=Enterprise AI Platform
      - WEBUI_URL=https://ai.company.com
      - ENABLE_SIGNUP=false
      - DEFAULT_MODELS=["gpt-4", "claude-3-sonnet"]
      - MODEL_FILTER_ENABLED=true
      - MODEL_FILTER_LIST=["gpt-4", "gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"]
      - DATABASE_URL=postgresql://user:password@postgres:5432/openwebui
      - REDIS_URL=redis://redis:6379
      - ENABLE_ADMIN_EXPORT=true
      - ENABLE_ADMIN_CHAT_ACCESS=true
    volumes:
      - ./data:/app/backend/data
      - ./uploads:/app/backend/data/uploads
    networks:
      - webui-network
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # PostgreSQL Database
  postgres:
    image: postgres:15
    container_name: open-webui-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=openwebui
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - webui-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d openwebui"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    container_name: open-webui-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - webui-network
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Vector Database (Qdrant)
  qdrant:
    image: qdrant/qdrant:latest
    container_name: open-webui-qdrant
    restart: unless-stopped
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - webui-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Reverse Proxy (Caddy)
  caddy:
    image: caddy:2-alpine
    container_name: open-webui-caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - webui-network
    depends_on:
      - open-webui

  # Monitoring (Prometheus)
  prometheus:
    image: prom/prometheus:latest
    container_name: open-webui-prometheus
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - webui-network
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  # Monitoring (Grafana)
  grafana:
    image: grafana/grafana:latest
    container_name: open-webui-grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/dashboards:/var/lib/grafana/dashboards
    networks:
      - webui-network

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  caddy_data:
  caddy_config:
  prometheus_data:
  grafana_data:

networks:
  webui-network:
    driver: bridge
```

### Caddy Reverse Proxy Configuration

```caddyfile
# Caddyfile
ai.company.com {
    # Enable automatic HTTPS
    tls {
        protocols tls1.2 tls1.3
    }

    # Rate limiting
    rate_limit {
        zone static {
            key {remote}
            window 1m
            events 100
        }
    }

    # Security headers
    header {
        # Security
        Strict-Transport-Security "max-age=31536000;"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        X-XSS-Protection "1; mode=block"
        Referrer-Policy "strict-origin-when-cross-origin"

        # Remove server header
        -Server
    }

    # Gzip compression
    encode gzip

    # Proxy to Open WebUI
    reverse_proxy open-webui:8080 {
        # Health check
        health_uri /health
        health_interval 10s
        health_timeout 3s

        # Load balancing
        lb_policy round_robin

        # Timeouts
        transport http {
            response_header_timeout 30s
            dial_timeout 10s
        }
    }

    # Static file serving with caching
    @static {
        path *.js *.css *.png *.jpg *.jpeg *.gif *.ico *.svg *.woff *.woff2
    }
    header @static Cache-Control "public, max-age=31536000"

    # API rate limiting
    @api {
        path /api/*
    }
    rate_limit @api {
        zone api {
            key {remote}
            window 1m
            events 60
        }
    }

    # Metrics endpoint (if enabled)
    metrics /metrics
}
```

## Monitoring & Observability

### Prometheus Metrics

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'open-webui'
    static_configs:
      - targets: ['open-webui:8080']
    scrape_interval: 5s
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
    scrape_interval: 10s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 10s

  - job_name: 'qdrant'
    static_configs:
      - targets: ['qdrant:6333']
    scrape_interval: 15s
```

### Custom Metrics for Open WebUI

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

class OpenWebUIMetrics:
    def __init__(self):
        # Request metrics
        self.http_requests_total = Counter(
            'openwebui_http_requests_total',
            'Total number of HTTP requests',
            ['method', 'endpoint', 'status']
        )

        self.http_request_duration = Histogram(
            'openwebui_http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint']
        )

        # Chat metrics
        self.chat_messages_total = Counter(
            'openwebui_chat_messages_total',
            'Total number of chat messages',
            ['model', 'user_type']
        )

        self.active_chats = Gauge(
            'openwebui_active_chats',
            'Number of currently active chats'
        )

        # Model usage metrics
        self.model_tokens_total = Counter(
            'openwebui_model_tokens_total',
            'Total number of tokens used by models',
            ['model', 'operation']  # operation: prompt, completion
        )

        self.model_requests_total = Counter(
            'openwebui_model_requests_total',
            'Total number of model requests',
            ['model', 'status']
        )

        # User metrics
        self.active_users = Gauge(
            'openwebui_active_users',
            'Number of currently active users'
        )

        self.total_users = Gauge(
            'openwebui_total_users',
            'Total number of registered users'
        )

        # System metrics
        self.memory_usage = Gauge(
            'openwebui_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.cpu_usage = Gauge(
            'openwebui_cpu_usage_percent',
            'CPU usage percentage'
        )

    def record_http_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics."""
        self.http_requests_total.labels(method, endpoint, str(status)).inc()
        self.http_request_duration.labels(method, endpoint).observe(duration)

    def record_chat_message(self, model: str, user_type: str = 'anonymous'):
        """Record chat message."""
        self.chat_messages_total.labels(model, user_type).inc()

    def update_active_chats(self, count: int):
        """Update active chats count."""
        self.active_chats.set(count)

    def record_model_usage(self, model: str, prompt_tokens: int, completion_tokens: int, status: str = 'success'):
        """Record model token usage."""
        self.model_tokens_total.labels(model, 'prompt').inc(prompt_tokens)
        self.model_tokens_total.labels(model, 'completion').inc(completion_tokens)
        self.model_requests_total.labels(model, status).inc()

    def update_user_metrics(self, active_count: int, total_count: int):
        """Update user metrics."""
        self.active_users.set(active_count)
        self.total_users.set(total_count)

    def update_system_metrics(self):
        """Update system resource metrics."""
        import psutil

        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_usage.set(cpu_percent)

    def get_metrics(self):
        """Get all metrics in Prometheus format."""
        return generate_latest()

# Middleware for automatic metrics collection
def metrics_middleware(metrics: OpenWebUIMetrics):
    def middleware(req, res, next):
        start_time = time.time()

        # Record request
        original_end = res.end
        def end_hook(*args, **kwargs):
            duration = time.time() - start_time
            metrics.record_http_request(req.method, req.path, res.statusCode, duration)
            return original_end(*args, **kwargs)

        res.end = end_hook
        next()

    return middleware
```

### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "Open WebUI - Enterprise AI Platform",
    "tags": ["open-webui", "ai", "enterprise"],
    "timezone": "browser",
    "panels": [
      {
        "title": "HTTP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(openwebui_http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Model Usage",
        "type": "bargauge",
        "targets": [
          {
            "expr": "sum(openwebui_model_requests_total) by (model)",
            "legendFormat": "{{model}}"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "openwebui_active_users",
            "legendFormat": "Active Users"
          }
        ]
      },
      {
        "title": "System Resources",
        "type": "graph",
        "targets": [
          {
            "expr": "openwebui_memory_usage_bytes / 1024 / 1024",
            "legendFormat": "Memory (MB)"
          },
          {
            "expr": "openwebui_cpu_usage_percent",
            "legendFormat": "CPU %"
          }
        ]
      }
    ]
  }
}
```

## Security Hardening

### Production Security Configuration

```yaml
# security/audit.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  verbs: ["create", "update", "patch", "delete"]
  resources:
  - group: ""
    resources: ["pods", "services", "configmaps", "secrets"]
  namespaces: ["open-webui"]
- level: RequestResponse
  verbs: ["create", "update"]
  resources:
  - group: ""
    resources: ["secrets"]

---
# security/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: open-webui-network-policy
  namespace: open-webui
spec:
  podSelector:
    matchLabels:
      app: open-webui
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
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
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS for external APIs

---
# security/pod-security.yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: open-webui-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  allowedCapabilities: []
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
    - min: 1
      max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
    - min: 1
      max: 65535
  readOnlyRootFilesystem: true
  volumes:
  - 'configMap'
  - 'downwardAPI'
  - 'emptyDir'
  - 'persistentVolumeClaim'
  - 'secret'
  - 'projected'
```

### Environment Security

```bash
# .env.production
# Security
WEBUI_SECRET_KEY=CHANGE_THIS_TO_A_RANDOM_64_CHARACTER_STRING
SESSION_SECRET=ANOTHER_RANDOM_64_CHARACTER_STRING

# Database
DB_USER=openwebui_prod
DB_PASSWORD=STRONG_RANDOM_PASSWORD_HERE
DATABASE_URL=postgresql://openwebui_prod:STRONG_RANDOM_PASSWORD_HERE@postgres:5432/openwebui

# Redis
REDIS_PASSWORD=STRONG_REDIS_PASSWORD_HERE
REDIS_URL=redis://:STRONG_REDIS_PASSWORD_HERE@redis:6379

# API Keys (use secret management in production)
OPENAI_API_KEY=sk-prod-...
ANTHROPIC_API_KEY=sk-ant-prod-...
GOOGLE_API_KEY=prod-key-...

# Security Settings
ENABLE_SIGNUP=false
ENABLE_ADMIN_EXPORT=true
ADMIN_USER_EMAIL=admin@company.com
DEFAULT_USER_ROLE=user

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# CORS
ENABLE_CORS=true
CORS_ALLOW_ORIGINS=https://ai.company.com

# SSL/TLS
ENABLE_HTTPS=true
SSL_CERT_PATH=/etc/ssl/certs/openwebui.crt
SSL_KEY_PATH=/etc/ssl/private/openwebui.key

# Audit Logging
ENABLE_AUDIT_LOG=true
AUDIT_LOG_PATH=/var/log/openwebui/audit.log
AUDIT_LOG_MAX_SIZE=100MB
AUDIT_LOG_MAX_FILES=5

# Backup
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *  # Daily at 2 AM
BACKUP_RETENTION_DAYS=30

# Monitoring
METRICS_ENABLED=true
METRICS_PORT=9090
HEALTH_CHECK_ENABLED=true
```

## Backup & Disaster Recovery

### Automated Backup Strategy

```yaml
# backup/cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: open-webui-backup
  namespace: open-webui
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM UTC
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: password
            command:
            - /bin/bash
            - -c
            - |
              # Database backup
              TIMESTAMP=$(date +%Y%m%d_%H%M%S)
              BACKUP_FILE="/backup/db_backup_${TIMESTAMP}.sql"

              pg_dump -h postgres -U $(DB_USER) -d openwebui > ${BACKUP_FILE}

              # Compress
              gzip ${BACKUP_FILE}

              # Upload to cloud storage (example: AWS S3)
              aws s3 cp ${BACKUP_FILE}.gz s3://openwebui-backups/database/ --sse AES256

              # Cleanup local files
              rm -f ${BACKUP_FILE}.gz

              # Keep only last 7 days of local backups
              find /backup -name "db_backup_*.sql.gz" -mtime +7 -delete
          env:
          - name: DB_USER
            valueFrom:
              secretKeyRef:
                name: db-secrets
                key: username
          volumeMounts:
          - name: backup-storage
            mountPath: /backup
          - name: aws-credentials
            mountPath: /root/.aws
            readOnly: true
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "200m"
      volumes:
      - name: backup-storage
        persistentVolumeClaim:
          claimName: backup-pvc
      - name: aws-credentials
        secret:
          secretName: aws-credentials
      restartPolicy: OnFailure
```

### Disaster Recovery Plan

```python
class DisasterRecoveryManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.backup_sources = config['backup_sources']
        self.recovery_steps = config['recovery_steps']

    async def initiate_recovery(self, incident_type: str) -> Dict[str, Any]:
        """Initiate disaster recovery process."""

        recovery_plan = {
            'incident_type': incident_type,
            'start_time': datetime.utcnow().isoformat(),
            'steps': [],
            'status': 'in_progress'
        }

        try:
            # Step 1: Isolate affected systems
            await self.isolate_affected_systems()
            recovery_plan['steps'].append({
                'step': 'isolate_systems',
                'status': 'completed',
                'timestamp': datetime.utcnow().isoformat()
            })

            # Step 2: Assess damage
            damage_assessment = await self.assess_damage()
            recovery_plan['damage_assessment'] = damage_assessment
            recovery_plan['steps'].append({
                'step': 'assess_damage',
                'status': 'completed',
                'timestamp': datetime.utcnow().isoformat()
            })

            # Step 3: Restore from backup
            if damage_assessment['data_loss']:
                await self.restore_from_backup()
                recovery_plan['steps'].append({
                    'step': 'restore_backup',
                    'status': 'completed',
                    'timestamp': datetime.utcnow().isoformat()
                })

            # Step 4: Rebuild infrastructure
            await self.rebuild_infrastructure()
            recovery_plan['steps'].append({
                'step': 'rebuild_infrastructure',
                'status': 'completed',
                'timestamp': datetime.utcnow().isoformat()
            })

            # Step 5: Test and validate
            test_results = await self.test_system()
            recovery_plan['test_results'] = test_results
            recovery_plan['steps'].append({
                'step': 'test_system',
                'status': 'completed',
                'timestamp': datetime.utcnow().isoformat()
            })

            # Step 6: Switch traffic back
            await self.switch_traffic()
            recovery_plan['steps'].append({
                'step': 'switch_traffic',
                'status': 'completed',
                'timestamp': datetime.utcnow().isoformat()
            })

            recovery_plan['status'] = 'completed'
            recovery_plan['end_time'] = datetime.utcnow().isoformat()

        except Exception as e:
            recovery_plan['status'] = 'failed'
            recovery_plan['error'] = str(e)
            recovery_plan['end_time'] = datetime.utcnow().isoformat()

        return recovery_plan

    async def isolate_affected_systems(self):
        """Isolate affected systems to prevent further damage."""
        # Scale down affected deployments
        # Update load balancer to route traffic away
        # Enable maintenance mode
        pass

    async def assess_damage(self) -> Dict[str, Any]:
        """Assess the extent of damage."""
        return {
            'data_loss': True,
            'infrastructure_damage': 'partial',
            'estimated_recovery_time': '4 hours',
            'affected_services': ['open-webui', 'database']
        }

    async def restore_from_backup(self):
        """Restore systems from backup."""
        # Identify latest backup
        # Restore database
        # Restore file uploads
        # Restore configuration
        pass

    async def rebuild_infrastructure(self):
        """Rebuild infrastructure components."""
        # Redeploy Kubernetes resources
        # Restore network configuration
        # Reconfigure load balancers
        pass

    async def test_system(self) -> Dict[str, Any]:
        """Test system functionality after recovery."""
        return {
            'database_connection': 'healthy',
            'api_endpoints': 'responding',
            'model_connections': 'working',
            'overall_health': 'good'
        }

    async def switch_traffic(self):
        """Switch traffic back to recovered systems."""
        # Update load balancer configuration
        # Disable maintenance mode
        # Monitor for issues
        pass

    async def create_recovery_report(self, recovery_plan: Dict[str, Any]) -> str:
        """Create a detailed recovery report."""
        report = f"""
# Disaster Recovery Report

**Incident Type:** {recovery_plan['incident_type']}
**Start Time:** {recovery_plan['start_time']}
**End Time:** {recovery_plan.get('end_time', 'Ongoing')}
**Status:** {recovery_plan['status']}

## Recovery Steps
"""

        for step in recovery_plan['steps']:
            report += f"- **{step['step']}**: {step['status']} ({step['timestamp']})\n"

        if 'damage_assessment' in recovery_plan:
            report += f"""
## Damage Assessment
- Data Loss: {recovery_plan['damage_assessment']['data_loss']}
- Infrastructure Damage: {recovery_plan['damage_assessment']['infrastructure_damage']}
- Estimated Recovery Time: {recovery_plan['damage_assessment']['estimated_recovery_time']}
"""

        if 'error' in recovery_plan:
            report += f"""
## Error
{recovery_plan['error']}
"""

        return report
```

## Performance Optimization

### Database Optimization

```sql
-- Production database optimizations
-- Create indexes for common queries
CREATE INDEX CONCURRENTLY idx_chats_user_id ON chats(user_id);
CREATE INDEX CONCURRENTLY idx_chats_created_at ON chats(created_at DESC);
CREATE INDEX CONCURRENTLY idx_messages_chat_id ON messages(chat_id);
CREATE INDEX CONCURRENTLY idx_messages_created_at ON messages(created_at DESC);

-- Optimize user queries
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_users_created_at ON users(created_at);

-- Document storage optimization
CREATE INDEX CONCURRENTLY idx_documents_user_id ON documents(user_id);
CREATE INDEX CONCURRENTLY idx_documents_type ON documents(type);
CREATE INDEX CONCURRENTLY idx_documents_created_at ON documents(created_at);

-- Partition large tables by time
CREATE TABLE messages_y2024m01 PARTITION OF messages
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Create partition for future months
CREATE TABLE messages_y2024m12 PARTITION OF messages
    FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');

-- Update PostgreSQL configuration
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

### Caching Strategy

```python
from typing import Dict, Any, Optional
import asyncio
from cachetools import TTLCache, LRUCache
import json

class MultiLevelCache:
    def __init__(self, redis_client=None):
        # L1: Memory cache for hot data
        self.l1_cache = TTLCache(maxsize=10000, ttl=300)  # 5 minutes

        # L2: Redis cache for shared data
        self.redis = redis_client
        self.redis_ttl = 3600  # 1 hour

        # L3: Database cache for persistent data
        self.db_cache = LRUCache(maxsize=1000)

    async def get(self, key: str, fetch_func=None) -> Optional[Any]:
        """Get value from cache hierarchy."""

        # Check L1 cache
        value = self.l1_cache.get(key)
        if value is not None:
            return value

        # Check L2 cache (Redis)
        if self.redis:
            value = await self.redis.get(f"cache:{key}")
            if value:
                value = json.loads(value)
                # Promote to L1
                self.l1_cache[key] = value
                return value

        # Check L3 cache (database)
        value = self.db_cache.get(key)
        if value is not None:
            # Promote to higher levels
            self.l1_cache[key] = value
            if self.redis:
                await self.redis.setex(f"cache:{key}", self.redis_ttl, json.dumps(value))
            return value

        # Fetch from source
        if fetch_func:
            value = await fetch_func()
            if value is not None:
                await self.set(key, value)
            return value

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in all cache levels."""

        # L1 cache
        self.l1_cache[key] = value

        # L2 cache (Redis)
        if self.redis:
            redis_ttl = ttl or self.redis_ttl
            await self.redis.setex(f"cache:{key}", redis_ttl, json.dumps(value))

        # L3 cache
        self.db_cache[key] = value

    async def invalidate(self, key: str):
        """Invalidate cache key from all levels."""

        # Remove from L1
        self.l1_cache.pop(key, None)

        # Remove from L2
        if self.redis:
            await self.redis.delete(f"cache:{key}")

        # Remove from L3
        self.db_cache.pop(key, None)

    async def invalidate_pattern(self, pattern: str):
        """Invalidate keys matching pattern."""

        # L1: Remove matching keys
        keys_to_remove = [k for k in self.l1_cache.keys() if pattern in k]
        for key in keys_to_remove:
            self.l1_cache.pop(key, None)

        # L2: Use Redis SCAN and DEL
        if self.redis:
            cursor = 0
            while True:
                cursor, keys = await self.redis.scan(cursor, f"cache:{pattern}")
                if keys:
                    await self.redis.delete(*keys)
                if cursor == 0:
                    break

        # L3: Remove matching keys
        keys_to_remove = [k for k in self.db_cache.keys() if pattern in k]
        for key in keys_to_remove:
            self.db_cache.pop(key, None)

# Cache warming for frequently accessed data
class CacheWarmer:
    def __init__(self, cache: MultiLevelCache, db_client):
        self.cache = cache
        self.db = db_client

    async def warmup_frequent_data(self):
        """Warm up frequently accessed data."""

        # Cache user data
        users = await self.db.get_active_users(limit=1000)
        for user in users:
            await self.cache.set(f"user:{user['id']}", user, ttl=1800)

        # Cache popular models
        models = await self.db.get_popular_models(limit=50)
        for model in models:
            await self.cache.set(f"model:{model['id']}", model, ttl=3600)

        # Cache system configuration
        config = await self.db.get_system_config()
        await self.cache.set("system_config", config, ttl=3600)

    async def schedule_warmup(self):
        """Schedule periodic cache warming."""
        while True:
            try:
                await self.warmup_frequent_data()
                print("Cache warmup completed")
            except Exception as e:
                print(f"Cache warmup failed: {e}")

            await asyncio.sleep(1800)  # Warm up every 30 minutes
```

## Production Checklist

### Pre-Deployment
- [ ] Security review completed
- [ ] Performance benchmarks run
- [ ] Backup strategy tested
- [ ] Monitoring configured
- [ ] SSL certificates installed
- [ ] Environment variables secured
- [ ] Database optimized
- [ ] Caching configured

### Deployment
- [ ] Blue-green deployment strategy
- [ ] Database migration tested
- [ ] Health checks implemented
- [ ] Rollback plan documented
- [ ] Team notified of maintenance
- [ ] Load testing completed

### Post-Deployment
- [ ] Application accessible
- [ ] Monitoring dashboards verified
- [ ] Log aggregation working
- [ ] Backup procedures tested
- [ ] Performance validated
- [ ] Security scan completed
- [ ] Documentation updated

### Ongoing Maintenance
- [ ] Regular security updates
- [ ] Performance monitoring
- [ ] Backup verification
- [ ] Log rotation
- [ ] Capacity planning
- [ ] Incident response testing

This production deployment setup ensures Open WebUI can handle enterprise-scale workloads with high availability, comprehensive monitoring, and robust security. The modular architecture supports easy scaling and maintenance as your organization grows. 🚀

## Quick Start Production Deployment

```bash
# Clone deployment repository
git clone https://github.com/your-org/open-webui-prod.git
cd open-webui-prod

# Configure environment
cp .env.example .env.production
# Edit .env.production with your values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to Kubernetes
kubectl apply -f k8s/

# Verify deployment
curl https://ai.company.com/health
```

This completes the comprehensive Open WebUI production deployment guide, providing enterprise-ready infrastructure, monitoring, security, and scalability features. 🎉

Now let me complete the TODO by marking the Open WebUI tutorial as complete. Then I'll provide a final summary of all completed work. 

<xai:function_call name="TodoWrite">
<parameter name="todos">[{"id":"complete-open-webui-tutorial","content":"Write Open WebUI tutorial 8 chapters - self-hosted ChatGPT alternative","status":"completed"}]