---
layout: default
title: "Chapter 3: Knowledge Base Setup"
parent: "RAGFlow Tutorial"
nav_order: 3
---

# Chapter 3: Knowledge Base Setup

Welcome to **Chapter 3: Knowledge Base Setup**. In this part of **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter dives deep into creating and configuring knowledge bases in RAGFlow. You'll learn how to optimize knowledge bases for different use cases, configure embedding models, and fine-tune retrieval settings.

## 🎯 What You'll Learn

- Knowledge base creation and configuration
- Embedding model selection and optimization
- Retrieval strategy configuration
- Performance monitoring and optimization
- Multi-tenant knowledge base management

## 🗄️ Knowledge Base Fundamentals

### What is a Knowledge Base?

A knowledge base in RAGFlow is a structured collection of documents and their processed content, optimized for efficient retrieval and question answering.

```python
class KnowledgeBase:
    def __init__(self, name: str, description: str = ""):
        self.id = None
        self.name = name
        self.description = description
        self.documents = []
        self.embedding_model = None
        self.chunk_strategy = {}
        self.retrieval_config = {}
        self.created_at = None
        self.updated_at = None

    def add_document(self, document):
        """Add document to knowledge base"""
        self.documents.append(document)

    def get_stats(self):
        """Get knowledge base statistics"""
        return {
            'total_documents': len(self.documents),
            'total_chunks': sum(len(doc.chunks) for doc in self.documents),
            'embedding_model': self.embedding_model,
            'last_updated': self.updated_at
        }
```

## 🛠️ Creating Knowledge Bases

### Basic Knowledge Base Creation

```python
import requests
import json
from typing import Dict, Any

class KnowledgeBaseManager:
    def __init__(self, base_url: str = "http://localhost:80", api_key: str = None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def create_knowledge_base(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new knowledge base"""
        url = f"{self.base_url}/api/v1/knowledge-bases"

        response = requests.post(url, json=config, headers=self.headers)

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create knowledge base: {response.text}")

    def get_knowledge_base(self, kb_id: str) -> Dict[str, Any]:
        """Get knowledge base details"""
        url = f"{self.base_url}/api/v1/knowledge-bases/{kb_id}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get knowledge base: {response.text}")

    def update_knowledge_base(self, kb_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update knowledge base configuration"""
        url = f"{self.base_url}/api/v1/knowledge-bases/{kb_id}"

        response = requests.patch(url, json=updates, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update knowledge base: {response.text}")

    def delete_knowledge_base(self, kb_id: str) -> bool:
        """Delete knowledge base"""
        url = f"{self.base_url}/api/v1/knowledge-bases/{kb_id}"

        response = requests.delete(url, headers=self.headers)

        return response.status_code == 204
```

### Advanced Configuration

```python
def create_advanced_kb():
    """Create knowledge base with advanced configuration"""

    kb_config = {
        "name": "Advanced Technical Documentation",
        "description": "Comprehensive knowledge base for technical documentation with optimized retrieval",

        # Embedding configuration
        "embedding": {
            "model": "text-embedding-3-large",
            "dimensions": 3072,
            "api_key": "your_openai_key"
        },

        # Chunking configuration
        "chunking": {
            "strategy": "semantic",
            "size": 512,
            "overlap": 50,
            "method": "sentence"
        },

        # Retrieval configuration
        "retrieval": {
            "top_k": 5,
            "similarity_threshold": 0.7,
            "reranking": True,
            "rerank_model": "cross-encoder/ms-marco-MiniLM-L-6-v2"
        },

        # Parsing configuration
        "parsing": {
            "extract_images": True,
            "extract_tables": True,
            "ocr_fallback": True,
            "language": "en"
        },

        # Access control
        "permissions": {
            "public": False,
            "users": ["user1", "user2"],
            "groups": ["developers", "analysts"]
        },

        # Monitoring
        "monitoring": {
            "enable_metrics": True,
            "log_queries": True,
            "performance_tracking": True
        }
    }

    manager = KnowledgeBaseManager()
    return manager.create_knowledge_base(kb_config)
```

## 🎯 Embedding Model Selection

### Supported Embedding Models

