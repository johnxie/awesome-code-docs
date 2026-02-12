---
layout: default
title: "Chapter 4: CLI Mode, Automation, and CI Loops"
nav_order: 4
parent: MCP Inspector Tutorial
---

# Chapter 4: CLI Mode, Automation, and CI Loops

Inspector CLI mode is the bridge from manual debugging to deterministic automation.

## Learning Goals

- run CLI mode against local and remote MCP servers
- script list/call flows for smoke tests
- pass headers and args safely for CI use
- standardize JSON outputs for pipeline checks

## Core CLI Patterns

```bash
# Local stdio server, list tools
npx @modelcontextprotocol/inspector --cli node build/index.js --method tools/list

# Call a tool with arguments
npx @modelcontextprotocol/inspector --cli node build/index.js \
  --method tools/call --tool-name mytool --tool-arg key=value

# Remote streamable HTTP endpoint
npx @modelcontextprotocol/inspector --cli https://example.com/mcp \
  --transport http --method resources/list
```

## CI Strategy

- keep one golden endpoint per server family for smoke checks
- run read-only calls first (`tools/list`, `resources/list`)
- treat timeouts and transport errors as separate failure classes
- persist raw JSON output for regression diffs

## Source References

- [Inspector README - CLI Mode](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#cli-mode)
- [Inspector CLI Package](https://github.com/modelcontextprotocol/inspector/tree/main/cli)

## Summary

You can now automate Inspector-based checks in build and release pipelines.

Next: [Chapter 5: Security, Auth, and Network Hardening](05-security-auth-and-network-hardening.md)
