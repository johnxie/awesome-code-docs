---
layout: default
title: "DSPy Tutorial - Chapter 5: Automatic Optimization"
nav_order: 5
has_children: false
parent: DSPy Tutorial
---

# Chapter 5: Automatic Optimization - DSPy's Superpower

> Discover how DSPy automatically optimizes your programs through systematic prompt engineering and model selection.

## Overview

The true power of DSPy lies in its optimization capabilities. Unlike traditional prompt engineering (trial and error), DSPy uses systematic algorithms to automatically improve your programs by optimizing prompts, selecting better model configurations, and fine-tuning components.

## The Optimization Process

### Before vs After Optimization

```python
import dspy

# Configure DSPy
lm = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=lm)

# Define a simple program
class BasicQA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

program = dspy.Predict(BasicQA)

# BEFORE optimization: Manual approach
print("=== BEFORE OPTIMIZATION ===")
result1 = program(question="What is the capital of France?")
print(f"Answer: {result1.answer}")

# AFTER optimization: DSPy automatically improves it
print("\n=== AFTER OPTIMIZATION ===")
# We'll see how to do this below
```

### Optimization Components

DSPy optimizes three main aspects:

1. **Prompts**: Automatically improves instructions and examples
2. **Model Selection**: Chooses the best model for each task
3. **Hyperparameters**: Optimizes parameters like temperature, examples count, etc.

## Teleprompters - DSPy's Optimizers

### BootstrapFewShot - Learning from Examples

```python
from dspy.teleprompt import BootstrapFewShot

# Create a simple dataset
trainset = [
    dspy.Example(question="What is Python?", answer="Python is a programming language"),
    dspy.Example(question="What is AI?", answer="AI stands for Artificial Intelligence"),
    dspy.Example(question="What is machine learning?", answer="Machine learning is a subset of AI"),
    # ... more examples
]

# Define metric for optimization
def qa_metric(example, prediction, trace=None):
    """Evaluate answer quality"""
    # Simple exact match
    return prediction.answer.lower().strip() == example.answer.lower().strip()

# Alternative: Semantic similarity
def semantic_metric(example, prediction, trace=None):
    """More sophisticated evaluation"""
    pred_words = set(prediction.answer.lower().split())
    gold_words = set(example.answer.lower().split())

    # Jaccard similarity
    intersection = len(pred_words.intersection(gold_words))
    union = len(pred_words.union(gold_words))

    return intersection / union if union > 0 else 0

# Create optimizer
teleprompter = BootstrapFewShot(
    metric=semantic_metric,      # How to evaluate quality
    max_bootstraps=3,           # How many optimization rounds
    max_labeled_demos=4         # Max examples to include in prompt
)

# Optimize the program
optimized_program = teleprompter.compile(
    student=program,            # Program to optimize
    trainset=trainset           # Training examples
)

print("Optimization complete!")
print(f"Original program: {program}")
print(f"Optimized program: {optimized_program}")
```

### Understanding BootstrapFewShot

```python
# The optimization process:
# 1. Take your program (student)
# 2. Run it on training examples
# 3. Identify failures (according to metric)
# 4. Generate better examples/prompts from successful runs
# 5. Update the program with improved prompts
# 6. Repeat until convergence or max_bootstraps reached

# Example of what DSPy learns:
print("\n=== WHAT DSPY OPTIMIZES ===")

# Before: Basic prompt
basic_result = program(question="What is the largest planet?")
print(f"Basic: {basic_result.answer}")

# After: Optimized with examples and better instructions
optimized_result = optimized_program(question="What is the largest planet?")
print(f"Optimized: {optimized_result.answer}")
```

### MIPROv2 - Multi-Instruction Prompt Optimization

```python
from dspy.teleprompt import MIPROv2

# MIPROv2 optimizes both instructions and demonstrations
mipro_optimizer = MIPROv2(
    metric=semantic_metric,
    num_candidates=10,          # Try 10 different prompt variations
    init_temperature=1.0,       # Exploration vs exploitation
    verbose=True,               # Show optimization progress
    num_threads=4               # Parallel optimization
)

# Optimize with MIPROv2
mipro_optimized = mipro_optimizer.compile(
    student=program,
    trainset=trainset[:5],      # Smaller dataset for MIPRO
    valset=trainset[5:8],       # Validation set
    max_bootstraps=2
)

print(f"MIPRO optimization complete!")
print(f"Optimized instructions: {mipro_optimized.signature.instructions}")
```

