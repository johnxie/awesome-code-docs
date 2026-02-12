---
layout: default
title: "Chapter 3: Provider Integrations and Framework Mapping"
nav_order: 3
parent: Composio Tutorial
---

# Chapter 3: Provider Integrations and Framework Mapping

This chapter maps Composio provider options to concrete runtime and framework choices.

## Learning Goals

- choose a provider path aligned to your existing agent stack
- compare native-tool and MCP-backed integration flows
- design migration-friendly provider boundaries
- avoid lock-in to one framework-specific abstraction

## Integration Decision Table

| Scenario | Recommended Path |
|:---------|:-----------------|
| OpenAI Agents SDK runtime | OpenAI Agents provider with session tools |
| LangChain/LangGraph orchestration | LangChain provider for framework-native tools |
| Vercel AI SDK product stack | Vercel provider or MCP client path |
| mixed or evolving stack | keep Composio usage centered on sessions + explicit provider adapters |

## Practical Pattern

- prototype with one provider and one toolkit family
- document provider-specific tool object behavior
- keep execution contracts abstracted in your app service layer
- expand only after latency/reliability checks and auth validation

## Source References

- [OpenAI Agents Provider](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/providers/openai-agents.mdx)
- [LangChain Provider](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/providers/langchain.mdx)
- [Vercel AI SDK Provider](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/providers/vercel.mdx)

## Summary

You now have a framework-aware way to choose Composio provider integrations.

Next: [Chapter 4: Authentication and Connected Accounts](04-authentication-and-connected-accounts.md)