```python
class EmbeddingManager:
    def __init__(self):
        self.models = {
            # OpenAI models
            "text-embedding-ada-002": {
                "dimensions": 1536,
                "max_tokens": 8191,
                "cost_per_1k_tokens": 0.0001
            },
            "text-embedding-3-small": {
                "dimensions": 1536,
                "max_tokens": 8191,
                "cost_per_1k_tokens": 0.00002
            },
            "text-embedding-3-large": {
                "dimensions": 3072,
                "max_tokens": 8191,
                "cost_per_1k_tokens": 0.00013
            },

            # Local models
            "sentence-transformers/all-MiniLM-L6-v2": {
                "dimensions": 384,
                "max_tokens": 256,
                "local": True
            },
            "sentence-transformers/all-mpnet-base-v2": {
                "dimensions": 768,
                "max_tokens": 384,
                "local": True
            },

            # Specialized models
            "text-embedding-3-large": {
                "dimensions": 3072,
                "max_tokens": 8191,
                "specialized": "code"
            }
        }

    def recommend_model(self, use_case: str, content_type: str = "general") -> str:
        """Recommend embedding model based on use case"""

        recommendations = {
            "general_qa": "text-embedding-3-small",
            "technical_docs": "text-embedding-3-large",
            "code_search": "text-embedding-3-large",
            "semantic_search": "sentence-transformers/all-mpnet-base-v2",
            "cost_optimized": "text-embedding-ada-002",
            "local_only": "sentence-transformers/all-MiniLM-L6-v2"
        }

        return recommendations.get(use_case, "text-embedding-ada-002")

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed information about a model"""
        return self.models.get(model_name, {})

    def calculate_cost(self, model_name: str, token_count: int) -> float:
        """Calculate embedding cost"""
        model_info = self.get_model_info(model_name)
        cost_per_1k = model_info.get("cost_per_1k_tokens", 0)

        return (token_count / 1000) * cost_per_1k
```

### Model Performance Comparison

```python
import time
from typing import List, Dict

class ModelBenchmarker:
    def __init__(self, embedding_manager: EmbeddingManager):
        self.embedding_manager = embedding_manager

    def benchmark_models(self, test_texts: List[str]) -> Dict[str, Dict[str, Any]]:
        """Benchmark different embedding models"""

        models_to_test = [
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "sentence-transformers/all-MiniLM-L6-v2"
        ]

        results = {}

        for model_name in models_to_test:
            print(f"Benchmarking {model_name}...")

            start_time = time.time()
            total_tokens = 0

            # Simulate embedding generation
            for text in test_texts:
                # In real implementation, call actual embedding API
                token_count = len(text.split())  # Simplified token count
                total_tokens += token_count

                # Simulate API call delay
                time.sleep(0.01)

            processing_time = time.time() - start_time

            results[model_name] = {
                "processing_time": processing_time,
                "tokens_processed": total_tokens,
                "tokens_per_second": total_tokens / processing_time if processing_time > 0 else 0,
                "estimated_cost": self.embedding_manager.calculate_cost(model_name, total_tokens)
            }

        return results

    def compare_similarity_search(self, models: List[str], query: str, documents: List[str]):
        """Compare similarity search performance across models"""
        # This would implement actual similarity search comparison
        # For demonstration purposes, returning mock results
        return {
            model: {
                "precision": 0.85,
                "recall": 0.78,
                "f1_score": 0.81
            } for model in models
        }
```

## 🔍 Retrieval Configuration

### Basic Retrieval Settings

```python
class RetrievalConfig:
    def __init__(self):
        self.top_k = 5
        self.similarity_threshold = 0.7
        self.search_type = "similarity"  # similarity, keyword, hybrid
        self.reranking = False
        self.diversity_bias = 0.0
        self.temporal_decay = False

    def to_dict(self):
        """Convert to dictionary for API calls"""
        return {
            "top_k": self.top_k,
            "similarity_threshold": self.similarity_threshold,
            "search_type": self.search_type,
            "reranking": self.reranking,
            "diversity_bias": self.diversity_bias,
            "temporal_decay": self.temporal_decay
        }

def optimize_retrieval_config(content_type: str) -> RetrievalConfig:
    """Optimize retrieval configuration based on content type"""

    config = RetrievalConfig()

    if content_type == "technical":
        config.top_k = 7
        config.similarity_threshold = 0.75
        config.search_type = "hybrid"
        config.reranking = True

    elif content_type == "general":
        config.top_k = 5
        config.similarity_threshold = 0.7
        config.search_type = "similarity"

    elif content_type == "code":
        config.top_k = 10
        config.similarity_threshold = 0.8
        config.search_type = "hybrid"
        config.reranking = True

    return config
```

