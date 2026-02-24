---
layout: default
title: "Chapter 4: Query Engines & Retrieval"
parent: "LlamaIndex Tutorial"
nav_order: 4
---

# Chapter 4: Query Engines & Retrieval

Welcome to **Chapter 4: Query Engines & Retrieval**. In this part of **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build sophisticated query engines and retrieval systems for advanced RAG applications.

## 🎯 Overview

This chapter covers LlamaIndex's query engines and retrieval mechanisms, showing you how to build complex query pipelines, implement different retrieval strategies, and create intelligent systems that can answer complex questions using your indexed data.

## 🔍 Basic Query Engines

### Creating Query Engines

```python
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine, TransformQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

# Create basic query engine
def create_basic_query_engine(index):
    """Create a basic query engine from index"""

    # Method 1: Direct query engine from index
    query_engine = index.as_query_engine(
        similarity_top_k=5,  # Number of documents to retrieve
        response_mode="tree_summarize"  # How to synthesize response
    )

    return query_engine

# Create advanced query engine with custom components
def create_advanced_query_engine(index):
    """Create advanced query engine with custom retriever and synthesizer"""

    # Custom retriever
    retriever = index.as_retriever(similarity_top_k=10)

    # Custom response synthesizer
    response_synthesizer = get_response_synthesizer(
        response_mode="tree_summarize",
        use_async=True
    )

    # Post-processors for filtering
    node_postprocessors = [
        SimilarityPostprocessor(similarity_cutoff=0.7)
    ]

    # Create query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=node_postprocessors
    )

    return query_engine

# Usage
basic_engine = create_basic_query_engine(vector_index)
advanced_engine = create_advanced_query_engine(vector_index)

# Query both engines
query = "What are the benefits of machine learning?"

basic_response = basic_engine.query(query)
print(f"Basic Engine: {basic_response}")

advanced_response = advanced_engine.query(query)
print(f"Advanced Engine: {advanced_response}")
```

### Different Response Modes

```python
from llama_index.core import ResponseMode

def demonstrate_response_modes(index):
    """Demonstrate different response synthesis modes"""

    query = "Explain how neural networks learn"

    response_modes = [
        "tree_summarize",      # Hierarchical summarization
        "refine",              # Iterative refinement
        "compact",             # Compact single response
        "simple_summarize",    # Simple summarization
        "accumulate",          # Accumulate all responses
        "no_text"              # Return nodes without synthesis
    ]

    results = {}

    for mode in response_modes:
        try:
            query_engine = index.as_query_engine(
                response_mode=mode,
                similarity_top_k=3
            )

            response = query_engine.query(query)

            results[mode] = {
                "response": str(response),
                "response_length": len(str(response)),
                "source_nodes": len(response.source_nodes) if hasattr(response, 'source_nodes') else 0
            }

            print(f"✓ {mode}: {len(str(response))} chars, {results[mode]['source_nodes']} sources")

        except Exception as e:
            print(f"✗ {mode}: Error - {e}")
            results[mode] = {"error": str(e)}

    return results

# Usage
response_mode_results = demonstrate_response_modes(vector_index)

# Compare response lengths
for mode, result in response_mode_results.items():
    if "response_length" in result:
        print(f"{mode}: {result['response_length']} characters")
```

## 🔄 Advanced Retrieval Strategies

### Multi-Index Query Engines

```python
from llama_index.core.query_engine import SubQueryEngine, MultiStepQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent

def create_multi_index_query_engine(indexes):
    """Create query engine that searches across multiple indexes"""

    # Create individual query engines
    query_engines = {}
    query_engine_tools = []

    for name, index in indexes.items():
        engine = index.as_query_engine(similarity_top_k=3)
        query_engines[name] = engine

        # Create tool for agent
        tool = QueryEngineTool.from_defaults(
            query_engine=engine,
            name=f"{name}_engine",
            description=f"Useful for answering questions about {name}"
        )
        query_engine_tools.append(tool)

    # Method 1: Sub-query engine for complex questions
    sub_query_engine = SubQueryEngine.from_defaults(
        query_engines=query_engines,
        use_async=True
    )

    # Method 2: Multi-step reasoning engine
    multi_step_engine = MultiStepQueryEngine.from_defaults(
        query_engines=query_engines
    )

    # Method 3: Agent-based query engine
    agent = ReActAgent.from_tools(
        tools=query_engine_tools,
        verbose=True
    )

    return {
        "sub_query": sub_query_engine,
        "multi_step": multi_step_engine,
        "agent": agent
    }

# Usage
indexes = {
    "technical": vector_index,  # Technical documentation
    "business": summary_index,  # Business documents
    "general": list_index       # General content
}

multi_engines = create_multi_index_query_engine(indexes)

# Test different approaches
complex_query = "How does machine learning impact business strategy and what are the technical requirements?"

# Sub-query approach
sub_response = multi_engines["sub_query"].query(complex_query)
print(f"Sub-query response: {sub_response}")

# Multi-step approach
multi_response = multi_engines["multi_step"].query(complex_query)
print(f"Multi-step response: {multi_response}")

# Agent approach
agent_response = multi_engines["agent"].chat(complex_query)
print(f"Agent response: {agent_response}")
```

