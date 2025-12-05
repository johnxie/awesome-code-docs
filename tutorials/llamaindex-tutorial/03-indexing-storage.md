---
layout: default
title: "Chapter 3: Indexing & Storage"
parent: "LlamaIndex Tutorial"
nav_order: 3
---

# Chapter 3: Indexing & Storage

> Master the creation of efficient indexes and storage strategies for optimal retrieval performance.

## 🎯 Overview

This chapter covers LlamaIndex's indexing and storage capabilities, showing you how to create different types of indexes, choose appropriate storage backends, and optimize for various use cases. You'll learn to build scalable, high-performance knowledge bases for your RAG applications.

## 🗂️ Understanding Indexes

### Index Types and Use Cases

```python
from llama_index.core import VectorStoreIndex, DocumentSummaryIndex, TreeIndex
from llama_index.core import ListIndex, KeywordTableIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("data").load_data()

def create_different_indexes(documents):
    """Create different types of indexes for comparison"""

    indexes = {}

    # 1. Vector Store Index (most common for RAG)
    print("Creating Vector Store Index...")
    vector_index = VectorStoreIndex.from_documents(documents)
    indexes["vector"] = vector_index
    print(f"✓ Vector index created with {len(documents)} documents")

    # 2. Document Summary Index (for document-level retrieval)
    print("Creating Document Summary Index...")
    summary_index = DocumentSummaryIndex.from_documents(
        documents,
        response_mode="tree_summarize"  # How to generate summaries
    )
    indexes["summary"] = summary_index
    print("✓ Document summary index created")

    # 3. Tree Index (hierarchical structure)
    print("Creating Tree Index...")
    tree_index = TreeIndex.from_documents(documents)
    indexes["tree"] = tree_index
    print("✓ Tree index created")

    # 4. List Index (simple flat structure)
    print("Creating List Index...")
    list_index = ListIndex.from_documents(documents)
    indexes["list"] = list_index
    print("✓ List index created")

    # 5. Keyword Table Index (keyword-based retrieval)
    print("Creating Keyword Table Index...")
    keyword_index = KeywordTableIndex.from_documents(documents)
    indexes["keyword"] = keyword_index
    print("✓ Keyword table index created")

    return indexes

# Usage
indexes = create_different_indexes(documents)

# Query different indexes
query_engine = indexes["vector"].as_query_engine()
response = query_engine.query("What is machine learning?")
print(f"Vector Index Response: {response}")

query_engine = indexes["keyword"].as_query_engine()
response = query_engine.query("machine learning")
print(f"Keyword Index Response: {response}")
```

### Advanced Index Configuration

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SimpleNodeParser, HierarchicalNodeParser
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionPipeline

def create_advanced_index(documents):
    """Create index with advanced configuration"""

    # 1. Configure node parsing
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=1024,
        chunk_overlap=200,
        include_metadata=True,
        include_prev_next_rel=True
    )

    # 2. Configure metadata extractors
    metadata_extractors = [
        TitleExtractor(nodes=5),  # Extract titles from first 5 nodes
        QuestionsAnsweredExtractor(
            questions=3,  # Generate 3 questions per node
            prompt_template="{context_str}\n\nQuestions this content can answer:"
        )
    ]

    # 3. Create ingestion pipeline
    pipeline = IngestionPipeline(
        transformations=[
            node_parser,
            *metadata_extractors
        ]
    )

    # 4. Process documents through pipeline
    nodes = pipeline.run(documents=documents)
    print(f"Processed {len(nodes)} nodes with metadata extraction")

    # 5. Create index with custom storage context
    storage_context = StorageContext.from_defaults()

    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        show_progress=True
    )

    return index

def create_hierarchical_index(documents):
    """Create hierarchical index for complex documents"""

    # Hierarchical node parser for different levels
    node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 512, 128],  # Three levels of hierarchy
        chunk_overlap=100
    )

    # Process documents
    nodes = node_parser.get_nodes_from_documents(documents)
    print(f"Created hierarchical nodes: {len(nodes)} total")

    # Separate by level
    root_nodes = [n for n in nodes if n.parent_node is None]
    child_nodes = [n for n in nodes if n.parent_node is not None]

    print(f"Root nodes: {len(root_nodes)}, Child nodes: {len(child_nodes)}")

    # Create hierarchical index
    index = TreeIndex(nodes)

    return index

