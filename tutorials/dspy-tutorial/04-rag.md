---
layout: default
title: "DSPy Tutorial - Chapter 4: Retrieval-Augmented Generation"
nav_order: 4
has_children: false
parent: DSPy Tutorial
---

# Chapter 4: Retrieval-Augmented Generation (RAG) with DSPy

Welcome to **Chapter 4: Retrieval-Augmented Generation (RAG) with DSPy**. In this part of **DSPy Tutorial: Programming Language Models**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build powerful RAG systems that combine retrieval and generation for accurate, knowledgeable AI responses.

## Overview

Retrieval-Augmented Generation (RAG) combines the power of retrieval systems (finding relevant information) with generation models (creating natural responses). DSPy makes it easy to build sophisticated RAG systems that automatically optimize retrieval and generation components.

## Basic RAG Architecture

### Simple RAG Pipeline

```python
import dspy

# Configure DSPy with retrieval model
rm = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
dspy.settings.configure(rm=rm)

class BasicRAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        # Retrieval component
        self.retrieve = dspy.Retrieve(k=num_passages)

        # Generation component
        self.generate_answer = dspy.Predict(RAGSignature)

    def forward(self, question):
        # Step 1: Retrieve relevant passages
        retrieved_passages = self.retrieve(question)

        # Step 2: Generate answer using retrieved context
        answer = self.generate_answer(
            question=question,
            context=retrieved_passages.passages
        )

        return dspy.Prediction(
            context=retrieved_passages.passages,
            answer=answer.answer
        )

# RAG signature
class RAGSignature(dspy.Signature):
    """Generate answer based on retrieved context."""

    question = dspy.InputField(desc="user question")
    context = dspy.InputField(desc="retrieved relevant passages")
    answer = dspy.OutputField(desc="answer based on context")

# Usage
rag = BasicRAG(num_passages=3)
result = rag(question="What is the capital of France?")

print(f"Retrieved {len(result.context)} passages")
print(f"Answer: {result.answer}")
```

### Understanding RAG Components

```python
# The retrieval component
retrieve = dspy.Retrieve(k=3)

# Returns passages with scores
passages = retrieve("machine learning")

print("Passage 1:", passages.passages[0][:200] + "...")
print("Score 1:", passages.scores[0])

# The generation component uses retrieved context
class ContextualQA(dspy.Signature):
    question = dspy.InputField()
    context = dspy.InputField(desc="relevant information")
    grounded_answer = dspy.OutputField(desc="answer supported by context")

generate = dspy.Predict(ContextualQA)

# Combine retrieval + generation
def rag_qa(question):
    passages = retrieve(question)
    context = "\n".join(passages.passages[:3])

    answer = generate(
        question=question,
        context=context
    )

    return answer.grounded_answer
```

## Advanced RAG Patterns

### Multi-Hop Retrieval

