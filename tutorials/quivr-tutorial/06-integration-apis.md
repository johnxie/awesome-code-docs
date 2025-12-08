---
layout: default
title: "Chapter 6: Integration APIs"
parent: "Quivr Tutorial"
nav_order: 6
---

# Chapter 6: Integration APIs

Expose Quivr capabilities to external apps via REST or GraphQL.

## Objectives
- Use Quivr APIs to ingest and query
- Secure API access
- Stream responses to clients

## Example Ingest (REST)
```bash
curl -X POST https://api.quivr.local/ingest \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@docs/report.pdf" \
  -F "kb=engineering-handbook"
```

## Example Query (REST)
```bash
curl -X POST https://api.quivr.local/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"kb": "engineering-handbook", "query": "How do we deploy?", "top_k": 4}'
```

## Streaming Responses
- Use SSE/websocket endpoints to stream partial answers
- Show citations progressively

## Security
- Bearer tokens per user/workspace
- Rate limit by token; log queries

## Troubleshooting
- 401/403: verify token scope; check workspace ownership
- Slow responses: reduce top_k; cache embeddings

## Next Steps
Chapter 7 focuses on customization and pipelines.
