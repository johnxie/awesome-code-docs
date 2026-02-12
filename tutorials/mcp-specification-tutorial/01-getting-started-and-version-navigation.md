---
layout: default
title: "Chapter 1: Getting Started and Version Navigation"
nav_order: 1
parent: MCP Specification Tutorial
---

# Chapter 1: Getting Started and Version Navigation

This chapter defines a reliable way to choose and track MCP protocol revisions.

## Learning Goals

- identify the canonical source of protocol requirements
- select a versioning strategy for client/server compatibility
- map spec revision docs to implementation backlog tasks
- avoid mixing stale transport or auth behavior from older revisions

## Practical Versioning Workflow

1. lock your implementation baseline to a specific protocol revision (for example `2025-11-25`)
2. document which revision each SDK in your stack currently targets
3. check the spec changelog before adding new capabilities (tasks, elicitation modes, scope flows)
4. treat revision upgrades as planned change windows, not ad-hoc refactors

## Minimum Source Map

- `docs/specification/<revision>/index.mdx` for authoritative behavior
- `schema/<revision>/schema.ts` and generated schema for machine validation
- `docs/specification/<revision>/changelog.mdx` for delta review
- `docs/development/roadmap.mdx` for upcoming protocol priorities

## Source References

- [Specification 2025-11-25 Index](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/index.mdx)
- [Schema 2025-11-25 (TypeScript)](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-11-25/schema.ts)
- [Key Changes vs 2025-06-18](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)
- [Development Roadmap](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/development/roadmap.mdx)

## Summary

You now have a revision-first process that keeps implementation decisions aligned with the protocol source of truth.

Next: [Chapter 2: Architecture and Capability Negotiation](02-architecture-and-capability-negotiation.md)
