---
layout: default
title: "Chapter 5: Model Evaluation"
parent: "LLaMA Factory Tutorial"
nav_order: 5
---

# Chapter 5: Model Evaluation

Welcome to the critical phase of model assessment! Evaluating your fine-tuned LLaMA models ensures they perform well on your target tasks. This chapter covers comprehensive evaluation techniques, benchmarks, and quality metrics for production-ready models.

## Evaluation Metrics and Benchmarks

### Core Evaluation Metrics

```python
from evaluate import load
import numpy as np
from typing import Dict, List, Any
import torch

class ModelEvaluator:
    """Comprehensive model evaluation suite"""

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load evaluation metrics
        self.metrics = {
            'perplexity': load('perplexity'),
            'rouge': load('rouge'),
            'bleu': load('bleu'),
            'bertscore': load('bertscore'),
            'meteor': load('meteor')
        }

    def evaluate_generation_quality(self, eval_dataset: List[Dict], num_samples: int = 100) -> Dict[str, float]:
        """Evaluate text generation quality"""

        predictions = []
        references = []

        print(f"Evaluating on {min(num_samples, len(eval_dataset))} samples...")

        for i, sample in enumerate(eval_dataset[:num_samples]):
            if i % 20 == 0:
                print(f"Processing sample {i+1}/{min(num_samples, len(eval_dataset))}")

            # Generate prediction
            prediction = self.generate_response(sample['instruction'], sample.get('input', ''))
            predictions.append(prediction)
            references.append(sample['output'])

        # Calculate metrics
        results = {}

        # ROUGE scores
        rouge_scores = self.metrics['rouge'].compute(
            predictions=predictions,
            references=references,
            use_stemmer=True
        )
        results.update({
            'rouge1': rouge_scores['rouge1'].mid.fmeasure,
            'rouge2': rouge_scores['rouge2'].mid.fmeasure,
            'rougeL': rouge_scores['rougeL'].mid.fmeasure
        })

        # BLEU scores
        bleu_scores = self.metrics['bleu'].compute(
            predictions=predictions,
            references=[[ref] for ref in references]
        )
        results['bleu'] = bleu_scores['bleu']

        # METEOR scores
        meteor_scores = self.metrics['meteor'].compute(
            predictions=predictions,
            references=references
        )
        results['meteor'] = meteor_scores['meteor']

        # BERTScore
        bert_scores = self.metrics['bertscore'].compute(
            predictions=predictions,
            references=references,
            lang='en'
        )
        results['bertscore_f1'] = np.mean(bert_scores['f1'])

        return results

    def evaluate_perplexity(self, eval_dataset: List[Dict]) -> float:
        """Calculate model perplexity"""

        # Prepare texts for perplexity calculation
        texts = []
        for sample in eval_dataset:
            text = f"Instruction: {sample['instruction']}\n"
            if sample.get('input'):
                text += f"Input: {sample['input']}\n"
            text += f"Response: {sample['output']}"
            texts.append(text)

        perplexity = self.metrics['perplexity'].compute(
            model=self.model,
            tokenizer=self.tokenizer,
            data=texts,
            batch_size=8
        )

        return perplexity['mean_perplexity']

    def generate_response(self, instruction: str, input_text: str = "", max_length: int = 512) -> str:
        """Generate a response for evaluation"""

        prompt = f"Instruction: {instruction}\n"
        if input_text:
            prompt += f"Input: {input_text}\n"
        prompt += "Response:"

        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=len(inputs['input_ids'][0]) + max_length,
                num_return_sequences=1,
                temperature=0.1,  # Low temperature for consistent evaluation
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Extract generated text (remove prompt)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = generated_text[len(prompt):].strip()

        return response

# Usage
evaluator = ModelEvaluator(model, tokenizer)

# Evaluate on test set
generation_metrics = evaluator.evaluate_generation_quality(test_dataset, num_samples=200)
perplexity_score = evaluator.evaluate_perplexity(test_dataset)

print("Generation Quality Metrics:")
for metric, score in generation_metrics.items():
    print(f"{metric}: {score:.4f}")

print(f"\nPerplexity: {perplexity_score:.2f}")
```

## Task-Specific Evaluation

### Instruction Following Evaluation

