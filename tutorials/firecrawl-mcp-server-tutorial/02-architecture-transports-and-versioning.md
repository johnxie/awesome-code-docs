---
layout: default
title: "Chapter 2: Architecture, Transports, and Versioning"
nav_order: 2
parent: Firecrawl MCP Server Tutorial
---

# Chapter 2: Architecture, Transports, and Versioning

Firecrawl MCP supports local transports and cloud-mode versioned endpoints, with V2 as the default modern path.

## Learning Goals

- understand transport mode implications
- map V1 vs V2 endpoint differences
- avoid migration mistakes in existing integrations

## Endpoint Model Highlights

| Mode | Notes |
|:-----|:------|
| local stdio/streamable | V2 behavior by default |
| cloud service mode | versioned V1 and V2 endpoint paths |

## Versioning Guidance

- V1 endpoints remain for backward compatibility.
- V2 is the current path for modern tool behavior and API support.
- migration requires endpoint and tool-surface awareness.

## Source References

- [Versioning Guide](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/VERSIONING.md)
- [README Transport Setup](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/README.md)

## Summary

You now understand the transport and version boundaries that shape deployment architecture.

Next: [Chapter 3: Tool Selection: Scrape, Map, Crawl, Search, Extract](03-tool-selection-scrape-map-crawl-search-extract.md)
