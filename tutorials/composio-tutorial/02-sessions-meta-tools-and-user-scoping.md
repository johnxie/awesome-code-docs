---
layout: default
title: "Chapter 2: Sessions, Meta Tools, and User Scoping"
nav_order: 2
parent: Composio Tutorial
---

# Chapter 2: Sessions, Meta Tools, and User Scoping

This chapter explains the core operational model: user-scoped sessions with meta tools that discover and execute capabilities dynamically.

## Learning Goals

- understand why Composio uses session-scoped meta tools
- map user IDs to connected accounts and execution context
- control discoverability boundaries for safer tool use
- avoid context overload from indiscriminate tool loading

## Core Model

Composio sessions expose meta tools such as `COMPOSIO_SEARCH_TOOLS`, `COMPOSIO_MANAGE_CONNECTIONS`, and execution/workbench helpers. Instead of preloading hundreds of raw tools, agents discover and call what they need at runtime.

This model improves scalability and reduces prompt/tool context bloat while preserving user-specific auth and permissions.

## Design Guardrails

| Design Choice | Recommendation |
|:--------------|:---------------|
| User identity | use stable app-level user IDs, not transient request IDs |
| Session scope | restrict discoverable toolkits for narrower workloads |
| Connection handling | keep connected account lifecycle auditable |
| Catalog browsing | inspect tool schemas before enabling broad access |

## Source References

- [Tools and Toolkits](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-and-toolkits.mdx)
- [Fetching Tools and Toolkits](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/toolkits/fetching-tools-and-toolkits.mdx)
- [Users and Sessions](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/users-and-sessions.mdx)

## Summary

You now understand the session-centric model that underpins scalable Composio deployments.

Next: [Chapter 3: Provider Integrations and Framework Mapping](03-provider-integrations-and-framework-mapping.md)
