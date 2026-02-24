---
layout: default
title: "Chapter 7: Production Deployment"
parent: "LanceDB Tutorial"
nav_order: 7
---

# Chapter 7: Production Deployment

Welcome to **Chapter 7: Production Deployment**. In this part of **LanceDB Tutorial: Serverless Vector Database for AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy LanceDB to production with cloud storage, monitoring, backup strategies, and operational best practices.

## Overview

This chapter covers deploying LanceDB in production environments, including cloud storage backends, scaling strategies, monitoring, backup and recovery, and operational best practices.

## Cloud Storage Backends

### Amazon S3

```python
import lancedb

# Connect to S3
db = lancedb.connect("s3://my-bucket/lancedb-data")

# With explicit credentials
db = lancedb.connect(
    "s3://my-bucket/lancedb-data",
    storage_options={
        "aws_access_key_id": "AKIA...",
        "aws_secret_access_key": "...",
        "aws_region": "us-east-1"
    }
)

# With IAM role (recommended for EC2/EKS)
# Just use the URI - credentials come from instance metadata
db = lancedb.connect("s3://my-bucket/lancedb-data")

# With S3-compatible storage (MinIO, etc.)
db = lancedb.connect(
    "s3://my-bucket/lancedb-data",
    storage_options={
        "aws_endpoint": "http://minio.local:9000",
        "aws_access_key_id": "minioadmin",
        "aws_secret_access_key": "minioadmin"
    }
)
```

### Google Cloud Storage

```python
import lancedb

# Connect to GCS
db = lancedb.connect("gs://my-bucket/lancedb-data")

# With service account
db = lancedb.connect(
    "gs://my-bucket/lancedb-data",
    storage_options={
        "google_service_account": "/path/to/service-account.json"
    }
)

# With Application Default Credentials
# gcloud auth application-default login
db = lancedb.connect("gs://my-bucket/lancedb-data")
```

### Azure Blob Storage

```python
import lancedb

# Connect to Azure
db = lancedb.connect("az://my-container/lancedb-data")

# With connection string
db = lancedb.connect(
    "az://my-container/lancedb-data",
    storage_options={
        "azure_storage_connection_string": "DefaultEndpointsProtocol=https;..."
    }
)

# With account key
db = lancedb.connect(
    "az://my-container/lancedb-data",
    storage_options={
        "azure_storage_account_name": "mystorageaccount",
        "azure_storage_account_key": "..."
    }
)
```

## Deployment Architectures

### Single Instance

```python
# Simple deployment for small to medium workloads
# Good for: < 10M vectors, < 100 QPS

import lancedb
from fastapi import FastAPI

app = FastAPI()
db = lancedb.connect("s3://my-bucket/lancedb")

@app.post("/search")
async def search(query: list[float], limit: int = 10):
    table = db.open_table("documents")
    results = table.search(query).limit(limit).to_list()
    return {"results": results}
```

### Multi-Instance with Shared Storage

```python
# Multiple instances sharing cloud storage
# Good for: Read-heavy workloads, horizontal scaling

# Instance 1, 2, 3... all connect to same storage
db = lancedb.connect("s3://my-bucket/shared-lancedb")

# Use a load balancer to distribute requests
# Each instance can handle reads independently
# Writes should be coordinated (single writer or distributed lock)
```

### Read Replicas

```python
# Primary for writes, replicas for reads
# Good for: High read throughput requirements

class LanceDBCluster:
    def __init__(self, primary_uri: str, replica_uris: list[str]):
        self.primary = lancedb.connect(primary_uri)
        self.replicas = [lancedb.connect(uri) for uri in replica_uris]
        self._replica_index = 0

    def get_read_connection(self):
        """Round-robin replica selection."""
        conn = self.replicas[self._replica_index]
        self._replica_index = (self._replica_index + 1) % len(self.replicas)
        return conn

    def get_write_connection(self):
        """Always use primary for writes."""
        return self.primary

# Usage
cluster = LanceDBCluster(
    primary_uri="s3://bucket/primary",
    replica_uris=[
        "s3://bucket/replica-1",
        "s3://bucket/replica-2"
    ]
)

# Reads go to replicas
read_db = cluster.get_read_connection()
results = read_db.open_table("docs").search(query).to_list()

# Writes go to primary
write_db = cluster.get_write_connection()
write_db.open_table("docs").add(new_data)
```

