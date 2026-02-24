---
layout: default
title: "Chapter 6: Evaluation & Optimization"
parent: "Haystack Tutorial"
nav_order: 6
---

# Chapter 6: Evaluation & Optimization

Welcome to **Chapter 6: Evaluation & Optimization**. In this part of **Haystack: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Measure search quality and optimize Haystack pipelines for maximum performance.

## 🎯 Overview

This chapter covers evaluation methodologies for assessing search system quality and optimization techniques to improve performance. You'll learn to measure retrieval accuracy, generation quality, and end-to-end system performance.

## 📊 Evaluation Frameworks

### Retrieval Evaluation Metrics

```python
from haystack.evaluation import EvaluationRunResult
from sklearn.metrics import precision_score, recall_score, f1_score, ndcg_score
import numpy as np

class RetrievalEvaluator:
    def __init__(self):
        self.metrics = {}

    def evaluate_retrieval(self, queries, retrieved_docs, relevant_docs, k_values=[1, 3, 5, 10]):
        """Comprehensive retrieval evaluation"""
        results = {}

        for k in k_values:
            precision_scores = []
            recall_scores = []
            f1_scores = []
            ndcg_scores = []
            mrr_scores = []

            for query_docs, query_relevant in zip(retrieved_docs, relevant_docs):
                # Limit to top-k
                top_k_docs = query_docs[:k]

                # Calculate metrics
                precision = self._calculate_precision_at_k(top_k_docs, query_relevant, k)
                recall = self._calculate_recall_at_k(top_k_docs, query_relevant, k)
                f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

                # NDCG calculation
                ndcg = self._calculate_ndcg_at_k(top_k_docs, query_relevant, k)

                # MRR calculation
                mrr = self._calculate_mrr(top_k_docs, query_relevant)

                precision_scores.append(precision)
                recall_scores.append(recall)
                f1_scores.append(f1)
                ndcg_scores.append(ndcg)
                mrr_scores.append(mrr)

            results[f"k={k}"] = {
                "precision": np.mean(precision_scores),
                "recall": np.mean(recall_scores),
                "f1": np.mean(f1_scores),
                "ndcg": np.mean(ndcg_scores),
                "mrr": np.mean(mrr_scores)
            }

        return results

    def _calculate_precision_at_k(self, retrieved, relevant, k):
        """Calculate Precision@K"""
        retrieved_set = set(doc.id for doc in retrieved)
        relevant_set = set(relevant)

        if not retrieved:
            return 0.0

        return len(retrieved_set & relevant_set) / len(retrieved)

    def _calculate_recall_at_k(self, retrieved, relevant, k):
        """Calculate Recall@K"""
        retrieved_set = set(doc.id for doc in retrieved)
        relevant_set = set(relevant)

        if not relevant_set:
            return 1.0 if not retrieved else 0.0

        return len(retrieved_set & relevant_set) / len(relevant_set)

    def _calculate_ndcg_at_k(self, retrieved, relevant, k):
        """Calculate NDCG@K"""
        relevant_set = set(relevant)

        dcg = 0.0
        for i, doc in enumerate(retrieved[:k]):
            if doc.id in relevant_set:
                dcg += 1.0 / np.log2(i + 2)

        # Calculate IDCG (ideal DCG)
        idcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(relevant_set), k)))

        return dcg / idcg if idcg > 0 else 0.0

    def _calculate_mrr(self, retrieved, relevant):
        """Calculate Mean Reciprocal Rank"""
        relevant_set = set(relevant)

        for rank, doc in enumerate(retrieved, 1):
            if doc.id in relevant_set:
                return 1.0 / rank

        return 0.0

# Usage
evaluator = RetrievalEvaluator()

# Sample evaluation data
queries = ["What is machine learning?", "How do neural networks work?"]
retrieved_docs = [
    # Retrieved docs for first query (simplified)
    [Document(id="doc1", content="ML definition"), Document(id="doc2", content="AI overview")],
    # Retrieved docs for second query
    [Document(id="doc3", content="Neural networks"), Document(id="doc4", content="Deep learning")]
]

relevant_docs = [
    ["doc1", "doc5"],  # Ground truth relevant docs
    ["doc3", "doc6"]
]

results = evaluator.evaluate_retrieval(queries, retrieved_docs, relevant_docs)
print("Retrieval Evaluation Results:")
for k, metrics in results.items():
    print(f"{k}:")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")
```