```python
class MultiHopRAG(dspy.Module):
    def __init__(self, num_hops=2, passages_per_hop=3):
        super().__init__()

        self.num_hops = num_hops
        self.passages_per_hop = passages_per_hop

        # Components for each hop
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_query = dspy.Predict(QueryExpansion)
        self.generate_answer = dspy.Predict(MultiHopAnswer)

    def forward(self, question):
        all_passages = []
        current_query = question

        # Multi-hop retrieval
        for hop in range(self.num_hops):
            # Retrieve passages for current query
            passages = self.retrieve(current_query)
            all_passages.extend(passages.passages)

            # Generate next query based on current findings
            if hop < self.num_hops - 1:  # Not the last hop
                query_expansion = self.generate_query(
                    original_question=question,
                    current_findings="\n".join(passages.passages),
                    hop_number=hop + 1
                )
                current_query = query_expansion.expanded_query

        # Remove duplicates and limit total passages
        unique_passages = list(dict.fromkeys(all_passages))[:self.passages_per_hop * 2]

        # Generate final answer
        answer = self.generate_answer(
            question=question,
            context="\n".join(unique_passages)
        )

        return dspy.Prediction(
            context=unique_passages,
            answer=answer.answer,
            reasoning=answer.reasoning,
            hops=self.num_hops
        )

# Supporting signatures
class QueryExpansion(dspy.Signature):
    """Expand query for next retrieval hop."""

    original_question = dspy.InputField()
    current_findings = dspy.InputField(desc="information found so far")
    hop_number = dspy.InputField(desc="which hop this is")
    expanded_query = dspy.OutputField(desc="improved query for next hop")

class MultiHopAnswer(dspy.Signature):
    """Generate answer using multi-hop context."""

    question = dspy.InputField()
    context = dspy.InputField(desc="information from multiple hops")
    answer = dspy.OutputField(desc="comprehensive answer")
    reasoning = dspy.OutputField(desc="reasoning across hops")

# Usage
multi_hop_rag = MultiHopRAG(num_hops=2)
result = multi_hop_rag("How does climate change affect polar bears?")

print(f"Hops used: {result.hops}")
print(f"Passages retrieved: {len(result.context)}")
print(f"Answer: {result.answer}")
```

### Reranking-Based RAG

```python
class RerankingRAG(dspy.Module):
    def __init__(self, num_candidates=10, num_final=3):
        super().__init__()

        self.num_candidates = num_candidates
        self.num_final = num_final

        # Retrieve more candidates than needed
        self.retrieve = dspy.Retrieve(k=num_candidates)

        # Reranking component
        self.rerank = dspy.Predict(RerankSignature)

        # Final generation
        self.generate = dspy.Predict(FinalAnswer)

    def forward(self, question):
        # Step 1: Retrieve candidate passages
        candidates = self.retrieve(question)

        # Step 2: Rerank passages by relevance
        reranked = self.rerank(
            question=question,
            passages=candidates.passages
        )

        # Take top passages after reranking
        top_passages = reranked.top_passages[:self.num_final]

        # Step 3: Generate final answer
        answer = self.generate(
            question=question,
            context=top_passages
        )

        return dspy.Prediction(
            candidates=candidates.passages,
            top_passages=top_passages,
            answer=answer.answer,
            confidence=answer.confidence
        )

# Reranking signatures
class RerankSignature(dspy.Signature):
    """Rerank passages by relevance to question."""

    question = dspy.InputField()
    passages = dspy.InputField(desc="candidate passages to rerank")
    top_passages = dspy.OutputField(desc=f"top {self.num_final} most relevant passages")

class FinalAnswer(dspy.Signature):
    """Generate final answer from top passages."""

    question = dspy.InputField()
    context = dspy.InputField(desc="highest-ranked passages")
    answer = dspy.OutputField(desc="final answer")
    confidence = dspy.OutputField(desc="confidence score 0-1")

# Usage
reranking_rag = RerankingRAG(num_candidates=10, num_final=3)
result = reranking_rag("What are the benefits of renewable energy?")

print(f"Candidates: {len(result.candidates)}")
print(f"Top passages: {len(result.top_passages)}")
print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
```

### Evidence-Based RAG

