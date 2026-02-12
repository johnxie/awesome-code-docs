---
layout: default
title: "Chapter 6: Server Deployment and API Integration"
nav_order: 6
parent: Claude Code Router Tutorial
---

# Chapter 6: Server Deployment and API Integration

This chapter covers running CCR as a service beyond local interactive usage.

## Learning Goals

- choose deployment mode based on environment constraints
- mount and manage configuration safely in containers
- use API endpoints for operational observability
- apply basic production hardening patterns

## Deployment Modes

| Mode | Use Case |
|:-----|:---------|
| local service | single-user development and experimentation |
| Docker / compose | shared team runtime and repeatability |
| reverse-proxied service | internet-facing hardened deployments |

## Source References

- [Server Deployment Docs](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/deployment.md)
- [Server API Overview](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/api/overview.md)

## Summary

You now have a practical baseline for CCR deployment and API-level operations.

Next: [Chapter 7: CI and Non-Interactive Team Workflows](07-ci-and-non-interactive-team-workflows.md)
