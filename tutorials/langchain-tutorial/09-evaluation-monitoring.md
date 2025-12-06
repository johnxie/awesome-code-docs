---
layout: default
title: "LangChain Tutorial - Chapter 9: Evaluation & Monitoring"
nav_order: 9
has_children: false
parent: LangChain Tutorial
---

# Chapter 9: Evaluation, Monitoring, and Observability

> Evaluate LangChain application performance, monitor production deployments, and implement comprehensive observability.

## Evaluation Frameworks

### LangChain Evaluation

```python
from langchain.evaluation import load_evaluator, EvaluatorType
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Initialize evaluator
evaluator = load_evaluator(
    EvaluatorType.CRITERIA,
    criteria="accuracy",
    llm=ChatOpenAI(model="gpt-4o", temperature=0)
)

# Evaluate a prediction
eval_result = evaluator.evaluate_strings(
    prediction="The capital of France is Paris.",
    input="What is the capital of France?",
    reference="Paris"
)

print(f"Score: {eval_result['score']}")  # 1.0 for correct
print(f"Reasoning: {eval_result['reasoning']}")
```

### Custom Evaluation Metrics

```python
from typing import Dict, Any
from langchain.evaluation import StringEvaluator

class CustomEvaluator(StringEvaluator):
    """Custom evaluator for specific use cases."""

    @property
    def evaluation_name(self) -> str:
        return "custom_accuracy"

    def _evaluate_strings(
        self,
        prediction: str,
        input: str = None,
        reference: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Evaluate prediction against reference."""

        # Custom evaluation logic
        prediction_lower = prediction.lower().strip()
        reference_lower = reference.lower().strip()

        # Exact match
        exact_match = prediction_lower == reference_lower

        # Contains reference
        contains_ref = reference_lower in prediction_lower

        # Length similarity
        pred_len = len(prediction.split())
        ref_len = len(reference.split())
        length_ratio = min(pred_len, ref_len) / max(pred_len, ref_len)

        # Composite score
        score = 0.0
        if exact_match:
            score = 1.0
        elif contains_ref:
            score = 0.8
        elif length_ratio > 0.7:
            score = 0.6
        else:
            score = 0.2

        return {
            "score": score,
            "reasoning": f"Exact match: {exact_match}, Contains ref: {contains_ref}, Length ratio: {length_ratio:.2f}",
            "metadata": {
                "prediction_length": pred_len,
                "reference_length": ref_len,
                "exact_match": exact_match
            }
        }

# Usage
custom_evaluator = CustomEvaluator()
result = custom_evaluator.evaluate_strings(
    prediction="Paris is the capital of France.",
    reference="Paris"
)
```

### Batch Evaluation

```python
from langchain.evaluation import EvaluatorType
from langchain.smith import RunEvalConfig, run_on_dataset
import pandas as pd

# Load evaluation dataset
eval_data = [
    {
        "input": "What is 2 + 2?",
        "output": "4",
        "expected": "4"
    },
    {
        "input": "Capital of France?",
        "output": "Paris",
        "expected": "Paris"
    },
    # ... more examples
]

# Define evaluation configuration
eval_config = RunEvalConfig(
    evaluators=[
        EvaluatorType.QA,  # Question-answering evaluation
        EvaluatorType.CONTEXT_QA,  # Context-aware QA
        "custom_accuracy"  # Custom evaluator
    ],
    custom_evaluators=[CustomEvaluator()]
)

# Run evaluation
results = await run_on_dataset(
    client=your_langchain_app,  # Your LangChain chain/Runnable
    dataset=eval_data,
    evaluation=eval_config
)

# Analyze results
df = pd.DataFrame(results)
print(df.groupby('evaluator_name')['score'].mean())
```

## LangSmith Integration

### Tracing and Monitoring

