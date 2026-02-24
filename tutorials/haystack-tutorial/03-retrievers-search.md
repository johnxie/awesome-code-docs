---
layout: default
title: "Chapter 3: Retrievers & Search"
parent: "Haystack Tutorial"
nav_order: 3
---

# Chapter 3: Retrievers & Search

Welcome to **Chapter 3: Retrievers & Search**. In this part of **Haystack: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master document retrieval and search techniques in Haystack.

## 🎯 Overview

This chapter covers the core retrieval mechanisms in Haystack, including different types of retrievers, search strategies, and optimization techniques for finding relevant documents efficiently.

## 🔍 Understanding Retrievers

### Retriever Types

#### 1. **BM25Retriever** - Traditional Text Search
```python
from haystack.components.retrievers import BM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document

# Initialize document store
document_store = InMemoryDocumentStore()

# Add documents
documents = [
    Document(content="Python is a high-level programming language."),
    Document(content="Machine learning algorithms process data."),
    Document(content="Neural networks are inspired by biological brains."),
    Document(content="Deep learning uses multiple neural network layers.")
]
document_store.write_documents(documents)

# Create BM25 retriever
retriever = BM25Retriever(document_store=document_store)

# Search for documents
results = retriever.run(query="programming language", top_k=2)

for doc in results["documents"]:
    print(f"Content: {doc.content}")
    print(f"Score: {doc.score:.4f}")
    print("---")
```

#### 2. **EmbeddingRetriever** - Semantic Search
```python
from haystack.components.retrievers import EmbeddingRetriever
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline

# Create embedding retriever pipeline
document_embedder = SentenceTransformersDocumentEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# Create retriever
retriever = EmbeddingRetriever(document_store=document_store)

# Build indexing pipeline
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("embedder", document_embedder)
indexing_pipeline.add_component("retriever", retriever)

# Connect components
indexing_pipeline.connect("embedder", "retriever")

# Index documents
indexing_pipeline.run({"embedder": {"documents": documents}})

# Search with semantic similarity
results = retriever.run(query="computer programming", top_k=3)

for doc in results["documents"]:
    print(f"Content: {doc.content}")
    print(f"Score: {doc.score:.4f}")
    print("---")
```

#### 3. **DPRRetriever** - Dense Passage Retrieval
```python
from haystack.components.retrievers import DPRRetriever
from haystack.components.embedders import DPRDocumentEmbedder, DPRQueryEmbedder

# DPR-based retriever for better semantic understanding
document_embedder = DPRDocumentEmbedder(model="facebook/dpr-ctx_encoder-single-nq-base")
query_embedder = DPRQueryEmbedder(model="facebook/dpr-question_encoder-single-nq-base")

retriever = DPRRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    document_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
)

# Index documents with DPR embeddings
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("doc_embedder", document_embedder)
indexing_pipeline.add_component("retriever", retriever)
indexing_pipeline.connect("doc_embedder", "retriever")

indexing_pipeline.run({"doc_embedder": {"documents": documents}})

# DPR search
results = retriever.run(query="What is Python?", top_k=2)
```

## 🔄 Hybrid Search Strategies

### Combining BM25 and Semantic Search

