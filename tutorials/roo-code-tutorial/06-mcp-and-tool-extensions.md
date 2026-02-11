---
layout: default
title: "Chapter 6: MCP and Tool Extensions"
nav_order: 6
parent: Roo Code Tutorial
---

# Chapter 6: MCP and Tool Extensions

MCP lets Roo Code integrate with the real systems your team already operates.

## Typical Tooling Domains

- ticket/issue systems
- internal documentation and knowledge APIs
- cloud/deployment controls
- observability and incident data sources

## Tool Contract Checklist

| Area | Requirement |
|:-----|:------------|
| input schema | strict typed arguments and validation |
| output schema | structured response, not prose blobs |
| side effects | explicit read-only vs mutating class |
| errors/timeouts | deterministic handling and retry strategy |

## Rollout Pattern

1. onboard read-only tools first
2. verify output quality in real tasks
3. add mutating tools with explicit approvals
4. audit usage and remove low-signal tools

## Summary

You can now extend Roo Code into enterprise workflows while keeping operations governable.

Next: [Chapter 7: Profiles and Team Standards](07-profiles-and-team-standards.md)
