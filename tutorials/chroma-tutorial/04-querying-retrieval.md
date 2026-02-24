---
layout: default
title: "Chapter 4: Querying & Retrieval"
parent: "Chroma Tutorial"
nav_order: 4
---

# Chapter 4: Querying & Retrieval

Welcome to **Chapter 4: Querying & Retrieval**. In this part of **ChromaDB Tutorial: Building AI-Native Vector Databases**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Master the art of querying in Chroma! This chapter covers advanced querying techniques, metadata filtering, and retrieval strategies for building powerful search applications.

## Advanced Query Patterns

### Metadata Filtering

```python
# Query with metadata filters
results = collection.query(
    query_texts=["machine learning"],
    n_results=5,
    where={"category": "technology"}  # Simple equality filter
)

# Complex metadata filters
results = collection.query(
    query_texts=["python programming"],
    n_results=10,
    where={
        "$and": [
            {"difficulty": {"$in": ["beginner", "intermediate"]}},
            {"category": "programming"},
            {"rating": {"$gte": 4.0}}
        ]
    }
)

# Nested metadata queries
results = collection.query(
    query_texts=["web development"],
    where={
        "tags": {"$in": ["react", "javascript"]},
        "metadata.published": {"$eq": True}
    }
)
```

### Multi-Modal Queries

```python
# Combine text and metadata filters
hybrid_results = collection.query(
    query_texts=["artificial intelligence"],
    n_results=5,
    where={
        "category": "AI",
        "year": {"$gte": 2020}
    },
    include=["documents", "metadatas", "distances"]
)

# Temporal queries
recent_results = collection.query(
    query_texts=["latest developments"],
    where={
        "created_at": {"$gte": "2024-01-01"}
    }
)
```

## Retrieval Strategies

### Re-Ranking

```python
def rerank_results(query, initial_results, rerank_model):
    """Re-rank results using a more sophisticated model"""

    # Extract documents and scores
    documents = initial_results['documents'][0]
    scores = initial_results['distances'][0]

    # Create reranking input
    rerank_input = []
    for doc in documents:
        rerank_input.append(f"Query: {query} Document: {doc}")

    # Get reranking scores
    rerank_scores = rerank_model.predict(rerank_input)

    # Combine with original scores
    combined_scores = []
    for i, (orig_score, rerank_score) in enumerate(zip(scores, rerank_scores)):
        combined_score = 0.7 * orig_score + 0.3 * rerank_score
        combined_scores.append((i, combined_score))

    # Sort by combined score
    combined_scores.sort(key=lambda x: x[1])

    # Reorder results
    reranked_documents = [documents[i] for i, _ in combined_scores]

    return reranked_documents

# Usage
results = collection.query(query_texts=["complex query"], n_results=20)
reranked = rerank_results("complex query", results, rerank_model)
```

### Query Expansion

```python
def expand_query(original_query, expansion_model):
    """Expand query with synonyms and related terms"""

    # Generate expanded terms
    expanded_terms = expansion_model.generate_synonyms(original_query)

    # Create expanded queries
    expanded_queries = [original_query] + expanded_terms[:3]  # Limit expansion

    return expanded_queries

# Multi-query approach
expanded_queries = expand_query("machine learning", expansion_model)
results = collection.query(
    query_texts=expanded_queries,
    n_results=5
)

# Combine results from multiple queries
all_docs = []
for docs in results['documents']:
    all_docs.extend(docs)

# Remove duplicates and rerank
unique_docs = list(set(all_docs))
```

## Performance Optimization

### Query Optimization

```python
# Optimize query performance
optimized_results = collection.query(
    query_texts=["optimization techniques"],
    n_results=10,
    # Use efficient search parameters
    search_params={
        "ef": 64,  # Search quality parameter
        "k": 10    # Number of results
    }
)

# Batch queries for better performance
batch_queries = [
    "machine learning",
    "artificial intelligence",
    "data science",
    "neural networks"
]

batch_results = collection.query(
    query_texts=batch_queries,
    n_results=5
)
```

## What We've Accomplished

This chapter covered advanced querying and retrieval techniques in Chroma, including metadata filtering, re-ranking, query expansion, and performance optimization.

## Next Steps

Ready for metadata mastery? In [Chapter 5: Metadata & Filtering](05-metadata-filtering.md), we'll dive deep into advanced metadata strategies and complex filtering patterns.

---

**Practice what you've learned:**
1. Implement complex metadata filters
2. Build a re-ranking system
3. Create query expansion functionality
4. Optimize query performance for your use case

*How will you enhance your search capabilities?* 🔍

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `query`, `results`, `collection` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Querying & Retrieval` as an operating subsystem inside **ChromaDB Tutorial: Building AI-Native Vector Databases**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `query_texts`, `n_results`, `documents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Querying & Retrieval` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `query`.
2. **Input normalization**: shape incoming data so `results` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `collection`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/chroma-core/chroma)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `query` and `results` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Embeddings & Indexing](03-embeddings-indexing.md)
- [Next Chapter: Chapter 5: Metadata & Filtering](05-metadata-filtering.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
