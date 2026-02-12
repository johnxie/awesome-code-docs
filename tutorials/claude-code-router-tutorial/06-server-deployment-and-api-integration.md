---
layout: default
title: "Chapter 6: Server Deployment and API Integration"
nav_order: 6
parent: Claude Code Router Tutorial
---

# Chapter 6: Server Deployment and API Integration

This chapter covers deploying CCR server for local teams and service-oriented usage.

## Learning Goals

- choose local vs Docker deployment modes
- mount and manage configuration safely in containers
- expose and monitor core API surfaces
- apply production deployment hygiene

## Deployment Building Blocks

| Area | Key Artifact |
|:-----|:-------------|
| container deployment | Docker image / compose patterns |
| configuration management | mounted `config.json` and env interpolation |
| API surface | config and log endpoints |
| production hardening | reverse proxy + HTTPS + health checks |

## Source References

- [Server Deployment Guide](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/deployment.md)
- [Server API Overview](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/api/overview.md)
- [README](https://github.com/musistudio/claude-code-router/blob/main/README.md)

## Summary

You now have a baseline for running CCR as an operational service.

Next: [Chapter 7: GitHub Actions, Non-Interactive Mode, and Team Ops](07-github-actions-non-interactive-mode-and-team-ops.md)