```python
import os
from langchain_core.tracing import LangChainTracer
from langsmith import Client

# Set up LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langchain-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-langchain-app"

# Initialize tracer
tracer = LangChainTracer(project_name="my-langchain-app")

# Your LangChain application will automatically be traced
chain = your_langchain_chain.with_tracing(tracer)

# All executions will be logged to LangSmith
result = chain.invoke({"query": "What is machine learning?"})
```

### Performance Analysis

```python
from langsmith import Client

# Initialize LangSmith client
client = Client()

# Get recent runs
runs = client.list_runs(
    project_name="my-langchain-app",
    start_time=datetime.now() - timedelta(days=7)
)

# Analyze performance
total_runs = len(runs)
successful_runs = sum(1 for run in runs if run.status == "success")
error_runs = sum(1 for run in runs if run.status == "error")

print(f"Total runs: {total_runs}")
print(f"Success rate: {successful_runs/total_runs:.2%}")
print(f"Error rate: {error_runs/total_runs:.2%}")

# Analyze latency
latencies = [run.end_time - run.start_time for run in runs if run.end_time]
avg_latency = sum(latencies, timedelta()) / len(latencies)
print(f"Average latency: {avg_latency}")

# Get detailed run information
for run in runs[:5]:  # First 5 runs
    print(f"Run {run.id}: {run.name} - {run.status}")
    if run.error:
        print(f"  Error: {run.error}")
```

### Custom Metrics and Alerts

```python
from langsmith import Client
import time

class LangChainMonitor:
    def __init__(self, project_name: str):
        self.client = Client()
        self.project_name = project_name
        self.alerts = []

    def check_performance_metrics(self):
        """Check for performance issues and send alerts."""

        # Get recent runs
        runs = list(self.client.list_runs(
            project_name=self.project_name,
            start_time=datetime.now() - timedelta(hours=1)
        ))

        # Check error rate
        error_rate = sum(1 for run in runs if run.status == "error") / len(runs)

        if error_rate > 0.1:  # 10% error rate
            self.alerts.append({
                "type": "error_rate",
                "message": f"High error rate: {error_rate:.2%}",
                "severity": "high"
            })

        # Check latency
        latencies = [
            (run.end_time - run.start_time).total_seconds()
            for run in runs
            if run.end_time and run.start_time
        ]

        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            if avg_latency > 30:  # 30 seconds
                self.alerts.append({
                    "type": "latency",
                    "message": f"High latency: {avg_latency:.2f}s",
                    "severity": "medium"
                })

        return self.alerts

    def get_cost_analysis(self):
        """Analyze costs across different chains/models."""

        runs = list(self.client.list_runs(
            project_name=self.project_name,
            start_time=datetime.now() - timedelta(days=30)
        ))

        # Group by model
        model_costs = {}
        for run in runs:
            model = run.extra.get("model", "unknown")
            tokens = run.extra.get("tokens", 0)
            cost = self.calculate_cost(model, tokens)

            if model not in model_costs:
                model_costs[model] = {"total_cost": 0, "total_tokens": 0, "runs": 0}

            model_costs[model]["total_cost"] += cost
            model_costs[model]["total_tokens"] += tokens
            model_costs[model]["runs"] += 1

        return model_costs

    def calculate_cost(self, model: str, tokens: int) -> float:
        """Calculate cost based on model and token usage."""

        # Approximate costs per 1K tokens
        costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "claude-3-opus": {"input": 0.015, "output": 0.075}
        }

        model_costs = costs.get(model, {"input": 0, "output": 0})

        # Assume 70% of tokens are output (rough estimate)
        input_tokens = tokens * 0.3
        output_tokens = tokens * 0.7

        input_cost = (input_tokens / 1000) * model_costs["input"]
        output_cost = (output_tokens / 1000) * model_costs["output"]

        return input_cost + output_cost

# Usage
monitor = LangChainMonitor("my-langchain-app")

# Check for alerts
alerts = monitor.check_performance_metrics()
for alert in alerts:
    print(f"🚨 {alert['severity'].upper()}: {alert['message']}")

# Get cost analysis
costs = monitor.get_cost_analysis()
for model, data in costs.items():
    print(f"{model}: ${data['total_cost']:.2f} ({data['total_tokens']} tokens, {data['runs']} runs)")
```

