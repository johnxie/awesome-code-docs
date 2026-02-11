---
layout: default
title: "Chapter 3: Embeddings and Search"
nav_order: 3
parent: OpenAI Python SDK Tutorial
---

# Chapter 3: Embeddings and Search

Embeddings convert text into vectors so you can perform semantic retrieval for RAG and search.

## Create Embeddings

```python
from openai import OpenAI

client = OpenAI()

texts = [
    "How to rotate API keys safely",
    "Rate limits and retry policies",
    "How to design a deployment checklist",
]

emb = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)

vectors = [row.embedding for row in emb.data]
print(len(vectors), len(vectors[0]))
```

## Simple Similarity Search

```python
import math
from openai import OpenAI


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-12)

client = OpenAI()

docs = [
    "Use exponential backoff for transient failures",
    "Store credentials in env vars and rotate them",
    "Benchmark latency and tail percentiles",
]

query = "How should I handle temporary API errors?"

all_vectors = client.embeddings.create(model="text-embedding-3-small", input=docs + [query]).data

doc_vectors = [x.embedding for x in all_vectors[:-1]]
query_vec = all_vectors[-1].embedding

scores = [(i, cosine(query_vec, dv)) for i, dv in enumerate(doc_vectors)]
for i, s in sorted(scores, key=lambda t: t[1], reverse=True):
    print(round(s, 4), docs[i])
```

## Retrieval Pipeline Notes

- Chunk by meaning, not fixed bytes only.
- Store metadata (source, timestamp, section).
- Re-rank top candidates when quality matters.
- Track retrieval hit quality over time.

## Troubleshooting

| Issue | Cause | Fix |
|:------|:------|:----|
| Poor matches | Bad chunking or noisy docs | Improve segmentation and cleaning |
| High cost | Embedding everything repeatedly | Cache vectors and incremental updates |
| Slow retrieval | No ANN index | Use a vector DB or optimized index |

## Summary

You can now generate embeddings and implement semantic retrieval.

Next: [Chapter 4: Assistants API](04-assistants-api.md)
