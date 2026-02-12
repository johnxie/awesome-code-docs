---
layout: default
title: "Chapter 4: Tools, Prompts, Resources, and Filter Pipelines"
nav_order: 4
parent: MCP C# SDK Tutorial
---

# Chapter 4: Tools, Prompts, Resources, and Filter Pipelines

Filter pipelines are a major differentiator in the C# SDK for cross-cutting control.

## Learning Goals

- define tools/prompts/resources with clear metadata and constraints
- apply request-specific and message-level filters correctly
- order filters to enforce authorization and observability goals
- avoid hidden behavior interactions between filters and handlers

## Filter Design Rules

| Filter Type | Best Use |
|:------------|:---------|
| request-specific filters | validate/transform behavior for one primitive category |
| incoming message filters | protocol-level interception before handler dispatch |
| outgoing message filters | response/notification shaping and telemetry |

## Source References

- [Filter Concepts](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/filters.md)
- [C# SDK README - Tool/Prompt/Resource Examples](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md)
- [Core README - Server APIs](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.Core/README.md)

## Summary

You now have an extensibility model for primitives and filters that stays predictable under growth.

Next: [Chapter 5: Logging, Progress, Elicitation, and Tasks](05-logging-progress-elicitation-and-tasks.md)
