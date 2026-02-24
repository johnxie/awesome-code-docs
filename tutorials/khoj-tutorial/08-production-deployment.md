---
layout: default
title: "Khoj AI - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: "Khoj AI - Personal Assistant Deep Dive"
---

# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **Khoj AI: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Deploying Khoj in a production environment requires careful consideration of infrastructure, security, performance, and reliability. This chapter provides a comprehensive guide to running Khoj at scale, covering Docker deployment, reverse proxy configuration, security hardening, monitoring, backup strategies, and multi-user scaling.

## Production Architecture

A production Khoj deployment typically involves several components working together behind a reverse proxy, with persistent storage and monitoring infrastructure.

```mermaid
flowchart TD
    subgraph Internet["Internet"]
        U[Users]
    end

    subgraph Edge["Edge / Load Balancer"]
        LB[Nginx / Caddy]
        CERT[TLS Certificate]
    end

    subgraph App["Application Tier"]
        K1[Khoj Instance 1]
        K2[Khoj Instance 2]
        W[Celery Workers]
    end

    subgraph Data["Data Tier"]
        PG[(PostgreSQL + pgvector)]
        REDIS[(Redis Cache)]
        FS[File Storage / NFS]
    end

    subgraph External["External Services"]
        LLM[LLM API Providers]
        SMTP[Email Service]
    end

    subgraph Monitoring["Monitoring"]
        PROM[Prometheus]
        GRAF[Grafana]
        LOGS[Log Aggregator]
    end

    U --> LB
    LB --> CERT
    CERT --> K1
    CERT --> K2
    K1 --> PG
    K2 --> PG
    K1 --> REDIS
    K2 --> REDIS
    K1 --> FS
    K2 --> FS
    W --> PG
    W --> REDIS
    K1 --> LLM
    K2 --> LLM
    K1 --> SMTP
    K1 --> PROM
    K2 --> PROM
    PROM --> GRAF

    classDef edge fill:#fce4ec,stroke:#c62828
    classDef app fill:#e3f2fd,stroke:#1565c0
    classDef data fill:#e8f5e9,stroke:#2e7d32
    classDef external fill:#fff3e0,stroke:#e65100
    classDef monitor fill:#f3e5f5,stroke:#7b1fa2

    class LB,CERT edge
    class K1,K2,W app
    class PG,REDIS,FS data
    class LLM,SMTP external
    class PROM,GRAF,LOGS monitor
```

## Docker Deployment

Docker Compose is the recommended deployment method for production Khoj instances. Here is a production-ready configuration:

```python
# Generate a production docker-compose configuration
def generate_docker_compose_config(
    domain: str = "khoj.example.com",
    admin_email: str = "admin@example.com",
    postgres_password: str = "CHANGE_ME_STRONG_PASSWORD",
    enable_ssl: bool = True,
    replicas: int = 1,
) -> str:
    """
    Generate a production-grade Docker Compose configuration.

    Key differences from development:
    - PostgreSQL with pgvector for vector storage
    - Redis for caching and task queuing
    - Nginx reverse proxy with TLS
    - Persistent volumes for data durability
    - Resource limits for predictable performance
    - Health checks for automatic recovery
    """
    config = f"""
# Production Docker Compose for Khoj
# Domain: {domain}
# Generated configuration - review before deploying

version: '3.9'

services:
  khoj:
    image: ghcr.io/khoj-ai/khoj:latest
    container_name: khoj-app
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - KHOJ_ADMIN_EMAIL={admin_email}
      - KHOJ_ADMIN_PASSWORD=${{KHOJ_ADMIN_PASSWORD}}
      - DATABASE_URL=postgresql://khoj:{postgres_password}@postgres:5432/khoj
      - REDIS_URL=redis://redis:6379/0
      - KHOJ_DEBUG=false
      - KHOJ_DOMAIN={domain}
      - OPENAI_API_KEY=${{OPENAI_API_KEY}}
    volumes:
      - khoj-data:/root/.khoj
      - content-data:/data
    deploy:
      replicas: {replicas}
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:42110/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - khoj-network

  postgres:
    image: pgvector/pgvector:pg16
    container_name: khoj-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=khoj
      - POSTGRES_USER=khoj
      - POSTGRES_PASSWORD={postgres_password}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U khoj"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - khoj-network

  redis:
    image: redis:7-alpine
    container_name: khoj-redis
    restart: unless-stopped
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - khoj-network

  nginx:
    image: nginx:alpine
    container_name: khoj-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - certbot-data:/var/www/certbot
    depends_on:
      - khoj
    networks:
      - khoj-network

volumes:
  khoj-data:
  content-data:
  postgres-data:
  redis-data:
  certbot-data:

networks:
  khoj-network:
    driver: bridge
"""
    return config.strip()

config = generate_docker_compose_config(domain="khoj.example.com")
print("Docker Compose configuration generated")
print(f"Configuration length: {len(config)} characters")
```

