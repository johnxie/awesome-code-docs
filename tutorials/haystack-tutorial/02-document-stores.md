---
layout: default
title: "Chapter 2: Document Stores"
parent: "Haystack Tutorial"
nav_order: 2
---

# Chapter 2: Document Stores

Welcome to **Chapter 2: Document Stores**. In this part of **Haystack: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explores Haystack's document storage capabilities. You'll learn how to set up and manage document stores, work with different storage backends, and optimize document storage for search performance.

## 🎯 What You'll Learn

- Document store types and backends
- Document preprocessing and indexing
- Storage optimization techniques
- Multi-document store architectures
- Document lifecycle management

## 📚 Document Store Fundamentals

### What is a Document Store?

A document store in Haystack is a component that stores and manages your documents, making them searchable and retrievable. Document stores handle:

- **Document Storage**: Persistent storage of documents and metadata
- **Indexing**: Creating searchable indexes for fast retrieval
- **Retrieval**: Efficient querying and filtering of documents
- **Updates**: Adding, modifying, and deleting documents

```python
from haystack.document_stores import InMemoryDocumentStore

# Create a simple in-memory document store
document_store = InMemoryDocumentStore()

# Add documents
documents = [
    {"content": "Haystack is an open-source framework for building search systems.", "meta": {"source": "docs"}},
    {"content": "Document stores provide efficient storage and retrieval of documents.", "meta": {"source": "docs"}}
]

document_store.write_documents(documents)
```

## 🗄️ Document Store Types

### In-Memory Document Store

Perfect for development, testing, and small datasets:

```python
from haystack.document_stores import InMemoryDocumentStore

# Create in-memory store
document_store = InMemoryDocumentStore()

# Configure similarity function
document_store = InMemoryDocumentStore(
    similarity="cosine",  # cosine, dot_product, euclidean
    index="document",     # document, flat, hnsw
    embedding_dim=768
)

# Add documents with embeddings
documents = [
    Document(
        content="Machine learning is a subset of artificial intelligence.",
        meta={"category": "AI", "difficulty": "beginner"},
        embedding=[0.1, 0.2, 0.3, ...]  # 768-dimensional embedding
    )
]

document_store.write_documents(documents)
```

### Elasticsearch Document Store

Production-ready with advanced search capabilities:

```python
from haystack.document_stores import ElasticsearchDocumentStore

# Connect to Elasticsearch
document_store = ElasticsearchDocumentStore(
    host="localhost",
    port=9200,
    username="elastic",
    password="your_password",
    index="my_documents",
    similarity="cosine",
    embedding_dim=768
)

# Configure index settings
document_store = ElasticsearchDocumentStore(
    host="localhost",
    index="haystack_docs",
    search_fields=["content", "title"],
    content_field="content",
    name_field="title",
    embedding_field="embedding",
    embedding_dim=768,
    excluded_meta_data=["file_path"],  # Don't index these fields
    analyzer="standard"  # Text analyzer for search
)
```

### Pinecone Document Store

Cloud-native vector database for large-scale deployments:

```python
from haystack.document_stores import PineconeDocumentStore

# Initialize Pinecone
document_store = PineconeDocumentStore(
    api_key="your_pinecone_api_key",
    environment="us-west1-gcp",
    index="haystack-docs",
    similarity="cosine",
    embedding_dim=768,
    recreate_index=True  # Set to False for existing indexes
)

# Configure for hybrid search
document_store = PineconeDocumentStore(
    api_key="your_api_key",
    index="hybrid-search",
    similarity="dot_product",
    embedding_dim=768,
    # Enable sparse-dense embeddings for hybrid search
    sparse_embedding_field="sparse_embedding",
    sparse_embedding_dim=10000
)
```

### Weaviate Document Store

Graph-based vector database with advanced features:

```python
from haystack.document_stores import WeaviateDocumentStore

# Connect to Weaviate
document_store = WeaviateDocumentStore(
    host="http://localhost",
    port=8080,
    embedding_dim=768,
    similarity="cosine",
    index="Document",
    recreate_index=True
)

# Advanced configuration
document_store = WeaviateDocumentStore(
    url="https://your-weaviate-cluster.com",
    api_key="your_api_key",
    embedding_dim=768,
    # Custom class configuration
    custom_schema={
        "class": "Document",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "title", "dataType": ["string"]},
            {"name": "embedding", "dataType": ["number[]"]}
        ]
    }
)
```

## 📝 Document Processing

### Document Creation and Metadata

