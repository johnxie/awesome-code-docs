---
layout: default
title: "LiteLLM Tutorial - Chapter 5: Fallbacks & Retries"
nav_order: 5
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 5: Fallbacks & Retries

Welcome to **Chapter 5: Fallbacks & Retries**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build resilient LLM applications with automatic fallbacks, intelligent retries, and failure recovery.

## Overview

Production AI applications need to handle failures gracefully. This chapter covers implementing fallback strategies, retry logic, and circuit breakers to ensure your application remains available even when individual providers fail.

## Basic Retry Logic

Simple retry with exponential backoff:

```python
import litellm
import time
import random

def completion_with_retry(model, messages, max_retries=3, base_delay=1):
    """Completion with exponential backoff retry."""

    for attempt in range(max_retries):
        try:
            return litellm.completion(
                model=model,
                messages=messages,
                timeout=30
            )

        except litellm.RateLimitError as e:
            if attempt == max_retries - 1:
                raise  # Re-raise on last attempt

            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited, retrying in {delay:.2f} seconds...")
            time.sleep(delay)

        except litellm.APIError as e:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt)
            print(f"API error, retrying in {delay:.2f} seconds...")
            time.sleep(delay)

# Usage
try:
    response = completion_with_retry(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print(f"All retries failed: {e}")
```

## Provider Fallbacks

Automatically switch to backup providers:

```python
def completion_with_fallbacks(messages, primary_model="gpt-4", fallback_models=None):
    """Try multiple models/providers in sequence."""

    if fallback_models is None:
        fallback_models = ["gpt-4-turbo", "claude-3-opus-20240229", "gpt-3.5-turbo"]

    all_models = [primary_model] + fallback_models

    for model in all_models:
        try:
            print(f"Trying {model}...")
            response = litellm.completion(
                model=model,
                messages=messages,
                timeout=30
            )
            print(f"Success with {model}")
            return response, model

        except Exception as e:
            print(f"Failed with {model}: {e}")
            continue

    raise Exception(f"All models failed: {all_models}")

# Usage
response, used_model = completion_with_fallbacks(
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)
print(f"Used model: {used_model}")
```

## Intelligent Fallback Strategy

Choose fallbacks based on task requirements:

```python
class IntelligentFallback:
    def __init__(self):
        # Define fallback chains for different use cases
        self.strategies = {
            "high_quality": ["gpt-4", "claude-3-opus-20240229", "gpt-4-turbo"],
            "fast_cheap": ["gpt-3.5-turbo", "claude-3-haiku-20240307", "command"],
            "creative": ["claude-3-sonnet-20240229", "gpt-4", "claude-3-opus-20240229"],
            "coding": ["gpt-4", "claude-3-opus-20240229", "ollama/codellama"],
            "analysis": ["gpt-4-turbo", "claude-3-sonnet-20240229", "gpt-4"]
        }

    def select_strategy(self, task_description, budget=None):
        """Select appropriate fallback strategy based on task."""

        task_lower = task_description.lower()

        if "code" in task_lower or "programming" in task_lower:
            return self.strategies["coding"]
        elif "creative" in task_lower or "write" in task_lower or "story" in task_lower:
            return self.strategies["creative"]
        elif "analyze" in task_lower or "research" in task_lower:
            return self.strategies["analysis"]
        elif budget == "low" or len(task_description.split()) < 50:
            return self.strategies["fast_cheap"]
        else:
            return self.strategies["high_quality"]

    def complete_with_strategy(self, messages, strategy_name=None, task_description=None):
        """Complete with intelligent fallback strategy."""

        if strategy_name:
            models = self.strategies.get(strategy_name, self.strategies["high_quality"])
        elif task_description:
            models = self.select_strategy(task_description)
        else:
            models = self.strategies["high_quality"]

        return completion_with_fallbacks(messages, primary_model=models[0], fallback_models=models[1:])

# Usage
fallback_ai = IntelligentFallback()

# Auto-select strategy based on task
response, model = fallback_ai.complete_with_strategy(
    messages=[{"role": "user", "content": "Write a Python function to sort a list"}],
    task_description="Write a Python function to sort a list"
)

# Manual strategy selection
response, model = fallback_ai.complete_with_strategy(
    messages=[{"role": "user", "content": "Brainstorm marketing ideas"}],
    strategy_name="creative"
)
```

## Circuit Breaker Pattern

Prevent cascading failures:

