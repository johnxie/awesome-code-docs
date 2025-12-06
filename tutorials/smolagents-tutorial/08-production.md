---
layout: default
title: "Smolagents Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Smolagents Tutorial
---

# Chapter 8: Production Deployment & Operations

> Deploy smolagent-powered services with strong safety, observability, and scalability.

## Reference Architecture

- **API Layer**: FastAPI/Flask serving agent endpoints.
- **Model Backends**: HF Inference, OpenAI, Anthropic, or LiteLLM gateway.
- **Tooling Layer**: vetted tools for search, retrieval, storage.
- **State**: Redis/PostgreSQL for sessions, job queues, or audit logs.
- **Vector DB**: Chroma/Qdrant/Pinecone for retrieval (if you do RAG).
- **Observability**: metrics + tracing (Prometheus/Grafana, OpenTelemetry).

## FastAPI Skeleton

```python
from fastapi import FastAPI
from smolagents import CodeAgent, HfApiModel

agent = CodeAgent(model=HfApiModel(), tools=[], max_steps=8, verbose=False)
app = FastAPI()


@app.post("/agent/run")
async def run_agent(body: dict):
    prompt = body["prompt"]
    result = agent.run(prompt)
    return {"result": result}
```

## Security & Safety

- Enforce **auth** (API keys/JWT) at the API layer.
- Keep a **tool allowlist**; disable raw network access unless proxied.
- Limit `max_steps`, `max_tokens`, and ban dangerous imports.
- Log reasoning, tool calls, and code for **auditability**; redact PII.
- Add **human approval** for side-effectful actions (DB/file/system changes).

## Observability

- Export metrics: request latency, error rate, token usage, tool-call counts.
- Trace requests end-to-end with request IDs; sample traces for heavy paths.
- Capture code cells executed by CodeAgent in debug environments.

## Scaling

- Run behind a load balancer; make agents stateless where possible.
- Cache expensive tool results; reuse conversations via session IDs.
- Use queues (e.g., RabbitMQ/Redis) for long-running tasks.
- Horizontal scale API pods; set CPU/memory requests/limits.

## Deployment Snippet (Docker Compose)

```yaml
version: "3.8"
services:
  smolagents-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HF_API_TOKEN=${HF_API_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
```

## Production Checklist

- [ ] Auth in front of all agent endpoints
- [ ] Tool allowlists + import/network restrictions
- [ ] Metrics/tracing with dashboards and alerts
- [ ] Cost guards (rate limits, `max_steps`, `max_tokens`)
- [ ] Audit logs for prompts, tool calls, and executed code

You've shipped a safe, observable smolagents service! 🎯