### Generation Quality Evaluation

```python
from haystack.evaluation import Evaluator
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
import evaluate

class GenerationEvaluator:
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.bertscore = evaluate.load("bertscore")

    def evaluate_generation(self, predictions, references):
        """Evaluate generation quality against references"""
        results = {
            "rouge": self._calculate_rouge(predictions, references),
            "bleu": self._calculate_bleu(predictions, references),
            "bertscore": self._calculate_bertscore(predictions, references),
            "diversity": self._calculate_diversity(predictions),
            "factual_consistency": self._evaluate_factual_consistency(predictions, references)
        }

        return results

    def _calculate_rouge(self, predictions, references):
        """Calculate ROUGE scores"""
        rouge1_scores = []
        rouge2_scores = []
        rougeL_scores = []

        for pred, ref in zip(predictions, references):
            scores = self.rouge_scorer.score(ref, pred)
            rouge1_scores.append(scores["rouge1"].fmeasure)
            rouge2_scores.append(scores["rouge2"].fmeasure)
            rougeL_scores.append(scores["rougeL"].fmeasure)

        return {
            "rouge1": np.mean(rouge1_scores),
            "rouge2": np.mean(rouge2_scores),
            "rougeL": np.mean(rougeL_scores)
        }

    def _calculate_bleu(self, predictions, references):
        """Calculate BLEU scores"""
        bleu_scores = []

        for pred, ref in zip(predictions, references):
            # Tokenize
            pred_tokens = pred.split()
            ref_tokens = [ref.split()]  # BLEU expects list of references

            try:
                bleu = sentence_bleu(ref_tokens, pred_tokens)
                bleu_scores.append(bleu)
            except:
                bleu_scores.append(0.0)

        return np.mean(bleu_scores)

    def _calculate_bertscore(self, predictions, references):
        """Calculate BERTScore"""
        results = self.bertscore.compute(
            predictions=predictions,
            references=references,
            lang="en"
        )

        return {
            "precision": np.mean(results["precision"]),
            "recall": np.mean(results["recall"]),
            "f1": np.mean(results["f1"])
        }

    def _calculate_diversity(self, predictions):
        """Calculate lexical diversity"""
        diversities = []

        for pred in predictions:
            tokens = pred.lower().split()
            if len(tokens) > 1:
                unique_tokens = set(tokens)
                diversity = len(unique_tokens) / len(tokens)
                diversities.append(diversity)
            else:
                diversities.append(0.0)

        return np.mean(diversities)

    def _evaluate_factual_consistency(self, predictions, references):
        """Evaluate factual consistency (simplified)"""
        consistency_scores = []

        for pred, ref in zip(predictions, references):
            # Simple consistency check
            pred_lower = pred.lower()
            ref_lower = ref.lower()

            # Check for contradictory statements
            contradictions = 0
            if ("not" in pred_lower) != ("not" in ref_lower):
                contradictions += 1

            # Calculate overlap
            pred_words = set(pred_lower.split())
            ref_words = set(ref_lower.split())
            overlap = len(pred_words & ref_words)
            total = len(pred_words | ref_words)

            consistency = (overlap / total) if total > 0 else 0
            consistency_scores.append(consistency)

        return np.mean(consistency_scores)

# Usage
gen_evaluator = GenerationEvaluator()

predictions = [
    "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
    "Neural networks are computing systems inspired by biological neural networks."
]

references = [
    "Machine learning is a method of data analysis that automates analytical model building.",
    "Neural networks are computing systems inspired by the biological neural networks in animal brains."
]

results = gen_evaluator.evaluate_generation(predictions, references)
print("Generation Evaluation Results:")
for metric, score in results.items():
    if isinstance(score, dict):
        print(f"{metric}:")
        for sub_metric, sub_score in score.items():
            print(f"  {sub_metric}: {sub_score:.3f}")
    else:
        print(f"{metric}: {score:.3f}")
```