## Custom Observability

### Application Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import time

class LangChainMetrics:
    def __init__(self):
        # Request metrics
        self.requests_total = Counter(
            'langchain_requests_total',
            'Total number of requests',
            ['chain_name', 'status']
        )

        self.request_duration = Histogram(
            'langchain_request_duration_seconds',
            'Request duration in seconds',
            ['chain_name']
        )

        # Token usage
        self.tokens_total = Counter(
            'langchain_tokens_total',
            'Total number of tokens used',
            ['chain_name', 'model', 'token_type']
        )

        # Active chains
        self.active_chains = Gauge(
            'langchain_active_chains',
            'Number of currently active chains'
        )

    def track_request(self, chain_name: str, start_time: float, status: str = "success"):
        """Track a request."""
        duration = time.time() - start_time

        self.requests_total.labels(chain_name=chain_name, status=status).inc()
        self.request_duration.labels(chain_name=chain_name).observe(duration)

    def track_tokens(self, chain_name: str, model: str, prompt_tokens: int, completion_tokens: int):
        """Track token usage."""
        self.tokens_total.labels(
            chain_name=chain_name,
            model=model,
            token_type="prompt"
        ).inc(prompt_tokens)

        self.tokens_total.labels(
            chain_name=chain_name,
            model=model,
            token_type="completion"
        ).inc(completion_tokens)

    def set_active_chains(self, count: int):
        """Set the number of active chains."""
        self.active_chains.set(count)

# Usage in LangChain application
metrics = LangChainMetrics()

class MonitoredChain:
    def __init__(self, chain, chain_name: str):
        self.chain = chain
        self.chain_name = chain_name
        self.metrics = LangChainMetrics()

    async def invoke(self, inputs, **kwargs):
        start_time = time.time()
        active_chains = self.metrics.active_chains._value.get() or 0
        self.metrics.set_active_chains(active_chains + 1)

        try:
            result = await self.chain.ainvoke(inputs, **kwargs)
            self.metrics.track_request(self.chain_name, start_time, "success")

            # Track token usage (if available)
            if hasattr(result, 'usage'):
                usage = result.usage
                self.metrics.track_tokens(
                    self.chain_name,
                    getattr(result, 'model_name', 'unknown'),
                    usage.prompt_tokens,
                    usage.completion_tokens
                )

            return result

        except Exception as e:
            self.metrics.track_request(self.chain_name, start_time, "error")
            raise

        finally:
            active_chains = self.metrics.active_chains._value.get() or 0
            self.metrics.set_active_chains(max(0, active_chains - 1))

# Wrap your chain
monitored_chain = MonitoredChain(your_langchain_chain, "my_chain")
result = await monitored_chain.invoke({"query": "Hello"})
```

## A/B Testing and Experimentation

### Model Comparison

```python
import asyncio
from typing import Dict, List
import statistics

