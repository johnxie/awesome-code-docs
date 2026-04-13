---
layout: default
title: "Langfuse Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Langfuse Tutorial
---


# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **Langfuse Tutorial: LLM Observability, Evaluation, and Prompt Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Self-host Langfuse, secure your setup, and scale for high-traffic applications.

Previous: [Chapter 7: Integrations](07-integrations.md)

## Production Architecture

Here is a high-level view of a production Langfuse deployment:

```mermaid
flowchart TB
    subgraph Clients
        A[LLM App - Instance 1]
        B[LLM App - Instance 2]
        C[LLM App - Instance N]
    end

    subgraph Load Balancer
        D[NGINX / ALB]
    end

    subgraph Langfuse Cluster
        E[Langfuse Pod 1]
        F[Langfuse Pod 2]
        G[Langfuse Pod 3]
    end

    subgraph Data Layer
        H[(PostgreSQL Primary)]
        I[(PostgreSQL Replica)]
        J[(Redis Cluster)]
    end

    subgraph Observability
        K[Prometheus]
        L[Grafana]
        M[Log Aggregation]
    end

    subgraph Backup
        N[S3 / Object Storage]
    end

    A --> D
    B --> D
    C --> D
    D --> E
    D --> F
    D --> G
    E --> H
    F --> H
    G --> H
    H --> I
    E --> J
    F --> J
    G --> J
    E --> K
    F --> K
    G --> K
    K --> L
    H --> N
```

Multiple application instances send traces through a load balancer to a cluster of Langfuse pods. The data layer consists of a PostgreSQL primary with a read replica for analytics queries and a Redis cluster for caching and session management. Prometheus and Grafana handle monitoring, and automated backups go to object storage.

## Overview

Deploy Langfuse securely with proper scaling, backup, and monitoring. Options include Docker, Kubernetes, or cloud platforms.

## Self-Hosting with Docker

Production-ready Docker Compose:

```yaml
version: "3.9"
services:
  langfuse:
    image: ghcr.io/langfuse/langfuse:latest
    environment:
      - DATABASE_URL=postgresql://langfuse:password@db:5432/langfuse
      - NEXTAUTH_URL=https://langfuse.yourdomain.com
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - SALT=${SALT}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=langfuse
      - POSTGRES_USER=langfuse
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langfuse"]
      interval: 30s
      timeout: 10s

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

## Kubernetes Deployment

```yaml
# langfuse-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langfuse
spec:
  replicas: 3
  selector:
    matchLabels:
      app: langfuse
  template:
    metadata:
      labels:
        app: langfuse
    spec:
      containers:
      - name: langfuse
        image: ghcr.io/langfuse/langfuse:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: langfuse-secrets
              key: database-url
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: langfuse
spec:
  selector:
    app: langfuse
  ports:
    - port: 80
      targetPort: 3000
```

## Security Hardening

### Environment Variables

```bash
# .env.production
NEXTAUTH_SECRET=your-secure-random-string
SALT=another-secure-random-string
ENCRYPTION_KEY=32-char-encryption-key
DATABASE_URL=postgresql://user:password@host:5432/langfuse
REDIS_URL=redis://redis:6379
```

### Network Security

- Use HTTPS with TLS certificates
- Restrict database access to application pods only
- Enable Redis authentication
- Configure firewall rules

### API Security

```yaml
# nginx.conf
server {
    listen 443 ssl;
    server_name langfuse.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://langfuse:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Rate limiting
    limit_req zone=api burst=10 nodelay;
}
```

## Scaling Considerations

### Database Scaling

- Use connection pooling (PgBouncer)
- Implement read replicas for analytics
- Archive old traces to separate storage

### Redis Clustering

```yaml
# docker-compose.yml (clustered Redis)
services:
  redis:
    image: redis:7-alpine
    command: redis-server --cluster-enabled yes --cluster-config-file nodes.conf
    volumes:
      - redisdata:/data
```

### Horizontal Scaling

- Deploy multiple Langfuse instances behind a load balancer
- Use sticky sessions or external session storage
- Monitor instance health with readiness/liveness probes

## Backup and Recovery

### Database Backups

```yaml
# pg_backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h db -U langfuse langfuse > backup_$DATE.sql
# Upload to S3 or other storage
aws s3 cp backup_$DATE.sql s3://langfuse-backups/
```

### Automated Backups

```yaml
# kubernetes cronjob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: langfuse-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command: ["pg_dump", "-h", "db", "-U", "langfuse", "langfuse"]
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: langfuse-secrets
                  key: db-password
          restartPolicy: OnFailure
```

## Monitoring and Observability

### Application Metrics

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'langfuse'
    static_configs:
      - targets: ['langfuse:3000']
    metrics_path: '/api/metrics'
```

### Database Monitoring

- Monitor connection counts
- Track query performance
- Set up alerts for disk space

### Logging

```yaml
# Collect logs with ELK stack
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
data:
  fluent-bit.conf: |
    [INPUT]
        Name tail
        Path /var/log/containers/langfuse*.log
        Parser docker

    [OUTPUT]
        Name elasticsearch
        Host elasticsearch
        Port 9200
```

