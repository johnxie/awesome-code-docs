---
layout: default
title: "Pydantic AI Tutorial - Chapter 6: Error Handling & Recovery"
nav_order: 6
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 6: Error Handling, Retry Mechanisms & Recovery

Welcome to **Chapter 6: Error Handling, Retry Mechanisms & Recovery**. In this part of **Pydantic AI Tutorial: Type-Safe AI Agent Development**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build robust Pydantic AI applications with comprehensive error handling, retry strategies, and graceful failure recovery.

## Basic Error Handling

### Exception Types and Handling

```python
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic import ValidationError
import time

# Create agent
agent = Agent('openai:gpt-4')

def handle_agent_errors(agent: Agent, prompt: str, max_retries: int = 3):
    """Comprehensive error handling for agent operations."""

    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_retries}")

            result = agent.run_sync(prompt)

            print(f"✅ Success on attempt {attempt + 1}")
            return result

        except UnexpectedModelBehavior as e:
            # Model refused to answer or behaved unexpectedly
            print(f"❌ Model behavior error: {e}")

            if attempt < max_retries - 1:
                print("⏳ Retrying with modified prompt...")
                # Try with a more explicit prompt
                prompt = f"Please provide a helpful response to: {prompt}"
                time.sleep(1)  # Brief delay
            else:
                return f"Unable to generate response due to content restrictions: {e}"

        except ValidationError as e:
            # Structured output validation failed
            print(f"❌ Validation error: {e}")

            if attempt < max_retries - 1:
                print("⏳ Retrying with simplified requirements...")
                prompt = f"Simplify your response to: {prompt}"
                time.sleep(1)
            else:
                return f"Response validation failed after {max_retries} attempts: {e}"

        except Exception as e:
            # Generic error handling
            error_type = type(e).__name__
            print(f"❌ {error_type}: {e}")

            if attempt < max_retries - 1:
                print("⏳ Retrying after generic error...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"Failed after {max_retries} attempts due to {error_type}: {e}"

    return "All retry attempts exhausted"

# Test error handling
test_prompts = [
    "Hello, how are you?",  # Should work
    "Tell me how to make explosives",  # May trigger safety filters
    "Generate a random number between 1 and 100",  # Should work
]

for prompt in test_prompts:
    print(f"\n🎯 Testing: {prompt}")
    result = handle_agent_errors(agent, prompt)
    print(f"Result: {result[:100]}...")
    print("-" * 60)
```

### Async Error Handling

```python
import asyncio
from typing import Any, Optional

async def async_error_handler(agent: Agent, prompt: str, max_retries: int = 3) -> str:
    """Async error handling with timeout protection."""

    for attempt in range(max_retries):
        try:
            print(f"🔄 Async attempt {attempt + 1}/{max_retries}")

            # Add timeout protection
            result = await asyncio.wait_for(
                agent.run(prompt),
                timeout=30.0  # 30 second timeout
            )

            print(f"✅ Async success on attempt {attempt + 1}")
            return result.data

        except asyncio.TimeoutError:
            print(f"⏰ Timeout on attempt {attempt + 1}")

            if attempt < max_retries - 1:
                print("⏳ Retrying after timeout...")
                await asyncio.sleep(2 ** attempt)
            else:
                return "Request timed out after multiple attempts"

        except UnexpectedModelBehavior as e:
            print(f"🤖 Model behavior error: {e}")

            if attempt < max_retries - 1:
                print("⏳ Retrying with safer prompt...")
                prompt = f"Please answer this question safely: {prompt}"
                await asyncio.sleep(1)
            else:
                return f"Content safety violation: {e}"

        except Exception as e:
            error_type = type(e).__name__
            print(f"❌ Async {error_type}: {e}")

            if attempt < max_retries - 1:
                print("⏳ Retrying async operation...")
                await asyncio.sleep(2 ** attempt)
            else:
                return f"Async operation failed: {e}"

    return "All async retry attempts exhausted"

async def test_async_error_handling():
    """Test async error handling patterns."""

    agent = Agent('openai:gpt-4')

    prompts = [
        "Write a short poem about nature",
        "Explain the theory of relativity simply",
        "This is a very long prompt that might cause issues: " + "test " * 1000
    ]

    print("🌀 Testing async error handling:")

    for prompt in prompts:
        print(f"\n🎯 Testing: {prompt[:50]}...")
        result = await async_error_handler(agent, prompt)
        print(f"Result: {result[:100]}...")
        print("-" * 50)

# Run async error handling tests
asyncio.run(test_async_error_handling())
```

