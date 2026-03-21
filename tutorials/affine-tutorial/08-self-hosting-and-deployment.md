---
layout: default
title: "Chapter 8: Self-Hosting and Deployment"
nav_order: 8
parent: AFFiNE Tutorial
---

# Chapter 8: Self-Hosting and Deployment

Welcome to **Chapter 8: Self-Hosting and Deployment**. In this part of **AFFiNE Tutorial**, you will learn how to deploy AFFiNE to production environments using Docker, configure storage backends, set up authentication, and operate the platform reliably.

Self-hosting AFFiNE gives you full data ownership, the ability to use custom AI providers (see [Chapter 5: AI Copilot](05-ai-copilot.md)), and control over the collaboration infrastructure (see [Chapter 4: Collaborative Editing](04-collaborative-editing.md)). This chapter covers everything from a minimal Docker setup to a production-grade deployment with external databases and object storage.

## What Problem Does This Solve?

While AFFiNE Cloud provides a managed experience, many teams and organizations need to self-host for data sovereignty, compliance, air-gapped environments, or integration with internal infrastructure. This chapter provides a clear path from local Docker deployment to hardened production operations.

## Learning Goals

- deploy AFFiNE using Docker and Docker Compose
- configure PostgreSQL, Redis, and object storage backends
- set up authentication and user management
- understand the server architecture and API surface
- configure backups, monitoring, and operational health checks
- scale AFFiNE for team and organizational use

## Quick Start: Docker Compose

The fastest way to run a self-hosted AFFiNE instance:

```yaml
# docker-compose.yml

version: '3.8'

services:
  affine:
    image: ghcr.io/toeverything/affine-graphql:stable
    container_name: affine
    ports:
      - '3010:3010'
      - '5555:5555'
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - NODE_ENV=production
      - AFFINE_SERVER_PORT=3010
      - AFFINE_SERVER_HOST=0.0.0.0

      # Database configuration
      - DATABASE_URL=postgresql://affine:affine_password@postgres:5432/affine

      # Redis configuration
      - REDIS_SERVER_HOST=redis
      - REDIS_SERVER_PORT=6379

      # Server configuration
      - AFFINE_SERVER_HTTPS=false
      - AFFINE_SERVER_EXTERNAL_URL=http://localhost:3010

      # Authentication
      - AFFINE_AUTH_EMAIL_SENDER=noreply@example.com

      # Storage (local filesystem by default)
      - AFFINE_STORAGE_PROVIDER=fs
      - AFFINE_STORAGE_PATH=/data/storage

      # AI Copilot (optional)
      # - COPILOT_OPENAI_API_KEY=sk-...
      # - COPILOT_OPENAI_MODEL=gpt-4o

    volumes:
      - affine_data:/data
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    container_name: affine-postgres
    environment:
      POSTGRES_USER: affine
      POSTGRES_PASSWORD: affine_password
      POSTGRES_DB: affine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U affine']
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: affine-redis
    volumes:
      - redis_data:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  affine_data:
  postgres_data:
  redis_data:
```

```bash
# Deploy with Docker Compose
docker compose up -d

# Check logs
docker compose logs -f affine

# The application will be available at http://localhost:3010
```

## Server Architecture

The AFFiNE server is a Node.js application built with NestJS that provides several services:

```mermaid
flowchart TD
    subgraph "AFFiNE Server"
        A[NestJS Application]
        B[GraphQL API]
        C[WebSocket Server]
        D[REST Endpoints]
    end

    subgraph "Services"
        E[Auth Service]
        F[Workspace Service]
        G[Doc Sync Service]
        H[Copilot Service]
        I[Storage Service]
        J[User Service]
    end

    subgraph "Storage"
        K[(PostgreSQL)]
        L[(Redis)]
        M[(Object Storage)]
    end

    A --> B
    A --> C
    A --> D
    B --> E
    B --> F
    B --> J
    C --> G
    B --> H
    B --> I
    E --> K
    F --> K
    G --> K
    G --> L
    H --> K
    I --> M
    J --> K
```

### Key Server Components

```typescript
// packages/backend/server/src/app.module.ts
// Simplified module structure

@Module({
  imports: [
    // Core infrastructure
    ConfigModule,
    PrismaModule,        // PostgreSQL via Prisma ORM
    CacheModule,         // Redis caching
    StorageModule,       // File/blob storage

    // Feature modules
    AuthModule,          // Authentication and sessions
    UserModule,          // User management
    WorkspaceModule,     // Workspace CRUD and permissions
    DocModule,           // Document management and sync
    SyncModule,          // WebSocket sync protocol
    CopilotModule,       // AI features
    QuotaModule,         // Usage limits and quotas

    // API surface
    GraphQLModule,       // GraphQL API (primary)
  ],
})
export class AppModule {}
```

