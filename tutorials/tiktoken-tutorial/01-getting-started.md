---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: tiktoken Tutorial
---

# Chapter 1: Getting Started

This chapter introduces tiktoken and gets you productive with basic encode/decode and counting.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install tiktoken
```

## First Encode/Decode

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = "Tokenization makes cost estimation predictable."

ids = enc.encode(text)
print(ids)
print("token_count=", len(ids))
print("round_trip=", enc.decode(ids))
```

## Model-Specific Encoding

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4.1-mini")
print(len(enc.encode("hello world")))
```

## Why This Matters

- API cost is token-based.
- Context windows are token-limited.
- Retrieval chunking quality depends on token boundaries.

## Common Mistakes

| Mistake | Fix |
|:--------|:----|
| Using char counts as proxy | Always count actual tokens |
| Mixing encodings across pipelines | Standardize encoding per model |
| Ignoring special tokens | Include model-specific token behavior in tests |

## Summary

You now have the core encode/decode workflow and model-specific counting.

Next: [Chapter 2: Tokenization Mechanics](02-tokenization-mechanics.md)
