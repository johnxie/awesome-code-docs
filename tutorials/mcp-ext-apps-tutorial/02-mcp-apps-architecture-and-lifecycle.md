---
layout: default
title: "Chapter 2: MCP Apps Architecture and Lifecycle"
nav_order: 2
parent: MCP Ext Apps Tutorial
---

# Chapter 2: MCP Apps Architecture and Lifecycle

This chapter covers lifecycle stages from tool declaration to host-rendered UI interaction.

## Learning Goals

- map tool metadata to UI resource resolution
- understand host sandbox behavior and iframe lifecycle
- model bidirectional messaging between host and app
- identify lifecycle failure points before implementation

## Lifecycle Stages

1. server tool declares associated `ui://` resource
2. model invokes tool via normal MCP flow
3. host resolves UI resource and renders sandboxed app
4. host passes tool outputs/context into app runtime
5. app may trigger follow-up tool calls through the host bridge

## Source References

- [MCP Apps Overview](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/overview.md)
- [Ext Apps README - How It Works](https://github.com/modelcontextprotocol/ext-apps/blob/main/README.md#how-it-works)

## Summary

You now have a lifecycle model for MCP Apps interactions across server, host, and UI layers.

Next: [Chapter 3: App SDK: UI Resources and Tool Linkage](03-app-sdk-ui-resources-and-tool-linkage.md)
