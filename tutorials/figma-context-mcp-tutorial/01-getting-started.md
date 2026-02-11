---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Figma Context MCP Tutorial
---

# Chapter 1: Getting Started

This chapter gets Figma Context MCP connected to your coding client with a working token and first design fetch.

## Learning Goals

- create and configure a Figma personal access token
- register MCP server in client config
- fetch context from a Figma frame URL
- validate first design-to-code prompt roundtrip

## Minimal MCP Config (macOS/Linux)

```json
{
  "mcpServers": {
    "Framelink MCP for Figma": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--figma-api-key=YOUR-KEY", "--stdio"]
    }
  }
}
```

## Source References

- [Framelink Quickstart](https://www.framelink.ai/docs/quickstart)
- [Figma Token Docs](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)

## Summary

You now have a working MCP bridge between Figma and your coding assistant.

Next: [Chapter 2: Architecture and Context Translation](02-architecture-and-context-translation.md)
