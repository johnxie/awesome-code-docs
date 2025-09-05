---
layout: default
title: "Chapter 2: Collections & Documents"
parent: "Chroma Tutorial"
nav_order: 2
---

# Chapter 2: Collections & Documents

Welcome back! Now that you understand Chroma's basics, let's dive deeper into managing collections and documents. Collections are the core organizational unit in Chroma, and understanding how to work with them effectively is crucial for building robust AI applications.

## Collection Architecture

### Understanding Collections

Collections in Chroma are like specialized databases optimized for vector operations:

```python
import chromadb
from chromadb.config import Settings

# Initialize with custom settings
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Create a collection with specific configuration
collection = client.create_collection(
    name="knowledge_base",
    metadata={
        "description": "Company knowledge base",
        "created_by": "tutorial",
        "version": "1.0"
    }
)
```

### Collection Properties

```python
# Get collection information
print(f"Collection name: {collection.name}")
print(f"Document count: {collection.count()}")
print(f"Collection metadata: {collection.metadata}")

# Collection has these key properties:
# - name: Unique identifier
# - metadata: Custom key-value pairs
# - documents: Text content
# - embeddings: Vector representations
# - metadatas: Document-level metadata
# - ids: Unique document identifiers
```

## Document Management

### Adding Documents

```python
# Single document addition
collection.add(
    documents=["Machine learning is transforming industries"],
    metadatas=[{"category": "technology", "importance": "high"}],
    ids=["doc_001"]
)

# Batch document addition
documents = [
    "Python is a versatile programming language",
    "Data science combines statistics and programming",
    "AI models learn from data patterns",
    "Vector databases enable fast similarity search"
]

metadatas = [
    {"topic": "programming", "difficulty": "beginner"},
    {"topic": "data_science", "difficulty": "intermediate"},
    {"topic": "ai", "difficulty": "advanced"},
    {"topic": "databases", "difficulty": "intermediate"}
]

ids = [f"doc_{i+2:03d}" for i in range(len(documents))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
```

### Document Updates

```python
# Update existing documents
collection.update(
    ids=["doc_001"],
    documents=["Machine learning is revolutionizing industries"],
    metadatas=[{"category": "technology", "importance": "critical"}]
)

# Upsert (insert or update)
collection.upsert(
    documents=["New document content"],
    metadatas=[{"status": "new"}],
    ids=["doc_100"]
)
```

### Document Deletion

```python
# Delete specific documents
collection.delete(ids=["doc_005", "doc_010"])

# Delete with filters
collection.delete(where={"category": "obsolete"})
```

## Advanced Document Types

### Structured Documents

```python
# Store structured data as JSON strings
import json

structured_docs = [
    {
        "title": "Machine Learning Basics",
        "content": "ML is a subset of AI...",
        "tags": ["ml", "ai", "basics"],
        "metadata": {
            "difficulty": "beginner",
            "duration": "30min",
            "prerequisites": ["python"]
        }
    },
    {
        "title": "Advanced Neural Networks",
        "content": "Deep learning uses neural networks...",
        "tags": ["deep-learning", "neural-networks"],
        "metadata": {
            "difficulty": "advanced",
            "duration": "2hours",
            "prerequisites": ["calculus", "linear-algebra"]
        }
    }
]

# Convert to documents
documents = [json.dumps(doc) for doc in structured_docs]
metadatas = [{"type": "structured", "title": doc["title"]} for doc in structured_docs]
ids = [f"structured_{i}" for i in range(len(structured_docs))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
```

### Multi-Modal Documents

```python
# Handle different content types
multimodal_docs = [
    "This is a text document",
    "https://example.com/image.jpg",  # Image URL
    "base64_encoded_image_data",     # Base64 image
    "<html><body>HTML content</body></html>"  # HTML
]

content_types = ["text", "image_url", "image_base64", "html"]

collection.add(
    documents=multimodal_docs,
    metadatas=[{"content_type": ct} for ct in content_types],
    ids=[f"multi_{i}" for i in range(len(multimodal_docs))]
)
```