```python
class EvidenceBasedRAG(dspy.Module):
    def __init__(self, num_passages=5):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.extract_evidence = dspy.Predict(EvidenceExtraction)
        self.verify_claims = dspy.Predict(ClaimVerification)
        self.generate_answer = dspy.Predict(EvidenceBasedAnswer)

    def forward(self, question):
        # Retrieve passages
        passages = self.retrieve(question)

        # Extract evidence from passages
        evidence = self.extract_evidence(
            question=question,
            passages=passages.passages
        )

        # Verify claims in evidence
        verification = self.verify_claims(
            question=question,
            evidence=evidence.extracted_evidence
        )

        # Generate answer with verified evidence
        answer = self.generate_answer(
            question=question,
            verified_evidence=verification.verified_claims,
            confidence_scores=verification.confidence_scores
        )

        return dspy.Prediction(
            passages=passages.passages,
            evidence=evidence.extracted_evidence,
            verified_claims=verification.verified_claims,
            answer=answer.answer,
            confidence=answer.overall_confidence
        )

# Evidence-based signatures
class EvidenceExtraction(dspy.Signature):
    """Extract relevant evidence from passages."""

    question = dspy.InputField()
    passages = dspy.InputField()
    extracted_evidence = dspy.OutputField(desc="key facts and quotes supporting answer")

class ClaimVerification(dspy.Signature):
    """Verify claims and assign confidence scores."""

    question = dspy.InputField()
    evidence = dspy.InputField()
    verified_claims = dspy.OutputField(desc="claims confirmed by evidence")
    confidence_scores = dspy.OutputField(desc="confidence scores for each claim")

class EvidenceBasedAnswer(dspy.Signature):
    """Generate answer supported by verified evidence."""

    question = dspy.InputField()
    verified_evidence = dspy.InputField()
    confidence_scores = dspy.InputField()
    answer = dspy.OutputField(desc="answer with evidence")
    overall_confidence = dspy.OutputField(desc="overall confidence 0-1")

# Usage
evidence_rag = EvidenceBasedRAG()
result = evidence_rag("Is climate change caused by human activities?")

print(f"Evidence extracted: {len(result.evidence.split('.'))}")
print(f"Verified claims: {len(result.verified_claims.split('.'))}")
print(f"Answer: {result.answer}")
```

## DSPy-Optimized RAG

### Automatic RAG Optimization

```python
# DSPy can automatically optimize RAG components
def optimize_rag(trainset, valset):
    """Optimize RAG system using DSPy teleprompters."""

    # Define the RAG program
    class OptimizableRAG(dspy.Module):
        def __init__(self):
            super().__init__()
            self.retrieve = dspy.Retrieve(k=dspy.Suggest(num_passages))  # Optimize k
            self.generate = dspy.Predict(RAGSignature)

        def forward(self, question):
            passages = self.retrieve(question)
            answer = self.generate(question=question, context=passages.passages)
            return answer

    # Create program instance
    program = OptimizableRAG()

    # Define metric for optimization
    def rag_metric(example, prediction, trace=None):
        """Evaluate RAG answer quality."""
        question = example.question
        gold_answer = example.answer

        # Simple exact match (could be more sophisticated)
        return prediction.answer.lower().strip() == gold_answer.lower().strip()

    # Bootstrap few-shot examples
    teleprompter = dspy.BootstrapFewShot(metric=rag_metric, max_bootstraps=3)
    optimized_rag = teleprompter.compile(program, trainset=trainset)

    # Evaluate on validation set
    evaluator = dspy.Evaluate(
        devset=valset,
        metric=rag_metric,
        num_threads=4
    )

    score = evaluator(optimized_rag)
    print(f"Optimized RAG score: {score}")

    return optimized_rag

# Example usage (requires actual datasets)
# train_examples = load_your_training_data()
# val_examples = load_your_validation_data()
# optimized_rag = optimize_rag(train_examples, val_examples)
```

### Optimizing Retrieval Parameters

```python
# DSPy can optimize retrieval parameters like number of passages
class AdaptiveRAG(dspy.Module):
    def __init__(self):
        super().__init__()

        # DSPy will optimize these parameters
        self.num_passages = dspy.Suggest(candidates=[1, 3, 5, 7, 10])

        # Retrieval and generation
        self.retrieve = dspy.Retrieve(k=self.num_passages)
        self.generate = dspy.Predict(RAGSignature)

    def forward(self, question):
        passages = self.retrieve(question)
        answer = self.generate(question=question, context=passages.passages)
        return answer

# The optimization process will try different values of num_passages
# and find the best one for your specific use case
```

## RAG with Different Retrieval Models

### Vector Database RAG

