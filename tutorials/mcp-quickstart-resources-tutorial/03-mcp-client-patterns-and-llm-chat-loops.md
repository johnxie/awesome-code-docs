---
layout: default
title: "Chapter 3: MCP Client Patterns and LLM Chat Loops"
nav_order: 3
parent: MCP Quickstart Resources Tutorial
---

# Chapter 3: MCP Client Patterns and LLM Chat Loops

This chapter covers client-side flows for connecting to MCP servers and exposing tool calls in chat UX.

## Learning Goals

- compare client behavior across Go/Python/TypeScript examples
- map MCP tool discovery to conversational interaction loops
- handle absent credentials and fallback behavior safely
- design adapter layers for provider-specific LLM APIs

## Client Design Guardrails

- isolate MCP transport logic from model-provider wrappers.
- keep tool call schemas strict and explicit.
- fail gracefully when API keys or external services are unavailable.

## Source References

- [MCP Client (Go)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/mcp-client-go/README.md)
- [MCP Client (Python)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/mcp-client-python/README.md)
- [MCP Client (TypeScript)](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/mcp-client-typescript/README.md)

## Summary

You now have a practical MCP client loop model for chatbot-oriented integrations.

Next: [Chapter 4: Protocol Flow and stdio Transport Behavior](04-protocol-flow-and-stdio-transport-behavior.md)
