---
layout: default
title: "Chapter 7: Advanced Patterns"
nav_order: 7
parent: OpenAI Python SDK Tutorial
---

# Chapter 7: Advanced Patterns

This chapter covers production-grade resilience, observability, and cost controls.

## Retry with Exponential Backoff

```python
import random
import time
from openai import OpenAI

client = OpenAI(timeout=30.0)


def with_retry(fn, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception:
            if attempt == max_attempts:
                raise
            sleep_s = min(2 ** attempt, 20) + random.random()
            time.sleep(sleep_s)

resp = with_retry(lambda: client.responses.create(model="gpt-4.1-mini", input="health check"))
print(resp.id)
```

## Idempotent Work Units

- Generate deterministic work IDs in your app.
- Persist request/result state keyed by that ID.
- Avoid duplicate side effects during retries.

## Budget and Token Controls

- Pre-estimate tokens using tiktoken before sending.
- Cap response tokens for bounded workloads.
- Add per-tenant request quotas.

## Observability Checklist

- Log request ID, model, latency, and token usage.
- Record error class and retry count.
- Track p50/p95/p99 latency by endpoint.
- Build quality dashboards for output acceptance rates.

## Security Checklist

- Redact secrets and PII in logs.
- Restrict tool calls to allowlisted operations.
- Validate all tool-call parameters server-side.
- Isolate outbound network access for tool executors.

## Summary

You now have a practical production reliability blueprint.

Next: [Chapter 8: Integration Examples](08-integration-examples.md)
