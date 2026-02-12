---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Serena Tutorial
---

# Chapter 1: Getting Started

This chapter gets Serena running as an MCP server so your agent can use semantic code tools immediately.

## Learning Goals

- install required tooling (`uv`)
- launch Serena MCP server from the latest GitHub source
- connect a first MCP client
- validate basic semantic tool availability

## Fast Start Path

```bash
uvx --from git+https://github.com/oraios/serena serena start-mcp-server --help
```

## First Client Setup Pattern

1. choose MCP-capable client (Claude Code, Codex, Cursor, etc.)
2. configure Serena launch command in client MCP settings
3. restart client and verify Serena tools are listed
4. run a small retrieval task in a known repository

## Early Failure Triage

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| server fails to start | missing `uv` dependency | install/update `uv` and retry |
| tools not visible in client | MCP launch command not wired correctly | recheck client config path and restart client |
| weak retrieval results | repo context or backend not configured | verify project setup and backend prerequisites |

## Source References

- [Serena Quick Start](https://github.com/oraios/serena/blob/main/README.md#quick-start)
- [MCP Client Setup Guide](https://oraios.github.io/serena/02-usage/030_clients.html)

## Summary

You now have Serena launched and connected as an MCP server.

Next: [Chapter 2: Semantic Toolkit and Agent Loop](02-semantic-toolkit-and-agent-loop.md)
