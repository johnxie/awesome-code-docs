---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: FastMCP Tutorial
---

# Chapter 1: Getting Started

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
