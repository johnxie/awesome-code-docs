---
layout: default
title: "DSPy Tutorial - Chapter 3: Modules"
nav_order: 3
has_children: false
parent: DSPy Tutorial
---

# Chapter 3: Modules - Reusable DSPy Components

Welcome to **Chapter 3: Modules - Reusable DSPy Components**. In this part of **DSPy Tutorial: Programming Language Models**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Discover DSPy's built-in modules and learn to create custom modules for complex workflows.

## Overview

Modules are the reusable building blocks in DSPy. They implement specific behaviors using language models and can be combined to create complex systems. DSPy provides several built-in modules, and you can create custom modules for specialized tasks.

## Built-in Modules

### Predict

The most basic module - directly calls the LM with a signature:

```python
import dspy

class BasicQA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

# Basic prediction
predict_module = dspy.Predict(BasicQA)

result = predict_module(question="What is the capital of France?")
print(result.answer)  # "Paris"
```

### ChainOfThought

Adds step-by-step reasoning to predictions:

```python
class MathReasoning(dspy.Signature):
    problem = dspy.InputField()
    reasoning = dspy.OutputField(desc="step-by-step reasoning")
    answer = dspy.OutputField(desc="final numerical answer")

# Chain of thought reasoning
cot_module = dspy.ChainOfThought(MathReasoning)

result = cot_module(problem="If a train travels 120 km in 2 hours, what is its speed?")
print(f"Reasoning: {result.reasoning}")
print(f"Answer: {result.answer}")
```

### ReAct

Reasoning + Acting - the module can use tools and external information:

```python
class ReActQA(dspy.Signature):
    question = dspy.InputField()
    trajectory = dspy.OutputField(desc="reasoning steps and actions")
    answer = dspy.OutputField(desc="final answer")

# ReAct module
react_module = dspy.ReAct(ReActQA)

# Note: ReAct typically works with tools (covered in advanced chapters)
```

### MultiChainComparison

Compares multiple reasoning chains to improve accuracy:

```python
class ComparisonQA(dspy.Signature):
    question = dspy.InputField()
    reasoning1 = dspy.OutputField(desc="first reasoning approach")
    answer1 = dspy.OutputField(desc="first answer")
    reasoning2 = dspy.OutputField(desc="second reasoning approach")
    answer2 = dspy.OutputField(desc="second answer")
    final_answer = dspy.OutputField(desc="best answer after comparison")

# Multi-chain comparison
mcc_module = dspy.MultiChainComparison(ComparisonQA)

result = mcc_module(question="What is 15% of 200?")
print(f"Final Answer: {result.final_answer}")
```

### ProgramOfThought

Specialized for mathematical and symbolic reasoning:

```python
class SymbolicReasoning(dspy.Signature):
    problem = dspy.InputField()
    program = dspy.OutputField(desc="Python code to solve the problem")
    result = dspy.OutputField(desc="execution result")

# Program of thought
pot_module = dspy.ProgramOfThought(SymbolicReasoning)

result = pot_module(problem="Calculate the factorial of 5")
print(f"Code: {result.program}")
print(f"Result: {result.result}")
```

## Retrieval Modules

### Retrieve

Retrieves relevant passages from a knowledge base:

```python
# Configure retrieval model
rm = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
dspy.settings.configure(rm=rm)

# Basic retrieval
retrieve_module = dspy.Retrieve(k=3)  # Get top 3 passages

passages = retrieve_module("What is machine learning?")
for i, passage in enumerate(passages.passages):
    print(f"Passage {i+1}: {passage[:100]}...")
```

### RetrieveThenRead

Combines retrieval with reading comprehension:

```python
class RetrievalQA(dspy.Signature):
    question = dspy.InputField()
    context = dspy.InputField()
    answer = dspy.OutputField()

# Retrieve then read
rtr_module = dspy.RetrieveThenRead(RetrievalQA, k=3)

result = rtr_module(question="What causes earthquakes?")
print(f"Answer: {result.answer}")
```

## Custom Modules

### Basic Custom Module

