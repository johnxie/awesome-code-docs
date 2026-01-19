---
layout: default
title: "Chapter 3: Vector Operations"
parent: "LanceDB Tutorial"
nav_order: 3
---

# Chapter 3: Vector Operations

> Master vector indexing, similarity search, and advanced query techniques for efficient retrieval.

## Overview

Vector operations are at the heart of LanceDB. This chapter covers indexing strategies, distance metrics, approximate nearest neighbor (ANN) search, and advanced query patterns for building high-performance vector search applications.

## Vector Indexing

### Creating Vector Indexes

```python
import lancedb
import numpy as np

db = lancedb.connect("./my_lancedb")

# Create table with data
data = [
    {"id": i, "text": f"Document {i}", "vector": np.random.rand(384).tolist()}
    for i in range(10000)
]
table = db.create_table("indexed_table", data)

# Create IVF-PQ index (recommended for large datasets)
table.create_index(
    metric="cosine",
    num_partitions=256,  # Number of IVF partitions
    num_sub_vectors=96,  # Number of PQ sub-vectors
)

print("Index created successfully")
```

### Index Types

```python
# IVF_PQ (Inverted File with Product Quantization)
# Best for: Large datasets (100K+ vectors)
table.create_index(
    metric="cosine",
    num_partitions=256,
    num_sub_vectors=96,
    index_type="IVF_PQ"
)

# IVF_FLAT (Inverted File without compression)
# Best for: Medium datasets, higher accuracy needed
table.create_index(
    metric="cosine",
    num_partitions=256,
    index_type="IVF_FLAT"
)

# HNSW (Hierarchical Navigable Small World)
# Best for: Fast search, memory-constrained environments
table.create_index(
    metric="cosine",
    index_type="IVF_HNSW_SQ",
    num_partitions=256,
    max_iterations=50
)
```

### Index Configuration

```python
# Detailed index configuration
table.create_index(
    # Distance metric
    metric="cosine",  # or "L2", "dot"

    # IVF parameters
    num_partitions=256,  # More partitions = faster search, more memory

    # PQ parameters
    num_sub_vectors=96,  # More sub-vectors = better accuracy, more memory

    # Training parameters
    sample_rate=256,  # Samples per partition for training

    # Index name (for multiple indexes)
    index_name="my_vector_index",

    # Replace existing index
    replace=True
)
```

## Distance Metrics

### Cosine Similarity

```python
# Cosine similarity (default)
# Range: 0 to 2 (0 = identical, 2 = opposite)
# Best for: Text embeddings, normalized vectors

results = table.search(query_vector) \
    .metric("cosine") \
    .limit(10) \
    .to_pandas()

# Results include _distance column
# Lower distance = more similar
```

### Euclidean Distance (L2)

```python
# L2 (Euclidean) distance
# Range: 0 to infinity
# Best for: Image embeddings, spatial data

results = table.search(query_vector) \
    .metric("L2") \
    .limit(10) \
    .to_pandas()

# Lower distance = more similar
```

### Dot Product

```python
# Dot product
# Range: depends on vector magnitudes
# Best for: Recommendation systems, when vectors are normalized

results = table.search(query_vector) \
    .metric("dot") \
    .limit(10) \
    .to_pandas()

# Higher value = more similar (note: returns negative for sorting)
```

### Choosing the Right Metric

```python
def choose_metric(embedding_type: str) -> str:
    """Select appropriate distance metric."""
    metrics = {
        "text": "cosine",      # Most text embeddings are normalized
        "sentence": "cosine",  # Sentence transformers use cosine
        "openai": "cosine",    # OpenAI embeddings work best with cosine
        "image": "L2",         # CLIP and similar use L2
        "colbert": "dot",      # ColBERT-style uses dot product
    }
    return metrics.get(embedding_type, "cosine")
```

## Similarity Search

### Basic Search

```python
import lancedb
import numpy as np

db = lancedb.connect("./my_lancedb")
table = db.open_table("my_table")

# Search with numpy array
query = np.random.rand(384)
results = table.search(query).limit(10).to_pandas()

# Search with list
query = [0.1] * 384
results = table.search(query).limit(10).to_pandas()
```