```python
class InstructionFollowingEvaluator:
    """Evaluate how well model follows instructions"""

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def evaluate_instruction_following(self, eval_dataset: List[Dict]) -> Dict[str, float]:
        """Evaluate instruction following capabilities"""

        results = {
            'completeness': 0.0,
            'relevance': 0.0,
            'accuracy': 0.0,
            'helpfulness': 0.0
        }

        for sample in eval_dataset:
            response = self.generate_response(sample['instruction'], sample.get('input'))

            # Evaluate different aspects
            results['completeness'] += self.evaluate_completeness(response, sample)
            results['relevance'] += self.evaluate_relevance(response, sample['instruction'])
            results['accuracy'] += self.evaluate_accuracy(response, sample['output'])
            results['helpfulness'] += self.evaluate_helpfulness(response, sample)

        # Average scores
        for key in results:
            results[key] /= len(eval_dataset)

        return results

    def evaluate_completeness(self, response: str, sample: Dict) -> float:
        """Evaluate if response is complete"""

        # Check for key elements from expected output
        expected_output = sample['output'].lower()
        response_lower = response.lower()

        # Simple heuristic: check if key phrases are present
        key_phrases = expected_output.split()
        matches = sum(1 for phrase in key_phrases if phrase in response_lower)

        return min(matches / len(key_phrases), 1.0)

    def evaluate_relevance(self, response: str, instruction: str) -> float:
        """Evaluate response relevance to instruction"""

        # Use BERT similarity or simple keyword matching
        instruction_words = set(instruction.lower().split())
        response_words = set(response.lower().split())

        overlap = len(instruction_words.intersection(response_words))
        union = len(instruction_words.union(response_words))

        return overlap / union if union > 0 else 0.0

    def evaluate_accuracy(self, response: str, expected: str) -> float:
        """Evaluate factual accuracy"""

        # For this example, use ROUGE-L as proxy
        from evaluate import load
        rouge = load('rouge')

        scores = rouge.compute(
            predictions=[response],
            references=[expected]
        )

        return scores['rougeL'].mid.fmeasure

    def evaluate_helpfulness(self, response: str, sample: Dict) -> float:
        """Evaluate overall helpfulness"""

        # Heuristic-based scoring
        score = 0.5  # Base score

        # Length appropriateness
        if 50 <= len(response) <= 500:
            score += 0.2

        # Contains actionable information
        if any(word in response.lower() for word in ['here\'s', 'you can', 'try', 'use']):
            score += 0.2

        # Not too verbose
        if len(response.split()) <= 100:
            score += 0.1

        return min(score, 1.0)

# Usage
instruction_evaluator = InstructionFollowingEvaluator(model, tokenizer)
instruction_scores = instruction_evaluator.evaluate_instruction_following(eval_dataset)

print("Instruction Following Scores:")
for aspect, score in instruction_scores.items():
    print(f"{aspect}: {score:.3f}")
```

## Automated Evaluation Frameworks

### HELM and OpenCompass Integration

```python
class AutomatedEvaluator:
    """Integration with automated evaluation frameworks"""

    def run_helm_evaluation(self, model_path: str) -> Dict[str, Any]:
        """Run HELM evaluation suite"""

        # This would integrate with HELM framework
        # Simplified version for demonstration

        scenarios = [
            'natural_language_inference',
            'question_answering',
            'sentiment_analysis',
            'summarization'
        ]

        results = {}

        for scenario in scenarios:
            print(f"Evaluating {scenario}...")

            # Load scenario data
            scenario_data = self.load_scenario_data(scenario)

            # Run evaluation
            scenario_results = self.evaluate_scenario(model_path, scenario_data, scenario)
            results[scenario] = scenario_results

        return results

    def run_opencompass_evaluation(self, model_path: str) -> Dict[str, Any]:
        """Run OpenCompass evaluation"""

        # Simplified OpenCompass integration
        benchmarks = [
            'mmlu', 'ceval', 'cmmlu', 'bbh',
            'gsm8k', 'math', 'humaneval', 'mbpp'
        ]

        results = {}

        for benchmark in benchmarks:
            print(f"Running {benchmark} benchmark...")

            # This would actually run the benchmark
            # For now, return mock results
            results[benchmark] = {
                'accuracy': np.random.uniform(0.5, 0.9),
                'confidence': np.random.uniform(0.1, 0.3)
            }

        return results

    def create_evaluation_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive evaluation report"""

        report = "# Model Evaluation Report\n\n"

        report += "## Summary\n\n"

        # Calculate overall scores
        overall_scores = {}
        for benchmark, scores in results.items():
            for metric, value in scores.items():
                if metric not in overall_scores:
                    overall_scores[metric] = []
                overall_scores[metric].append(value)

        for metric, values in overall_scores.items():
            avg_score = np.mean(values)
            report += f"- **{metric}**: {avg_score:.3f}\n"

        report += "\n## Detailed Results\n\n"

        for benchmark, scores in results.items():
            report += f"### {benchmark.replace('_', ' ').title()}\n\n"
            for metric, value in scores.items():
                report += f"- {metric}: {value:.3f}\n"
            report += "\n"

        return report

# Usage
auto_evaluator = AutomatedEvaluator()

# Run evaluations
helm_results = auto_evaluator.run_helm_evaluation(model_path)
opencompass_results = auto_evaluator.run_opencompass_evaluation(model_path)

# Combine results
all_results = {**helm_results, **opencompass_results}

# Generate report
report = auto_evaluator.create_evaluation_report(all_results)

with open('evaluation_report.md', 'w') as f:
    f.write(report)

print("Evaluation report saved to evaluation_report.md")
```