## Kubernetes Deployment

### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lancedb-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lancedb-api
  template:
    metadata:
      labels:
        app: lancedb-api
    spec:
      containers:
      - name: api
        image: my-registry/lancedb-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: LANCEDB_URI
          value: "s3://my-bucket/lancedb"
        - name: AWS_REGION
          value: "us-east-1"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
      serviceAccountName: lancedb-sa  # For IRSA with S3
---
apiVersion: v1
kind: Service
metadata:
  name: lancedb-api
spec:
  selector:
    app: lancedb-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### Service Account for AWS

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: lancedb-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/lancedb-s3-role
```

## Monitoring

### Health Checks

```python
from fastapi import FastAPI, HTTPException
import lancedb
import time

app = FastAPI()

@app.get("/health")
async def health():
    """Basic health check."""
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    """Readiness check - verify database connectivity."""
    try:
        db = lancedb.connect("s3://my-bucket/lancedb")
        tables = db.table_names()
        return {"status": "ready", "tables": len(tables)}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/health/deep")
async def deep_health():
    """Deep health check - verify search functionality."""
    try:
        db = lancedb.connect("s3://my-bucket/lancedb")
        table = db.open_table("documents")

        # Test search
        start = time.time()
        table.search([0.1] * 384).limit(1).to_list()
        latency = time.time() - start

        return {
            "status": "healthy",
            "search_latency_ms": latency * 1000,
            "row_count": table.count_rows()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response
import time

# Define metrics
SEARCH_REQUESTS = Counter(
    'lancedb_search_requests_total',
    'Total search requests',
    ['table', 'status']
)

SEARCH_LATENCY = Histogram(
    'lancedb_search_latency_seconds',
    'Search latency',
    ['table'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

TABLE_ROWS = Gauge(
    'lancedb_table_rows',
    'Number of rows in table',
    ['table']
)

app = FastAPI()

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

@app.post("/search/{table_name}")
async def search(table_name: str, query: list[float]):
    start = time.time()

    try:
        table = db.open_table(table_name)
        results = table.search(query).limit(10).to_list()

        SEARCH_REQUESTS.labels(table=table_name, status="success").inc()
        SEARCH_LATENCY.labels(table=table_name).observe(time.time() - start)

        return {"results": results}

    except Exception as e:
        SEARCH_REQUESTS.labels(table=table_name, status="error").inc()
        raise

# Background task to update row counts
async def update_table_metrics():
    while True:
        for table_name in db.table_names():
            table = db.open_table(table_name)
            TABLE_ROWS.labels(table=table_name).set(table.count_rows())
        await asyncio.sleep(60)
```

### Logging

```python
import logging
import json
from datetime import datetime

# Configure structured logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, 'extra'):
            log_entry.update(record.extra)
        return json.dumps(log_entry)

logger = logging.getLogger("lancedb")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Log search operations
def search_with_logging(table, query, limit=10):
    start = time.time()

    try:
        results = table.search(query).limit(limit).to_list()

        logger.info(
            "Search completed",
            extra={
                "extra": {
                    "table": table.name,
                    "limit": limit,
                    "results_count": len(results),
                    "latency_ms": (time.time() - start) * 1000
                }
            }
        )

        return results

    except Exception as e:
        logger.error(
            "Search failed",
            extra={
                "extra": {
                    "table": table.name,
                    "error": str(e)
                }
            }
        )
        raise
```

## Backup and Recovery

### Backup Strategies

```python
import shutil
from datetime import datetime
import boto3

def backup_to_s3(local_path: str, bucket: str, prefix: str):
    """Backup local LanceDB to S3."""
    s3 = boto3.client('s3')
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_prefix = f"{prefix}/backup_{timestamp}"

    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(local_file, local_path)
            s3_key = f"{backup_prefix}/{relative_path}"

            s3.upload_file(local_file, bucket, s3_key)
            print(f"Uploaded: {s3_key}")

    return backup_prefix

def restore_from_s3(bucket: str, backup_prefix: str, local_path: str):
    """Restore LanceDB from S3 backup."""
    s3 = boto3.client('s3')

    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=backup_prefix):
        for obj in page.get('Contents', []):
            s3_key = obj['Key']
            relative_path = s3_key[len(backup_prefix) + 1:]
            local_file = os.path.join(local_path, relative_path)

            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            s3.download_file(bucket, s3_key, local_file)
            print(f"Downloaded: {local_file}")
```

### Point-in-Time Recovery

```python
# LanceDB uses versioned storage in Lance format
# You can access historical versions

import lancedb

db = lancedb.connect("./my_lancedb")
table = db.open_table("documents")

# List versions
versions = table.list_versions()
for v in versions:
    print(f"Version {v['version']}: {v['timestamp']}")

# Checkout specific version
table.checkout(version=5)

# Read from historical version
historical_data = table.to_pandas()

# Restore to latest
table.checkout_latest()

# Time travel query
table.checkout(datetime="2024-01-15T10:30:00")
```

## Security

### Access Control

```python
# Use IAM policies for S3 access control

# Example IAM policy for read-only access
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-lancedb-bucket",
                "arn:aws:s3:::my-lancedb-bucket/*"
            ]
        }
    ]
}

