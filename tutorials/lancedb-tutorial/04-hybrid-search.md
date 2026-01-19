---
layout: default
title: "Chapter 4: Hybrid Search"
parent: "LanceDB Tutorial"
nav_order: 4
---

# Chapter 4: Hybrid Search

> Combine vector similarity search with full-text search and SQL filters for powerful retrieval systems.

## Overview

Hybrid search combines multiple retrieval strategies to improve search quality. This chapter covers LanceDB's full-text search capabilities, combining vector and keyword search, and building effective hybrid retrieval pipelines.

## Full-Text Search

### Creating Full-Text Index

```python
import lancedb

db = lancedb.connect("./my_lancedb")

# Create table with text content
data = [
    {"id": 1, "title": "Introduction to Machine Learning", "content": "Machine learning is a subset of AI..."},
    {"id": 2, "title": "Deep Learning Fundamentals", "content": "Deep learning uses neural networks..."},
    {"id": 3, "title": "Natural Language Processing", "content": "NLP deals with text and speech..."},
]
table = db.create_table("articles", data)

# Create full-text search index
table.create_fts_index("content")  # Index the content column

# Also index title
table.create_fts_index("title")
```

### Basic Full-Text Search

```python
# Search using full-text index
results = table.search("machine learning", query_type="fts") \
    .limit(10) \
    .to_pandas()

print(results)
# Returns: id, title, content, _score (BM25 score)
```

### Full-Text Search Options

```python
# Search specific column
results = table.search("neural networks") \
    .query_type("fts") \
    .fts_columns(["title", "content"]) \
    .limit(10) \
    .to_pandas()

# Boolean queries
results = table.search("machine AND learning") \
    .query_type("fts") \
    .limit(10) \
    .to_pandas()

# Phrase search
results = table.search('"deep learning"') \
    .query_type("fts") \
    .limit(10) \
    .to_pandas()

# Fuzzy search
results = table.search("machne~1") \  # Allows 1 edit distance
    .query_type("fts") \
    .limit(10) \
    .to_pandas()
```

## Hybrid Search Strategies

### Combined Vector + Full-Text

```python
import lancedb
import numpy as np

db = lancedb.connect("./my_lancedb")
table = db.open_table("articles")

# Query text
query_text = "machine learning basics"

# Get vector embedding (using your embedding function)
query_vector = embed_text(query_text)

# Hybrid search: combines vector and FTS
results = table.search(query_vector) \
    .query_type("hybrid") \  # Enable hybrid search
    .fts_query(query_text) \  # Add full-text query
    .limit(10) \
    .to_pandas()
```

### Weighted Hybrid Search

```python
def weighted_hybrid_search(
    table,
    query_text: str,
    query_vector: list,
    vector_weight: float = 0.5,
    fts_weight: float = 0.5,
    limit: int = 10
):
    """Perform weighted hybrid search."""

    # Get vector search results
    vector_results = table.search(query_vector) \
        .limit(limit * 2) \
        .to_list()

    # Get full-text search results
    fts_results = table.search(query_text, query_type="fts") \
        .limit(limit * 2) \
        .to_list()

    # Normalize and combine scores
    combined = {}

    # Process vector results
    if vector_results:
        max_dist = max(r['_distance'] for r in vector_results)
        for r in vector_results:
            item_id = r['id']
            # Convert distance to similarity score (0-1)
            vector_score = 1 - (r['_distance'] / max_dist if max_dist > 0 else 0)
            combined[item_id] = {
                'item': r,
                'vector_score': vector_score,
                'fts_score': 0
            }

    # Process FTS results
    if fts_results:
        max_score = max(r.get('_score', 0) for r in fts_results)
        for r in fts_results:
            item_id = r['id']
            fts_score = r.get('_score', 0) / max_score if max_score > 0 else 0

            if item_id in combined:
                combined[item_id]['fts_score'] = fts_score
            else:
                combined[item_id] = {
                    'item': r,
                    'vector_score': 0,
                    'fts_score': fts_score
                }

    # Calculate weighted scores
    for item_id in combined:
        combined[item_id]['final_score'] = (
            vector_weight * combined[item_id]['vector_score'] +
            fts_weight * combined[item_id]['fts_score']
        )

    # Sort by final score
    sorted_results = sorted(
        combined.values(),
        key=lambda x: x['final_score'],
        reverse=True
    )

    return [r['item'] for r in sorted_results[:limit]]

# Usage
results = weighted_hybrid_search(
    table,
    query_text="machine learning tutorial",
    query_vector=embed_text("machine learning tutorial"),
    vector_weight=0.7,
    fts_weight=0.3,
    limit=10
)
```