class ABTester:
    def __init__(self, chains: Dict[str, Any]):
        self.chains = chains  # {"model_a": chain_a, "model_b": chain_b}
        self.results = {name: [] for name in chains.keys()}

    async def run_experiment(self, test_cases: List[Dict], runs_per_case: int = 3):
        """Run A/B test across multiple test cases."""

        for test_case in test_cases:
            print(f"Testing: {test_case['name']}")

            for model_name, chain in self.chains.items():
                latencies = []
                scores = []

                for run in range(runs_per_case):
                    start_time = time.time()

                    try:
                        result = await chain.ainvoke(test_case["input"])
                        latency = time.time() - start_time

                        # Evaluate result (you would implement actual evaluation)
                        score = self.evaluate_result(result, test_case.get("expected"))

                        latencies.append(latency)
                        scores.append(score)

                        print(f"  {model_name} run {run + 1}: {latency:.2f}s, score: {score}")

                    except Exception as e:
                        print(f"  {model_name} run {run + 1}: Failed - {e}")

                # Store results
                if latencies and scores:
                    self.results[model_name].append({
                        "test_case": test_case["name"],
                        "avg_latency": statistics.mean(latencies),
                        "avg_score": statistics.mean(scores),
                        "min_latency": min(latencies),
                        "max_latency": max(latencies)
                    })

    def evaluate_result(self, result: str, expected: str = None) -> float:
        """Evaluate result quality (implement your own logic)."""
        if not expected:
            # Basic evaluation - check if result is reasonable length
            return min(1.0, len(result.split()) / 50)  # Reward longer responses up to 50 words

        # Simple string similarity
        result_lower = result.lower()
        expected_lower = expected.lower()

        if expected_lower in result_lower:
            return 1.0
        elif len(set(result_lower.split()) & set(expected_lower.split())) > 0:
            return 0.5  # Some overlap
        else:
            return 0.0

    def get_report(self):
        """Generate experiment report."""
        report = {}

        for model_name, results in self.results.items():
            if results:
                avg_latencies = [r["avg_latency"] for r in results]
                avg_scores = [r["avg_score"] for r in results]

                report[model_name] = {
                    "overall_avg_latency": statistics.mean(avg_latencies),
                    "overall_avg_score": statistics.mean(avg_scores),
                    "best_latency": min(avg_latencies),
                    "best_score": max(avg_scores),
                    "test_results": results
                }

        return report

# Usage
test_cases = [
    {"name": "Simple QA", "input": {"query": "What is Python?"}},
    {"name": "Complex Reasoning", "input": {"query": "Explain how neural networks work"}},
    {"name": "Creative Task", "input": {"query": "Write a haiku about coding"}}
]

# Assume you have different model chains
chains = {
    "gpt-4": gpt4_chain,
    "claude-3": claude_chain,
    "gpt-3.5-turbo": gpt35_chain
}

tester = ABTester(chains)
await tester.run_experiment(test_cases)

report = tester.get_report()
for model, stats in report.items():
    print(f"{model}:")
    print(f"  Avg Latency: {stats['overall_avg_latency']:.2f}s")
    print(f"  Avg Score: {stats['overall_avg_score']:.2f}")
    print()
```

## Error Tracking and Debugging

### Structured Error Logging

```python
import logging
import json
from datetime import datetime