## High Availability

### Multi-AZ Deployment

- Deploy across multiple availability zones
- Use RDS Aurora with multi-AZ for database
- Configure load balancer health checks

### Disaster Recovery

- Regular backups with cross-region replication
- Documented recovery procedures
- Regular DR testing

## Performance Optimization

### Database Tuning

```sql
-- PostgreSQL optimizations
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
```

### Caching Strategy

- Cache frequent queries
- Use Redis for session storage
- Implement API response caching

### Resource Limits

Set appropriate resource limits based on usage patterns:

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

## Compliance and Governance

- Enable audit logging
- Implement data retention policies
- Regular security updates
- Access control and RBAC

## Troubleshooting Production Issues

### Common Issues

1. **High Latency**: Check database query performance, add indexes
2. **Memory Leaks**: Monitor heap usage, implement garbage collection tuning
3. **Rate Limiting**: Implement proper rate limiting and queue management
4. **Data Loss**: Ensure proper backup and replication setup

### Debug Commands

```bash
# Check database connections
docker exec langfuse-db psql -U langfuse -c "SELECT count(*) FROM pg_stat_activity;"

# View application logs
docker logs langfuse-app

# Redis monitoring
docker exec langfuse-redis redis-cli info
```

## Conclusion

Congratulations -- you have completed the Langfuse tutorial series! Over eight chapters, you have gone from setting up your first trace to deploying a production-grade observability platform for your LLM applications. Here is a quick recap of what you learned:

- **Chapter 1**: Getting started with Langfuse -- installation, configuration, and your first trace.
- **Chapter 2**: Tracing -- capturing the full lifecycle of LLM requests with spans and generations.
- **Chapter 3**: Prompt management -- versioning, deploying, and A/B testing prompts.
- **Chapter 4**: Evaluation -- using LLM judges and human feedback to measure quality.
- **Chapter 5**: Analytics and metrics -- tracking costs, latency, and ROI.
- **Chapter 6**: Datasets and testing -- building test suites and running regression tests.
- **Chapter 7**: Integrations -- connecting Langfuse with LangChain, OpenAI, and other frameworks.
- **Chapter 8**: Production deployment -- self-hosting, security, scaling, and monitoring.

With these tools and practices in place, you are well-equipped to build, monitor, and continuously improve LLM applications at any scale. The key is to start simple, measure everything, and iterate based on real data. Happy building!

## Depth Expansion Playbook

## Source Code Walkthrough

### `package.json`

