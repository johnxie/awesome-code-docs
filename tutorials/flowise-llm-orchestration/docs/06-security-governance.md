---
layout: default
title: "Chapter 6: Security and Governance"
nav_order: 6
has_children: false
parent: "Flowise LLM Orchestration"
---

# Chapter 6: Security and Governance

Security controls are required when orchestrating models, tools, and external data.

## Core Risk Areas

- secret leakage in node configs and logs
- unsafe tool execution with unvalidated model output
- data exfiltration via connectors

## Governance Controls

- scoped credentials per workflow/environment
- allowlisted tools and outbound domains
- policy checks for prompt and response classes
- immutable audit logs for workflow runs

## Summary

You now understand baseline security posture for Flowise workflow operations.

Next: [Chapter 7: Observability](07-observability.md)
