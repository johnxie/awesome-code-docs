---
layout: default
title: "Chapter 6: Admin Governance and AI Provider Control"
nav_order: 6
parent: Activepieces Tutorial
---


# Chapter 6: Admin Governance and AI Provider Control

Welcome to **Chapter 6: Admin Governance and AI Provider Control**. In this part of **Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers platform admin capabilities for organizational control and AI-provider governance.

## Learning Goals

- apply role, project, and piece governance controls effectively
- configure AI providers for shared org usage safely
- support cost visibility and policy enforcement via AI gateways
- keep admin operations auditable and repeatable

## Governance Areas

- project and user management boundaries
- piece availability controls per organization context
- SSO/security settings and policy alignment
- centralized AI provider configuration and logging practices

## Source References

- [Admin Overview](https://github.com/activepieces/activepieces/blob/main/docs/admin-guide/overview.mdx)
- [Setup AI Providers](https://github.com/activepieces/activepieces/blob/main/docs/admin-guide/guides/setup-ai-providers.mdx)

## Summary

You now have an admin-level operating model for controlling platform risk and shared AI usage.

Next: [Chapter 7: API Automation and Embedding Patterns](07-api-automation-and-embedding-patterns.md)

## Source Code Walkthrough

### `packages/server/api` (admin and platform modules)

Admin governance features live in the `packages/server/api` package. Look for modules related to `platform`, `user`, `project`, and `ai-provider` to see how role enforcement, piece allowlists, and AI provider configuration are implemented server-side.

The platform settings and AI provider endpoints define exactly which governance knobs are available programmatically — useful for automating governance policy rollout across projects as described in this chapter.