---
layout: default
title: "Chapter 8: Production Deployment"
parent: "PhotoPrism Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **PhotoPrism Tutorial: AI-Powered Photos App**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This final chapter covers deploying PhotoPrism in production environments with scaling, security, monitoring, and performance optimization.

## 🚀 Production Architecture

### High Availability Setup

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  photoprism-1:
    image: photoprism/photoprism:latest
    environment:
      PHOTOPRISM_DATABASE_DRIVER: postgresql
      PHOTOPRISM_DATABASE_DSN: "host=postgres user=photoprism password=${DB_PASSWORD} dbname=photoprism sslmode=disable"
      PHOTOPRISM_SITE_URL: https://photos.example.com
    volumes:
      - photos_data:/photoprism/photos
      - storage_data:/photoprism/storage
    depends_on:
      - postgres
      - redis
    networks:
      - photoprism_network
    deploy:
      replicas: 2

  photoprism-2:
    image: photoprism/photoprism:latest
    environment:
      PHOTOPRISM_DATABASE_DRIVER: postgresql
      PHOTOPRISM_DATABASE_DSN: "host=postgres user=photoprism password=${DB_PASSWORD} dbname=photoprism sslmode=disable"
    volumes:
      - photos_data:/photoprism/photos
      - storage_data:/photoprism/storage
    depends_on:
      - postgres
      - redis
    networks:
      - photoprism_network
    deploy:
      replicas: 2

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: photoprism
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: photoprism
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - photoprism_network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - photoprism_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - photoprism-1
      - photoprism-2
    networks:
      - photoprism_network

networks:
  photoprism_network:
    driver: overlay

volumes:
  photos_data:
    driver: local
  storage_data:
    driver: local
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

## 🔒 Security Hardening

### SSL/TLS Configuration

```nginx
# nginx.conf for PhotoPrism
upstream photoprism_backend {
    server photoprism-1:2342;
    server photoprism-2:2342;
}

server {
    listen 80;
    server_name photos.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name photos.example.com;

    ssl_certificate /etc/ssl/certs/photos.example.com.crt;
    ssl_certificate_key /etc/ssl/certs/photos.example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        proxy_pass http://photoprism_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### Database Security

```sql
-- Production database security
CREATE USER photoprism_prod WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE photoprism_prod TO photoprism_prod;
GRANT USAGE ON SCHEMA public TO photoprism_prod;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO photoprism_prod;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO photoprism_prod;

-- Enable SSL connections
ALTER SYSTEM SET ssl = on;
```

### Environment Security

```bash
# Secure environment variables
PHOTOPRISM_ADMIN_PASSWORD="$(openssl rand -base64 32)"
PHOTOPRISM_DATABASE_PASSWORD="$(openssl rand -base64 32)"
PHOTOPRISM_SITE_URL="https://photos.example.com"
PHOTOPRISM_DISABLE_TLS=false
PHOTOPRISM_HTTP_HOST="127.0.0.1"
PHOTOPRISM_HTTP_PORT=2342

# Disable debug mode
PHOTOPRISM_DEBUG=false
PHOTOPRISM_TRACE=false
```

## 📊 Monitoring & Observability

### Application Monitoring

```typescript
// Production monitoring setup
const monitoring = {
  prometheus: {
    metrics: {
      http_requests_total: 'Total HTTP requests',
      http_request_duration_seconds: 'Request duration',
      photoprism_photos_total: 'Total photos',
      photoprism_storage_used_bytes: 'Storage used'
    }
  },

  grafana: {
    dashboards: [
      'PhotoPrism Overview',
      'Performance Metrics',
      'Storage Usage',
      'AI Processing'
    ]
  },

  alerting: {
    rules: [
      {
        name: 'High CPU Usage',
        condition: 'cpu_usage > 80',
        duration: '5m',
        severity: 'warning'
      },
      {
        name: 'Low Disk Space',
        condition: 'disk_free < 10GB',
        duration: '1m',
        severity: 'critical'
      }
    ]
  }
}
```

### Log Aggregation

```typescript
// Centralized logging
const logging = {
  elk: {
    elasticsearch: {
      index: 'photoprism-%{+YYYY.MM.dd}',
      mapping: {
        timestamp: '@timestamp',
        level: 'level',
        message: 'message',
        service: 'photoprism'
      }
    }
  },

  logLevels: {
    production: 'warn',
    staging: 'info',
    development: 'debug'
  },

  retention: {
    days: 30,
    compress: true
  }
}
```

## 🚀 Performance Optimization

### Database Optimization

```sql
-- Production database optimization
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- PhotoPrism specific optimizations
CREATE INDEX CONCURRENTLY idx_photos_taken_at ON photos (taken_at);
CREATE INDEX CONCURRENTLY idx_photos_location ON photos USING GIST (location);
CREATE INDEX CONCURRENTLY idx_photos_labels ON photos USING GIN (labels);
```

### Caching Strategy

```typescript
// Multi-level caching
const cachingStrategy = {
  browser: {
    staticAssets: '1 year',
    thumbnails: '30 days',
    apiResponses: '5 minutes'
  },

  cdn: {
    images: '1 year',
    thumbnails: '30 days',
    withQueryString: true
  },

  application: {
    metadata: '1 hour',
    searchResults: '15 minutes',
    aiResults: '24 hours'
  },

  database: {
    queryCache: '10 minutes',
    tableCache: '1 hour'
  }
}
```

### Resource Optimization

```bash
# Production resource allocation
PHOTOPRISM_WORKERS=8
PHOTOPRISM_INDEX_WORKERS=4
PHOTOPRISM_THUMB_WORKERS=6
PHOTOPRISM_FACE_WORKERS=2
PHOTOPRISM_UPLOAD_NSFW=false
PHOTOPRISM_DETECT_NSFW=false
```

## 📈 Scaling Strategies

### Horizontal Scaling

```yaml
# Auto-scaling configuration
services:
  photoprism:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

