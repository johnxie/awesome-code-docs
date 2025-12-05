---
layout: default
title: "DSPy Tutorial - Chapter 7: Evaluation & Metrics"
nav_order: 7
has_children: false
parent: DSPy Tutorial
---

# Chapter 7: Evaluation & Metrics - Systematic Assessment of DSPy Programs

> Learn to evaluate DSPy programs comprehensively using multiple metrics, statistical analysis, and systematic validation approaches.

## Overview

Evaluation is crucial for DSPy programs. Unlike traditional ML where you train once and evaluate, DSPy programs can be continuously improved through optimization. Proper evaluation ensures your programs work correctly and helps guide optimization efforts.

## Basic Evaluation with DSPy

### The Evaluate Class

```python
import dspy

# Configure DSPy
lm = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=lm)

# Create a simple program to evaluate
class BasicQA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

program = dspy.Predict(BasicQA)

# Create test dataset
testset = [
    dspy.Example(question="What is the capital of France?", answer="Paris"),
    dspy.Example(question="What is 2+2?", answer="4"),
    dspy.Example(question="What is the largest planet?", answer="Jupiter"),
]

# Define evaluation metric
def exact_match_metric(example, prediction, trace=None):
    """Exact match evaluation"""
    return prediction.answer.lower().strip() == example.answer.lower().strip()

# Create evaluator
evaluator = dspy.Evaluate(
    devset=testset,              # Test dataset
    metric=exact_match_metric,   # Evaluation function
    num_threads=4,              # Parallel evaluation
    display_progress=True,      # Show progress bar
    display_table=True          # Show results table
)

# Run evaluation
score = evaluator(program)
print(f"Exact Match Score: {score}")
```

### Understanding Evaluation Results

```python
# Detailed evaluation with progress tracking
detailed_evaluator = dspy.Evaluate(
    devset=testset,
    metric=exact_match_metric,
    num_threads=1,  # Sequential for detailed logging
    return_all_scores=True,  # Return individual scores
    return_outputs=True       # Return predictions
)

# Run detailed evaluation
result = detailed_evaluator(program)

print("Evaluation Results:")
print(f"Overall Score: {result['overall_score']}")
print(f"Individual Scores: {result['score_per_example']}")
print(f"Total Examples: {len(result['outputs'])}")

# Analyze failures
failures = [(i, ex, pred) for i, (ex, pred, score) in enumerate(
    zip(testset, result['outputs'], result['score_per_example'])
) if score == 0.0]

print(f"\nFailures ({len(failures)}):")
for i, example, prediction in failures:
    print(f"Example {i}: Q='{example.question}' | Expected='{example.answer}' | Got='{prediction.answer}'")
```

## Advanced Metrics

### Semantic Similarity Metrics

```python
def semantic_similarity_metric(example, prediction, trace=None):
    """Evaluate semantic similarity using embeddings"""
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Simple word overlap (in practice, use embeddings)
    pred_words = set(prediction.answer.lower().split())
    gold_words = set(example.answer.lower().split())

    if not pred_words or not gold_words:
        return 0.0

    intersection = len(pred_words.intersection(gold_words))
    union = len(pred_words.union(gold_words))

    return intersection / union

def embedding_similarity_metric(example, prediction, trace=None):
    """More sophisticated embedding-based similarity"""
    # In practice, you would:
    # 1. Get embeddings for prediction.answer and example.answer
    # 2. Compute cosine similarity
    # 3. Return similarity score

    # Placeholder implementation
    pred_len = len(prediction.answer.split())
    gold_len = len(example.answer.split())

    # Simple length-based similarity (not recommended for real use)
    length_diff = abs(pred_len - gold_len)
    max_length = max(pred_len, gold_len)

    return max(0, 1 - (length_diff / max_length)) if max_length > 0 else 0

# Use semantic metrics
semantic_evaluator = dspy.Evaluate(
    devset=testset,
    metric=semantic_similarity_metric,
    num_threads=4
)

semantic_score = semantic_evaluator(program)
print(f"Semantic Similarity Score: {semantic_score}")
```

### Multi-Dimensional Metrics

