---
layout: default
title: "Chapter 1: Getting Started with Chroma"
parent: "Chroma Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Chroma

Welcome to Chroma! If you've ever wanted to build AI applications with a sophisticated memory system, you're in the right place. Chroma is the AI-native open-source embedding database that makes it easy to add persistent memory and fast retrieval to your AI applications.

## What Makes Chroma Special?

Chroma revolutionizes how we think about data storage for AI applications by:

- **AI-Native Design** - Built specifically for embeddings and vector operations
- **Simple API** - Easy to use with minimal setup required
- **Fast Retrieval** - Optimized for similarity search and nearest neighbor queries
- **Metadata Support** - Rich filtering and organization capabilities
- **Multi-Modal** - Supports text, images, and structured data
- **Production Ready** - Scalable architecture with persistence and backup

## Installing Chroma

### Local Installation

```bash
# Install Chroma using pip
pip install chromadb

# Or install with additional dependencies
pip install chromadb[all]

# For development and testing
pip install chromadb[dev]
```

### Docker Setup

```bash
# Run Chroma with Docker
docker run -p 8000:8000 chromadb/chroma

# Or use Docker Compose
docker-compose up chroma
```

### Cloud Deployment

```bash
# Deploy to cloud platforms
# Chroma supports various cloud deployments
pip install chromadb[cloud]
```

## Your First Chroma Collection

Let's create your first vector database and add some data:

```python
import chromadb

# Initialize Chroma client
client = chromadb.Client()

# Create a collection (like a table in traditional databases)
collection = client.create_collection(name="my_first_collection")

# Add some documents with metadata
documents = [
    "The quick brown fox jumps over the lazy dog",
    "Python is a programming language",
    "Machine learning is fascinating",
    "Chroma is great for AI applications"
]

metadata = [
    {"source": "example", "category": "animal"},
    {"source": "example", "category": "programming"},
    {"source": "example", "category": "ai"},
    {"source": "example", "category": "ai"}
]

ids = ["doc1", "doc2", "doc3", "doc4"]

# Add documents to the collection
collection.add(
    documents=documents,
    metadatas=metadata,
    ids=ids
)

print(f"Added {len(documents)} documents to collection")
```

## Understanding Embeddings

### What are Embeddings?

Embeddings are numerical representations of data that capture semantic meaning:

```python
# Chroma automatically generates embeddings for your documents
# Let's see what the embeddings look like
results = collection.get(include=['embeddings'])
print("Embedding dimensions:", len(results['embeddings'][0]))

# Embeddings are high-dimensional vectors
print("Sample embedding:", results['embeddings'][0][:5], "...")
```

### Custom Embedding Functions

```python
import chromadb
from chromadb.utils import embedding_functions

# Use different embedding models
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-openai-key",
    model_name="text-embedding-ada-002"
)

# Create collection with custom embeddings
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=openai_ef
)

# Add documents (embeddings generated automatically)
collection.add(
    documents=["Hello world", "How are you?"],
    ids=["doc1", "doc2"]
)
```

## Basic Queries

### Similarity Search

```python
# Query for similar documents
results = collection.query(
    query_texts=["fast animals"],
    n_results=2
)

print("Query results:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")
```

### Metadata Filtering

```python
# Query with metadata filters
results = collection.query(
    query_texts=["artificial intelligence"],
    n_results=3,
    where={"category": "ai"}
)

print("Filtered results:")
for doc in results['documents'][0]:
    print(f"- {doc}")
```

## Chroma Architecture

### Core Components

```mermaid
graph TD
    A[Client] --> B[API Server]
    B --> C[Vector Database]
    C --> D[Embedding Function]
    C --> E[Metadata Store]
    C --> F[Index Manager]

    D --> G[OpenAI/Sentence Transformers]
    E --> H[SQLite/PostgreSQL]
    F --> I[HNSW/IVF]

    classDef client fill:#e1f5fe,stroke:#01579b
    classDef core fill:#f3e5f5,stroke:#4a148c
    classDef storage fill:#fff3e0,stroke:#ef6c00

    class A client
    class B,C core
    class D,E,F,G,H,I storage
```

### Data Flow

