---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Context7 Tutorial
---

# Chapter 1: Getting Started

This chapter gets Context7 connected to your coding agent so documentation lookups work immediately.

## Learning Goals

- choose local or remote Context7 MCP deployment
- connect Context7 in your primary coding client
- verify tool connectivity and first query
- avoid common first-install mistakes

## Fast Install Patterns

| Pattern | Example |
|:--------|:--------|
| Claude Code local | `claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY` |
| Claude Code remote | `claude mcp add --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp` |
| Cursor remote config | MCP URL `https://mcp.context7.com/mcp` + optional API key header |

## First-Use Checklist

1. add Context7 MCP server in your client
2. run client MCP status command or panel
3. ask a targeted library question with `use context7`
4. confirm the response cites current docs patterns

## Source References

- [Context7 README: Installation](https://github.com/upstash/context7/blob/master/README.md#installation)
- [Claude Code client guide](https://context7.com/docs/clients/claude-code)
- [Cursor client guide](https://context7.com/docs/clients/cursor)

## Summary

You now have Context7 running and reachable from your coding client.

Next: [Chapter 2: Architecture and Tooling Model](02-architecture-and-tooling-model.md)
