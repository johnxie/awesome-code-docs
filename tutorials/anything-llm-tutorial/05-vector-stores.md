---
layout: default
title: "AnythingLLM Tutorial - Chapter 5: Vector Stores"
nav_order: 5
has_children: false
parent: AnythingLLM Tutorial
---

# Chapter 5: Vector Stores - Choosing and Configuring Storage Backends

Welcome to **Chapter 5: Vector Stores - Choosing and Configuring Storage Backends**. In this part of **AnythingLLM Tutorial: Self-Hosted RAG and Agents Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Select and configure vector databases for optimal semantic search performance.

## Overview

Vector stores are the foundation of semantic search in AnythingLLM. This chapter covers the different vector database options, their configuration, and optimization strategies for different use cases.

## Supported Vector Stores

### LanceDB (Built-in)

```bash
# Default choice - works out of the box
# Excellent for getting started and small deployments
# Stores vectors locally in Docker volume

# Pros:
# - No additional setup required
# - Fast for small to medium datasets
# - Built-in to AnythingLLM
# - Good default similarity search

# Cons:
# - Not distributed (single instance)
# - Limited to local storage
# - May be slow for very large datasets

# Configuration (automatic):
# - Storage: /app/server/storage/lancedb
# - No additional settings needed
```

### Chroma

```bash
# Self-hosted vector database
# Good for development and small teams
# Supports distributed deployment

# Installation:
docker run -d \
  -p 8000:8000 \
  --name chroma \
  -v chroma-data:/chroma/chroma \
  chromadb/chroma

# Configuration in AnythingLLM:
# Settings > Vector Database > Chroma
# - Host: http://host.docker.internal:8000
# - SSL: false (unless configured)

# Advanced settings:
# - Collection: anythingllm  (default)
# - Chunk Size: 1000
# - Overlap: 200
```

```yaml
# Docker Compose setup
version: '3.8'
services:
  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000

volumes:
  chroma_data:
```

### Pinecone

```bash
# Cloud-native vector database
# Excellent for production and large-scale deployments
# Managed service with high availability

# Sign up at pinecone.io
# Create project and index

# Configuration in AnythingLLM:
# Settings > Vector Database > Pinecone
# - API Key: your-pinecone-api-key
# - Index Name: anythingllm-index
# - Environment: us-east1-gcp (or your region)
# - Project ID: your-project-id

# Index settings (create in Pinecone console):
# - Dimension: 1536 (for OpenAI embeddings) or 768 (for local)
# - Metric: cosine
# - Pod Type: p1 (starter) or s1 (production)
```

### Weaviate

```bash
# Graph-based vector database
# Supports complex queries and relationships
# Good for knowledge graphs and structured data

# Installation:
docker run -d \
  -p 8080:8080 \
  --name weaviate \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  semitechnologies/weaviate:latest

# Configuration in AnythingLLM:
# Settings > Vector Database > Weaviate
# - Host: http://host.docker.internal:8080
# - API Key: (leave blank for anonymous)
# - Class Name: AnythingLLM

# Schema configuration:
# Weaviate will auto-create schema based on your data
```

### Qdrant

```bash
# High-performance vector database
# Excellent for large-scale semantic search
# Supports distributed deployment

# Installation:
docker run -d \
  -p 6333:6333 \
  -p 6334:6334 \
  -v qdrant_data:/qdrant/storage \
  qdrant/qdrant

# Configuration in AnythingLLM:
# Settings > Vector Database > Qdrant
# - Host: http://host.docker.internal:6333
# - API Key: (optional)
# - Collection: anythingllm

# Collection settings:
# - Vector size: 1536 (matches embedding model)
# - Distance: Cosine
# - Replication factor: 1 (single node)
```

## Vector Store Selection Guide

### By Use Case

```yaml
# Getting Started / Small Projects
Best: LanceDB (built-in)
Good: Chroma
Why: Zero configuration, works immediately

# Development / Small Teams
Best: Chroma
Good: LanceDB, Weaviate
Why: Easy setup, good performance, development-friendly

# Production / Enterprise
Best: Pinecone, Qdrant
Good: Weaviate
Why: Scalable, reliable, managed services

# Large Datasets (>1M vectors)
Best: Pinecone, Qdrant
Good: Weaviate (distributed)
Why: Optimized for scale, distributed architecture

# Complex Queries / Knowledge Graphs
Best: Weaviate
Good: Qdrant (with filtering)
Why: Graph capabilities, rich query language

# Cost Sensitive
Best: LanceDB, Chroma
Good: Self-hosted options
Why: No cloud costs, local storage
```