### Custom Retrievers

```python
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore
from typing import List
import numpy as np

class HybridRetriever(BaseRetriever):
    """Custom hybrid retriever combining multiple retrieval strategies"""

    def __init__(self, index, keyword_weight=0.3, semantic_weight=0.7):
        super().__init__()
        self.index = index
        self.keyword_weight = keyword_weight
        self.semantic_weight = semantic_weight

        # Create different retrievers
        self.semantic_retriever = index.as_retriever(similarity_top_k=10)
        self.keyword_retriever = self._create_keyword_retriever()

    def _create_keyword_retriever(self):
        """Create a simple keyword-based retriever"""
        # This would be implemented with a keyword index
        # For now, return semantic retriever as fallback
        return self.semantic_retriever

    def _retrieve(self, query_bundle):
        """Main retrieval logic"""
        query = query_bundle.query_str

        # Get results from both retrievers
        semantic_results = self.semantic_retriever.retrieve(query)
        keyword_results = self.keyword_retriever.retrieve(query)

        # Combine results with weighted scoring
        combined_results = self._combine_results(semantic_results, keyword_results)

        return combined_results

    def _combine_results(self, semantic_results, keyword_results):
        """Combine and re-rank results from multiple retrievers"""

        # Create score mapping
        result_scores = {}

        # Process semantic results
        for result in semantic_results:
            doc_id = result.node.id_
            semantic_score = result.score or 0.5
            result_scores[doc_id] = {
                "node": result.node,
                "semantic_score": semantic_score,
                "keyword_score": 0.0,
                "final_score": 0.0
            }

        # Process keyword results
        for result in keyword_results:
            doc_id = result.node.id_
            keyword_score = result.score or 0.5

            if doc_id in result_scores:
                result_scores[doc_id]["keyword_score"] = keyword_score
            else:
                result_scores[doc_id] = {
                    "node": result.node,
                    "semantic_score": 0.0,
                    "keyword_score": keyword_score,
                    "final_score": 0.0
                }

        # Calculate final scores
        for doc_id, scores in result_scores.items():
            final_score = (
                self.semantic_weight * scores["semantic_score"] +
                self.keyword_weight * scores["keyword_score"]
            )
            scores["final_score"] = final_score

        # Sort by final score and create NodeWithScore objects
        sorted_results = sorted(
            result_scores.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )

        # Return top results
        top_results = []
        for result in sorted_results[:5]:  # Return top 5
            node_with_score = NodeWithScore(
                node=result["node"],
                score=result["final_score"]
            )
            top_results.append(node_with_score)

        return top_results

class TimeWeightedRetriever(BaseRetriever):
    """Retriever that considers document recency"""

    def __init__(self, index, time_decay_factor=0.1):
        super().__init__()
        self.index = index
        self.time_decay_factor = time_decay_factor
        self.base_retriever = index.as_retriever(similarity_top_k=10)

    def _retrieve(self, query_bundle):
        """Retrieve with time-based weighting"""
        query = query_bundle.query_str

        # Get base retrieval results
        base_results = self.base_retriever.retrieve(query)

        # Apply time weighting
        weighted_results = []
        current_time = time.time()

        for result in base_results:
            # Extract timestamp from metadata
            timestamp = result.node.metadata.get("created_at", current_time)
            if isinstance(timestamp, str):
                # Parse timestamp (simplified)
                timestamp = current_time - 86400  # Default to 1 day ago

            # Calculate time weight (newer = higher weight)
            time_diff_days = (current_time - timestamp) / 86400
            time_weight = 1.0 / (1.0 + self.time_decay_factor * time_diff_days)

            # Combine with original score
            original_score = result.score or 0.5
            weighted_score = original_score * (0.7 + 0.3 * time_weight)  # 70% original, 30% time

            weighted_result = NodeWithScore(
                node=result.node,
                score=weighted_score
            )
            weighted_results.append(weighted_result)

        # Re-sort by weighted score
        weighted_results.sort(key=lambda x: x.score, reverse=True)

        return weighted_results[:5]

# Usage
# Hybrid retriever
hybrid_retriever = HybridRetriever(vector_index)
hybrid_query_engine = RetrieverQueryEngine.from_args(hybrid_retriever)

# Time-weighted retriever
time_retriever = TimeWeightedRetriever(vector_index)
time_query_engine = RetrieverQueryEngine.from_args(time_retriever)

# Test queries
test_query = "What are the latest developments in AI?"

hybrid_response = hybrid_query_engine.query(test_query)
print(f"Hybrid response: {hybrid_response}")

time_response = time_query_engine.query(test_query)
print(f"Time-weighted response: {time_response}")
```

