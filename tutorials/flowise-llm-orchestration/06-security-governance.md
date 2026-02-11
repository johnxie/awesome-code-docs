---
layout: default
title: "Chapter 6: Security and Governance"
nav_order: 6
has_children: false
parent: "Flowise LLM Orchestration"
---

# Chapter 6: Security and Governance

Flowise workflows combine models, tools, connectors, and credentials. Governance must be explicit.

## Primary Risk Areas

- secrets exposed in node configs or logs
- unsafe tool execution from unvalidated model outputs
- data exfiltration through permissive connectors
- tenant boundary violations in shared deployments

## Security Control Layers

| Layer | Required Control |
|:------|:-----------------|
| Credential handling | scoped secrets per environment/workflow |
| Tool invocation | input validation + allowlists |
| Data access | least privilege for connectors and stores |
| Network egress | outbound domain and protocol restrictions |
| Audit | immutable run-level logs with redaction |

## Governance Process

1. classify workflow risk level (read-only vs mutating)
2. require reviews for prompt/node changes on high-risk flows
3. version workflow definitions and policies together
4. enforce release gates before production promotion

## Runtime Safeguards

- timeout budgets per node
- bounded retry policies
- explicit human approval for destructive actions
- deny-by-default for new external tool integrations

## Incident Readiness

Maintain playbooks for:

- secret leakage response
- unsafe automation rollback
- connector compromise or abuse
- tenant-isolation incidents

## Summary

You now have a practical security and governance baseline for operating Flowise in production.

Next: [Chapter 7: Observability](07-observability.md)
