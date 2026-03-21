---
layout: default
title: "Appsmith Tutorial - Chapter 8: Production Operations"
nav_order: 8
has_children: false
parent: Appsmith Tutorial
---

# Chapter 8: Production Operations

This chapter covers running Appsmith in production — self-hosting strategies, scaling, backups, monitoring, upgrades, and operational best practices for maintaining a reliable internal tools platform.

> Self-host Appsmith at scale with Docker or Kubernetes, automate backups, monitor health, and manage upgrades.

## What Problem Does This Solve?

Running a low-code platform in production is fundamentally different from running it locally. You need high availability so your internal tools do not go down during business hours. You need backups so a disk failure does not erase months of application development. You need monitoring so you catch problems before users report them. And you need an upgrade strategy that does not require downtime.

## Production Architecture

```mermaid
flowchart TB
    subgraph LB["Load Balancer"]
        Nginx[Nginx / ALB / Traefik]
    end

    subgraph Appsmith["Appsmith Nodes"]
        Node1[Appsmith Instance 1]
        Node2[Appsmith Instance 2]
    end

    subgraph Data["Data Layer"]
        Mongo[(MongoDB Replica Set)]
        Redis[(Redis Cluster)]
        S3[(S3 / MinIO)]
    end

    subgraph Monitoring["Observability"]
        Prometheus[Prometheus]
        Grafana[Grafana]
        Alerts[Alertmanager]
        Logs[Loki / ELK]
    end

    Nginx --> Node1
    Nginx --> Node2
    Node1 & Node2 --> Mongo
    Node1 & Node2 --> Redis
    Node1 & Node2 --> S3
    Node1 & Node2 -->|metrics| Prometheus
    Node1 & Node2 -->|logs| Logs
    Prometheus --> Grafana
    Prometheus --> Alerts

    classDef lb fill:#e1f5fe,stroke:#01579b
    classDef app fill:#f3e5f5,stroke:#4a148c
    classDef data fill:#fff3e0,stroke:#ef6c00
    classDef monitor fill:#e8f5e8,stroke:#1b5e20

    class Nginx lb
    class Node1,Node2 app
    class Mongo,Redis,S3 data
    class Prometheus,Grafana,Alerts,Logs monitor
```

## Docker Production Deployment

### docker-compose.yml for Production

```yaml
# docker-compose.production.yml
version: "3.8"

services:
  appsmith:
    image: appsmith/appsmith-ce:latest
    container_name: appsmith
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./stacks:/appsmith-stacks
      - ./certs:/appsmith-stacks/ssl
    environment:
      # External MongoDB (recommended for production)
      APPSMITH_MONGODB_URI: "mongodb://appsmith:password@mongo1:27017,mongo2:27017,mongo3:27017/appsmith?replicaSet=rs0&authSource=admin"

      # External Redis
      APPSMITH_REDIS_URL: "redis://redis:6379"

      # Encryption (generate once, store securely)
      APPSMITH_ENCRYPTION_PASSWORD: "${APPSMITH_ENCRYPTION_PASSWORD}"
      APPSMITH_ENCRYPTION_SALT: "${APPSMITH_ENCRYPTION_SALT}"

      # Email
      APPSMITH_MAIL_ENABLED: "true"
      APPSMITH_MAIL_HOST: "smtp.example.com"
      APPSMITH_MAIL_PORT: "587"
      APPSMITH_MAIL_USERNAME: "${SMTP_USERNAME}"
      APPSMITH_MAIL_PASSWORD: "${SMTP_PASSWORD}"
      APPSMITH_MAIL_FROM: "appsmith@example.com"

      # Custom domain
      APPSMITH_CUSTOM_DOMAIN: "tools.example.com"

      # Disable signup (invite-only)
      APPSMITH_SIGNUP_DISABLED: "true"

      # Telemetry
      APPSMITH_DISABLE_TELEMETRY: "true"
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 8G
        reservations:
          cpus: "2"
          memory: 4G
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "10"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
```

### SSL/TLS Configuration

