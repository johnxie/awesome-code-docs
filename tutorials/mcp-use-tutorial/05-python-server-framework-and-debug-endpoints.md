---
layout: default
title: "Chapter 5: Python Server Framework and Debug Endpoints"
nav_order: 5
parent: MCP Use Tutorial
---

# Chapter 5: Python Server Framework and Debug Endpoints

mcp-use Python server flows prioritize compatibility with official SDK behavior while adding stronger developer diagnostics.

## Learning Goals

- create MCP servers with tool decorators and transport selection
- use debug endpoints (`/inspector`, `/docs`, `/openmcp.json`) during development
- separate stdio vs streamable-http modes by deployment needs
- keep migration paths clear for existing official SDK users

## Python Server Pattern

- use stdio for local host-client integrations
- use streamable-http for remote or shared environments
- enable debug mode in development only
- validate tool behavior via inspector before production rollout

## Source References

- [Python Server Intro](https://github.com/mcp-use/mcp-use/blob/main/docs/python/server/index.mdx)
- [Python Quickstart](https://github.com/mcp-use/mcp-use/blob/main/docs/python/getting-started/quickstart.mdx)
- [Python README](https://github.com/mcp-use/mcp-use/blob/main/libraries/python/README.md)

## Summary

You now have a practical Python server development and debugging baseline.

Next: [Chapter 6: Inspector Debugging and Chat App Workflows](06-inspector-debugging-and-chat-app-workflows.md)
