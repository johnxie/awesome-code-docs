---
layout: default
title: "Chapter 7: Advanced Patterns"
nav_order: 7
parent: OpenAI Python SDK Tutorial
---

# Chapter 7: Advanced Patterns

Production systems need reliability and observability defaults, not optional add-ons.

## Retry Wrapper Pattern

```python
import random
import time
from openai import OpenAI

client = OpenAI(timeout=30.0)

def with_retry(fn, attempts=5):
    for i in range(1, attempts + 1):
        try:
            return fn()
        except Exception:
            if i == attempts:
                raise
            time.sleep(min(2 ** i, 20) + random.random())

resp = with_retry(lambda: client.responses.create(model="gpt-5.2", input="health check"))
print(resp.id)
```

## Observability Minimum Set

- request id
- model id
- latency
- token usage
- retry count
- error class

## Cost Control Tactics

- estimate token budgets before request
- cap max output size where possible
- cache deterministic intermediate artifacts
- route low-stakes requests to smaller/cheaper models

## Summary

You now have practical building blocks for resilient, cost-aware, and debuggable SDK services.

Next: [Chapter 8: Integration Examples](08-integration-examples.md)
