---
layout: default
title: "Chapter 6: Extensions and MCP Integration"
nav_order: 6
parent: Goose Tutorial
---

# Chapter 6: Extensions and MCP Integration

This chapter covers how Goose expands beyond built-ins through MCP extension workflows.

## Learning Goals

- understand Goose extension architecture
- enable and manage built-in extensions safely
- add custom MCP servers via UI or CLI
- standardize extension rollout for teams

## Built-In Extension Surface

Goose includes development and platform extensions such as:

- Developer
- Computer Controller
- Memory
- Extension Manager
- Skills
- Todo

These can be toggled based on task needs to reduce tool overload.

## Custom MCP Flow (CLI)

```bash
goose configure
# select: Add Extension
# choose: Command-line Extension OR Remote Extension
```

Example pattern for an MCP server command:

```bash
npx -y @modelcontextprotocol/server-memory
```

## Extension Safety Checklist

1. review extension command/source
2. set reasonable timeout values
3. apply tool permissions before broad usage
4. test in a sandbox repository first

## Source References

- [Using Extensions](https://block.github.io/goose/docs/getting-started/using-extensions)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server Directory](https://www.pulsemcp.com/servers)

## Summary

You now know how to evolve Goose capabilities with built-in and external MCP integrations.

Next: [Chapter 7: CLI Workflows and Automation](07-cli-workflows-and-automation.md)
