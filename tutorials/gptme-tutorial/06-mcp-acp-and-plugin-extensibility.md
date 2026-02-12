---
layout: default
title: "Chapter 6: MCP, ACP, and Plugin Extensibility"
nav_order: 6
parent: gptme Tutorial
---

# Chapter 6: MCP, ACP, and Plugin Extensibility

gptme supports protocol and plugin extensions for richer integrations with external tools and clients.

## Extension Surfaces

- MCP integration for external tool servers
- ACP components for agent-client protocol use
- plugin system for packaged capabilities

## Strategy

- start with minimal plugin footprint
- audit MCP tool trust before enabling write-capable actions
- version extension dependencies with the same rigor as app code

## Source References

- [MCP docs](https://github.com/gptme/gptme/blob/master/docs/mcp.rst)
- [ACP docs](https://github.com/gptme/gptme/blob/master/docs/acp.rst)
- [Plugins docs](https://github.com/gptme/gptme/blob/master/docs/plugins.rst)

## Summary

You now have an extensibility model for connecting gptme to broader tool ecosystems.

Next: [Chapter 7: Automation, Server Mode, and Agent Templates](07-automation-server-mode-and-agent-templates.md)