## 🔧 Performance Optimization

### Index Optimization

```python
class IndexOptimizer:
    def __init__(self, document_store):
        self.document_store = document_store

    def optimize_index(self, optimization_type="comprehensive"):
        """Apply various index optimizations"""
        optimizations = {}

        if optimization_type in ["comprehensive", "chunking"]:
            optimizations["chunking"] = self._optimize_chunking()

        if optimization_type in ["comprehensive", "embedding"]:
            optimizations["embedding"] = self._optimize_embedding()

        if optimization_type in ["comprehensive", "index_structure"]:
            optimizations["index_structure"] = self._optimize_index_structure()

        if optimization_type in ["comprehensive", "caching"]:
            optimizations["caching"] = self._optimize_caching()

        return optimizations

    def _optimize_chunking(self):
        """Optimize document chunking strategy"""
        # Analyze current chunking performance
        current_stats = self._analyze_chunking_stats()

        # Determine optimal chunk size
        optimal_size = self._calculate_optimal_chunk_size(current_stats)

        # Apply new chunking strategy
        self.document_store.update_chunking_strategy(
            chunk_size=optimal_size,
            overlap=optimal_size // 10
        )

        return {
            "old_chunk_size": current_stats["avg_chunk_size"],
            "new_chunk_size": optimal_size,
            "improvement": self._calculate_chunking_improvement(current_stats, optimal_size)
        }

    def _optimize_embedding(self):
        """Optimize embedding configuration"""
        # Test different embedding models
        models_to_test = [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-MiniLM-L12-v2",
            "sentence-transformers/paraphrase-MiniLM-L6-v2"
        ]

        best_model = None
        best_score = 0

        for model_name in models_to_test:
            score = self._evaluate_embedding_model(model_name)
            if score > best_score:
                best_score = score
                best_model = model_name

        # Apply best model
        self.document_store.update_embedding_model(best_model)

        return {
            "selected_model": best_model,
            "performance_score": best_score,
            "tested_models": len(models_to_test)
        }

    def _optimize_index_structure(self):
        """Optimize index structure for better performance"""
        # Analyze current index
        index_stats = self._analyze_index_stats()

        # Determine optimal index type
        if index_stats["dataset_size"] > 100000:
            index_type = "IVF_PQ"  # Approximate nearest neighbors
        elif index_stats["dimensionality"] > 768:
            index_type = "HNSW"  # Hierarchical Navigable Small World
        else:
            index_type = "FLAT"  # Exact search

        # Apply optimization
        self.document_store.rebuild_index(index_type=index_type)

        return {
            "old_index_type": index_stats["current_index_type"],
            "new_index_type": index_type,
            "expected_improvement": self._estimate_index_improvement(index_type, index_stats)
        }

    def _optimize_caching(self):
        """Optimize caching strategy"""
        # Analyze query patterns
        query_patterns = self._analyze_query_patterns()

        # Implement intelligent caching
        cache_config = {
            "frequent_queries_ttl": 3600,  # 1 hour
            "semantic_cache_enabled": True,
            "result_deduplication": True,
            "prefetching_enabled": query_patterns["has_patterns"]
        }

        self.document_store.configure_caching(cache_config)

        return cache_config

    def _analyze_chunking_stats(self):
        """Analyze current chunking performance"""
        # This would analyze actual document chunks
        return {
            "avg_chunk_size": 512,
            "chunk_count": 1000,
            "overlap_ratio": 0.1
        }

    def _calculate_optimal_chunk_size(self, stats):
        """Calculate optimal chunk size based on analysis"""
        # Simple heuristic - could be more sophisticated
        base_size = 512
        if stats["avg_chunk_size"] > 600:
            return base_size * 0.8
        elif stats["avg_chunk_size"] < 400:
            return base_size * 1.2
        else:
            return base_size

    def _evaluate_embedding_model(self, model_name):
        """Evaluate embedding model performance"""
        # Simplified evaluation - would use actual retrieval metrics
        model_scores = {
            "sentence-transformers/all-MiniLM-L6-v2": 0.85,
            "sentence-transformers/all-MiniLM-L12-v2": 0.87,
            "sentence-transformers/paraphrase-MiniLM-L6-v2": 0.82
        }
        return model_scores.get(model_name, 0.8)

# Usage
optimizer = IndexOptimizer(document_store)
optimizations = optimizer.optimize_index()

print("Index Optimization Results:")
for opt_type, results in optimizations.items():
    print(f"{opt_type}:")
    for key, value in results.items():
        print(f"  {key}: {value}")
```