```python
from haystack.components.retrievers import BM25Retriever, EmbeddingRetriever
from haystack.components.joiners import DocumentJoiner

class HybridRetriever:
    def __init__(self, document_store):
        self.document_store = document_store

        # Initialize both retrievers
        self.bm25_retriever = BM25Retriever(document_store=document_store)
        self.embedding_retriever = EmbeddingRetriever(document_store=document_store)

        # Document joiner for combining results
        self.joiner = DocumentJoiner(join_mode="reciprocal_rank_fusion", top_k=10)

        # Build hybrid pipeline
        self.pipeline = Pipeline()
        self.pipeline.add_component("bm25_retriever", self.bm25_retriever)
        self.pipeline.add_component("embedding_retriever", self.embedding_retriever)
        self.pipeline.add_component("joiner", self.joiner)

        self.pipeline.connect("bm25_retriever", "joiner")
        self.pipeline.connect("embedding_retriever", "joiner")

    def search(self, query, bm25_weight=0.3, embedding_weight=0.7, top_k=5):
        """Perform hybrid search combining BM25 and semantic similarity"""
        # Run both retrievers
        bm25_results = self.bm25_retriever.run(query=query, top_k=top_k)["documents"]
        embedding_results = self.embedding_retriever.run(query=query, top_k=top_k)["documents"]

        # Apply weights and combine
        combined_results = []

        # Create score mapping for BM25 results
        bm25_scores = {doc.id: doc.score * bm25_weight for doc in bm25_results}

        # Create score mapping for embedding results
        embedding_scores = {doc.id: doc.score * embedding_weight for doc in embedding_results}

        # Combine all unique documents
        all_doc_ids = set(bm25_scores.keys()) | set(embedding_scores.keys())

        for doc_id in all_doc_ids:
            # Find the document object
            doc = None
            for d in bm25_results + embedding_results:
                if d.id == doc_id:
                    doc = d
                    break

            if doc:
                # Combine scores
                combined_score = bm25_scores.get(doc_id, 0) + embedding_scores.get(doc_id, 0)
                doc.score = combined_score
                combined_results.append(doc)

        # Sort by combined score and return top_k
        combined_results.sort(key=lambda x: x.score, reverse=True)
        return combined_results[:top_k]

# Usage
hybrid_retriever = HybridRetriever(document_store)

# Hybrid search
results = hybrid_retriever.search("Python programming", top_k=3)

for doc in results:
    print(f"Content: {doc.content}")
    print(f"Combined Score: {doc.score:.4f}")
    print("---")
```

### Reciprocal Rank Fusion

```python
from haystack.components.joiners import DocumentJoiner

# Using Haystack's built-in reciprocal rank fusion
def create_hybrid_pipeline(document_store):
    """Create a hybrid search pipeline with RRF"""
    pipeline = Pipeline()

    # BM25 retriever
    bm25_retriever = BM25Retriever(document_store=document_store)
    pipeline.add_component("bm25_retriever", bm25_retriever)

    # Embedding retriever
    embedding_retriever = EmbeddingRetriever(document_store=document_store)
    pipeline.add_component("embedding_retriever", embedding_retriever)

    # Joiner with reciprocal rank fusion
    joiner = DocumentJoiner(
        join_mode="reciprocal_rank_fusion",
        weights=[0.4, 0.6],  # BM25 weight, Embedding weight
        top_k=10
    )
    pipeline.add_component("joiner", joiner)

    # Connect components
    pipeline.connect("bm25_retriever", "joiner")
    pipeline.connect("embedding_retriever", "joiner")

    return pipeline

# Create and use hybrid pipeline
hybrid_pipeline = create_hybrid_pipeline(document_store)
results = hybrid_pipeline.run({
    "bm25_retriever": {"query": "machine learning algorithms"},
    "embedding_retriever": {"query": "machine learning algorithms"}
})

print("Hybrid search results with RRF:")
for doc in results["joiner"]["documents"]:
    print(f"Content: {doc.content}")
    print(f"RRF Score: {doc.score:.4f}")
    print("---")
```

## 🎯 Advanced Retrieval Techniques

### Query Expansion

```python
from haystack.components.builders import QueryBuilder
from haystack.components.generators import OpenAIGenerator

class QueryExpansionRetriever:
    def __init__(self, base_retriever):
        self.base_retriever = base_retriever

        # Query expansion using LLM
        self.expansion_generator = OpenAIGenerator(
            model="gpt-3.5-turbo",
            generation_kwargs={"temperature": 0.1, "max_tokens": 50}
        )

    def expand_query(self, original_query):
        """Expand query using LLM to generate related terms"""
        expansion_prompt = f"""
        Given the search query: "{original_query}"

        Generate 3-5 related search terms or synonyms that would help find more relevant results.
        Return them as a comma-separated list.

        Examples:
        Query: "machine learning"
        Expanded: "artificial intelligence, ML algorithms, data science, predictive modeling"

        Query: "{original_query}"
        Expanded:"""

        try:
            response = self.expansion_generator.run(prompt=expansion_prompt)
            expanded_terms = response["replies"][0].strip()

            # Combine original query with expanded terms
            expanded_query = f"{original_query} {expanded_terms}"
            return expanded_query

        except Exception as e:
            print(f"Query expansion failed: {e}")
            return original_query

    def search_with_expansion(self, query, top_k=5):
        """Search with query expansion"""
        # Expand the query
        expanded_query = self.expand_query(query)
        print(f"Original: {query}")
        print(f"Expanded: {expanded_query}")

        # Search with expanded query
        results = self.base_retriever.run(query=expanded_query, top_k=top_k)

        return results

# Usage
expansion_retriever = QueryExpansionRetriever(embedding_retriever)
results = expansion_retriever.search_with_expansion("neural networks", top_k=3)
```