## Retry Strategies

### Exponential Backoff

```python
import random
from typing import Callable, Any
import asyncio

class RetryStrategy:
    """Advanced retry strategy with exponential backoff and jitter."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0,
                 max_delay: float = 60.0, backoff_factor: float = 2.0,
                 jitter: bool = True):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""

        # Exponential backoff: base_delay * (backoff_factor ^ attempt)
        delay = self.base_delay * (self.backoff_factor ** attempt)

        # Apply maximum delay limit
        delay = min(delay, self.max_delay)

        # Add jitter to prevent thundering herd
        if self.jitter:
            jitter_amount = random.uniform(0, delay * 0.1)  # 10% jitter
            delay += jitter_amount

        return delay

    async def execute_with_retry(self, operation: Callable[[], Any],
                               should_retry: Callable[[Exception], bool] = None) -> Any:
        """Execute operation with retry strategy."""

        last_exception = None

        for attempt in range(self.max_retries + 1):  # +1 for initial attempt
            try:
                print(f"🔄 Attempt {attempt + 1}/{self.max_retries + 1}")

                result = await operation()
                print(f"✅ Success on attempt {attempt + 1}")

                return result

            except Exception as e:
                last_exception = e

                # Check if we should retry this exception
                if should_retry and not should_retry(e):
                    print(f"❌ Non-retryable error: {e}")
                    raise e

                if attempt < self.max_retries:
                    delay = self.calculate_delay(attempt)
                    print(f"⏳ Retrying in {delay:.2f}s after error: {e}")
                    await asyncio.sleep(delay)
                else:
                    print(f"💥 All {self.max_retries + 1} attempts failed")

        raise last_exception

# Define retry conditions
def should_retry_error(error: Exception) -> bool:
    """Determine if error should trigger retry."""

    error_str = str(error).lower()
    error_type = type(error).__name__

    # Retry on network/rate limit errors
    retryable_errors = [
        "timeout", "connection", "rate limit", "502", "503", "504",
        "temporary", "transient", "overload"
    ]

    # Don't retry on validation or authentication errors
    non_retryable = [
        "validation", "authentication", "authorization", "400", "401", "403",
        "pydantic", "valueerror"
    ]

    # Check for non-retryable errors first
    for non_retry in non_retryable:
        if non_retry in error_str or non_retry in error_type.lower():
            return False

    # Check for retryable errors
    for retryable in retryable_errors:
        if retryable in error_str or retryable in error_type.lower():
            return True

    # Default: retry on unknown errors
    return True

# Create retry strategy
retry_strategy = RetryStrategy(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0,
    backoff_factor=2.0,
    jitter=True
)

async def test_retry_strategy():
    """Test retry strategy with various failure scenarios."""

    agent = Agent('openai:gpt-4')

    # Test cases with different failure patterns
    test_cases = [
        {
            "name": "Normal operation",
            "prompt": "Hello, world!",
            "should_fail": False
        },
        {
            "name": "Rate limit simulation",
            "prompt": "This prompt might trigger rate limiting",
            "should_fail": False  # In practice, this might fail
        },
        {
            "name": "Validation error",
            "prompt": "Generate invalid structured data",
            "should_fail": True
        }
    ]

    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")

        async def operation():
            return await agent.run(test_case['prompt'])

        try:
            result = await retry_strategy.execute_with_retry(
                operation,
                should_retry_error
            )

            if isinstance(result, Exception):
                print(f"❌ Operation failed: {result}")
            else:
                print(f"✅ Operation succeeded: {len(result.data)} chars")

        except Exception as e:
            print(f"💥 Final failure: {e}")

        print("-" * 60)

# Run retry strategy tests
asyncio.run(test_retry_strategy())
```

### Circuit Breaker Pattern

