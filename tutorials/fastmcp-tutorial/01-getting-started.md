---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: FastMCP Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gives you a quick path from installation to a working FastMCP server and first client call.

## Learning Goals

- create and run a minimal server with one tool
- validate a basic client-server call loop
- understand local stdio versus HTTP first-run choices
- establish a repeatable baseline for future extension

## Fast Start Loop

1. install FastMCP from the [installation guide](https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/installation.mdx)
2. create a minimal server with `FastMCP(...)` and one `@mcp.tool`
3. run locally using `mcp.run()` or `fastmcp run ...`
4. call the tool from a client to verify end-to-end behavior
5. capture this setup as your baseline template for new services

## Source References

- [Quickstart](https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx)
- [README](https://github.com/jlowin/fastmcp/blob/main/README.md)

## Summary

You now have a reliable baseline for expanding FastMCP servers beyond toy examples.

Next: [Chapter 2: Core Abstractions: Components, Providers, Transforms](02-core-abstractions-components-providers-transforms.md)

## How These Components Connect

```mermaid
flowchart TD
    A[Install fastmcp] --> B[Create FastMCP server]
    B --> C[Define tools with @mcp.tool]
    B --> D[Define resources with @mcp.resource]
    C --> E[Run: mcp.run()]
    D --> E
    E --> F{Transport}
    F -->|stdio| G[Claude Desktop / local host]
    F -->|SSE/HTTP| H[Remote clients]
```