### Nginx Reverse Proxy Configuration

```python
def generate_nginx_config(
    domain: str = "khoj.example.com",
    upstream_port: int = 42110,
    enable_ssl: bool = True,
    enable_websockets: bool = True,
) -> str:
    """Generate Nginx configuration for Khoj."""
    config = f"""
worker_processes auto;

events {{
    worker_connections 1024;
}}

http {{
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
    limit_req_zone $binary_remote_addr zone=search:10m rate=60r/m;

    # Upstream for Khoj
    upstream khoj_backend {{
        server khoj:42110;
        keepalive 32;
    }}

    # Redirect HTTP to HTTPS
    server {{
        listen 80;
        server_name {domain};
        return 301 https://$server_name$request_uri;
    }}

    # HTTPS server
    server {{
        listen 443 ssl http2;
        server_name {domain};

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 1d;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Strict-Transport-Security "max-age=63072000" always;

        # Request size limit (for file uploads)
        client_max_body_size 50M;

        # API rate limiting
        location /api/chat {{
            limit_req zone=api burst=5 nodelay;
            proxy_pass http://khoj_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # SSE support for streaming
            proxy_buffering off;
            proxy_cache off;
            proxy_read_timeout 300s;
        }}

        location /api/search {{
            limit_req zone=search burst=10 nodelay;
            proxy_pass http://khoj_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}

        # WebSocket support
        location /ws/ {{
            proxy_pass http://khoj_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_read_timeout 86400s;
        }}

        # All other requests
        location / {{
            proxy_pass http://khoj_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}

        # Static files caching
        location /static/ {{
            proxy_pass http://khoj_backend;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }}
    }}
}}
"""
    return config.strip()

nginx_config = generate_nginx_config(domain="khoj.example.com")
print("Nginx configuration generated with SSL, rate limiting, and WebSocket support")
```

## Security Hardening

### Authentication and Access Control

