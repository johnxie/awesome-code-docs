---
layout: default
title: "Chapter 6: Observability, Deployment, and Operations"
nav_order: 6
parent: Refly Tutorial
---

# Chapter 6: Observability, Deployment, and Operations

This chapter covers operating Refly with visibility into metrics, traces, logs, and deployment surfaces.

## Learning Goals

- run local observability stack for deeper runtime debugging
- correlate workflow behavior across traces, logs, and metrics
- understand deployment artifacts for self-hosted operations
- establish operational baselines before scaling usage

## Operations Building Blocks

| Domain | Key Assets |
|:-------|:-----------|
| deployment | `deploy/docker/docker-compose*.yml` |
| runtime telemetry | `deploy/docker/trace/` stack (Grafana, Prometheus, Tempo, Loki) |
| API verification | OpenAPI status/output endpoints |
| workload stability | middleware health + execution history |

## Trace Stack Quick Start

```bash
cd deploy/docker/trace
docker-compose up -d
```

Then verify data flow in Grafana and API checks before diagnosing workflow-level behavior.

## Source References

- [Trace Stack README](https://github.com/refly-ai/refly/blob/main/deploy/docker/trace/README.md)
- [Docker Deployment Assets](https://github.com/refly-ai/refly/tree/main/deploy/docker)
- [OpenAPI Guide](https://github.com/refly-ai/refly/blob/main/docs/en/guide/api/openapi.md)

## Summary

You now have a baseline operational model for running Refly beyond local experimentation.

Next: [Chapter 7: Troubleshooting, Safety, and Cost Controls](07-troubleshooting-safety-and-cost-controls.md)