### Query Optimization

```python
class QueryOptimizer:
    def __init__(self):
        self.query_patterns = {}
        self.performance_stats = {}

    def optimize_query(self, query, context=None):
        """Apply various query optimizations"""
        optimized_query = query

        # Apply optimizations in sequence
        optimized_query = self._expand_query(optimized_query, context)
        optimized_query = self._rewrite_query(optimized_query)
        optimized_query = self._add_boosting_terms(optimized_query, context)

        return optimized_query

    def _expand_query(self, query, context):
        """Expand query with synonyms and related terms"""
        # Simple synonym expansion
        synonyms = {
            "machine learning": ["ML", "artificial intelligence", "data science"],
            "neural network": ["neural net", "deep learning", "artificial neural network"],
            "database": ["data store", "data warehouse", "repository"]
        }

        expanded_terms = []
        query_lower = query.lower()

        for term, syns in synonyms.items():
            if term in query_lower:
                expanded_terms.extend(syns[:2])  # Limit to 2 synonyms

        if expanded_terms:
            return f"{query} {' '.join(expanded_terms)}"
        return query

    def _rewrite_query(self, query):
        """Rewrite query for better retrieval"""
        # Simple query rewriting rules
        rewrites = {
            "how do i": "how to",
            "what's": "what is",
            "can't": "cannot",
            "don't": "do not"
        }

        rewritten = query
        for old, new in rewrites.items():
            rewritten = rewritten.replace(old, new)

        return rewritten

    def _add_boosting_terms(self, query, context):
        """Add context-based boosting terms"""
        if not context or not context.get("user_profile"):
            return query

        user_profile = context["user_profile"]
        boost_terms = []

        # Add expertise-based terms
        if user_profile.get("expertise") == "beginner":
            boost_terms.extend(["introduction", "basics", "fundamentals"])
        elif user_profile.get("expertise") == "expert":
            boost_terms.extend(["advanced", "implementation", "optimization"])

        # Add domain-specific terms
        if user_profile.get("domain"):
            domain_terms = {
                "software": ["programming", "development", "code"],
                "data_science": ["statistics", "modeling", "analysis"],
                "business": ["strategy", "management", "operations"]
            }
            boost_terms.extend(domain_terms.get(user_profile["domain"], []))

        if boost_terms:
            return f"{query} {' '.join(boost_terms[:3])}"  # Limit boost terms

        return query

    def track_performance(self, query, response_time, result_quality):
        """Track query performance for optimization"""
        query_hash = hash(query) % 10000  # Simple hashing

        if query_hash not in self.performance_stats:
            self.performance_stats[query_hash] = []

        self.performance_stats[query_hash].append({
            "response_time": response_time,
            "quality_score": result_quality,
            "timestamp": time.time()
        })

        # Keep only recent stats (last 100)
        if len(self.performance_stats[query_hash]) > 100:
            self.performance_stats[query_hash] = self.performance_stats[query_hash][-100:]

    def analyze_performance(self):
        """Analyze query performance patterns"""
        analysis = {
            "slow_queries": [],
            "low_quality_queries": [],
            "optimization_opportunities": []
        }

        for query_hash, stats in self.performance_stats.items():
            avg_time = np.mean([s["response_time"] for s in stats])
            avg_quality = np.mean([s["quality_score"] for s in stats])

            if avg_time > 2.0:  # Slow queries
                analysis["slow_queries"].append({
                    "query_hash": query_hash,
                    "avg_time": avg_time,
                    "count": len(stats)
                })

            if avg_quality < 0.7:  # Low quality queries
                analysis["low_quality_queries"].append({
                    "query_hash": query_hash,
                    "avg_quality": avg_quality,
                    "count": len(stats)
                })

        return analysis

# Usage
query_optimizer = QueryOptimizer()

# Optimize a query
original_query = "how do i learn machine learning"
optimized_query = query_optimizer.optimize_query(
    original_query,
    context={"user_profile": {"expertise": "beginner", "domain": "software"}}
)

print(f"Original: {original_query}")
print(f"Optimized: {optimized_query}")

# Track performance
query_optimizer.track_performance(optimized_query, 1.2, 0.85)
```

