---
layout: default
title: "Chapter 4: Retrieval System"
parent: "RAGFlow Tutorial"
nav_order: 4
---

# Chapter 4: Retrieval System

Welcome to **Chapter 4: Retrieval System**. In this part of **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explores advanced retrieval techniques in RAGFlow. You'll learn about hybrid search, reranking, query expansion, and other sophisticated methods to improve retrieval quality and relevance.

## 🎯 What You'll Learn

- Hybrid search implementation
- Query expansion and rewriting
- Re-ranking algorithms
- Multi-stage retrieval pipelines
- Retrieval evaluation and optimization

## 🔍 Retrieval Fundamentals

### Basic Retrieval Types

```python
from typing import List, Dict, Any
from abc import ABC, abstractmethod
import numpy as np

class RetrievalStrategy(ABC):
    """Abstract base class for retrieval strategies"""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        pass

class KeywordRetrieval(RetrievalStrategy):
    """Keyword-based retrieval using TF-IDF or BM25"""

    def __init__(self, documents: List[str]):
        self.documents = documents
        self.vocab = self._build_vocabulary()
        self.tfidf_matrix = self._build_tfidf_matrix()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents using keyword matching"""
        query_vector = self._vectorize_query(query)
        similarities = self._calculate_similarities(query_vector)

        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'document': self.documents[idx],
                'score': similarities[idx],
                'index': idx
            })

        return results

    def _build_vocabulary(self) -> Dict[str, int]:
        """Build vocabulary from documents"""
        vocab = {}
        idx = 0
        for doc in self.documents:
            for word in doc.lower().split():
                if word not in vocab:
                    vocab[word] = idx
                    idx += 1
        return vocab

    def _build_tfidf_matrix(self) -> np.ndarray:
        """Build TF-IDF matrix"""
        # Simplified TF-IDF implementation
        matrix = np.zeros((len(self.documents), len(self.vocab)))

        for i, doc in enumerate(self.documents):
            words = doc.lower().split()
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1

            for word, count in word_counts.items():
                if word in self.vocab:
                    tf = count / len(words)
                    idf = np.log(len(self.documents) / sum(1 for d in self.documents if word in d.lower()))
                    matrix[i, self.vocab[word]] = tf * idf

        return matrix

    def _vectorize_query(self, query: str) -> np.ndarray:
        """Convert query to vector"""
        vector = np.zeros(len(self.vocab))
        words = query.lower().split()

        for word in words:
            if word in self.vocab:
                vector[self.vocab[word]] = 1  # Simple binary encoding

        return vector

    def _calculate_similarities(self, query_vector: np.ndarray) -> np.ndarray:
        """Calculate cosine similarities"""
        dot_products = np.dot(self.tfidf_matrix, query_vector)
        doc_norms = np.linalg.norm(self.tfidf_matrix, axis=1)
        query_norm = np.linalg.norm(query_vector)

        # Avoid division by zero
        similarities = np.zeros(len(self.documents))
        mask = doc_norms > 0
        similarities[mask] = dot_products[mask] / (doc_norms[mask] * query_norm)

        return similarities

class SemanticRetrieval(RetrievalStrategy):
    """Semantic retrieval using embeddings"""

    def __init__(self, documents: List[str], embeddings: np.ndarray):
        self.documents = documents
        self.embeddings = embeddings

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents using semantic similarity"""
        # In practice, you would embed the query here
        # For demonstration, using a mock query embedding
        query_embedding = np.random.rand(self.embeddings.shape[1])

        similarities = self._calculate_cosine_similarity(query_embedding)

        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'document': self.documents[idx],
                'score': similarities[idx],
                'index': idx
            })

        return results

    def _calculate_cosine_similarity(self, query_embedding: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between query and documents"""
        dot_products = np.dot(self.embeddings, query_embedding)
        doc_norms = np.linalg.norm(self.embeddings, axis=1)
        query_norm = np.linalg.norm(query_embedding)

        similarities = dot_products / (doc_norms * query_norm)
        return similarities
```

## 🔄 Hybrid Search Implementation

### Combining Keyword and Semantic Search

