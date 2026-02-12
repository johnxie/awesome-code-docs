---
layout: default
title: "Chapter 3: Agent Configuration, Tool Governance, and Memory"
nav_order: 3
parent: MCP Use Tutorial
---

# Chapter 3: Agent Configuration, Tool Governance, and Memory

Agent reliability depends on explicit control of tools, memory, and step budgets.

## Learning Goals

- configure `MCPAgent` with practical limits (`maxSteps`, memory)
- apply `disallowedTools` to reduce unsafe or irrelevant tool use
- use server-manager patterns for multi-server environments
- align LLM selection with tool-calling support expectations

## Governance Pattern

1. start with minimal tool surface
2. explicitly block dangerous categories unless needed
3. set conservative step limits first
4. monitor behavior before widening capability scope

## Source References

- [TypeScript Agent Configuration](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/agent/agent-configuration.mdx)
- [Python Agent Configuration](https://github.com/mcp-use/mcp-use/blob/main/docs/python/agent/agent-configuration.mdx)
- [Python README - Agent examples](https://github.com/mcp-use/mcp-use/blob/main/libraries/python/README.md)

## Summary

You now have agent-level guardrails for safer, more predictable tool execution.

Next: [Chapter 4: TypeScript Server Framework and UI Widgets](04-typescript-server-framework-and-ui-widgets.md)