```python
from enum import Enum
from typing import Dict, Any
import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"        # Failing, requests rejected
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker for API failure protection."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60,
                 success_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

    def can_execute(self) -> bool:
        """Check if operation can be executed."""

        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True

        return False

    def record_success(self):
        """Record successful operation."""

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._reset_circuit()
        else:
            # Reset failure count on success
            self.failure_count = 0

    def record_failure(self):
        """Record failed operation."""

        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt reset."""

        if self.last_failure_time is None:
            return True

        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.recovery_timeout

    def _reset_circuit(self):
        """Reset circuit to closed state."""

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        print("🔄 Circuit breaker reset - service recovered")

    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status."""

        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time
        }

class ProtectedAgent:
    """Agent protected by circuit breaker."""

    def __init__(self, agent: Agent, circuit_breaker: CircuitBreaker):
        self.agent = agent
        self.circuit_breaker = circuit_breaker

    async def run_protected(self, prompt: str) -> Any:
        """Run agent with circuit breaker protection."""

        if not self.circuit_breaker.can_execute():
            raise Exception("Circuit breaker is OPEN - service unavailable")

        try:
            result = await self.agent.run(prompt)
            self.circuit_breaker.record_success()
            return result

        except Exception as e:
            self.circuit_breaker.record_failure()
            raise e

# Create protected agent
circuit_breaker = CircuitBreaker(
    failure_threshold=3,    # Open after 3 failures
    recovery_timeout=30,    # Try reset after 30 seconds
    success_threshold=2     # Close after 2 successes
)

protected_agent = ProtectedAgent(
    Agent('openai:gpt-4'),
    circuit_breaker
)

async def test_circuit_breaker():
    """Test circuit breaker functionality."""

    print("🛡️ Testing circuit breaker protection:")

    # Simulate normal operation
    print("\n✅ Testing normal operation:")
    for i in range(3):
        try:
            result = await protected_agent.run_protected("Hello!")
            print(f"  Request {i+1}: Success")
        except Exception as e:
            print(f"  Request {i+1}: Failed - {e}")

    # Simulate failures
    print("\n❌ Simulating failures:")
    original_run = protected_agent.agent.run

    async def failing_run(*args, **kwargs):
        raise Exception("Simulated API failure")

    protected_agent.agent.run = failing_run

    for i in range(5):
        try:
            result = await protected_agent.run_protected("This will fail")
            print(f"  Request {i+1}: Unexpected success")
        except Exception as e:
            status = circuit_breaker.get_status()
            print(f"  Request {i+1}: Failed - Circuit state: {status['state']}")

    # Restore normal operation
    protected_agent.agent.run = original_run

    # Wait for recovery timeout
    print("
⏳ Waiting for circuit recovery..."    await asyncio.sleep(35)

    # Test recovery
    print("\n🔄 Testing recovery:")
    try:
        result = await protected_agent.run_protected("Recovery test")
        status = circuit_breaker.get_status()
        print(f"  Recovery successful - Circuit state: {status['state']}")
    except Exception as e:
        print(f"  Recovery failed: {e}")

# Run circuit breaker tests
asyncio.run(test_circuit_breaker())
```

## Recovery Strategies

### Graceful Degradation

