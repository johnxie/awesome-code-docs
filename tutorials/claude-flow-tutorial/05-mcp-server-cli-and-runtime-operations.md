---
layout: default
title: "Chapter 5: MCP Server, CLI, and Runtime Operations"
nav_order: 5
parent: Claude Flow Tutorial
---

# Chapter 5: MCP Server, CLI, and Runtime Operations

This chapter explains day-to-day operations across MCP transport, tool registry, sessions, and CLI orchestration.

## Learning Goals

- operate MCP server transports and session controls
- map tool registration and runtime behavior to observability needs
- align CLI patterns with execution ownership in your team workflow
- avoid confusion between coordination commands and actual code execution

## Operating Pattern

Keep Claude Flow as orchestration and state-tracking infrastructure, while your executor (developer, agent, or automation runtime) performs actual code changes and command execution.

## Source References

- [@claude-flow/mcp](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/mcp/README.md)
- [AGENTS Guide](https://github.com/ruvnet/claude-flow/blob/main/AGENTS.md)
- [README](https://github.com/ruvnet/claude-flow/blob/main/README.md)

## Summary

You now have a clearer mental model for running MCP/CLI surfaces without operational ambiguity.

Next: [Chapter 6: Plugin SDK and Extensibility Patterns](06-plugin-sdk-and-extensibility-patterns.md)
