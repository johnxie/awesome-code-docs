---
layout: default
title: "Chapter 5: Logging, Progress, Elicitation, and Tasks"
nav_order: 5
parent: MCP C# SDK Tutorial
---

# Chapter 5: Logging, Progress, Elicitation, and Tasks

This chapter covers advanced capability flows that usually fail first in production.

## Learning Goals

- configure logging and level controls for host/client observability
- implement progress updates for long-running tool operations
- use form and URL elicitation paths safely
- design durable task workflows and task stores

## Capability Guidance

- logging: map SDK log levels to your centralized .NET logging pipeline
- progress: emit meaningful milestones, not noisy micro-events
- elicitation: reserve URL mode for flows needing out-of-band trust boundaries
- tasks: use durable task store implementations for restart resilience

## Source References

- [Logging Concepts](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/logging/logging.md)
- [Progress Concepts](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/progress/progress.md)
- [Elicitation Concepts](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/elicitation/elicitation.md)
- [Tasks Concepts](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/tasks/tasks.md)
- [Long Running Tasks Sample](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/LongRunningTasks/README.md)

## Summary

You now have a plan for operating advanced MCP capability flows with better durability and control.

Next: [Chapter 6: OAuth-Protected MCP Servers and Clients](06-oauth-protected-mcp-servers-and-clients.md)
