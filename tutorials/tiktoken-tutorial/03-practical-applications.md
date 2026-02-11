---
layout: default
title: "Chapter 3: Practical Applications"
nav_order: 3
parent: tiktoken Tutorial
---

# Chapter 3: Practical Applications

Use token counting to manage cost, context limits, and RAG chunking.

## Cost Estimation

```python
import tiktoken

PRICE_PER_1K = 0.0003
enc = tiktoken.encoding_for_model("gpt-4.1-mini")

prompt = "Summarize this incident timeline with actions and owners."
tokens = len(enc.encode(prompt))
estimated_cost = (tokens / 1000.0) * PRICE_PER_1K

print(tokens, round(estimated_cost, 6))
```

## Safe Context Budgeting

```python
MODEL_LIMIT = 128000
RESPONSE_BUDGET = 2000

prompt_tokens = len(enc.encode(prompt))
remaining = MODEL_LIMIT - RESPONSE_BUDGET - prompt_tokens
print("max_context_tokens=", max(0, remaining))
```

## Token-Aware Chunking

```python
def token_chunks(text: str, chunk_size: int, overlap: int):
    ids = enc.encode(text)
    i = 0
    while i < len(ids):
        window = ids[i:i + chunk_size]
        yield enc.decode(window)
        if i + chunk_size >= len(ids):
            break
        i += max(1, chunk_size - overlap)
```

## Summary

You can now budget cost, enforce context limits, and chunk by tokens.

Next: [Chapter 4: Educational Module](04-educational-module.md)
