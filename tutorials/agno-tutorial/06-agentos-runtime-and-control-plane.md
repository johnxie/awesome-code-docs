---
layout: default
title: "Chapter 6: AgentOS Runtime and Control Plane"
nav_order: 6
parent: Agno Tutorial
---

# Chapter 6: AgentOS Runtime and Control Plane

AgentOS provides runtime and control-plane support for operating Agno systems in production.

## Runtime Concerns

| Concern | Practice |
|:--------|:---------|
| deployment topology | isolate workloads by environment and risk |
| execution state | durable storage and recovery strategy |
| control-plane access | strict auth and role boundaries |

## Control Plane Playbook

1. define service ownership and SLOs
2. expose key runtime metrics and traces
3. establish rollback and emergency stop procedures

## Source References

- [AgentOS Introduction](https://docs.agno.com/agent-os/introduction)
- [Agno Production Overview](https://docs.agno.com/production/overview)

## Summary

You now have an operational model for running Agno via AgentOS infrastructure.

Next: [Chapter 7: Guardrails, Evals, and Observability](07-guardrails-evals-and-observability.md)