## Metadata Strategies

### Hierarchical Metadata

```python
# Organize metadata hierarchically
hierarchical_metadata = [
    {
        "domain": "technology",
        "category": "programming",
        "subcategory": "python",
        "difficulty": "intermediate",
        "tags": ["python", "web", "api"],
        "author": "tutorial_author",
        "created_date": "2024-01-01",
        "version": "1.0"
    },
    {
        "domain": "science",
        "category": "ai",
        "subcategory": "machine_learning",
        "difficulty": "advanced",
        "tags": ["ml", "neural", "deep-learning"],
        "author": "ml_expert",
        "created_date": "2024-01-02",
        "version": "2.0"
    }
]

collection.add(
    documents=["Python programming guide", "Neural networks explained"],
    metadatas=hierarchical_metadata,
    ids=["python_guide", "neural_guide"]
)
```

### Metadata Validation

```python
# Validate metadata before adding
def validate_metadata(metadata):
    required_fields = ["category", "difficulty"]
    allowed_difficulties = ["beginner", "intermediate", "advanced"]

    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"Missing required field: {field}")

    if metadata["difficulty"] not in allowed_difficulties:
        raise ValueError(f"Invalid difficulty: {metadata['difficulty']}")

    return True

# Usage
valid_metadata = {
    "category": "programming",
    "difficulty": "intermediate",
    "tags": ["python", "tutorial"]
}

validate_metadata(valid_metadata)

collection.add(
    documents=["Validated document"],
    metadatas=[valid_metadata],
    ids=["validated_doc"]
)
```

## Collection Operations

### Collection Merging

```python
# Merge collections
source_collection = client.get_collection("source_collection")
target_collection = client.get_collection("target_collection")

# Get all data from source
source_data = source_collection.get()

# Add to target with new IDs
target_collection.add(
    documents=source_data["documents"],
    metadatas=source_data["metadatas"],
    ids=[f"merged_{i}" for i in range(len(source_data["documents"]))]
)
```

### Collection Splitting

```python
# Split large collection into smaller ones
def split_collection(collection, max_docs_per_split=1000):
    total_docs = collection.count()
    splits = []

    for i in range(0, total_docs, max_docs_per_split):
        # Get batch of documents
        batch = collection.get(limit=max_docs_per_split, offset=i)

        # Create new collection for this batch
        split_collection = client.create_collection(f"{collection.name}_split_{i//max_docs_per_split}")

        split_collection.add(
            documents=batch["documents"],
            metadatas=batch["metadatas"],
            ids=batch["ids"]
        )

        splits.append(split_collection)

    return splits

# Usage
large_collection = client.get_collection("large_collection")
splits = split_collection(large_collection)
```

## Document Preprocessing

### Text Preprocessing

```python
import re
from typing import List

def preprocess_documents(documents: List[str]) -> List[str]:
    processed = []

    for doc in documents:
        # Remove extra whitespace
        doc = re.sub(r'\s+', ' ', doc.strip())

        # Remove special characters but keep punctuation
        doc = re.sub(r'[^\w\s.,!?-]', '', doc)

        # Normalize case (optional)
        # doc = doc.lower()

        # Remove very short documents
        if len(doc.split()) < 5:
            continue

        processed.append(doc)

    return processed

# Usage
raw_documents = [
    "  Hello   World!   ",
    "This is a test document.",
    "Short"
]

processed = preprocess_documents(raw_documents)
print("Processed documents:", processed)
```

### Document Chunking

```python
def chunk_documents(documents: List[str], chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []

    for doc in documents:
        words = doc.split()

        for i in range(0, len(words), chunk_size - overlap):
            chunk = words[i:i + chunk_size]
            if len(chunk) >= chunk_size * 0.5:  # Avoid very small chunks
                chunks.append(' '.join(chunk))

    return chunks

# Usage
long_document = "Your long document text here..."
chunks = chunk_documents([long_document], chunk_size=100, overlap=20)

print(f"Created {len(chunks)} chunks")
```