### Context-Aware Retrieval

```python
class ContextAwareRetriever:
    def __init__(self, retriever, conversation_history=None):
        self.retriever = retriever
        self.conversation_history = conversation_history or []

    def search_with_context(self, query, user_context=None, conversation_context=True):
        """Search considering user context and conversation history"""
        # Build enhanced query
        enhanced_query = self._enhance_query_with_context(
            query, user_context, conversation_context
        )

        # Apply context-based filtering
        filters = self._build_context_filters(user_context)

        # Search with enhanced query and filters
        results = self.retriever.run(
            query=enhanced_query,
            filters=filters,
            top_k=10
        )

        # Re-rank results based on context relevance
        reranked_results = self._rerank_by_context(results["documents"], user_context)

        return {"documents": reranked_results[:5]}

    def _enhance_query_with_context(self, query, user_context, conversation_context):
        """Enhance query with contextual information"""
        enhanced_parts = [query]

        # Add user context
        if user_context:
            if user_context.get("expertise_level") == "beginner":
                enhanced_parts.append("beginner friendly explanation")
            elif user_context.get("expertise_level") == "expert":
                enhanced_parts.append("advanced technical details")

            if user_context.get("preferred_language"):
                enhanced_parts.append(user_context["preferred_language"])

        # Add conversation context
        if conversation_context and self.conversation_history:
            recent_topics = self._extract_recent_topics()
            if recent_topics:
                enhanced_parts.append(f"related to {recent_topics}")

        return " ".join(enhanced_parts)

    def _build_context_filters(self, user_context):
        """Build filters based on user context"""
        filters = {}

        if user_context:
            # Filter by difficulty level
            if user_context.get("expertise_level") == "beginner":
                filters["difficulty"] = ["beginner", "intermediate"]
            elif user_context.get("expertise_level") == "expert":
                filters["difficulty"] = ["intermediate", "advanced"]

            # Filter by language
            if user_context.get("preferred_language"):
                filters["language"] = user_context["preferred_language"]

        return filters

    def _extract_recent_topics(self):
        """Extract topics from recent conversation"""
        recent_messages = self.conversation_history[-5:]  # Last 5 messages
        topics = []

        # Simple topic extraction (could use NLP for better results)
        topic_keywords = ["python", "machine learning", "neural networks", "algorithms"]

        for message in recent_messages:
            for topic in topic_keywords:
                if topic.lower() in message.lower():
                    topics.append(topic)

        return list(set(topics))  # Remove duplicates

    def _rerank_by_context(self, documents, user_context):
        """Re-rank documents based on context relevance"""
        if not user_context:
            return documents

        scored_docs = []

        for doc in documents:
            score = doc.score or 0

            # Boost score based on context matching
            if user_context.get("expertise_level") == "beginner":
                if any(word in doc.content.lower() for word in ["simple", "basic", "easy"]):
                    score *= 1.2

            if user_context.get("preferred_language"):
                lang = user_context["preferred_language"]
                if lang.lower() in doc.content.lower():
                    score *= 1.1

            doc.score = score
            scored_docs.append(doc)

        # Sort by new scores
        scored_docs.sort(key=lambda x: x.score, reverse=True)
        return scored_docs

# Usage
context_retriever = ContextAwareRetriever(embedding_retriever)

# User context
user_context = {
    "expertise_level": "beginner",
    "preferred_language": "python",
    "interests": ["machine learning", "programming"]
}

# Search with context
results = context_retriever.search_with_context(
    "how do neural networks work?",
    user_context=user_context
)

print("Context-aware search results:")
for doc in results["documents"]:
    print(f"Content: {doc.content[:100]}...")
    print(f"Score: {doc.score:.4f}")
    print("---")
```