```python
def comprehensive_metric(example, prediction, trace=None):
    """Multi-dimensional evaluation"""

    scores = {}

    # Accuracy
    scores['exact_match'] = float(
        prediction.answer.lower().strip() == example.answer.lower().strip()
    )

    # Length appropriateness
    pred_len = len(prediction.answer.split())
    expected_len = len(example.answer.split())
    scores['length_similarity'] = max(0, 1 - abs(pred_len - expected_len) / max(pred_len, expected_len))

    # Contains expected keywords
    gold_words = set(example.answer.lower().split())
    pred_words = set(prediction.answer.lower().split())
    scores['keyword_overlap'] = len(gold_words.intersection(pred_words)) / len(gold_words) if gold_words else 0

    # Informativeness (simple heuristic)
    scores['informativeness'] = min(1.0, pred_len / 10)  # Prefer answers with some detail

    # Combine scores with weights
    final_score = (
        0.4 * scores['exact_match'] +
        0.2 * scores['length_similarity'] +
        0.3 * scores['keyword_overlap'] +
        0.1 * scores['informativeness']
    )

    # Store individual scores for analysis
    prediction._individual_scores = scores

    return final_score

# Evaluate with comprehensive metric
comprehensive_evaluator = dspy.Evaluate(
    devset=testset,
    metric=comprehensive_metric,
    num_threads=1,
    return_outputs=True
)

comp_result = comprehensive_evaluator(program)

# Analyze individual score components
for i, (example, prediction) in enumerate(zip(testset, comp_result['outputs'])):
    if hasattr(prediction, '_individual_scores'):
        scores = prediction._individual_scores
        print(f"Example {i}:")
        print(f"  Question: {example.question}")
        print(f"  Answer: {prediction.answer}")
        print(f"  Scores: EM={scores['exact_match']:.2f}, KW={scores['keyword_overlap']:.2f}, Len={scores['length_similarity']:.2f}")
        print()
```

### Task-Specific Metrics

```python
# Math problem evaluation
def math_accuracy_metric(example, prediction, trace=None):
    """Evaluate mathematical correctness"""
    import re

    # Extract numbers from prediction and gold answer
    pred_nums = re.findall(r'\d+\.?\d*', prediction.answer)
    gold_nums = re.findall(r'\d+\.?\d*', example.answer)

    if not pred_nums or not gold_nums:
        return 0.0

    # Compare final answers (last number in each)
    try:
        pred_final = float(pred_nums[-1])
        gold_final = float(gold_nums[-1])

        # Allow small numerical tolerance
        return 1.0 if abs(pred_final - gold_final) < 0.01 else 0.0
    except (ValueError, IndexError):
        return 0.0

# Code generation evaluation
def code_execution_metric(example, prediction, trace=None):
    """Evaluate code by attempting to execute it"""
    import subprocess
    import tempfile
    import os

    code = prediction.answer

    # Check if it looks like code
    if not any(keyword in code.lower() for keyword in ['def ', 'class ', 'import ', 'print']):
        return 0.0

    # Try to execute the code
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        # Run the code with timeout
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5  # 5 second timeout
        )

        os.unlink(temp_file)

        # Success if no errors
        return 1.0 if result.returncode == 0 else 0.0

    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file)
            except:
                pass
        return 0.0

# Usage examples
math_problems = [
    dspy.Example(question="What is 15 * 7?", answer="105"),
    dspy.Example(question="What is 144 / 12?", answer="12"),
]

math_evaluator = dspy.Evaluate(
    devset=math_problems,
    metric=math_accuracy_metric
)

math_score = math_evaluator(program)
print(f"Math Accuracy: {math_score}")
```

## Statistical Analysis of Results

### Confidence Intervals and Significance Testing

