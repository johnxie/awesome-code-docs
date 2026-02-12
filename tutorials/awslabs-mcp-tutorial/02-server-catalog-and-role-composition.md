---
layout: default
title: "Chapter 2: Server Catalog and Role Composition"
nav_order: 2
parent: awslabs/mcp Tutorial
---

# Chapter 2: Server Catalog and Role Composition

This chapter explains how to navigate and compose capabilities from a large server catalog.

## Learning Goals

- map server choices to concrete job-to-be-done categories
- avoid loading unnecessary servers and tools for each workflow
- use role-based composition patterns where available
- keep context and tool surface area intentionally constrained

## Selection Heuristic

Start with the smallest server set that satisfies your workflow. Expand only when a measurable capability gap appears. More servers is not automatically better.

## Source References

- [Repository README Catalog](https://github.com/awslabs/mcp/blob/main/README.md)
- [Core MCP Server README](https://github.com/awslabs/mcp/blob/main/src/core-mcp-server/README.md)
- [Samples Overview](https://github.com/awslabs/mcp/blob/main/samples/README.md)

## Summary

You now have a strategy for selecting servers without overwhelming client context.

Next: [Chapter 3: Transport and Client Integration Patterns](03-transport-and-client-integration-patterns.md)
