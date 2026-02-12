---
layout: default
title: "Chapter 7: Testing, Troubleshooting, and Rough Edges"
nav_order: 7
parent: MCP Go SDK Tutorial
---

# Chapter 7: Testing, Troubleshooting, and Rough Edges

Operational quality improves when teams treat debugging and known limitations as first-class concerns.

## Learning Goals

- build a practical troubleshooting loop for MCP transport and handler issues
- use inspector and HTTP traffic inspection effectively
- account for known v1 rough edges in API usage
- reduce recurring production support incidents

## Troubleshooting Workflow

1. reproduce against a minimal example transport path
2. inspect MCP wire logs and HTTP traces
3. validate capability advertisement vs actual handlers
4. cross-check behavior against rough-edge notes before escalating

## Rough-Edge Themes to Track

- default capabilities behavior can surprise teams expecting empty defaults
- some naming and capability field decisions are scheduled for v2 cleanup
- event store and stream semantics need careful design in resumable deployments

## Source References

- [Troubleshooting Guide](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/troubleshooting.md)
- [Rough Edges](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/rough_edges.md)
- [MCP Inspector Tutorial](../mcp-inspector-tutorial/)

## Summary

You now have a disciplined debugging approach and awareness of v1 API edges that affect production behavior.

Next: [Chapter 8: Conformance, Operations, and Upgrade Strategy](08-conformance-operations-and-upgrade-strategy.md)