```python
class CustomQAModule(dspy.Module):
    def __init__(self):
        super().__init__()
        # Define sub-modules
        self.generate_answer = dspy.Predict(BasicQA)

    def forward(self, question):
        # Implement the forward pass
        result = self.generate_answer(question=question)
        return result

# Usage
custom_qa = CustomQAModule()
result = custom_qa(question="What is AI?")
print(result.answer)
```

### Multi-Step Custom Module

```python
class ResearchModule(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        # Define signatures
        self.plan_signature = dspy.Signature(
            "topic: str -> research_plan: str"
        )
        self.search_signature = dspy.Signature(
            "query: str, plan: str -> findings: str"
        )
        self.synthesize_signature = dspy.Signature(
            "topic: str, findings: str -> summary: str, key_points: list"
        )

        # Define modules
        self.planner = dspy.Predict(self.plan_signature)
        self.searcher = dspy.Predict(self.search_signature)
        self.synthesizer = dspy.Predict(self.synthesize_signature)

        self.num_passages = num_passages

    def forward(self, topic):
        # Step 1: Create research plan
        plan_result = self.planner(topic=topic)
        research_plan = plan_result.research_plan

        # Step 2: Conduct research (simplified)
        findings_result = self.searcher(
            query=topic,
            plan=research_plan
        )
        findings = findings_result.findings

        # Step 3: Synthesize results
        synthesis_result = self.synthesizer(
            topic=topic,
            findings=findings
        )

        return dspy.Prediction(
            plan=research_plan,
            findings=findings,
            summary=synthesis_result.summary,
            key_points=synthesis_result.key_points
        )

# Usage
researcher = ResearchModule()
result = researcher(topic="Quantum Computing")
print(f"Summary: {result.summary}")
print(f"Key Points: {result.key_points}")
```

### Conditional Module

```python
class AdaptiveQAModule(dspy.Module):
    def __init__(self):
        super().__init__()

        # Different strategies for different question types
        self.simple_qa = dspy.Predict(BasicQA)
        self.complex_qa = dspy.ChainOfThought(ComplexQA)

        # Classifier to determine question complexity
        self.classifier = dspy.Predict(QuestionClassifier)

    def forward(self, question):
        # Classify question complexity
        classification = self.classifier(question=question)

        if classification.complexity == "simple":
            result = self.simple_qa(question=question)
        else:
            result = self.complex_qa(question=question)

        return dspy.Prediction(
            answer=result.answer,
            reasoning=result.get('reasoning', 'Direct answer'),
            strategy=classification.complexity
        )

# Supporting signatures
class ComplexQA(dspy.Signature):
    question = dspy.InputField()
    reasoning = dspy.OutputField(desc="step-by-step reasoning")
    answer = dspy.OutputField()

class QuestionClassifier(dspy.Signature):
    question = dspy.InputField()
    complexity = dspy.OutputField(desc="simple or complex")

# Usage
adaptive_qa = AdaptiveQAModule()

# Simple question
result1 = adaptive_qa("What is 2+2?")
print(f"Simple: {result1.answer} (Strategy: {result1.strategy})")

# Complex question
result2 = adaptive_qa("Explain the impact of AI on employment")
print(f"Complex: {result2.answer} (Strategy: {result2.strategy})")
```

## RAG Modules

### Basic RAG Module

```python
class BasicRAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        # Retrieval component
        self.retrieve = dspy.Retrieve(k=num_passages)

        # Generation component
        self.generate = dspy.Predict(RAGSignature)

    def forward(self, question):
        # Retrieve relevant passages
        passages = self.retrieve(question)

        # Generate answer using context
        result = self.generate(
            question=question,
            context=passages.passages
        )

        return dspy.Prediction(
            context=passages.passages,
            answer=result.answer
        )

# RAG signature
class RAGSignature(dspy.Signature):
    question = dspy.InputField()
    context = dspy.InputField(desc="relevant passages")
    answer = dspy.OutputField()

# Usage
rag = BasicRAG()
result = rag("What is machine learning?")
print(f"Context: {result.context[:200]}...")
print(f"Answer: {result.answer}")
```

### Advanced RAG with Multiple Retrieval

