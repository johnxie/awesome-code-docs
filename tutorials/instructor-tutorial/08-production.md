---
layout: default
title: "Instructor Tutorial - Chapter 8: Production Use"
nav_order: 8
has_children: false
parent: Instructor Tutorial
---

# Chapter 8: Production Use and Operations

> Harden Instructor apps with observability, safety, cost controls, and deployment patterns.

## Overview

Take your structured-output workflows to production: secure secrets, add logging and tracing, control costs, and deploy with confidence.

## Deployment Patterns

- **Serverless (FastAPI/Functions)**: Great for bursty workloads; ensure cold-start friendly models (short prompts).
- **Containers/Kubernetes**: For steady traffic and custom gateways; pair with an API gateway for auth and rate limits.
- **Edge**: Only if your provider supports it and latency is critical; otherwise use standard runtimes for compatibility.

## Configuration and Secrets

```
# .env.production
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...
MODEL_PRIMARY=gpt-4o-mini
MODEL_FALLBACK=claude-3-opus-20240229
MAX_RETRIES=2
RATE_LIMIT_PER_MIN=120
LOG_LEVEL=info
```

Inject via your platform’s secret manager; never ship keys in the client bundle.

## Observability

```python
import logging, time

logger = logging.getLogger("instructor")
logger.setLevel(logging.INFO)

def generate():
    start = time.time()
    resp = client.responses.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Summarize Q4 metrics"}],
        response_model=Report,
    )
    logger.info(
        {
            "path": "/api/report",
            "duration_ms": int((time.time() - start) * 1000),
            "model": "gpt-4o-mini",
        }
    )
    return resp
```

- Add request IDs to correlate frontend/backends.
- Export latency, error rate, and token usage to Prometheus/Grafana or your APM.

## Safety and Guardrails

- Enforce authentication on every generation endpoint.
- Validate tool-call arguments server-side before execution.
- Reject prompts with disallowed content; add allowlists for file paths and URLs.
- Redact PII in logs; store only hashed identifiers where possible.

## Cost and Rate Control

```python
from collections import defaultdict
from datetime import datetime

token_usage = defaultdict(int)

def record_usage(user_id: str, tokens: int):
    month = datetime.utcnow().strftime("%Y-%m")
    token_usage[(user_id, month)] += tokens
```

- Set per-tenant budgets; alert when nearing limits.
- Use smaller models for classification/routing; reserve premium models for critical tasks.
- Cache stable context (FAQs, docs) to shrink prompts.

## Testing and QA

- **Unit**: Validate schemas and custom validators.
- **Contract**: Mock LLM responses; assert `ValidationError` on bad payloads.
- **E2E**: Run Playwright or Cypress against your UI; assert structured outputs render correctly.
- **Load**: Run k6/Locust to test throughput and retry behavior.

## Reliability Playbook

- Health checks on `/health` plus dependency checks (LLM provider reachability).
- Circuit breaker or fallback provider on repeated failures.
- Rollback strategy: previous container tag or serverless version; keep migrations backwards-compatible.
- Feature flags for new schemas or tools; enable per-tenant first.

## Checklist Before Go-Live

- Secrets in a manager, not in code.
- Rate limiting enabled on all generation endpoints.
- Structured logging with request IDs.
- Alerts on p95 latency, error rate, and monthly token spend.
- Automated tests pass in CI; preview environment validated by QA.

With these practices, Instructor-based apps can run safely in production while keeping structured outputs reliable and cost-efficient.
