---
layout: default
title: "Chapter 3: Template Server Architecture: Resources, Prompts, and Tools"
nav_order: 3
parent: Create Python Server Tutorial
---

# Chapter 3: Template Server Architecture: Resources, Prompts, and Tools

This chapter dives into the generated server template and how it models core MCP primitives.

## Learning Goals

- inspect generated handlers for resource, prompt, and tool endpoints
- understand state management patterns in template code
- map primitive behavior to MCP protocol semantics
- identify extension points for domain-specific logic

## Template Highlights

- `list_resources` and `read_resource` expose note-based URI resources.
- `list_prompts` and `get_prompt` generate argument-aware prompt messages.
- `list_tools` and `call_tool` demonstrate tool registration, validation, and state mutation.

## Source References

- [Template Server Implementation](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/server.py.jinja2)
- [Template README](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2)

## Summary

You now have a concrete mental model for generated MCP primitive handlers.

Next: [Chapter 4: Runtime, Dependencies, and uv Packaging](04-runtime-dependencies-and-uv-packaging.md)
