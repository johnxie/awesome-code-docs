---
layout: default
title: "Chapter 7: Security Considerations"
nav_order: 7
parent: MCP Servers Tutorial
---

# Chapter 7: Security Considerations

Security is the largest gap between reference servers and production deployment.

## Start with a Threat Model

At minimum, answer:

- What can this server read?
- What can it mutate?
- What trust boundary separates model output from side effects?
- What happens if tool arguments are malicious or malformed?

## Control Layers

| Layer | Control |
|:------|:--------|
| Input validation | Strict schema + semantic checks |
| Authorization | Allowlists for paths/resources/actions |
| Execution boundary | Sandboxing and least privilege runtime |
| Change protection | Confirmation gates for destructive operations |
| Auditing | Immutable logs with actor, inputs, outputs, and outcome |

## High-Risk Patterns to Block

- unrestricted filesystem roots
- unconstrained shell/network execution behind tools
- silent mutation without user/system confirmation
- missing source-of-truth identity for requests

## Practical Security Enhancements

- classify tools by read/write/destructive and route policies accordingly
- require explicit approval for destructive or non-idempotent operations
- redact sensitive payloads in logs while preserving traceability
- enforce policy checks before tool execution, not after

## Incident Readiness

Have a runbook with:

- emergency disable switch for tool classes
- rollback strategy for unintended mutations
- artifact and log retention windows
- owner escalation path

## Summary

You now have a concrete security baseline for adapting MCP server patterns responsibly.

Next: [Chapter 8: Production Adaptation](08-production-adaptation.md)