## 🔄 Query Transformations

### Query Expansion and Rewriting

```python
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.core.indices.query.query_transform import HyDEQueryTransform

class QueryTransformer:
    """Transform and enhance queries for better retrieval"""

    def __init__(self, index):
        self.index = index

    def create_expanded_query_engine(self):
        """Create query engine with automatic query expansion"""

        # Base retriever
        retriever = self.index.as_retriever(similarity_top_k=5)

        # Create expanded query engine
        query_engine = TransformQueryEngine(
            retriever=retriever,
            query_transform=self._expand_query_transform,
            transform_metadata={"expand_factor": 2}
        )

        return query_engine

    def create_hyde_query_engine(self):
        """Create HyDE (Hypothetical Document Embeddings) query engine"""

        # HyDE transform generates hypothetical answers
        hyde_transform = HyDEQueryTransform(
            llm=self._get_llm(),
            include_original=True
        )

        query_engine = TransformQueryEngine(
            retriever=self.index.as_retriever(similarity_top_k=5),
            query_transform=hyde_transform
        )

        return query_engine

    def _expand_query_transform(self, query_bundle):
        """Custom query expansion logic"""
        from llama_index.core.schema import QueryBundle

        original_query = query_bundle.query_str

        # Simple expansion: add related terms
        expansions = {
            "AI": ["artificial intelligence", "machine learning", "deep learning"],
            "ML": ["machine learning", "algorithms", "data science"],
            "neural": ["neural networks", "deep learning", "AI"]
        }

        expanded_terms = []
        query_lower = original_query.lower()

        for key, terms in expansions.items():
            if key.lower() in query_lower:
                expanded_terms.extend(terms[:2])  # Add up to 2 related terms

        if expanded_terms:
            expanded_query = f"{original_query} {' '.join(set(expanded_terms))}"
        else:
            expanded_query = original_query

        return QueryBundle(
            query_str=expanded_query,
            custom_embedding_strs=query_bundle.custom_embedding_strs
        )

    def _get_llm(self):
        """Get LLM for transformations"""
        from llama_index.llms.openai import OpenAI
        return OpenAI(model="gpt-3.5-turbo", temperature=0.1)

# Usage
transformer = QueryTransformer(vector_index)

# Expanded query engine
expanded_engine = transformer.create_expanded_query_engine()

# HyDE query engine
hyde_engine = transformer.create_hyde_query_engine()

# Test queries
test_queries = [
    "What is AI?",
    "How do neural networks work?"
]

for query in test_queries:
    print(f"\nOriginal: {query}")

    # Expanded query
    expanded_response = expanded_engine.query(query)
    print(f"Expanded response: {expanded_response}")

    # HyDE query
    hyde_response = hyde_engine.query(query)
    print(f"HyDE response: {hyde_response}")
```

### Multi-Step Reasoning