```bash
# Option 1: Let's Encrypt (automatic)
# Set APPSMITH_CUSTOM_DOMAIN and Appsmith handles certificate generation

# Option 2: Custom certificates
# Mount certificates to the ssl volume
cp fullchain.pem ./certs/fullchain.pem
cp privkey.pem ./certs/privkey.pem
```

## Kubernetes Deployment

### Helm Values for Production

```yaml
# values-production.yaml
replicaCount: 2

image:
  repository: appsmith/appsmith-ce
  tag: latest
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: "2"
    memory: "4Gi"
  limits:
    cpu: "4"
    memory: "8Gi"

persistence:
  enabled: true
  storageClass: gp3
  size: 50Gi

mongodb:
  enabled: false  # Use external MongoDB
  externalUri: "mongodb+srv://appsmith:password@cluster0.example.net/appsmith?retryWrites=true"

redis:
  enabled: false  # Use external Redis
  externalUrl: "redis://redis.example.com:6379"

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "150m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
  hosts:
    - host: tools.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: appsmith-tls
      hosts:
        - tools.example.com

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

env:
  APPSMITH_ENCRYPTION_PASSWORD:
    valueFrom:
      secretKeyRef:
        name: appsmith-secrets
        key: encryption-password
  APPSMITH_ENCRYPTION_SALT:
    valueFrom:
      secretKeyRef:
        name: appsmith-secrets
        key: encryption-salt
  APPSMITH_SIGNUP_DISABLED: "true"
  APPSMITH_DISABLE_TELEMETRY: "true"

podDisruptionBudget:
  enabled: true
  minAvailable: 1

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
          labelSelector:
            matchLabels:
              app: appsmith
```

```bash
# Deploy with production values
helm install appsmith appsmith/appsmith \
  --namespace appsmith \
  --create-namespace \
  -f values-production.yaml

# Upgrade
helm upgrade appsmith appsmith/appsmith \
  --namespace appsmith \
  -f values-production.yaml
```

## Backup and Restore

### Automated Backups

```bash
#!/bin/bash
# backup-appsmith.sh — Run daily via cron

BACKUP_DIR="/backups/appsmith"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# 1. MongoDB backup
mongodump \
  --uri="mongodb://appsmith:password@mongo:27017/appsmith?authSource=admin" \
  --out="$BACKUP_DIR/mongo_$TIMESTAMP"

# Compress the backup
tar -czf "$BACKUP_DIR/mongo_$TIMESTAMP.tar.gz" \
  -C "$BACKUP_DIR" "mongo_$TIMESTAMP"
rm -rf "$BACKUP_DIR/mongo_$TIMESTAMP"

# 2. Backup Git repositories (stored in stacks)
tar -czf "$BACKUP_DIR/git_repos_$TIMESTAMP.tar.gz" \
  -C /appsmith-stacks git

# 3. Backup configuration
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
  -C /appsmith-stacks configuration

# 4. Upload to S3 (optional)
aws s3 sync "$BACKUP_DIR" s3://my-backups/appsmith/ \
  --exclude "*" \
  --include "*_$TIMESTAMP*"

# 5. Clean up old backups
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $TIMESTAMP"
```

### Restore from Backup

```bash
#!/bin/bash
# restore-appsmith.sh

BACKUP_DIR="/backups/appsmith"
TIMESTAMP=$1  # Pass as argument: ./restore-appsmith.sh 20260321_140000

if [ -z "$TIMESTAMP" ]; then
  echo "Usage: $0 <timestamp>"
  echo "Available backups:"
  ls -la "$BACKUP_DIR"/mongo_*.tar.gz
  exit 1
fi

# 1. Stop Appsmith
docker compose stop appsmith

# 2. Restore MongoDB
tar -xzf "$BACKUP_DIR/mongo_$TIMESTAMP.tar.gz" -C /tmp/
mongorestore \
  --uri="mongodb://appsmith:password@mongo:27017/?authSource=admin" \
  --drop \
  "/tmp/mongo_$TIMESTAMP/appsmith"
rm -rf "/tmp/mongo_$TIMESTAMP"

# 3. Restore Git repositories
tar -xzf "$BACKUP_DIR/git_repos_$TIMESTAMP.tar.gz" \
  -C /appsmith-stacks/

# 4. Restore configuration
tar -xzf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
  -C /appsmith-stacks/

# 5. Restart Appsmith
docker compose start appsmith

echo "Restore completed from backup: $TIMESTAMP"
```