## Database Configuration

AFFiNE uses PostgreSQL for relational data and metadata:

```typescript
// Database schema managed by Prisma
// packages/backend/server/prisma/schema.prisma

// Key models:

model User {
  id            String   @id @default(uuid())
  email         String   @unique
  name          String?
  avatarUrl     String?
  emailVerified Boolean  @default(false)
  createdAt     DateTime @default(now())

  workspaces    WorkspaceUserPermission[]
  sessions      Session[]
}

model Workspace {
  id        String   @id @default(uuid())
  public    Boolean  @default(false)
  createdAt DateTime @default(now())

  permissions WorkspaceUserPermission[]
  docs        Doc[]
}

model Doc {
  id          String   @id
  workspaceId String
  workspace   Workspace @relation(fields: [workspaceId], references: [id])

  // yjs document binary data
  blob        Bytes?

  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model WorkspaceUserPermission {
  id          String   @id @default(uuid())
  workspaceId String
  userId      String
  // Owner, Admin, Write, Read
  permission  Int

  workspace   Workspace @relation(fields: [workspaceId], references: [id])
  user        User      @relation(fields: [userId], references: [id])
}
```

### Running Database Migrations

```bash
# Run pending migrations
docker compose exec affine npx prisma migrate deploy

# Or within the container
docker compose exec affine sh -c "node --import ./scripts/migrate.mjs"
```

## Storage Backend Configuration

AFFiNE supports multiple storage backends for blobs (images, attachments, files):

### Local Filesystem (Default)

```bash
# Environment variables
AFFINE_STORAGE_PROVIDER=fs
AFFINE_STORAGE_PATH=/data/storage
```

### AWS S3

```bash
# S3-compatible object storage
AFFINE_STORAGE_PROVIDER=s3
AFFINE_S3_BUCKET=my-affine-bucket
AFFINE_S3_REGION=us-east-1
AFFINE_S3_ACCESS_KEY_ID=AKIA...
AFFINE_S3_SECRET_ACCESS_KEY=...
AFFINE_S3_ENDPOINT=https://s3.amazonaws.com
```

### S3-Compatible (MinIO, R2, etc.)

```bash
# MinIO example
AFFINE_STORAGE_PROVIDER=s3
AFFINE_S3_BUCKET=affine
AFFINE_S3_REGION=us-east-1
AFFINE_S3_ACCESS_KEY_ID=minioadmin
AFFINE_S3_SECRET_ACCESS_KEY=minioadmin
AFFINE_S3_ENDPOINT=http://minio:9000
AFFINE_S3_FORCE_PATH_STYLE=true
```

## Authentication Configuration

### Email/Password (Default)

```bash
# SMTP configuration for email verification
MAILER_HOST=smtp.example.com
MAILER_PORT=465
MAILER_USER=noreply@example.com
MAILER_PASSWORD=your_smtp_password
MAILER_SENDER=noreply@example.com
MAILER_SECURE=true
```

### OAuth Providers

```bash
# Google OAuth
OAUTH_GOOGLE_CLIENT_ID=...
OAUTH_GOOGLE_CLIENT_SECRET=...

# GitHub OAuth
OAUTH_GITHUB_CLIENT_ID=...
OAUTH_GITHUB_CLIENT_SECRET=...
```

## How It Works Under the Hood: Request Flow

```mermaid
sequenceDiagram
    participant Client as AFFiNE Client
    participant LB as Load Balancer / Reverse Proxy
    participant Server as AFFiNE Server
    participant PG as PostgreSQL
    participant Redis as Redis
    participant S3 as Object Storage

    Note over Client,S3: Page Load
    Client->>LB: GET / (static assets)
    LB->>Server: Proxy request
    Server->>Client: SPA bundle

    Note over Client,S3: Authentication
    Client->>Server: GraphQL mutation: signIn
    Server->>PG: Verify credentials
    Server->>Redis: Create session
    Server->>Client: Auth token

    Note over Client,S3: Document Sync
    Client->>Server: WebSocket connect
    Server->>PG: Load doc state
    Server->>Client: SyncStep2 (yjs updates)
    Client->>Server: Live updates (yjs binary)
    Server->>PG: Persist updates
    Server->>Redis: Pub/Sub to other instances

    Note over Client,S3: Blob Upload
    Client->>Server: Upload image
    Server->>S3: Store blob
    Server->>PG: Record blob metadata
    Server->>Client: Blob URL
```

## Reverse Proxy Configuration

### Nginx