## Collection Backup and Recovery

### Backup Operations

```python
import json
import os
from datetime import datetime

def backup_collection(collection, backup_dir="./backups"):
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)

    # Get all data
    data = collection.get(include=["documents", "metadatas", "embeddings"])

    # Create backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/{collection.name}_{timestamp}.json"

    # Save to file
    with open(backup_file, 'w') as f:
        json.dump({
            "collection_name": collection.name,
            "metadata": collection.metadata,
            "data": data,
            "backup_date": timestamp
        }, f, indent=2)

    print(f"Backup saved to: {backup_file}")
    return backup_file

# Usage
backup_file = backup_collection(collection)
```

### Recovery Operations

```python
def restore_collection(backup_file: str):
    # Load backup
    with open(backup_file, 'r') as f:
        backup = json.load(f)

    # Create new collection
    collection = client.create_collection(
        name=f"{backup['collection_name']}_restored",
        metadata=backup['metadata']
    )

    # Restore data
    collection.add(
        documents=backup['data']['documents'],
        metadatas=backup['data']['metadatas'],
        ids=backup['data']['ids']
    )

    print(f"Collection restored: {collection.name}")
    return collection

# Usage
restored_collection = restore_collection(backup_file)
```

## Performance Optimization

### Indexing Strategies

```python
# Optimize for different query patterns
def optimize_collection_for_queries(collection):
    # For metadata filtering heavy workloads
    collection.modify(metadata={
        "index_type": "metadata_optimized",
        "cache_size": "2GB"
    })

    # For similarity search heavy workloads
    collection.modify(metadata={
        "index_type": "similarity_optimized",
        "hnsw_m": 32,
        "hnsw_ef_construction": 200
    })

# Usage
optimize_collection_for_queries(collection)
```

### Memory Management

```python
# Configure memory settings
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(
        chroma_memory_limit=4 * 1024 * 1024 * 1024,  # 4GB
        chroma_cache_size=512 * 1024 * 1024,         # 512MB
        chroma_max_batch_size=1000
    )
)
```

## Collection Monitoring

### Collection Statistics

```python
def get_collection_stats(collection):
    count = collection.count()

    # Get sample of data
    sample = collection.get(limit=100)

    # Calculate statistics
    stats = {
        "total_documents": count,
        "avg_document_length": sum(len(doc.split()) for doc in sample["documents"]) / len(sample["documents"]),
        "metadata_fields": set(),
        "categories": set()
    }

    # Analyze metadata
    for metadata in sample["metadatas"]:
        stats["metadata_fields"].update(metadata.keys())
        if "category" in metadata:
            stats["categories"].add(metadata["category"])

    return stats

# Usage
stats = get_collection_stats(collection)
print("Collection statistics:", stats)
```

## What We've Accomplished

Congratulations! 🎉 You've mastered:

1. **Collection Architecture** - Understanding Chroma's collection system
2. **Document Management** - Adding, updating, and deleting documents
3. **Advanced Document Types** - Structured and multi-modal content
4. **Metadata Strategies** - Hierarchical and validated metadata
5. **Collection Operations** - Merging, splitting, and backup/recovery
6. **Document Preprocessing** - Text cleaning and chunking
7. **Performance Optimization** - Indexing and memory management
8. **Collection Monitoring** - Statistics and analytics

## Next Steps

Ready for more advanced features? In [Chapter 3: Embeddings & Indexing](03-embeddings-indexing.md), we'll explore how Chroma handles embeddings, vector indexing, and similarity search algorithms.

---

**Practice what you've learned:**
1. Create a collection with structured metadata
2. Implement document preprocessing for your use case
3. Set up backup and recovery procedures
4. Experiment with different chunking strategies
5. Build collection monitoring and statistics

*How will you organize your documents in Chroma?* 📚