## 📊 Retrieval Evaluation

### Evaluating Retriever Performance

```python
from haystack.evaluation import EvaluationRunResult
import numpy as np

class RetrieverEvaluator:
    def __init__(self, retriever):
        self.retriever = retriever

    def evaluate_retrieval(self, queries, relevant_docs, k_values=[1, 3, 5, 10]):
        """Evaluate retrieval performance using standard metrics"""
        all_metrics = {}

        for k in k_values:
            precision_scores = []
            recall_scores = []
            ndcg_scores = []

            for query, relevant in zip(queries, relevant_docs):
                # Get retrieved documents
                results = self.retriever.run(query=query, top_k=k)
                retrieved_docs = results["documents"]

                # Calculate metrics
                precision = self._calculate_precision(retrieved_docs, relevant, k)
                recall = self._calculate_recall(retrieved_docs, relevant, k)
                ndcg = self._calculate_ndcg(retrieved_docs, relevant, k)

                precision_scores.append(precision)
                recall_scores.append(recall)
                ndcg_scores.append(ndcg)

            all_metrics[f"k={k}"] = {
                "precision": np.mean(precision_scores),
                "recall": np.mean(recall_scores),
                "ndcg": np.mean(ndcg_scores)
            }

        return all_metrics

    def _calculate_precision(self, retrieved, relevant, k):
        """Calculate precision@k"""
        retrieved_ids = {doc.id for doc in retrieved[:k]}
        relevant_ids = set(relevant)

        if not retrieved_ids:
            return 0.0

        return len(retrieved_ids & relevant_ids) / len(retrieved_ids)

    def _calculate_recall(self, retrieved, relevant, k):
        """Calculate recall@k"""
        retrieved_ids = {doc.id for doc in retrieved[:k]}
        relevant_ids = set(relevant)

        if not relevant_ids:
            return 1.0 if not retrieved_ids else 0.0

        return len(retrieved_ids & relevant_ids) / len(relevant_ids)

    def _calculate_ndcg(self, retrieved, relevant, k):
        """Calculate NDCG@k"""
        retrieved_ids = {doc.id: i for i, doc in enumerate(retrieved[:k])}
        relevant_ids = set(relevant)

        if not relevant_ids:
            return 0.0

        # Calculate DCG
        dcg = 0.0
        for i, doc in enumerate(retrieved[:k]):
            if doc.id in relevant_ids:
                dcg += 1.0 / np.log2(i + 2)

        # Calculate IDCG (ideal DCG)
        idcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(relevant_ids), k)))

        return dcg / idcg if idcg > 0 else 0.0

    def compare_retrievers(self, retrievers, queries, relevant_docs):
        """Compare multiple retrievers"""
        comparison_results = {}

        for retriever_name, retriever in retrievers.items():
            evaluator = RetrieverEvaluator(retriever)
            metrics = evaluator.evaluate_retrieval(queries, relevant_docs)
            comparison_results[retriever_name] = metrics

        return comparison_results

# Usage
evaluator = RetrieverEvaluator(embedding_retriever)

# Sample evaluation data
queries = [
    "What is machine learning?",
    "How do neural networks work?"
]

relevant_docs = [
    ["doc1", "doc3"],  # Relevant docs for first query
    ["doc2", "doc4"]   # Relevant docs for second query
]

# Evaluate
metrics = evaluator.evaluate_retrieval(queries, relevant_docs)
print("Retrieval Evaluation Results:")
for k, scores in metrics.items():
    print(f"{k}:")
    print(f"  Precision: {scores['precision']:.3f}")
    print(f"  Recall: {scores['recall']:.3f}")
    print(f"  NDCG: {scores['ndcg']:.3f}")
```

## 🚀 Optimization Techniques

### Index Optimization

