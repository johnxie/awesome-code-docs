---
layout: default
title: "Chapter 6: Deployment and Observability Patterns"
nav_order: 6
parent: GenAI Toolbox Tutorial
---

# Chapter 6: Deployment and Observability Patterns

This chapter explains runtime deployment options and telemetry controls.

## Learning Goals

- deploy Toolbox with Docker Compose and containerized workflows
- configure network and host controls explicitly
- enable telemetry export modes deliberately
- prepare observability baselines before production traffic

## Deployment Baseline

Use pinned image versions, explicit host/origin settings, and telemetry destinations from day one. Treat local defaults as development conveniences, not production policy.

## Source References

- [Deploy using Docker Compose](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/how-to/deploy_docker.md)
- [CLI Reference](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/reference/cli.md)
- [Telemetry Concepts](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/concepts/telemetry/index.md)

## Summary

You now have a deployment model that balances speed with operational controls.

Next: [Chapter 7: CLI, Testing, and Development Workflow](07-cli-testing-and-development-workflow.md)
