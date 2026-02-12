---
layout: default
title: "Chapter 4: Tools, MCP, and Confirmation Flows"
nav_order: 4
parent: ADK Python Tutorial
---

# Chapter 4: Tools, MCP, and Confirmation Flows

This chapter explains how to safely expose external capabilities to ADK agents.

## Learning Goals

- use Python tools and OpenAPI/MCP integrations
- gate risky tool actions with confirmation flows
- build safer human-in-the-loop controls
- reduce runtime surprises from tool misuse

## Tooling Categories in ADK

- Python function tools
- OpenAPI-based tools
- MCP-based tools
- Google ecosystem connectors

## Confirmation Strategy

For tools with side effects, add explicit confirmation requirements before execution. This keeps the agent useful while reducing accidental writes or external operations.

## Source References

- [ADK Tools Docs](https://google.github.io/adk-docs/tools/)
- [ADK MCP Tools Docs](https://google.github.io/adk-docs/tools/mcp-tools/)
- [ADK Tool Confirmation Docs](https://google.github.io/adk-docs/tools/confirmation/)

## Summary

You now have a practical pattern for shipping tool-enabled ADK agents with stronger safety defaults.

Next: [Chapter 5: Sessions, Memory, and Context Management](05-sessions-memory-and-context-management.md)