## 🎯 A/B Testing Framework

### Automated A/B Testing

```python
import random
from collections import defaultdict
import json

class ABTestingFramework:
    def __init__(self):
        self.experiments = {}
        self.results = defaultdict(dict)

    def create_experiment(self, experiment_name, variants, traffic_split=None):
        """Create a new A/B test experiment"""
        if traffic_split is None:
            # Equal split
            traffic_split = [1.0 / len(variants)] * len(variants)

        self.experiments[experiment_name] = {
            "variants": variants,
            "traffic_split": traffic_split,
            "start_time": time.time(),
            "metrics": {}
        }

    def assign_variant(self, experiment_name, user_id):
        """Assign user to a variant based on consistent hashing"""
        if experiment_name not in self.experiments:
            return None

        experiment = self.experiments[experiment_name]
        variants = experiment["variants"]
        traffic_split = experiment["traffic_split"]

        # Consistent assignment based on user_id
        user_hash = hash(user_id) % 100
        cumulative_split = 0

        for i, split in enumerate(traffic_split):
            cumulative_split += split
            if user_hash < cumulative_split * 100:
                return variants[i]

        return variants[0]  # Fallback

    def track_metric(self, experiment_name, variant, metric_name, value):
        """Track a metric for a specific variant"""
        if experiment_name not in self.experiments:
            return

        if variant not in self.results[experiment_name]:
            self.results[experiment_name][variant] = defaultdict(list)

        self.results[experiment_name][variant][metric_name].append(value)

    def get_experiment_results(self, experiment_name, min_samples=100):
        """Get statistical results for an experiment"""
        if experiment_name not in self.results:
            return None

        experiment = self.experiments[experiment_name]
        results = self.results[experiment_name]

        analysis = {}

        for variant, metrics in results.items():
            variant_analysis = {}

            for metric_name, values in metrics.items():
                if len(values) >= min_samples:
                    variant_analysis[metric_name] = {
                        "mean": np.mean(values),
                        "std": np.std(values),
                        "count": len(values),
                        "confidence_interval": self._calculate_confidence_interval(values)
                    }

            analysis[variant] = variant_analysis

        # Statistical significance testing
        analysis["statistical_tests"] = self._perform_statistical_tests(results)

        return analysis

    def _calculate_confidence_interval(self, values, confidence=0.95):
        """Calculate confidence interval"""
        mean = np.mean(values)
        std = np.std(values)
        n = len(values)

        # z-score for 95% confidence
        z = 1.96
        margin = z * (std / np.sqrt(n))

        return {
            "lower": mean - margin,
            "upper": mean + margin,
            "margin": margin
        }

    def _perform_statistical_tests(self, results):
        """Perform statistical significance tests between variants"""
        tests = {}

        if len(results) < 2:
            return tests

        # Compare first two variants for each metric
        variants = list(results.keys())
        variant1, variant2 = variants[0], variants[1]

        for metric_name in results[variant1].keys():
            if metric_name in results[variant2]:
                values1 = results[variant1][metric_name]
                values2 = results[variant2][metric_name]

                if len(values1) > 10 and len(values2) > 10:
                    # T-test
                    t_stat, p_value = stats.ttest_ind(values1, values2)

                    tests[f"{metric_name}_{variant1}_vs_{variant2}"] = {
                        "t_statistic": t_stat,
                        "p_value": p_value,
                        "significant": p_value < 0.05
                    }

        return tests

# Usage
ab_tester = ABTestingFramework()

# Create experiment comparing different retrieval strategies
ab_tester.create_experiment(
    "retrieval_strategy_test",
    variants=["bm25", "semantic", "hybrid"],
    traffic_split=[0.3, 0.3, 0.4]  # 30%, 30%, 40% traffic split
)

# Simulate user interactions
users = [f"user_{i}" for i in range(1000)]

for user in users:
    variant = ab_tester.assign_variant("retrieval_strategy_test", user)

    # Simulate performance metrics based on variant
    if variant == "bm25":
        latency = random.normalvariate(1.2, 0.2)
        accuracy = random.normalvariate(0.75, 0.05)
    elif variant == "semantic":
        latency = random.normalvariate(1.8, 0.3)
        accuracy = random.normalvariate(0.82, 0.04)
    else:  # hybrid
        latency = random.normalvariate(1.5, 0.25)
        accuracy = random.normalvariate(0.85, 0.03)

    ab_tester.track_metric("retrieval_strategy_test", variant, "latency", latency)
    ab_tester.track_metric("retrieval_strategy_test", variant, "accuracy", accuracy)

# Get results
results = ab_tester.get_experiment_results("retrieval_strategy_test")
print("A/B Test Results:")
print(json.dumps(results, indent=2, default=str))
```

