---
layout: default
title: "Chapter 7: Production Best Practices"
parent: "Anthropic API Tutorial"
nav_order: 7
---

# Chapter 7: Production Best Practices

> Build reliable, scalable, and cost-effective AI applications with proper error handling, rate limiting, monitoring, and deployment strategies.

## Overview

Moving from development to production requires careful attention to reliability, performance, cost management, and observability. This chapter covers best practices for deploying Claude-powered applications at scale.

## Error Handling

### Comprehensive Error Handling

```python
import anthropic
from anthropic import (
    APIError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    APIConnectionError,
    InternalServerError
)
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeClient:
    """Production-ready Claude client with comprehensive error handling."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.client = anthropic.Anthropic()
        self.max_retries = max_retries
        self.base_delay = base_delay

    def create_message(self, **kwargs) -> anthropic.types.Message:
        """Create a message with automatic retry and error handling."""

        last_error = None

        for attempt in range(self.max_retries):
            try:
                return self.client.messages.create(**kwargs)

            except AuthenticationError as e:
                logger.error(f"Authentication failed: {e}")
                raise  # Don't retry auth errors

            except BadRequestError as e:
                logger.error(f"Bad request: {e}")
                raise  # Don't retry invalid requests

            except RateLimitError as e:
                delay = self._get_retry_delay(e, attempt)
                logger.warning(f"Rate limited. Waiting {delay}s before retry {attempt + 1}")
                time.sleep(delay)
                last_error = e

            except APIConnectionError as e:
                delay = self._exponential_backoff(attempt)
                logger.warning(f"Connection error. Waiting {delay}s before retry {attempt + 1}")
                time.sleep(delay)
                last_error = e

            except InternalServerError as e:
                delay = self._exponential_backoff(attempt)
                logger.warning(f"Server error. Waiting {delay}s before retry {attempt + 1}")
                time.sleep(delay)
                last_error = e

            except APIError as e:
                logger.error(f"API error: {e}")
                if e.status_code and e.status_code >= 500:
                    delay = self._exponential_backoff(attempt)
                    time.sleep(delay)
                    last_error = e
                else:
                    raise

        # All retries exhausted
        logger.error(f"All {self.max_retries} retries exhausted")
        raise last_error

    def _get_retry_delay(self, error: RateLimitError, attempt: int) -> float:
        """Get retry delay from rate limit headers or calculate exponentially."""
        # Check for Retry-After header
        if hasattr(error, 'response') and error.response:
            retry_after = error.response.headers.get('retry-after')
            if retry_after:
                return float(retry_after)

        return self._exponential_backoff(attempt)

    def _exponential_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff with jitter."""
        import random
        delay = self.base_delay * (2 ** attempt)
        jitter = random.uniform(0, delay * 0.1)
        return delay + jitter
```

### Circuit Breaker Pattern

```python
import time
from enum import Enum
from threading import Lock

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """Circuit breaker for API calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        self.lock = Lock()

    def can_execute(self) -> bool:
        """Check if request can be executed."""
        with self.lock:
            if self.state == CircuitState.CLOSED:
                return True

            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    return True
                return False

            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls < self.half_open_max_calls:
                    self.half_open_calls += 1
                    return True
                return False

        return False

    def record_success(self):
        """Record a successful call."""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.half_open_calls += 1
                if self.half_open_calls >= self.half_open_max_calls:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    def record_failure(self):
        """Record a failed call."""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN


class ResilientClaudeClient:
    """Claude client with circuit breaker."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.circuit_breaker = CircuitBreaker()

    def create_message(self, **kwargs):
        if not self.circuit_breaker.can_execute():
            raise Exception("Circuit breaker is open - service unavailable")

        try:
            response = self.client.messages.create(**kwargs)
            self.circuit_breaker.record_success()
            return response
        except Exception as e:
            self.circuit_breaker.record_failure()
            raise
```

## Rate Limiting

### Client-Side Rate Limiting