```python
import time
from collections import defaultdict

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_counts = defaultdict(int)
        self.last_failure_times = defaultdict(float)
        self.states = defaultdict(str)  # 'closed', 'open', 'half_open'

    def _is_open(self, key):
        """Check if circuit breaker is open."""
        return (self.states[key] == 'open' and
                time.time() - self.last_failure_times[key] < self.recovery_timeout)

    def _record_success(self, key):
        """Record successful operation."""
        self.failure_counts[key] = 0
        self.states[key] = 'closed'

    def _record_failure(self, key):
        """Record failed operation."""
        self.failure_counts[key] += 1
        self.last_failure_times[key] = time.time()

        if self.failure_counts[key] >= self.failure_threshold:
            self.states[key] = 'open'
            print(f"Circuit breaker opened for {key}")

    def call(self, key, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""

        if self._is_open(key):
            raise Exception(f"Circuit breaker is open for {key}")

        try:
            result = func(*args, **kwargs)
            self._record_success(key)
            return result
        except Exception as e:
            self._record_failure(key)
            raise

# Usage
circuit_breaker = CircuitBreaker()

def protected_completion(model, messages):
    """Completion protected by circuit breaker."""
    return circuit_breaker.call(
        f"model_{model}",
        litellm.completion,
        model=model,
        messages=messages,
        timeout=30
    )

# Try with circuit breaker
try:
    response = protected_completion("unreliable-model", messages)
except Exception as e:
    print(f"Request failed: {e}")
```

## Async Fallbacks

Concurrent fallback attempts for faster recovery:

```python
import asyncio

async def async_completion_with_fallbacks(messages, models, timeout=30):
    """Try multiple models concurrently for faster fallback."""

    async def try_model(model):
        """Try a single model with timeout."""
        try:
            return await asyncio.wait_for(
                litellm.acompletion(
                    model=model,
                    messages=messages,
                    max_tokens=500
                ),
                timeout=timeout
            ), model
        except Exception as e:
            return None, model, str(e)

    # Launch all attempts concurrently
    tasks = [try_model(model) for model in models]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Return first successful result
    for result in results:
        if result and result[0] is not None:
            response, successful_model = result[0], result[1]
            print(f"Success with {successful_model}")
            return response, successful_model

    # All failed
    errors = [result[2] for result in results if result and len(result) > 2]
    raise Exception(f"All models failed: {errors}")

# Usage
models = ["gpt-4", "claude-3-opus-20240229", "gpt-3.5-turbo"]

response, used_model = await async_completion_with_fallbacks(
    messages=[{"role": "user", "content": "Hello, world!"}],
    models=models
)
```

## Load Balancing

Distribute load across multiple providers:

```python
import random
from collections import defaultdict

class LoadBalancer:
    def __init__(self, models_and_weights):
        """
        models_and_weights: dict of {"model_name": weight}
        Higher weight = more likely to be selected
        """
        self.models = list(models_and_weights.keys())
        self.weights = list(models_and_weights.values())
        self.success_counts = defaultdict(int)
        self.failure_counts = defaultdict(int)

    def select_model(self, strategy="weighted"):
        """Select a model based on strategy."""

        if strategy == "weighted":
            # Weighted random selection
            return random.choices(self.models, weights=self.weights)[0]

        elif strategy == "round_robin":
            # Simple round-robin (simplified)
            return random.choice(self.models)

        elif strategy == "least_loaded":
            # Choose model with fewest recent failures
            scores = {}
            for model in self.models:
                total = self.success_counts[model] + self.failure_counts[model]
                if total == 0:
                    scores[model] = 1.0  # No data, assume good
                else:
                    success_rate = self.success_counts[model] / total
                    scores[model] = success_rate

            return max(scores, key=scores.get)

    def record_result(self, model, success):
        """Record success/failure for load balancing."""
        if success:
            self.success_counts[model] += 1
        else:
            self.failure_counts[model] += 1

    def completion_with_load_balancing(self, messages, **kwargs):
        """Completion with load balancing."""
        max_attempts = len(self.models)

        for attempt in range(max_attempts):
            model = self.select_model()

            try:
                response = litellm.completion(
                    model=model,
                    messages=messages,
                    **kwargs
                )

                self.record_result(model, True)
                return response, model

            except Exception as e:
                self.record_result(model, False)
                if attempt == max_attempts - 1:
                    raise
                continue

# Usage
load_balancer = LoadBalancer({
    "gpt-4": 1,           # Low weight, expensive
    "gpt-4-turbo": 3,     # Medium weight
    "gpt-3.5-turbo": 5,   # High weight, cheap
    "claude-3-haiku-20240307": 4  # Good balance
})

response, used_model = load_balancer.completion_with_load_balancing(
    messages=[{"role": "user", "content": "Summarize this article"}]
)
```

## Comprehensive Resilience Framework

Combine all patterns into a robust framework:

```python
class ResilientAIClient:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker()
        self.load_balancer = LoadBalancer({
            "gpt-4": 1,
            "claude-3-opus-20240229": 2,
            "gpt-3.5-turbo": 3
        })
        self.fallback_ai = IntelligentFallback()

    async def resilient_completion(self, messages, task_description=None, **kwargs):
        """Highly resilient completion with all protection mechanisms."""

        # Select appropriate fallback strategy
        if task_description:
            models = self.fallback_ai.select_strategy(task_description)
        else:
            models = ["gpt-4", "claude-3-opus-20240229", "gpt-3.5-turbo"]

        # Try with load balancing and circuit breaker
        primary_model = self.load_balancer.select_model()

        try:
            # Try primary model with circuit breaker
            response = self.circuit_breaker.call(
                f"model_{primary_model}",
                litellm.completion,
                model=primary_model,
                messages=messages,
                **kwargs
            )

            self.load_balancer.record_result(primary_model, True)
            return response, primary_model

        except Exception as e:
            self.load_balancer.record_result(primary_model, False)

            # Fallback to other models concurrently
            try:
                response, successful_model = await async_completion_with_fallbacks(
                    messages, models[1:], **kwargs
                )
                return response, successful_model

            except Exception as fallback_error:
                raise Exception(f"All models failed. Primary: {e}, Fallbacks: {fallback_error}")

# Usage
resilient_client = ResilientAIClient()

response, model_used = await resilient_client.resilient_completion(
    messages=[{"role": "user", "content": "Write a business plan summary"}],
    task_description="business analysis"
)
```