1. **Document Input** - You provide text documents
2. **Embedding Generation** - Chroma converts text to vectors
3. **Storage** - Vectors stored with metadata
4. **Indexing** - Efficient search structures created
5. **Query Processing** - Fast similarity search
6. **Results** - Relevant documents returned

## Persistence and Configuration

### Persistent Storage

```python
# Persistent client (data survives restarts)
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.create_collection(name="persistent_collection")

# Data persists between sessions
collection.add(
    documents=["Persistent storage example"],
    ids=["persistent_doc"]
)
```

### Configuration Options

```python
# Advanced configuration
client = chromadb.Client(Settings(
    chroma_server_host="localhost",
    chroma_server_http_port=8000,
    chroma_api_impl="rest",
    anonymized_telemetry=False
))
```

## Working with Collections

### Collection Management

```python
# List all collections
collections = client.list_collections()
print("Available collections:", [c.name for c in collections])

# Get existing collection
collection = client.get_collection(name="my_collection")

# Delete collection
client.delete_collection(name="old_collection")

# Collection info
print(f"Collection: {collection.name}")
print(f"Count: {collection.count()}")
```

### Collection Metadata

```python
# Add collection-level metadata
collection = client.create_collection(
    name="advanced_collection",
    metadata={"description": "Advanced AI collection", "version": "1.0"}
)

# Update collection metadata
collection.modify(metadata={"version": "1.1"})
```

## Error Handling and Best Practices

### Error Handling

```python
try:
    collection = client.create_collection(name="test_collection")
    collection.add(
        documents=["Test document"],
        ids=["test_id"]
    )
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
```

### Best Practices

```python
# Use meaningful IDs
collection.add(
    documents=["Important document"],
    ids=["important_doc_001"]  # Not just "1"
)

# Add comprehensive metadata
collection.add(
    documents=["Document content"],
    metadatas=[{
        "source": "user_input",
        "timestamp": "2024-01-01",
        "category": "important",
        "tags": ["urgent", "review"]
    }],
    ids=["doc_001"]
)

# Use batch operations for performance
batch_size = 100
for i in range(0, len(all_documents), batch_size):
    batch = all_documents[i:i+batch_size]
    collection.add(
        documents=batch,
        ids=[f"doc_{j}" for j in range(i, i+len(batch))]
    )
```

## Integration Examples

### With LangChain

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Create Chroma vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    collection_name="langchain_collection",
    embedding_function=embeddings
)

# Add documents
vectorstore.add_texts([
    "LangChain is a framework for developing applications powered by language models",
    "Chroma provides the vector storage backend"
])

# Query
results = vectorstore.similarity_search("language model framework", k=2)
```

### With LlamaIndex

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage import StorageContext

# Create Chroma vector store
chroma_store = ChromaVectorStore(chroma_collection=collection)

# Create storage context
storage_context = StorageContext.from_defaults(vector_store=chroma_store)

# Create index
index = VectorStoreIndex.from_documents(
    documents=documents,
    storage_context=storage_context
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is Chroma?")
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed Chroma** and set up your development environment
2. **Created your first collection** and added documents with metadata
3. **Generated embeddings** and understood their role in AI applications
4. **Performed similarity searches** to find relevant documents
5. **Implemented metadata filtering** for advanced queries
6. **Set up persistent storage** for production use
7. **Integrated Chroma** with popular AI frameworks

## Next Steps

Now that you understand Chroma's fundamentals, let's explore more advanced features. In [Chapter 2: Collections & Documents](02-collections-documents.md), we'll dive deeper into managing collections, handling different document types, and optimizing storage strategies.

---

**Practice what you've learned:**
1. Create a collection for your personal notes or documents
2. Experiment with different embedding functions
3. Try various query patterns and metadata filters
4. Build a simple document search application

*What kind of AI application are you excited to build with Chroma?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `collection`, `documents`, `client` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Chroma` as an operating subsystem inside **ChromaDB Tutorial: Building AI-Native Vector Databases**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Chroma`, `print`, `chromadb` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Chroma` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `collection`.
2. **Input normalization**: shape incoming data so `documents` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `client`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/chroma-core/chroma)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `collection` and `documents` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Collections & Documents](02-collections-documents.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