### Reciprocal Rank Fusion (RRF)

```python
def rrf_hybrid_search(
    table,
    query_text: str,
    query_vector: list,
    k: int = 60,
    limit: int = 10
):
    """Combine vector and FTS using Reciprocal Rank Fusion."""

    # Get vector search results
    vector_results = table.search(query_vector) \
        .limit(limit * 3) \
        .to_list()

    # Get full-text search results
    fts_results = table.search(query_text, query_type="fts") \
        .limit(limit * 3) \
        .to_list()

    # Calculate RRF scores
    scores = {}

    for rank, r in enumerate(vector_results):
        item_id = r['id']
        if item_id not in scores:
            scores[item_id] = {'item': r, 'score': 0}
        scores[item_id]['score'] += 1 / (k + rank + 1)

    for rank, r in enumerate(fts_results):
        item_id = r['id']
        if item_id not in scores:
            scores[item_id] = {'item': r, 'score': 0}
        scores[item_id]['score'] += 1 / (k + rank + 1)

    # Sort by RRF score
    sorted_results = sorted(
        scores.values(),
        key=lambda x: x['score'],
        reverse=True
    )

    return [r['item'] for r in sorted_results[:limit]]
```

## SQL Integration

### SQL Queries

```python
# Query table with SQL
results = db.execute_sql("""
    SELECT id, title, content
    FROM articles
    WHERE category = 'technology'
    ORDER BY created_at DESC
    LIMIT 100
""").to_pandas()
```

### Combining SQL with Vector Search

```python
# Vector search with SQL-like filters
results = table.search(query_vector) \
    .where("""
        category IN ('technology', 'science')
        AND published_at >= '2024-01-01'
        AND is_active = true
    """) \
    .limit(10) \
    .to_pandas()
```

### Complex Queries

```python
# Aggregations (via SQL)
stats = db.execute_sql("""
    SELECT
        category,
        COUNT(*) as count,
        AVG(view_count) as avg_views
    FROM articles
    GROUP BY category
    ORDER BY count DESC
""").to_pandas()

# Subqueries
results = db.execute_sql("""
    SELECT *
    FROM articles
    WHERE author_id IN (
        SELECT id FROM authors WHERE expertise = 'AI'
    )
    LIMIT 100
""").to_pandas()
```

## Multi-Stage Retrieval

### Two-Stage Retrieval

```python
def two_stage_retrieval(
    table,
    query_text: str,
    query_vector: list,
    first_stage_limit: int = 100,
    final_limit: int = 10
):
    """
    Stage 1: Fast vector search for candidates
    Stage 2: Rerank with cross-encoder or FTS boost
    """

    # Stage 1: Get candidates with vector search
    candidates = table.search(query_vector) \
        .limit(first_stage_limit) \
        .to_list()

    # Stage 2: Score candidates with multiple signals
    scored = []
    for item in candidates:
        # Vector similarity (convert distance to score)
        vector_score = 1 / (1 + item['_distance'])

        # Keyword match score
        title_match = query_text.lower() in item.get('title', '').lower()
        content_match = query_text.lower() in item.get('content', '').lower()
        keyword_score = 0.3 * title_match + 0.2 * content_match

        # Recency boost
        # recency_score = calculate_recency(item.get('created_at'))

        # Combined score
        final_score = vector_score + keyword_score
        scored.append((final_score, item))

    # Sort and return top results
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored[:final_limit]]
```

### Multi-Index Retrieval

```python
def multi_index_retrieval(
    db,
    query_text: str,
    query_vector: list,
    limit: int = 10
):
    """Search across multiple tables and combine results."""

    # Search different content types
    articles = db.open_table("articles").search(query_vector).limit(limit).to_list()
    docs = db.open_table("documents").search(query_vector).limit(limit).to_list()
    faqs = db.open_table("faqs").search(query_vector).limit(limit).to_list()

    # Tag results with source
    for r in articles:
        r['_source'] = 'articles'
    for r in docs:
        r['_source'] = 'documents'
    for r in faqs:
        r['_source'] = 'faqs'

    # Combine and sort
    all_results = articles + docs + faqs
    all_results.sort(key=lambda x: x['_distance'])

    return all_results[:limit]
```

## RAG Pipeline Integration

### Basic RAG Retrieval