### Advanced Retrieval Strategies

```python
class AdvancedRetrieval:
    def __init__(self):
        self.query_expansion = False
        self.context_window = 2
        self.metadata_filtering = False
        self.temporal_weighting = False

    def hybrid_search(self, query: str, kb_id: str) -> List[Dict[str, Any]]:
        """Implement hybrid search combining multiple strategies"""

        # Step 1: Keyword search
        keyword_results = self.keyword_search(query, kb_id)

        # Step 2: Semantic search
        semantic_results = self.semantic_search(query, kb_id)

        # Step 3: Combine and rerank
        combined_results = self.combine_results(keyword_results, semantic_results)

        return combined_results

    def keyword_search(self, query: str, kb_id: str) -> List[Dict[str, Any]]:
        """Perform keyword-based search"""
        # Implementation would use text search algorithms
        # BM25, TF-IDF, etc.
        return []

    def semantic_search(self, query: str, kb_id: str) -> List[Dict[str, Any]]:
        """Perform semantic similarity search"""
        # Implementation would use vector similarity search
        return []

    def combine_results(self, keyword_results, semantic_results) -> List[Dict[str, Any]]:
        """Combine and rerank results from multiple strategies"""
        # Implementation would use reciprocal rank fusion or other reranking methods
        return []

    def query_expansion(self, query: str) -> List[str]:
        """Expand query with synonyms and related terms"""
        # Use word embeddings or knowledge graphs for expansion
        expanded_queries = [query]

        # Add synonyms
        synonyms = self.get_synonyms(query)
        expanded_queries.extend(synonyms)

        return expanded_queries

    def get_synonyms(self, word: str) -> List[str]:
        """Get synonyms for a word"""
        # Implementation would use WordNet, or API calls
        return []
```

## 📊 Performance Monitoring

### Knowledge Base Metrics

```python
class KnowledgeBaseMonitor:
    def __init__(self, kb_id: str):
        self.kb_id = kb_id
        self.metrics = {
            "query_count": 0,
            "avg_response_time": 0.0,
            "hit_rate": 0.0,
            "avg_relevance_score": 0.0
        }

    def record_query(self, response_time: float, relevance_score: float):
        """Record query metrics"""
        self.metrics["query_count"] += 1

        # Update average response time
        current_avg = self.metrics["avg_response_time"]
        self.metrics["avg_response_time"] = (
            current_avg + (response_time - current_avg) / self.metrics["query_count"]
        )

        # Update average relevance score
        current_relevance = self.metrics["avg_relevance_score"]
        self.metrics["avg_relevance_score"] = (
            current_relevance + (relevance_score - current_relevance) / self.metrics["query_count"]
        )

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        return {
            "knowledge_base_id": self.kb_id,
            "metrics": self.metrics,
            "health_score": self.calculate_health_score(),
            "recommendations": self.generate_recommendations()
        }

    def calculate_health_score(self) -> float:
        """Calculate overall health score (0-100)"""
        weights = {
            "response_time": 0.4,
            "relevance_score": 0.4,
            "query_count": 0.2
        }

        # Normalize metrics to 0-100 scale
        response_time_score = max(0, 100 - (self.metrics["avg_response_time"] * 10))
        relevance_score = self.metrics["avg_relevance_score"] * 100
        query_volume_score = min(100, self.metrics["query_count"] / 10 * 100)

        return (
            weights["response_time"] * response_time_score +
            weights["relevance_score"] * relevance_score +
            weights["query_count"] * query_volume_score
        )

    def generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        if self.metrics["avg_response_time"] > 2.0:
            recommendations.append("Consider using smaller embedding models or optimizing chunk size")

        if self.metrics["avg_relevance_score"] < 0.7:
            recommendations.append("Try different embedding models or adjust similarity threshold")

        if self.metrics["query_count"] > 1000:
            recommendations.append("Consider implementing query caching")

        return recommendations
```

## 🔧 Optimization Techniques

### Chunk Size Optimization