# Usage
advanced_index = create_advanced_index(documents)
hierarchical_index = create_hierarchical_index(documents)

# Query with different retrieval modes
query_engine = advanced_index.as_query_engine(
    response_mode="tree_summarize",  # Use tree summarization
    use_async=True  # Enable async processing
)

response = query_engine.query("Summarize the key concepts")
print(f"Advanced query response: {response}")
```

## 💾 Storage Backends

### Vector Store Options

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

def setup_chroma_vector_store():
    """Setup ChromaDB vector store"""
    import chromadb

    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = chroma_client.get_or_create_collection("my_docs")

    # Create vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Create storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context

def setup_pinecone_vector_store():
    """Setup Pinecone vector store"""
    import pinecone

    # Initialize Pinecone
    pinecone.init(api_key="your-pinecone-api-key", environment="us-east-1")

    # Create index if it doesn't exist
    if "my-index" not in pinecone.list_indexes():
        pinecone.create_index(
            name="my-index",
            dimension=1536,  # OpenAI embedding dimension
            metric="cosine"
        )

    # Create vector store
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone.Index("my-index"),
        add_sparse_vector=True  # Enable hybrid search
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context

def setup_weaviate_vector_store():
    """Setup Weaviate vector store"""
    import weaviate

    # Connect to Weaviate
    client = weaviate.Client("http://localhost:8080")

    # Create schema if needed
    schema = {
        "class": "Document",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "metadata", "dataType": ["object"]},
        ],
        "vectorizer": "text2vec-openai"
    }

    if not client.schema.exists("Document"):
        client.schema.create_class(schema)

    # Create vector store
    vector_store = WeaviateVectorStore(
        weaviate_client=client,
        index_name="Document"
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context

def setup_qdrant_vector_store():
    """Setup Qdrant vector store"""
    from qdrant_client import QdrantClient

    # Initialize Qdrant client
    client = QdrantClient("localhost", port=6333)

    # Create collection if needed
    if not client.collection_exists("my_collection"):
        client.create_collection(
            collection_name="my_collection",
            vectors_config={
                "content": {
                    "size": 1536,
                    "distance": "Cosine"
                }
            }
        )

    # Create vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="my_collection"
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context

def create_index_with_vector_store(storage_context, documents):
    """Create index using specified vector store"""

    # Create index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )

    return index

# Usage examples
# ChromaDB
chroma_context = setup_chroma_vector_store()
chroma_index = create_index_with_vector_store(chroma_context, documents)

# Pinecone (requires API key and setup)
# pinecone_context = setup_pinecone_vector_store()
# pinecone_index = create_index_with_vector_store(pinecone_context, documents)

# Weaviate (requires Weaviate instance)
# weaviate_context = setup_weaviate_vector_store()
# weaviate_index = create_index_with_vector_store(weaviate_context, documents)

# Qdrant (requires Qdrant instance)
# qdrant_context = setup_qdrant_vector_store()
# qdrant_index = create_index_with_vector_store(qdrant_context, documents)

print("Vector store indexes created successfully")
```

### Document Store Options