### Search with Refinement

```python
# nprobes: Number of partitions to search (for IVF indexes)
# Higher = more accurate, slower
results = table.search(query) \
    .nprobes(20) \  # Search 20 partitions
    .limit(10) \
    .to_pandas()

# refine_factor: Rerank top results for better accuracy
results = table.search(query) \
    .refine_factor(10) \  # Fetch 10x candidates, rerank
    .limit(10) \
    .to_pandas()
```

### Multi-Vector Search

```python
from lancedb.pydantic import LanceModel, Vector

class MultiVectorDoc(LanceModel):
    id: str
    title_vector: Vector(384)
    content_vector: Vector(768)

table = db.create_table("multi_vec", schema=MultiVectorDoc)

# Search on specific vector column
title_results = table.search(
    query_vector,
    vector_column_name="title_vector"
).limit(10).to_pandas()

content_results = table.search(
    query_vector,
    vector_column_name="content_vector"
).limit(10).to_pandas()
```

### Batch Search

```python
# Search with multiple queries
queries = [
    np.random.rand(384).tolist(),
    np.random.rand(384).tolist(),
    np.random.rand(384).tolist(),
]

# Process each query
all_results = []
for query in queries:
    results = table.search(query).limit(10).to_list()
    all_results.append(results)

# Or use async for better performance
import asyncio

async def batch_search(table, queries, limit=10):
    tasks = [
        asyncio.to_thread(lambda q=q: table.search(q).limit(limit).to_list())
        for q in queries
    ]
    return await asyncio.gather(*tasks)
```

## Filtered Search

### Pre-filtering

```python
# Filter BEFORE vector search (more efficient for selective filters)
results = table.search(query) \
    .where("category = 'technology'") \
    .limit(10) \
    .to_pandas()

# Multiple conditions
results = table.search(query) \
    .where("category = 'technology' AND year >= 2023") \
    .limit(10) \
    .to_pandas()
```

### Post-filtering

```python
# Post-filter mode (search first, then filter)
results = table.search(query) \
    .where("category = 'technology'", prefilter=False) \
    .limit(10) \
    .to_pandas()
```

### Complex Filters

```python
# IN clause
results = table.search(query) \
    .where("category IN ('tech', 'science', 'health')") \
    .limit(10) \
    .to_pandas()

# BETWEEN
results = table.search(query) \
    .where("price BETWEEN 10 AND 100") \
    .limit(10) \
    .to_pandas()

# NULL checks
results = table.search(query) \
    .where("author IS NOT NULL") \
    .limit(10) \
    .to_pandas()

# String operations
results = table.search(query) \
    .where("title LIKE '%LanceDB%'") \
    .limit(10) \
    .to_pandas()

# Date comparisons
results = table.search(query) \
    .where("created_at > '2024-01-01'") \
    .limit(10) \
    .to_pandas()
```

## Output Formats

### To Pandas DataFrame

```python
# Most common format
df = table.search(query).limit(10).to_pandas()
print(df.columns)  # id, text, vector, _distance
```

### To List

```python
# List of dictionaries
results = table.search(query).limit(10).to_list()
for item in results:
    print(f"{item['id']}: {item['_distance']}")
```

### To Arrow

```python
# PyArrow Table (efficient for further processing)
arrow_table = table.search(query).limit(10).to_arrow()
print(arrow_table.schema)
```

### To Pydantic Models

```python
from lancedb.pydantic import LanceModel, Vector

class Document(LanceModel):
    id: str
    text: str
    vector: Vector(384)

# Get results as Pydantic models
results = table.search(query).limit(10).to_pydantic(Document)
for doc in results:
    print(f"{doc.id}: {doc.text}")
```

## Column Selection

### Select Specific Columns

```python
# Only retrieve specific columns (faster)
results = table.search(query) \
    .select(["id", "title", "content"]) \
    .limit(10) \
    .to_pandas()

# Exclude vector column (much faster for large vectors)
results = table.search(query) \
    .select(["id", "title"]) \
    .limit(10) \
    .to_pandas()
```

### Computed Columns

