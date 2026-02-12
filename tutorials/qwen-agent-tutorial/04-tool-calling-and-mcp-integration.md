---
layout: default
title: "Chapter 4: Tool Calling and MCP Integration"
nav_order: 4
parent: Qwen-Agent Tutorial
---

# Chapter 4: Tool Calling and MCP Integration

This chapter explains capability expansion through tools and MCP services.

## Learning Goals

- implement function-calling and custom tool patterns
- configure MCP servers for external tool access
- secure filesystem/database boundaries in MCP configs
- test MCP workflows with deterministic examples

## Integration Strategy

- start from known-good MCP configuration blocks
- add only required servers and permissions
- verify tool outputs with integration scripts before production use

## Source References

- [Core Modules: MCP](https://qwenlm.github.io/Qwen-Agent/en/guide/core_moduls/mcp/)
- [MCP SQLite Example](https://github.com/QwenLM/Qwen-Agent/blob/main/examples/assistant_mcp_sqlite_bot.py)
- [Function Calling Example](https://github.com/QwenLM/Qwen-Agent/blob/main/examples/function_calling.py)

## Summary

You now have a practical model for tool + MCP integration in Qwen-Agent.

Next: [Chapter 5: Memory, RAG, and Long-Context Workflows](05-memory-rag-and-long-context-workflows.md)