### Ensemble Optimization

```python
from dspy.teleprompt import Ensemble

# Create multiple optimized versions
ensemble_optimizer = Ensemble(
    reduction="mean",           # How to combine predictions
    num_candidates=5
)

# Generate ensemble of optimized programs
ensemble_program = ensemble_optimizer.compile(
    student=program,
    trainset=trainset,
    metric=semantic_metric
)

# Ensemble makes multiple predictions and combines them
result = ensemble_program(question="What is deep learning?")
print(f"Ensemble prediction: {result.answer}")
print(f"Individual predictions: {result.predictions}")  # If available
```

## Optimizing Complex Programs

### Optimizing RAG Systems

```python
# Define a RAG program to optimize
class RAGProgram(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.num_passages = num_passages
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.Predict(RAGSignature)

    def forward(self, question):
        passages = self.retrieve(question)
        answer = self.generate(question=question, context=passages.passages)
        return answer

# DSPy can optimize the number of passages
class OptimizableRAG(dspy.Module):
    def __init__(self):
        super().__init__()
        # DSPy will optimize this parameter
        self.num_passages = dspy.Suggest(candidates=[1, 3, 5, 7])
        self.retrieve = dspy.Retrieve(k=self.num_passages)
        self.generate = dspy.Predict(RAGSignature)

    def forward(self, question):
        passages = self.retrieve(question)
        answer = self.generate(question=question, context=passages.passages)
        return answer

# Optimize RAG
rag_optimizer = BootstrapFewShot(
    metric=rag_metric,
    max_bootstraps=3
)

optimized_rag = rag_optimizer.compile(
    student=OptimizableRAG(),
    trainset=rag_trainset
)

print(f"Optimized to use {optimized_rag.num_passages} passages")
```

### Optimizing Signatures

```python
# DSPy can optimize signature descriptions and field definitions
class OptimizableSignature(dspy.Signature):
    """DSPy will optimize these descriptions"""

    question = dspy.InputField(desc=dspy.Suggest([
        "the question to answer",
        "user's query that needs answering",
        "question requiring a factual answer"
    ]))

    context = dspy.InputField(
        desc=dspy.Suggest([
            "relevant background information",
            "supporting facts and context",
            "additional information for answering"
        ]),
        required=dspy.Suggest([True, False])
    )

    answer = dspy.OutputField(desc=dspy.Suggest([
        "accurate answer based on facts",
        "concise and correct response",
        "answer supported by context"
    ]))

# Optimize the signature itself
signature_optimizer = MIPROv2(metric=qa_metric, num_candidates=5)

optimized_signature_program = signature_optimizer.compile(
    student=dspy.Predict(OptimizableSignature),
    trainset=trainset
)
```

## Advanced Optimization Techniques

### Multi-Metric Optimization

```python
def comprehensive_metric(example, prediction, trace=None):
    """Multi-dimensional evaluation"""

    scores = {}

    # Accuracy
    scores['accuracy'] = float(
        prediction.answer.lower().strip() == example.answer.lower().strip()
    )

    # Length appropriateness (prefer concise answers)
    answer_length = len(prediction.answer.split())
    scores['conciseness'] = 1.0 if 1 <= answer_length <= 10 else 0.5

    # Factual correctness (placeholder - would use fact-checking)
    scores['factual'] = 0.9  # Placeholder

    # Combine scores with weights
    final_score = (
        0.5 * scores['accuracy'] +
        0.3 * scores['conciseness'] +
        0.2 * scores['factual']
    )

    return final_score

# Use comprehensive metric
comprehensive_optimizer = BootstrapFewShot(
    metric=comprehensive_metric,
    max_bootstraps=5
)

comprehensively_optimized = comprehensive_optimizer.compile(
    student=program,
    trainset=trainset
)
```

### Cross-Validation Optimization