## 🔍 Automated Optimization

### Hyperparameter Tuning

```python
from sklearn.model_selection import ParameterSampler
import optuna

class HyperparameterOptimizer:
    def __init__(self, pipeline_factory):
        self.pipeline_factory = pipeline_factory

    def optimize_pipeline(self, train_data, val_data, param_space, n_trials=50):
        """Optimize pipeline hyperparameters"""
        def objective(trial):
            # Sample hyperparameters
            params = {}
            for param_name, param_config in param_space.items():
                if param_config["type"] == "int":
                    params[param_name] = trial.suggest_int(
                        param_name,
                        param_config["low"],
                        param_config["high"]
                    )
                elif param_config["type"] == "float":
                    params[param_name] = trial.suggest_float(
                        param_name,
                        param_config["low"],
                        param_config["high"]
                    )
                elif param_config["type"] == "categorical":
                    params[param_name] = trial.suggest_categorical(
                        param_name,
                        param_config["choices"]
                    )

            # Create pipeline with parameters
            pipeline = self.pipeline_factory(params)

            # Evaluate on validation data
            score = self._evaluate_pipeline(pipeline, val_data)

            return score

        # Run optimization
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials)

        # Get best parameters
        best_params = study.best_params
        best_score = study.best_value

        return {
            "best_params": best_params,
            "best_score": best_score,
            "study": study
        }

    def _evaluate_pipeline(self, pipeline, eval_data):
        """Evaluate pipeline performance"""
        # Simplified evaluation - would use actual metrics
        total_score = 0

        for query, expected_results in eval_data:
            try:
                results = pipeline.run({"query": query})
                score = self._calculate_query_score(results, expected_results)
                total_score += score
            except Exception as e:
                print(f"Error evaluating query '{query}': {e}")
                total_score += 0  # Penalize failures

        return total_score / len(eval_data)

    def _calculate_query_score(self, results, expected):
        """Calculate score for a single query"""
        # Simplified scoring - would use proper retrieval metrics
        retrieved_ids = {doc.id for doc in results["documents"]}
        expected_ids = set(expected)

        if not expected_ids:
            return 1.0 if not retrieved_ids else 0.0

        precision = len(retrieved_ids & expected_ids) / len(retrieved_ids) if retrieved_ids else 0
        recall = len(retrieved_ids & expected_ids) / len(expected_ids)

        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return f1

# Usage
def create_optimized_pipeline(params):
    """Factory function for creating pipelines with different parameters"""
    pipeline = Pipeline()

    # Retriever with tunable parameters
    retriever = EmbeddingRetriever(
        document_store=document_store,
        top_k=params["top_k"]
    )
    pipeline.add_component("retriever", retriever)

    # Generator with tunable parameters
    generator = OpenAIGenerator(
        model=params["model"],
        generation_kwargs={
            "temperature": params["temperature"],
            "max_tokens": params["max_tokens"]
        }
    )
    pipeline.add_component("generator", generator)

    # Connect components
    pipeline.connect("retriever", "generator")

    return pipeline

# Define parameter space
param_space = {
    "top_k": {"type": "int", "low": 3, "high": 10},
    "model": {"type": "categorical", "choices": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]},
    "temperature": {"type": "float", "low": 0.1, "high": 1.0},
    "max_tokens": {"type": "int", "low": 100, "high": 500}
}

# Sample evaluation data
eval_data = [
    ("What is machine learning?", ["doc1", "doc2"]),
    ("How do neural networks work?", ["doc3", "doc4"])
]

optimizer = HyperparameterOptimizer(create_optimized_pipeline)
results = optimizer.optimize_pipeline(None, eval_data, param_space, n_trials=20)

print("Hyperparameter Optimization Results:")
print(f"Best Parameters: {results['best_params']}")
print(f"Best Score: {results['best_score']:.3f}")
```

