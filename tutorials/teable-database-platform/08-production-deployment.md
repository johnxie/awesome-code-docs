---
layout: default
title: "Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: "Teable Database Platform"
---

# Chapter 8: Production Deployment

This chapter covers production hardening for Teable-based deployments.

## Deployment Baseline

- containerized backend/frontend split
- managed PostgreSQL and Redis with backups
- TLS termination and ingress controls
- horizontal scaling for API and websocket nodes

## Observability Baseline

- p50/p95/p99 query latency by endpoint
- websocket connection churn and reconnects
- workspace-level mutation error rates
- replication/backup health signals

## Final Summary

You now have complete Teable coverage from system architecture to production operations.

Related:
- [Teable Index](index.md)
