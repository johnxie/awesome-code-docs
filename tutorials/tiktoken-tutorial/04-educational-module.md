---
layout: default
title: "Chapter 4: Educational Module"
nav_order: 4
parent: tiktoken Tutorial
---

# Chapter 4: Educational Module

The educational module helps you visualize and understand tokenization internals.

## Explore the Educational API

```python
from tiktoken._educational import SimpleBytePairEncoding

corpus = """
incident response runbook reliability oncall escalation
incident review postmortem runbook reliability
"""

enc = SimpleBytePairEncoding.train(corpus, vocab_size=300)
ids = enc.encode("runbook reliability")
print(ids)
print(enc.decode(ids))
```

## What to Learn Here

- How merges change token boundaries.
- Why domain corpora influence tokenization efficiency.
- Why tokenizer design impacts downstream model behavior.

## Visualization Tip

Print token pieces for representative prompts before finalizing prompt templates.

```python
pieces = [enc.decode([i]) for i in ids]
print(pieces)
```

## Summary

You can now use the educational API to reason about BPE behavior.

Next: [Chapter 5: Optimization Strategies](05-optimization-strategies.md)