```python
from typing import List, Dict, Any, Optional

class GracefulDegradationAgent:
    """Agent with graceful degradation capabilities."""

    def __init__(self, primary_agent: Agent, fallback_agents: List[Agent] = None):
        self.primary_agent = primary_agent
        self.fallback_agents = fallback_agents or []
        self.performance_history: List[Dict[str, Any]] = []

    async def run_with_degradation(self, prompt: str, quality_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run with graceful degradation based on quality preferences."""

        quality_preferences = quality_preferences or {
            "max_tokens": 1000,
            "require_structured_output": False,
            "allow_fallback": True
        }

        # Try primary agent first
        try:
            print("🎯 Trying primary agent...")

            start_time = time.time()
            result = await self.primary_agent.run(prompt)
            duration = time.time() - start_time

            self._record_performance("primary", duration, True)

            return {
                "result": result.data,
                "agent_used": "primary",
                "quality": "full",
                "duration": duration
            }

        except Exception as e:
            print(f"❌ Primary agent failed: {e}")
            self._record_performance("primary", 0, False)

            if not quality_preferences.get("allow_fallback", True):
                raise e

        # Try fallback agents with reduced quality
        for i, fallback_agent in enumerate(self.fallback_agents):
            try:
                print(f"🔄 Trying fallback agent {i+1}...")

                # Modify prompt for fallback (simpler requirements)
                degraded_prompt = self._degrade_prompt(prompt, quality_preferences)

                start_time = time.time()
                result = await fallback_agent.run(degraded_prompt)
                duration = time.time() - start_time

                self._record_performance(f"fallback_{i+1}", duration, True)

                return {
                    "result": result.data,
                    "agent_used": f"fallback_{i+1}",
                    "quality": "degraded",
                    "duration": duration,
                    "degradation_reason": "primary_agent_failed"
                }

            except Exception as e:
                print(f"❌ Fallback agent {i+1} also failed: {e}")
                self._record_performance(f"fallback_{i+1}", 0, False)

        # All agents failed - provide minimal response
        return {
            "result": "I'm currently experiencing technical difficulties. Please try again later.",
            "agent_used": "none",
            "quality": "minimal",
            "error": "all_agents_failed"
        }

    def _degrade_prompt(self, prompt: str, preferences: Dict[str, Any]) -> str:
        """Degrade prompt for fallback agents."""

        degraded = prompt

        # Reduce complexity
        if len(prompt) > 500:
            degraded = prompt[:500] + "... (truncated for performance)"

        # Remove structured output requirements
        if "JSON" in prompt.upper() or "structured" in prompt.lower():
            degraded += "\n\nProvide a simple text response instead of structured data."

        # Add performance hint
        degraded += "\n\nPlease provide a concise response due to technical constraints."

        return degraded

    def _record_performance(self, agent_name: str, duration: float, success: bool):
        """Record agent performance."""

        self.performance_history.append({
            "agent": agent_name,
            "duration": duration,
            "success": success,
            "timestamp": time.time()
        })

        # Keep only last 100 records
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""

        if not self.performance_history:
            return {"error": "No performance data available"}

        stats = {}

        for record in self.performance_history:
            agent = record["agent"]
            if agent not in stats:
                stats[agent] = {
                    "total_calls": 0,
                    "successful_calls": 0,
                    "total_duration": 0,
                    "avg_duration": 0
                }

            stats[agent]["total_calls"] += 1
            stats[agent]["total_duration"] += record["duration"]

            if record["success"]:
                stats[agent]["successful_calls"] += 1

        # Calculate averages
        for agent_stats in stats.values():
            if agent_stats["total_calls"] > 0:
                agent_stats["success_rate"] = agent_stats["successful_calls"] / agent_stats["total_calls"]
                agent_stats["avg_duration"] = agent_stats["total_duration"] / agent_stats["total_calls"]

        return stats

# Create agents with different capabilities
primary_agent = Agent('openai:gpt-4')  # High quality, expensive
fallback_agent1 = Agent('anthropic:claude-3-haiku-20240307')  # Medium quality, cheaper
fallback_agent2 = Agent('google:gemini-1.5-flash')  # Lower quality, fastest

degradation_agent = GracefulDegradationAgent(
    primary_agent,
    [fallback_agent1, fallback_agent2]
)

async def test_graceful_degradation():
    """Test graceful degradation under various conditions."""

    test_scenarios = [
        {
            "name": "Normal operation",
            "prompt": "Explain photosynthesis in simple terms",
            "simulate_failure": False
        },
        {
            "name": "Primary failure - fallback success",
            "prompt": "Write a short story about a robot",
            "simulate_failure": True
        },
        {
            "name": "All failures - minimal response",
            "prompt": "Analyze this complex dataset",
            "simulate_failure": True,
            "fail_all": True
        }
    ]

    print("🛟 Testing graceful degradation:")

    for scenario in test_scenarios:
        print(f"\n🎯 Scenario: {scenario['name']}")

        # Simulate failures if requested
        if scenario.get("simulate_failure"):
            original_run = degradation_agent.primary_agent.run

            async def failing_run(*args, **kwargs):
                raise Exception("Simulated primary agent failure")

            degradation_agent.primary_agent.run = failing_run

            if scenario.get("fail_all"):
                # Make all agents fail
                for i, agent in enumerate(degradation_agent.fallback_agents):
                    agent.run = failing_run

        # Run test
        result = await degradation_agent.run_with_degradation(scenario["prompt"])

        print(f"  Agent used: {result['agent_used']}")
        print(f"  Quality: {result['quality']}")
        print(f"  Duration: {result.get('duration', 'N/A')}")
        print(f"  Response preview: {result['result'][:100]}...")

        # Restore normal operation
        if scenario.get("simulate_failure"):
            degradation_agent.primary_agent.run = original_run
            for agent in degradation_agent.fallback_agents:
                agent.run = original_run

        print("-" * 80)

    # Show performance stats
    stats = degradation_agent.get_performance_stats()
    print("
📊 Performance Statistics:"    for agent, agent_stats in stats.items():
        print(f"  {agent}:")
        print(f"    Calls: {agent_stats['total_calls']}")
        print(f"    Success rate: {agent_stats['success_rate']:.2%}")
        print(f"    Avg duration: {agent_stats['avg_duration']:.2f}s")

# Run graceful degradation tests
asyncio.run(test_graceful_degradation())
```