### Load Balancing

```nginx
# Advanced load balancing
upstream photoprism_backend {
    least_conn;
    server photoprism-1:2342 weight=1 max_fails=3 fail_timeout=30s;
    server photoprism-2:2342 weight=1 max_fails=3 fail_timeout=30s;
    server photoprism-3:2342 weight=1 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name photos.example.com;

    location / {
        proxy_pass http://photoprism_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Health check
        health_check interval=10s;
    }
}
```

## 💾 Storage Optimization

### File System Choice

```bash
# Production storage setup
# Use XFS for large files
mkfs.xfs /dev/sdb
mount /dev/sdb /photoprism/photos

# Add to fstab
echo "/dev/sdb /photoprism/photos xfs defaults 0 0" >> /etc/fstab

# Optimize for large files
xfs_io -c "extsize 1m" /photoprism/photos
```

### Storage Monitoring

```typescript
// Storage monitoring and alerts
const storageMonitoring = {
  thresholds: {
    warning: 0.8,  // 80% used
    critical: 0.9  // 90% used
  },

  async checkStorage() {
    const stats = await fs.promises.statvfs('/photoprism/photos')
    const usedPercent = 1 - (stats.f_bavail / stats.f_blocks)

    return {
      total: stats.f_blocks * stats.f_frsize,
      used: (stats.f_blocks - stats.f_bavail) * stats.f_frsize,
      available: stats.f_bavail * stats.f_frsize,
      usedPercent
    }
  },

  async monitorStorage() {
    const storage = await this.checkStorage()

    if (storage.usedPercent > this.thresholds.critical) {
      await alertSystem.alert('CRITICAL', 'Storage usage above 90%')
    } else if (storage.usedPercent > this.thresholds.warning) {
      await alertSystem.alert('WARNING', 'Storage usage above 80%')
    }
  }
}
```

## 🔧 Maintenance Procedures

### Automated Maintenance

```bash
#!/bin/bash
# production_maintenance.sh

# Update PhotoPrism
docker-compose pull
docker-compose up -d --no-deps photoprism

# Database maintenance
docker exec postgres vacuumdb -U photoprism --analyze --verbose photoprism

# Clean old thumbnails
docker exec photoprism photoprism thumbs clean --dry-run
docker exec photoprism photoprism thumbs clean

# Update AI models
docker exec photoprism photoprism convert

# Health check
curl -f https://photos.example.com/api/v1/health

# Log rotation
logrotate /etc/logrotate.d/photoprism
```

### Backup Strategy

```bash
#!/bin/bash
# production_backup.sh

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/photoprism"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup with compression
docker exec postgres pg_dump -U photoprism photoprism | gzip > $BACKUP_DIR/db_$BACKUP_DATE.sql.gz

# File backup
tar -czf $BACKUP_DIR/files_$BACKUP_DATE.tar.gz -C /photoprism/photos .

# Upload to cloud
aws s3 cp $BACKUP_DIR/db_$BACKUP_DATE.sql.gz s3://photoprism-backups/
aws s3 cp $BACKUP_DIR/files_$BACKUP_DATE.tar.gz s3://photoprism-backups/

# Clean local backups older than 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

# Send notification
curl -X POST -H 'Content-Type: application/json' \
  https://api.example.com/notifications \
  -d "{\"message\": \"PhotoPrism backup completed: $BACKUP_DATE\"}"
```