### By Performance Characteristics

```yaml
# Fastest Queries
- Qdrant: Optimized for speed
- Pinecone: Cloud performance
- Chroma: Good for development

# Highest Accuracy
- Pinecone: Advanced indexing
- Weaviate: Rich similarity measures
- Qdrant: Multiple distance metrics

# Best Scaling
- Pinecone: Serverless scaling
- Qdrant: Distributed clustering
- Weaviate: Horizontal scaling

# Lowest Latency
- Qdrant: In-memory operations
- Pinecone: Global CDN
- Chroma: Local deployment
```

### By Cost

```yaml
# Free / Self-hosted
- LanceDB: Completely free
- Chroma: Free, self-hosted
- Weaviate: Free community edition
- Qdrant: Free community edition

# Paid / Cloud
- Pinecone: $0.10/GB/month + query costs
- Qdrant Cloud: $0.05/GB/month
- Weaviate Cloud: Custom pricing
```

## Configuration and Optimization

### Embedding Model Compatibility

```yaml
# Match vector dimensions to embedding model

# OpenAI text-embedding-3-small: 1536 dimensions
# OpenAI text-embedding-ada-002: 1536 dimensions
# OpenAI text-embedding-3-large: 3072 dimensions

# Local models (sentence-transformers):
# all-MiniLM-L6-v2: 384 dimensions
# all-mpnet-base-v2: 768 dimensions

# Anthropic (if using embeddings): 1024 dimensions

# Configuration example:
vector_store:
  type: "pinecone"
  dimensions: 1536  # Must match embedding model
  metric: "cosine"
  index_name: "anythingllm-docs"
```

### Index Optimization

```yaml
# Optimize indexes for your use case

# For accuracy (slower, more accurate):
index_optimization:
  ef_construction: 200  # Higher = more accurate but slower builds
  m: 16                 # Higher = more accurate but more memory

# For speed (faster, slightly less accurate):
index_optimization:
  ef_construction: 100
  m: 8

# For memory efficiency:
index_optimization:
  ef_construction: 128
  m: 12
```

### Chunking Strategy

```yaml
# Different chunking for different content types

# Code files:
chunking:
  strategy: semantic
  size: 500
  overlap: 50
  separators: ["\nclass ", "\ndef ", "\n    def "]

# Documentation:
chunking:
  strategy: sentence
  size: 1000
  overlap: 200
  separators: [". ", "! ", "? ", "\n\n"]

# Long documents (research papers):
chunking:
  strategy: paragraph
  size: 1500
  overlap: 300
  separators: ["\n\n", "\n"]
```

## Performance Tuning

### Query Optimization

```yaml
# Optimize similarity search

# Search parameters:
similarity_search:
  top_k: 5              # Number of results to return
  score_threshold: 0.7  # Minimum similarity score
  ef_search: 64         # Search parameter (higher = more accurate but slower)

# For speed (reduce ef_search):
similarity_search:
  top_k: 5
  ef_search: 32

# For accuracy (increase ef_search):
similarity_search:
  top_k: 5
  ef_search: 128
```

### Caching Strategies

```yaml
# Vector cache for frequently accessed documents
vector_cache:
  enabled: true
  size_mb: 512
  ttl_hours: 24

# Query result cache
query_cache:
  enabled: true
  size_mb: 256
  ttl_minutes: 60

# Embedding cache (avoid re-embedding unchanged content)
embedding_cache:
  enabled: true
  persist_to_disk: true
```

### Batch Operations

```yaml
# Optimize bulk operations

# Batch embedding:
embedding_batch:
  size: 100
  concurrency: 4

# Batch indexing:
indexing_batch:
  size: 1000
  concurrency: 2

# Bulk queries:
bulk_query:
  max_queries: 10
  concurrency: 3
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check vector store health
curl http://localhost:3001/api/v1/system/health \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response includes vector store status:
{
  "vector_store": {
    "status": "healthy",
    "connection": "connected",
    "index_count": 5,
    "vector_count": 125000
  }
}
```

