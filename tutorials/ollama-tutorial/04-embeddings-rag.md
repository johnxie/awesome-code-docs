---
layout: default
title: "Ollama Tutorial - Chapter 4: Embeddings & RAG"
nav_order: 4
has_children: false
parent: Ollama Tutorial
---

# Chapter 4: Embeddings and RAG with Ollama

> Create vector embeddings locally and build retrieval-augmented generation (RAG) workflows.

## Embeddings Endpoint

Ollama exposes an embeddings API compatible with OpenAI.

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "An embedding turns text into a vector."
}'
```

Python:
```python
import requests
r = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "nomic-embed-text",
    "prompt": "Searchable vector"
})
vec = r.json()["embedding"]
print(len(vec), vec[:5])
```

Node (OpenAI client):
```javascript
import OpenAI from "openai";
const client = new OpenAI({ baseURL: "http://localhost:11434/v1", apiKey: "ollama" });
const emb = await client.embeddings.create({
  model: "nomic-embed-text",
  input: "Vectorize this text"
});
console.log(emb.data[0].embedding.length);
```

## Recommended Embedding Models
- `nomic-embed-text` (fast, high quality)
- `all-minilm` variants (small, quick)
- `bge` models (high quality, larger)

Pull example:
```bash
ollama pull nomic-embed-text
```

## Simple RAG Pipeline (Python + Chroma)

Install deps:
```bash
pip install chromadb requests tiktoken
```

Index documents:
```python
import chromadb, requests, uuid
client = chromadb.Client()
collection = client.create_collection("docs")

texts = ["Ollama runs LLMs locally.", "RAG combines retrieval + generation."]
for t in texts:
    r = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "nomic-embed-text",
        "prompt": t
    })
    emb = r.json()["embedding"]
    collection.add(ids=[str(uuid.uuid4())], embeddings=[emb], documents=[t])
```

Query with context:
```python
question = "What is RAG?"
q = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "nomic-embed-text",
    "prompt": question
}).json()["embedding"]

results = collection.query(query_embeddings=[q], n_results=3)
context = "\n".join(results["documents"][0])

answer = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3",
    "messages": [
        {"role": "system", "content": "Use the provided context to answer."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
}).json()["message"]["content"]
print(answer)
```

## Retrieval Patterns

- **Top-k search**: adjust `n_results`
- **Hybrid search**: combine keyword filter + embeddings
- **Chunking**: split long docs (e.g., 300-800 tokens with overlap)
- **Caching**: store embeddings on disk (Chroma persistent client or other DB)

## Performance Tips

- Use smaller embed models for speed (MiniLM) when quality is sufficient
- Batch requests client-side to avoid repeated HTTP overhead
- Keep context windows reasonable (`num_ctx` aligns with your generator model)

## Troubleshooting

- **Dimension mismatch**: ensure same embedding model for index and queries
- **Slow queries**: use smaller vectors/models; persist DB; avoid huge top-k
- **Relevance low**: better chunking; higher-quality embed model; clean text

Next: craft custom models with Modelfiles, adapters, and prompt templates.
