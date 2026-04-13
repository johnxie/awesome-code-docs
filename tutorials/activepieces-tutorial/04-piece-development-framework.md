---
layout: default
title: "Chapter 4: Piece Development Framework"
nav_order: 4
parent: Activepieces Tutorial
---


# Chapter 4: Piece Development Framework

Welcome to **Chapter 4: Piece Development Framework**. In this part of **Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how to extend Activepieces through custom TypeScript pieces.

## Learning Goals

- understand piece lifecycle: definition, auth, action, trigger
- set up local piece development efficiently
- apply piece versioning rules for backward compatibility
- contribute pieces without destabilizing existing flows

## Piece Development Path

1. set up local dev environment and start the platform
2. define piece metadata and authentication
3. add actions and triggers incrementally
4. test behavior in local flow runs
5. version and publish with explicit compatibility intent

## Source References

- [Build Pieces Overview](https://github.com/activepieces/activepieces/blob/main/docs/build-pieces/building-pieces/overview.mdx)
- [Development Setup](https://github.com/activepieces/activepieces/blob/main/docs/build-pieces/building-pieces/development-setup.mdx)
- [Start Building](https://github.com/activepieces/activepieces/blob/main/docs/build-pieces/building-pieces/start-building.mdx)
- [Piece Versioning](https://github.com/activepieces/activepieces/blob/main/docs/build-pieces/piece-reference/piece-versioning.mdx)

## Summary

You now have an extensibility workflow that balances speed with compatibility discipline.

Next: [Chapter 5: Installation and Environment Configuration](05-installation-and-environment-configuration.md)

## Source Code Walkthrough

### `packages/pieces` (piece SDK)

Custom piece development centers on the `packages/pieces` directory of the upstream monorepo. Each subdirectory is a published piece package that exports actions and triggers using the Activepieces piece SDK (`@activepieces/pieces-framework`).

To understand the full piece lifecycle, browse any built-in piece (for example, `packages/pieces/community/http`) to see how authentication, actions, and triggers are defined. The [`packages/pieces/community/http/src/index.ts`](https://github.com/activepieces/activepieces/blob/main/packages/pieces/community/http/src/index.ts) entry point shows the minimal shape every piece must follow.