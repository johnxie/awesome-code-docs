---
layout: default
title: "Chapter 5: Transport, Retry, and Reconnect Strategy"
nav_order: 5
parent: use-mcp Tutorial
---

# Chapter 5: Transport, Retry, and Reconnect Strategy

This chapter focuses on resilience controls for unstable networks and intermittent server availability.

## Learning Goals

- choose transport preference (`auto`, `http`, `sse`) by server behavior
- tune `autoRetry` and `autoReconnect` without overloading endpoints
- distinguish auth failures from transport connectivity failures
- expose clear user-visible retry paths in UI

## Reliability Checklist

1. start with `transportType: auto` unless you need strict transport pinning
2. set bounded retry intervals for both initial connection and reconnect
3. instrument and surface failure reasons before forcing auth retries
4. disable aggressive reconnect loops in high-failure environments

## Source References

- [use-mcp README - Options](https://github.com/modelcontextprotocol/use-mcp/blob/main/README.md#options)
- [React Integration README - Hook Options](https://github.com/modelcontextprotocol/use-mcp/blob/main/src/react/README.md#hook-options-usemcpoptions)

## Summary

You now have a practical resilience model for browser-based MCP client sessions.

Next: [Chapter 6: React Integration Patterns: Chat UI and Inspector](06-react-integration-patterns-chat-ui-and-inspector.md)
