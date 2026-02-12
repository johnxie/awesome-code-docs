---
layout: default
title: "Chapter 3: Provider Configuration and Transformer Strategy"
nav_order: 3
parent: Claude Code Router Tutorial
---

# Chapter 3: Provider Configuration and Transformer Strategy

This chapter covers building reliable provider definitions and transformer chains.

## Learning Goals

- configure providers with secure key handling
- apply transformer choices by provider compatibility needs
- understand global vs scoped transformation behavior
- avoid brittle cross-provider configuration patterns

## Provider Baseline

| Field | Role |
|:------|:-----|
| `name` | routing identifier |
| `api_base_url` | provider endpoint |
| `api_key` | authentication secret |
| `models` | allowed model surface |
| `transformer` | protocol compatibility adjustments |

## Source References

- [README: Configuration](https://github.com/musistudio/claude-code-router/blob/main/README.md#2-configuration)
- [README: Transformers](https://github.com/musistudio/claude-code-router/blob/main/README.md#transformers)
- [Providers Config Docs](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/config/providers.md)

## Summary

You now have a safer strategy for provider and transformer setup.

Next: [Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic](04-routing-rules-fallbacks-and-custom-router-logic.md)