```python
import time
import threading
from collections import deque

class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, requests_per_minute: int = 50, tokens_per_minute: int = 100000):
        self.rpm_limit = requests_per_minute
        self.tpm_limit = tokens_per_minute

        self.request_times = deque()
        self.token_usage = deque()
        self.lock = threading.Lock()

    def acquire(self, estimated_tokens: int = 1000) -> float:
        """
        Acquire permission to make a request.
        Returns wait time in seconds (0 if immediate).
        """
        with self.lock:
            now = time.time()
            minute_ago = now - 60

            # Clean old entries
            while self.request_times and self.request_times[0] < minute_ago:
                self.request_times.popleft()
            while self.token_usage and self.token_usage[0][0] < minute_ago:
                self.token_usage.popleft()

            # Check request limit
            if len(self.request_times) >= self.rpm_limit:
                wait_time = self.request_times[0] - minute_ago
                return wait_time

            # Check token limit
            current_tokens = sum(t[1] for t in self.token_usage)
            if current_tokens + estimated_tokens > self.tpm_limit:
                wait_time = self.token_usage[0][0] - minute_ago
                return wait_time

            # Record this request
            self.request_times.append(now)
            self.token_usage.append((now, estimated_tokens))

            return 0

    def update_tokens(self, actual_tokens: int, estimated_tokens: int):
        """Update token count with actual usage."""
        with self.lock:
            # Adjust the last entry
            if self.token_usage:
                timestamp, _ = self.token_usage.pop()
                self.token_usage.append((timestamp, actual_tokens))


class RateLimitedClient:
    """Client with built-in rate limiting."""

    def __init__(self, rpm: int = 50, tpm: int = 100000):
        self.client = anthropic.Anthropic()
        self.limiter = RateLimiter(rpm, tpm)

    def create_message(self, **kwargs):
        # Estimate tokens (rough approximation)
        estimated = self._estimate_tokens(kwargs)

        # Wait if needed
        wait_time = self.limiter.acquire(estimated)
        if wait_time > 0:
            time.sleep(wait_time)
            self.limiter.acquire(estimated)

        # Make request
        response = self.client.messages.create(**kwargs)

        # Update actual usage
        actual = response.usage.input_tokens + response.usage.output_tokens
        self.limiter.update_tokens(actual, estimated)

        return response

    def _estimate_tokens(self, kwargs) -> int:
        """Estimate token count for a request."""
        messages = kwargs.get("messages", [])
        text_length = sum(
            len(str(m.get("content", "")))
            for m in messages
        )
        # Rough estimate: 4 chars per token
        input_estimate = text_length // 4
        output_estimate = kwargs.get("max_tokens", 1024)
        return input_estimate + output_estimate
```

## Monitoring and Observability

### Request Logging

```python
import logging
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class RequestLog:
    """Structured log entry for API requests."""
    request_id: str
    timestamp: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    status: str
    error: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[dict] = None

class MonitoredClient:
    """Client with comprehensive monitoring."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.logger = logging.getLogger("anthropic.requests")

        # Metrics storage (in production, use Prometheus, DataDog, etc.)
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_latency_ms": 0
        }

    def create_message(self, user_id: str = None, **kwargs):
        import uuid
        request_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            response = self.client.messages.create(**kwargs)

            latency_ms = (time.time() - start_time) * 1000

            log = RequestLog(
                request_id=request_id,
                timestamp=datetime.utcnow().isoformat(),
                model=kwargs.get("model", "unknown"),
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                latency_ms=latency_ms,
                status="success",
                user_id=user_id
            )

            self._record_metrics(log)
            self.logger.info(json.dumps(asdict(log)))

            return response

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000

            log = RequestLog(
                request_id=request_id,
                timestamp=datetime.utcnow().isoformat(),
                model=kwargs.get("model", "unknown"),
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
                status="error",
                error=str(e),
                user_id=user_id
            )

            self._record_metrics(log)
            self.logger.error(json.dumps(asdict(log)))

            raise

    def _record_metrics(self, log: RequestLog):
        """Update metrics."""
        self.metrics["total_requests"] += 1
        if log.status == "success":
            self.metrics["successful_requests"] += 1
            self.metrics["total_input_tokens"] += log.input_tokens
            self.metrics["total_output_tokens"] += log.output_tokens
        else:
            self.metrics["failed_requests"] += 1
        self.metrics["total_latency_ms"] += log.latency_ms

    def get_metrics(self) -> dict:
        """Get current metrics."""
        m = self.metrics.copy()
        if m["total_requests"] > 0:
            m["avg_latency_ms"] = m["total_latency_ms"] / m["total_requests"]
            m["success_rate"] = m["successful_requests"] / m["total_requests"]
        return m
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
REQUEST_COUNT = Counter(
    'anthropic_requests_total',
    'Total API requests',
    ['model', 'status']
)

REQUEST_LATENCY = Histogram(
    'anthropic_request_latency_seconds',
    'Request latency',
    ['model'],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30]
)

TOKEN_USAGE = Counter(
    'anthropic_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: input or output
)

ACTIVE_REQUESTS = Gauge(
    'anthropic_active_requests',
    'Currently active requests'
)

class PrometheusMonitoredClient:
    """Client with Prometheus metrics."""

    def __init__(self):
        self.client = anthropic.Anthropic()

    def create_message(self, **kwargs):
        model = kwargs.get("model", "unknown")
        ACTIVE_REQUESTS.inc()

        start_time = time.time()
        try:
            response = self.client.messages.create(**kwargs)

            # Record success metrics
            REQUEST_COUNT.labels(model=model, status="success").inc()
            REQUEST_LATENCY.labels(model=model).observe(time.time() - start_time)
            TOKEN_USAGE.labels(model=model, type="input").inc(response.usage.input_tokens)
            TOKEN_USAGE.labels(model=model, type="output").inc(response.usage.output_tokens)

            return response

        except Exception as e:
            REQUEST_COUNT.labels(model=model, status="error").inc()
            raise

        finally:
            ACTIVE_REQUESTS.dec()
```

