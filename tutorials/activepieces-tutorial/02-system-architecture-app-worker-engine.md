---
layout: default
title: "Chapter 2: System Architecture: App, Worker, Engine"
nav_order: 2
parent: Activepieces Tutorial
---

# Chapter 2: System Architecture: App, Worker, Engine

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