```nginx
# /etc/nginx/conf.d/affine.conf

server {
    listen 443 ssl http2;
    server_name affine.example.com;

    ssl_certificate /etc/ssl/certs/affine.pem;
    ssl_certificate_key /etc/ssl/private/affine.key;

    # Maximum upload size for attachments
    client_max_body_size 100M;

    location / {
        proxy_pass http://localhost:3010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support for real-time sync
    location /socket.io/ {
        proxy_pass http://localhost:3010;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }
}
```

## Backup Strategy

### Database Backup

```bash
#!/bin/bash
# backup.sh — automated PostgreSQL backup

BACKUP_DIR="/backups/affine"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/affine_${TIMESTAMP}.sql.gz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Dump PostgreSQL database
docker compose exec -T postgres pg_dump \
  -U affine \
  -d affine \
  --format=custom \
  | gzip > "$BACKUP_FILE"

# Retain last 30 days of backups
find "$BACKUP_DIR" -name "affine_*.sql.gz" -mtime +30 -delete

echo "Backup created: $BACKUP_FILE"
```

### Blob Storage Backup

```bash
# For filesystem storage
rsync -avz /data/storage/ /backups/affine-blobs/

# For S3 storage — blobs are already durable in S3
# But you may want cross-region replication for DR
```

## Health Checks and Monitoring

```bash
# Server health endpoint
curl http://localhost:3010/api/healthz

# Response: { "status": "ok" }
```

```yaml
# Docker Compose healthcheck for the AFFiNE service
services:
  affine:
    # ... other config ...
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:3010/api/healthz']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Key Metrics to Monitor

```typescript
// Important operational metrics:
const monitoringChecklist = {
  // Infrastructure
  'cpu_usage': 'Server CPU utilization',
  'memory_usage': 'Server memory utilization',
  'disk_usage': 'Storage volume capacity',

  // Application
  'websocket_connections': 'Active sync connections',
  'api_response_time': 'GraphQL query latency (p50, p95, p99)',
  'sync_latency': 'Time for yjs updates to propagate',

  // Database
  'pg_connections': 'Active PostgreSQL connections',
  'pg_query_time': 'Slow query detection',
  'redis_memory': 'Redis memory usage',

  // Storage
  'blob_storage_size': 'Total blob storage consumption',
  'upload_errors': 'Failed blob uploads',
};
```

## Scaling Considerations

### Horizontal Scaling

```mermaid
flowchart TD
    LB[Load Balancer] --> S1[AFFiNE Server 1]
    LB --> S2[AFFiNE Server 2]
    LB --> S3[AFFiNE Server 3]

    S1 --> PG[(PostgreSQL)]
    S2 --> PG
    S3 --> PG

    S1 --> R[(Redis - Pub/Sub)]
    S2 --> R
    S3 --> R

    S1 --> OS[(Object Storage)]
    S2 --> OS
    S3 --> OS
```

When running multiple server instances:

- **WebSocket affinity** — use sticky sessions or Redis Pub/Sub to ensure real-time sync works across instances
- **Redis Pub/Sub** — used to broadcast yjs updates between server instances so all connected clients receive updates
- **Shared storage** — all instances must use the same PostgreSQL database and object storage backend
- **Session management** — Redis-backed sessions work across instances

### Environment Variables for Scaling

```bash
# Enable Redis-based pub/sub for multi-instance sync
AFFINE_SYNC_PUBSUB=redis

# Connection pool sizing
DATABASE_POOL_SIZE=20

# WebSocket configuration
AFFINE_WS_MAX_CONNECTIONS=10000
AFFINE_WS_PING_INTERVAL=30000
```

## Upgrade Procedure

```bash
# 1. Pull the latest image
docker compose pull affine

# 2. Stop the current instance
docker compose stop affine

# 3. Run database migrations (if needed)
docker compose run --rm affine npx prisma migrate deploy

# 4. Start the new version
docker compose up -d affine

# 5. Verify health
curl http://localhost:3010/api/healthz

# 6. Check logs for errors
docker compose logs --tail=100 affine
```

## Source References

- [AFFiNE Self-Host Docs](https://docs.affine.pro/docs/self-host-affine)
- [AFFiNE Docker Images](https://github.com/toeverything/AFFiNE/pkgs/container/affine-graphql)
- [Server Package](https://github.com/toeverything/AFFiNE/tree/canary/packages/backend/server)
- [Docker Configuration](https://github.com/toeverything/AFFiNE/tree/canary/docker)

## Summary

Self-hosting AFFiNE involves deploying the server with Docker Compose, configuring PostgreSQL for metadata, Redis for caching and pub/sub, and an object storage backend for blobs. The server provides GraphQL APIs, WebSocket sync, and authentication — all behind a reverse proxy for production use. Backup, monitoring, and scaling follow standard patterns for Node.js applications with stateful WebSocket connections.

---

[Back to Tutorial Index](README.md) | [Previous: Chapter 7](07-plugin-system.md)

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
