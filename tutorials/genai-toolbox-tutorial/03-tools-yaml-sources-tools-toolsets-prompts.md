---
layout: default
title: "Chapter 3: `tools.yaml`: Sources, Tools, Toolsets, Prompts"
nav_order: 3
parent: GenAI Toolbox Tutorial
---

# Chapter 3: `tools.yaml`: Sources, Tools, Toolsets, Prompts

This chapter focuses on building maintainable configuration contracts in `tools.yaml`.

## Learning Goals

- model sources cleanly and avoid hardcoded secrets
- define tools with safe parameters and clear descriptions
- group capabilities into toolsets for context-specific loading
- add prompt templates for repeatable model instruction patterns

## Configuration Rule

Treat `tools.yaml` as a versioned interface contract. Keep it small, explicit, and environment-variable driven to avoid hidden coupling and credential leakage.

## Source References

- [Configuration Guide](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/getting-started/configure.md)
- [README Configuration](https://github.com/googleapis/genai-toolbox/blob/main/README.md)

## Summary

You can now design `tools.yaml` schemas that stay readable and stable as capabilities grow.

Next: [Chapter 4: MCP Connectivity and Client Integration](04-mcp-connectivity-and-client-integration.md)
