---
layout: default
title: "Chapter 3: Embeddings & Indexing"
parent: "Chroma Tutorial"
nav_order: 3
---

# Chapter 3: Embeddings & Indexing

Welcome to the heart of Chroma's power! This chapter explores how embeddings work, how Chroma indexes them for fast retrieval, and how to optimize similarity search performance.

## Understanding Embeddings

### What Are Embeddings?

Embeddings are mathematical representations that capture the semantic meaning of text in vector form:

```python
import chromadb
import numpy as np

# Create collection and add documents
client = chromadb.Client()
collection = client.create_collection("embeddings_demo")

documents = [
    "The cat sits on the mat",
    "A feline rests on a rug",
    "Python is a programming language",
    "Dogs love to play fetch"
]

collection.add(
    documents=documents,
    ids=["doc1", "doc2", "doc3", "doc4"]
)

# Examine the embeddings
results = collection.get(include=['embeddings', 'documents'])

print("Embedding dimensions:", len(results['embeddings'][0]))
print("Sample embedding values:", results['embeddings'][0][:5])

# Notice: doc1 and doc2 have similar meanings -> similar embeddings
# doc1 and doc3 have different meanings -> different embeddings
```

### Embedding Mathematics

```python
# Calculate similarity between embeddings
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Compare embeddings
embeddings = results['embeddings']
similarity_1_2 = cosine_similarity(embeddings[0], embeddings[1])  # Similar documents
similarity_1_3 = cosine_similarity(embeddings[0], embeddings[2])  # Different documents

print(f"Cat/mat similarity: {similarity_1_2:.3f}")
print(f"Cat/Python similarity: {similarity_1_3:.3f}")
```

## Custom Embedding Functions

### Using Different Models

```python
from chromadb.utils import embedding_functions

# OpenAI embeddings
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-openai-key",
    model_name="text-embedding-ada-002"
)

# Sentence Transformers
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create collections with different embeddings
openai_collection = client.create_collection(
    name="openai_embeddings",
    embedding_function=openai_ef
)

st_collection = client.create_collection(
    name="sentence_transformers",
    embedding_function=sentence_transformer_ef
)
```

### Custom Embedding Implementation

```python
import chromadb
from typing import List

class CustomEmbeddingFunction:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def __call__(self, texts: List[str]) -> List[List[float]]:
        # Generate embeddings
        embeddings = self.model.encode(texts)

        # Convert to list of lists (Chroma format)
        return embeddings.tolist()

# Use custom embedding function
custom_ef = CustomEmbeddingFunction()
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=custom_ef
)
```

## Vector Indexing Deep Dive

### HNSW Algorithm

```python
# Understanding HNSW (Hierarchical Navigable Small World)
# Chroma uses HNSW for approximate nearest neighbor search

collection = client.create_collection(
    name="hnsw_demo",
    metadata={
        "hnsw:space": "cosine",  # Distance metric
        "hnsw:construction_ef": 100,  # Construction parameter
        "hnsw:M": 16  # Maximum connections per node
    }
)

# Add documents
collection.add(
    documents=["Document " + str(i) for i in range(1000)],
    ids=[f"doc_{i}" for i in range(1000)]
)

# Query with different ef (search quality vs speed tradeoff)
results = collection.query(
    query_texts=["Document 42"],
    n_results=10,
    # Higher ef = better accuracy, slower search
    # Lower ef = faster search, lower accuracy
)
```

### Indexing Parameters

```python
# Optimize indexing for your use case
def create_optimized_collection(name: str, use_case: str):
    if use_case == "accuracy":
        # High accuracy, slower search
        metadata = {
            "hnsw:M": 32,
            "hnsw:construction_ef": 200,
            "hnsw:search_ef": 100
        }
    elif use_case == "speed":
        # Fast search, lower accuracy
        metadata = {
            "hnsw:M": 8,
            "hnsw:construction_ef": 50,
            "hnsw:search_ef": 32
        }
    else:
        # Balanced approach
        metadata = {
            "hnsw:M": 16,
            "hnsw:construction_ef": 100,
            "hnsw:search_ef": 64
        }

    return client.create_collection(
        name=name,
        metadata=metadata
    )

# Usage
accuracy_collection = create_optimized_collection("accuracy_focused", "accuracy")
speed_collection = create_optimized_collection("speed_focused", "speed")
```

## Similarity Search Strategies

### Exact vs Approximate Search

```python
# Exact search (brute force) - accurate but slow
def exact_search(query_embedding, all_embeddings, k=5):
    similarities = []
    for i, emb in enumerate(all_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        similarities.append((i, sim))

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]

# Approximate search (HNSW) - fast but approximate
results = collection.query(
    query_texts=["machine learning algorithms"],
    n_results=5
)
```

### Distance Metrics

```python
# Different distance metrics for different use cases
distance_configs = {
    "cosine": {  # Good for text similarity
        "description": "Cosine similarity - measures angle between vectors",
        "use_case": "Semantic similarity, text matching"
    },
    "l2": {  # Good for location data
        "description": "Euclidean distance - straight-line distance",
        "use_case": "Location-based search, numerical data"
    },
    "ip": {  # Good for normalized embeddings
        "description": "Inner product - dot product similarity",
        "use_case": "Recommendation systems, collaborative filtering"
    }
}

# Create collections with different distance metrics
for metric, config in distance_configs.items():
    collection = client.create_collection(
        name=f"{metric}_collection",
        metadata={
            "hnsw:space": metric,
            "description": config["description"]
        }
    )
    print(f"Created {metric} collection: {config['use_case']}")
```

