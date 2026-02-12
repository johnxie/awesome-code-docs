---
layout: default
title: "Chapter 3: Installation Across Host Clients"
nav_order: 3
parent: Playwright MCP Tutorial
---

# Chapter 3: Installation Across Host Clients

This chapter shows how to reuse one conceptual setup across multiple MCP host clients.

## Learning Goals

- map standard configuration to host-specific install flows
- avoid host-specific assumptions that break portability
- keep one canonical server profile across environments
- accelerate team onboarding across mixed toolchains

## Host Coverage in README

The upstream README provides setup patterns for Claude, Codex, Cursor, Copilot, Goose, Gemini CLI, Warp, Windsurf, and more.

## Portability Pattern

- maintain a canonical `npx @playwright/mcp@latest` baseline
- only vary config syntax required by each host
- keep capability and security flags consistent across hosts

## Source References

- [README: Client Installation Sections](https://github.com/microsoft/playwright-mcp/blob/main/README.md#getting-started)
- [Codex MCP Config Example](https://github.com/microsoft/playwright-mcp/blob/main/README.md#for-openai-codex)

## Summary

You now have a host-portable installation strategy for Playwright MCP.

Next: [Chapter 4: Configuration, Capabilities, and Runtime Modes](04-configuration-capabilities-and-runtime-modes.md)
