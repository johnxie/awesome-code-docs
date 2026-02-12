---
layout: default
title: "Chapter 5: Local Integration: Claude Desktop and Inspector"
nav_order: 5
parent: Create Python Server Tutorial
---

# Chapter 5: Local Integration: Claude Desktop and Inspector

This chapter explains local integration and debugging workflows for generated servers.

## Learning Goals

- configure generated server commands for Claude Desktop
- use Inspector workflows for stdio debugging and validation
- test development vs published server command paths
- reduce time-to-diagnosis for integration issues

## Integration Modes

| Mode | Command Pattern |
|:-----|:----------------|
| development | `uv --directory <server-dir> run <server-name>` |
| published | `uvx <server-name>` |

## Source References

- [Template README - Claude Desktop Configuration](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2#claude-desktop)
- [Template README - Debugging](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2#debugging)

## Summary

You now have a working local integration and debugging strategy for scaffolded servers.

Next: [Chapter 6: Customization and Extension Patterns](06-customization-and-extension-patterns.md)
