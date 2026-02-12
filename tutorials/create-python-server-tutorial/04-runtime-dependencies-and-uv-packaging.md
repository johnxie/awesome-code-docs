---
layout: default
title: "Chapter 4: Runtime, Dependencies, and uv Packaging"
nav_order: 4
parent: Create Python Server Tutorial
---

# Chapter 4: Runtime, Dependencies, and uv Packaging

This chapter focuses on dependency/runtime controls for reliable local and publish workflows.

## Learning Goals

- manage dependencies with `uv` conventions
- run generated servers in development and publish modes
- keep lockfiles and build artifacts reproducible
- avoid environment drift across contributors

## Packaging Flow

1. sync dependencies (`uv sync`)
2. build artifacts (`uv build`)
3. publish package (`uv publish`) with secure credential handling

## Source References

- [Create Python Server README](https://github.com/modelcontextprotocol/create-python-server/blob/main/README.md)
- [Template README - Building and Publishing](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2#building-and-publishing)

## Summary

You now have a consistent runtime and packaging model for generated MCP servers.

Next: [Chapter 5: Local Integration: Claude Desktop and Inspector](05-local-integration-claude-desktop-and-inspector.md)
