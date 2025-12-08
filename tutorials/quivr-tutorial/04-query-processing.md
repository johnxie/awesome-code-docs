---
layout: default
title: "Chapter 4: Query Processing"
parent: "Quivr Tutorial"
nav_order: 4
---

# Chapter 4: Query Processing

Enhance user queries, retrieve relevant chunks, and prepare context for the LLM.

## Objectives
- Normalize and expand queries
- Retrieve top-k chunks
- Build prompts with citations

## Retrieval
```python
query = "How does access control work?"
q_emb = model.encode([query]).tolist()
res = collection.query(query_embeddings=q_emb, n_results=5)
context = res["documents"][0]
```

## Prompt Assembly
```python
def build_prompt(question, context):
    joined = "\n\n".join(context)
    return f"Answer using the context. Cite sources.\n\nContext:\n{joined}\n\nQuestion: {question}\nAnswer:" 
```

## Query Expansion Ideas
- Add synonyms/keywords
- Rephrase as declarative statement for better retrieval

## Troubleshooting
- Irrelevant results: tune chunk size/overlap; increase k; add filters
- Long prompts: trim context to token budget

## Next Steps
Chapter 5 organizes documents into knowledge bases.