The `package` module in [`package.json`](https://github.com/langfuse/langfuse/blob/HEAD/package.json) handles a key part of this chapter's functionality:

```json
{
  "name": "langfuse",
  "version": "3.163.0",
  "author": "engineering@langfuse.com",
  "license": "MIT",
  "private": true,
  "engines": {
    "node": "24"
  },
  "scripts": {
    "agents:check": "node scripts/agents/sync-agent-shims.mjs --check",
    "agents:sync": "node scripts/agents/sync-agent-shims.mjs",
    "postinstall": "node -e \"const fs = require('node:fs'); const cp = require('node:child_process'); if (!fs.existsSync('scripts/postinstall.sh')) { console.log('Skipping repo postinstall helper: scripts/postinstall.sh is not present in this install context.'); process.exit(0); } cp.execSync('bash scripts/postinstall.sh', { stdio: 'inherit' });\"",
    "preinstall": "npx only-allow pnpm",
    "infra:dev:up": "docker compose -f ./docker-compose.dev.yml up -d --wait",
    "infra:dev:down": "docker compose -f ./docker-compose.dev.yml down",
    "infra:dev:prune": "docker compose -f ./docker-compose.dev.yml down -v",
    "db:generate": "turbo run db:generate",
    "db:migrate": "turbo run db:migrate",
    "db:seed": "turbo run db:seed",
    "db:seed:examples": "turbo run db:seed:examples",
    "nuke": "bash ./scripts/nuke.sh",
    "dx": "pnpm i && pnpm run infra:dev:prune && pnpm run infra:dev:up --pull always && pnpm --filter=shared run db:reset:test && pnpm --filter=shared run db:reset && pnpm --filter=shared run ch:reset && pnpm --filter=shared run db:seed:examples && pnpm run dev",
    "dx-f": "pnpm i && pnpm run infra:dev:prune && pnpm run infra:dev:up --pull always && pnpm --filter=shared run db:reset:test && pnpm --filter=shared run db:reset -f && SKIP_CONFIRM=1 pnpm --filter=shared run ch:reset && pnpm --filter=shared run db:seed:examples && pnpm run dev",
    "dx:skip-infra": "pnpm i && pnpm --filter=shared run db:reset:test && pnpm --filter=shared run db:reset && pnpm --filter=shared run ch:reset && pnpm --filter=shared run db:seed:examples && pnpm run dev",
    "build": "turbo run build",
    "build:check": "turbo run build:check",
    "typecheck": "turbo run typecheck",
    "tc": "turbo run typecheck",
    "start": "turbo run start",
    "dev": "turbo run dev",
    "dev:worker": "turbo run dev --filter=worker",
    "dev:web": "turbo run dev --filter=web",
    "dev:web-webpack": "turbo run dev --filter=web -- --webpack",
    "lint": "turbo run lint",
```

This module is important because it defines how Langfuse Tutorial: LLM Observability, Evaluation, and Prompt Operations implements the patterns covered in this chapter.

### `docker-compose.dev-azure.yml`

The `docker-compose.dev-azure` module in [`docker-compose.dev-azure.yml`](https://github.com/langfuse/langfuse/blob/HEAD/docker-compose.dev-azure.yml) handles a key part of this chapter's functionality:

```yml
services:
  clickhouse:
    image: docker.io/clickhouse/clickhouse-server:24.3
    user: "101:101"
    environment:
      CLICKHOUSE_DB: default
      CLICKHOUSE_USER: ${CLICKHOUSE_USER:-clickhouse}
      CLICKHOUSE_PASSWORD: ${CLICKHOUSE_PASSWORD:-clickhouse}
    volumes:
      - langfuse_clickhouse_data:/var/lib/clickhouse
      - langfuse_clickhouse_logs:/var/log/clickhouse-server
    ports:
      - "8123:8123"
      - "9000:9000"
    healthcheck:
      test: wget --no-verbose --tries=1 --spider http://localhost:8123/ping || exit 1
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 1s
    depends_on:
      - postgres

  azurite:
    image: mcr.microsoft.com/azure-storage/azurite
    command: azurite-blob --blobHost 0.0.0.0
    ports:
      - "10000:10000"
    volumes:
      - langfuse_azurite_data:/data

  minio:
    image: cgr.dev/chainguard/minio
    container_name: ${MINIO_CONTAINER_NAME:-langfuse-minio}
    entrypoint: sh
```

This module is important because it defines how Langfuse Tutorial: LLM Observability, Evaluation, and Prompt Operations implements the patterns covered in this chapter.

### `docker-compose.yml`

The `docker-compose` module in [`docker-compose.yml`](https://github.com/langfuse/langfuse/blob/HEAD/docker-compose.yml) handles a key part of this chapter's functionality:

```yml
# Make sure to update the credential placeholders with your own secrets.
# We mark them with # CHANGEME in the file below.
# In addition, we recommend to restrict inbound traffic on the host to langfuse-web (port 3000) and minio (port 9090) only.
# All other components are bound to localhost (127.0.0.1) to only accept connections from the local machine.
# External connections from other machines will not be able to reach these services directly.
services:
  langfuse-worker:
    image: docker.io/langfuse/langfuse-worker:3
    restart: always
    depends_on: &langfuse-depends-on
      postgres:
        condition: service_healthy
      minio:
        condition: service_healthy
      redis:
        condition: service_healthy
      clickhouse:
        condition: service_healthy
    ports:
      - 127.0.0.1:3030:3030
    environment: &langfuse-worker-env
      NEXTAUTH_URL: ${NEXTAUTH_URL:-http://localhost:3000}
      DATABASE_URL: ${DATABASE_URL:-postgresql://postgres:postgres@postgres:5432/postgres} # CHANGEME
      SALT: ${SALT:-mysalt} # CHANGEME
      ENCRYPTION_KEY: ${ENCRYPTION_KEY:-0000000000000000000000000000000000000000000000000000000000000000} # CHANGEME: generate via `openssl rand -hex 32`
      TELEMETRY_ENABLED: ${TELEMETRY_ENABLED:-true}
      LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES: ${LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES:-false}
      CLICKHOUSE_MIGRATION_URL: ${CLICKHOUSE_MIGRATION_URL:-clickhouse://clickhouse:9000}
      CLICKHOUSE_URL: ${CLICKHOUSE_URL:-http://clickhouse:8123}
      CLICKHOUSE_USER: ${CLICKHOUSE_USER:-clickhouse}
      CLICKHOUSE_PASSWORD: ${CLICKHOUSE_PASSWORD:-clickhouse} # CHANGEME
      CLICKHOUSE_CLUSTER_ENABLED: ${CLICKHOUSE_CLUSTER_ENABLED:-false}
      LANGFUSE_USE_AZURE_BLOB: ${LANGFUSE_USE_AZURE_BLOB:-false}
      LANGFUSE_S3_EVENT_UPLOAD_BUCKET: ${LANGFUSE_S3_EVENT_UPLOAD_BUCKET:-langfuse}
      LANGFUSE_S3_EVENT_UPLOAD_REGION: ${LANGFUSE_S3_EVENT_UPLOAD_REGION:-auto}
```

This module is important because it defines how Langfuse Tutorial: LLM Observability, Evaluation, and Prompt Operations implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[package]
    B[docker-compose.dev-azure]
    C[docker-compose]
    A --> B
    B --> C
```
