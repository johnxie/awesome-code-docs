---
layout: default
title: "Chapter 3: Provider Configuration and Transformer Strategy"
nav_order: 3
parent: Claude Code Router Tutorial
---

# Chapter 3: Provider Configuration and Transformer Strategy

This chapter focuses on building reliable provider definitions and transformation pipelines.

## Learning Goals

- configure providers with environment-variable-safe secrets
- select transformers by provider API compatibility needs
- understand global vs model-scoped transformer application
- avoid brittle provider configs that fail under load

## Provider Configuration Essentials

| Field | Why It Matters |
|:------|:---------------|
| `name` | routing and model reference key |
| `api_base_url` | provider endpoint compatibility |
| `api_key` | secure auth, ideally via env interpolation |
| `models` | allowed model surface for routing |
| `transformer` | request/response compatibility adjustments |

## Source References

- [README: Configuration](https://github.com/musistudio/claude-code-router/blob/main/README.md#2-configuration)
- [README: Transformers](https://github.com/musistudio/claude-code-router/blob/main/README.md#transformers)
- [Server Config: Providers](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/config/providers.md)

## Summary

You now have a stable foundation for provider onboarding and transformer management.

Next: [Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic](04-routing-rules-fallbacks-and-custom-router-logic.md)