```python
from sklearn.model_selection import KFold

def cross_validate_optimization(trainset, folds=3):
    """Cross-validation for optimization stability"""

    kf = KFold(n_splits=folds, shuffle=True, random_state=42)
    fold_scores = []

    for fold, (train_idx, val_idx) in enumerate(kf.split(trainset)):
        fold_train = [trainset[i] for i in train_idx]
        fold_val = [trainset[i] for i in val_idx]

        # Optimize on this fold
        optimizer = BootstrapFewShot(metric=qa_metric, max_bootstraps=2)
        optimized_program = optimizer.compile(
            student=dspy.Predict(BasicQA),
            trainset=fold_train
        )

        # Evaluate on validation fold
        evaluator = dspy.Evaluate(
            devset=fold_val,
            metric=qa_metric,
            num_threads=1
        )

        score = evaluator(optimized_program)
        fold_scores.append(score)

        print(f"Fold {fold + 1} score: {score}")

    # Average score across folds
    avg_score = sum(fold_scores) / len(fold_scores)
    print(f"Cross-validation average: {avg_score}")

    return avg_score

# Run cross-validation
cv_score = cross_validate_optimization(trainset)
```

### Iterative Optimization

```python
class IterativeOptimizer:
    def __init__(self, base_optimizer, max_iterations=3):
        self.base_optimizer = base_optimizer
        self.max_iterations = max_iterations

    def compile(self, student, trainset, valset=None):
        """Iteratively optimize, using validation to guide improvements"""

        current_program = student
        best_score = 0
        best_program = student

        for iteration in range(self.max_iterations):
            print(f"\n=== Iteration {iteration + 1} ===")

            # Optimize current program
            optimized = self.base_optimizer.compile(
                student=current_program,
                trainset=trainset
            )

            # Evaluate
            evaluator = dspy.Evaluate(
                devset=valset or trainset,
                metric=qa_metric,
                num_threads=4
            )

            score = evaluator(optimized)
            print(f"Iteration {iteration + 1} score: {score}")

            # Keep best version
            if score > best_score:
                best_score = score
                best_program = optimized
                current_program = optimized
            else:
                # If no improvement, try different approach
                print("No improvement, trying different optimization strategy...")
                # Could change metric, add more examples, etc.

        return best_program

# Use iterative optimization
iterative_opt = IterativeOptimizer(
    base_optimizer=BootstrapFewShot(metric=qa_metric, max_bootstraps=2),
    max_iterations=3
)

best_program = iterative_opt.compile(
    student=program,
    trainset=trainset,
    valset=valset
)

print(f"Best score achieved: {best_score}")
```

## Optimization Evaluation and Validation

### Comparing Optimization Methods

```python
def compare_optimizers(trainset, valset, testset):
    """Compare different optimization approaches"""

    optimizers = {
        "baseline": lambda: program,  # No optimization

        "few_shot": lambda: BootstrapFewShot(
            metric=qa_metric, max_bootstraps=3
        ).compile(program, trainset),

        "mipro": lambda: MIPROv2(
            metric=qa_metric, num_candidates=5
        ).compile(program, trainset, valset),

        "ensemble": lambda: Ensemble(
            num_candidates=3
        ).compile(program, trainset, metric=qa_metric)
    }

    results = {}

    for name, optimizer_func in optimizers.items():
        print(f"\n=== Testing {name} ===")

        try:
            # Get optimized program
            optimized = optimizer_func()

            # Evaluate on test set
            evaluator = dspy.Evaluate(
                devset=testset,
                metric=qa_metric,
                num_threads=4
            )

            score = evaluator(optimized)
            results[name] = score

            print(f"{name} score: {score}")

        except Exception as e:
            print(f"{name} failed: {e}")
            results[name] = 0.0

    # Print comparison
    print("\n=== OPTIMIZATION COMPARISON ===")
    for name, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print("10")

    return results

# Compare optimization methods
comparison_results = compare_optimizers(trainset, valset, testset)
```

### Optimization Stability Analysis

```python
def analyze_optimization_stability(trainset, num_runs=5):
    """Test if optimization produces consistent results"""

    scores = []

    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs}")

        # Same optimization, different random seed
        optimizer = BootstrapFewShot(
            metric=qa_metric,
            max_bootstraps=3
            # random seed would be set here if available
        )

        optimized = optimizer.compile(student=program, trainset=trainset)

        # Evaluate
        evaluator = dspy.Evaluate(devset=valset, metric=qa_metric)
        score = evaluator(optimized)
        scores.append(score)

        print(f"Score: {score}")

    # Analyze stability
    mean_score = sum(scores) / len(scores)
    variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
    std_dev = variance ** 0.5

    print("
Stability Analysis:")
    print(f"Mean score: {mean_score:.3f}")
    print(f"Standard deviation: {std_dev:.3f}")
    print(f"Coefficient of variation: {std_dev/mean_score:.3f}")

    return {
        "mean": mean_score,
        "std": std_dev,
        "scores": scores
    }

# Analyze stability
stability_results = analyze_optimization_stability(trainset, num_runs=3)
```

