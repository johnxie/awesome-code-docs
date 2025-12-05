---
layout: default
title: "LiteLLM Tutorial - Chapter 5: Fallbacks & Retries"
nav_order: 5
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 5: Fallbacks & Retries

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