```python
class AdvancedRAG(dspy.Module):
    def __init__(self, num_passages=5):
        super().__init__()

        # Multiple retrieval strategies
        self.bm25_retrieve = dspy.Retrieve(k=num_passages//2, retrieval_model="bm25")
        self.semantic_retrieve = dspy.Retrieve(k=num_passages//2, retrieval_model="semantic")

        # Reranking component
        self.rerank = dspy.Predict(RerankSignature)

        # Generation with evidence
        self.generate = dspy.Predict(EvidenceBasedQA)

    def forward(self, question):
        # Retrieve from multiple sources
        bm25_passages = self.bm25_retrieve(question)
        semantic_passages = self.semantic_retrieve(question)

        # Combine and rerank
        all_passages = bm25_passages.passages + semantic_passages.passages

        rerank_result = self.rerank(
            question=question,
            passages=all_passages
        )

        top_passages = rerank_result.top_passages[:3]  # Top 3 after reranking

        # Generate answer with evidence
        final_result = self.generate(
            question=question,
            context=top_passages
        )

        return dspy.Prediction(
            question=question,
            context=top_passages,
            answer=final_result.answer,
            evidence=final_result.evidence,
            confidence=final_result.confidence
        )

# Supporting signatures
class RerankSignature(dspy.Signature):
    question = dspy.InputField()
    passages = dspy.InputField(desc="list of passages to rerank")
    top_passages = dspy.OutputField(desc="top 3 most relevant passages")

class EvidenceBasedQA(dspy.Signature):
    question = dspy.InputField()
    context = dspy.InputField(desc="relevant passages")
    answer = dspy.OutputField()
    evidence = dspy.OutputField(desc="evidence supporting the answer")
    confidence = dspy.OutputField(desc="confidence score 0-1")

# Usage
advanced_rag = AdvancedRAG()
result = advanced_rag("How does photosynthesis work?")
print(f"Answer: {result.answer}")
print(f"Evidence: {result.evidence}")
print(f"Confidence: {result.confidence}")
```

## Ensemble Modules

### Voting Ensemble

```python
class VotingEnsemble(dspy.Module):
    def __init__(self, modules, weights=None):
        super().__init__()

        self.modules = modules
        self.weights = weights or [1.0] * len(modules)

        # Voting mechanism
        self.voter = dspy.Predict(VotingSignature)

    def forward(self, **kwargs):
        # Get predictions from all modules
        predictions = []
        for module in self.modules:
            pred = module(**kwargs)
            predictions.append(pred)

        # Format for voting
        candidates = [p.answer for p in predictions]
        reasoning = [p.get('reasoning', '') for p in predictions]

        # Vote on best answer
        vote_result = self.voter(
            question=kwargs.get('question', ''),
            candidates=candidates,
            reasoning=reasoning
        )

        return dspy.Prediction(
            answer=vote_result.final_answer,
            reasoning=vote_result.voting_reasoning,
            all_candidates=candidates,
            confidence=vote_result.confidence
        )

# Voting signature
class VotingSignature(dspy.Signature):
    question = dspy.InputField()
    candidates = dspy.InputField(desc="list of candidate answers")
    reasoning = dspy.InputField(desc="reasoning for each candidate")
    final_answer = dspy.OutputField(desc="best answer after voting")
    voting_reasoning = dspy.OutputField(desc="reasoning for the chosen answer")
    confidence = dspy.OutputField(desc="confidence in final answer")

# Usage
modules = [
    dspy.ChainOfThought(BasicQA),
    dspy.Predict(BasicQA),
    dspy.ReAct(BasicQA)
]

ensemble = VotingEnsemble(modules)
result = ensemble(question="What is the speed of light?")
print(f"Ensemble Answer: {result.answer}")
```

### Weighted Ensemble