## Production Optimization Considerations

### Incremental Optimization

```python
class IncrementalOptimizer:
    def __init__(self, base_optimizer):
        self.base_optimizer = base_optimizer
        self.optimization_history = []

    def compile(self, student, trainset, batch_size=10):
        """Optimize incrementally with growing dataset"""

        optimized_program = student
        available_data = trainset[:batch_size]

        while len(available_data) <= len(trainset):
            print(f"Optimizing with {len(available_data)} examples...")

            # Optimize with current data
            optimized_program = self.base_optimizer.compile(
                student=optimized_program,
                trainset=available_data
            )

            # Evaluate current performance
            evaluator = dspy.Evaluate(devset=trainset, metric=qa_metric)
            score = evaluator(optimized_program)

            self.optimization_history.append({
                "examples_used": len(available_data),
                "score": score,
                "program": optimized_program
            })

            # Add more data for next iteration
            available_data = trainset[:len(available_data) + batch_size]

        # Return best performing version
        best_result = max(self.optimization_history, key=lambda x: x["score"])
        return best_result["program"]

# Incremental optimization
incremental_opt = IncrementalOptimizer(
    base_optimizer=BootstrapFewShot(metric=qa_metric, max_bootstraps=2)
)

incrementally_optimized = incremental_opt.compile(
    student=program,
    trainset=trainset,
    batch_size=5
)
```

### A/B Testing Optimized Programs

```python
class ABTester:
    def __init__(self, programs, metric):
        self.programs = programs  # Dict of name -> program
        self.metric = metric
        self.results = {name: [] for name in programs}

    def test_example(self, example):
        """Test all programs on one example"""

        results = {}
        for name, program in self.programs.items():
            prediction = program(**example.__dict__)
            score = self.metric(example, prediction)
            results[name] = {"prediction": prediction, "score": score}
            self.results[name].append(score)

        return results

    def run_test(self, testset):
        """Run A/B test on dataset"""

        all_results = []

        for example in testset:
            result = self.test_example(example)
            all_results.append(result)

        # Calculate statistics
        stats = {}
        for name in self.programs:
            scores = self.results[name]
            stats[name] = {
                "mean_score": sum(scores) / len(scores),
                "total_examples": len(scores),
                "wins": sum(1 for result in all_results
                           if result[name]["score"] == max(r[p]["score"] for p in self.programs))
            }

        return stats

# A/B test different optimization approaches
ab_tester = ABTester({
    "baseline": program,
    "optimized_v1": optimized_program,
    "optimized_v2": mipro_optimized
}, metric=qa_metric)

ab_results = ab_tester.run_test(testset)

print("A/B Test Results:")
for name, stats in ab_results.items():
    print(f"{name}: {stats['mean_score']:.3f} (wins: {stats['wins']})")
```

## Summary

In this chapter, we've explored:

- **Teleprompters**: BootstrapFewShot, MIPROv2, Ensemble optimization
- **Complex Program Optimization**: RAG systems, signatures, multi-metric evaluation
- **Advanced Techniques**: Cross-validation, iterative optimization, stability analysis
- **Production Considerations**: Incremental optimization, A/B testing
- **Evaluation**: Comparing optimizers, measuring stability

DSPy's optimization capabilities transform manual prompt engineering into systematic, data-driven improvement of AI systems.

## Key Takeaways

1. **Automatic Improvement**: DSPy optimizes prompts and configurations automatically
2. **Multiple Optimizers**: Different teleprompters for different optimization needs
3. **Comprehensive Evaluation**: Use multiple metrics for thorough assessment
4. **Stability Matters**: Test optimization consistency across runs
5. **Production Ready**: Incremental optimization and A/B testing for deployment

Next, we'll explore **advanced patterns** - multi-hop reasoning, tool integration, and complex workflows.

---

**Ready for the next chapter?** [Chapter 6: Advanced Patterns](06-advanced-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*