## Cost Management

### Cost Tracking

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List
import json

@dataclass
class UsageRecord:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    user_id: str = None
    request_type: str = None

class CostTracker:
    """Track and manage API costs."""

    # Pricing per million tokens (update as needed)
    PRICING = {
        "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
        "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
        "claude-3-5-haiku-20241022": {"input": 0.25, "output": 1.25}
    }

    def __init__(self, budget_limit: float = None):
        self.records: List[UsageRecord] = []
        self.budget_limit = budget_limit

    def record_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        user_id: str = None,
        request_type: str = None
    ):
        """Record API usage."""
        cost = self.calculate_cost(model, input_tokens, output_tokens)

        record = UsageRecord(
            timestamp=datetime.utcnow(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            user_id=user_id,
            request_type=request_type
        )
        self.records.append(record)

        # Check budget
        if self.budget_limit:
            period_cost = self.get_period_cost(days=30)
            if period_cost > self.budget_limit:
                raise Exception(f"Budget exceeded: ${period_cost:.2f} > ${self.budget_limit:.2f}")

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a request."""
        pricing = self.PRICING.get(model, self.PRICING["claude-sonnet-4-20250514"])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost

    def get_period_cost(self, days: int = 30) -> float:
        """Get total cost for a time period."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return sum(r.cost for r in self.records if r.timestamp > cutoff)

    def get_cost_by_model(self, days: int = 30) -> Dict[str, float]:
        """Get cost breakdown by model."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        costs = {}
        for r in self.records:
            if r.timestamp > cutoff:
                costs[r.model] = costs.get(r.model, 0) + r.cost
        return costs

    def get_cost_by_user(self, days: int = 30) -> Dict[str, float]:
        """Get cost breakdown by user."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        costs = {}
        for r in self.records:
            if r.timestamp > cutoff and r.user_id:
                costs[r.user_id] = costs.get(r.user_id, 0) + r.cost
        return costs

    def get_summary(self, days: int = 30) -> dict:
        """Get usage summary."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        period_records = [r for r in self.records if r.timestamp > cutoff]

        return {
            "period_days": days,
            "total_requests": len(period_records),
            "total_cost": sum(r.cost for r in period_records),
            "total_input_tokens": sum(r.input_tokens for r in period_records),
            "total_output_tokens": sum(r.output_tokens for r in period_records),
            "cost_by_model": self.get_cost_by_model(days),
            "avg_cost_per_request": sum(r.cost for r in period_records) / len(period_records) if period_records else 0
        }
```

### Cost Optimization Strategies

```python
class CostOptimizedClient:
    """Client with automatic cost optimization."""

    def __init__(self, cost_tracker: CostTracker):
        self.client = anthropic.Anthropic()
        self.cost_tracker = cost_tracker

    def create_message(
        self,
        optimize_cost: bool = True,
        user_id: str = None,
        **kwargs
    ):
        """Create message with optional cost optimization."""

        if optimize_cost:
            kwargs = self._optimize_request(kwargs)

        response = self.client.messages.create(**kwargs)

        # Track usage
        self.cost_tracker.record_usage(
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            user_id=user_id
        )

        return response

    def _optimize_request(self, kwargs: dict) -> dict:
        """Apply cost optimizations to request."""
        optimized = kwargs.copy()

        # 1. Use smaller model for simple tasks
        messages = kwargs.get("messages", [])
        if self._is_simple_task(messages):
            optimized["model"] = "claude-3-5-haiku-20241022"

        # 2. Reduce max_tokens if possible
        max_tokens = kwargs.get("max_tokens", 4096)
        if max_tokens > 2048 and self._likely_short_response(messages):
            optimized["max_tokens"] = 1024

        # 3. Truncate very long inputs
        optimized["messages"] = self._truncate_messages(messages, max_chars=50000)

        return optimized

    def _is_simple_task(self, messages: list) -> bool:
        """Determine if task is simple enough for Haiku."""
        if not messages:
            return True

        last_content = str(messages[-1].get("content", ""))

        # Simple task indicators
        simple_patterns = [
            "translate", "summarize briefly", "yes or no",
            "single word", "one sentence", "classify"
        ]
        return any(p in last_content.lower() for p in simple_patterns)

    def _likely_short_response(self, messages: list) -> bool:
        """Estimate if response will be short."""
        if not messages:
            return True

        last_content = str(messages[-1].get("content", ""))
        short_indicators = [
            "brief", "concise", "short", "one", "single",
            "summarize", "list 3", "list 5"
        ]
        return any(i in last_content.lower() for i in short_indicators)

    def _truncate_messages(self, messages: list, max_chars: int) -> list:
        """Truncate messages to fit within character limit."""
        total_chars = sum(len(str(m.get("content", ""))) for m in messages)

        if total_chars <= max_chars:
            return messages

        # Keep system/recent messages, truncate older ones
        truncated = []
        remaining = max_chars

        for msg in reversed(messages):
            content = str(msg.get("content", ""))
            if len(content) <= remaining:
                truncated.insert(0, msg)
                remaining -= len(content)
            else:
                # Truncate this message
                truncated.insert(0, {
                    **msg,
                    "content": content[:remaining] + "..."
                })
                break

        return truncated
```

## Security

### API Key Management

```python
import os
from cryptography.fernet import Fernet
import keyring

class SecureKeyManager:
    """Secure API key management."""

    @staticmethod
    def get_api_key() -> str:
        """Get API key from secure storage."""

        # Priority 1: Environment variable
        key = os.environ.get("ANTHROPIC_API_KEY")
        if key:
            return key

        # Priority 2: System keyring
        key = keyring.get_password("anthropic", "api_key")
        if key:
            return key

        # Priority 3: Encrypted file
        key = SecureKeyManager._read_encrypted_key()
        if key:
            return key

        raise ValueError("No API key found. Set ANTHROPIC_API_KEY or use set_api_key()")

    @staticmethod
    def set_api_key(key: str, method: str = "keyring"):
        """Store API key securely."""
        if method == "keyring":
            keyring.set_password("anthropic", "api_key", key)
        elif method == "encrypted_file":
            SecureKeyManager._write_encrypted_key(key)
        else:
            raise ValueError(f"Unknown storage method: {method}")

    @staticmethod
    def _read_encrypted_key() -> str:
        """Read encrypted key from file."""
        key_file = os.path.expanduser("~/.anthropic/key.enc")
        master_key_file = os.path.expanduser("~/.anthropic/master.key")

        if not os.path.exists(key_file) or not os.path.exists(master_key_file):
            return None

        with open(master_key_file, "rb") as f:
            master_key = f.read()

        with open(key_file, "rb") as f:
            encrypted = f.read()

        fernet = Fernet(master_key)
        return fernet.decrypt(encrypted).decode()

    @staticmethod
    def _write_encrypted_key(key: str):
        """Write encrypted key to file."""
        import os
        os.makedirs(os.path.expanduser("~/.anthropic"), exist_ok=True)

        master_key = Fernet.generate_key()
        fernet = Fernet(master_key)
        encrypted = fernet.encrypt(key.encode())

        key_file = os.path.expanduser("~/.anthropic/key.enc")
        master_key_file = os.path.expanduser("~/.anthropic/master.key")

        with open(master_key_file, "wb") as f:
            f.write(master_key)
        os.chmod(master_key_file, 0o600)

        with open(key_file, "wb") as f:
            f.write(encrypted)
        os.chmod(key_file, 0o600)
```

### Input Sanitization

```python
import re
from typing import List

class InputSanitizer:
    """Sanitize user inputs before sending to API."""

    # Patterns that might indicate prompt injection attempts
    SUSPICIOUS_PATTERNS = [
        r"ignore (previous|all|above) instructions",
        r"disregard (previous|all|above)",
        r"new instructions:",
        r"system prompt:",
        r"<\|.*\|>",  # Special tokens
    ]

    def __init__(self, max_length: int = 100000):
        self.max_length = max_length
        self.compiled_patterns = [
            re.compile(p, re.IGNORECASE)
            for p in self.SUSPICIOUS_PATTERNS
        ]

    def sanitize(self, text: str) -> str:
        """Sanitize user input."""
        # Length limit
        if len(text) > self.max_length:
            text = text[:self.max_length]

        # Remove null bytes
        text = text.replace("\x00", "")

        # Check for suspicious patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                # Log the attempt
                logging.warning(f"Suspicious pattern detected in input")
                # Optionally raise or sanitize
                # raise ValueError("Potentially malicious input detected")

        return text

    def sanitize_messages(self, messages: List[dict]) -> List[dict]:
        """Sanitize all messages."""
        sanitized = []
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                sanitized.append({
                    **msg,
                    "content": self.sanitize(content)
                })
            elif isinstance(content, list):
                # Handle content blocks
                sanitized_blocks = []
                for block in content:
                    if block.get("type") == "text":
                        sanitized_blocks.append({
                            **block,
                            "text": self.sanitize(block.get("text", ""))
                        })
                    else:
                        sanitized_blocks.append(block)
                sanitized.append({**msg, "content": sanitized_blocks})
            else:
                sanitized.append(msg)
        return sanitized
```

## Deployment Patterns

### Load Balancing

```python
import random
from typing import List

class LoadBalancedClient:
    """Client with multiple API keys for load distribution."""

    def __init__(self, api_keys: List[str]):
        self.clients = [
            anthropic.Anthropic(api_key=key)
            for key in api_keys
        ]
        self.current_index = 0

    def create_message(self, strategy: str = "round_robin", **kwargs):
        """Create message using selected load balancing strategy."""

        if strategy == "round_robin":
            client = self._round_robin()
        elif strategy == "random":
            client = self._random()
        else:
            client = self.clients[0]

        return client.messages.create(**kwargs)

    def _round_robin(self):
        """Round-robin client selection."""
        client = self.clients[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.clients)
        return client

    def _random(self):
        """Random client selection."""
        return random.choice(self.clients)
```

### Health Checks

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

class HealthChecker:
    """Health check system for Claude integration."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.last_check = None
        self.last_status = None

    def check(self) -> dict:
        """Perform health check."""
        start = datetime.utcnow()

        try:
            # Simple API call to verify connectivity
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )

            latency_ms = (datetime.utcnow() - start).total_seconds() * 1000

            self.last_check = datetime.utcnow()
            self.last_status = {
                "status": "healthy",
                "latency_ms": latency_ms,
                "timestamp": self.last_check.isoformat()
            }

        except Exception as e:
            self.last_check = datetime.utcnow()
            self.last_status = {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": self.last_check.isoformat()
            }

        return self.last_status

