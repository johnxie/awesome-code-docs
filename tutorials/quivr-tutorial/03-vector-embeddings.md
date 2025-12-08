---
layout: default
title: "Chapter 3: Vector Embeddings"
parent: "Quivr Tutorial"
nav_order: 3
---

# Chapter 3: Vector Embeddings

Generate embeddings for your chunks and store them in a vector database.

## Objectives
- Choose an embedding model
- Batch encode chunks
- Persist to a vector store

## Encode with SentenceTransformers
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, show_progress_bar=True)
```

## Store in Chroma
```python
from chromadb import Client

client = Client()
collection = client.create_collection("quivr-docs")
ids = [f"doc-{i}" for i in range(len(chunks))]
collection.add(ids=ids, documents=chunks, embeddings=embeddings.tolist())
```

## Tips
- Batch size 32–64 for throughput
- Normalize text before embedding

## Troubleshooting
- OOM: reduce batch size
- Slow encode: use GPU model or smaller model

## Next Steps
In Chapter 4, build query processing and retrieval.
