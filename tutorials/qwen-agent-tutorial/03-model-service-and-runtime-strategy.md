---
layout: default
title: "Chapter 3: Model Service and Runtime Strategy"
nav_order: 3
parent: Qwen-Agent Tutorial
---

# Chapter 3: Model Service and Runtime Strategy

This chapter covers model-serving choices and runtime tradeoffs.

## Learning Goals

- choose DashScope or self-hosted OpenAI-compatible backends
- configure model parser modes appropriately
- align runtime choice with throughput and cost constraints
- avoid parser/config mismatches in tool-calling flows

## Runtime Strategy Notes

- DashScope for managed-service simplicity
- vLLM/SGLang paths for self-hosted performance control
- parser mode must align with model family and deployment mode

## Source References

- [Quickstart: Model Service Prep](https://qwenlm.github.io/Qwen-Agent/en/guide/get_started/quickstart/)
- [Qwen-Agent Configuration Guide](https://qwenlm.github.io/Qwen-Agent/en/guide/get_started/configuration/)
- [Qwen-Agent README Runtime Notes](https://github.com/QwenLM/Qwen-Agent/blob/main/README.md)

## Summary

You now can pick model service and parser strategies with fewer integration surprises.

Next: [Chapter 4: Tool Calling and MCP Integration](04-tool-calling-and-mcp-integration.md)
