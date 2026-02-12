---
layout: default
title: "Chapter 4: MCP Connectivity and Client Integration"
nav_order: 4
parent: GenAI Toolbox Tutorial
---

# Chapter 4: MCP Connectivity and Client Integration

This chapter compares MCP transport options with native SDK integrations.

## Learning Goals

- configure stdio and HTTP-based MCP client connectivity
- understand current MCP-spec coverage and version compatibility notes
- identify features that are available in native SDK paths but not MCP
- choose integration mode by capability, not trend

## Integration Decision Rule

Use native Toolbox SDKs when you need Toolbox-specific auth/authorization features. Use MCP for host compatibility and interoperability where protocol constraints are acceptable.

## Source References

- [Connect via MCP](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/how-to/connect_via_mcp.md)
- [MCP Toolbox Extension README](https://github.com/googleapis/genai-toolbox/blob/main/MCP-TOOLBOX-EXTENSION.md)
- [README Integration Section](https://github.com/googleapis/genai-toolbox/blob/main/README.md)

## Summary

You now have a practical framework for choosing and operating Toolbox integration paths.

Next: [Chapter 5: Prebuilt Connectors and Database Patterns](05-prebuilt-connectors-and-database-patterns.md)