```python
from dataclasses import dataclass

@dataclass
class SecurityConfig:
    """Production security configuration for Khoj."""

    # Authentication
    require_authentication: bool = True
    session_timeout_hours: int = 24
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30

    # API Security
    api_rate_limit_per_minute: int = 60
    require_api_key: bool = True
    api_key_rotation_days: int = 90

    # Network Security
    allowed_origins: list = None  # CORS origins
    allowed_hosts: list = None
    force_https: bool = True

    # Data Security
    encrypt_at_rest: bool = True
    encrypt_api_keys: bool = True
    mask_sensitive_logs: bool = True

    # Content Security
    max_upload_size_mb: int = 50
    allowed_file_types: list = None

    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = ["https://khoj.example.com"]
        if self.allowed_hosts is None:
            self.allowed_hosts = ["khoj.example.com"]
        if self.allowed_file_types is None:
            self.allowed_file_types = [
                ".md", ".org", ".txt", ".pdf",
                ".rst", ".html", ".json",
            ]

class SecurityHardener:
    """
    Applies security hardening measures to a Khoj deployment.
    """

    def __init__(self, config: SecurityConfig):
        self.config = config

    def generate_env_security_vars(self) -> dict:
        """Generate environment variables for security settings."""
        env_vars = {
            "KHOJ_REQUIRE_AUTH": str(self.config.require_authentication),
            "KHOJ_SESSION_TIMEOUT": str(
                self.config.session_timeout_hours * 3600
            ),
            "KHOJ_MAX_LOGIN_ATTEMPTS": str(self.config.max_login_attempts),
            "KHOJ_FORCE_HTTPS": str(self.config.force_https),
            "KHOJ_ALLOWED_HOSTS": ",".join(self.config.allowed_hosts),
            "KHOJ_CORS_ORIGINS": ",".join(self.config.allowed_origins),
            "KHOJ_MAX_UPLOAD_SIZE": str(
                self.config.max_upload_size_mb * 1024 * 1024
            ),
        }
        return env_vars

    def audit_configuration(self) -> list[dict]:
        """Audit the security configuration and return findings."""
        findings = []

        if not self.config.require_authentication:
            findings.append({
                "severity": "HIGH",
                "finding": "Authentication is disabled",
                "recommendation": "Enable require_authentication for production",
            })

        if not self.config.force_https:
            findings.append({
                "severity": "HIGH",
                "finding": "HTTPS is not enforced",
                "recommendation": "Enable force_https for production",
            })

        if self.config.api_rate_limit_per_minute > 120:
            findings.append({
                "severity": "MEDIUM",
                "finding": "API rate limit may be too high",
                "recommendation": "Consider lowering to prevent abuse",
            })

        if self.config.session_timeout_hours > 48:
            findings.append({
                "severity": "MEDIUM",
                "finding": "Session timeout is very long",
                "recommendation": "Consider reducing to 24 hours or less",
            })

        if not self.config.mask_sensitive_logs:
            findings.append({
                "severity": "MEDIUM",
                "finding": "Sensitive data may appear in logs",
                "recommendation": "Enable mask_sensitive_logs",
            })

        if not findings:
            findings.append({
                "severity": "INFO",
                "finding": "No security issues found",
                "recommendation": "Configuration looks good",
            })

        return findings

# Example
security_config = SecurityConfig(
    require_authentication=True,
    force_https=True,
    api_rate_limit_per_minute=60,
)

hardener = SecurityHardener(security_config)
env_vars = hardener.generate_env_security_vars()
print("Security environment variables:")
for key, value in env_vars.items():
    print(f"  {key}={value}")

print("\nSecurity audit:")
for finding in hardener.audit_configuration():
    print(f"  [{finding['severity']}] {finding['finding']}")
    print(f"    -> {finding['recommendation']}")
```

### Secrets Management

```python
import os
from typing import Optional

class SecretsManager:
    """
    Manages secrets for a Khoj production deployment.

    Supports multiple backends:
    - Environment variables
    - Docker secrets
    - HashiCorp Vault
    - AWS Secrets Manager
    """

    REQUIRED_SECRETS = [
        "KHOJ_ADMIN_PASSWORD",
        "DATABASE_URL",
        "OPENAI_API_KEY",  # If using OpenAI
    ]

    OPTIONAL_SECRETS = [
        "ANTHROPIC_API_KEY",
        "SERPER_API_KEY",
        "SMTP_PASSWORD",
        "WEBHOOK_SECRET",
    ]

    def validate_secrets(self) -> dict:
        """Validate that all required secrets are configured."""
        results = {"valid": True, "missing": [], "present": []}

        for secret in self.REQUIRED_SECRETS:
            if os.environ.get(secret):
                results["present"].append(secret)
            else:
                results["missing"].append(secret)
                results["valid"] = False

        return results

    def generate_secrets_template(self) -> str:
        """Generate a .env template for production deployment."""
        template = "# Khoj Production Secrets\n"
        template += "# Copy to .env and fill in values\n\n"

        template += "# Required\n"
        for secret in self.REQUIRED_SECRETS:
            template += f"{secret}=\n"

        template += "\n# Optional\n"
        for secret in self.OPTIONAL_SECRETS:
            template += f"# {secret}=\n"

        return template

secrets_mgr = SecretsManager()
validation = secrets_mgr.validate_secrets()
print(f"Secrets validation: {'PASS' if validation['valid'] else 'FAIL'}")
if validation["missing"]:
    print(f"Missing secrets: {', '.join(validation['missing'])}")
```