```python
class ChunkOptimizer:
    def __init__(self):
        self.chunk_sizes = [256, 512, 768, 1024, 1536, 2048]

    def find_optimal_chunk_size(self, documents: List[str], queries: List[str]) -> int:
        """Find optimal chunk size through experimentation"""

        best_score = 0
        best_size = 512

        for chunk_size in self.chunk_sizes:
            # Create chunks
            all_chunks = []
            for doc in documents:
                chunks = self.create_chunks(doc, chunk_size)
                all_chunks.extend(chunks)

            # Evaluate retrieval performance
            score = self.evaluate_chunk_performance(all_chunks, queries)

            if score > best_score:
                best_score = score
                best_size = chunk_size

        return best_size

    def create_chunks(self, text: str, chunk_size: int) -> List[str]:
        """Create chunks of specified size"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def evaluate_chunk_performance(self, chunks: List[str], queries: List[str]) -> float:
        """Evaluate chunk performance (simplified)"""
        # In real implementation, this would:
        # 1. Embed chunks and queries
        # 2. Perform similarity search
        # 3. Calculate precision/recall metrics
        return 0.8  # Mock score
```

### Embedding Model Fine-tuning

```python
class EmbeddingFineTuner:
    def __init__(self):
        self.base_model = None
        self.fine_tuned_model = None

    def prepare_training_data(self, documents: List[str], queries: List[str]):
        """Prepare training data for fine-tuning"""
        training_pairs = []

        for query in queries:
            # Find relevant documents for each query
            relevant_docs = self.find_relevant_documents(query, documents)

            for doc in relevant_docs:
                training_pairs.append({
                    "query": query,
                    "document": doc,
                    "label": 1  # Positive pair
                })

                # Add negative examples
                negative_docs = self.sample_negative_documents(doc, documents)
                for neg_doc in negative_docs:
                    training_pairs.append({
                        "query": query,
                        "document": neg_doc,
                        "label": 0  # Negative pair
                    })

        return training_pairs

    def fine_tune_model(self, training_data: List[Dict], epochs: int = 3):
        """Fine-tune embedding model"""
        # Implementation would use sentence-transformers or similar library
        print(f"Fine-tuning model for {epochs} epochs...")

        # Mock fine-tuning process
        for epoch in range(epochs):
            print(f"Epoch {epoch + 1}/{epochs}")
            # Training loop would go here

        print("Fine-tuning completed!")
        return "fine-tuned-model"

    def find_relevant_documents(self, query: str, documents: List[str]) -> List[str]:
        """Find documents relevant to query"""
        # Simplified relevance detection
        relevant = []
        query_words = set(query.lower().split())

        for doc in documents:
            doc_words = set(doc.lower().split())
            overlap = len(query_words.intersection(doc_words))

            if overlap > 0:
                relevant.append(doc)

        return relevant[:3]  # Return top 3

    def sample_negative_documents(self, positive_doc: str, all_docs: List[str], n: int = 2) -> List[str]:
        """Sample negative documents for training"""
        # Exclude the positive document and return random others
        negative_docs = [doc for doc in all_docs if doc != positive_doc]
        return negative_docs[:n]
```

## 🎯 Best Practices

### Knowledge Base Design Principles

1. **Content Organization**
   - Group related documents together
   - Use consistent naming conventions
   - Maintain document metadata

2. **Performance Optimization**
   - Choose appropriate embedding models
   - Optimize chunk sizes for your use case
   - Implement caching for frequent queries

3. **Maintenance Strategies**
   - Regular content updates
   - Performance monitoring
   - User feedback integration

4. **Security Considerations**
   - Access control implementation
   - Data privacy compliance
   - Audit logging

## 🏆 Achievement Unlocked!

Congratulations! 🎉 You've mastered:

- ✅ Knowledge base creation and configuration
- ✅ Embedding model selection and optimization
- ✅ Advanced retrieval strategy configuration
- ✅ Performance monitoring and metrics
- ✅ Chunk size and model optimization techniques

## 🚀 What's Next?

Ready to dive into retrieval systems? Let's explore [Chapter 4: Retrieval System](04-retrieval-system.md) to learn about advanced retrieval techniques and algorithms.

---

**Practice what you've learned:**
1. Create knowledge bases with different configurations
2. Benchmark embedding models for your use case
3. Optimize retrieval settings for different content types
4. Implement performance monitoring
5. Experiment with chunk size optimization

*What's the most important factor for your knowledge base performance?* 🧠

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `List`, `query` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Knowledge Base Setup` as an operating subsystem inside **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `embedding`, `text`, `metrics` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Knowledge Base Setup` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `List` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `query`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/infiniflow/ragflow)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `List` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Document Processing](02-document-processing.md)
- [Next Chapter: Chapter 4: Retrieval System](04-retrieval-system.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