```python
from llama_index.core.storage.docstore import SimpleDocumentStore, MongoDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore, MongoIndexStore
from llama_index.core import StorageContext

def setup_mongodb_storage():
    """Setup MongoDB-based storage"""
    import pymongo

    # Connect to MongoDB
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Create document store
    docstore = MongoDocumentStore(
        mongo_client=mongo_client,
        db_name="llamaindex_db",
        collection_name="documents"
    )

    # Create index store
    index_store = MongoIndexStore(
        mongo_client=mongo_client,
        db_name="llamaindex_db",
        collection_name="indexes"
    )

    # Create storage context
    storage_context = StorageContext.from_defaults(
        docstore=docstore,
        index_store=index_store
    )

    return storage_context

def setup_redis_storage():
    """Setup Redis-based storage for caching"""
    from llama_index.storage.kvstore.redis import RedisKVStore
    from llama_index.core.storage.index_store import KVIndexStore

    # Create Redis KV store
    kv_store = RedisKVStore(
        redis_uri="redis://localhost:6379",
        namespace="llamaindex"
    )

    # Create index store using Redis
    index_store = KVIndexStore(kv_store=kv_store)

    storage_context = StorageContext.from_defaults(
        index_store=index_store
    )

    return storage_context

def setup_s3_storage():
    """Setup S3-based storage for large datasets"""
    import boto3
    from llama_index.storage.docstore import SimpleDocumentStore

    # Configure S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id='your-access-key',
        aws_secret_access_key='your-secret-key',
        region_name='us-east-1'
    )

    # Create custom document store that uses S3
    class S3DocumentStore(SimpleDocumentStore):
        def __init__(self, s3_client, bucket_name):
            super().__init__()
            self.s3_client = s3_client
            self.bucket_name = bucket_name

        def persist(self, persist_dir="./storage"):
            """Persist to S3 instead of local disk"""
            import pickle
            import io

            # Serialize documents
            data = pickle.dumps(self.docs)
            buffer = io.BytesIO(data)

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key="llamaindex_documents.pkl",
                Body=buffer.getvalue()
            )

        def load_from_s3(self):
            """Load documents from S3"""
            try:
                response = self.s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key="llamaindex_documents.pkl"
                )
                data = response['Body'].read()
                self.docs = pickle.loads(data)
            except:
                print("No existing documents found in S3")

    # Create S3 document store
    docstore = S3DocumentStore(s3_client, "my-llamaindex-bucket")
    docstore.load_from_s3()

    storage_context = StorageContext.from_defaults(docstore=docstore)

    return storage_context

# Usage
# MongoDB storage
mongo_context = setup_mongodb_storage()
mongo_index = VectorStoreIndex.from_documents(documents, storage_context=mongo_context)

# Redis storage (for caching)
redis_context = setup_redis_storage()
redis_index = VectorStoreIndex.from_documents(documents, storage_context=redis_context)

# S3 storage (for large datasets)
# s3_context = setup_s3_storage()
# s3_index = VectorStoreIndex.from_documents(documents, storage_context=s3_context)

print("Document stores configured successfully")
```

## 🔄 Index Persistence and Loading

### Saving and Loading Indexes

```python
from llama_index.core import load_index_from_storage, StorageContext
import os

def save_index_to_disk(index, index_name="my_index"):
    """Save index to disk for persistence"""

    # Create directory for index
    index_dir = f"./storage/{index_name}"
    os.makedirs(index_dir, exist_ok=True)

    # Persist index
    index.storage_context.persist(persist_dir=index_dir)

    print(f"Index saved to {index_dir}")

    return index_dir

def load_index_from_disk(index_dir):
    """Load index from disk"""

    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)

    # Load index
    index = load_index_from_storage(storage_context)

    print(f"Index loaded from {index_dir}")

    return index

def save_multiple_indexes(indexes_dict):
    """Save multiple indexes with metadata"""

    # Save each index
    saved_indexes = {}
    for name, index in indexes_dict.items():
        index_dir = save_index_to_disk(index, f"indexes/{name}")
        saved_indexes[name] = {
            "path": index_dir,
            "type": type(index).__name__,
            "created_at": time.time()
        }

    # Save metadata
    import json
    with open("./storage/index_metadata.json", "w") as f:
        json.dump(saved_indexes, f, indent=2)

    print(f"Saved {len(saved_indexes)} indexes with metadata")

    return saved_indexes

def load_multiple_indexes(metadata_file="./storage/index_metadata.json"):
    """Load multiple indexes from metadata"""

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    loaded_indexes = {}
    for name, info in metadata.items():
        try:
            index = load_index_from_disk(info["path"])
            loaded_indexes[name] = {
                "index": index,
                "type": info["type"],
                "created_at": info["created_at"],
                "path": info["path"]
            }
            print(f"✓ Loaded {name} ({info['type']})")
        except Exception as e:
            print(f"✗ Failed to load {name}: {e}")

    return loaded_indexes

def incremental_index_update(existing_index, new_documents):
    """Update existing index with new documents incrementally"""

    # Insert new documents
    for doc in new_documents:
        existing_index.insert(doc)

    # Refresh index mappings if needed
    existing_index.refresh_reflectors()

    # Save updated index
    index_dir = save_index_to_disk(existing_index, "updated_index")

    print(f"Index updated with {len(new_documents)} new documents")

    return existing_index

# Usage
# Save index
index_dir = save_index_to_disk(vector_index, "my_vector_index")

# Load index
loaded_index = load_index_from_disk(index_dir)

# Test loaded index
query_engine = loaded_index.as_query_engine()
response = query_engine.query("Test query")
print(f"Loaded index response: {response}")

# Save multiple indexes
indexes = {
    "vector": vector_index,
    "summary": DocumentSummaryIndex.from_documents(documents),
    "keyword": KeywordTableIndex.from_documents(documents)
}
save_multiple_indexes(indexes)

# Load multiple indexes
loaded_indexes = load_multiple_indexes()
print(f"Loaded {len(loaded_indexes)} indexes")
```