health_checker = HealthChecker()

@app.get("/health")
async def health_endpoint():
    """Health check endpoint."""
    return health_checker.check()

@app.get("/health/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    """Kubernetes readiness probe."""
    status = health_checker.last_status
    if status and status.get("status") == "healthy":
        return {"status": "ready"}
    return {"status": "not ready"}, 503
```

## Summary

In this chapter, you've learned:

- **Error Handling**: Comprehensive retry logic and circuit breakers
- **Rate Limiting**: Client-side rate limiting implementation
- **Monitoring**: Request logging and Prometheus metrics
- **Cost Management**: Tracking, budgeting, and optimization
- **Security**: Key management and input sanitization
- **Deployment**: Load balancing and health checks

## Key Takeaways

1. **Handle All Errors**: Implement retry logic with exponential backoff
2. **Rate Limit Proactively**: Don't wait for 429 errors
3. **Monitor Everything**: Log requests, track costs, alert on issues
4. **Secure by Default**: Protect API keys and sanitize inputs
5. **Plan for Scale**: Use circuit breakers and load balancing

## Next Steps

Now that you have production-ready patterns, let's explore Enterprise Integration in Chapter 8 for advanced security, compliance, and enterprise features.

---

**Ready for Chapter 8?** [Enterprise Integration](08-enterprise.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
