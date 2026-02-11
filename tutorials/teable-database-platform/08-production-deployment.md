---
layout: default
title: "Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: "Teable Database Platform"
---

# Chapter 8: Production Deployment

Production Teable deployments require coordinated application, database, and realtime operations.

## Deployment Baseline

- containerized API/frontend services
- managed PostgreSQL and cache/message infrastructure
- TLS termination and ingress policy controls
- horizontal scaling for API and websocket workers

## Operational Metrics

Track:

- p50/p95/p99 API and query latency
- websocket connection churn/reconnect rate
- workspace mutation error rates
- replication and backup health indicators

## Release and Rollback Strategy

1. stage schema migrations with backward compatibility checks
2. run canary rollout for API/websocket nodes
3. monitor error/latency deviations
4. rollback quickly on sustained regression

## Final Summary

You now have full Teable coverage from architecture to production-grade deployment and operations.

Related:
- [Teable Index](index.md)