## Monitoring

### Health Check Endpoint

```bash
# Appsmith exposes a health endpoint
curl http://localhost/api/v1/health

# Expected response
{
  "status": "UP",
  "components": {
    "mongo": { "status": "UP" },
    "redis": { "status": "UP" },
    "rts": { "status": "UP" }
  }
}
```

### Prometheus Metrics

Configure Prometheus to scrape Appsmith JVM and application metrics:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: "appsmith"
    metrics_path: "/actuator/prometheus"
    scrape_interval: 30s
    static_configs:
      - targets: ["appsmith:8080"]
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: "jvm_.*|http_server_.*|appsmith_.*"
        action: keep
```

### Key Metrics to Monitor

| Metric | Description | Alert Threshold |
|:-------|:------------|:----------------|
| `jvm_memory_used_bytes` | JVM heap usage | > 85% of max |
| `http_server_requests_seconds` | API response latency | p99 > 5s |
| `appsmith_query_execution_time` | Query execution duration | p95 > 10s |
| `mongodb_connections_current` | Active MongoDB connections | > 80% of pool |
| `appsmith_active_users` | Concurrent users | Trending analysis |
| `system_cpu_usage` | Container CPU usage | > 80% sustained |

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Appsmith Production",
    "panels": [
      {
        "title": "API Response Time (p99)",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(http_server_requests_seconds_bucket{job='appsmith'}[5m]))"
          }
        ]
      },
      {
        "title": "JVM Heap Usage",
        "type": "gauge",
        "targets": [
          {
            "expr": "jvm_memory_used_bytes{area='heap'} / jvm_memory_max_bytes{area='heap'} * 100"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "appsmith_active_users"
          }
        ]
      },
      {
        "title": "Query Execution Time",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(appsmith_query_execution_time_bucket[5m])"
          }
        ]
      }
    ]
  }
}
```

## Upgrade Strategy

### Rolling Upgrades (Zero Downtime)

```mermaid
sequenceDiagram
    participant LB as Load Balancer
    participant N1 as Node 1 (v1.10)
    participant N2 as Node 2 (v1.10)

    Note over LB,N2: Upgrade starts

    LB->>N1: Remove from pool
    Note over N1: Upgrade to v1.11
    N1->>N1: Pull new image
    N1->>N1: Run migrations
    N1->>N1: Health check passes
    LB->>N1: Add back to pool

    LB->>N2: Remove from pool
    Note over N2: Upgrade to v1.11
    N2->>N2: Pull new image
    N2->>N2: Health check passes
    LB->>N2: Add back to pool

    Note over LB,N2: Upgrade complete — zero downtime
```

### Docker Upgrade Process

```bash
#!/bin/bash
# upgrade-appsmith.sh

# 1. Pre-flight checks
echo "Current version:"
docker exec appsmith cat /opt/appsmith/info.json | jq '.version'

# 2. Backup before upgrade (always)
./backup-appsmith.sh

# 3. Pull new image
docker pull appsmith/appsmith-ce:latest

# 4. Rolling restart
docker compose up -d --no-deps appsmith

# 5. Wait for health check
echo "Waiting for Appsmith to become healthy..."
for i in $(seq 1 60); do
  if curl -sf http://localhost/api/v1/health > /dev/null 2>&1; then
    echo "Appsmith is healthy!"
    break
  fi
  sleep 5
done

# 6. Verify new version
echo "New version:"
docker exec appsmith cat /opt/appsmith/info.json | jq '.version'
```

### Kubernetes Upgrade

