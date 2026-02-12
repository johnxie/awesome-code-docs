---
layout: default
title: "Chapter 2: Registry Architecture and Data Flow"
nav_order: 2
parent: MCP Registry Tutorial
---

# Chapter 2: Registry Architecture and Data Flow

The registry is a lightweight metadata service: publishers write versioned data, consumers read and cache it.

## Learning Goals

- map core components (API, DB, CLI, CDN)
- understand publication and discovery flows
- locate critical source areas for extension work
- reason about cache and polling expectations

## System Components

| Component | Primary Role |
|:----------|:-------------|
| Go API | read/write endpoints, auth flows, validation |
| PostgreSQL | versioned metadata, auth state, verification data |
| CDN layer | cache public read endpoints globally |
| `mcp-publisher` CLI | publisher entrypoint for auth and publish workflows |

## Data Flow Principle

Publish once to canonical metadata; downstream clients and aggregators consume via API and maintain their own caches.

## Source References

- [Registry README - Architecture](https://github.com/modelcontextprotocol/registry/blob/main/README.md#architecture)
- [Technical Architecture](https://github.com/modelcontextprotocol/registry/blob/main/docs/design/tech-architecture.md)
- [Design Principles](https://github.com/modelcontextprotocol/registry/blob/main/docs/design/design-principles.md)

## Summary

You now have a system-level model for registry behavior.

Next: [Chapter 3: server.json Schema and Package Verification](03-server-json-schema-and-package-verification.md)
