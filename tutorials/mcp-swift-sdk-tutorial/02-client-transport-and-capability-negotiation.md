---
layout: default
title: "Chapter 2: Client Transport and Capability Negotiation"
nav_order: 2
parent: MCP Swift SDK Tutorial
---

# Chapter 2: Client Transport and Capability Negotiation

Transport and capability negotiation choices drive most client-side behavior variance.

## Learning Goals

- choose between stdio and HTTP client transport paths
- interpret initialization results and capability availability
- handle capability mismatch behavior intentionally
- keep transport configuration explicit in app architecture

## Transport Decision Guide

| Transport | Best Fit |
|:----------|:---------|
| `StdioTransport` | local subprocess workflows |
| `HTTPClientTransport` | remote MCP endpoints with optional streaming |

## Source References

- [Swift SDK README - Client Usage](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#client-usage)
- [Swift SDK README - Transport Options](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#transport-options-for-clients)

## Summary

You now have a client setup model that keeps capability assumptions and transport behavior aligned.

Next: [Chapter 3: Tools, Resources, Prompts, and Request Patterns](03-tools-resources-prompts-and-request-patterns.md)
