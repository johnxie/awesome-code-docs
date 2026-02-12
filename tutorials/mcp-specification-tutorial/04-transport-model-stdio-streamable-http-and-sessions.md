---
layout: default
title: "Chapter 4: Transport Model: stdio, Streamable HTTP, and Sessions"
nav_order: 4
parent: MCP Specification Tutorial
---

# Chapter 4: Transport Model: stdio, Streamable HTTP, and Sessions

Transport behavior drives most production incidents in MCP systems.

## Learning Goals

- choose between stdio and Streamable HTTP based on deployment context
- implement session headers and protocol-version headers correctly
- handle SSE polling and resumability without breaking message ordering
- apply required security controls for remote/local HTTP endpoints

## Transport Decision Matrix

| Transport | Best Fit | Core Risks |
|:----------|:---------|:-----------|
| `stdio` | local subprocess servers | stdout contamination, process lifecycle leaks |
| Streamable HTTP | remote/shared servers and multi-client deployments | origin validation, session hijack, reconnection loss |

## Streamable HTTP Must-Haves

- validate `Origin` and reject invalid origin with `403`
- include and honor `MCP-Session-Id` when server assigns stateful sessions
- include `MCP-Protocol-Version` on follow-up HTTP requests
- support both `application/json` and `text/event-stream` response paths
- plan explicit behavior for resumability/redelivery and session expiration

## Source References

- [Transports](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx)
- [Lifecycle](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/lifecycle.mdx)
- [Security Best Practices - Session Hijacking](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/security_best_practices.mdx)

## Summary

You now have a transport operations model that is compatible with current session and security requirements.

Next: [Chapter 5: Server Primitives: Tools, Resources, and Prompts](05-server-primitives-tools-resources-and-prompts.md)
