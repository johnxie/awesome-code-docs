---
layout: default
title: "Chapter 5: Transports: stdio, Streamable HTTP, and Session Modes"
nav_order: 5
parent: MCP Ruby SDK Tutorial
---

# Chapter 5: Transports: stdio, Streamable HTTP, and Session Modes

This chapter maps transport options to local development and distributed runtime scenarios.

## Learning Goals

- choose between stdio and streamable HTTP deployment modes
- understand stateful vs stateless streamable HTTP behavior
- handle session headers and lifecycle flow correctly
- test SSE notification paths with realistic tooling

## Transport Decision Matrix

| Mode | Best Fit |
|:-----|:---------|
| stdio | local subprocess integrations and desktop tooling |
| streamable HTTP (stateful) | session-based services with SSE notifications |
| streamable HTTP (stateless) | horizontally scaled request/response-only deployments |

## Session Flow (HTTP)

1. client initializes and receives `Mcp-Session-Id`
2. optional SSE stream opens for notifications
3. client sends JSON-RPC POST requests with session context
4. client closes session when done

## Source References

- [Ruby SDK README - Transport Support](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#transport-support)
- [Ruby SDK README - Stateless Streamable HTTP](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#usage-example)
- [Ruby Examples - Streamable HTTP Details](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/examples/README.md#streamable-http-transport-details)

## Summary

You now have a transport/session framework for Ruby MCP runtime planning.

Next: [Chapter 6: Client Workflows, HTTP Integration, and Auth Considerations](06-client-workflows-http-integration-and-auth-considerations.md)