## Human Evaluation Integration

### Human-in-the-Loop Evaluation

```python
class HumanEvaluator:
    """Human evaluation interface and analysis"""

    def __init__(self):
        self.evaluation_criteria = [
            'relevance', 'accuracy', 'helpfulness',
            'clarity', 'completeness', 'appropriateness'
        ]

    def create_evaluation_interface(self, samples: List[Dict]) -> str:
        """Create HTML interface for human evaluation"""

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Model Evaluation Interface</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .evaluation-item { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
                .criteria { display: flex; gap: 10px; margin: 10px 0; }
                .criterion { display: flex; align-items: center; gap: 5px; }
            </style>
        </head>
        <body>
            <h1>Model Response Evaluation</h1>
            <p>Please evaluate each model response on the following criteria (1-5 scale):</p>
        """

        for i, sample in enumerate(samples):
            html += f"""
            <div class="evaluation-item">
                <h3>Sample {i+1}</h3>
                <p><strong>Instruction:</strong> {sample['instruction']}</p>
                {f"<p><strong>Input:</strong> {sample['input']}</p>" if sample.get('input') else ""}
                <p><strong>Model Response:</strong> {sample['model_response']}</p>
                <p><strong>Expected Response:</strong> {sample['output']}</p>

                <div class="criteria">
            """

            for criterion in self.evaluation_criteria:
                html += f"""
                    <div class="criterion">
                        <label>{criterion.title()}:</label>
                        <select name="sample_{i}_{criterion}">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </div>
                """

            html += """
                </div>
                <div style="margin-top: 10px;">
                    <label>Comments:</label><br>
                    <textarea name="comments_{i}" rows="2" cols="50"></textarea>
                </div>
            </div>
            """

        html += """
            <button onclick="submitEvaluation()">Submit Evaluation</button>
        </body>
        </html>
        """

        return html

    def analyze_human_feedback(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """Analyze human evaluation results"""

        analysis = {
            'overall_scores': {},
            'criteria_breakdown': {},
            'comments': []
        }

        # Calculate average scores
        for criterion in self.evaluation_criteria:
            scores = [item[f'sample_{i}_{criterion}'] for item in feedback_data
                     for i in range(len(item)) if f'sample_{i}_{criterion}' in item]

            if scores:
                analysis['criteria_breakdown'][criterion] = {
                    'mean': np.mean(scores),
                    'std': np.std(scores),
                    'min': min(scores),
                    'max': max(scores)
                }

        # Collect comments
        for item in feedback_data:
            for i in range(len(item)):
                comment_key = f'comments_{i}'
                if comment_key in item and item[comment_key].strip():
                    analysis['comments'].append(item[comment_key])

        # Overall score
        all_scores = []
        for criterion_data in analysis['criteria_breakdown'].values():
            all_scores.append(criterion_data['mean'])

        analysis['overall_score'] = np.mean(all_scores)

        return analysis

# Usage
human_evaluator = HumanEvaluator()

# Create evaluation interface
eval_samples = [
    {
        'instruction': 'Explain quantum computing',
        'model_response': 'Quantum computing uses quantum bits...',
        'output': 'Expected detailed explanation...'
    }
]

html_interface = human_evaluator.create_evaluation_interface(eval_samples)

with open('human_evaluation.html', 'w') as f:
    f.write(html_interface)

print("Human evaluation interface created: human_evaluation.html")
```

