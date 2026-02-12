---
layout: default
title: "Chapter 5: CLI and Self-Hosted Deployment"
nav_order: 5
parent: Sweep Tutorial
---

# Chapter 5: CLI and Self-Hosted Deployment

Sweep supports local CLI workflows and self-hosted GitHub app deployments for teams with tighter control requirements.

## Learning Goals

- choose between hosted app, local CLI, and self-hosted deployment
- understand key dependencies and environment assumptions
- define rollout criteria for private infrastructure

## Deployment Modes

| Mode | Best For |
|:-----|:---------|
| hosted GitHub app | fastest adoption with minimal ops overhead |
| Sweep CLI | local runs and experimentation |
| self-hosted Docker app | enterprise network and data-control requirements |

## CLI Bootstrap

```bash
pip install sweepai
sweep init
sweep run https://github.com/ORG/REPO/issues/1
```

## Self-Hosted Highlights

- create GitHub app and webhook configuration
- manage OpenAI/Anthropic credentials in `.env`
- deploy backend with Docker Compose
- configure webhook URL and monitor long-running tasks

## Source References

- [CLI Docs](https://github.com/sweepai/sweep/blob/main/docs/pages/cli.mdx)
- [Deployment Docs](https://github.com/sweepai/sweep/blob/main/docs/pages/deployment.mdx)

## Summary

You now have a mode-selection model for operating Sweep in different risk and compliance contexts.

Next: [Chapter 6: Search, Planning, and Execution Patterns](06-search-planning-and-execution-patterns.md)
