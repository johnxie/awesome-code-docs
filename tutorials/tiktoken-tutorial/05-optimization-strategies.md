---
layout: default
title: "Chapter 5: Optimization Strategies"
nav_order: 5
parent: tiktoken Tutorial
---

# Chapter 5: Optimization Strategies

Welcome to **Chapter 5: Optimization Strategies**. In this part of **tiktoken Tutorial: OpenAI Token Encoding & Optimization**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

Next: [Chapter 6: ChatML and Tool Call Accounting](06-chatml-and-tool-calls.md)

Related:
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/)
- [LangChain Tutorial](../langchain-tutorial/)
- [LlamaIndex Tutorial](../llamaindex-tutorial/)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `text`, `encode`, `tiktoken` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Optimization Strategies` as an operating subsystem inside **tiktoken Tutorial: OpenAI Token Encoding & Optimization**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `lru_cache`, `texts`, `encoding_for_model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Optimization Strategies` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `text`.
2. **Input normalization**: shape incoming data so `encode` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `tiktoken`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [tiktoken repository](https://github.com/openai/tiktoken)
  Why it matters: authoritative reference on `tiktoken repository` (github.com).

Suggested trace strategy:
- search upstream code for `text` and `encode` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Educational Module](04-educational-module.md)
- [Next Chapter: Chapter 6: ChatML and Tool Call Accounting](06-chatml-and-tool-calls.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