## Database Management

### PostgreSQL with pgvector Optimization

```python
class DatabaseOptimizer:
    """
    Optimization guidelines and scripts for PostgreSQL
    with pgvector in a production Khoj deployment.
    """

    RECOMMENDED_SETTINGS = {
        # Connection pool
        "max_connections": 100,
        "shared_buffers": "256MB",       # 25% of RAM
        "effective_cache_size": "768MB",  # 75% of RAM

        # Write performance
        "wal_buffers": "16MB",
        "checkpoint_completion_target": 0.9,
        "max_wal_size": "1GB",

        # Query performance
        "random_page_cost": 1.1,         # SSD optimized
        "effective_io_concurrency": 200,  # SSD optimized
        "work_mem": "16MB",
        "maintenance_work_mem": "128MB",

        # pgvector specific
        "ivfflat.probes": 10,
    }

    def generate_postgresql_conf(self, total_ram_gb: int = 4) -> str:
        """Generate optimized PostgreSQL configuration."""
        shared_buffers = f"{total_ram_gb * 256}MB"
        effective_cache = f"{total_ram_gb * 768}MB"
        maintenance_mem = f"{min(total_ram_gb * 64, 512)}MB"

        conf = f"""
# PostgreSQL Production Configuration for Khoj
# Optimized for {total_ram_gb}GB RAM

# Memory
shared_buffers = {shared_buffers}
effective_cache_size = {effective_cache}
work_mem = 16MB
maintenance_work_mem = {maintenance_mem}

# Connections
max_connections = 100

# Write Ahead Log
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 1GB

# Query Planner
random_page_cost = 1.1
effective_io_concurrency = 200

# Logging
log_min_duration_statement = 1000
log_checkpoints = on
log_connections = on
log_disconnections = on

# Autovacuum
autovacuum_max_workers = 3
autovacuum_naptime = 60
"""
        return conf.strip()

    def generate_index_maintenance_sql(self) -> str:
        """Generate SQL for maintaining vector indexes."""
        return """
-- Reindex vector embeddings (run periodically after large data changes)
REINDEX INDEX CONCURRENTLY entry_embeddings_idx;

-- Analyze tables for query planner
ANALYZE entry;
ANALYZE conversation;

-- Check index health
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_indexes
WHERE tablename = 'entry'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check table bloat
SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    pg_size_pretty(pg_relation_size(relid)) AS data_size,
    n_live_tup AS live_rows,
    n_dead_tup AS dead_rows
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
"""

optimizer = DatabaseOptimizer()
print("PostgreSQL optimization for 4GB RAM:")
print(optimizer.generate_postgresql_conf(total_ram_gb=4)[:200] + "...")
```

## Monitoring and Observability

### Health Check Endpoints

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class HealthStatus:
    """Health check result for a Khoj component."""
    component: str
    healthy: bool
    latency_ms: float
    details: Optional[str] = None