### Performance Metrics

```bash
# Monitor vector store performance
curl http://localhost:3001/api/v1/analytics/vector-store \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
{
  "query_performance": {
    "avg_query_time_ms": 45,
    "queries_per_second": 22,
    "cache_hit_rate": 0.85
  },
  "storage_metrics": {
    "total_vectors": 125000,
    "index_size_mb": 450,
    "memory_usage_mb": 1200
  },
  "error_rates": {
    "connection_errors": 0.001,
    "query_errors": 0.005
  }
}
```

### Maintenance Tasks

```bash
# Regular maintenance

# 1. Index optimization
curl -X POST http://localhost:3001/api/v1/admin/vector-store/optimize \
  -H "Authorization: Bearer YOUR_API_KEY"

# 2. Cache cleanup
curl -X POST http://localhost:3001/api/v1/admin/cache/cleanup \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. Backup vectors
curl -X GET http://localhost:3001/api/v1/admin/vector-store/backup \
  -H "Authorization: Bearer YOUR_API_KEY" \
  --output vector-backup.tar.gz

# 4. Rebuild indexes (if corrupted)
curl -X POST http://localhost:3001/api/v1/admin/vector-store/rebuild \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Backup and Recovery

### Vector Store Backup

```bash
# Backup strategies by vector store type

# LanceDB (file-based):
docker exec anythingllm tar czf /tmp/lancedb-backup.tar.gz /app/server/storage/lancedb
docker cp anythingllm:/tmp/lancedb-backup.tar.gz ./backups/

# Chroma:
docker exec chroma tar czf /tmp/chroma-backup.tar.gz /chroma/chroma
docker cp chroma:/tmp/chroma-backup.tar.gz ./backups/

# Pinecone (cloud):
# Automatic replication, no manual backup needed
# Use API to export data if required

# Qdrant:
curl -X POST http://localhost:6333/collections/anythingllm/snapshots \
  -H "Content-Type: application/json" \
  -d '{}' > snapshot-info.json
```

### Recovery Procedures

```bash
# Restore from backup

# LanceDB:
docker cp ./backups/lancedb-backup.tar.gz anythingllm:/tmp/
docker exec anythingllm tar xzf /tmp/lancedb-backup.tar.gz -C /

# Chroma:
docker cp ./backups/chroma-backup.tar.gz chroma:/tmp/
docker exec chroma tar xzf /tmp/chroma-backup.tar.gz -C /

# Trigger reindexing:
curl -X POST http://localhost:3001/api/v1/admin/vector-store/reindex \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Migration Between Vector Stores

### Export/Import Process

```bash
# Step 1: Export from current store
curl -X GET http://localhost:3001/api/v1/admin/vector-store/export \
  -H "Authorization: Bearer YOUR_API_KEY" \
  --output vectors-export.json

# Step 2: Configure new vector store in UI
# Settings > Vector Database > [New Store]

# Step 3: Import to new store
curl -X POST http://localhost:3001/api/v1/admin/vector-store/import \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @vectors-export.json

# Step 4: Verify import
curl http://localhost:3001/api/v1/system/health \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Zero-Downtime Migration

```yaml
# Advanced migration with zero downtime

# 1. Set up new vector store alongside existing
# 2. Configure dual writing (write to both stores)
# 3. Gradually migrate read operations
# 4. Remove old store after full migration

dual_writing:
  enabled: true
  primary_store: "pinecone"
  secondary_store: "qdrant"
  read_from_primary: true
  migration_progress: 0.0  # 0.0 to 1.0

# Gradual migration:
# - Start with 10% traffic to new store
# - Monitor performance and accuracy
# - Increase traffic gradually
# - Complete migration when confident
```

## Advanced Features

### Hybrid Search

```yaml
# Combine semantic and keyword search
hybrid_search:
  enabled: true
  semantic_weight: 0.7
  keyword_weight: 0.3
  rerank_results: true

# Benefits:
# - Better precision for exact matches
# - Improved recall for related concepts
# - Handles both specific queries and general questions
```

### Metadata Filtering

```yaml
# Filter results by metadata
metadata_filters:
  enabled: true
  supported_fields:
    - "document_type"
    - "author"
    - "date_created"
    - "tags"

