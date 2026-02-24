---
layout: default
title: "Chapter 8: Advanced Patterns"
parent: "LanceDB Tutorial"
nav_order: 8
---

# Chapter 8: Advanced Patterns

Welcome to **Chapter 8: Advanced Patterns**. In this part of **LanceDB Tutorial: Serverless Vector Database for AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement multi-tenancy, document chunking, RAG systems, and other advanced patterns for production applications.

## Overview

This chapter covers advanced patterns for building sophisticated applications with LanceDB, including multi-tenant architectures, document processing pipelines, RAG systems, and real-time applications.

## Multi-Tenancy

### Table-Per-Tenant

```python
import lancedb
from typing import Optional

class MultiTenantDB:
    """Multi-tenant LanceDB with table-per-tenant isolation."""

    def __init__(self, uri: str):
        self.db = lancedb.connect(uri)

    def get_table_name(self, tenant_id: str, table_type: str) -> str:
        """Generate tenant-specific table name."""
        return f"tenant_{tenant_id}_{table_type}"

    def create_tenant_table(self, tenant_id: str, table_type: str, schema):
        """Create a table for a tenant."""
        table_name = self.get_table_name(tenant_id, table_type)
        return self.db.create_table(table_name, schema=schema)

    def get_tenant_table(self, tenant_id: str, table_type: str):
        """Get a tenant's table."""
        table_name = self.get_table_name(tenant_id, table_type)
        return self.db.open_table(table_name)

    def search(self, tenant_id: str, table_type: str, query, limit: int = 10):
        """Search within a tenant's table."""
        table = self.get_tenant_table(tenant_id, table_type)
        return table.search(query).limit(limit).to_list()

    def delete_tenant(self, tenant_id: str):
        """Delete all tables for a tenant."""
        prefix = f"tenant_{tenant_id}_"
        for table_name in self.db.table_names():
            if table_name.startswith(prefix):
                self.db.drop_table(table_name)

# Usage
mt_db = MultiTenantDB("s3://bucket/multi-tenant")

# Create tenant tables
mt_db.create_tenant_table("acme", "documents", DocumentSchema)
mt_db.create_tenant_table("globex", "documents", DocumentSchema)

# Search within tenant
results = mt_db.search("acme", "documents", query_vector)
```

### Row-Level Isolation

```python
from lancedb.pydantic import LanceModel, Vector

class TenantDocument(LanceModel):
    """Document with tenant isolation."""
    tenant_id: str
    document_id: str
    content: str
    vector: Vector(384)
    metadata: dict = {}

class RowLevelMultiTenant:
    """Multi-tenant with row-level isolation."""

    def __init__(self, uri: str):
        self.db = lancedb.connect(uri)
        self.table = None

    def initialize(self):
        """Initialize the shared table."""
        self.table = self.db.create_table(
            "documents",
            schema=TenantDocument,
            mode="overwrite"
        )
        # Create index on tenant_id for fast filtering
        self.table.create_scalar_index("tenant_id")

    def add_documents(self, tenant_id: str, documents: list):
        """Add documents for a tenant."""
        for doc in documents:
            doc["tenant_id"] = tenant_id
        self.table.add(documents)

    def search(self, tenant_id: str, query, limit: int = 10):
        """Search with tenant isolation."""
        return self.table.search(query) \
            .where(f"tenant_id = '{tenant_id}'") \
            .limit(limit) \
            .to_list()

    def delete_tenant_data(self, tenant_id: str):
        """Delete all data for a tenant."""
        self.table.delete(f"tenant_id = '{tenant_id}'")

# Usage
mt = RowLevelMultiTenant("./multi-tenant")
mt.initialize()

mt.add_documents("tenant_a", [{"content": "...", "vector": [...]}])
results = mt.search("tenant_a", query_vector)
```

## Document Chunking

### Basic Chunking

```python
from typing import List
import hashlib

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

def chunk_document(doc: dict, chunk_size: int = 1000) -> List[dict]:
    """Chunk a document while preserving metadata."""
    content = doc["content"]
    chunks = chunk_text(content, chunk_size)

    chunked_docs = []
    for i, chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{doc['id']}_{i}".encode()).hexdigest()
        chunked_docs.append({
            "chunk_id": chunk_id,
            "document_id": doc["id"],
            "chunk_index": i,
            "total_chunks": len(chunks),
            "content": chunk,
            **{k: v for k, v in doc.items() if k not in ["id", "content"]}
        })

    return chunked_docs
```

