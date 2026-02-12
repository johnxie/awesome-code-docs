---
layout: default
title: "Chapter 5: Search Tools and Progressive Disclosure"
nav_order: 5
parent: Claude-Mem Tutorial
---

# Chapter 5: Search Tools and Progressive Disclosure

This chapter shows how to retrieve memory context efficiently with layered search patterns.

## Learning Goals

- use the three-layer retrieval workflow correctly
- choose search/timeline/full-observation calls intentionally
- minimize token burn while maximizing relevance
- apply memory search patterns to debugging and planning tasks

## Three-Layer Retrieval Pattern

1. `search` for compact candidate index
2. `timeline` for chronological context around candidates
3. `get_observations` for full details of filtered IDs only

This staged approach is the primary token-efficiency mechanism in Claude-Mem.

## Practical Retrieval Rules

- batch relevant IDs instead of one-by-one requests
- filter by project/type/date before full detail fetches
- keep search queries explicit and scoped to intent

## Source References

- [Search Tools Guide](https://docs.claude-mem.ai/usage/search-tools)
- [README MCP Search Tools](https://github.com/thedotmack/claude-mem/blob/main/README.md#mcp-search-tools)
- [Progressive Disclosure Guide](https://docs.claude-mem.ai/progressive-disclosure)

## Summary

You now have a token-efficient memory retrieval workflow for complex sessions.

Next: [Chapter 6: Viewer Operations and Maintenance Workflows](06-viewer-operations-and-maintenance-workflows.md)