### Index Versioning and Rollback

```python
import json
from datetime import datetime

class IndexVersionManager:
    def __init__(self, base_dir="./storage/versions"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create_version(self, index, version_name=None, description=""):
        """Create a new version of the index"""

        # Generate version name if not provided
        if version_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_name = f"v_{timestamp}"

        version_dir = os.path.join(self.base_dir, version_name)
        os.makedirs(version_dir, exist_ok=True)

        # Save index
        index.storage_context.persist(persist_dir=version_dir)

        # Save metadata
        metadata = {
            "version_name": version_name,
            "created_at": datetime.now().isoformat(),
            "description": description,
            "index_type": type(index).__name__,
            "document_count": len(index.docstore.docs) if hasattr(index, 'docstore') else "unknown",
            "index_stats": self._get_index_stats(index)
        }

        metadata_file = os.path.join(version_dir, "version_metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        # Update versions registry
        self._update_versions_registry(version_name, metadata)

        print(f"Created index version: {version_name}")
        return version_name

    def list_versions(self):
        """List all available versions"""
        registry_file = os.path.join(self.base_dir, "versions_registry.json")

        if not os.path.exists(registry_file):
            return []

        with open(registry_file, "r") as f:
            registry = json.load(f)

        return registry

    def load_version(self, version_name):
        """Load a specific version of the index"""
        version_dir = os.path.join(self.base_dir, version_name)

        if not os.path.exists(version_dir):
            raise ValueError(f"Version {version_name} does not exist")

        # Load index
        storage_context = StorageContext.from_defaults(persist_dir=version_dir)
        index = load_index_from_storage(storage_context)

        print(f"Loaded index version: {version_name}")
        return index

    def rollback_to_version(self, version_name):
        """Rollback to a previous version"""
        if version_name not in [v["version_name"] for v in self.list_versions()]:
            raise ValueError(f"Version {version_name} not found")

        # Load the specified version
        index = self.load_version(version_name)

        # Make it the current active version
        current_dir = os.path.join(self.base_dir, "current")
        if os.path.exists(current_dir):
            import shutil
            shutil.rmtree(current_dir)

        # Copy version to current
        shutil.copytree(
            os.path.join(self.base_dir, version_name),
            current_dir
        )

        print(f"Rolled back to version: {version_name}")
        return index

    def compare_versions(self, version1, version2):
        """Compare two versions"""
        v1_metadata = self._get_version_metadata(version1)
        v2_metadata = self._get_version_metadata(version2)

        comparison = {
            "version1": version1,
            "version2": version2,
            "document_count_diff": v2_metadata["document_count"] - v1_metadata["document_count"],
            "created_diff_days": (
                datetime.fromisoformat(v2_metadata["created_at"]) -
                datetime.fromisoformat(v1_metadata["created_at"])
            ).days,
            "v1_stats": v1_metadata["index_stats"],
            "v2_stats": v2_metadata["index_stats"]
        }

        return comparison

    def _update_versions_registry(self, version_name, metadata):
        """Update the versions registry"""
        registry_file = os.path.join(self.base_dir, "versions_registry.json")

        # Load existing registry
        registry = []
        if os.path.exists(registry_file):
            with open(registry_file, "r") as f:
                registry = json.load(f)

        # Add new version
        registry.append(metadata)

        # Save updated registry
        with open(registry_file, "w") as f:
            json.dump(registry, f, indent=2)

    def _get_version_metadata(self, version_name):
        """Get metadata for a specific version"""
        metadata_file = os.path.join(self.base_dir, version_name, "version_metadata.json")

        with open(metadata_file, "r") as f:
            return json.load(f)

    def _get_index_stats(self, index):
        """Get statistics about the index"""
        stats = {}

        try:
            if hasattr(index, 'docstore') and hasattr(index.docstore, 'docs'):
                stats["document_count"] = len(index.docstore.docs)

            if hasattr(index, 'index_struct'):
                stats["index_structure"] = str(type(index.index_struct))

            if hasattr(index, 'vector_store'):
                stats["vector_store_type"] = type(index.vector_store).__name__

        except Exception as e:
            stats["error"] = str(e)

        return stats

# Usage
version_manager = IndexVersionManager()

# Create versions
v1 = version_manager.create_version(vector_index, "v1.0", "Initial index with base documents")
v2 = version_manager.create_version(vector_index, "v1.1", "Updated with additional documents")

# List versions
versions = version_manager.list_versions()
print("Available versions:")
for v in versions:
    print(f"  {v['version_name']}: {v['description']} ({v['created_at']})")

# Load specific version
old_index = version_manager.load_version("v1.0")

# Compare versions
comparison = version_manager.compare_versions("v1.0", "v1.1")
print(f"Version comparison: {comparison['document_count_diff']} documents added")

# Rollback if needed
# rolled_back_index = version_manager.rollback_to_version("v1.0")
```

