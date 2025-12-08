---
layout: default
title: "Semantic Kernel Tutorial - Chapter 5: Memory & Embeddings"
nav_order: 5
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 5: Memory & Embeddings

> Add semantic memory with vector stores, embeddings, and grounded retrieval.

## Setting Up Text Memory (Python)

```python
import semantic_kernel as sk
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.memory import SemanticTextMemory


memory = SemanticTextMemory(
    storage=ChromaMemoryStore(persist_directory="./memory"),
    embeddings_generator=OpenAITextEmbedding(model_id="text-embedding-3-small"),
)

# If your app wires memory into a kernel instance, store it there.
# kernel = sk.Kernel()
# kernel.memory = memory
```

## Save & Search

```python
# Save information
await memory.save_information(
    collection="docs",
    id="sk-overview",
    text="Semantic Kernel is Microsoft's SDK for AI orchestration.",
    description="SK overview",
)

# Semantic search
results = await memory.search(
    collection="docs",
    query="What is Semantic Kernel?",
    limit=3,
)

for r in results:
    print(r.text, r.relevance)
```

## Using Memory in Prompts

```python
context = "\n".join([r.text for r in results])

response = await kernel.invoke(
    some_function,
    context=context,
    question="How do I add plugins?",
)
```

## Alternative Stores

- **Qdrant**: `from semantic_kernel.connectors.memory.qdrant import QdrantMemoryStore`
- **Pinecone**: `from semantic_kernel.connectors.memory.pinecone import PineconeMemoryStore`
- **Azure Cognitive Search**: Use search connector + embeddings.

Switch storage by replacing the `storage` implementation; keep the same `SemanticTextMemory` API.

## Chunking & Ingestion Tips

- Use **adaptive chunking** (by headings/paragraphs) for higher recall.
- Store **source metadata** (id, url, tags) to filter later.
- Normalize text (lowercase, strip boilerplate) before embedding for consistency.
- Re-embed when changing models to keep vector quality consistent.

## Caching & Persistence

- Enable on-disk persistence for Chroma (`persist_directory`) or use managed vector DBs (Pinecone/Qdrant Cloud).
- Cache embeddings for repeated content; dedupe by hash.

## Checklist

- [ ] Configure `SemanticTextMemory` with an embeddings generator
- [ ] Persist vectors locally or in a managed store
- [ ] Store metadata for filtering
- [ ] Integrate retrieval results into prompts
- [ ] Add tests for save/search flows

Next: **[Chapter 6: Planners](06-planners.md)** to automate multi-step tasks. 📋