class HealthChecker:
    """
    Comprehensive health checking for a Khoj deployment.

    Monitors:
    - Application server responsiveness
    - Database connectivity and query performance
    - Redis cache connectivity
    - Embedding model availability
    - LLM backend connectivity
    - Disk space availability
    """

    def run_all_checks(self) -> dict:
        """Execute all health checks and return results."""
        checks = [
            self._check_server(),
            self._check_database(),
            self._check_redis(),
            self._check_embedding_model(),
            self._check_llm_backend(),
            self._check_disk_space(),
        ]

        overall_healthy = all(c.healthy for c in checks)

        return {
            "status": "healthy" if overall_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "checks": [
                {
                    "component": c.component,
                    "healthy": c.healthy,
                    "latency_ms": c.latency_ms,
                    "details": c.details,
                }
                for c in checks
            ],
        }

    def _check_server(self) -> HealthStatus:
        """Check application server health."""
        return HealthStatus(
            component="server",
            healthy=True,
            latency_ms=1.2,
            details="Application server responding",
        )

    def _check_database(self) -> HealthStatus:
        """Check PostgreSQL connectivity and query performance."""
        # In production:
        # start = time.time()
        # cursor.execute("SELECT 1")
        # latency = (time.time() - start) * 1000
        return HealthStatus(
            component="database",
            healthy=True,
            latency_ms=5.3,
            details="PostgreSQL responding, pgvector extension loaded",
        )

    def _check_redis(self) -> HealthStatus:
        """Check Redis connectivity."""
        return HealthStatus(
            component="redis",
            healthy=True,
            latency_ms=0.8,
            details="Redis responding, memory usage 45MB/256MB",
        )

    def _check_embedding_model(self) -> HealthStatus:
        """Check embedding model availability."""
        return HealthStatus(
            component="embedding_model",
            healthy=True,
            latency_ms=15.0,
            details="Model loaded: all-MiniLM-L6-v2",
        )

    def _check_llm_backend(self) -> HealthStatus:
        """Check LLM backend connectivity."""
        return HealthStatus(
            component="llm_backend",
            healthy=True,
            latency_ms=120.0,
            details="OpenAI API responding",
        )

    def _check_disk_space(self) -> HealthStatus:
        """Check available disk space."""
        # In production: uses shutil.disk_usage()
        return HealthStatus(
            component="disk_space",
            healthy=True,
            latency_ms=0.5,
            details="45GB free of 100GB (55% used)",
        )

checker = HealthChecker()
health = checker.run_all_checks()
print(f"Overall status: {health['status']}")
for check in health["checks"]:
    status = "OK" if check["healthy"] else "FAIL"
    print(f"  [{status}] {check['component']}: "
          f"{check['latency_ms']:.1f}ms - {check['details']}")