## ⚡ Performance Optimization

### Index Optimization Techniques

```python
from llama_index.core.postprocessor import SimilarityPostprocessor, KeywordNodePostprocessor
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

def optimize_index_performance(index):
    """Apply performance optimizations to index"""

    optimizations = {}

    # 1. Similarity threshold filtering
    similarity_filter = SimilarityPostprocessor(similarity_cutoff=0.7)
    optimizations["similarity_filter"] = similarity_filter

    # 2. Keyword-based filtering
    keyword_filter = KeywordNodePostprocessor(
        required_keywords=["important", "key", "critical"],
        exclude_keywords=["obsolete", "deprecated"]
    )
    optimizations["keyword_filter"] = keyword_filter

    # 3. Optimized retriever configuration
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,  # Retrieve more candidates for re-ranking
        vector_store_query_mode="default"  # or "hybrid" for mixed search
    )
    optimizations["optimized_retriever"] = retriever

    # 4. Create optimized query engine
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=[similarity_filter, keyword_filter],
        response_mode="tree_summarize",
        use_async=True
    )
    optimizations["optimized_query_engine"] = query_engine

    return optimizations

def benchmark_index_performance(index, test_queries):
    """Benchmark index performance"""

    import time

    results = {
        "queries": [],
        "avg_response_time": 0,
        "total_queries": len(test_queries),
        "successful_queries": 0
    }

    query_engine = index.as_query_engine()

    for query in test_queries:
        start_time = time.time()

        try:
            response = query_engine.query(query)
            response_time = time.time() - start_time

            results["queries"].append({
                "query": query,
                "response_time": response_time,
                "response_length": len(response.response) if hasattr(response, 'response') else 0,
                "success": True
            })

            results["successful_queries"] += 1

        except Exception as e:
            response_time = time.time() - start_time
            results["queries"].append({
                "query": query,
                "response_time": response_time,
                "error": str(e),
                "success": False
            })

    # Calculate statistics
    response_times = [q["response_time"] for q in results["queries"]]
    results["avg_response_time"] = sum(response_times) / len(response_times)
    results["min_response_time"] = min(response_times)
    results["max_response_time"] = max(response_times)
    results["p95_response_time"] = sorted(response_times)[int(len(response_times) * 0.95)]

    return results

def create_index_sharding_strategy(documents, num_shards=4):
    """Create sharded index for better performance"""

    # Split documents into shards
    shard_size = len(documents) // num_shards
    shards = []

    for i in range(num_shards):
        start_idx = i * shard_size
        end_idx = start_idx + shard_size if i < num_shards - 1 else len(documents)
        shard_docs = documents[start_idx:end_idx]

        # Create index for this shard
        shard_index = VectorStoreIndex.from_documents(shard_docs)
        shards.append({
            "index": shard_index,
            "shard_id": i,
            "document_count": len(shard_docs)
        })

    print(f"Created {num_shards} shards with average {shard_size} documents each")

    return shards

def query_sharded_indexes(shards, query):
    """Query across multiple shards"""

    all_results = []

    # Query each shard
    for shard in shards:
        query_engine = shard["index"].as_query_engine()
        response = query_engine.query(query)
        all_results.append({
            "shard_id": shard["shard_id"],
            "response": response,
            "score": getattr(response, 'score', 0.5)  # Assuming score attribute
        })

    # Combine results (simple approach - take best from each shard)
    # In production, you'd implement more sophisticated combination
    combined_results = sorted(all_results, key=lambda x: x["score"], reverse=True)

    return combined_results[:3]  # Return top 3 results

# Usage
# Optimize index
optimizations = optimize_index_performance(vector_index)
optimized_engine = optimizations["optimized_query_engine"]

# Benchmark performance
test_queries = [
    "What is machine learning?",
    "How do neural networks work?",
    "Explain data science concepts"
]

benchmark_results = benchmark_index_performance(vector_index, test_queries)
print(f"Benchmark: {benchmark_results['successful_queries']}/{benchmark_results['total_queries']} successful")
print(f"Average response time: {benchmark_results['avg_response_time']:.3f}s")

# Sharding for large datasets
if len(documents) > 1000:
    shards = create_index_sharding_strategy(documents, num_shards=4)
    sharded_results = query_sharded_indexes(shards, "What is AI?")
    print(f"Sharded query returned {len(sharded_results)} results")
```

