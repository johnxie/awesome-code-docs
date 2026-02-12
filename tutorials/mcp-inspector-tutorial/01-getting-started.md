---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: MCP Inspector Tutorial
---

# Chapter 1: Getting Started

This chapter gives you the fastest path to a usable Inspector baseline.

## Learning Goals

- launch Inspector in UI mode with default local-safe settings
- connect to a local MCP server process
- confirm core methods (`tools/list`, `resources/list`, `prompts/list`) work
- capture a reproducible baseline command for your team

## Fast Start Loop

1. ensure Node.js version satisfies `^22.7.5`
2. run `npx @modelcontextprotocol/inspector`
3. open `http://localhost:6274`
4. connect a known test server (for example `node build/index.js`)
5. run one list call per capability area and verify outputs in the UI

## Baseline Command Variants

```bash
# Start inspector UI and proxy on defaults
npx @modelcontextprotocol/inspector

# Start inspector against a local stdio server
npx @modelcontextprotocol/inspector node build/index.js

# Override ports if defaults are occupied
CLIENT_PORT=8080 SERVER_PORT=9000 npx @modelcontextprotocol/inspector node build/index.js
```

## Source References

- [Inspector README - Quick Start](https://github.com/modelcontextprotocol/inspector/blob/main/README.md)
- [Inspector README - Running from an MCP server repository](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#from-an-mcp-server-repository)

## Summary

You now have a working Inspector baseline with validated server connectivity.

Next: [Chapter 2: Architecture, Transports, and Session Model](02-architecture-transports-and-session-model.md)
