---
layout: default
title: "Chapter 8: Production Deployment"
parent: "Quivr Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Deploy Quivr securely with observability, scaling, and cost controls.

## Objectives
- Containerize and deploy
- Secure auth and data
- Monitor performance and cost

## Deploy (Docker Compose sketch)
```yaml
services:
  api:
    image: quivr/api:latest
    env_file: .env
    depends_on: [db, vectordb]
  db:
    image: postgres:15
  vectordb:
    image: chromadb/chroma:latest
```

## Security
- HTTPS termination; WAF if public
- Per-tenant keys; rate limits per token
- Encrypt at rest for DB/object storage

## Observability
- Metrics: ingest success, query latency, embedding queue depth
- Logs: structured JSON; include kb, user, latency
- Alerts: 5xx rate, slow queries, storage nearing limits

## Cost Controls
- Limit file size and pages per upload
- Cache embeddings; avoid re-embedding unchanged docs
- Use smaller models where acceptable

## Troubleshooting
- Slow queries: add HNSW index; lower top_k
- Memory pressure: cap concurrent ingest; batch embedding
- Access issues: verify token scopes and tenant mapping

## Go-Live Checklist
- [ ] TLS and auth configured
- [ ] Backups for DB/vector store
- [ ] Alerts and dashboards live
- [ ] Load test completed

## Next Steps
Iterate on reranking quality and user feedback loops.