```

### Metrics and Dashboards

```python
class MetricsCollector:
    """
    Collects operational metrics for monitoring Khoj deployments.

    Exports metrics in Prometheus format for scraping.
    """

    def __init__(self):
        self.metrics = {
            # Request metrics
            "http_requests_total": 0,
            "http_request_duration_seconds": [],
            "http_errors_total": 0,

            # Search metrics
            "search_queries_total": 0,
            "search_latency_seconds": [],
            "search_results_count": [],

            # Chat metrics
            "chat_messages_total": 0,
            "chat_response_tokens": [],
            "chat_context_entries_used": [],

            # Indexing metrics
            "index_entries_total": 0,
            "index_duration_seconds": [],
            "index_errors_total": 0,

            # System metrics
            "memory_usage_bytes": 0,
            "cpu_usage_percent": 0,
            "database_connections_active": 0,
        }

    def record_search(self, latency: float, results_count: int):
        """Record a search operation."""
        self.metrics["search_queries_total"] += 1
        self.metrics["search_latency_seconds"].append(latency)
        self.metrics["search_results_count"].append(results_count)

    def record_chat(self, response_tokens: int, context_entries: int):
        """Record a chat interaction."""
        self.metrics["chat_messages_total"] += 1
        self.metrics["chat_response_tokens"].append(response_tokens)
        self.metrics["chat_context_entries_used"].append(context_entries)

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus exposition format."""
        lines = []

        lines.append(
            f"khoj_search_queries_total "
            f"{self.metrics['search_queries_total']}"
        )
        lines.append(
            f"khoj_chat_messages_total "
            f"{self.metrics['chat_messages_total']}"
        )
        lines.append(
            f"khoj_index_entries_total "
            f"{self.metrics['index_entries_total']}"
        )

        # Calculate averages
        search_latencies = self.metrics["search_latency_seconds"]
        if search_latencies:
            avg_latency = sum(search_latencies) / len(search_latencies)
            lines.append(
                f"khoj_search_latency_seconds_avg {avg_latency:.4f}"
            )

        return "\n".join(lines)

    def get_dashboard_summary(self) -> dict:
        """Get a summary suitable for a monitoring dashboard."""
        return {
            "total_searches": self.metrics["search_queries_total"],
            "total_chats": self.metrics["chat_messages_total"],
            "total_indexed": self.metrics["index_entries_total"],
            "avg_search_latency_ms": self._avg(
                self.metrics["search_latency_seconds"]
            ) * 1000 if self.metrics["search_latency_seconds"] else 0,
            "error_rate": (
                self.metrics["http_errors_total"] /
                max(self.metrics["http_requests_total"], 1) * 100
            ),
        }

    def _avg(self, values: list) -> float:
        return sum(values) / len(values) if values else 0

collector = MetricsCollector()
collector.record_search(latency=0.045, results_count=5)
collector.record_search(latency=0.032, results_count=3)
collector.record_chat(response_tokens=150, context_entries=4)

print("Prometheus metrics:")
print(collector.export_prometheus())
print("\nDashboard summary:")
summary = collector.get_dashboard_summary()
for key, value in summary.items():
    print(f"  {key}: {value}")
```

## Backup and Recovery

```mermaid
flowchart TD
    A[Backup Strategy] --> B[Database Backup]
    A --> C[File Storage Backup]
    A --> D[Configuration Backup]

    B --> E[pg_dump - Full]
    B --> F[WAL Archiving - Continuous]
    B --> G[pgvector Index Backup]

    C --> H[Volume Snapshots]
    C --> I[File Sync to S3/GCS]

    D --> J[Export Config via API]
    D --> K[Docker Compose Files]
    D --> L[Environment Variables]

    E --> M[Encrypted Off-site Storage]
    F --> M
    H --> M
    I --> M
    J --> M

    classDef strategy fill:#e3f2fd,stroke:#1565c0
    classDef method fill:#fff3e0,stroke:#e65100
    classDef storage fill:#e8f5e9,stroke:#2e7d32

    class A strategy
    class B,C,D,E,F,G,H,I,J,K,L method
    class M storage
```

```python
from datetime import datetime
import subprocess

class BackupManager:
    """
    Manages backup and recovery for a Khoj production deployment.
    """

    def __init__(
        self,
        db_url: str = "postgresql://khoj:password@localhost:5432/khoj",
        backup_dir: str = "/var/backups/khoj",
        retention_days: int = 30,
    ):
        self.db_url = db_url
        self.backup_dir = backup_dir
        self.retention_days = retention_days

    def create_full_backup(self) -> dict:
        """
        Create a full backup of the Khoj deployment.

        Includes:
        1. PostgreSQL database dump (including pgvector data)
        2. File storage snapshot
        3. Configuration export
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/khoj_backup_{timestamp}"

        results = {
            "timestamp": timestamp,
            "backup_path": backup_path,
            "components": {},
        }

        # 1. Database backup
        db_backup = self._backup_database(backup_path)
        results["components"]["database"] = db_backup

        # 2. File storage backup
        files_backup = self._backup_files(backup_path)
        results["components"]["files"] = files_backup

        # 3. Configuration backup
        config_backup = self._backup_config(backup_path)
        results["components"]["config"] = config_backup

        return results

    def _backup_database(self, backup_path: str) -> dict:
        """Create a PostgreSQL database dump."""
        dump_file = f"{backup_path}/database.sql.gz"

        # Command to run:
        # pg_dump $DATABASE_URL | gzip > $dump_file
        command = (
            f"pg_dump {self.db_url} "
            f"--format=custom "
            f"--compress=9 "
            f"--file={dump_file}"
        )

        print(f"Database backup command: pg_dump -> {dump_file}")
        return {"file": dump_file, "status": "completed"}

    def _backup_files(self, backup_path: str) -> dict:
        """Backup file storage volume."""
        tar_file = f"{backup_path}/files.tar.gz"

        # Command to run:
        # tar czf $tar_file /root/.khoj /data
        print(f"Files backup: /root/.khoj, /data -> {tar_file}")
        return {"file": tar_file, "status": "completed"}

    def _backup_config(self, backup_path: str) -> dict:
        """Backup configuration files."""
        config_file = f"{backup_path}/config.json"

        # Export configuration via API
        # response = requests.get(f"{base_url}/api/config/export")
        print(f"Config backup -> {config_file}")
        return {"file": config_file, "status": "completed"}

    def restore_from_backup(self, backup_path: str) -> dict:
        """Restore a Khoj deployment from a backup."""
        print(f"Restoring from: {backup_path}")
        steps = [
            "1. Stop Khoj services",
            "2. Restore PostgreSQL database from dump",
            "3. Restore file storage from tar archive",
            "4. Import configuration",
            "5. Rebuild vector indexes",
            "6. Restart Khoj services",
            "7. Verify health checks pass",
        ]

        for step in steps:
            print(f"  {step}")

        return {"status": "restored", "backup_path": backup_path}

    def generate_backup_cron(self) -> str:
        """Generate a cron schedule for automated backups."""
        cron = f"""
# Khoj Backup Schedule
# Full backup daily at 2 AM
0 2 * * * /usr/local/bin/khoj-backup.sh full >> /var/log/khoj-backup.log 2>&1

# Clean old backups weekly
0 3 * * 0 find {self.backup_dir} -type f -mtime +{self.retention_days} -delete

# Verify backup integrity monthly
0 4 1 * * /usr/local/bin/khoj-backup.sh verify >> /var/log/khoj-backup.log 2>&1
"""
        return cron.strip()