```python
import numpy as np
from scipy import stats

def statistical_analysis(scores, confidence_level=0.95):
    """Perform statistical analysis on evaluation scores"""

    scores_array = np.array(scores)

    analysis = {
        'mean': np.mean(scores_array),
        'std': np.std(scores_array, ddof=1),  # Sample standard deviation
        'median': np.median(scores_array),
        'min': np.min(scores_array),
        'max': np.max(scores_array),
        'q25': np.percentile(scores_array, 25),
        'q75': np.percentile(scores_array, 75),
    }

    # Confidence interval for mean
    if len(scores_array) > 1:
        sem = stats.sem(scores_array)  # Standard error of mean
        ci = stats.t.interval(confidence_level, len(scores_array)-1,
                            loc=analysis['mean'], scale=sem)
        analysis['ci_lower'] = ci[0]
        analysis['ci_upper'] = ci[1]

    # Test for normality (Shapiro-Wilk)
    if len(scores_array) >= 3:
        stat, p_value = stats.shapiro(scores_array)
        analysis['normality_test'] = {
            'statistic': stat,
            'p_value': p_value,
            'is_normal': p_value > 0.05
        }

    return analysis

# Collect multiple evaluation runs
def multiple_evaluation_runs(program, testset, metric, num_runs=5):
    """Run evaluation multiple times for statistical analysis"""

    all_scores = []

    for run in range(num_runs):
        evaluator = dspy.Evaluate(
            devset=testset,
            metric=metric,
            num_threads=4,
            return_all_scores=True
        )

        result = evaluator(program)
        all_scores.extend(result['score_per_example'])

    return all_scores

# Run statistical analysis
scores = multiple_evaluation_runs(program, testset, exact_match_metric, num_runs=3)
stats_analysis = statistical_analysis(scores)

print("Statistical Analysis:")
print(f"Mean Score: {stats_analysis['mean']:.3f} ± {(stats_analysis['ci_upper'] - stats_analysis['ci_lower'])/2:.3f}")
print(f"Median: {stats_analysis['median']:.3f}")
print(f"95% CI: [{stats_analysis['ci_lower']:.3f}, {stats_analysis['ci_upper']:.3f}]")
print(f"Normal distribution: {stats_analysis.get('normality_test', {}).get('is_normal', 'Unknown')}")
```

### A/B Testing for DSPy Programs

```python
def ab_test_programs(program_a, program_b, testset, metric, num_trials=10):
    """A/B test two DSPy programs"""

    results_a = []
    results_b = []

    for trial in range(num_trials):
        # Evaluate both programs
        evaluator_a = dspy.Evaluate(devset=testset, metric=metric, return_all_scores=True)
        evaluator_b = dspy.Evaluate(devset=testset, metric=metric, return_all_scores=True)

        result_a = evaluator_a(program_a)
        result_b = evaluator_b(program_b)

        results_a.append(result_a['overall_score'])
        results_b.append(result_b['overall_score'])

    # Statistical comparison
    t_stat, p_value = stats.ttest_ind(results_a, results_b)

    ab_results = {
        'program_a': {
            'scores': results_a,
            'mean': np.mean(results_a),
            'std': np.std(results_a)
        },
        'program_b': {
            'scores': results_b,
            'mean': np.mean(results_b),
            'std': np.std(results_b)
        },
        'statistical_test': {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'winner': 'A' if np.mean(results_a) > np.mean(results_b) else 'B'
        }
    }

    return ab_results

# Example A/B test
from dspy.teleprompt import BootstrapFewShot

# Program A: Basic
program_a = dspy.Predict(BasicQA)

# Program B: Optimized
optimizer = BootstrapFewShot(metric=exact_match_metric, max_bootstraps=2)
program_b = optimizer.compile(program_a, trainset=testset[:5])

# Run A/B test
ab_results = ab_test_programs(program_a, program_b, testset, exact_match_metric)

print("A/B Test Results:")
print(f"Program A: {ab_results['program_a']['mean']:.3f} ± {ab_results['program_a']['std']:.3f}")
print(f"Program B: {ab_results['program_b']['mean']:.3f} ± {ab_results['program_b']['std']:.3f}")
print(f"Winner: Program {ab_results['statistical_test']['winner']} (p={ab_results['statistical_test']['p_value']:.3f})")
```

## Custom Evaluation Frameworks

### Hierarchical Evaluation

