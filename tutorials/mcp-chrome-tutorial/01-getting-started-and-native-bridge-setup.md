---
layout: default
title: "Chapter 1: Getting Started and Native Bridge Setup"
nav_order: 1
parent: MCP Chrome Tutorial
---

# Chapter 1: Getting Started and Native Bridge Setup

This chapter establishes a stable local setup across native bridge install, extension loading, and MCP client connection.

## Learning Goals

- install `mcp-chrome-bridge` globally
- load the Chrome extension and verify connection
- connect an MCP client using streamable HTTP or stdio

## Baseline Install

```bash
npm install -g mcp-chrome-bridge
```

If needed, run manual registration:

```bash
mcp-chrome-bridge register
```

## Connection Checklist

1. extension is loaded in `chrome://extensions/`
2. extension UI shows connected bridge status
3. MCP client can call at least one basic tool
4. browser tab listing returns expected windows/tabs

## Source References

- [README Quick Start](https://github.com/hangwin/mcp-chrome/blob/master/README.md)
- [Native Install Guide](https://github.com/hangwin/mcp-chrome/blob/master/app/native-server/install.md)

## Summary

You now have MCP Chrome installed and reachable from an MCP client.

Next: [Chapter 2: Architecture and Component Boundaries](02-architecture-and-component-boundaries.md)