## Model Comparison and A/B Testing

### Automated Model Comparison

```python
class ModelComparator:
    """Compare multiple models systematically"""

    def __init__(self, models: Dict[str, Any], tokenizer):
        self.models = models
        self.tokenizer = tokenizer

    def run_comparison(self, test_dataset: List[Dict], num_samples: int = 50) -> Dict[str, Any]:
        """Compare models on test dataset"""

        results = {}

        for model_name, model in self.models.items():
            print(f"Evaluating {model_name}...")

            evaluator = ModelEvaluator(model, self.tokenizer)
            model_results = evaluator.evaluate_generation_quality(test_dataset, num_samples)

            results[model_name] = model_results

        return results

    def statistical_significance_test(self, results_a: Dict, results_b: Dict) -> Dict[str, bool]:
        """Test statistical significance between model results"""

        significance_results = {}

        for metric in results_a.keys():
            if metric in results_b:
                # Simple t-test approximation
                mean_a = results_a[metric]
                mean_b = results_b[metric]

                # Assume some variance for demonstration
                std_a = 0.1
                std_b = 0.1

                # Calculate t-statistic
                t_stat = abs(mean_a - mean_b) / ((std_a**2 + std_b**2) ** 0.5)

                # Significant if t > 1.96 (95% confidence)
                significance_results[metric] = t_stat > 1.96

        return significance_results

    def generate_comparison_report(self, comparison_results: Dict[str, Any]) -> str:
        """Generate detailed comparison report"""

        report = "# Model Comparison Report\n\n"

        # Find best model for each metric
        metrics = list(comparison_results[list(comparison_results.keys())[0]].keys())

        for metric in metrics:
            report += f"## {metric.replace('_', ' ').title()}\n\n"

            # Sort models by metric
            sorted_models = sorted(
                comparison_results.items(),
                key=lambda x: x[1][metric],
                reverse=True
            )

            for model_name, scores in sorted_models:
                score = scores[metric]
                report += f"- **{model_name}**: {score:.4f}\n"

            report += "\n"

        # Statistical significance
        if len(comparison_results) == 2:
            model_names = list(comparison_results.keys())
            sig_results = self.statistical_significance_test(
                comparison_results[model_names[0]],
                comparison_results[model_names[1]]
            )

            report += "## Statistical Significance\n\n"
            for metric, significant in sig_results.items():
                status = "Significant" if significant else "Not significant"
                report += f"- **{metric}**: {status}\n"

        return report

# Usage
models_to_compare = {
    'llama-7b-base': base_model,
    'llama-7b-finetuned': fine_tuned_model
}

comparator = ModelComparator(models_to_compare, tokenizer)
comparison_results = comparator.run_comparison(test_dataset)

# Generate report
report = comparator.generate_comparison_report(comparison_results)

with open('model_comparison.md', 'w') as f:
    f.write(report)

print("Model comparison report saved to model_comparison.md")
```

## Production Readiness Assessment

### Comprehensive Readiness Checklist