```bash
# Update Helm chart
helm repo update appsmith

# Upgrade with rolling deployment
helm upgrade appsmith appsmith/appsmith \
  --namespace appsmith \
  -f values-production.yaml \
  --set image.tag=v1.11.0

# Monitor rollout
kubectl rollout status deployment/appsmith -n appsmith

# Rollback if needed
kubectl rollout undo deployment/appsmith -n appsmith
```

## How It Works Under the Hood

### The Startup Sequence

When Appsmith starts, the container runs an entrypoint script that initializes all services in order:

```mermaid
flowchart TB
    A[Container Start] --> B[Read environment variables]
    B --> C[Initialize MongoDB]
    C --> D[Run database migrations]
    D --> E[Start Redis]
    E --> F[Start Spring Boot API Server]
    F --> G[Start RTS Node.js Server]
    G --> H[Start Nginx]
    H --> I[Health check passes]
    I --> J[Ready to serve traffic]

    classDef init fill:#e1f5fe,stroke:#01579b
    classDef service fill:#f3e5f5,stroke:#4a148c
    classDef ready fill:#e8f5e8,stroke:#1b5e20

    class A,B init
    class C,D,E,F,G,H service
    class I,J ready
```

### Database Migrations

Appsmith uses a migration framework that runs on startup to evolve the MongoDB schema:

```java
// Simplified migration pattern
// server/appsmith-server/src/main/java/com/appsmith/server/migrations/

@ChangeLog(order = "001")
public class DatabaseChangelog {

    @ChangeSet(order = "001", id = "add-default-workspace-permissions")
    public void addDefaultWorkspacePermissions(MongoTemplate mongoTemplate) {
        // Migration logic — runs once per database
        mongoTemplate.getCollection("workspace").updateMany(
            new Document("permissions", new Document("$exists", false)),
            new Document("$set", new Document("permissions", defaultPermissions))
        );
    }

    @ChangeSet(order = "002", id = "migrate-page-dsl-v2")
    public void migratePageDSLv2(MongoTemplate mongoTemplate) {
        // Migrate widget tree format
    }
}
```

## Performance Tuning

### JVM Configuration

```bash
# Tune JVM for production workloads
APPSMITH_JAVA_OPTS="-Xms2g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/appsmith-stacks/logs/"
```

### MongoDB Optimization

```javascript
// Ensure proper indexes exist
db.application.createIndex({ "workspaceId": 1, "name": 1 });
db.newPage.createIndex({ "applicationId": 1, "slug": 1 });
db.newAction.createIndex({ "applicationId": 1, "pageId": 1 });
db.actionCollection.createIndex({ "applicationId": 1, "pageId": 1 });
db.user.createIndex({ "email": 1 }, { unique: true });
```

### Nginx Tuning

```nginx
# Custom nginx overrides
# /appsmith-stacks/configuration/nginx/conf.d/custom.conf

client_max_body_size 150m;
proxy_read_timeout 300s;
proxy_connect_timeout 30s;

# Enable gzip for JSON responses
gzip on;
gzip_types application/json text/plain text/css application/javascript;
gzip_min_length 1000;

# Connection pooling
upstream appsmith_api {
    server 127.0.0.1:8080;
    keepalive 32;
}
```

## Key Takeaways

- Use external MongoDB (replica set) and Redis for production — do not rely on the embedded database.
- Automate backups of MongoDB, Git repositories, and configuration daily with retention policies.
- Monitor JVM metrics, API latency, and query execution time with Prometheus and Grafana.
- Use rolling upgrades (Kubernetes or Docker) to achieve zero-downtime updates.
- Tune JVM heap, MongoDB indexes, and Nginx timeouts for production workloads.

## Cross-References

- **Previous chapter:** [Chapter 7: Access Control & Governance](07-access-control-and-governance.md) covers RBAC and audit logging for security.
- **Getting started:** [Chapter 1: Getting Started](01-getting-started.md) covers initial Docker setup.
- **Data sources:** [Chapter 3: Data Sources & Queries](03-data-sources-and-queries.md) covers connection pooling configuration.
- **Git sync:** [Chapter 6: Git Sync & Deployment](06-git-sync-and-deployment.md) covers CI/CD pipelines for deployment automation.

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