# Usage in queries:
# "Find API documentation created after 2024-01-01"
# Automatically filters by metadata before vector search
```

### Multi-Index Support

```yaml
# Multiple indexes for different content types
multi_index:
  enabled: true
  indexes:
    - name: "code"
      content_types: ["py", "js", "java"]
      embedding_model: "code-search-embeddings"
    - name: "docs"
      content_types: ["md", "txt", "pdf"]
      embedding_model: "text-embedding-ada-002"
    - name: "data"
      content_types: ["csv", "json"]
      embedding_model: "text-embedding-3-small"

# Automatically route queries to appropriate index
# Improves relevance for specialized content
```

## Troubleshooting

### Common Issues

```bash
# Connection failed
# - Check network connectivity
# - Verify host/port settings
# - Check authentication credentials

curl -f http://localhost:8000/api/v1/heartbeat  # Chroma health check
curl -f http://localhost:6333/health             # Qdrant health check

# Slow queries
# - Increase ef_search parameter
# - Check index optimization
# - Monitor resource usage
# - Consider upgrading instance size

# Out of memory
# - Reduce batch sizes
# - Increase server memory
# - Optimize index parameters
# - Use disk-based storage for large datasets

# Index corruption
# - Rebuild index from documents
# - Restore from backup
# - Check disk space and permissions
```

### Performance Debugging

```bash
# Enable detailed logging
export VECTOR_STORE_LOG_LEVEL=debug

# Monitor query performance
curl http://localhost:3001/api/v1/debug/query-performance \
  -H "Authorization: Bearer YOUR_API_KEY"

# Analyze slow queries
# - Check embedding generation time
# - Monitor vector search time
# - Review result post-processing
```

## Summary

In this chapter, we've covered:

- **Vector Store Options**: LanceDB, Chroma, Pinecone, Weaviate, Qdrant
- **Selection Guide**: Choosing the right store for your use case
- **Configuration**: Setting up and optimizing vector stores
- **Performance Tuning**: Query optimization, caching, and batching
- **Monitoring**: Health checks and performance metrics
- **Maintenance**: Backup, recovery, and migration
- **Advanced Features**: Hybrid search, metadata filtering, multi-index
- **Troubleshooting**: Common issues and debugging techniques

## Key Takeaways

1. **Right Tool for the Job**: Choose vector store based on scale, cost, and requirements
2. **Configuration Matters**: Match dimensions and optimize for your use case
3. **Performance Tuning**: Balance speed, accuracy, and resource usage
4. **Monitoring**: Track health and performance regularly
5. **Backup Strategy**: Implement regular backups and recovery procedures
6. **Scalability**: Plan for growth and migration needs
7. **Hybrid Approaches**: Combine multiple techniques for best results

## Next Steps

Now that you understand vector stores, let's explore **agents** and how to add intelligent capabilities to your AnythingLLM instance.

---

**Ready for Chapter 6?** [Agents](06-agents.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `vector`, `chroma`, `http` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Vector Stores - Choosing and Configuring Storage Backends` as an operating subsystem inside **AnythingLLM Tutorial: Self-Hosted RAG and Agents Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `store`, `docker`, `curl` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Vector Stores - Choosing and Configuring Storage Backends` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `vector`.
2. **Input normalization**: shape incoming data so `chroma` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `http`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [AnythingLLM Repository](https://github.com/Mintplex-Labs/anything-llm)
  Why it matters: authoritative reference on `AnythingLLM Repository` (github.com).
- [AnythingLLM Releases](https://github.com/Mintplex-Labs/anything-llm/releases)
  Why it matters: authoritative reference on `AnythingLLM Releases` (github.com).
- [AnythingLLM Docs](https://docs.anythingllm.com/)
  Why it matters: authoritative reference on `AnythingLLM Docs` (docs.anythingllm.com).
- [AnythingLLM Website](https://anythingllm.com/)
  Why it matters: authoritative reference on `AnythingLLM Website` (anythingllm.com).

Suggested trace strategy:
- search upstream code for `vector` and `chroma` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: LLM Configuration - Connecting Language Models](04-llm-config.md)
- [Next Chapter: Chapter 6: Agents - Intelligent Capabilities and Automation](06-agents.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