```python
class HierarchicalEvaluator:
    def __init__(self, metrics_by_level):
        self.metrics_by_level = metrics_by_level  # Dict of level -> metric functions

    def evaluate_hierarchical(self, program, testset):
        """Multi-level evaluation"""

        results = {}

        # Level 1: Basic correctness
        level1_metric = self.metrics_by_level.get('basic', exact_match_metric)
        evaluator1 = dspy.Evaluate(devset=testset, metric=level1_metric, return_outputs=True)
        result1 = evaluator1(program)

        results['basic'] = {
            'score': result1['overall_score'],
            'outputs': result1['outputs']
        }

        # Filter examples that passed basic evaluation
        passed_basic = [
            ex for ex, pred, score in zip(testset, result1['outputs'], result1['score_per_example'])
            if score > 0.5  # Threshold for passing basic
        ]

        if passed_basic and 'advanced' in self.metrics_by_level:
            # Level 2: Advanced evaluation on passed examples
            level2_metric = self.metrics_by_level['advanced']
            evaluator2 = dspy.Evaluate(devset=passed_basic, metric=level2_metric)
            result2 = evaluator2(program)

            results['advanced'] = {
                'score': result2,
                'passed_basic_count': len(passed_basic)
            }

        return results

# Define hierarchical metrics
hierarchical_metrics = {
    'basic': exact_match_metric,
    'advanced': comprehensive_metric
}

hierarchical_evaluator = HierarchicalEvaluator(hierarchical_metrics)
hierarchical_results = hierarchical_evaluator.evaluate_hierarchical(program, testset)

print("Hierarchical Evaluation:")
print(f"Basic Score: {hierarchical_results['basic']['score']:.3f}")
if 'advanced' in hierarchical_results:
    print(f"Advanced Score: {hierarchical_results['advanced']['score']:.3f}")
    print(f"Examples passing basic: {hierarchical_results['advanced']['passed_basic_count']}")
```

### Progressive Evaluation

```python
class ProgressiveEvaluator:
    def __init__(self, difficulty_levels):
        self.difficulty_levels = difficulty_levels  # List of (name, filter_func, metric)

    def evaluate_progressive(self, program):
        """Evaluate progressively by difficulty"""

        results = {}

        for level_name, filter_func, metric in self.difficulty_levels:
            # Filter testset for this difficulty level
            filtered_set = [ex for ex in testset if filter_func(ex)]

            if not filtered_set:
                results[level_name] = {'score': None, 'count': 0}
                continue

            # Evaluate on this subset
            evaluator = dspy.Evaluate(devset=filtered_set, metric=metric)
            score = evaluator(program)

            results[level_name] = {
                'score': score,
                'count': len(filtered_set)
            }

        return results

# Define difficulty levels
def is_easy(example):
    return len(example.question.split()) <= 5

def is_medium(example):
    length = len(example.question.split())
    return 5 < length <= 10

def is_hard(example):
    return len(example.question.split()) > 10

progressive_metrics = [
    ('easy', is_easy, exact_match_metric),
    ('medium', is_medium, semantic_similarity_metric),
    ('hard', is_hard, comprehensive_metric)
]

progressive_evaluator = ProgressiveEvaluator(progressive_metrics)
progressive_results = progressive_evaluator.evaluate_progressive(program)

print("Progressive Evaluation:")
for level, result in progressive_results.items():
    if result['score'] is not None:
        print(f"{level.capitalize()}: {result['score']:.3f} ({result['count']} examples)")
    else:
        print(f"{level.capitalize()}: No examples")
```

## Evaluation Best Practices

### Robustness Testing

```python
def robustness_test(program, test_variations):
    """Test program robustness against input variations"""

    robustness_results = {}

    for variation_name, variation_func in test_variations.items():
        # Create modified testset
        modified_testset = []
        for example in testset:
            modified_example = dspy.Example(
                question=variation_func(example.question),
                answer=example.answer
            )
            modified_testset.append(modified_example)

        # Evaluate on modified testset
        evaluator = dspy.Evaluate(devset=modified_testset, metric=exact_match_metric)
        score = evaluator(program)

        robustness_results[variation_name] = score

    return robustness_results

# Define input variations
variations = {
    'original': lambda x: x,
    'uppercase': lambda x: x.upper(),
    'extra_spaces': lambda x: '  '.join(x.split()),
    'typos': lambda x: x.replace('the', 'teh').replace('is', 'si'),  # Simple typos
    'paraphrased': lambda x: f"Can you tell me {x.lower()}?" if not x.startswith("Can you") else x
}

robustness_results = robustness_test(program, variations)

print("Robustness Test Results:")
for variation, score in robustness_results.items():
    print(f"{variation}: {score:.3f}")
```

### Cross-Domain Evaluation

