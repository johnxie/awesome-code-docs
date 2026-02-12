---
layout: default
title: "Chapter 3: Authentication and Model Configuration"
nav_order: 3
parent: Codex CLI Tutorial
---

# Chapter 3: Authentication and Model Configuration

This chapter covers secure access patterns and model configuration controls.

## Learning Goals

- choose between ChatGPT sign-in and API key flows
- configure model defaults for task classes
- avoid auth/config drift across environments
- align access mode with team governance

## Configuration Priorities

- centralize config in `~/.codex/config.toml`
- document auth mode per environment
- pin stable defaults for reproducible sessions

## Source References

- [Codex Auth Docs](https://developers.openai.com/codex/auth#sign-in-with-an-api-key)
- [Codex Config Basic](https://developers.openai.com/codex/config-basic)
- [Codex Config Advanced](https://developers.openai.com/codex/config-advanced)

## Summary

You now have reliable authentication and configuration patterns for Codex CLI.

Next: [Chapter 4: Sandbox, Approvals, and MCP Integration](04-sandbox-approvals-and-mcp-integration.md)
