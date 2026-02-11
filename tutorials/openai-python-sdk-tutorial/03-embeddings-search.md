---
layout: default
title: "Chapter 3: Embeddings and Search"
nav_order: 3
parent: OpenAI Python SDK Tutorial
---

# Chapter 3: Embeddings and Search

Embeddings power retrieval quality in most production RAG systems.

## Create Embeddings

```python
from openai import OpenAI

client = OpenAI()

docs = [
    "Retry transient failures with exponential backoff.",
    "Use idempotency keys for side-effecting writes.",
    "Track p95 and p99 latency separately."
]

emb = client.embeddings.create(
    model="text-embedding-3-small",
    input=docs,
)

vectors = [row.embedding for row in emb.data]
print(len(vectors), len(vectors[0]))
```

## Retrieval Pipeline Blueprint

1. chunk source docs with semantic boundaries
2. generate embeddings and store vectors + metadata
3. retrieve top-k candidates by similarity
4. re-rank or filter by business constraints
5. pass compact context to generation layer

## Quality Controls

- maintain versioned chunking strategy
- keep source timestamps for freshness checks
- evaluate retrieval quality with labeled benchmark queries

## Summary

You now have the core pieces to build and evaluate a robust embeddings-backed retrieval system.

Next: [Chapter 4: Agents and Assistants](04-assistants-api.md)