## Monitoring and Alerting

### Error Tracking and Metrics

```python
from collections import defaultdict, Counter
import json

class ErrorMonitor:
    """Monitor and track errors for alerting and analysis."""

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.error_counts = Counter()
        self.alert_thresholds = {
            "rate_limit_errors": 10,
            "validation_errors": 5,
            "timeout_errors": 15,
            "total_errors_per_hour": 50
        }

    def record_error(self, error: Exception, context: Dict[str, Any] = None):
        """Record an error with context."""

        error_record = {
            "timestamp": time.time(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "stack_trace": self._get_stack_trace(error)
        }

        self.errors.append(error_record)
        self.error_counts[type(error).__name__] += 1

        # Keep only last 1000 errors
        if len(self.errors) > 1000:
            self.errors = self.errors[-1000:]

        # Check for alerts
        self._check_alerts()

    def _get_stack_trace(self, error: Exception) -> str:
        """Get formatted stack trace."""
        import traceback
        return "".join(traceback.format_exception(type(error), error, error.__traceback__))

    def _check_alerts(self):
        """Check if any error thresholds have been exceeded."""

        # Check per error type thresholds
        for error_type, threshold in self.alert_thresholds.items():
            if error_type in self.error_counts:
                count = self.error_counts[error_type]
                if count >= threshold:
                    self._trigger_alert(error_type, count, threshold)

        # Check time-based thresholds
        recent_errors = self._get_recent_errors(3600)  # Last hour
        if len(recent_errors) >= self.alert_thresholds["total_errors_per_hour"]:
            self._trigger_alert("total_errors_per_hour", len(recent_errors),
                              self.alert_thresholds["total_errors_per_hour"])

    def _get_recent_errors(self, time_window: int) -> List[Dict[str, Any]]:
        """Get errors within time window."""
        cutoff_time = time.time() - time_window
        return [e for e in self.errors if e["timestamp"] >= cutoff_time]

    def _trigger_alert(self, alert_type: str, current_count: int, threshold: int):
        """Trigger an alert."""

        alert_message = f"""
🚨 ALERT: {alert_type}
Current count: {current_count}
Threshold: {threshold}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

Recent errors:
{self._format_recent_errors(5)}
        """.strip()

        print(alert_message)

        # In production, this would send email/Slack alerts
        # self._send_alert_notification(alert_message)

    def _format_recent_errors(self, limit: int) -> str:
        """Format recent errors for alert."""
        recent = self.errors[-limit:]
        formatted = []

        for error in recent:
            formatted.append(
                f"• {error['error_type']}: {error['error_message'][:100]}..."
            )

        return "\n".join(formatted)

    def get_error_report(self, time_window: int = 3600) -> Dict[str, Any]:
        """Generate error report."""

        recent_errors = self._get_recent_errors(time_window)

        report = {
            "time_window_seconds": time_window,
            "total_errors": len(recent_errors),
            "error_types": dict(self.error_counts),
            "most_common_errors": self.error_counts.most_common(5),
            "error_rate_per_hour": len(recent_errors) / (time_window / 3600),
            "recent_errors": recent_errors[-10:]  # Last 10 errors
        }

        return report

# Create error monitor
error_monitor = ErrorMonitor()

class MonitoredAgent:
    """Agent with comprehensive error monitoring."""

    def __init__(self, agent: Agent, error_monitor: ErrorMonitor):
        self.agent = agent
        self.error_monitor = error_monitor

    async def run_monitored(self, prompt: str, context: Dict[str, Any] = None) -> Any:
        """Run agent with error monitoring."""

        try:
            result = await self.agent.run(prompt)
            return result

        except Exception as e:
            # Record error with context
            error_context = {
                "agent_model": getattr(self.agent, 'model', {}).get('model_name', 'unknown'),
                "prompt_length": len(prompt),
                "timestamp": time.time(),
                **(context or {})
            }

            self.error_monitor.record_error(e, error_context)
            raise e

# Create monitored agent
monitored_agent = MonitoredAgent(Agent('openai:gpt-4'), error_monitor)

async def test_error_monitoring():
    """Test comprehensive error monitoring."""

    print("📊 Testing error monitoring and alerting:")

    # Simulate various errors
    error_scenarios = [
        ("rate_limit", lambda: (_ for _ in ()).throw(Exception("Rate limit exceeded"))),
        ("validation", lambda: (_ for _ in ()).throw(ValueError("Invalid input data"))),
        ("timeout", lambda: (_ for _ in ()).throw(TimeoutError("Request timed out"))),
        ("network", lambda: (_ for _ in ()).throw(ConnectionError("Network unreachable"))),
    ]

    for error_type, error_func in error_scenarios:
        print(f"\n🔥 Simulating {error_type} errors:")

        for i in range(12):  # Trigger alert threshold
            try:
                # Simulate error
                next(error_func())
            except Exception as e:
                try:
                    await monitored_agent.run_monitored(f"Test prompt {i}", {"test_id": i})
                except Exception:
                    pass  # Expected to fail

            if (i + 1) % 5 == 0:
                # Check error report
                report = error_monitor.get_error_report()
                print(f"  After {i+1} attempts: {report['total_errors']} total errors")

    # Generate final report
    final_report = error_monitor.get_error_report()

    print("
📋 Final Error Report:"    print(f"Total errors: {final_report['total_errors']}")
    print(f"Error rate per hour: {final_report['error_rate_per_hour']:.2f}")
    print(f"Most common errors: {final_report['most_common_errors']}")

    print("
📝 Recent Errors:"    for error in final_report['recent_errors'][-3:]:
        print(f"• {error['error_type']}: {error['error_message'][:80]}...")

# Run error monitoring tests
asyncio.run(test_error_monitoring())
```