```python
from haystack import Document

# Create documents with metadata
documents = [
    Document(
        content="Natural language processing (NLP) is a field of AI that focuses on the interaction between computers and humans through natural language.",
        meta={
            "title": "Introduction to NLP",
            "author": "AI Researcher",
            "category": "AI",
            "difficulty": "intermediate",
            "tags": ["NLP", "AI", "machine learning"],
            "created_at": "2023-01-15",
            "source": "research_paper.pdf"
        },
        id="doc_001"
    ),
    Document(
        content="Vector databases store and query high-dimensional vectors efficiently, enabling fast similarity search.",
        meta={
            "title": "Vector Databases Explained",
            "author": "Data Engineer",
            "category": "Databases",
            "difficulty": "advanced",
            "tags": ["vector database", "similarity search", "embeddings"],
            "created_at": "2023-02-01",
            "source": "tech_blog.md"
        },
        id="doc_002"
    )
]
```

### Document Preprocessing

```python
from haystack.nodes import PreProcessor

# Text preprocessing
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=True,
    split_by="word",
    split_length=200,
    split_overlap=20,
    split_respect_sentence_boundary=True
)

# Process documents
processed_docs = preprocessor.process(documents)
```

### Batch Document Operations

```python
# Batch write documents
document_store.write_documents(documents, batch_size=100)

# Batch update documents
updates = [
    {"id": "doc_001", "meta": {"read_count": 150}},
    {"id": "doc_002", "meta": {"read_count": 89}}
]
document_store.update_documents(updates)

# Batch delete documents
document_store.delete_documents(ids=["doc_001", "doc_002"])
```

## 🔍 Document Retrieval

### Basic Retrieval

```python
# Get all documents
all_docs = document_store.get_all_documents()
print(f"Total documents: {len(all_docs)}")

# Get documents by IDs
specific_docs = document_store.get_documents_by_id(["doc_001", "doc_002"])

# Get documents with filters
filtered_docs = document_store.get_documents(
    filters={"category": "AI", "difficulty": "intermediate"}
)

# Search documents
search_results = document_store.query(
    query="machine learning",
    filters={"category": "AI"},
    top_k=10,
    return_embedding=False
)
```

### Advanced Filtering

```python
# Complex filters
complex_filters = {
    "$and": {
        "category": {"$in": ["AI", "ML"]},
        "difficulty": {"$ne": "beginner"},
        "created_at": {"$gte": "2023-01-01"},
        "tags": {"$in": ["NLP", "deep learning"]}
    }
}

results = document_store.get_documents(filters=complex_filters)
```

### Document Pagination

```python
# Paginated retrieval
page = 1
page_size = 50

while True:
    docs = document_store.get_documents(
        filters={"category": "AI"},
        page=page,
        page_size=page_size
    )

    if not docs:
        break

    print(f"Page {page}: {len(docs)} documents")
    page += 1
```

## 🔧 Document Store Optimization

### Indexing Strategies

```python
# Configure indexing for performance
document_store = ElasticsearchDocumentStore(
    # Index settings
    index_settings={
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "refresh_interval": "30s"
    },
    # Mapping settings
    mapping_settings={
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "embedding": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
)
```

### Memory Optimization

```python
# Configure memory settings
document_store = InMemoryDocumentStore(
    # Memory management
    similarity="cosine",
    index="hnsw",  # More memory efficient than flat
    embedding_dim=768,
    # HNSW index parameters
    hnsw_config={
        "m": 16,        # Number of bi-directional links
        "ef_construction": 200,  # Size of dynamic candidate list
        "ef_runtime": 10         # Size of candidate list at runtime
    }
)
```

### Caching Strategies

```python
from haystack.document_stores import CachedDocumentStore
from haystack.caching import SimpleCache

# Add caching to document store
cache = SimpleCache()
cached_store = CachedDocumentStore(
    document_store=document_store,
    cache=cache,
    cache_key_prefix="haystack_docs"
)

# Cache will automatically store frequent queries
results = cached_store.query(query="machine learning")
# Second query will be served from cache
results = cached_store.query(query="machine learning")
```

## 📊 Document Store Monitoring

### Performance Metrics

```python
# Get store statistics
stats = document_store.get_documents_count()
print(f"Total documents: {stats}")

# Query performance
import time

start_time = time.time()
results = document_store.query(query="AI", top_k=100)
query_time = time.time() - start_time

print(f"Query time: {query_time:.3f} seconds")
print(f"Results: {len(results)}")
```