```python
class HybridRetrieval(RetrievalStrategy):
    """Hybrid retrieval combining keyword and semantic search"""

    def __init__(self, keyword_retrieval: KeywordRetrieval, semantic_retrieval: SemanticRetrieval):
        self.keyword_retrieval = keyword_retrieval
        self.semantic_retrieval = semantic_retrieval
        self.keyword_weight = 0.3
        self.semantic_weight = 0.7

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents using hybrid approach"""
        # Get results from both methods
        keyword_results = self.keyword_retrieval.retrieve(query, top_k * 2)
        semantic_results = self.semantic_retrieval.retrieve(query, top_k * 2)

        # Combine results using reciprocal rank fusion
        combined_results = self._reciprocal_rank_fusion(
            keyword_results, semantic_results, top_k
        )

        return combined_results

    def _reciprocal_rank_fusion(self, list1: List[Dict], list2: List[Dict], k: int) -> List[Dict]:
        """Combine rankings using Reciprocal Rank Fusion"""
        # Create score dictionaries
        scores = {}

        # Add scores from first list
        for rank, result in enumerate(list1, 1):
            doc_id = result['index']
            scores[doc_id] = scores.get(doc_id, 0) + (1.0 / (k + rank))

        # Add scores from second list
        for rank, result in enumerate(list2, 1):
            doc_id = result['index']
            scores[doc_id] = scores.get(doc_id, 0) + (1.0 / (k + rank))

        # Sort by combined scores
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Convert back to result format
        results = []
        for doc_id, score in sorted_docs[:k]:
            results.append({
                'document': self.keyword_retrieval.documents[doc_id],
                'score': score,
                'index': doc_id
            })

        return results
```

### Advanced Hybrid Search with Reranking

```python
class AdvancedHybridRetrieval:
    """Advanced hybrid retrieval with reranking"""

    def __init__(self, keyword_retrieval, semantic_retrieval, reranker=None):
        self.keyword_retrieval = keyword_retrieval
        self.semantic_retrieval = semantic_retrieval
        self.reranker = reranker

    def retrieve_with_reranking(self, query: str, top_k: int = 5, expand_results: int = 20) -> List[Dict[str, Any]]:
        """Retrieve with hybrid search and reranking"""
        # Get expanded results from both methods
        keyword_results = self.keyword_retrieval.retrieve(query, expand_results)
        semantic_results = self.semantic_retrieval.retrieve(query, expand_results)

        # Combine using RRF
        combined_results = self._reciprocal_rank_fusion(
            keyword_results, semantic_results, expand_results
        )

        # Apply reranking if available
        if self.reranker:
            combined_results = self.reranker.rerank(query, combined_results)

        return combined_results[:top_k]

    def _reciprocal_rank_fusion(self, list1, list2, k):
        """Reciprocal Rank Fusion implementation"""
        scores = {}

        # Score from first list
        for rank, result in enumerate(list1, 1):
            doc_id = result['index']
            scores[doc_id] = scores.get(doc_id, 0) + (1.0 / (k + rank))

        # Score from second list
        for rank, result in enumerate(list2, 1):
            doc_id = result['index']
            scores[doc_id] = scores.get(doc_id, 0) + (1.0 / (k + rank))

        # Sort and format results
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in sorted_docs:
            results.append({
                'document': self.keyword_retrieval.documents[doc_id],
                'score': score,
                'index': doc_id
            })

        return results
```

## 🔄 Query Expansion

### Synonym Expansion

```python
class QueryExpander:
    """Expand queries with synonyms and related terms"""

    def __init__(self):
        # Simple synonym dictionary (in practice, use WordNet or similar)
        self.synonyms = {
            'car': ['automobile', 'vehicle', 'auto'],
            'fast': ['quick', 'rapid', 'speedy', 'swift'],
            'computer': ['PC', 'machine', 'device', 'system'],
            'learn': ['study', 'understand', 'master', 'grasp'],
            'build': ['create', 'develop', 'construct', 'make']
        }

    def expand_query(self, query: str, max_expansions: int = 3) -> List[str]:
        """Expand query with synonyms"""
        words = query.lower().split()
        expanded_queries = [query]

        for i, word in enumerate(words):
            if word in self.synonyms:
                for synonym in self.synonyms[word][:max_expansions]:
                    # Replace word with synonym
                    new_words = words.copy()
                    new_words[i] = synonym
                    expanded_query = ' '.join(new_words)
                    expanded_queries.append(expanded_query)

        return list(set(expanded_queries))  # Remove duplicates

    def expand_with_embeddings(self, query: str, embeddings, top_n: int = 5) -> List[str]:
        """Expand query using embeddings"""
        # This would use embedding similarity to find related terms
        # For demonstration, returning mock expansions
        return [
            query,
            f"{query} tutorial",
            f"{query} guide",
            f"{query} examples",
            f"how to {query}"
        ]
```

