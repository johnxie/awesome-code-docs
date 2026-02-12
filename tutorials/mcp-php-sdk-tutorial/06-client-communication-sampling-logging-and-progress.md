---
layout: default
title: "Chapter 6: Client Communication: Sampling, Logging, and Progress"
nav_order: 6
parent: MCP PHP SDK Tutorial
---

# Chapter 6: Client Communication: Sampling, Logging, and Progress

This chapter explains server-to-client communication utilities in PHP MCP handlers.

## Learning Goals

- use client gateway patterns for server-initiated communication
- apply sampling requests with clear user-control boundaries
- emit log and progress signals in protocol-compliant form
- reduce handler complexity around async-like notification flows

## Communication Surface

| Surface | Purpose |
|:--------|:--------|
| Sampling | server asks client to run model generation |
| Logging | structured diagnostics and observability |
| Progress | incremental status feedback for long-running calls |
| Notifications | out-of-band updates to client state |

## Source References

- [Client Communication Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-client-communication.md)
- [MCP Elements Guide - Logging](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md#logging)

## Summary

You now have an operational communication model for richer PHP MCP server UX.

Next: [Chapter 7: Framework Integration, Session Stores, and Dependencies](07-framework-integration-session-stores-and-dependencies.md)
