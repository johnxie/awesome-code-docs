---
layout: default
title: "Chapter 3: Model Serving and Completion Pipeline"
nav_order: 3
parent: Tabby Tutorial
---

# Chapter 3: Model Serving and Completion Pipeline

This chapter focuses on how Tabby combines completion, chat, and embedding configuration into practical response quality.

## Learning Goals

- separate completion and chat model responsibilities
- configure HTTP model providers correctly
- choose safe defaults for latency and quality

## Model Roles in Tabby

| Model Type | Typical Purpose |
|:-----------|:----------------|
| completion model | inline code completion and edit suggestions |
| chat model | assistant responses and interactive reasoning |
| embedding model | retrieval and repository/document context matching |

## Example Configuration Strategy

```toml
# ~/.tabby/config.toml
[model.chat.http]
kind = "openai/chat"
model_name = "gpt-4o"
api_endpoint = "https://api.openai.com/v1"
api_key = "${OPENAI_API_KEY}"

[model.embedding.http]
kind = "openai/embedding"
model_name = "text-embedding-3-small"
api_endpoint = "https://api.openai.com/v1"
api_key = "${OPENAI_API_KEY}"
```

Use a completion-capable model path that matches your deployment target (local model or compatible API).

## Tuning Priorities

1. stabilize response time first
2. validate completion relevance in real repositories
3. tune model size and provider routing after baseline quality is stable

## Common Tradeoffs

| Decision | Benefit | Cost |
|:---------|:--------|:-----|
| smaller local completion model | lower latency and lower infra cost | weaker long-context quality |
| remote high-capability chat model | better reasoning for chat workflows | network and usage cost |
| shared provider for all roles | simpler operations | less control per workload |

## Source References

- [Config TOML](https://tabby.tabbyml.com/docs/administration/config-toml)
- [OpenAI HTTP API Reference in Tabby Docs](https://tabby.tabbyml.com/docs/references/models-http-api/openai)
- [Tabby Models Directory](https://tabby.tabbyml.com/docs/models)

## Summary

You now understand how model role separation drives both quality and operational cost.

Next: [Chapter 4: Answer Engine and Context Indexing](04-answer-engine-and-context-indexing.md)
