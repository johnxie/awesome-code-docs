---
layout: default
title: "LocalAI Tutorial - Chapter 6: Embeddings"
nav_order: 6
has_children: false
parent: LocalAI Tutorial
---

# Chapter 6: Vector Embeddings for RAG

> Generate embeddings locally and build semantic search applications with LocalAI.

## Overview

LocalAI supports various embedding models for generating vector representations of text, enabling semantic search and RAG (Retrieval-Augmented Generation) applications.

## Installing Embedding Models

### Sentence Transformers

```bash
# Install popular embedding models
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "text-embedding-ada-002"}'

# All-MiniLM models (fast, good quality)
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "all-minilm-l6-v2"}'

# BGE models (high quality)
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "bge-large-en-v1.5"}'
```

## Basic Embeddings

### Single Text Embedding

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

# Generate embedding
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Hello, world!"
)

embedding = response.data[0].embedding
print(f"Embedding dimension: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
```

### Batch Embeddings

```python
# Embed multiple texts
texts = [
    "The cat sits on the mat",
    "A feline rests on a rug",
    "Python is a programming language",
    "Machine learning is fascinating"
]

response = client.embeddings.create(
    model="all-minilm-l6-v2",
    input=texts
)

embeddings = [data.embedding for data in response.data]
print(f"Generated {len(embeddings)} embeddings")
print(f"Each embedding has {len(embeddings[0])} dimensions")
```

## Semantic Search Implementation

### Vector Search Class

```python
import numpy as np
from typing import List, Tuple

class SemanticSearch:
    def __init__(self, model="all-minilm-l6-v2"):
        self.client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")
        self.model = model
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents: List[str]):
        """Add documents to the search index."""
        if not documents:
            return

        # Generate embeddings for new documents
        response = self.client.embeddings.create(
            model=self.model,
            input=documents
        )

        new_embeddings = [data.embedding for data in response.data]

        # Add to index
        self.documents.extend(documents)
        self.embeddings.extend(new_embeddings)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search for most similar documents."""
        # Generate query embedding
        response = self.client.embeddings.create(
            model=self.model,
            input=[query]
        )
        query_embedding = response.data[0].embedding

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            # Cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((self.documents[i], similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

# Usage
search = SemanticSearch()

# Add documents
docs = [
    "Python is a high-level programming language known for its simplicity.",
    "Machine learning algorithms can learn patterns from data.",
    "Neural networks are inspired by the human brain structure.",
    "Data science combines statistics, programming, and domain expertise.",
    "Natural language processing helps computers understand human language."
]

search.add_documents(docs)

# Search
results = search.search("artificial intelligence and programming", top_k=3)
for doc, score in results:
    print(f"Score: {score:.3f} - {doc}")
```

## RAG (Retrieval-Augmented Generation)

### Basic RAG Implementation

```python
class RAGChatbot:
    def __init__(self):
        self.search = SemanticSearch()
        self.client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

    def add_knowledge_base(self, documents: List[str]):
        """Add documents to knowledge base."""
        self.search.add_documents(documents)

    def chat(self, query: str, context_docs: int = 3) -> str:
        """Answer query using retrieved context."""
        # Retrieve relevant documents
        relevant_docs = self.search.search(query, top_k=context_docs)

        # Build context
        context = "\n".join([doc for doc, _ in relevant_docs])

        # Generate response with context
        prompt = f"""
Use the following information to answer the question. If the information doesn't contain the answer, say so.

Context:
{context}

Question: {query}