## 📊 Performance Monitoring

### Key Metrics

```typescript
// Production metrics to monitor
const productionMetrics = {
  responseTime: {
    p50: '< 500ms',
    p95: '< 2s',
    p99: '< 5s'
  },

  throughput: {
    requestsPerSecond: '> 100',
    photosProcessedPerHour: '> 1000'
  },

  resourceUsage: {
    cpu: '< 70%',
    memory: '< 80%',
    disk: '< 85%'
  },

  errors: {
    httpErrors: '< 1%',
    applicationErrors: '< 0.1%'
  }
}
```

### APM Integration

```typescript
// Application Performance Monitoring
const apmConfig = {
  newRelic: {
    appName: 'PhotoPrism Production',
    licenseKey: process.env.NEW_RELIC_LICENSE_KEY,
    distributedTracing: true
  },

  datadog: {
    serviceName: 'photoprism',
    env: 'production',
    version: process.env.APP_VERSION
  },

  customMetrics: {
    photoUploadTime: 'histogram',
    searchResponseTime: 'histogram',
    aiProcessingTime: 'histogram',
    storageUsage: 'gauge'
  }
}
```

## 🚨 Incident Response

### Alert Configuration

```typescript
// Production alerting
const alertConfig = {
  channels: {
    slack: '#photoprism-alerts',
    email: 'team@example.com',
    sms: '+1234567890'
  },

  rules: [
    {
      name: 'Service Down',
      condition: 'up == 0',
      duration: '5m',
      severity: 'critical'
    },
    {
      name: 'High Error Rate',
      condition: 'error_rate > 0.05',
      duration: '10m',
      severity: 'warning'
    },
    {
      name: 'Storage Full',
      condition: 'disk_usage > 0.9',
      duration: '1m',
      severity: 'critical'
    }
  ]
}
```

### Runbook

```typescript
// Incident response runbook
const incidentRunbook = {
  'service-down': {
    steps: [
      'Check Docker container status',
      'Review application logs',
      'Check database connectivity',
      'Verify storage availability',
      'Restart services if needed',
      'Escalate to engineering if persistent'
    ],
    contacts: ['devops@company.com', '+1234567890']
  },

  'high-error-rate': {
    steps: [
      'Check error logs',
      'Review recent deployments',
      'Monitor resource usage',
      'Check third-party service status',
      'Implement rate limiting if needed'
    ]
  },

  'storage-full': {
    steps: [
      'Check current storage usage',
      'Identify large files for cleanup',
      'Implement log rotation',
      'Add additional storage if needed',
      'Update backup strategy'
    ]
  }
}
```

## 📝 Production Checklist

```bash
# Pre-deployment checklist
PRODUCTION_CHECKLIST="
☐ SSL/TLS certificates configured
☐ Database optimized for production
☐ Monitoring and alerting set up
☐ Backup strategy implemented
☐ Load balancer configured
☐ Security hardening applied
☐ Performance benchmarks completed
☐ Incident response plan documented
☐ Team trained on procedures
☐ Rollback plan ready
☐ Go-live date scheduled
"
```

## 📝 Chapter Summary

- ✅ Configured high availability architecture
- ✅ Implemented security hardening measures
- ✅ Set up comprehensive monitoring
- ✅ Optimized performance and scaling
- ✅ Configured automated maintenance
- ✅ Established backup and recovery
- ✅ Built incident response procedures

**Key Takeaways:**
- Production requires careful planning and monitoring
- Security should be implemented at all levels
- Performance optimization is ongoing
- Automation reduces manual errors
- Monitoring enables proactive issue resolution
- Documentation ensures smooth operations
- Regular maintenance prevents problems

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `photoprism`, `photos`, `example` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment` as an operating subsystem inside **PhotoPrism Tutorial: AI-Powered Photos App**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `storage`, `stats`, `proxy_set_header` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `photoprism`.
2. **Input normalization**: shape incoming data so `photos` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `example`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [github.com/photoprism/photoprism](https://github.com/photoprism/photoprism)
  Why it matters: authoritative reference on `github.com/photoprism/photoprism` (github.com).
- [github.com/photoprism/photoprism/discussions](https://github.com/photoprism/photoprism/discussions)
  Why it matters: authoritative reference on `github.com/photoprism/photoprism/discussions` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `photoprism` and `photos` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Backup & Migration](07-backup-migration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
