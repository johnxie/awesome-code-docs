---
layout: default
title: "Chapter 1: Getting Started and First Publish"
nav_order: 1
parent: MCP Registry Tutorial
---

# Chapter 1: Getting Started and First Publish

This chapter sets up the first end-to-end publish flow using `mcp-publisher`.

## Learning Goals

- prepare a minimal valid `server.json`
- align package metadata and registry naming requirements
- authenticate and publish with the official CLI
- verify publication via registry API search

## Fast Start Loop

1. publish your package artifact first (npm/PyPI/NuGet/OCI/MCPB)
2. generate `server.json` with `mcp-publisher init`
3. authenticate with `mcp-publisher login <method>`
4. run `mcp-publisher publish`
5. verify with `GET /v0.1/servers?search=<server-name>`

## Baseline Commands

```bash
# Install tool
brew install mcp-publisher

# Create template
mcp-publisher init

# Authenticate (example: GitHub)
mcp-publisher login github

# Publish
mcp-publisher publish
```

## Source References

- [Quickstart: Publish a Server](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx)
- [Publisher CLI Commands](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/cli/commands.md)

## Summary

You now have a working baseline for first publication.

Next: [Chapter 2: Registry Architecture and Data Flow](02-registry-architecture-and-data-flow.md)