class LangChainErrorTracker:
    def __init__(self):
        self.errors = []
        self.logger = logging.getLogger("langchain_errors")

        # Set up logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

    def track_error(self, chain_name: str, error: Exception, inputs: Dict = None):
        """Track and log errors."""

        error_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "chain_name": chain_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "inputs": inputs,
            "stack_trace": self.get_stack_trace(error)
        }

        self.errors.append(error_info)

        # Log error
        self.logger.error(
            f"Chain '{chain_name}' failed: {error_info['error_message']}",
            extra={
                "chain_name": chain_name,
                "error_type": error_info["error_type"],
                "inputs": json.dumps(inputs) if inputs else None
            }
        )

        # Check for patterns
        self.analyze_error_patterns()

    def get_stack_trace(self, error: Exception) -> str:
        """Get formatted stack trace."""
        import traceback
        return "".join(traceback.format_exception(type(error), error, error.__traceback__))

    def analyze_error_patterns(self):
        """Analyze error patterns and suggest fixes."""

        if len(self.errors) < 5:
            return  # Need more data

        recent_errors = self.errors[-10:]  # Last 10 errors

        # Group by error type
        error_types = {}
        for error in recent_errors:
            error_type = error["error_type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        # Find most common error
        most_common = max(error_types.items(), key=lambda x: x[1])

        if most_common[1] >= 3:  # 3+ occurrences
            self.suggest_fix(most_common[0])

    def suggest_fix(self, error_type: str):
        """Suggest fixes for common errors."""

        suggestions = {
            "RateLimitError": "Implement rate limiting or exponential backoff",
            "AuthenticationError": "Check API keys and permissions",
            "TimeoutError": "Increase timeout or implement retries",
            "ValidationError": "Check input validation and schema",
            "ConnectionError": "Check network connectivity and endpoints"
        }

        suggestion = suggestions.get(error_type, "Review error details and implement error handling")

        self.logger.warning(f"Suggested fix for {error_type}: {suggestion}")

    def get_error_report(self):
        """Generate error summary report."""

        if not self.errors:
            return {"total_errors": 0, "message": "No errors recorded"}

        total_errors = len(self.errors)
        recent_errors = self.errors[-24:]  # Last 24 hours (assuming timestamp tracking)

        error_types = {}
        for error in recent_errors:
            error_type = error["error_type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        return {
            "total_errors": total_errors,
            "recent_errors": len(recent_errors),
            "error_types": error_types,
            "most_common_error": max(error_types.items(), key=lambda x: x[1]) if error_types else None
        }

# Usage in error handling
error_tracker = LangChainErrorTracker()

# Wrap chain execution
try:
    result = await chain.ainvoke(inputs)
except Exception as e:
    error_tracker.track_error("my_chain", e, inputs)
    # Handle error appropriately
```

## Continuous Improvement

### Automated Retraining Triggers

```python
class PerformanceMonitor:
    def __init__(self, threshold_score: float = 0.7):
        self.threshold_score = threshold_score
        self.performance_history = []
        self.retraining_triggers = []

    def track_performance(self, chain_name: str, score: float, latency: float):
        """Track chain performance metrics."""

        self.performance_history.append({
            "timestamp": datetime.utcnow(),
            "chain_name": chain_name,
            "score": score,
            "latency": latency
        })

        # Check if retraining is needed
        if self.should_retrain(chain_name):
            self.trigger_retraining(chain_name)

    def should_retrain(self, chain_name: str) -> bool:
        """Determine if retraining is needed."""

        # Get recent performance for this chain
        recent_perf = [
            p for p in self.performance_history[-50:]  # Last 50 runs
            if p["chain_name"] == chain_name
        ]

        if len(recent_perf) < 10:
            return False  # Need more data

        avg_score = sum(p["score"] for p in recent_perf) / len(recent_perf)
        avg_latency = sum(p["latency"] for p in recent_perf) / len(recent_perf)

        # Trigger retraining if performance degrades
        score_threshold = self.threshold_score * 0.9  # 10% degradation
        latency_threshold = avg_latency * 1.5  # 50% increase

        return avg_score < score_threshold

    def trigger_retraining(self, chain_name: str):
        """Trigger model retraining."""

        trigger_info = {
            "chain_name": chain_name,
            "timestamp": datetime.utcnow(),
            "reason": "performance_degradation",
            "current_metrics": self.get_current_metrics(chain_name)
        }

        self.retraining_triggers.append(trigger_info)

        # Log retraining trigger
        print(f"🔄 Retraining triggered for {chain_name}")
        print(f"Reason: {trigger_info['reason']}")
        print(f"Metrics: {trigger_info['current_metrics']}")

        # Here you would integrate with your ML pipeline
        # self.ml_pipeline.start_retraining(chain_name)

    def get_current_metrics(self, chain_name: str):
        """Get current performance metrics."""

        recent_perf = [
            p for p in self.performance_history[-20:]
            if p["chain_name"] == chain_name
        ]

        if not recent_perf:
            return {}

        return {
            "avg_score": sum(p["score"] for p in recent_perf) / len(recent_perf),
            "avg_latency": sum(p["latency"] for p in recent_perf) / len(recent_perf),
            "total_runs": len(recent_perf)
        }

# Usage
monitor = PerformanceMonitor(threshold_score=0.8)

# After each chain execution
monitor.track_performance("qa_chain", evaluation_score, latency_seconds)
```

This evaluation and monitoring chapter provides comprehensive tools for maintaining and improving LangChain application performance in production environments. The combination of evaluation frameworks, monitoring systems, and continuous improvement processes ensures your AI applications remain reliable and effective over time. 