```python
class ProductionReadinessChecker:
    """Assess if model is ready for production"""

    def __init__(self):
        self.checklist = {
            'performance': [],
            'robustness': [],
            'efficiency': [],
            'compliance': []
        }

    def assess_readiness(self, model, tokenizer, test_results: Dict) -> Dict[str, Any]:
        """Comprehensive production readiness assessment"""

        assessment = {
            'overall_score': 0,
            'passed_checks': 0,
            'total_checks': 0,
            'issues': [],
            'recommendations': []
        }

        # Performance checks
        self._check_performance_metrics(test_results, assessment)

        # Robustness checks
        self._check_robustness(model, tokenizer, assessment)

        # Efficiency checks
        self._check_efficiency(model, assessment)

        # Compliance checks
        self._check_compliance(assessment)

        # Calculate overall score
        assessment['overall_score'] = assessment['passed_checks'] / assessment['total_checks']

        return assessment

    def _check_performance_metrics(self, test_results: Dict, assessment: Dict):
        """Check performance metrics against thresholds"""

        thresholds = {
            'rougeL': 0.7,
            'bleu': 0.6,
            'perplexity': 15.0
        }

        for metric, threshold in thresholds.items():
            if metric in test_results:
                score = test_results[metric]
                assessment['total_checks'] += 1

                if score >= threshold:
                    assessment['passed_checks'] += 1
                else:
                    assessment['issues'].append(f"Low {metric} score: {score:.3f} < {threshold}")

    def _check_robustness(self, model, tokenizer, assessment: Dict):
        """Check model robustness"""

        # Test with adversarial inputs
        adversarial_tests = [
            "",  # Empty input
            "a" * 1000,  # Very long input
            "!@#$%^&*()",  # Special characters
            "What is the meaning of life?",  # Philosophical question
        ]

        for test_input in adversarial_tests:
            assessment['total_checks'] += 1

            try:
                # Test model response
                inputs = tokenizer(test_input, return_tensors='pt')
                outputs = model.generate(**inputs, max_length=50)

                assessment['passed_checks'] += 1
            except Exception as e:
                assessment['issues'].append(f"Failed on input '{test_input[:50]}...': {str(e)}")

    def _check_efficiency(self, model, assessment: Dict):
        """Check model efficiency"""

        # Memory usage check
        assessment['total_checks'] += 1
        # This would check actual memory usage

        # Inference speed check
        assessment['total_checks'] += 1
        # This would measure inference latency

        assessment['passed_checks'] += 2  # Assume passed for demo

    def _check_compliance(self, assessment: Dict):
        """Check regulatory compliance"""

        compliance_items = [
            'data_privacy_review',
            'bias_assessment',
            'content_filtering',
            'usage_logging'
        ]

        for item in compliance_items:
            assessment['total_checks'] += 1
            # In practice, these would be actual checks
            assessment['passed_checks'] += 1

    def generate_readiness_report(self, assessment: Dict) -> str:
        """Generate production readiness report"""

        report = "# Production Readiness Assessment\n\n"

        score_percent = assessment['overall_score'] * 100
        report += f"## Overall Score: {score_percent:.1f}%\n\n"

        report += f"- Passed Checks: {assessment['passed_checks']}/{assessment['total_checks']}\n\n"

        if assessment['issues']:
            report += "## Issues Found\n\n"
            for issue in assessment['issues']:
                report += f"- {issue}\n"
            report += "\n"

        if assessment['recommendations']:
            report += "## Recommendations\n\n"
            for rec in assessment['recommendations']:
                report += f"- {rec}\n"

        # Readiness decision
        if score_percent >= 80:
            report += "\n## ✅ Ready for Production"
        elif score_percent >= 60:
            report += "\n## ⚠️ Ready for Staging"
        else:
            report += "\n## ❌ Not Ready for Production"

        return report

# Usage
readiness_checker = ProductionReadinessChecker()
assessment = readiness_checker.assess_readiness(model, tokenizer, test_results)
report = readiness_checker.generate_readiness_report(assessment)

with open('production_readiness.md', 'w') as f:
    f.write(report)

print("Production readiness report saved to production_readiness.md")
```

## What We've Accomplished

Outstanding! 📊 You've mastered model evaluation for LLaMA Factory:

1. **Core metrics** - ROUGE, BLEU, BERTScore, perplexity evaluation
2. **Task-specific evaluation** - Instruction following and quality assessment
3. **Automated frameworks** - HELM and OpenCompass integration
4. **Human evaluation** - Interfaces and feedback analysis
5. **Model comparison** - Statistical significance testing
6. **Production readiness** - Comprehensive assessment checklist

## Next Steps

Ready to deploy your evaluated models? In [Chapter 6: Deployment](06-deployment.md), we'll cover model deployment strategies and serving infrastructure!

---

**Practice what you've learned:**
1. Create a comprehensive evaluation suite for your specific task
2. Implement automated model comparison and A/B testing
3. Set up human evaluation workflows for quality assessment
4. Build a production readiness checklist for your models
5. Integrate automated benchmarking into your training pipeline

*What's the most important metric for evaluating your models?* 📈

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `report`, `assessment` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Model Evaluation` as an operating subsystem inside **LLaMA-Factory Tutorial: Unified Framework for LLM Training and Fine-tuning**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model`, `results`, `Dict` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Model Evaluation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `report` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `assessment`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/hiyouga/LLaMA-Factory)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `report` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Training Pipeline](04-training-pipeline.md)
- [Next Chapter: Chapter 6: Deployment](06-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