backup_mgr = BackupManager()
backup_result = backup_mgr.create_full_backup()
print(f"\nBackup completed: {backup_result['timestamp']}")
for component, details in backup_result["components"].items():
    print(f"  {component}: {details['status']}")
```

## Scaling Considerations

### Scaling Strategy

| Users | Configuration | Resources | Notes |
|-------|--------------|-----------|-------|
| 1-10 | Single instance | 2 CPU, 4 GB RAM | Development/personal use |
| 10-50 | Single instance + Redis | 4 CPU, 8 GB RAM | Small team |
| 50-200 | 2 instances + load balancer | 8 CPU, 16 GB RAM | Medium organization |
| 200+ | Multiple instances + dedicated DB | 16+ CPU, 32+ GB RAM | Large organization |

```python
class ScalingAdvisor:
    """
    Provides scaling recommendations based on deployment parameters.
    """

    def recommend(
        self,
        user_count: int,
        total_documents: int,
        avg_queries_per_day: int,
    ) -> dict:
        """Generate scaling recommendations."""
        recommendation = {
            "user_count": user_count,
            "total_documents": total_documents,
            "avg_queries_per_day": avg_queries_per_day,
        }

        # Compute resource requirements
        if user_count <= 10:
            recommendation["tier"] = "Personal"
            recommendation["instances"] = 1
            recommendation["cpu_cores"] = 2
            recommendation["ram_gb"] = 4
            recommendation["db_storage_gb"] = 10
        elif user_count <= 50:
            recommendation["tier"] = "Team"
            recommendation["instances"] = 1
            recommendation["cpu_cores"] = 4
            recommendation["ram_gb"] = 8
            recommendation["db_storage_gb"] = 50
        elif user_count <= 200:
            recommendation["tier"] = "Organization"
            recommendation["instances"] = 2
            recommendation["cpu_cores"] = 8
            recommendation["ram_gb"] = 16
            recommendation["db_storage_gb"] = 200
        else:
            recommendation["tier"] = "Enterprise"
            recommendation["instances"] = max(4, user_count // 50)
            recommendation["cpu_cores"] = 16
            recommendation["ram_gb"] = 32
            recommendation["db_storage_gb"] = 500

        # Estimate embedding storage
        embedding_dim = 384
        bytes_per_embedding = embedding_dim * 4  # float32
        total_embedding_bytes = total_documents * bytes_per_embedding
        recommendation["embedding_storage_mb"] = round(
            total_embedding_bytes / (1024 * 1024), 1
        )

        # Recommendations
        recommendation["use_redis"] = user_count > 5
        recommendation["use_load_balancer"] = recommendation["instances"] > 1
        recommendation["use_gpu"] = total_documents > 100_000
        recommendation["dedicated_db"] = user_count > 100

        return recommendation

advisor = ScalingAdvisor()
rec = advisor.recommend(
    user_count=50,
    total_documents=25_000,
    avg_queries_per_day=500,
)

print(f"Scaling Recommendation: {rec['tier']} Tier")
print(f"  Instances: {rec['instances']}")
print(f"  CPU Cores: {rec['cpu_cores']}")
print(f"  RAM: {rec['ram_gb']} GB")
print(f"  DB Storage: {rec['db_storage_gb']} GB")
print(f"  Embedding Storage: {rec['embedding_storage_mb']} MB")
print(f"  Redis: {'Yes' if rec['use_redis'] else 'No'}")
print(f"  Load Balancer: {'Yes' if rec['use_load_balancer'] else 'No'}")
print(f"  GPU: {'Recommended' if rec['use_gpu'] else 'Not needed'}")
```

## Deployment Checklist

```python
PRODUCTION_CHECKLIST = {
    "Infrastructure": [
        "PostgreSQL with pgvector extension installed",
        "Redis configured with memory limits",
        "TLS certificates provisioned (Let's Encrypt or custom)",
        "Reverse proxy configured (Nginx/Caddy)",
        "DNS records pointing to server",
        "Firewall rules: only 80/443 exposed",
    ],
    "Security": [
        "Strong admin password set",
        "API keys configured and rotated",
        "HTTPS enforced (HTTP redirects to HTTPS)",
        "CORS origins restricted to known domains",
        "Rate limiting configured on API endpoints",
        "Security headers added (HSTS, CSP, etc.)",
    ],
    "Data": [
        "Database backups scheduled (daily)",
        "Backup retention policy defined (30+ days)",
        "Backup restoration tested",
        "Content source paths configured",
        "Initial indexing completed successfully",
    ],
    "Monitoring": [
        "Health check endpoint verified",
        "Metrics collection configured (Prometheus)",
        "Alerting rules set for critical failures",
        "Log aggregation configured",
        "Dashboard set up (Grafana)",
    ],
    "Operations": [
        "Docker Compose file version controlled",
        "Environment variables documented",
        "Rollback procedure documented",
        "Update/upgrade procedure documented",
        "On-call rotation established (if team)",
    ],
}

def print_checklist():
    """Print the production deployment checklist."""
    total = 0
    for category, items in PRODUCTION_CHECKLIST.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  [ ] {item}")
            total += 1
    print(f"\nTotal items: {total}")

print_checklist()
```

## Summary

In this chapter, you covered the full spectrum of production deployment for Khoj:

- **Docker Compose deployment** with PostgreSQL (pgvector), Redis, and Nginx reverse proxy
- **Nginx configuration** with TLS termination, rate limiting, WebSocket support, and security headers
- **Security hardening** including authentication, access control, secrets management, and security auditing
- **Database optimization** with PostgreSQL tuning, pgvector index maintenance, and connection pooling
- **Monitoring and observability** with health checks, Prometheus metrics, and dashboard summaries
- **Backup and recovery** with automated database dumps, file storage snapshots, and restoration procedures
- **Scaling strategies** with tier-based recommendations for different user counts and data volumes

## Key Takeaways

1. Docker Compose with pgvector/pgvector images provides the most straightforward production deployment path with built-in vector search support.
2. A reverse proxy (Nginx or Caddy) is essential for TLS termination, rate limiting, and security headers in production.
3. Regular automated backups with tested restoration procedures are non-negotiable for production deployments.
4. Health checks and monitoring should cover all critical components: application, database, cache, embedding model, and LLM backend.
5. Scaling is primarily vertical for small-to-medium deployments; horizontal scaling with load balancing becomes relevant above 50 concurrent users.
6. Security hardening is a continuous process -- the checklist provides a baseline, but regular audits and updates are essential.

---
*Built with insights from the [Khoj](https://github.com/khoj-ai/khoj) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `khoj`, `print` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment` as an operating subsystem inside **Khoj AI: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `recommendation`, `metrics`, `config` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `khoj` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `print`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Khoj](https://github.com/khoj-ai/khoj)
  Why it matters: authoritative reference on `Khoj` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `khoj` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Customization & Plugins](07-customization-and-plugins.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