```python
# Using Pinecone for vector retrieval
class PineconeRAG(dspy.Module):
    def __init__(self, index_name, api_key, dimension=768):
        super().__init__()

        # Configure Pinecone retrieval
        self.rm = dspy.Pinecone(
            index=index_name,
            api_key=api_key,
            dimension=dimension
        )

        dspy.settings.configure(rm=self.rm)

        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.Predict(RAGSignature)

    def forward(self, question):
        passages = self.retrieve(question)
        answer = self.generate(question=question, context=passages.passages)
        return answer

# Usage
pinecone_rag = PineconeRAG(
    index_name="my-knowledge-base",
    api_key="your-pinecone-key"
)

result = pinecone_rag("What is machine learning?")
```

### Hybrid Retrieval RAG

```python
class HybridRAG(dspy.Module):
    def __init__(self):
        super().__init__()

        # Multiple retrieval strategies
        self.bm25_retrieve = dspy.Retrieve(k=3, retrieval_model="bm25")
        self.semantic_retrieve = dspy.Retrieve(k=3, retrieval_model="semantic")

        # Fusion component
        self.fuse = dspy.Predict(FusionSignature)

        # Final generation
        self.generate = dspy.Predict(RAGSignature)

    def forward(self, question):
        # Retrieve using different methods
        bm25_results = self.bm25_retrieve(question)
        semantic_results = self.semantic_retrieve(question)

        # Fuse results
        fusion = self.fuse(
            question=question,
            bm25_passages=bm25_results.passages,
            bm25_scores=bm25_results.scores,
            semantic_passages=semantic_results.passages,
            semantic_scores=semantic_results.scores
        )

        # Generate final answer
        answer = self.generate(
            question=question,
            context=fusion.fused_passages
        )

        return answer

class FusionSignature(dspy.Signature):
    """Fuse results from multiple retrieval methods."""

    question = dspy.InputField()
    bm25_passages = dspy.InputField()
    bm25_scores = dspy.InputField()
    semantic_passages = dspy.InputField()
    semantic_scores = dspy.InputField()
    fused_passages = dspy.OutputField(desc="best passages combining both methods")

# Usage
hybrid_rag = HybridRAG()
result = hybrid_rag("Explain quantum computing")
```

## RAG Evaluation and Metrics

### Comprehensive RAG Evaluation

```python
def evaluate_rag_system(rag_system, testset):
    """Comprehensive RAG evaluation."""

    # Multiple evaluation metrics
    metrics = {
        "exact_match": lambda pred, gold: pred.answer.strip().lower() == gold.answer.strip().lower(),
        "contains_answer": lambda pred, gold: gold.answer.lower() in pred.answer.lower(),
        "context_relevance": evaluate_context_relevance,
        "answer_fluency": evaluate_fluency,
        "factual_accuracy": evaluate_factual_accuracy
    }

    results = {metric_name: [] for metric_name in metrics}

    for example in testset:
        prediction = rag_system(example.question)

        for metric_name, metric_func in metrics.items():
            score = metric_func(prediction, example)
            results[metric_name].append(score)

    # Calculate averages
    summary = {}
    for metric_name, scores in results.items():
        summary[metric_name] = {
            "mean": sum(scores) / len(scores),
            "std": (sum((x - sum(scores)/len(scores))**2 for x in scores) / len(scores))**0.5
        }

    return summary

def evaluate_context_relevance(prediction, example):
    """Evaluate if retrieved context is relevant."""
    context_text = " ".join(prediction.context)
    question_words = set(example.question.lower().split())

    # Simple relevance: percentage of question words in context
    context_words = set(context_text.lower().split())
    overlap = len(question_words.intersection(context_words))

    return overlap / len(question_words) if question_words else 0

def evaluate_fluency(prediction, example):
    """Evaluate answer fluency (placeholder)."""
    # Could use a language model to score fluency
    return 0.8  # Placeholder

def evaluate_factual_accuracy(prediction, example):
    """Evaluate factual accuracy (placeholder)."""
    # Could use fact-checking or comparison with gold standard
    return 0.9  # Placeholder

# Evaluate RAG system
evaluation_results = evaluate_rag_system(rag_system, test_examples)

for metric, stats in evaluation_results.items():
    print(f"{metric}: {stats['mean']:.3f} ± {stats['std']:.3f}")
```

