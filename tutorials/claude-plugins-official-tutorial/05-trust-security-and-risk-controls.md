---
layout: default
title: "Chapter 5: Trust, Security, and Risk Controls"
nav_order: 5
parent: Claude Plugins Official Tutorial
---

# Chapter 5: Trust, Security, and Risk Controls

This chapter focuses on safe plugin adoption and third-party risk controls.

## Learning Goals

- evaluate trust boundaries before plugin installation
- apply security controls for plugins with MCP/tool integrations
- document risk posture for internal approval workflows
- reduce blast radius of plugin misbehavior

## Baseline Risk Controls

- install only trusted and reviewed plugins
- audit plugin README and metadata before install
- inspect `.mcp.json` and hook behaviors for sensitive operations
- isolate experimental plugins from production-critical workflows

## Operational Safety Pattern

- pilot plugins in non-critical projects first
- require explicit approval for plugins with external network actions
- maintain an allowlist of approved plugin names and versions

## Source References

- [Directory Trust Warning](https://github.com/anthropics/claude-plugins-official/blob/main/README.md)
- [Official Plugin Docs](https://code.claude.com/docs/en/plugins)
- [External Plugins Directory](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins)

## Summary

You now have a practical safety model for directory plugin adoption.

Next: [Chapter 6: Installation, Operations, and Update Strategy](06-installation-operations-and-update-strategy.md)
