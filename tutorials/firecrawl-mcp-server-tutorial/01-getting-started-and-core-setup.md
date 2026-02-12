---
layout: default
title: "Chapter 1: Getting Started and Core Setup"
nav_order: 1
parent: Firecrawl MCP Server Tutorial
---

# Chapter 1: Getting Started and Core Setup

This chapter gets Firecrawl MCP running with minimum viable configuration.

## Learning Goals

- launch Firecrawl MCP with cloud credentials
- verify tool availability in your client
- capture initial connectivity checks

## Quick Start Command

```bash
env FIRECRAWL_API_KEY=fc-YOUR_API_KEY npx -y firecrawl-mcp
```

## First-Run Checklist

1. API key is valid
2. client connects to server process
3. at least one scrape/search call succeeds
4. logs show no repeated auth or rate-limit failures

## Source References

- [README Installation](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/README.md)

## Summary

You now have a working Firecrawl MCP baseline.

Next: [Chapter 2: Architecture, Transports, and Versioning](02-architecture-transports-and-versioning.md)
