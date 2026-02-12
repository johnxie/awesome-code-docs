---
layout: default
title: "Chapter 5: Tool Execution Modes and Modifiers"
nav_order: 5
parent: Composio Tutorial
---

# Chapter 5: Tool Execution Modes and Modifiers

This chapter explains how to choose execution mode and when to apply schema/before/after modifiers.

## Learning Goals

- compare chat-completion, agentic-framework, and direct execution paths
- understand where tool-call loops are owned in each path
- use modifiers to enforce safer inputs and cleaner outputs
- decide when proxy execution or custom tools are appropriate

## Execution Modes

| Mode | Best For |
|:-----|:---------|
| chat completion providers | explicit control over tool loop and response handling |
| agentic frameworks | framework-managed plan/act loops with Composio tool objects |
| direct execution | deterministic backend jobs and non-LLM automation |
| proxy execution | calling supported toolkit endpoints not exposed as predefined tools |

## Modifier Strategy

- schema modifiers: simplify tool inputs before the model sees schemas
- before modifiers: enforce runtime argument defaults/guards
- after modifiers: normalize outputs for downstream systems

## Source References

- [Executing Tools](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/executing-tools.mdx)
- [Schema Modifiers](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/modify-tool-behavior/schema-modifiers.mdx)
- [Before Execution Modifiers](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/modify-tool-behavior/before-execution-modifiers.mdx)
- [After Execution Modifiers](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/modify-tool-behavior/after-execution-modifiers.mdx)

## Summary

You now have an execution and modifier model that can be adapted to both agentic and deterministic workloads.

Next: [Chapter 6: MCP Server Patterns and Toolkit Control](06-mcp-server-patterns-and-toolkit-control.md)