### Health Checks

```python
# Document store health check
def health_check(document_store):
    """Perform comprehensive health check"""
    health_status = {
        "connection": False,
        "read_access": False,
        "write_access": False,
        "query_performance": False
    }

    try:
        # Test connection
        count = document_store.get_documents_count()
        health_status["connection"] = True

        # Test read access
        docs = document_store.get_documents(limit=1)
        health_status["read_access"] = True

        # Test write access (if supported)
        if hasattr(document_store, 'write_documents'):
            test_doc = Document(content="Health check document")
            document_store.write_documents([test_doc])
            health_status["write_access"] = True

        # Test query performance
        start_time = time.time()
        results = document_store.query(query="test", top_k=5)
        query_time = time.time() - start_time
        health_status["query_performance"] = query_time < 1.0  # Should be < 1 second

    except Exception as e:
        print(f"Health check failed: {e}")

    return health_status

# Run health check
status = health_check(document_store)
print("Health Status:", status)
```

## 🔄 Document Lifecycle Management

### Document Versioning

```python
# Version control for documents
class VersionedDocumentStore:
    def __init__(self, document_store):
        self.document_store = document_store
        self.version_store = {}  # Simple version tracking

    def save_version(self, document_id, version="latest"):
        """Save a version of a document"""
        doc = self.document_store.get_documents_by_id([document_id])[0]
        self.version_store[f"{document_id}_{version}"] = doc
        return version

    def get_version(self, document_id, version="latest"):
        """Retrieve a specific version of a document"""
        return self.version_store.get(f"{document_id}_{version}")

    def list_versions(self, document_id):
        """List all versions of a document"""
        return [k for k in self.version_store.keys() if k.startswith(f"{document_id}_")]
```

### Document Archiving

```python
# Archive old documents
def archive_documents(document_store, archive_store, days_old=90):
    """Archive documents older than specified days"""
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days_old)

    # Find old documents
    old_docs = document_store.get_documents(
        filters={"created_at": {"$lt": cutoff_date.isoformat()}}
    )

    # Move to archive store
    archive_store.write_documents(old_docs)

    # Remove from main store
    document_store.delete_documents(ids=[doc.id for doc in old_docs])

    return len(old_docs)
```

## 🎯 Best Practices

### Document Store Selection

1. **Development**: Use `InMemoryDocumentStore` for quick prototyping
2. **Small Production**: `ElasticsearchDocumentStore` for search-heavy workloads
3. **Large Scale**: `PineconeDocumentStore` or `WeaviateDocumentStore` for vector search
4. **Hybrid Search**: Choose stores that support both keyword and vector search

### Performance Optimization

1. **Batch Operations**: Always use batch writes for multiple documents
2. **Index Optimization**: Configure indexes based on your query patterns
3. **Caching**: Implement caching for frequently accessed documents
4. **Pagination**: Use pagination for large result sets

### Data Management

1. **Regular Backups**: Implement automated backup strategies
2. **Version Control**: Track document versions for audit trails
3. **Data Validation**: Validate documents before storage
4. **Cleanup**: Regularly archive or delete old/unused documents

## 🏆 Achievement Unlocked!

Congratulations! 🎉 You've mastered:

- ✅ Different document store types and their use cases
- ✅ Document creation with rich metadata
- ✅ Advanced filtering and querying
- ✅ Performance optimization techniques
- ✅ Document lifecycle management
- ✅ Health monitoring and maintenance

## 🚀 What's Next?

Ready to explore retrieval techniques? Let's dive into [Chapter 3: Retrievers & Search](03-retrievers-search.md) to learn about finding relevant documents efficiently.

---

**Practice what you've learned:**
1. Set up different document stores (in-memory, Elasticsearch, Pinecone)
2. Create documents with comprehensive metadata
3. Implement complex filtering and querying
4. Optimize your document store for performance
5. Set up monitoring and health checks

*What's your preferred document store for different use cases?* 📚

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `document_store`, `documents`, `query` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Document Stores` as an operating subsystem inside **Haystack: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `index`, `haystack`, `content` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Document Stores` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `document_store`.
2. **Input normalization**: shape incoming data so `documents` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `query`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Haystack](https://github.com/deepset-ai/haystack)
  Why it matters: authoritative reference on `Haystack` (github.com).

Suggested trace strategy:
- search upstream code for `document_store` and `documents` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Haystack](01-getting-started.md)
- [Next Chapter: Chapter 3: Retrievers & Search](03-retrievers-search.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