## Monitoring and Alerting

Track failure patterns and performance:

```python
class FailureMonitor:
    def __init__(self):
        self.failures = defaultdict(list)
        self.alert_threshold = 5  # failures per hour

    def record_failure(self, model, error_type, error_message):
        """Record a failure for monitoring."""
        timestamp = time.time()
        self.failures[model].append({
            "timestamp": timestamp,
            "error_type": error_type,
            "error_message": error_message
        })

        # Clean old failures (keep last hour)
        cutoff = timestamp - 3600
        self.failures[model] = [
            f for f in self.failures[model]
            if f["timestamp"] > cutoff
        ]

        # Check for alert condition
        if len(self.failures[model]) >= self.alert_threshold:
            self.send_alert(model, len(self.failures[model]))

    def send_alert(self, model, failure_count):
        """Send alert about high failure rate."""
        print(f"🚨 ALERT: {model} has {failure_count} failures in the last hour!")
        # In production, send email/SMS/webhook here

# Integrate with your completion functions
monitor = FailureMonitor()

def monitored_completion(model, messages, **kwargs):
    """Completion with failure monitoring."""
    try:
        response = litellm.completion(model=model, messages=messages, **kwargs)
        return response
    except Exception as e:
        error_type = type(e).__name__
        monitor.record_failure(model, error_type, str(e))
        raise

# Usage
try:
    response = monitored_completion("gpt-4", messages)
except Exception as e:
    print(f"Completion failed: {e}")
    # Alert already sent by monitor
```

## Best Practices

1. **Start Simple**: Begin with basic retries, add complexity as needed
2. **Monitor Everything**: Track success rates, latency, and error types
3. **Graceful Degradation**: Have fallback behaviors that work even when all providers fail
4. **Cost Awareness**: Consider cost implications of fallback chains
5. **User Communication**: Inform users when fallbacks are being used
6. **Testing**: Regularly test your fallback scenarios
7. **Metrics**: Collect metrics on fallback usage and effectiveness

## Configuration Examples

Production-ready configuration:

```python
# production_config.py
RESILIENCE_CONFIG = {
    "retry": {
        "max_attempts": 3,
        "base_delay": 1,
        "max_delay": 60
    },
    "circuit_breaker": {
        "failure_threshold": 10,
        "recovery_timeout": 300  # 5 minutes
    },
    "load_balancer": {
        "models": {
            "gpt-4": 1,
            "gpt-4-turbo": 3,
            "claude-3-opus-20240229": 2,
            "gpt-3.5-turbo": 5
        },
        "strategy": "weighted"
    },
    "fallback_chains": {
        "default": ["gpt-4", "claude-3-opus-20240229", "gpt-3.5-turbo"],
        "fast": ["gpt-3.5-turbo", "claude-3-haiku-20240307"],
        "quality": ["gpt-4", "claude-3-opus-20240229"]
    }
}

def create_resilient_client(config=RESILIENCE_CONFIG):
    """Create a fully configured resilient client."""
    # Implementation would use all the patterns above
    return ResilientAIClient(config)
```

These resilience patterns ensure your AI applications remain reliable and available, even when individual providers experience issues. The key is layering multiple protection mechanisms to handle different types of failures gracefully.

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- tutorial slug: **litellm-tutorial**
- chapter focus: **Chapter 5: Fallbacks & Retries**
- system context: **Litellm Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 5: Fallbacks & Retries`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
- [LiteLLM Docs](https://docs.litellm.ai/)

### Cross-Tutorial Connection Map

- [Langfuse Tutorial](../langfuse-tutorial/)
- [Vercel AI SDK Tutorial](../vercel-ai-tutorial/)
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/)
- [Aider Tutorial](../aider-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 5: Fallbacks & Retries`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `model`, `messages` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Fallbacks & Retries` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `models`, `response`, `claude` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Fallbacks & Retries` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `messages`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
  Why it matters: authoritative reference on `LiteLLM Repository` (github.com).
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
  Why it matters: authoritative reference on `LiteLLM Releases` (github.com).
- [LiteLLM Docs](https://docs.litellm.ai/)
  Why it matters: authoritative reference on `LiteLLM Docs` (docs.litellm.ai).

Suggested trace strategy:
- search upstream code for `self` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Streaming & Async](04-streaming.md)
- [Next Chapter: Chapter 6: Cost Tracking](06-cost-tracking.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