```python
def cross_domain_evaluation(program, domain_datasets):
    """Evaluate program across different domains"""

    domain_results = {}

    for domain_name, domain_testset in domain_datasets.items():
        evaluator = dspy.Evaluate(
            devset=domain_testset,
            metric=exact_match_metric
        )

        score = evaluator(program)
        domain_results[domain_name] = score

    return domain_results

# Define domain-specific datasets
domain_datasets = {
    'general_knowledge': [
        dspy.Example(question="What is the capital of France?", answer="Paris"),
        dspy.Example(question="What is the largest planet?", answer="Jupiter"),
    ],
    'mathematics': [
        dspy.Example(question="What is 2+2?", answer="4"),
        dspy.Example(question="What is 15*7?", answer="105"),
    ],
    'programming': [
        dspy.Example(question="What does 'print' do in Python?", answer="Outputs text to console"),
        dspy.Example(question="What is a variable?", answer="Named storage for data"),
    ]
}

cross_domain_results = cross_domain_evaluation(program, domain_datasets)

print("Cross-Domain Evaluation:")
for domain, score in cross_domain_results.items():
    print(f"{domain}: {score:.3f}")
```

### Automated Evaluation Pipelines

```python
class EvaluationPipeline:
    def __init__(self, program, testsets, metrics):
        self.program = program
        self.testsets = testsets  # Dict of name -> testset
        self.metrics = metrics    # Dict of name -> metric_func

    def run_full_evaluation(self):
        """Run comprehensive evaluation pipeline"""

        results = {}

        for testset_name, testset in self.testsets.items():
            testset_results = {}

            for metric_name, metric_func in self.metrics.items():
                evaluator = dspy.Evaluate(
                    devset=testset,
                    metric=metric_func,
                    num_threads=4,
                    return_all_scores=True
                )

                result = evaluator(self.program)

                testset_results[metric_name] = {
                    'overall_score': result['overall_score'],
                    'individual_scores': result['score_per_example'],
                    'outputs': result['outputs']
                }

            results[testset_name] = testset_results

        return results

    def generate_report(self, results):
        """Generate comprehensive evaluation report"""

        report = "# DSPy Program Evaluation Report\n\n"

        for testset_name, testset_results in results.items():
            report += f"## {testset_name.title()} Test Set\n\n"

            for metric_name, metric_results in testset_results.items():
                score = metric_results['overall_score']
                report += f"### {metric_name.replace('_', ' ').title()}\n"
                report += f"- Score: {score:.3f}\n"
                report += f"- Examples: {len(metric_results['individual_scores'])}\n\n"

        return report

# Create comprehensive evaluation pipeline
pipeline = EvaluationPipeline(
    program=program,
    testsets={
        'general': testset,
        'robustness': testset,  # Could be different robustness tests
    },
    metrics={
        'exact_match': exact_match_metric,
        'semantic_similarity': semantic_similarity_metric,
        'comprehensive': comprehensive_metric
    }
)

# Run full evaluation
evaluation_results = pipeline.run_full_evaluation()

# Generate report
report = pipeline.generate_report(evaluation_results)
print(report)
```

## Summary

In this chapter, we've explored:

- **Basic Evaluation**: Using DSPy's Evaluate class with simple metrics
- **Advanced Metrics**: Semantic similarity, multi-dimensional, and task-specific evaluation
- **Statistical Analysis**: Confidence intervals, significance testing, and A/B testing
- **Custom Frameworks**: Hierarchical, progressive, and automated evaluation
- **Best Practices**: Robustness testing, cross-domain evaluation, and comprehensive reporting

Proper evaluation is essential for developing reliable DSPy programs and guiding optimization efforts.

## Key Takeaways

1. **Multi-Metric Evaluation**: Use multiple metrics for comprehensive assessment
2. **Statistical Rigor**: Apply statistical analysis for reliable results
3. **Progressive Testing**: Evaluate across difficulty levels and domains
4. **Automated Pipelines**: Build systematic evaluation workflows
5. **Continuous Monitoring**: Regularly evaluate as programs evolve

Next, we'll explore **production deployment** - scaling DSPy systems for real-world applications.

---

**Ready for the next chapter?** [Chapter 8: Production Deployment](08-production.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*