### Semantic Chunking

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticChunker:
    """Chunk documents based on semantic boundaries."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = 0.7

    def chunk(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Split text at semantic boundaries."""
        # Split into sentences
        sentences = self._split_sentences(text)

        # Get embeddings
        embeddings = self.model.encode(sentences)

        # Find semantic boundaries
        chunks = []
        current_chunk = []
        current_embedding = None

        for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
            if current_embedding is None:
                current_chunk.append(sentence)
                current_embedding = embedding
                continue

            # Calculate similarity to current chunk
            similarity = np.dot(current_embedding, embedding) / (
                np.linalg.norm(current_embedding) * np.linalg.norm(embedding)
            )

            chunk_text = " ".join(current_chunk)

            # Start new chunk if semantically different or too long
            if similarity < self.similarity_threshold or len(chunk_text) > max_chunk_size:
                chunks.append(chunk_text)
                current_chunk = [sentence]
                current_embedding = embedding
            else:
                current_chunk.append(sentence)
                # Update embedding as average
                current_embedding = (current_embedding + embedding) / 2

        # Add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
```

### Hierarchical Chunking

```python
class HierarchicalChunker:
    """Create hierarchical chunks (summary + details)."""

    def __init__(self, summarizer, embedder):
        self.summarizer = summarizer
        self.embedder = embedder

    def chunk_hierarchical(self, document: dict) -> dict:
        """Create hierarchical representation."""
        content = document["content"]

        # Level 1: Full document summary
        summary = self.summarizer.summarize(content, max_length=200)

        # Level 2: Section summaries
        sections = self._split_sections(content)
        section_summaries = [
            self.summarizer.summarize(s, max_length=100)
            for s in sections
        ]

        # Level 3: Detailed chunks
        chunks = []
        for i, section in enumerate(sections):
            section_chunks = chunk_text(section, chunk_size=500)
            for j, chunk in enumerate(section_chunks):
                chunks.append({
                    "level": 3,
                    "section_index": i,
                    "chunk_index": j,
                    "content": chunk,
                    "vector": self.embedder.encode(chunk).tolist()
                })

        return {
            "document_id": document["id"],
            "levels": {
                "summary": {
                    "content": summary,
                    "vector": self.embedder.encode(summary).tolist()
                },
                "sections": [
                    {
                        "content": s,
                        "vector": self.embedder.encode(s).tolist()
                    }
                    for s in section_summaries
                ],
                "chunks": chunks
            }
        }

    def _split_sections(self, text: str) -> List[str]:
        """Split text into sections (by headers, paragraphs, etc.)."""
        import re
        # Split on markdown headers or double newlines
        sections = re.split(r'\n#{1,3}\s+|\n\n\n+', text)
        return [s.strip() for s in sections if s.strip()]
```

## RAG Systems

### Basic RAG

```python
import lancedb
from typing import List

class BasicRAG:
    """Basic Retrieval-Augmented Generation system."""

    def __init__(self, db_uri: str, table_name: str, embedder, llm):
        self.db = lancedb.connect(db_uri)
        self.table = self.db.open_table(table_name)
        self.embedder = embedder
        self.llm = llm

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant documents."""
        query_vector = self.embedder.encode(query).tolist()
        results = self.table.search(query_vector).limit(top_k).to_list()
        return [r["content"] for r in results]

    def generate(self, query: str, context: List[str]) -> str:
        """Generate response using retrieved context."""
        context_text = "\n\n---\n\n".join(context)

        prompt = f"""Answer the question based on the provided context.

Context:
{context_text}

Question: {query}

Answer:"""

        return self.llm.generate(prompt)

    def query(self, question: str, top_k: int = 5) -> str:
        """End-to-end RAG query."""
        context = self.retrieve(question, top_k)
        return self.generate(question, context)
```

### Advanced RAG with Reranking

```python
from sentence_transformers import CrossEncoder

class AdvancedRAG:
    """RAG with query expansion, hybrid search, and reranking."""

    def __init__(self, db_uri: str, table_name: str, embedder, llm):
        self.db = lancedb.connect(db_uri)
        self.table = self.db.open_table(table_name)
        self.embedder = embedder
        self.llm = llm
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def expand_query(self, query: str) -> List[str]:
        """Expand query with variations."""
        expansion_prompt = f"""Generate 3 alternative search queries for: "{query}"

