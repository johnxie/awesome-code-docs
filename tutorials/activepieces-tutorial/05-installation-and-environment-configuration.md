---
layout: default
title: "Chapter 5: Installation and Environment Configuration"
nav_order: 5
parent: Activepieces Tutorial
---

# Chapter 5: Installation and Environment Configuration

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
