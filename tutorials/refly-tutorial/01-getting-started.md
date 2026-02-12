---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Refly Tutorial
---

# Chapter 1: Getting Started

This chapter establishes a local Refly baseline for experimentation and integration.

## Learning Goals

- install runtime prerequisites for local development
- run middleware and application services
- verify baseline web/API availability
- identify fastest path for first workflow execution

## Local Dev Bootstrap

```bash
docker compose -f deploy/docker/docker-compose.middleware.yml -p refly up -d
corepack enable
pnpm install
pnpm copy-env:develop
pnpm build
pnpm dev
```

## First Validation Checklist

- middleware containers are healthy
- web app is reachable at `http://localhost:5173`
- API responds after startup
- you can create and run a simple workflow

## Source References

- [README Quick Start](https://github.com/refly-ai/refly/blob/main/README.md#quick-start)
- [Contributing: Developing API and Web](https://github.com/refly-ai/refly/blob/main/CONTRIBUTING.md#developing-api-and-web)

## Summary

You now have a baseline local environment for running Refly workflows.

Next: [Chapter 2: Architecture and Component Topology](02-architecture-and-component-topology.md)
