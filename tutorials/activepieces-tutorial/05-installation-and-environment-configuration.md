---
layout: default
title: "Chapter 5: Installation and Environment Configuration"
nav_order: 5
parent: Activepieces Tutorial
---


# Chapter 5: Installation and Environment Configuration

Welcome to **Chapter 5: Installation and Environment Configuration**. In this part of **Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on deployment configuration, environment variables, and operational setup hygiene.

## Learning Goals

- standardize deployment footprints for local and server environments
- configure database, queue, and webhook settings safely
- avoid fragile defaults in production-like contexts
- create repeatable upgrade and rollback pathways

## Configuration Priorities

| Priority | Why It Matters |
|:---------|:---------------|
| frontend/webhook URL correctness | ensures trigger/webhook reliability |
| database and redis configuration | protects execution durability and throughput |
| encryption/JWT keys | protects sensitive connection and auth data |
| execution mode and retention policies | controls runtime risk and storage behavior |

## Source References

- [Environment Variables](https://github.com/activepieces/activepieces/blob/main/docs/install/configuration/environment-variables.mdx)
- [Docker Compose Install](https://github.com/activepieces/activepieces/blob/main/docs/install/options/docker-compose.mdx)

## Summary

You now have a configuration baseline that reduces deployment and runtime misconfiguration risk.

Next: [Chapter 6: Admin Governance and AI Provider Control](06-admin-governance-and-ai-provider-control.md)

## Source Code Walkthrough

### `docker-compose.yml` and environment variable reference

Installation and environment configuration are specified in [`docker-compose.yml`](https://github.com/activepieces/activepieces/blob/HEAD/docker-compose.yml), which uses an `.env` file for secrets and operational settings. The compose file shows which environment variables are expected (`AP_CONTAINER_TYPE`, database URLs, Redis config) and how they flow into the container at startup.

The upstream docs folder contains an [environment variable reference](https://github.com/activepieces/activepieces/blob/main/docs/install/overview.mdx) that lists all supported configuration keys, their defaults, and their effects — the authoritative checklist for this chapter's configuration guidance.