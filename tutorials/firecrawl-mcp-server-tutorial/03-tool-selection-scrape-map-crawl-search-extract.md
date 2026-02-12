---
layout: default
title: "Chapter 3: Tool Selection: Scrape, Map, Crawl, Search, Extract"
nav_order: 3
parent: Firecrawl MCP Server Tutorial
---

# Chapter 3: Tool Selection: Scrape, Map, Crawl, Search, Extract

Effective Firecrawl usage depends on selecting the right tool for each information-retrieval task.

## Learning Goals

- choose tools based on known vs unknown URL scope
- combine tools for multi-step research tasks
- avoid over-crawling when simpler methods suffice

## Tool Selection Matrix

| Task Type | Preferred Tool |
|:----------|:---------------|
| single known URL | `scrape` |
| many known URLs | batch scrape variants |
| discover URLs on a domain | `map` |
| broad web discovery | `search` |
| large site traversal | `crawl` with strict limits |
| structured extraction | `extract` with schema guidance |

## Source References

- [README Tool Guide](https://github.com/firecrawl/firecrawl-mcp-server/blob/main/README.md)

## Summary

You now have a decision framework for tool selection that balances depth, cost, and speed.

Next: [Chapter 4: Client Integrations: Cursor, Claude, Windsurf, VS Code](04-client-integrations-cursor-claude-windsurf-vscode.md)
