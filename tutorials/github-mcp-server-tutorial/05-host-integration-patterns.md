---
layout: default
title: "Chapter 5: Host Integration Patterns"
nav_order: 5
parent: GitHub MCP Server Tutorial
---

# Chapter 5: Host Integration Patterns

This chapter maps integration patterns across major MCP hosts.

## Learning Goals

- identify host-specific installation nuances quickly
- standardize configuration practices across teams
- avoid brittle host assumptions during rollout
- maintain one conceptual model with host-specific syntax

## Common Host Targets

- Claude Code and Claude Desktop
- Codex
- Cursor and Windsurf
- Copilot CLI and other Copilot IDE surfaces

## Integration Principle

Keep one canonical server policy (toolsets, read-only defaults, auth model), then adapt host syntax only at the configuration boundary.

## Source References

- [Installation Guides](https://github.com/github/github-mcp-server/tree/main/docs/installation-guides)
- [Install in Claude Applications](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)
- [Install in Codex](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md)

## Summary

You now have a host-portable integration strategy for GitHub MCP.

Next: [Chapter 6: Security, Governance, and Enterprise Controls](06-security-governance-and-enterprise-controls.md)
