---
layout: default
title: "Chapter 6: Observability and Security"
nav_order: 6
parent: Langflow Tutorial
---

# Chapter 6: Observability and Security

Langflow production usage requires strong observability and strict security boundaries.

## Security Baseline

- keep Langflow version current for advisory fixes
- use environment and secret segregation
- enforce endpoint auth for API/MCP surfaces
- restrict access to administrative control paths

## Observability Baseline

| Signal | Why It Matters |
|:-------|:---------------|
| flow success rate | quality and runtime stability |
| node latency | bottleneck diagnosis |
| tool error rate | integration health |
| auth failures | abuse and misconfiguration detection |

## Source References

- [Langflow Security Advisories](https://github.com/langflow-ai/langflow/security/advisories)
- [Langflow Security Policy](https://github.com/langflow-ai/langflow/blob/main/SECURITY.md)

## Summary

You now have a security and telemetry baseline for operating Langflow safely.

Next: [Chapter 7: Custom Components and Extensions](07-custom-components-and-extensions.md)