## 🎯 Best Practices

### Index Selection Guidelines

| Use Case | Recommended Index | Rationale |
|:---------|:------------------|:----------|
| **General Q&A** | VectorStoreIndex | Semantic search with embeddings |
| **Document Summaries** | DocumentSummaryIndex | Document-level retrieval |
| **Hierarchical Data** | TreeIndex | Structured document organization |
| **Simple Lists** | ListIndex | Flat document collections |
| **Keyword Search** | KeywordTableIndex | Exact keyword matching |
| **Hybrid Search** | Custom combination | Best of multiple approaches |

### Storage Backend Selection

| Requirement | Recommended Backend | Benefits |
|:------------|:--------------------|:---------|
| **Development** | ChromaDB | Easy setup, good for prototyping |
| **Production** | Pinecone/Weaviate | Scalable, managed vector search |
| **Large Scale** | Qdrant | High performance, advanced features |
| **Document Storage** | MongoDB | Flexible document storage |
| **Caching** | Redis | Fast access, session storage |
| **Cost Effective** | Local storage | No cloud costs, full control |

### Performance Optimization Tips

1. **Choose Right Chunk Size**: Balance between context and specificity
2. **Use Appropriate Embeddings**: Match embedding model to your domain
3. **Implement Caching**: Cache frequent queries and embeddings
4. **Batch Operations**: Process multiple queries together
5. **Index Regularly**: Keep indexes updated with fresh data
6. **Monitor Usage**: Track query patterns and performance metrics
7. **Scale Horizontally**: Use sharding for large document collections

## 📈 Next Steps

With indexing and storage mastered, you're ready to:

- **[Chapter 4: Query Engines & Retrieval](04-query-engines.md)** - Build sophisticated query and retrieval systems
- **[Chapter 5: Advanced RAG Patterns](05-advanced-rag.md)** - Multi-modal, agent-based, and hybrid approaches
- **[Chapter 6: Custom Components](06-custom-components.md)** - Building custom loaders, indexes, and query engines

---

**Ready to build powerful query engines? Continue to [Chapter 4: Query Engines & Retrieval](04-query-engines.md)!** 🚀