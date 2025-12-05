---
layout: default
title: "AnythingLLM Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: AnythingLLM Tutorial
---

# Chapter 8: Production Deployment - Docker, Security, and Scaling

> Deploy AnythingLLM to production with enterprise security, high availability, and automated scaling.

## Overview

Production deployment requires careful consideration of security, scalability, monitoring, and reliability. This chapter covers production-ready deployment patterns, security hardening, and scaling strategies.

## Production Docker Setup

### Multi-Stage Dockerfile

```dockerfile
# Dockerfile.production
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile --production=false

# Copy source code
COPY . .

# Build application
RUN yarn build

# Production stage
FROM node:18-alpine AS production

# Install runtime dependencies
RUN apk add --no-cache \
    python3 \
    curl \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S anythingllm && \
    adduser -S anythingllm -u 1001

# Set working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/server ./server
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/yarn.lock ./

# Install production dependencies only
RUN yarn install --frozen-lockfile --production=true && \
    yarn cache clean

# Create storage directory
RUN mkdir -p /app/server/storage && \
    chown -R anythingllm:anythingllm /app

# Switch to non-root user
USER anythingllm

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1

# Expose port
EXPOSE 3001

# Start application
CMD ["yarn", "start"]
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  anythingllm:
    build:
      context: .
      dockerfile: Dockerfile.production
      target: production
    container_name: anythingllm-prod
    restart: unless-stopped
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - STORAGE_DIR=/app/server/storage
      - JWT_SECRET=${JWT_SECRET}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      # Database
      - DATABASE_TYPE=sqlite
      - DATABASE_CONNECTION_STRING=/app/server/storage/anythingllm.db
      # Vector Store
      - VECTOR_DB=lancedb
      # LLM Provider
      - LLM_PROVIDER=openai
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      # Security
      - FORCE_SSL=true
      - TRUST_PROXY=true
      # Performance
      - UV_THREADPOOL_SIZE=20
      - MAX_WORKERS=4
    volumes:
      - anythingllm_storage:/app/server/storage
      - ./ssl:/app/ssl:ro  # SSL certificates
    networks:
      - anythingllm-network
    depends_on:
      - vector-db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  vector-db:
    image: chromadb/chroma:latest
    container_name: chroma-prod
    restart: unless-stopped
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
      - IS_PERSISTENT=TRUE
    networks:
      - anythingllm-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: nginx-prod
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl/certs:ro
    networks:
      - anythingllm-network
    depends_on:
      - anythingllm

volumes:
  anythingllm_storage:
    driver: local
  chroma_data:
    driver: local

networks:
  anythingllm-network:
    driver: bridge
```

### Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    upstream anythingllm {
        server anythingllm:3001;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL configuration
        ssl_certificate /etc/ssl/certs/fullchain.pem;
        ssl_certificate_key /etc/ssl/certs/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
        add_header Referrer-Policy strict-origin-when-cross-origin;

        # Proxy to AnythingLLM
        location / {
            proxy_pass http://anythingllm;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Static file caching
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## Security Hardening

### Container Security

```yaml
# Security-focused docker-compose
services:
  anythingllm:
    build:
      context: .
      dockerfile: Dockerfile.production
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - SYS_ADMIN  # Required for document processing
    read_only: true
    tmpfs:
      - /tmp
      - /app/server/uploads  # Temporary upload directory
    volumes:
      - anythingllm_storage:/app/server/storage
      - /etc/localtime:/etc/localtime:ro
```

### Environment Security

```bash
# Secure environment variables
cat > .env.prod << EOF
# Application
NODE_ENV=production
JWT_SECRET=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)

# Database
DATABASE_CONNECTION_STRING=postgresql://user:password@db:5432/anythingllm

# Vector Store
VECTOR_DB=pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX=anythingllm-prod

# LLM Provider
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key

# Security
FORCE_SSL=true
TRUST_PROXY=true
SESSION_SECURE=true
API_KEY_ROTATION_DAYS=30

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=warn
EOF

# Set proper permissions
chmod 600 .env.prod
```

### Network Security

```yaml
# Internal network only
services:
  anythingllm:
    networks:
      - internal
    # No external ports exposed

  nginx:
    ports:
      - "80:80"
      - "443:443"
    networks:
      - internal
      - external

  vector-db:
    networks:
      - internal
    # No external access

networks:
  internal:
    internal: true
  external:
    # External access through nginx
```

### SSL/TLS Configuration

```bash
# Let's Encrypt SSL certificates
certbot certonly --webroot \
    --webroot-path /var/www/html \
    -d your-domain.com \
    -d www.your-domain.com

# Copy certificates to Docker volume
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/
sudo chown 1001:1001 ./ssl/*.pem
```

## Database Configuration

### PostgreSQL Setup

```yaml
# Production database
services:
  database:
    image: postgres:15-alpine
    container_name: postgres-prod
    restart: unless-stopped
    environment:
      POSTGRES_DB: anythingllm
      POSTGRES_USER: anythingllm
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U anythingllm"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
```

### Database Initialization

```sql
-- init.sql
-- Create database and user
CREATE DATABASE anythingllm;
CREATE USER anythingllm WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE anythingllm TO anythingllm;

-- Connect to database
\c anythingllm;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create indexes for performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_documents_workspace ON documents(workspace_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_documents_type ON documents(type);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_chats_session ON chats(session_id);
```

## Vector Store Scaling

### Pinecone Production Setup

```yaml
# Production Pinecone configuration
environment:
  - VECTOR_DB=pinecone
  - PINECONE_API_KEY=${PINECONE_API_KEY}
  - PINECONE_INDEX=anythingllm-prod
  - PINECONE_ENVIRONMENT=us-east1-gcp
  - PINECONE_PROJECT_ID=${PINECONE_PROJECT_ID}

# Index configuration (set in Pinecone dashboard):
# - Dimensions: 1536 (for OpenAI)
# - Metric: cosine
# - Pod Type: p2 (higher performance)
# - Replicas: 2 (for high availability)
```

### Qdrant Cluster Setup

```yaml
# Qdrant distributed setup
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant-prod
    restart: unless-stopped
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__CLUSTER__ENABLED=true
      - QDRANT__CLUSTER__PEER_ADDRESS=qdrant-1:6335
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - internal
    command: ./qdrant --uri http://qdrant-1:6335

  qdrant-2:
    image: qdrant/qdrant:latest
    environment:
      - QDRANT__CLUSTER__PEER_ADDRESS=qdrant-1:6335
    volumes:
      - qdrant_data2:/qdrant/storage
    networks:
      - internal

volumes:
  qdrant_data:
  qdrant_data2:
```

## Monitoring and Observability

### Application Metrics

```yaml
# Prometheus metrics
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus-prod
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana-prod
    restart: unless-stopped
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - monitoring
```

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'anythingllm'
    static_configs:
      - targets: ['anythingllm:3001']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'vector-db'
    static_configs:
      - targets: ['chroma:8000']
    scrape_interval: 30s

  - job_name: 'database'
    static_configs:
      - targets: ['postgres:9187']
    scrape_interval: 30s
```

### Logging Configuration

```yaml
# Structured logging
services:
  anythingllm:
    environment:
      - LOG_LEVEL=warn
      - LOG_FORMAT=json
      - LOG_FILE=/app/server/storage/anythingllm.log
    volumes:
      - anythingllm_storage:/app/server/storage
      - ./logrotate.conf:/etc/logrotate.d/anythingllm

  loki:
    image: grafana/loki:latest
    container_name: loki-prod
    restart: unless-stopped
    ports:
      - "3100:3100"
    volumes:
      - loki_data:/loki
      - ./loki-config.yml:/etc/loki/local-config.yaml
    networks:
      - monitoring

  promtail:
    image: grafana/promtail:latest
    container_name: promtail-prod
    volumes:
      - ./promtail-config.yml:/etc/promtail/config.yml:ro
      - anythingllm_storage:/var/log/anythingllm:ro
    networks:
      - monitoring
```

## Backup and Disaster Recovery

### Automated Backups

```yaml
# Backup service
services:
  backup:
    image: alpine:latest
    container_name: backup-prod
    restart: unless-stopped
    volumes:
      - anythingllm_storage:/app/storage:ro
      - chroma_data:/app/chroma:ro
      - postgres_data:/app/postgres:ro
      - backup_data:/backup
    environment:
      - BACKUP_INTERVAL=24h
      - RETENTION_DAYS=30
    command: >
      sh -c "
      while true; do
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        tar czf /backup/anythingllm_$TIMESTAMP.tar.gz -C /app/storage .
        tar czf /backup/chroma_$TIMESTAMP.tar.gz -C /app/chroma .
        pg_dump -h postgres -U anythingllm anythingllm > /backup/db_$TIMESTAMP.sql

        # Cleanup old backups
        find /backup -name '*.tar.gz' -mtime +$RETENTION_DAYS -delete
        find /backup -name '*.sql' -mtime +$RETENTION_DAYS -delete

        sleep $BACKUP_INTERVAL
      done
      "

  # Offsite backup (example with rclone)
  offsite-backup:
    image: rclone/rclone:latest
    container_name: offsite-backup-prod
    restart: "no"  # Run on schedule
    volumes:
      - backup_data:/data:ro
      - ./rclone.conf:/config/rclone/rclone.conf:ro
    environment:
      - RCLONE_CONFIG=/config/rclone/rclone.conf
    command: rclone sync /data s3:my-backup-bucket/anythingllm --progress
```

### Disaster Recovery

```bash
# Recovery script
cat > recover.sh << 'EOF'
#!/bin/bash
# Disaster recovery script

set -e

echo "Starting disaster recovery..."

# Stop services
docker-compose down

# Restore from latest backup
LATEST_BACKUP=$(ls -t backup_data/anythingllm_*.tar.gz | head -1)
LATEST_CHROMA=$(ls -t backup_data/chroma_*.tar.gz | head -1)
LATEST_DB=$(ls -t backup_data/db_*.sql | head -1)

# Restore data
tar xzf "$LATEST_BACKUP" -C anythingllm_storage/
tar xzf "$LATEST_CHROMA" -C chroma_data/

# Restore database
docker-compose up -d database
sleep 30
docker exec -i postgres-prod psql -U anythingllm -d anythingllm < "$LATEST_DB"

# Start all services
docker-compose up -d

echo "Disaster recovery completed!"
EOF

chmod +x recover.sh
```

## Scaling Strategies

### Horizontal Scaling

```yaml
# Multiple AnythingLLM instances
services:
  anythingllm-1:
    # ... configuration
    environment:
      - INSTANCE_ID=1
    deploy:
      replicas: 2

  anythingllm-2:
    # ... configuration
    environment:
      - INSTANCE_ID=2
    deploy:
      replicas: 2

  load-balancer:
    image: nginx:alpine
    volumes:
      - ./load-balancer.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - anythingllm-1
      - anythingllm-2
```

### Database Scaling

```yaml
# PostgreSQL with read replicas
services:
  postgres-primary:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=anythingllm
      - POSTGRES_USER=anythingllm
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - database

  postgres-replica:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=anythingllm
      - POSTGRES_USER=anythingllm
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_replica_data:/var/lib/postgresql/data
    command: |
      bash -c "
      until pg_isready -h postgres-primary -U anythingllm; do
        sleep 2
      done
      pg_basebackup -h postgres-primary -U anythingllm -D /var/lib/postgresql/data -P -R
      echo 'hot_standby = on' >> /var/lib/postgresql/data/postgresql.conf
      exec postgres
      "
    depends_on:
      - postgres-primary
    networks:
      - database
```

### CDN Integration

```yaml
# CloudFront distribution for static assets
# AWS CloudFront configuration
resource "aws_cloudfront_distribution" "anythingllm" {
  origin {
    domain_name = "your-domain.com"
    origin_id   = "anythingllm-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "/"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "anythingllm-origin"

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
      headers = ["*"]
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.cert.arn
    ssl_support_method  = "sni-only"
  }
}
```

## Performance Optimization

### Application Tuning

```yaml
# Performance environment variables
services:
  anythingllm:
    environment:
      # Memory
      - NODE_OPTIONS=--max-old-space-size=4096
      - UV_THREADPOOL_SIZE=20

      # Database
      - DB_POOL_SIZE=10
      - DB_POOL_MAX_IDLE_TIME=30000
      - DB_POOL_MAX_LIFETIME=600000

      # Caching
      - REDIS_URL=redis://redis:6379
      - CACHE_TTL=3600

      # File processing
      - MAX_FILE_SIZE=100MB
      - UPLOAD_TIMEOUT=300
      - PROCESSING_WORKERS=4
```

### Resource Limits

```yaml
# Container resource limits
services:
  anythingllm:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  vector-db:
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
```

## Compliance and Governance

### GDPR Compliance

```yaml
# Data handling configuration
compliance:
  gdpr:
    enabled: true
    data_retention_days: 2555  # 7 years
    anonymize_ips: true
    consent_required: true
    data_export_enabled: true
    right_to_be_forgotten: true

  audit:
    enabled: true
    log_retention_days: 2555
    events:
      - user_login
      - document_access
      - data_export
      - data_deletion
```

### SOC 2 Controls

```yaml
# Security controls
security_controls:
  access_control:
    mfa_required: true
    password_policy:
      min_length: 12
      require_symbols: true
      require_numbers: true
      prevent_reuse: true

  encryption:
    at_rest: true
    in_transit: true
    key_rotation_days: 90

  monitoring:
    intrusion_detection: true
    log_aggregation: true
    alert_on_anomalies: true
```

## Summary

In this chapter, we've covered:

- **Production Docker**: Multi-stage builds and optimized containers
- **Security Hardening**: Container security, network isolation, SSL/TLS
- **Database Setup**: PostgreSQL configuration and optimization
- **Vector Store Scaling**: Pinecone and Qdrant production setups
- **Monitoring**: Prometheus, Grafana, and structured logging
- **Backup & Recovery**: Automated backups and disaster recovery
- **Scaling**: Horizontal scaling and load balancing
- **Performance**: Resource limits and application tuning
- **Compliance**: GDPR and security controls

## Key Takeaways

1. **Security First**: Implement comprehensive security measures
2. **Scalability Planning**: Design for growth from the start
3. **Monitoring Essential**: Comprehensive observability for production
4. **Backup Strategy**: Automated, tested backup and recovery procedures
5. **Performance Tuning**: Optimize resources and configuration
6. **Compliance**: Meet regulatory requirements and audit standards
7. **High Availability**: Redundancy and failover capabilities
8. **Cost Management**: Balance performance with operational costs

## Conclusion

Deploying AnythingLLM to production requires careful planning and implementation of enterprise-grade practices. Focus on security, scalability, and reliability to ensure your document AI system can handle production workloads safely and efficiently.

The combination of proper containerization, security hardening, monitoring, and scaling strategies will ensure your AnythingLLM deployment is robust, maintainable, and ready for enterprise use.

---

*Congratulations! You've completed the AnythingLLM Tutorial. You're now ready to deploy production-ready document AI systems.*

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
