---
layout: default
title: "Chapter 8: Operations, Observability, and Contribution Model"
nav_order: 8
parent: MCP Use Tutorial
---

# Chapter 8: Operations, Observability, and Contribution Model

Sustained mcp-use adoption requires explicit operational standards, observability paths, and contribution workflows.

## Learning Goals

- structure CI and runtime observability around tool-calling behavior
- separate Python and TypeScript release/testing responsibilities
- align contribution workflow with monorepo boundaries
- keep docs and examples synchronized with runtime behavior changes

## Operating Model

- keep package-level ownership clear (Python vs TypeScript)
- run focused integration tests per transport and primitive area
- centralize configuration examples to avoid copy drift
- enforce issue-first + small-PR contribution discipline

## Source References

- [Contributing Guide](https://github.com/mcp-use/mcp-use/blob/main/CONTRIBUTING.md)
- [Main README](https://github.com/mcp-use/mcp-use/blob/main/README.md)
- [TypeScript README](https://github.com/mcp-use/mcp-use/blob/main/libraries/typescript/README.md)
- [Python README](https://github.com/mcp-use/mcp-use/blob/main/libraries/python/README.md)

## Summary

You now have an end-to-end operational model for running and evolving mcp-use based systems.

Next: Continue with [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)
