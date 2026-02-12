---
layout: default
title: "Chapter 2: Generated Project Structure and Conventions"
nav_order: 2
parent: Create Python Server Tutorial
---

# Chapter 2: Generated Project Structure and Conventions

This chapter explains generated file layout and how each piece supports maintainable server development.

## Learning Goals

- navigate scaffolded project structure (`README`, `pyproject.toml`, `src/*`)
- map template files to runtime behavior
- understand naming/package conventions used by the generator
- keep customization changes isolated from generated boilerplate

## Structure Overview

| Path | Purpose |
|:-----|:--------|
| `README.md` | usage and integration instructions |
| `pyproject.toml` | packaging and dependency definition |
| `src/<package>/server.py` | MCP primitives and handler logic |

## Source References

- [Create Python Server README](https://github.com/modelcontextprotocol/create-python-server/blob/main/README.md)
- [Template README](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/README.md.jinja2)

## Summary

You now have a structural map for generated MCP Python server projects.

Next: [Chapter 3: Template Server Architecture: Resources, Prompts, and Tools](03-template-server-architecture-resources-prompts-and-tools.md)