### Contextual Query Expansion

```python
class ContextualQueryExpander:
    """Expand queries based on context and conversation history"""

    def __init__(self):
        self.conversation_history = []
        self.context_window = 3

    def expand_with_context(self, current_query: str, context_docs: List[str] = None) -> List[str]:
        """Expand query using conversation context"""
        expanded_queries = [current_query]

        # Add recent conversation context
        recent_queries = self.conversation_history[-self.context_window:]
        for prev_query in recent_queries:
            # Combine current and previous queries
            combined = f"{prev_query} {current_query}"
            expanded_queries.append(combined)

        # Add context from relevant documents
        if context_docs:
            for doc in context_docs[:2]:  # Use top 2 docs
                # Extract key terms from document
                key_terms = self._extract_key_terms(doc)
                for term in key_terms:
                    expanded = f"{current_query} {term}"
                    expanded_queries.append(expanded)

        return list(set(expanded_queries))

    def add_to_history(self, query: str):
        """Add query to conversation history"""
        self.conversation_history.append(query)

        # Keep only recent history
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def _extract_key_terms(self, document: str) -> List[str]:
        """Extract key terms from document"""
        # Simple implementation - in practice, use NLP techniques
        words = document.lower().split()
        # Return most frequent words (excluding stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'}
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]

        # Count frequency
        word_counts = {}
        for word in filtered_words:
            word_counts[word] = word_counts.get(word, 0) + 1

        # Return top 3 most frequent words
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:3]]
```

## 🔀 Re-ranking Algorithms

### Cross-Encoder Re-ranking

```python
class CrossEncoderReranker:
    """Re-rank documents using cross-encoder model"""

    def __init__(self):
        # In practice, load a cross-encoder model like sentence-transformers
        self.model = None

    def rerank(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Re-rank documents based on query-document relevance"""
        if not documents:
            return documents

        reranked_docs = []

        for doc in documents:
            # In practice, this would use the cross-encoder to score relevance
            # For demonstration, using mock scores
            relevance_score = self._calculate_relevance_score(query, doc['document'])

            doc_with_score = doc.copy()
            doc_with_score['rerank_score'] = relevance_score
            doc_with_score['final_score'] = (
                doc.get('score', 0) * 0.7 + relevance_score * 0.3
            )
            reranked_docs.append(doc_with_score)

        # Sort by final score
        reranked_docs.sort(key=lambda x: x['final_score'], reverse=True)

        return reranked_docs

    def _calculate_relevance_score(self, query: str, document: str) -> float:
        """Calculate relevance score (mock implementation)"""
        # In practice, this would use a trained cross-encoder model
        query_words = set(query.lower().split())
        doc_words = set(document.lower().split())

        overlap = len(query_words.intersection(doc_words))
        query_coverage = overlap / len(query_words) if query_words else 0

        return min(query_coverage, 1.0)  # Normalize to 0-1
```

### Learning-to-Rank Re-ranking

```python
class LearningToRankReranker:
    """Re-rank using learning-to-rank approach"""

    def __init__(self):
        self.features = [
            'bm25_score',
            'semantic_similarity',
            'document_length',
            'query_term_frequency',
            'document_freshness'
        ]

    def rerank(self, query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Re-rank documents using multiple features"""
        reranked_docs = []

        for doc in documents:
            # Extract features
            features = self._extract_features(query, doc)

            # Calculate learning-to-rank score
            ltr_score = self._calculate_ltr_score(features)

            doc_with_score = doc.copy()
            doc_with_score['ltr_score'] = ltr_score
            doc_with_score['final_score'] = (
                doc.get('score', 0) * 0.6 + ltr_score * 0.4
            )
            reranked_docs.append(doc_with_score)

        # Sort by final score
        reranked_docs.sort(key=lambda x: x['final_score'], reverse=True)

        return reranked_docs

    def _extract_features(self, query: str, doc: Dict[str, Any]) -> Dict[str, float]:
        """Extract ranking features"""
        document_text = doc['document']

        features = {
            'bm25_score': doc.get('bm25_score', 0.5),
            'semantic_similarity': doc.get('semantic_score', 0.5),
            'document_length': len(document_text.split()),
            'query_term_frequency': self._calculate_query_term_frequency(query, document_text),
            'document_freshness': 0.8  # Mock freshness score
        }

        return features

    def _calculate_query_term_frequency(self, query: str, document: str) -> float:
        """Calculate query term frequency in document"""
        query_words = query.lower().split()
        doc_words = document.lower().split()

        total_frequency = 0
        for query_word in query_words:
            frequency = doc_words.count(query_word.lower())
            total_frequency += frequency

        return total_frequency / len(query_words) if query_words else 0

    def _calculate_ltr_score(self, features: Dict[str, float]) -> float:
        """Calculate learning-to-rank score using simple linear model"""
        # Simple weighted combination (in practice, use trained model)
        weights = {
            'bm25_score': 0.3,
            'semantic_similarity': 0.4,
            'document_length': -0.1,  # Shorter documents often better
            'query_term_frequency': 0.2,
            'document_freshness': 0.2
        }

        score = 0.0
        for feature, weight in weights.items():
            score += features[feature] * weight

        return max(0, min(1, score))  # Normalize to 0-1
```

