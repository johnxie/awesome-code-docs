---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Activepieces Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter provides a fast path to first workflow value with minimal setup overhead.

## Learning Goals

- choose an installation path that matches your current stage
- run the platform locally and validate a first flow
- understand where key operational settings live
- establish a reproducible team onboarding baseline

## Fast Start Workflow

1. start from the [Install Overview](https://github.com/activepieces/activepieces/blob/main/docs/install/overview.mdx)
2. choose Docker or Docker Compose for first-run setup
3. validate platform startup and account access
4. create one simple trigger-action flow
5. capture setup and validation notes in a short team runbook

## Source References

- [Install Overview](https://github.com/activepieces/activepieces/blob/main/docs/install/overview.mdx)
- [Docker Compose Setup](https://github.com/activepieces/activepieces/blob/main/docs/install/options/docker-compose.mdx)

## Summary

You now have a working baseline for expanding Activepieces usage safely.

Next: [Chapter 2: System Architecture: App, Worker, Engine](02-system-architecture-app-worker-engine.md)

## Source Code Walkthrough

### `docker-compose.yml`

The [`docker-compose.yml`](https://github.com/activepieces/activepieces/blob/HEAD/docker-compose.yml) file is the primary reference for getting started with Activepieces locally. It defines the app, worker, postgres, and redis service configuration that Chapter 1 walks through — including port mapping, environment variable injection via `.env`, and the `AP_CONTAINER_TYPE` variable that determines whether a container runs as the main app or a background worker.

Review this file alongside the [install overview docs](https://github.com/activepieces/activepieces/blob/main/docs/install/overview.mdx) to understand the minimal setup required before creating your first flow.
