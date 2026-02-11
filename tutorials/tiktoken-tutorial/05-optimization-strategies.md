---
layout: default
title: "Chapter 5: Optimization Strategies"
nav_order: 5
parent: tiktoken Tutorial
---

# Chapter 5: Optimization Strategies

This chapter focuses on performance and operational optimization for token-heavy systems.

## Strategy 1: Reuse Encoders

```python
import tiktoken

ENC = tiktoken.encoding_for_model("gpt-4.1-mini")

def count_tokens(text: str) -> int:
    return len(ENC.encode(text))
```

## Strategy 2: Cache Common Counts

```python
from functools import lru_cache

@lru_cache(maxsize=20000)
def cached_count(text: str) -> int:
    return len(ENC.encode(text))
```

## Strategy 3: Batch Counting

```python
def count_many(texts):
    return [len(ENC.encode(t)) for t in texts]
```

## Strategy 4: Guardrails in CI

- Add tests for max prompt token budget.
- Fail builds when prompt templates exceed limits.
- Track token deltas for prompt changes.

## Production Checklist

- Fixed encoding strategy per model.
- Centralized counting utility in shared library.
- Caching for repeated templates.
- Alerting for sudden token-cost spikes.

## Final Summary

You now have a complete tiktoken workflow from basics to production optimization.

Related:
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/)
- [LangChain Tutorial](../langchain-tutorial/)
- [LlamaIndex Tutorial](../llamaindex-tutorial/)