```python
class WeightedEnsemble(dspy.Module):
    def __init__(self, experts):
        super().__init__()

        self.experts = experts  # List of (module, weight) tuples

        # Meta-learner to combine predictions
        self.combiner = dspy.Predict(CombinePredictions)

    def forward(self, **kwargs):
        # Get weighted predictions
        predictions = []
        weights = []

        for expert, weight in self.experts:
            pred = expert(**kwargs)
            predictions.append(pred)
            weights.append(weight)

        # Combine predictions
        answers = [p.answer for p in predictions]

        combine_result = self.combiner(
            question=kwargs.get('question', ''),
            answers=answers,
            weights=weights
        )

        return dspy.Prediction(
            answer=combine_result.final_answer,
            combination_reasoning=combine_result.reasoning,
            expert_answers=list(zip(answers, weights))
        )

# Combination signature
class CombinePredictions(dspy.Signature):
    question = dspy.InputField()
    answers = dspy.InputField(desc="list of answers from experts")
    weights = dspy.InputField(desc="corresponding weights for each answer")
    final_answer = dspy.OutputField(desc="weighted combination of answers")
    reasoning = dspy.OutputField(desc="reasoning for the combination")

# Usage
experts = [
    (dspy.ChainOfThought(BasicQA), 0.4),
    (dspy.Predict(BasicQA), 0.3),
    (dspy.ReAct(BasicQA), 0.3)
]

weighted_ensemble = WeightedEnsemble(experts)
result = weighted_ensemble(question="Explain neural networks")
```

## Module Composition

### Pipeline Pattern

```python
class PipelineModule(dspy.Module):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps  # List of modules in sequence

    def forward(self, **kwargs):
        result = kwargs

        for step in self.steps:
            # Pass results from previous step to next
            if isinstance(result, dspy.Prediction):
                result = step(**result.__dict__)
            else:
                result = step(**result)

        return result

# Example pipeline: Retrieve -> Rerank -> Generate
pipeline = PipelineModule([
    lambda **kwargs: dspy.Retrieve(k=5)(kwargs.get('question', '')),
    lambda **kwargs: dspy.Predict(RerankSignature)(
        question=kwargs.get('question', ''),
        passages=kwargs.get('passages', [])
    ),
    lambda **kwargs: dspy.Predict(RAGSignature)(
        question=kwargs.get('question', ''),
        context=kwargs.get('top_passages', [])
    )
])

result = pipeline(question="What is quantum computing?")
```

### DAG (Directed Acyclic Graph) Pattern

```python
class DAGModule(dspy.Module):
    def __init__(self, dag_definition):
        super().__init__()
        self.dag = dag_definition  # Dict of step_name -> (module, dependencies)

    def forward(self, **kwargs):
        # Execute DAG
        results = {}
        executed = set()

        while len(executed) < len(self.dag):
            # Find steps whose dependencies are satisfied
            ready_steps = [
                step for step, (module, deps) in self.dag.items()
                if step not in executed and all(d in executed for d in deps)
            ]

            if not ready_steps:
                raise ValueError("Circular dependency or missing dependencies")

            # Execute ready steps
            for step in ready_steps:
                module, deps = self.dag[step]

                # Gather inputs from dependencies
                step_inputs = kwargs.copy()
                for dep in deps:
                    if dep in results:
                        step_inputs.update(results[dep].__dict__)

                # Execute step
                result = module(**step_inputs)
                results[step] = result
                executed.add(step)

        return results

# Example DAG: Parallel analysis then synthesis
dag = {
    "factual_analysis": (dspy.Predict(FactualAnalysis), []),
    "sentiment_analysis": (dspy.Predict(SentimentAnalysis), []),
    "synthesis": (dspy.Predict(Synthesis), ["factual_analysis", "sentiment_analysis"])
}

dag_module = DAGModule(dag)
result = dag_module(text="I love this new AI model, it's incredibly fast and accurate!")
```

## Module Testing and Validation

### Unit Testing Modules

```python
def test_module(module, test_cases):
    """Test a module with various inputs"""

    results = []

    for test_case in test_cases:
        try:
            result = module(**test_case["input"])

            # Validate output structure
            for expected_field in test_case["expected_fields"]:
                assert hasattr(result, expected_field), f"Missing field: {expected_field}"

            # Validate output quality (custom validation)
            if "validator" in test_case:
                assert test_case["validator"](result), f"Validation failed for {test_case['input']}"

            results.append({"status": "pass", "result": result})

        except Exception as e:
            results.append({"status": "fail", "error": str(e), "input": test_case["input"]})

    return results

# Test cases
test_cases = [
    {
        "input": {"question": "What is 2+2?"},
        "expected_fields": ["answer"],
        "validator": lambda r: "4" in r.answer
    },
    {
        "input": {"question": "What is the capital of France?"},
        "expected_fields": ["answer"],
        "validator": lambda r: "paris" in r.answer.lower()
    }
]

# Test a module
qa_module = dspy.Predict(BasicQA)
test_results = test_module(qa_module, test_cases)

for i, result in enumerate(test_results):
    print(f"Test {i+1}: {result['status']}")
```

