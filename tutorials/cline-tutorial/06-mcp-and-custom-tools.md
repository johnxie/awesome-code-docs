---
layout: default
title: "Chapter 6: MCP and Custom Tools"
nav_order: 6
parent: Cline Tutorial
---

# Chapter 6: MCP and Custom Tools

Cline can be extended through MCP to interact with domain-specific tools.

## Why MCP Matters

MCP allows structured tool integration with clear contracts, enabling workflows like issue tracking, cloud ops, internal knowledge retrieval, and custom automation.

## Tool Design Principles

- strict input schema validation
- explicit output schemas
- side-effect classification (read-only vs mutating)
- robust timeout and error behavior

## Integration Workflow

1. define tool contract
2. connect MCP server
3. verify tool listing and invocation
4. gate high-risk operations with explicit approval

## Summary

You can now extend Cline beyond base capabilities with governed tool integrations.

Next: [Chapter 7: Context and Cost Control](07-context-and-cost-control.md)
