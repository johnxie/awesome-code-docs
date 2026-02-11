---
layout: default
title: "Chapter 6: Integrations and MCP"
nav_order: 6
parent: Bolt.diy Tutorial
---

# Chapter 6: Integrations and MCP

bolt.diy can connect to external systems through provider APIs and MCP-oriented tool paths.

## Integration Domains

- model providers and gateways
- deployment targets
- backend/data services
- MCP-style external tools

## Tool Contract Standards

| Contract Area | Requirement |
|:--------------|:------------|
| inputs | strict schema validation |
| outputs | structured, machine-readable results |
| side effects | declared mutating vs read-only class |
| reliability | timeout, retry, and fallback behavior |

## Rollout Pattern

1. start with read-only integrations
2. validate outputs in real workflows
3. add mutating tools behind explicit approvals
4. monitor and prune low-value integrations

## Governance Boundaries

- isolate credentials per environment and integration
- log all mutating tool calls with actor + timestamp
- define emergency disable switches for unstable connectors

## Summary

You can now treat bolt.diy integrations as governed platform components.

Next: [Chapter 7: Deployment and Distribution](07-deployment-distribution.md)
