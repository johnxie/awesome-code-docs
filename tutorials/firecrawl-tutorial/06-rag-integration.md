---
layout: default
title: "Chapter 6: Building RAG Systems"
parent: "Firecrawl Tutorial"
nav_order: 6
---

# Chapter 6: Building RAG Systems

Connect Firecrawl outputs to vector databases and build retrieval-augmented generation pipelines.

## Objectives
- Chunk cleaned content effectively
- Generate embeddings and store in a vector DB
- Build retrieval pipelines for Q&A
- Measure latency, relevance, and cost

## Chunking Strategy (Python)
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    separators=["\n\n", "\n", ". ", " "],
)

chunks = splitter.split_text(clean_markdown)
print(len(chunks), "chunks")
```

## Store in Chroma
```python
from chromadb import Client
from sentence_transformers import SentenceTransformer

client = Client()
collection = client.create_collection("firecrawl-docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks).tolist()
ids = [f"doc-{i}" for i in range(len(chunks))]
collection.add(ids=ids, documents=chunks, embeddings=embeddings)
```

## Retrieval and QA
```python
query = "How does the site handle JavaScript rendering?"
q_emb = model.encode([query]).tolist()
results = collection.query(query_embeddings=q_emb, n_results=4)
for doc in results["documents"][0]:
    print(doc[:200], "...\n")
```

## Metrics
- Latency: embedding + retrieval + generation
- Relevance: simple manual eval or LLM-as-judge on sampled queries
- Cost: track tokens for downstream LLM calls

## Troubleshooting
- Low relevance: adjust chunk size/overlap; add metadata filters
- Slow queries: add HNSW index; reduce embedding dimensionality
- Hallucinations: increase retrieved k; add citations in prompts

## Performance Notes
- Pre-compute embeddings offline
- Use batching for embedding generation
- Persist vector stores to disk or remote backend

## Security Notes
- Filter sensitive content before embedding
- Obey robots/terms for stored content

## Next Steps
Proceed to Chapter 7 to scale scraping and RAG pipelines for production loads.
