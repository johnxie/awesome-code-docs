---
layout: default
title: "Chapter 8: Security and Team Governance"
nav_order: 8
parent: Cipher Tutorial
---

# Chapter 8: Security and Team Governance

Team usage of Cipher requires explicit controls over secrets, memory write behavior, and MCP tool exposure.

## Governance Checklist

1. keep API keys and vector-store secrets in secure env management
2. define policy for memory extraction/update permissions
3. review MCP server/tool additions before enabling in shared environments
4. partition workspace memory scope by team or project boundaries
5. audit logs and memory retention behavior regularly

## Source References

- [Cipher configuration docs](https://github.com/campfirein/cipher/blob/main/docs/configuration.md)
- [Cipher MCP integration docs](https://github.com/campfirein/cipher/blob/main/docs/mcp-integration.md)

## Summary

You now have a governance baseline for production Cipher deployments across teams and tools.