## 📊 Retrieval Evaluation

### Evaluation Metrics

```python
class RetrievalEvaluator:
    """Evaluate retrieval system performance"""

    def __init__(self):
        self.metrics = {}

    def evaluate(self, queries: List[str], relevant_docs: Dict[str, List[int]],
                 retrieved_docs: Dict[str, List[int]], k: int = 10) -> Dict[str, float]:
        """Evaluate retrieval performance"""

        precision_scores = []
        recall_scores = []
        ndcg_scores = []

        for query in queries:
            if query not in relevant_docs or query not in retrieved_docs:
                continue

            relevant = set(relevant_docs[query])
            retrieved = retrieved_docs[query][:k]

            # Calculate Precision@K
            precision = self._precision_at_k(retrieved, relevant, k)
            precision_scores.append(precision)

            # Calculate Recall@K
            recall = self._recall_at_k(retrieved, relevant, k)
            recall_scores.append(recall)

            # Calculate NDCG@K
            ndcg = self._ndcg_at_k(retrieved, relevant, k)
            ndcg_scores.append(ndcg)

        return {
            'precision@k': np.mean(precision_scores),
            'recall@k': np.mean(recall_scores),
            'ndcg@k': np.mean(ndcg_scores)
        }

    def _precision_at_k(self, retrieved: List[int], relevant: set, k: int) -> float:
        """Calculate Precision@K"""
        retrieved_at_k = retrieved[:k]
        relevant_retrieved = len(set(retrieved_at_k).intersection(relevant))

        return relevant_retrieved / k if k > 0 else 0

    def _recall_at_k(self, retrieved: List[int], relevant: set, k: int) -> float:
        """Calculate Recall@K"""
        retrieved_at_k = retrieved[:k]
        relevant_retrieved = len(set(retrieved_at_k).intersection(relevant))

        return relevant_retrieved / len(relevant) if relevant else 0

    def _ndcg_at_k(self, retrieved: List[int], relevant: set, k: int) -> float:
        """Calculate NDCG@K"""
        retrieved_at_k = retrieved[:k]

        dcg = 0
        for i, doc_id in enumerate(retrieved_at_k):
            if doc_id in relevant:
                dcg += 1 / np.log2(i + 2)

        # Calculate IDCG (ideal DCG)
        idcg = 0
        for i in range(min(k, len(relevant))):
            idcg += 1 / np.log2(i + 2)

        return dcg / idcg if idcg > 0 else 0

    def evaluate_retrieval_time(self, queries: List[str], retrieval_times: List[float]) -> Dict[str, float]:
        """Evaluate retrieval speed"""
        return {
            'avg_retrieval_time': np.mean(retrieval_times),
            'median_retrieval_time': np.median(retrieval_times),
            'p95_retrieval_time': np.percentile(retrieval_times, 95),
            'p99_retrieval_time': np.percentile(retrieval_times, 99)
        }
```

### A/B Testing Framework

