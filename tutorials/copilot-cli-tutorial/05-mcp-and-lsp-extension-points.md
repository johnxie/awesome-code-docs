---
layout: default
title: "Chapter 5: MCP and LSP Extension Points"
nav_order: 5
parent: GitHub Copilot CLI Tutorial
---

# Chapter 5: MCP and LSP Extension Points

Copilot CLI is extensible through MCP servers and optional LSP configuration.

## Extension Surfaces

| Surface | Purpose |
|:--------|:--------|
| MCP | external tools/services via protocol integration |
| LSP | richer code intelligence in supported languages |

## LSP Configuration Paths

- user-level: `~/.copilot/lsp-config.json`
- repository-level: `.github/lsp.json`

## Source References

- [Copilot CLI README: MCP and custom MCP support](https://github.com/github/copilot-cli/blob/main/README.md)
- [Copilot CLI README: LSP configuration](https://github.com/github/copilot-cli/blob/main/README.md#-configuring-lsp-servers)

## Summary

You now have a practical model for extending Copilot CLI with external tools and language intelligence.

Next: [Chapter 6: GitHub-Native Context Workflows](06-github-native-context-workflows.md)
