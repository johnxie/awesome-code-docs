---
layout: default
title: "Chapter 3: App SDK: UI Resources and Tool Linkage"
nav_order: 3
parent: MCP Ext Apps Tutorial
---

# Chapter 3: App SDK: UI Resources and Tool Linkage

This chapter focuses on app-developer workflows for rendering and interacting with tool-driven data.

## Learning Goals

- link tool output to UI resource rendering paths
- structure app state around host-delivered context and events
- use framework integrations (React hooks or vanilla helpers) effectively
- avoid brittle coupling between tool payload shape and UI behavior

## App-Side Checklist

1. register tool metadata with clear UI linkage
2. parse and validate incoming structured tool payloads
3. keep view state resilient across host context changes
4. implement graceful fallback for missing/partial data

## Source References

- [Quickstart Guide](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/quickstart.md)
- [MCP Apps Patterns](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/patterns.md)
- [Basic Server React Example](https://github.com/modelcontextprotocol/ext-apps/blob/main/examples/basic-server-react/README.md)

## Summary

You now have an app-side implementation model for tool-linked MCP UI resources.

Next: [Chapter 4: Host Bridge and Context Management](04-host-bridge-and-context-management.md)
