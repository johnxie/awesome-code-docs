---
layout: default
title: "Chapter 5: Configuration, Retries, and Credit Monitoring"
nav_order: 5
parent: Firecrawl MCP Server Tutorial
---

# Chapter 5: Configuration, Retries, and Credit Monitoring

Production reliability depends on proper retry controls and credit thresholds.

## Learning Goals

- configure retry behavior for rate-limited environments
- tune warning and critical thresholds for credits
- support cloud and self-hosted API endpoints cleanly

## Key Environment Variables

| Variable | Purpose |
|:---------|:--------|
| `FIRECRAWL_API_KEY` | authentication for cloud usage |
| `FIRECRAWL_API_URL` | custom endpoint for self-hosted deployments |
| `FIRECRAWL_RETRY_*` | retry/backoff behavior controls |
| `FIRECRAWL_CREDIT_*` | warning and critical credit thresholds |

## Source References

- [README Configuration](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/README.md)
- [Changelog 1.2.4 and 1.2.0](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/CHANGELOG.md)

## Summary

You now know which controls matter most for resilient Firecrawl MCP operations.

Next: [Chapter 6: Batch Workflows, Deep Research, and API Evolution](06-batch-workflows-deep-research-and-api-evolution.md)
