---
layout: default
title: "Chapter 4: Permissions and Tool Controls"
nav_order: 4
parent: Crush Tutorial
---

# Chapter 4: Permissions and Tool Controls

This chapter covers how to define safe execution boundaries without killing productivity.

## Learning Goals

- set explicit tool-permission policies in Crush
- constrain high-risk tools and commands
- understand `--yolo` mode risks
- use ignore rules to reduce accidental context exposure

## Permission Controls

| Control | Location | Purpose |
|:--------|:---------|:--------|
| `permissions.allowed_tools` | config | allow safe tools to run without repeated prompts |
| `options.disabled_tools` | config | fully hide high-risk or irrelevant built-in tools |
| `disabled_tools` under MCP configs | config | disable specific MCP-exposed tools |
| `--yolo` | CLI flag | bypass prompts; use only in trusted environments |

## Practical Safety Baseline

1. default to prompts for write/destructive actions
2. disable tools not required for your current task class
3. use `.crushignore` to exclude large/noisy/sensitive paths
4. reserve `--yolo` for disposable sandboxes

## Source References

- [Crush README: Allowing Tools](https://github.com/charmbracelet/crush/blob/main/README.md#allowing-tools)
- [Crush README: Disabling Built-In Tools](https://github.com/charmbracelet/crush/blob/main/README.md#disabling-built-in-tools)
- [Crush README: Ignoring Files](https://github.com/charmbracelet/crush/blob/main/README.md#ignoring-files)

## Summary

You now have a practical control model for balancing Crush autonomy and safety.

Next: [Chapter 5: LSP and MCP Integration](05-lsp-and-mcp-integration.md)
