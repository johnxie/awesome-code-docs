---
layout: default
title: "Chapter 8: Production Deployment"
parent: "Firecrawl Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Package, secure, and operate Firecrawl-based pipelines in production.

## Objectives
- Containerize workers and queues
- Deploy on Kubernetes with autoscaling
- Secure credentials and traffic
- Add observability for reliability

## Containerization (Dockerfile sketch)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "worker.py"]
```

## Kubernetes Essentials
- Deployment for workers; HPA on CPU/RAM
- Job/Queue backend (e.g., Redis, RabbitMQ, SQS)
- ConfigMaps for non-secret config; Secrets for API keys
- PodDisruptionBudgets to keep capacity during maintenance

## Ingress & Security
- Enforce HTTPS; WAF where applicable
- Rate limit public endpoints
- Rotate API keys; scoped least-privilege access

## Observability
- Metrics: success/error rates, latency, cost per scrape
- Logs: structured JSON; include domain, status, duration
- Traces: instrument scraping and embedding pipelines

## Backup & Recovery
- Persist vector stores; snapshot on schedule
- Backup job queue state if durable
- Run disaster-recovery drills (restore embeddings, requeue jobs)

## Reliability Runbook
- Common failures: 429/403 spikes, render timeouts, queue backlog
- Standard mitigations: reduce concurrency, pause high-failure domains, scale workers
- On-call checklist: dashboards, recent deploys, error budgets

## Go-Live Checklist
- [ ] Secrets stored in manager (KMS/SSM)
- [ ] Alerts configured (429, 5xx, latency, queue depth)
- [ ] Autoscaling tested under load
- [ ] Backups validated
- [ ] Runbook documented and accessible

## Next Steps
Proceed to observability and continuous improvements—evaluate retrieval quality and latency regularly.