Answer:"""

        response = self.client.chat.completions.create(
            model="phi-2",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.1  # Low temperature for factual responses
        )

        return response.choices[0].message.content

# Usage
rag_bot = RAGChatbot()

# Add knowledge base
knowledge = [
    "The capital of France is Paris. It has a population of over 2 million people.",
    "Python was created by Guido van Rossum and first released in 1991.",
    "Machine learning is a subset of artificial intelligence focused on algorithms that learn from data.",
    "The Earth orbits around the Sun once every 365.25 days, which is why we have leap years.",
    "Photosynthesis is the process by which plants convert sunlight into energy."
]

rag_bot.add_knowledge_base(knowledge)

# Ask questions
questions = [
    "What is the capital of France?",
    "Who created Python?",
    "How does machine learning work?"
]

for question in questions:
    answer = rag_bot.chat(question)
    print(f"Q: {question}")
    print(f"A: {answer}")
    print("-" * 50)
```

## Advanced Embedding Techniques

### Hybrid Search

```python
class HybridSearch:
    def __init__(self):
        self.semantic_search = SemanticSearch()
        self.keyword_index = {}  # Simple keyword index

    def add_documents(self, documents: List[str]):
        """Add documents with both semantic and keyword indexing."""
        self.semantic_search.add_documents(documents)

        # Build keyword index
        for i, doc in enumerate(documents):
            words = doc.lower().split()
            for word in words:
                if word not in self.keyword_index:
                    self.keyword_index[word] = []
                self.keyword_index[word].append(i)

    def hybrid_search(self, query: str, semantic_weight: float = 0.7, top_k: int = 5):
        """Combine semantic and keyword search."""
        # Semantic search
        semantic_results = self.semantic_search.search(query, top_k=top_k*2)

        # Keyword search
        query_words = query.lower().split()
        keyword_scores = {}

        for word in query_words:
            if word in self.keyword_index:
                for doc_idx in self.keyword_index[word]:
                    keyword_scores[doc_idx] = keyword_scores.get(doc_idx, 0) + 1

        # Normalize keyword scores
        max_keyword_score = max(keyword_scores.values()) if keyword_scores else 1
        keyword_results = [
            (self.semantic_search.documents[idx], score / max_keyword_score)
            for idx, score in keyword_scores.items()
        ]
        keyword_results.sort(key=lambda x: x[1], reverse=True)

        # Combine results
        combined_scores = {}

        # Add semantic scores
        for doc, score in semantic_results:
            combined_scores[doc] = semantic_weight * score

        # Add keyword scores
        for doc, score in keyword_results[:top_k]:
            combined_scores[doc] = combined_scores.get(doc, 0) + (1 - semantic_weight) * score

        # Sort and return top results
        final_results = [(doc, score) for doc, score in combined_scores.items()]
        final_results.sort(key=lambda x: x[1], reverse=True)

        return final_results[:top_k]

# Usage
hybrid = HybridSearch()
hybrid.add_documents(knowledge)

results = hybrid.hybrid_search("Python programming language", semantic_weight=0.6)
for doc, score in results:
    print(f"Score: {score:.3f} - {doc}")
```

## Embedding Model Comparison

### Performance Benchmarking

```python
def benchmark_embedding_models(models, test_texts):
    """Compare embedding model performance."""
    results = {}

    for model in models:
        print(f"Testing {model}...")

        start_time = time.time()

        try:
            response = client.embeddings.create(
                model=model,
                input=test_texts
            )

            end_time = time.time()
            duration = end_time - start_time

            embedding_dim = len(response.data[0].embedding)
            tokens_per_sec = len(test_texts) / duration

            results[model] = {
                "success": True,
                "dimension": embedding_dim,
                "speed": tokens_per_sec,
                "duration": duration
            }

        except Exception as e:
            results[model] = {
                "success": False,
                "error": str(e)
            }

    return results

# Test different models
models_to_test = ["all-minilm-l6-v2", "text-embedding-ada-002", "bge-base-en-v1.5"]
test_texts = ["Hello world", "Machine learning", "Python programming"] * 10  # 30 texts

benchmark_results = benchmark_embedding_models(models_to_test, test_texts)

for model, result in benchmark_results.items():
    if result["success"]:
        print(f"{model}: {result['dimension']}D, {result['speed']:.2f} texts/sec")
    else:
        print(f"{model}: Failed - {result['error']}")
```

## Vector Database Integration

### Simple In-Memory Vector Store

```python
class VectorStore:
    def __init__(self, embedding_model="all-minilm-l6-v2"):
        self.client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")
        self.embedding_model = embedding_model
        self.vectors = []
        self.metadata = []

    def add_texts(self, texts: List[str], metadata: List[dict] = None):
        """Add texts with optional metadata."""
        if metadata is None:
            metadata = [{}] * len(texts)

        # Generate embeddings
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )

        embeddings = [data.embedding for data in response.data]

        # Store
        self.vectors.extend(embeddings)
        self.metadata.extend(metadata)

    def similarity_search(self, query: str, top_k: int = 5):
        """Search for similar texts."""
        # Generate query embedding
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=[query]
        )
        query_vector = response.data[0].embedding

        # Calculate similarities
        similarities = []
        for i, vector in enumerate(self.vectors):
            similarity = np.dot(query_vector, vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(vector)
            )
            similarities.append((similarity, i))

        # Sort by similarity
        similarities.sort(reverse=True, key=lambda x: x[0])

        # Return results with metadata
        results = []
        for similarity, idx in similarities[:top_k]:
            results.append({
                "similarity": similarity,
                "metadata": self.metadata[idx],
                "index": idx
            })

        return results

# Usage
store = VectorStore()

# Add documents with metadata
documents = [
    "Python is a versatile programming language.",
    "Machine learning uses statistical techniques.",
    "Data science combines domain expertise with programming.",
    "Neural networks can learn complex patterns."
]

metadata = [
    {"category": "programming", "language": "python"},
    {"category": "ml", "topic": "fundamentals"},
    {"category": "data", "field": "science"},
    {"category": "ml", "topic": "neural_networks"}
]

store.add_texts(documents, metadata)

# Search
results = store.similarity_search("artificial intelligence algorithms", top_k=3)
for result in results:
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Category: {result['metadata']['category']}")
    print(f"Document index: {result['index']}")
    print("-" * 30)
```

## Chunking Strategies

### Document Chunking for RAG

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks

def prepare_documents_for_rag(file_paths: List[str], chunk_size: int = 500):
    """Prepare documents for RAG by chunking and embedding."""
    all_chunks = []
    all_metadata = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chunk the document
        chunks = chunk_text(content, chunk_size=chunk_size, overlap=50)

        # Add metadata
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                "source": file_path,
                "chunk_id": i,
                "total_chunks": len(chunks)
            })

    return all_chunks, all_metadata

# Usage
file_paths = ["document1.txt", "document2.txt"]
chunks, metadata = prepare_documents_for_rag(file_paths)

# Add to vector store
store = VectorStore()
store.add_texts(chunks, metadata)

# Query
query = "What are the main benefits of machine learning?"
results = store.similarity_search(query, top_k=3)

for result in results:
    print(f"Source: {result['metadata']['source']}")
    print(f"Chunk: {result['metadata']['chunk_id']}")
    print(f"Similarity: {result['similarity']:.3f}")
    print("-" * 40)
```

## Best Practices

1. **Model Selection**: Choose embedding models based on your use case and performance requirements
2. **Chunking**: Split long documents into meaningful chunks with overlap
3. **Normalization**: Normalize embeddings for consistent similarity calculations
4. **Caching**: Cache embeddings for frequently accessed content
5. **Indexing**: Use efficient data structures for large-scale similarity search
6. **Evaluation**: Regularly evaluate retrieval quality and adjust parameters
7. **Privacy**: Keep sensitive data local when using embeddings

Next: Explore advanced configuration options and performance tuning. 