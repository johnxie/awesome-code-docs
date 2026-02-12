---
layout: default
title: "Chapter 3: MCP Client Integrations"
nav_order: 3
parent: Serena Tutorial
---

# Chapter 3: MCP Client Integrations

This chapter shows how Serena is deployed as a shared capability layer across different agent surfaces.

## Learning Goals

- connect Serena with terminal, desktop, and IDE clients
- choose integration style for your workflow constraints
- use MCP transport assumptions safely
- standardize client setup for team onboarding

## Supported Integration Surfaces

Serena documentation and README list integrations with:

- Claude Code / Claude Desktop
- Codex and other terminal MCP clients
- VS Code / Cursor / IntelliJ class IDEs
- Cline / Roo Code extensions
- local GUI clients and framework integrations

## Integration Decision Matrix

| Environment | Preferred Integration |
|:------------|:----------------------|
| terminal-heavy developer flow | CLI MCP client + Serena |
| IDE-centric flow | MCP-enabled IDE + Serena |
| mixed team tooling | standard Serena launch profile shared across clients |

## Source References

- [Connecting Your MCP Client](https://oraios.github.io/serena/02-usage/030_clients.html)
- [Serena README: LLM Integration](https://github.com/oraios/serena/blob/main/README.md#llm-integration)

## Summary

You now know how Serena fits across multiple agent clients without locking into a single UI.

Next: [Chapter 4: Language Backends and Analysis Strategy](04-language-backends-and-analysis-strategy.md)
