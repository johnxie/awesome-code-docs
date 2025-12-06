---
layout: default
title: "Semantic Kernel Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 8: Production Deployment & Operations

> Deploy Semantic Kernel-based apps with scalable architecture, Kubernetes manifests, security, and observability.

## Reference Architecture

- **API Gateway / Ingress**: auth, rate limiting, routing.
- **App Service**: your API (FastAPI/ASP.NET) hosting SK kernels and plugins.
- **AI Providers**: OpenAI, Azure OpenAI, local models.
- **Vector DB**: Chroma/Qdrant/Pinecone for memory.
- **Cache/Queue**: Redis/RabbitMQ for session state and jobs.
- **Observability**: Prometheus/Grafana, OpenTelemetry tracing.

## FastAPI Integration (Python)

```python
from fastapi import FastAPI, Depends
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


def build_kernel() -> sk.Kernel:
    k = sk.Kernel()
    k.add_service(OpenAIChatCompletion("chat", ai_model_id="gpt-4o"))
    # register plugins, memory, etc.
    return k


app = FastAPI()
kernel = build_kernel()


@app.post("/summarize")
async def summarize(body: dict, k: sk.Kernel = Depends(lambda: kernel)):
    summarize_fn = k.create_function_from_prompt(
        "summarize",
        "Writer",
        prompt="Summarize in 3 bullets:\n{{$input}}",
    )
    result = await k.invoke(summarize_fn, input=body["text"])
    return {"result": str(result)}
```

## Kubernetes (excerpt)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sk-api
  namespace: semantic-kernel
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app: sk-api
  template:
    metadata:
      labels:
        app: sk-api
    spec:
      containers:
      - name: api
        image: your-registry/sk-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef: { name: sk-secrets }
        - configMapRef: { name: sk-config }
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "1000m"
            memory: "2Gi"
        livenessProbe:
          httpGet: { path: /health, port: 8000 }
          initialDelaySeconds: 30
        readinessProbe:
          httpGet: { path: /ready, port: 8000 }
          initialDelaySeconds: 10
```

## Security

- Store secrets in **Kubernetes Secrets** or a vault; never bake into images.
- Enforce **authN/Z** at the gateway (JWT, API keys, IP allowlists).
- Add **rate limiting** and **request size limits** to protect models.
- Redact sensitive fields in logs; encrypt data at rest for vector stores.

## Observability & SRE

- Export **metrics**: latency, tokens, errors per provider; queue depth; cache hit rate.
- Enable **tracing** for prompt + tool calls; propagate request IDs end-to-end.
- Set **budgets**: cost per request/session; alert on anomalies.
- Add **chaos tests** for provider outages and slowdowns.

## Performance & Cost

- Use **connection pooling** and **async IO** to reduce overhead.
- Prefer **cheaper models** for drafting; promote to larger models for finalization.
- Warm up models/functions during deploy; cache embeddings and retrieval results.

## Deployment Checklist

- [ ] Containerized API with SK kernel and plugins
- [ ] Secrets managed via vault/Secrets; configs via ConfigMap/env
- [ ] Health probes, HPA, and rolling updates configured
- [ ] Metrics + tracing exported and dashboards/alerts in place
- [ ] Cost and rate limits enforced per provider

You're production-ready! 🎯
