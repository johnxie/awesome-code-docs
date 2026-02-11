---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: MCP Servers Tutorial
---

# Chapter 1: Getting Started

This chapter orients you to the official MCP servers repository and local setup.

## Clone and Inspect

```bash
git clone https://github.com/modelcontextprotocol/servers.git
cd servers
ls
```

## Why Start with Reference Servers

- Real implementations of protocol patterns.
- Consistent examples across languages.
- Good defaults for testing and security posture.

## First Run Strategy

- Pick one server (`filesystem` or `time`).
- Run locally with minimal config.
- Connect from an MCP-capable client.

## Summary

You now have a local baseline for exploring MCP reference implementations.

Next: [Chapter 2: Filesystem Server](02-filesystem-server.md)