## 🎯 Best Practices

### Evaluation Best Practices

1. **Use Multiple Metrics**: Combine precision, recall, F1, NDCG, and user satisfaction
2. **Cross-Validation**: Evaluate on multiple datasets and query types
3. **Statistical Significance**: Use proper statistical tests for comparing systems
4. **User-Centric Metrics**: Include user satisfaction and task completion rates
5. **Continuous Evaluation**: Monitor performance over time and after updates

### Optimization Strategies

1. **Start Simple**: Begin with basic optimizations before advanced techniques
2. **Measure Impact**: A/B test optimizations to ensure they improve user experience
3. **Iterative Approach**: Make small changes and evaluate each incrementally
4. **Resource Awareness**: Balance performance improvements with resource costs
5. **Monitoring**: Track optimization impact on all system metrics

### Automation and MLOps

1. **Automated Testing**: Implement continuous evaluation pipelines
2. **Model Versioning**: Track which optimizations work for which model versions
3. **Rollback Capability**: Ability to revert optimizations that degrade performance
4. **Experiment Tracking**: Log all optimization experiments and results
5. **Production Monitoring**: Monitor optimized systems for performance regression

## 📈 Next Steps

With evaluation and optimization mastered, you're ready to:

- **[Chapter 7: Custom Components](07-custom-components.md)** - Extend Haystack with custom functionality
- **[Chapter 8: Production Deployment](08-production-deployment.md)** - Deploy optimized systems at scale

---

**Ready to build custom Haystack components? Continue to [Chapter 7: Custom Components](07-custom-components.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `results`, `query` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Evaluation & Optimization` as an operating subsystem inside **Haystack: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `mean`, `print`, `predictions` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Evaluation & Optimization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `results` receives stable contracts.
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
- search upstream code for `self` and `results` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Pipelines & Workflows](05-pipelines-workflows.md)
- [Next Chapter: Chapter 7: Custom Components](07-custom-components.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
