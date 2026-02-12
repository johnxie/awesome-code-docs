---
layout: default
title: "Chapter 1: Getting Started and Scaffolding Workflow"
nav_order: 1
parent: Create Python Server Tutorial
---

# Chapter 1: Getting Started and Scaffolding Workflow

This chapter covers initial project generation and first-run commands.

## Learning Goals

- scaffold a new MCP Python server via `uvx create-mcp-server`
- understand prerequisites (`uv` tooling) and generated output
- run the generated server locally with minimal setup
- avoid onboarding drift across team environments

## Quick Start

```bash
uvx create-mcp-server
```

After generation, run `uv sync --dev --all-extras` and `uv run <server-name>` from the created project directory.

## Source References

- [Create Python Server README](https://github.com/modelcontextprotocol/create-python-server/blob/main/README.md)

## Summary

You now have a reproducible baseline for generating MCP Python server projects.

Next: [Chapter 2: Generated Project Structure and Conventions](02-generated-project-structure-and-conventions.md)
