---
layout: default
title: "Chapter 4: Toolsets, Tools, and Dynamic Discovery"
nav_order: 4
parent: GitHub MCP Server Tutorial
---

# Chapter 4: Toolsets, Tools, and Dynamic Discovery

This chapter explains how to precisely shape the server capability surface for better reliability and safety.

## Learning Goals

- constrain tools using toolsets and explicit tool allow-lists
- use dynamic discovery to limit initial tool overload
- combine read-only mode with selective tool exposure
- prevent accidental write operations in exploratory sessions

## Control Surface Options

| Control | Local | Remote |
|:--------|:------|:-------|
| toolsets | `--toolsets` / `GITHUB_TOOLSETS` | URL + `X-MCP-Toolsets` |
| individual tools | `--tools` / `GITHUB_TOOLS` | header-based filtering |
| read-only | `--read-only` / `GITHUB_READ_ONLY` | `/readonly` or `X-MCP-Readonly` |
| dynamic discovery | `--dynamic-toolsets` | not available |
| lockdown mode | `--lockdown-mode` | `X-MCP-Lockdown` |

## Source References

- [README: Tool Configuration](https://github.com/github/github-mcp-server/blob/main/README.md#tool-configuration)
- [Server Configuration Guide](https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md)
- [Remote Server Docs: Headers](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md#headers)

## Summary

You now know how to expose just enough capability for each task context.

Next: [Chapter 5: Host Integration Patterns](05-host-integration-patterns.md)
