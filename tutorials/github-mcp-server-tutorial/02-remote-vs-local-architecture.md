---
layout: default
title: "Chapter 2: Remote vs Local Architecture"
nav_order: 2
parent: GitHub MCP Server Tutorial
---

# Chapter 2: Remote vs Local Architecture

This chapter explains the tradeoffs between the hosted remote server and self-run local server.

## Learning Goals

- understand feature and operational differences by mode
- pick deployment mode based on host and governance needs
- reason about scalability, maintenance, and control boundaries
- avoid configuration mismatches across modes

## Mode Comparison

| Mode | Best For | Key Constraint |
|:-----|:---------|:---------------|
| remote (`https://api.githubcopilot.com/mcp/`) | fastest setup and managed operations | depends on host support for remote MCP/OAuth |
| local (`ghcr.io/github/github-mcp-server`) | strict environment control and custom execution | requires Docker/binary lifecycle management |

## Practical Rule

Use remote mode first when available. Use local mode when host limitations, environment policy, or deeper control requires it.

## Source References

- [README: Remote GitHub MCP Server](https://github.com/github/github-mcp-server/blob/main/README.md#remote-github-mcp-server)
- [README: Local GitHub MCP Server](https://github.com/github/github-mcp-server/blob/main/README.md#local-github-mcp-server)
- [Remote Server Docs](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)

## Summary

You now understand the operational boundaries of remote and local modes.

Next: [Chapter 3: Authentication and Token Strategy](03-authentication-and-token-strategy.md)