### Performance Benchmarking

```python
import time

def benchmark_module(module, test_inputs, num_runs=5):
    """Benchmark module performance"""

    latencies = []
    token_counts = []  # If available

    for _ in range(num_runs):
        for test_input in test_inputs:
            start_time = time.time()

            result = module(**test_input)

            end_time = time.time()
            latencies.append(end_time - start_time)

            # Could track token usage if LM provides it
            # token_counts.append(result.token_count)

    return {
        "average_latency": sum(latencies) / len(latencies),
        "min_latency": min(latencies),
        "max_latency": max(latencies),
        "p95_latency": sorted(latencies)[int(len(latencies) * 0.95)],
        "total_runs": len(latencies)
    }

# Benchmark example
benchmark_results = benchmark_module(
    qa_module,
    [{"question": "What is machine learning?"}],
    num_runs=10
)

print(f"Average latency: {benchmark_results['average_latency']:.3f}s")
print(f"P95 latency: {benchmark_results['p95_latency']:.3f}s")
```

## Best Practices

### Module Design
- **Single Responsibility**: Each module should do one thing well
- **Clear Interfaces**: Well-defined inputs and outputs
- **Error Handling**: Graceful failure and informative error messages
- **Configurability**: Parameters for different use cases

### Performance Optimization
- **Caching**: Cache expensive operations when possible
- **Batch Processing**: Process multiple inputs together when beneficial
- **Resource Management**: Monitor and limit resource usage
- **Async Support**: Use async patterns for I/O operations

### Testing and Validation
- **Comprehensive Testing**: Test edge cases and failure modes
- **Performance Monitoring**: Track latency and resource usage
- **Output Validation**: Ensure outputs meet quality standards
- **Regression Testing**: Test after changes to prevent regressions

### Maintainability
- **Documentation**: Clear docstrings and usage examples
- **Versioning**: Track module versions and compatibility
- **Modular Updates**: Easy to update individual components
- **Deprecation**: Clear deprecation paths for old interfaces

## Summary

In this chapter, we've covered:

- **Built-in Modules**: Predict, ChainOfThought, ReAct, MultiChainComparison, ProgramOfThought
- **Retrieval Modules**: Retrieve, RetrieveThenRead for RAG systems
- **Custom Modules**: Creating specialized modules for specific tasks
- **RAG Modules**: Basic and advanced retrieval-augmented generation
- **Ensemble Modules**: Voting and weighted ensembles for improved accuracy
- **Composition Patterns**: Pipelines and DAGs for complex workflows
- **Testing**: Unit testing and performance benchmarking
- **Best Practices**: Design, performance, testing, and maintenance

Modules are the building blocks of DSPy programs. By combining built-in modules with custom ones, you can create sophisticated AI systems that are both powerful and maintainable.

## Key Takeaways

1. **Composition over Complexity**: Build complex systems from simple, focused modules
2. **Reuse Built-in Modules**: Leverage DSPy's optimized implementations
3. **Test Thoroughly**: Validate modules work correctly and perform well
4. **Design for Composition**: Create modules that work well together
5. **Monitor Performance**: Track latency, accuracy, and resource usage

Next, we'll explore **Retrieval-Augmented Generation (RAG)** - combining retrieval with generation for more accurate and knowledgeable AI systems.

---

**Ready for the next chapter?** [Chapter 4: Retrieval-Augmented Generation](04-rag.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `dspy`, `self`, `question` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Modules - Reusable DSPy Components` as an operating subsystem inside **DSPy Tutorial: Programming Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `result`, `answer`, `desc` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Modules - Reusable DSPy Components` usually follows a repeatable control path:

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
- [Previous Chapter: Chapter 2: Signatures - Defining LM Input/Output Behavior](02-signatures.md)
- [Next Chapter: Chapter 4: Retrieval-Augmented Generation (RAG) with DSPy](04-rag.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