```python
class RetrievalABTester:
    """A/B test different retrieval strategies"""

    def __init__(self):
        self.experiments = {}

    def create_experiment(self, name: str, strategy_a, strategy_b, traffic_split: float = 0.5):
        """Create A/B test experiment"""
        self.experiments[name] = {
            'strategy_a': strategy_a,
            'strategy_b': strategy_b,
            'traffic_split': traffic_split,
            'results': {'a': [], 'b': []}
        }

    def run_query(self, experiment_name: str, query: str) -> Dict[str, Any]:
        """Run query through A/B test"""
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment {experiment_name} not found")

        experiment = self.experiments[experiment_name]

        # Randomly assign to A or B
        import random
        if random.random() < experiment['traffic_split']:
            strategy = experiment['strategy_a']
            group = 'a'
        else:
            strategy = experiment['strategy_b']
            group = 'b'

        # Run retrieval
        results = strategy.retrieve(query)

        # Record results
        experiment['results'][group].append({
            'query': query,
            'results': results,
            'timestamp': time.time()
        })

        return {
            'results': results,
            'group': group,
            'experiment': experiment_name
        }

    def get_experiment_results(self, experiment_name: str) -> Dict[str, Any]:
        """Get A/B test results"""
        experiment = self.experiments[experiment_name]

        results_a = experiment['results']['a']
        results_b = experiment['results']['b']

        return {
            'experiment': experiment_name,
            'group_a_count': len(results_a),
            'group_b_count': len(results_b),
            'conversion_a': self._calculate_conversion(results_a),
            'conversion_b': self._calculate_conversion(results_b)
        }

    def _calculate_conversion(self, results: List[Dict]) -> float:
        """Calculate conversion rate (mock implementation)"""
        if not results:
            return 0

        # Mock conversion based on result quality
        total_score = sum(
            np.mean([r.get('score', 0) for r in result['results']])
            for result in results
        )

        return min(total_score / len(results), 1.0)
```

## 🚀 Advanced Techniques

### Multi-Stage Retrieval Pipeline

```python
class MultiStageRetrieval:
    """Multi-stage retrieval pipeline"""

    def __init__(self):
        self.stages = []

    def add_stage(self, retriever, top_k: int, threshold: float = 0.0):
        """Add retrieval stage"""
        self.stages.append({
            'retriever': retriever,
            'top_k': top_k,
            'threshold': threshold
        })

    def retrieve(self, query: str, final_k: int = 5) -> List[Dict[str, Any]]:
        """Execute multi-stage retrieval"""
        candidates = None

        for stage in self.stages:
            retriever = stage['retriever']
            top_k = stage['top_k']
            threshold = stage['threshold']

            # Retrieve candidates
            if candidates is None:
                # First stage - retrieve from all documents
                stage_results = retriever.retrieve(query, top_k)
            else:
                # Subsequent stages - retrieve from previous candidates
                candidate_docs = [c['document'] for c in candidates]
                # Mock retrieval from candidates
                stage_results = candidates[:top_k]

            # Apply threshold filtering
            filtered_results = [
                r for r in stage_results
                if r.get('score', 0) >= threshold
            ]

            candidates = filtered_results

            if len(candidates) < final_k:
                break

        return candidates[:final_k]
```

## 🎯 Best Practices

### Retrieval Optimization Guidelines

1. **Hybrid Search Implementation**
   - Combine keyword and semantic search
   - Use reciprocal rank fusion for combination
   - Tune weights based on content type

2. **Query Expansion Strategies**
   - Use synonyms for general queries
   - Leverage conversation context
   - Avoid over-expansion

3. **Re-ranking Techniques**
   - Apply cross-encoders for precision
   - Use learning-to-rank for complex scenarios
   - Balance computational cost with quality gains

4. **Evaluation and Monitoring**
   - Regularly evaluate retrieval metrics
   - A/B test improvements
   - Monitor query performance

## 🏆 Achievement Unlocked!

Congratulations! 🎉 You've mastered:

- ✅ Hybrid search combining multiple retrieval methods
- ✅ Query expansion and contextual understanding
- ✅ Advanced re-ranking algorithms
- ✅ Multi-stage retrieval pipelines
- ✅ Comprehensive evaluation metrics
- ✅ A/B testing frameworks

## 🚀 What's Next?

Ready to build chatbots? Let's explore [Chapter 5: LLM Integration](05-llm-integration.md) to learn how to integrate large language models with your retrieval system.

---

**Practice what you've learned:**
1. Implement hybrid search for your documents
2. Create query expansion strategies
3. Build a re-ranking pipeline
4. Evaluate your retrieval system performance
5. Set up A/B testing for retrieval improvements

*What's the most challenging retrieval scenario you've encountered?* 🔍

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `query`, `documents` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Retrieval System` as an operating subsystem inside **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `results`, `List`, `Dict` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Retrieval System` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `query` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `documents`.
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
- search upstream code for `self` and `query` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Knowledge Base Setup](03-knowledge-base-setup.md)
- [Next Chapter: Chapter 5: LLM Integration & Configuration](05-llm-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
