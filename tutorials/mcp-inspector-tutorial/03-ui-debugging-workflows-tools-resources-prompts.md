---
layout: default
title: "Chapter 3: UI Debugging Workflows: Tools, Resources, Prompts"
nav_order: 3
parent: MCP Inspector Tutorial
---

# Chapter 3: UI Debugging Workflows: Tools, Resources, Prompts

The UI is optimized for rapid exploratory debugging across tools, resources, prompts, sampling, and request history.

## Learning Goals

- validate capability discovery quickly after connecting
- run tool calls with structured argument payloads
- inspect response payloads and error output in a repeatable way
- export server entries for reuse in client config files

## Recommended Debug Loop

1. run `tools/list`, inspect parameter schemas
2. execute one low-risk tool call with explicit arguments
3. run `resources/list` and fetch a small resource payload
4. run `prompts/list` and test one prompt path
5. export a Server Entry or full `mcp.json` for downstream clients

## UI-to-Config Handoff

Use Inspector's "Server Entry" and "Servers File" export buttons to avoid manual config drift when moving from local debug to tools like Claude Code or Cursor.

## Source References

- [Inspector README - Servers File Export](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#servers-file-export)
- [Inspector README - UI Mode vs CLI Mode](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#ui-mode-vs-cli-mode-when-to-use-each)
- [Inspector Client Source Tree](https://github.com/modelcontextprotocol/inspector/tree/main/client/src/components)

## Summary

You now have a practical, repeatable UI workflow for MCP server debugging.

Next: [Chapter 4: CLI Mode, Automation, and CI Loops](04-cli-mode-automation-and-ci-loops.md)
