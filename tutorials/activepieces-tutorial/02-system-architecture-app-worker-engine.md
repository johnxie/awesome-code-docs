---
layout: default
title: "Chapter 2: System Architecture: App, Worker, Engine"
nav_order: 2
parent: Activepieces Tutorial
---


# Chapter 2: System Architecture: App, Worker, Engine

Welcome to **Chapter 2: System Architecture: App, Worker, Engine**. In this part of **Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains the execution architecture that powers scale and reliability.

## Learning Goals

- understand responsibilities of app, worker, engine, and UI layers
- map queue/database dependencies to execution behavior
- identify likely bottlenecks under load spikes
- plan scaling steps without breaking flow reliability

## Architecture Summary

Activepieces separates concerns:

- app handles APIs, validation, and orchestration entrypoints
- worker pulls jobs and executes flows via the engine
- engine parses flow JSON and runs execution logic
- Postgres + Redis back persistent state and queueing behavior

## Scaling Heuristic

Start by scaling workers for execution pressure, then app replicas for ingress/API load, while keeping Redis/Postgres availability and capacity visible through monitoring.

## Source References

- [Architecture Overview](https://github.com/activepieces/activepieces/blob/main/docs/install/architecture/overview.mdx)

## Summary

You now understand the runtime surfaces that matter for production scaling decisions.

Next: [Chapter 3: Flow Design, Versioning, and Debugging](03-flow-design-versioning-and-debugging.md)

## Source Code Walkthrough

### `docker-compose.yml`

The [`docker-compose.yml`](https://github.com/activepieces/activepieces/blob/HEAD/docker-compose.yml) makes the app/worker/engine split concrete. The `AP_CONTAINER_TYPE=APP` and `AP_CONTAINER_TYPE=WORKER` environment variables confirm the two-process deployment model described in this chapter — a single image, different runtime roles. The worker service also shows `replicas: 5`, which reflects the horizontal scaling design of the execution layer.

For the broader monorepo package structure, the [`package.json`](https://github.com/activepieces/activepieces/blob/HEAD/package.json) workspace scripts (`serve:backend`, `serve:worker`, `serve:engine`) map directly to the architectural boundaries between the API, engine, and worker packages.