## Advanced Querying

### Multi-Vector Queries

```python
# Query with multiple vectors (ensemble search)
query_texts = [
    "artificial intelligence",
    "machine learning",
    "neural networks"
]

results = collection.query(
    query_texts=query_texts,
    n_results=5,
    # Chroma will combine results from all queries
)

print("Multi-query results:")
for i, docs in enumerate(results['documents']):
    print(f"Query {i+1}: {docs[0][:50]}...")
```

### Weighted Queries

```python
# Custom weighted similarity
def weighted_query(collection, query_texts, weights, n_results=5):
    # Get embeddings for query texts
    query_embeddings = []
    for text in query_texts:
        # This is simplified - you'd use the actual embedding function
        embedding = get_embedding(text)
        query_embeddings.append(embedding)

    # Perform individual queries
    all_results = []
    for i, (embedding, weight) in enumerate(zip(query_embeddings, weights)):
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results * 2  # Get more candidates
        )

        # Add weight to results
        for j, doc in enumerate(results['documents'][0]):
            all_results.append({
                'document': doc,
                'similarity': results['distances'][0][j],
                'weight': weight,
                'query_index': i
            })

    # Combine and rerank results
    combined = {}
    for result in all_results:
        doc = result['document']
        if doc not in combined:
            combined[doc] = {'score': 0, 'weights': []}

        combined[doc]['score'] += result['similarity'] * result['weight']
        combined[doc]['weights'].append(result['weight'])

    # Sort by combined score
    sorted_results = sorted(combined.items(), key=lambda x: x[1]['score'])

    return [doc for doc, _ in sorted_results[:n_results]]

# Usage
results = weighted_query(
    collection=collection,
    query_texts=["AI", "ML", "neural"],
    weights=[0.5, 0.3, 0.2],
    n_results=5
)
```

## Performance Optimization

### Indexing Best Practices

```python
# Optimize indexing for production
production_config = {
    "hnsw:M": 32,                    # Higher connectivity
    "hnsw:construction_ef": 200,     # Better index quality
    "hnsw:search_ef": 128,          # Good search quality
    "hnsw:space": "cosine",         # Distance metric
    "hnsw:num_threads": 4,          # Parallel indexing
    "persist_directory": "./chroma_prod"  # Persistent storage
}

production_collection = client.create_collection(
    name="production_ready",
    metadata=production_config
)
```

### Memory and Storage Optimization

```python
from chromadb.config import Settings

# Optimize for memory usage
memory_optimized_client = chromadb.PersistentClient(
    path="./optimized_chroma",
    settings=Settings(
        chroma_memory_limit=8 * 1024 * 1024 * 1024,  # 8GB limit
        chroma_cache_size=1 * 1024 * 1024 * 1024,    # 1GB cache
        chroma_max_batch_size=500,                   # Batch size
        chroma_batch_cache_size=1000                 # Batch cache
    )
)
```

## Embedding Quality Assessment

### Evaluating Embedding Performance

```python
def evaluate_embedding_quality(collection, test_queries):
    results = []

    for query in test_queries:
        # Get similar documents
        search_results = collection.query(
            query_texts=[query['text']],
            n_results=10
        )

        # Calculate metrics
        precision = calculate_precision(search_results, query['relevant_docs'])
        recall = calculate_recall(search_results, query['relevant_docs'])
        ndcg = calculate_ndcg(search_results, query['relevant_docs'])

        results.append({
            'query': query['text'],
            'precision@10': precision,
            'recall@10': recall,
            'ndcg@10': ndcg
        })

    return results

# Usage
test_queries = [
    {
        'text': 'machine learning algorithms',
        'relevant_docs': ['doc_ml_1', 'doc_ml_2', 'doc_algo_1']
    }
]

evaluation_results = evaluate_embedding_quality(collection, test_queries)
```

## What We've Accomplished

Congratulations! 🎉 You've mastered:

1. **Embeddings Fundamentals** - Understanding vector representations
2. **Custom Embedding Functions** - Using different models and implementations
3. **Vector Indexing** - HNSW algorithm and optimization parameters
4. **Similarity Search** - Exact vs approximate search strategies
5. **Advanced Querying** - Multi-vector and weighted queries
6. **Performance Optimization** - Production-ready indexing and memory management
7. **Quality Assessment** - Evaluating embedding and search performance

## Next Steps

Ready to query like a pro? In [Chapter 4: Querying & Retrieval](04-querying-retrieval.md), we'll explore advanced querying patterns, metadata filtering, and retrieval strategies.

---

**Practice what you've learned:**
1. Experiment with different embedding models
2. Optimize indexing parameters for your use case
3. Implement custom similarity metrics
4. Build a performance evaluation pipeline
5. Create weighted query combinations

*How will you optimize embeddings for your application?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `embeddings`, `collection`, `results` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Embeddings & Indexing` as an operating subsystem inside **ChromaDB Tutorial: Building AI-Native Vector Databases**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `hnsw`, `query`, `documents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Embeddings & Indexing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `embeddings`.
2. **Input normalization**: shape incoming data so `collection` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `results`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/chroma-core/chroma)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `embeddings` and `collection` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Collections & Documents](02-collections-documents.md)
- [Next Chapter: Chapter 4: Querying & Retrieval](04-querying-retrieval.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
