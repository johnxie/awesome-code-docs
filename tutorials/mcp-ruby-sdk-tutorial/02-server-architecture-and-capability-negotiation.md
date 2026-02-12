---
layout: default
title: "Chapter 2: Server Architecture and Capability Negotiation"
nav_order: 2
parent: MCP Ruby SDK Tutorial
---

# Chapter 2: Server Architecture and Capability Negotiation

This chapter explains how `MCP::Server` handles initialization, method routing, and capability exposure.

## Learning Goals

- map `MCP::Server` responsibilities to JSON-RPC protocol flow
- configure capability surfaces intentionally
- understand built-in MCP methods and extension points
- keep custom method behavior isolated from core protocol methods

## Core Server Method Groups

| Method Group | Purpose |
|:-------------|:--------|
| `initialize`, `ping` | protocol startup and health checks |
| `tools/*`, `prompts/*`, `resources/*` | primitive discovery and execution |
| custom methods | domain-specific RPC extensions |

## Design Guardrails

- do not overload standard MCP methods with application semantics.
- use `define_custom_method` only for non-protocol behaviors.
- keep initialize capability claims synchronized with implemented handlers.

## Source References

- [Ruby SDK README - Building an MCP Server](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#building-an-mcp-server)
- [Ruby SDK README - Supported Methods](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#supported-methods)
- [Ruby SDK README - Custom Methods](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#custom-methods)

## Summary

You now have a server architecture baseline aligned to MCP method and capability semantics.

Next: [Chapter 3: Tools, Prompts, Resources, and Schema Discipline](03-tools-prompts-resources-and-schema-discipline.md)
