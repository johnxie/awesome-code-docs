---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Chrome DevTools MCP Tutorial
---

# Chapter 1: Getting Started

This chapter gets Chrome DevTools MCP connected to your coding client.

## Learning Goals

- install and run the MCP server quickly
- configure client-side MCP server entries
- verify browser connection and first tool call
- avoid common first-install mistakes

## Fast Setup Pattern

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## Source References

- [Chrome DevTools MCP README](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/README.md)
- [Chrome DevTools MCP Releases](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases)

## Summary

You now have a working Chrome DevTools MCP baseline in your coding client.

Next: [Chapter 2: Architecture and Design Principles](02-architecture-and-design-principles.md)