```python
# Add computed columns (if supported)
results = table.search(query) \
    .select(["id", "title", "LENGTH(content) as content_length"]) \
    .limit(10) \
    .to_pandas()
```

## Reranking

### Basic Reranking

```python
# Use refine_factor for basic reranking
results = table.search(query) \
    .refine_factor(5) \  # Fetch 5x, rerank with exact distances
    .limit(10) \
    .to_pandas()
```

### Custom Reranking

```python
from sentence_transformers import CrossEncoder

# Load cross-encoder for reranking
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_results(query_text: str, results: list, top_k: int = 10) -> list:
    """Rerank results using cross-encoder."""
    if not results:
        return results

    # Prepare pairs for cross-encoder
    pairs = [(query_text, r['content']) for r in results]

    # Get cross-encoder scores
    scores = cross_encoder.predict(pairs)

    # Add scores to results
    for i, r in enumerate(results):
        r['rerank_score'] = scores[i]

    # Sort by rerank score
    results.sort(key=lambda x: x['rerank_score'], reverse=True)

    return results[:top_k]

# Usage
initial_results = table.search(query_vector).limit(50).to_list()
reranked = rerank_results("What is LanceDB?", initial_results, top_k=10)
```

### Reciprocal Rank Fusion

```python
def reciprocal_rank_fusion(result_lists: list[list], k: int = 60) -> list:
    """Combine multiple result lists using RRF."""
    scores = {}

    for results in result_lists:
        for rank, item in enumerate(results):
            item_id = item['id']
            if item_id not in scores:
                scores[item_id] = {'item': item, 'score': 0}
            scores[item_id]['score'] += 1 / (k + rank + 1)

    # Sort by combined score
    sorted_items = sorted(scores.values(), key=lambda x: x['score'], reverse=True)
    return [item['item'] for item in sorted_items]

# Combine vector search with different queries
results1 = table.search(query1).limit(50).to_list()
results2 = table.search(query2).limit(50).to_list()
combined = reciprocal_rank_fusion([results1, results2])
```

## Performance Optimization

### Index Tuning

```python
# For high recall (accuracy)
table.create_index(
    metric="cosine",
    num_partitions=512,  # More partitions
    num_sub_vectors=128,  # More sub-vectors
)

# For high throughput (speed)
table.create_index(
    metric="cosine",
    num_partitions=128,  # Fewer partitions
    num_sub_vectors=48,  # Fewer sub-vectors
)
```

### Query Optimization

```python
# Optimize for latency
results = table.search(query) \
    .nprobes(10) \  # Fewer probes
    .limit(10) \
    .select(["id", "title"]) \  # Minimal columns
    .to_list()

# Optimize for accuracy
results = table.search(query) \
    .nprobes(50) \  # More probes
    .refine_factor(10) \  # Rerank candidates
    .limit(10) \
    .to_pandas()
```

### Batch Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def search_batch(queries: list, table, limit: int = 10):
    """Process search queries in parallel."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(lambda q: table.search(q).limit(limit).to_list(), query)
            for query in queries
        ]
        return [f.result() for f in futures]
```

## Summary

In this chapter, you've learned:

- **Indexing**: Creating and configuring vector indexes
- **Distance Metrics**: Choosing between cosine, L2, and dot product
- **Search Operations**: Basic and advanced similarity search
- **Filtering**: Pre-filter and post-filter strategies
- **Output Formats**: DataFrames, lists, Arrow, and Pydantic
- **Reranking**: Basic and custom reranking approaches
- **Optimization**: Index and query performance tuning

## Key Takeaways

1. **Index Large Tables**: IVF-PQ for datasets over 100K vectors
2. **Choose Metrics Wisely**: Cosine for text, L2 for images
3. **Use Pre-filtering**: More efficient for selective filters
4. **Minimize Columns**: Don't fetch vectors if not needed
5. **Tune for Your Needs**: Balance accuracy vs. speed

## Next Steps

Now that you understand vector operations, let's explore Hybrid Search in Chapter 4 for combining vector, full-text, and SQL search.

---

**Ready for Chapter 4?** [Hybrid Search](04-hybrid-search.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
