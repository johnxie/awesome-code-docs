---
layout: default
title: "Chapter 6: React Integration Patterns: Chat UI and Inspector"
nav_order: 6
parent: use-mcp Tutorial
---

# Chapter 6: React Integration Patterns: Chat UI and Inspector

This chapter extracts reusable architecture patterns from official example apps.

## Learning Goals

- compare chat-oriented vs inspector-oriented integration approaches
- reuse server management, tool inspection, and prompt/resource panels
- structure app state to isolate MCP concerns from core product logic
- accelerate UI prototyping with known-good component boundaries

## Example Pattern Highlights

- **Inspector**: capability discovery/debug and operational visibility
- **Chat UI**: conversational tooling and server/session UX
- **Server examples**: reference backends for integration experiments

## Source References

- [Chat UI Example](https://github.com/modelcontextprotocol/use-mcp/blob/main/examples/chat-ui/README.md)
- [Inspector Example](https://github.com/modelcontextprotocol/use-mcp/blob/main/examples/inspector/README.md)
- [Hono MCP Server Example](https://github.com/modelcontextprotocol/use-mcp/blob/main/examples/servers/hono-mcp/README.md)
- [Cloudflare Agents Example](https://github.com/modelcontextprotocol/use-mcp/blob/main/examples/servers/cf-agents/README.md)

## Summary

You now have an example-driven component architecture model for MCP-enabled React apps.

Next: [Chapter 7: Testing, Debugging, and Integration Servers](07-testing-debugging-and-integration-servers.md)