```python
class RetrievalOptimizer:
    def __init__(self, retriever):
        self.retriever = retriever

    def optimize_index(self):
        """Optimize document index for better retrieval"""
        optimizations = {
            "preprocessing": self._optimize_preprocessing(),
            "chunking": self._optimize_chunking(),
            "embedding": self._optimize_embedding(),
            "indexing": self._optimize_indexing()
        }

        return optimizations

    def _optimize_preprocessing(self):
        """Optimize document preprocessing"""
        return {
            "remove_stopwords": True,
            "stemming": True,
            "lowercase": True,
            "remove_punctuation": True
        }

    def _optimize_chunking(self):
        """Optimize text chunking strategy"""
        return {
            "chunk_size": 512,
            "overlap": 50,
            "strategy": "sentence_aware",
            "respect_boundaries": True
        }

    def _optimize_embedding(self):
        """Optimize embedding configuration"""
        return {
            "model": "all-MiniLM-L6-v2",  # Smaller, faster model
            "normalize": True,
            "batch_size": 32,
            "max_seq_length": 256
        }

    def _optimize_indexing(self):
        """Optimize index structure"""
        return {
            "index_type": "IVF_PQ",  # Approximate nearest neighbors
            "nlist": 100,            # Number of clusters
            "nprobe": 10,            # Number of clusters to search
            "quantizer": "PQ64"      # Product quantization
        }

    def benchmark_retrieval_speed(self, queries, batch_sizes=[1, 5, 10, 20]):
        """Benchmark retrieval speed for different batch sizes"""
        import time

        results = {}

        for batch_size in batch_sizes:
            batch_queries = queries * (batch_size // len(queries) + 1)
            batch_queries = batch_queries[:batch_size]

            start_time = time.time()

            for query in batch_queries:
                self.retriever.run(query=query, top_k=10)

            end_time = time.time()

            avg_time = (end_time - start_time) / batch_size
            results[batch_size] = {
                "avg_query_time": avg_time,
                "queries_per_second": 1.0 / avg_time
            }

        return results

# Usage
optimizer = RetrievalOptimizer(embedding_retriever)

# Benchmark performance
queries = ["machine learning", "neural networks", "deep learning"]
benchmark_results = optimizer.benchmark_retrieval_speed(queries)

print("Retrieval Speed Benchmark:")
for batch_size, metrics in benchmark_results.items():
    print(f"Batch size {batch_size}:")
    print(".4f")
    print(".2f")
```

## 🎯 Best Practices

### Choosing the Right Retriever

| Scenario | Recommended Retriever | Rationale |
|----------|----------------------|-----------|
| **Exact keyword search** | BM25Retriever | Precise keyword matching |
| **Semantic similarity** | EmbeddingRetriever | Understands meaning and context |
| **Question answering** | DPRRetriever | Optimized for QA tasks |
| **Hybrid requirements** | Custom hybrid approach | Combines strengths of multiple methods |
| **Large document sets** | EmbeddingRetriever with HNSW | Efficient similarity search |

### Performance Optimization

1. **Use appropriate embedding models** - Balance quality vs speed
2. **Implement caching** for frequent queries
3. **Batch requests** when possible
4. **Use approximate nearest neighbors** for large indexes
5. **Pre-compute embeddings** for static documents

### Quality Improvement

1. **Fine-tune embeddings** on domain-specific data
2. **Implement re-ranking** for better relevance
3. **Use query expansion** for broader retrieval
4. **Apply metadata filtering** to narrow results
5. **Regularly evaluate and update** retrieval strategies

## 📈 Next Steps

With retrieval mastered, you're ready to:

- **[Chapter 4: Generators & LLMs](04-generators-llms.md)** - Integrate language models for answer generation
- **[Chapter 5: Pipelines & Workflows](05-pipelines-workflows.md)** - Build complex search workflows
- **[Chapter 6: Evaluation & Optimization](06-evaluation-optimization.md)** - Measure and improve search quality

---

**Ready to integrate LLMs with your search system? Continue to [Chapter 4: Generators & LLMs](04-generators-llms.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `query`, `retriever` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Retrievers & Search` as an operating subsystem inside **Haystack: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `results`, `print`, `documents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Retrievers & Search` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `query` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `retriever`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Haystack](https://github.com/deepset-ai/haystack)
  Why it matters: authoritative reference on `Haystack` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `query` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Document Stores](02-document-stores.md)
- [Next Chapter: Chapter 4: Generators & LLMs](04-generators-llms.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