```python
from llama_index.core.query_engine import FLAREInstructQueryEngine
from llama_index.core import PromptTemplate

class MultiStepReasoner:
    """Multi-step reasoning query engine"""

    def __init__(self, index):
        self.index = index

    def create_flare_engine(self):
        """Create FLARE (Forward-Looking Active REtrieval) engine"""

        # FLARE uses special tokens to trigger retrieval during generation
        flare_engine = FLAREInstructQueryEngine(
            query_engine=self.index.as_query_engine(similarity_top_k=3),
            instruct_prompt="""
            Please answer the following question with detailed reasoning.
            If you need additional information, use [Retrieval] to search for it.

            Question: {query}
            """,
            retrieval_instruction="[Retrieval]",
            max_iterations=3,
            verbose=True
        )

        return flare_engine

    def create_step_by_step_engine(self):
        """Create engine that breaks down complex queries"""

        # Custom prompt for step-by-step reasoning
        step_prompt = PromptTemplate("""
        Answer the following question by breaking it down into steps:

        1. Understand the question: What is being asked?
        2. Identify key concepts: What are the main topics involved?
        3. Gather information: What relevant information do I have?
        4. Synthesize answer: How do I combine the information?

        Question: {query}

        Step-by-step answer:
        """)

        query_engine = self.index.as_query_engine(
            text_qa_template=step_prompt,
            similarity_top_k=5
        )

        return query_engine

    def create_comparison_engine(self):
        """Create engine for comparing multiple options"""

        comparison_prompt = PromptTemplate("""
        Compare and contrast the following aspects. Use the provided context to support your analysis.

        Topic: {query}

        Provide a balanced comparison covering:
        - Key differences
        - Advantages and disadvantages
        - Use cases and applications
        - Recommendations

        Analysis:
        """)

        query_engine = self.index.as_query_engine(
            text_qa_template=comparison_prompt,
            similarity_top_k=8  # More context for comparisons
        )

        return query_engine

# Usage
reasoner = MultiStepReasoner(vector_index)

# FLARE reasoning
flare_engine = reasoner.create_flare_engine()
flare_response = flare_engine.query("Explain the relationship between AI and machine learning")
print(f"FLARE response: {flare_response}")

# Step-by-step reasoning
step_engine = reasoner.create_step_by_step_engine()
step_response = step_engine.query("How does gradient descent work in neural networks?")
print(f"Step-by-step response: {step_response}")

# Comparison reasoning
comparison_engine = reasoner.create_comparison_engine()
comparison_response = comparison_engine.query("Compare supervised vs unsupervised learning")
print(f"Comparison response: {comparison_response}")
```

## 📊 Evaluation and Monitoring

### Query Engine Evaluation

```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator
)
import asyncio

class QueryEngineEvaluator:
    """Evaluate query engine performance"""

    def __init__(self, llm=None):
        self.llm = llm or self._get_default_llm()

        # Create evaluators
        self.faithfulness_evaluator = FaithfulnessEvaluator(llm=self.llm)
        self.relevancy_evaluator = RelevancyEvaluator(llm=self.llm)
        self.correctness_evaluator = CorrectnessEvaluator(llm=self.llm)

    def _get_default_llm(self):
        """Get default LLM for evaluation"""
        from llama_index.llms.openai import OpenAI
        return OpenAI(model="gpt-3.5-turbo", temperature=0)

    async def evaluate_query_engine(self, query_engine, eval_queries):
        """Comprehensive evaluation of query engine"""

        results = {
            "queries": [],
            "faithfulness_scores": [],
            "relevancy_scores": [],
            "correctness_scores": [],
            "response_times": []
        }

        for query_data in eval_queries:
            query = query_data["query"]
            reference_answer = query_data.get("reference_answer")
            context = query_data.get("context", "")

            # Time the query
            start_time = time.time()
            response = query_engine.query(query)
            response_time = time.time() - start_time

            # Evaluate metrics
            faithfulness_score = await self.faithfulness_evaluator.aevaluate(
                query=query,
                response=str(response),
                contexts=[context] if context else None
            )

            relevancy_score = await self.relevancy_evaluator.aevaluate(
                query=query,
                response=str(response)
            )

            correctness_score = None
            if reference_answer:
                correctness_score = await self.correctness_evaluator.aevaluate(
                    query=query,
                    response=str(response),
                    reference=reference_answer
                )

            # Store results
            result = {
                "query": query,
                "response": str(response),
                "response_time": response_time,
                "faithfulness": faithfulness_score.score if faithfulness_score else None,
                "relevancy": relevancy_score.score if relevancy_score else None,
                "correctness": correctness_score.score if correctness_score else None
            }

            results["queries"].append(result)

            # Add to summary lists
            if faithfulness_score:
                results["faithfulness_scores"].append(faithfulness_score.score)
            if relevancy_score:
                results["relevancy_scores"].append(relevancy_score.score)
            if correctness_score:
                results["correctness_scores"].append(correctness_score.score)
            results["response_times"].append(response_time)

        # Calculate averages
        results["avg_faithfulness"] = np.mean(results["faithfulness_scores"]) if results["faithfulness_scores"] else None
        results["avg_relevancy"] = np.mean(results["relevancy_scores"]) if results["relevancy_scores"] else None
        results["avg_correctness"] = np.mean(results["correctness_scores"]) if results["correctness_scores"] else None
        results["avg_response_time"] = np.mean(results["response_times"])

        return results

    def compare_query_engines(self, engines, eval_queries):
        """Compare multiple query engines"""

        async def evaluate_all():
            results = {}
            for name, engine in engines.items():
                print(f"Evaluating {name}...")
                results[name] = await self.evaluate_query_engine(engine, eval_queries)
            return results

        # Run evaluations
        import nest_asyncio
        nest_asyncio.apply()

        results = asyncio.run(evaluate_all())

        # Create comparison summary
        comparison = {}
        for name, result in results.items():
            comparison[name] = {
                "avg_faithfulness": result["avg_faithfulness"],
                "avg_relevancy": result["avg_relevancy"],
                "avg_correctness": result["avg_correctness"],
                "avg_response_time": result["avg_response_time"]
            }

        return comparison

# Usage
evaluator = QueryEngineEvaluator()

# Sample evaluation queries
eval_queries = [
    {
        "query": "What is machine learning?",
        "reference_answer": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed.",
        "context": "Machine learning algorithms build mathematical models based on training data to make predictions or decisions."
    },
    {
        "query": "How do neural networks work?",
        "reference_answer": "Neural networks are computing systems inspired by biological neural networks that learn from data through interconnected nodes called neurons.",
        "context": "Neural networks consist of layers of nodes that process information and adjust connections based on training data."
    }
]

# Evaluate single engine
results = asyncio.run(evaluator.evaluate_query_engine(basic_engine, eval_queries))
print(f"Evaluation Results:")
print(f"Average Faithfulness: {results['avg_faithfulness']:.3f}")
print(f"Average Relevancy: {results['avg_relevancy']:.3f}")
print(f"Average Response Time: {results['avg_response_time']:.3f}s")

# Compare multiple engines
engines = {
    "basic": basic_engine,
    "advanced": advanced_engine
}

comparison = evaluator.compare_query_engines(engines, eval_queries)
print("Engine Comparison:")
for name, metrics in comparison.items():
    print(f"{name}: Faithfulness={metrics['avg_faithfulness']:.3f}, Response Time={metrics['avg_response_time']:.3f}s")
```