## Production RAG Considerations

### Caching for Performance

```python
class CachedRAG(dspy.Module):
    def __init__(self, cache_ttl=3600):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.Predict(RAGSignature)

        # Simple in-memory cache
        self.cache = {}
        self.cache_ttl = cache_ttl

    def _get_cache_key(self, question):
        """Generate cache key for question."""
        return hash(question)  # Simple hash

    def forward(self, question):
        cache_key = self._get_cache_key(question)
        current_time = time.time()

        # Check cache
        if cache_key in self.cache:
            cached_result, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_ttl:
                return cached_result

        # Compute result
        passages = self.retrieve(question)
        answer = self.generate(question=question, context=passages.passages)

        result = dspy.Prediction(
            context=passages.passages,
            answer=answer.answer,
            cached=False
        )

        # Cache result
        self.cache[cache_key] = (result, current_time)

        return result
```

### Error Handling and Fallbacks

```python
class RobustRAG(dspy.Module):
    def __init__(self):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.Predict(RAGSignature)

        # Fallback generation without retrieval
        self.fallback_generate = dspy.Predict(BasicQA)

    def forward(self, question):
        try:
            # Try RAG approach first
            passages = self.retrieve(question)

            if passages.passages:  # If we got passages
                answer = self.generate(question=question, context=passages.passages)
                return dspy.Prediction(
                    context=passages.passages,
                    answer=answer.answer,
                    method="rag"
                )
            else:
                # No passages found, use fallback
                answer = self.fallback_generate(question=question)
                return dspy.Prediction(
                    context=[],
                    answer=answer.answer,
                    method="fallback"
                )

        except Exception as e:
            # Complete failure, use fallback
            print(f"RAG failed: {e}")
            answer = self.fallback_generate(question=question)
            return dspy.Prediction(
                context=[],
                answer=answer.answer,
                method="error_fallback",
                error=str(e)
            )
```

## Summary

In this chapter, we've explored:

- **Basic RAG**: Simple retrieval + generation pipeline
- **Advanced Patterns**: Multi-hop, reranking, evidence-based RAG
- **DSPy Optimization**: Automatic improvement of RAG components
- **Multiple Retrieval Models**: Vector databases, hybrid retrieval
- **Evaluation**: Comprehensive RAG evaluation metrics
- **Production Features**: Caching, error handling, fallbacks

RAG systems built with DSPy can automatically optimize their retrieval and generation components, leading to more accurate and efficient question-answering systems.

## Key Takeaways

1. **Retrieval + Generation**: Combine the best of both worlds for accurate answers
2. **Multi-Hop Reasoning**: Follow complex information trails across documents
3. **Automatic Optimization**: Let DSPy improve your RAG system's performance
4. **Robust Evaluation**: Use comprehensive metrics for reliable assessment
5. **Production Ready**: Include caching, error handling, and fallbacks

Next, we'll explore **optimization** - how DSPy automatically improves your programs through systematic prompt and model optimization.

---

**Ready for the next chapter?** [Chapter 5: Optimization](05-optimization.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `dspy`, `self`, `question` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Retrieval-Augmented Generation (RAG) with DSPy` as an operating subsystem inside **DSPy Tutorial: Programming Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `answer`, `passages`, `context` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Retrieval-Augmented Generation (RAG) with DSPy` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `dspy`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `question`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/stanfordnlp/dspy)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `dspy` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Modules - Reusable DSPy Components](03-modules.md)
- [Next Chapter: Chapter 5: Automatic Optimization - DSPy's Superpower](05-optimization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
