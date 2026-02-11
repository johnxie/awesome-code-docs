---
layout: default
title: "Chapter 7: Observability"
nav_order: 7
has_children: false
parent: "Flowise LLM Orchestration"
---

# Chapter 7: Observability

Observability turns visual workflow orchestration into measurable production behavior.

## Metrics Baseline

Track at least:

- workflow latency (p50/p95/p99)
- node-level error and retry rates
- model token usage and cost per run
- connector dependency latency/failure rates

## Trace Strategy

Use a single run ID from entrypoint to final output.

Per node, capture:

- start/end timestamps
- node type and version
- safe metadata for inputs/outputs
- retry and fallback path taken

This allows fast root-cause analysis for partial failures.

## Logging Standards

- redact secrets and sensitive payload fields
- keep structured logs (JSON) for machine querying
- include policy decisions (allowed/blocked/escalated)

## Alerting Rules

| Alert | Trigger |
|:------|:--------|
| latency regression | p95 exceeds SLO threshold |
| failure burst | node error rate spike |
| cost anomaly | run cost deviates from baseline |
| dependency outage | repeated connector timeout/failures |

## Summary

You can now instrument Flowise workflows to debug incidents quickly and manage performance/cost predictably.

Next: [Chapter 8: Extension Ecosystem](08-extension-ecosystem.md)