# Example IAM policy for read-write access
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-lancedb-bucket",
                "arn:aws:s3:::my-lancedb-bucket/*"
            ]
        }
    ]
}
```

### Encryption

```python
# S3 Server-Side Encryption
db = lancedb.connect(
    "s3://my-bucket/lancedb",
    storage_options={
        "aws_server_side_encryption": "AES256"
    }
)

# Or with KMS
db = lancedb.connect(
    "s3://my-bucket/lancedb",
    storage_options={
        "aws_server_side_encryption": "aws:kms",
        "aws_sse_kms_key_id": "arn:aws:kms:region:account:key/key-id"
    }
)
```

## Disaster Recovery

### Multi-Region Setup

```python
class MultiRegionLanceDB:
    """Multi-region deployment for disaster recovery."""

    def __init__(self, primary_region: str, dr_region: str, bucket_name: str):
        self.primary = lancedb.connect(
            f"s3://{bucket_name}-{primary_region}/lancedb",
            storage_options={"aws_region": primary_region}
        )
        self.dr = lancedb.connect(
            f"s3://{bucket_name}-{dr_region}/lancedb",
            storage_options={"aws_region": dr_region}
        )
        self.active = self.primary

    def failover_to_dr(self):
        """Switch to DR region."""
        self.active = self.dr
        print(f"Failover complete - now using DR region")

    def failback_to_primary(self):
        """Switch back to primary region."""
        self.active = self.primary
        print(f"Failback complete - now using primary region")

    def get_connection(self):
        return self.active
```

## Summary

In this chapter, you've learned:

- **Cloud Storage**: S3, GCS, and Azure backends
- **Architectures**: Single instance, shared storage, read replicas
- **Kubernetes**: Deployment manifests and service accounts
- **Monitoring**: Health checks, Prometheus metrics, logging
- **Backup**: Backup strategies and point-in-time recovery
- **Security**: Access control and encryption
- **DR**: Multi-region disaster recovery

## Key Takeaways

1. **Use Cloud Storage**: S3/GCS/Azure for production
2. **Monitor Everything**: Health checks, metrics, logs
3. **Plan for Failure**: Backup and DR strategies
4. **Secure by Default**: IAM, encryption, access control
5. **Scale Horizontally**: Multiple instances with shared storage

## Next Steps

Now that you can deploy to production, let's explore Advanced Patterns in Chapter 8 for multi-tenancy, versioning, and RAG systems.

---

**Ready for Chapter 8?** [Advanced Patterns](08-advanced-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `lancedb`, `table`, `bucket` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Production Deployment` as an operating subsystem inside **LanceDB Tutorial: Serverless Vector Database for AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `self`, `connect`, `time` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `lancedb`.
2. **Input normalization**: shape incoming data so `table` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `bucket`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `lancedb` and `table` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Performance](06-performance.md)
- [Next Chapter: Chapter 8: Advanced Patterns](08-advanced-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
