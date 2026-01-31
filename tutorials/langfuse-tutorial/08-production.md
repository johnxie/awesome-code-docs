---
layout: default
title: "Langfuse Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Langfuse Tutorial
---

# Chapter 8: Production Deployment

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