## Recovery Workflows

### Automated Recovery Procedures

```python
from typing import Callable, Awaitable, Dict, Any
import asyncio

class RecoveryWorkflow:
    """Automated recovery workflow for agent failures."""

    def __init__(self):
        self.recovery_steps: Dict[str, Callable[[], Awaitable[bool]]] = {}
        self.recovery_history: List[Dict[str, Any]] = []

    def add_recovery_step(self, step_name: str, step_func: Callable[[], Awaitable[bool]]):
        """Add a recovery step."""
        self.recovery_steps[step_name] = step_func

    async def execute_recovery(self, error_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute recovery workflow."""

        recovery_session = {
            "start_time": time.time(),
            "error_context": error_context,
            "steps_executed": [],
            "success": False,
            "final_state": "unknown"
        }

        print("🔧 Initiating recovery workflow...")

        for step_name, step_func in self.recovery_steps.items():
            print(f"  Executing: {step_name}")

            try:
                start_time = time.time()
                success = await step_func()
                duration = time.time() - start_time

                step_result = {
                    "step": step_name,
                    "success": success,
                    "duration": duration,
                    "timestamp": time.time()
                }

                recovery_session["steps_executed"].append(step_result)

                if success:
                    print(f"    ✅ {step_name} succeeded ({duration:.2f}s)")
                else:
                    print(f"    ❌ {step_name} failed ({duration:.2f}s)")
                    break  # Stop on first failure

            except Exception as e:
                print(f"    💥 {step_name} crashed: {e}")
                step_result = {
                    "step": step_name,
                    "success": False,
                    "error": str(e),
                    "duration": 0,
                    "timestamp": time.time()
                }
                recovery_session["steps_executed"].append(step_result)
                break

        # Determine final state
        successful_steps = sum(1 for step in recovery_session["steps_executed"] if step["success"])

        if successful_steps == len(self.recovery_steps):
            recovery_session["success"] = True
            recovery_session["final_state"] = "fully_recovered"
        elif successful_steps > 0:
            recovery_session["success"] = True
            recovery_session["final_state"] = "partially_recovered"
        else:
            recovery_session["final_state"] = "recovery_failed"

        recovery_session["end_time"] = time.time()
        recovery_session["total_duration"] = recovery_session["end_time"] - recovery_session["start_time"]

        self.recovery_history.append(recovery_session)

        print(f"🔧 Recovery completed: {recovery_session['final_state']}")
        return recovery_session

# Create recovery workflow
recovery_workflow = RecoveryWorkflow()

# Add recovery steps
async def check_service_health() -> bool:
    """Check if services are healthy."""
    await asyncio.sleep(0.5)  # Simulate health check
    return True  # Assume service is healthy

async def restart_failed_components() -> bool:
    """Restart failed components."""
    await asyncio.sleep(1.0)  # Simulate restart
    return True  # Assume restart succeeded

async def verify_system_integrity() -> bool:
    """Verify system integrity after recovery."""
    await asyncio.sleep(0.8)  # Simulate integrity check
    return True  # Assume integrity verified

async def update_monitoring_alerts() -> bool:
    """Update monitoring and alert systems."""
    await asyncio.sleep(0.3)  # Simulate alert update
    return True  # Assume alerts updated

recovery_workflow.add_recovery_step("check_service_health", check_service_health)
recovery_workflow.add_recovery_step("restart_failed_components", restart_failed_components)
recovery_workflow.add_recovery_step("verify_system_integrity", verify_system_integrity)
recovery_workflow.add_recovery_step("update_monitoring_alerts", update_monitoring_alerts)

async def test_recovery_workflow():
    """Test recovery workflow execution."""

    print("🩺 Testing recovery workflow:")

    # Simulate different failure scenarios
    test_scenarios = [
        {"error_type": "api_timeout", "severity": "medium"},
        {"error_type": "rate_limit", "severity": "low"},
        {"error_type": "validation_error", "severity": "high"}
    ]

    for scenario in test_scenarios:
        print(f"\n💥 Simulating failure: {scenario['error_type']}")

        recovery_result = await recovery_workflow.execute_recovery(scenario)

        print("  Recovery Results:")
        print(f"    Success: {recovery_result['success']}")
        print(f"    Final State: {recovery_result['final_state']}")
        print(f"    Duration: {recovery_result['total_duration']:.2f}s")
        print(f"    Steps completed: {len(recovery_result['steps_executed'])}")

        successful_steps = sum(1 for step in recovery_result["steps_executed"] if step["success"])
        print(f"    Successful steps: {successful_steps}")

# Run recovery workflow tests
asyncio.run(test_recovery_workflow())
```

This comprehensive error handling chapter demonstrates robust error management, retry strategies, circuit breakers, graceful degradation, monitoring, and automated recovery procedures for production-ready Pydantic AI applications. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `print`, `agent` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Error Handling, Retry Mechanisms & Recovery` as an operating subsystem inside **Pydantic AI Tutorial: Type-Safe AI Agent Development**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `error`, `prompt`, `time` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Error Handling, Retry Mechanisms & Recovery` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `print` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `agent`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/pydantic/pydantic-ai)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `print` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Streaming Responses & Async Operations](05-streaming-async.md)
- [Next Chapter: Chapter 7: Advanced Patterns & Multi-Step Workflows](07-advanced-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