## 🎯 Best Practices

### Query Engine Selection

| Use Case | Recommended Engine | Configuration |
|:---------|:-------------------|:--------------|
| **Simple Q&A** | Basic query engine | `similarity_top_k=3-5` |
| **Complex reasoning** | Multi-step engine | `response_mode="tree_summarize"` |
| **Multiple sources** | Sub-query engine | Multiple indexes |
| **Real-time search** | Hybrid retriever | BM25 + semantic search |
| **Time-sensitive** | Time-weighted retriever | `time_decay_factor=0.1` |
| **Agent workflows** | ReAct agent | Custom tools |

### Performance Optimization

1. **Choose appropriate response modes** for different query types
2. **Implement caching** for frequent queries
3. **Use async operations** for concurrent processing
4. **Batch similar queries** together
5. **Monitor and tune similarity thresholds**
6. **Implement query expansion** for better retrieval
7. **Use post-processing** to filter irrelevant results

### Evaluation Guidelines

1. **Define clear metrics** for your use case (faithfulness, relevancy, correctness)
2. **Use diverse test queries** covering different scenarios
3. **Include reference answers** for objective evaluation
4. **Monitor performance over time** and after updates
5. **A/B test different configurations** to find optimal settings
6. **Consider user feedback** alongside automated metrics

## 📈 Next Steps

With query engines and retrieval mastered, you're ready to:

- **[Chapter 5: Advanced RAG Patterns](05-advanced-rag.md)** - Multi-modal, agent-based, and hybrid approaches
- **[Chapter 6: Custom Components](06-custom-components.md)** - Building custom loaders, indexes, and query engines
- **[Chapter 7: Production Deployment](07-production-deployment.md)** - Scaling LlamaIndex applications for production

---

**Ready to explore advanced RAG patterns? Continue to [Chapter 5: Advanced RAG Patterns](05-advanced-rag.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `query`, `self`, `results` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Query Engines & Retrieval` as an operating subsystem inside **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `index`, `engine` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Query Engines & Retrieval` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `query`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `results`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/run-llama/llama_index)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `query` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Indexing & Storage](03-indexing-storage.md)
- [Next Chapter: Chapter 5: Advanced RAG Patterns](05-advanced-rag.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