Return only the queries, one per line."""

        response = self.llm.generate(expansion_prompt)
        variations = [q.strip() for q in response.strip().split('\n') if q.strip()]
        return [query] + variations[:3]

    def hybrid_retrieve(self, query: str, top_k: int = 20) -> List[dict]:
        """Hybrid retrieval with vector + FTS."""
        query_vector = self.embedder.encode(query).tolist()

        # Vector search
        vector_results = self.table.search(query_vector).limit(top_k).to_list()

        # Full-text search
        fts_results = self.table.search(query, query_type="fts").limit(top_k).to_list()

        # Combine with RRF
        return self._rrf_combine([vector_results, fts_results])

    def rerank(self, query: str, documents: List[dict], top_k: int = 5) -> List[dict]:
        """Rerank documents using cross-encoder."""
        pairs = [(query, doc["content"]) for doc in documents]
        scores = self.reranker.predict(pairs)

        # Sort by score
        scored_docs = list(zip(scores, documents))
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        return [doc for _, doc in scored_docs[:top_k]]

    def query(self, question: str, top_k: int = 5) -> dict:
        """Full RAG pipeline."""
        # 1. Query expansion
        queries = self.expand_query(question)

        # 2. Retrieve for each query variation
        all_results = []
        for q in queries:
            results = self.hybrid_retrieve(q, top_k=20)
            all_results.extend(results)

        # 3. Deduplicate
        seen_ids = set()
        unique_results = []
        for r in all_results:
            if r["id"] not in seen_ids:
                seen_ids.add(r["id"])
                unique_results.append(r)

        # 4. Rerank
        reranked = self.rerank(question, unique_results, top_k)

        # 5. Generate
        context = [r["content"] for r in reranked]
        answer = self.generate(question, context)

        return {
            "answer": answer,
            "sources": reranked,
            "expanded_queries": queries
        }

    def _rrf_combine(self, result_lists: List[List[dict]], k: int = 60) -> List[dict]:
        """Reciprocal Rank Fusion."""
        scores = {}
        for results in result_lists:
            for rank, item in enumerate(results):
                item_id = item["id"]
                if item_id not in scores:
                    scores[item_id] = {"item": item, "score": 0}
                scores[item_id]["score"] += 1 / (k + rank + 1)

        sorted_items = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
        return [item["item"] for item in sorted_items]
```

## Real-Time Applications

### Streaming Ingestion

```python
import asyncio
from collections import deque

class StreamingIngester:
    """Batch and ingest streaming data."""

    def __init__(self, db_uri: str, table_name: str, embedder,
                 batch_size: int = 100, flush_interval: float = 5.0):
        self.db = lancedb.connect(db_uri)
        self.table = self.db.open_table(table_name)
        self.embedder = embedder
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer = deque()
        self._running = False

    async def start(self):
        """Start the background flusher."""
        self._running = True
        asyncio.create_task(self._flush_loop())

    async def stop(self):
        """Stop and flush remaining data."""
        self._running = False
        await self._flush()

    async def ingest(self, document: dict):
        """Add document to buffer."""
        # Embed asynchronously
        vector = await asyncio.to_thread(
            self.embedder.encode,
            document["content"]
        )
        document["vector"] = vector.tolist()
        self.buffer.append(document)

        # Flush if batch size reached
        if len(self.buffer) >= self.batch_size:
            await self._flush()

    async def _flush(self):
        """Flush buffer to database."""
        if not self.buffer:
            return

        # Get all items from buffer
        items = []
        while self.buffer:
            items.append(self.buffer.popleft())

        # Batch insert
        await asyncio.to_thread(self.table.add, items)
        print(f"Flushed {len(items)} documents")

    async def _flush_loop(self):
        """Periodic flush loop."""
        while self._running:
            await asyncio.sleep(self.flush_interval)
            await self._flush()

# Usage
async def main():
    ingester = StreamingIngester("./stream_db", "documents", embedder)
    await ingester.start()

    # Ingest streaming data
    async for doc in get_document_stream():
        await ingester.ingest(doc)

    await ingester.stop()
```

### Change Data Capture

```python
import time
from datetime import datetime

class CDCHandler:
    """Handle change data capture for LanceDB."""

    def __init__(self, db_uri: str, table_name: str):
        self.db = lancedb.connect(db_uri)
        self.table_name = table_name
        self.last_sync_time = None

    def get_changes(self, since: datetime = None) -> dict:
        """Get changes since last sync."""
        table = self.db.open_table(self.table_name)

        if since is None:
            since = self.last_sync_time or datetime.min

        # Get new/updated records
        new_records = table.search(None) \
            .where(f"updated_at > '{since.isoformat()}'") \
            .to_list()

        self.last_sync_time = datetime.utcnow()

        return {
            "changes": new_records,
            "sync_time": self.last_sync_time
        }

    def apply_changes(self, changes: list):
        """Apply changes from source system."""
        table = self.db.open_table(self.table_name)

        for change in changes:
            if change["operation"] == "INSERT":
                table.add([change["data"]])
            elif change["operation"] == "UPDATE":
                table.update(
                    where=f"id = '{change['id']}'",
                    values=change["data"]
                )
            elif change["operation"] == "DELETE":
                table.delete(f"id = '{change['id']}'")
```

## Testing Patterns

### Test Fixtures

```python
import pytest
import lancedb
import tempfile
import numpy as np

@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = lancedb.connect(tmpdir)
        yield db

@pytest.fixture
def sample_table(temp_db):
    """Create sample table with test data."""
    data = [
        {"id": i, "text": f"Document {i}", "vector": np.random.rand(384).tolist()}
        for i in range(100)
    ]
    table = temp_db.create_table("test_table", data)
    return table

def test_search(sample_table):
    """Test basic search functionality."""
    query = np.random.rand(384).tolist()
    results = sample_table.search(query).limit(10).to_list()

    assert len(results) == 10
    assert all("_distance" in r for r in results)

def test_filter(sample_table):
    """Test filtered search."""
    query = np.random.rand(384).tolist()
    results = sample_table.search(query) \
        .where("id < 50") \
        .limit(10) \
        .to_list()

    assert all(r["id"] < 50 for r in results)
```

### Integration Tests

```python
import pytest

@pytest.mark.integration
class TestRAGIntegration:
    """Integration tests for RAG system."""

    @pytest.fixture(autouse=True)
    def setup(self, temp_db, embedder, llm):
        self.rag = BasicRAG(
            db_uri=temp_db.uri,
            table_name="documents",
            embedder=embedder,
            llm=llm
        )
        # Add test documents
        self._add_test_documents()

    def _add_test_documents(self):
        docs = [
            {"content": "LanceDB is a vector database for AI applications."},
            {"content": "Vector search enables semantic similarity matching."},
        ]
        for doc in docs:
            doc["vector"] = self.rag.embedder.encode(doc["content"]).tolist()
        self.rag.table.add(docs)

    def test_retrieve_relevant(self):
        """Test that relevant documents are retrieved."""
        results = self.rag.retrieve("What is LanceDB?")
        assert len(results) > 0
        assert any("LanceDB" in r for r in results)

    def test_end_to_end(self):
        """Test full RAG pipeline."""
        answer = self.rag.query("What is LanceDB used for?")
        assert len(answer) > 0
        assert "vector" in answer.lower() or "ai" in answer.lower()
```

## Summary

In this chapter, you've learned:

- **Multi-Tenancy**: Table-per-tenant and row-level isolation
- **Document Chunking**: Basic, semantic, and hierarchical chunking
- **RAG Systems**: Basic and advanced RAG implementations
- **Real-Time**: Streaming ingestion and CDC patterns
- **Testing**: Fixtures and integration tests

## Key Takeaways

1. **Choose Isolation Level**: Table vs. row-level based on needs
2. **Chunk Intelligently**: Use semantic boundaries when possible
3. **Enhance RAG**: Query expansion + hybrid search + reranking
4. **Handle Streams**: Buffer and batch for efficiency
5. **Test Thoroughly**: Unit and integration tests

## Tutorial Complete!

Congratulations! You've completed the LanceDB Tutorial. You now have the knowledge to:

- Store and query vector data efficiently
- Design schemas for various use cases
- Optimize performance for production
- Deploy with cloud storage backends
- Build sophisticated AI applications

## Next Steps

- Explore the [LanceDB Documentation](https://lancedb.github.io/lancedb/)
- Check out [LanceDB Examples](https://github.com/lancedb/lancedb/tree/main/examples)
- Join the [LanceDB Discord](https://discord.gg/zMM32dvNtd)

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `table`, `query` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Advanced Patterns` as an operating subsystem inside **LanceDB Tutorial: Serverless Vector Database for AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `embedder`, `tenant_id`, `content` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Advanced Patterns` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `table` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `query`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `table` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Production Deployment](07-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
