---
layout: default
title: "Chapter 5: MCP, Extensions, and Skills"
nav_order: 5
parent: Gemini CLI Tutorial
---

# Chapter 5: MCP, Extensions, and Skills

This chapter covers extensibility through MCP servers, extension packs, and skills.

## Learning Goals

- configure and validate MCP server connections
- understand extension packaging and lifecycle controls
- install and manage skills across scopes
- apply safe defaults for third-party extension surfaces

## MCP Integration Basics

Configure MCP servers in Gemini settings and verify discovery:

- use `/mcp` for runtime visibility
- validate authentication and connection state per server
- test tool execution with low-risk read-only tasks first

## Extensions and Skills

- extensions package commands, hooks, MCP configs, and assets
- skills provide structured domain guidance with controlled activation
- both can be managed from CLI command surfaces

## Security Baseline

- install only trusted sources
- keep extension inventory minimal and reviewed
- isolate experimental integrations from critical workflows

## Source References

- [MCP Server Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)
- [Extensions Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md)
- [Skills Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)

## Summary

You now have an extensibility model that balances capability and control.

Next: [Chapter 6: Headless Mode and CI Automation](06-headless-mode-and-ci-automation.md)
