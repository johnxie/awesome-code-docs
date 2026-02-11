---
layout: default
title: "Chapter 2: Tokenization Mechanics"
nav_order: 2
parent: tiktoken Tutorial
---

# Chapter 2: Tokenization Mechanics

This chapter explains how BPE tokenization works and why token boundaries look unintuitive.

## BPE Intuition

Byte Pair Encoding (BPE) builds subword units from frequent patterns.

- Frequent substrings become single tokens.
- Rare words split into multiple tokens.
- Spaces and punctuation can be encoded as separate units.

## Inspect Token Pieces

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = "Kubernetes operators improve day-2 reliability."

ids = enc.encode(text)
for token_id in ids:
    piece = enc.decode([token_id])
    print(token_id, repr(piece))
```

## Unicode and Edge Cases

```python
samples = ["naive", "naive cafe", "naive cafe ☕", "emoji: 😀"]
for s in samples:
    print(s, len(enc.encode(s)))
```

## Practical Implications

- Prompt rewrites can change token count materially.
- Structured output formats may be more token-efficient.
- Localization can shift cost due to token distribution.

## Summary

You understand how token pieces are formed and how to inspect them.

Next: [Chapter 3: Practical Applications](03-practical-applications.md)