```python
def rag_retrieve(
    table,
    query: str,
    embed_fn,
    top_k: int = 5
) -> list[str]:
    """Retrieve context for RAG."""

    query_vector = embed_fn(query)

    results = table.search(query_vector) \
        .limit(top_k) \
        .select(["content"]) \
        .to_list()

    return [r['content'] for r in results]

def rag_generate(query: str, context: list[str], llm) -> str:
    """Generate response using retrieved context."""

    context_text = "\n\n".join(context)

    prompt = f"""Based on the following context, answer the question.

Context:
{context_text}

Question: {query}

Answer:"""

    return llm.generate(prompt)

# Usage
context = rag_retrieve(table, "What is LanceDB?", embed_fn)
response = rag_generate("What is LanceDB?", context, llm)
```

### Hybrid RAG

```python
def hybrid_rag_retrieve(
    table,
    query: str,
    embed_fn,
    top_k: int = 5
) -> list[str]:
    """Hybrid retrieval for RAG."""

    query_vector = embed_fn(query)

    # Vector search
    vector_results = table.search(query_vector) \
        .limit(top_k * 2) \
        .to_list()

    # Full-text search
    fts_results = table.search(query, query_type="fts") \
        .limit(top_k * 2) \
        .to_list()

    # Combine with RRF
    combined = rrf_hybrid_search_internal(vector_results, fts_results, k=60)

    return [r['content'] for r in combined[:top_k]]
```

## Query Expansion

### Synonym Expansion

```python
def expand_query_with_synonyms(query: str, synonyms: dict) -> list[str]:
    """Expand query with synonyms."""
    words = query.lower().split()
    expanded_queries = [query]

    for word in words:
        if word in synonyms:
            for syn in synonyms[word]:
                new_query = query.replace(word, syn)
                expanded_queries.append(new_query)

    return expanded_queries

# Usage
synonyms = {
    "ml": ["machine learning", "artificial intelligence"],
    "db": ["database", "data store"],
    "fast": ["quick", "rapid", "speedy"]
}

queries = expand_query_with_synonyms("fast ml db", synonyms)
# ['fast ml db', 'quick ml db', 'rapid ml db', ...]

# Search with expanded queries
all_results = []
for q in queries:
    results = table.search(q, query_type="fts").limit(10).to_list()
    all_results.extend(results)

# Deduplicate and rank
unique_results = deduplicate_by_id(all_results)
```

### LLM Query Expansion

```python
def llm_expand_query(query: str, llm) -> list[str]:
    """Use LLM to generate query variations."""

    prompt = f"""Generate 3 alternative search queries for: "{query}"

Return only the queries, one per line, without numbering or explanation."""

    response = llm.generate(prompt)
    variations = [q.strip() for q in response.strip().split('\n') if q.strip()]

    return [query] + variations[:3]
```

## Best Practices

### Choosing Search Strategy

```python
def choose_search_strategy(query: str) -> str:
    """Choose search strategy based on query characteristics."""

    # Short queries might be keyword-heavy
    if len(query.split()) <= 2:
        return "hybrid"

    # Questions often need semantic understanding
    if query.endswith('?') or query.lower().startswith(('what', 'how', 'why', 'when')):
        return "vector"

    # Queries with special terms might need keyword match
    if any(char in query for char in ['"', '+', '-']):
        return "fts"

    # Default to hybrid
    return "hybrid"
```

### Filter Optimization

```python
# Good: Selective filters first
results = table.search(query_vector) \
    .where("category = 'technology'") \  # Filters 90% of data
    .where("year >= 2023") \  # Additional filter
    .limit(10) \
    .to_pandas()

# Avoid: Non-selective filters
# where("is_active = true")  # If 99% are active, not useful
```

## Summary

In this chapter, you've learned:

- **Full-Text Search**: Creating FTS indexes and BM25 search
- **Hybrid Search**: Combining vector and keyword search
- **Fusion Methods**: Weighted scoring and RRF
- **SQL Integration**: Complex queries and aggregations
- **Multi-Stage**: Two-stage retrieval and reranking
- **RAG Integration**: Building retrieval pipelines
- **Query Expansion**: Synonym and LLM-based expansion

## Key Takeaways

1. **Hybrid is Often Best**: Combine vector + FTS for best results
2. **RRF Works Well**: Simple and effective fusion method
3. **Use Pre-filtering**: More efficient than post-filtering
4. **Match to Use Case**: Choose strategy based on query type
5. **Expand When Needed**: Query expansion helps recall

## Next Steps

Now that you understand hybrid search, let's explore Integrations in Chapter 5 for connecting LanceDB with LangChain, LlamaIndex, and other tools.

---

**Ready for Chapter 5?** [Integrations](05-integrations.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
