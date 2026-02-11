---
layout: default
title: "Chapter 2: Chat Completions"
nav_order: 2
parent: OpenAI Python SDK Tutorial
---

# Chapter 2: Chat Completions

Chat Completions remains important for existing systems even as new builds move to Responses-first flows.

## Basic Message-Based Request

```python
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5.2",
    messages=[
        {"role": "developer", "content": "Be concise and structured."},
        {"role": "user", "content": "Explain exponential backoff in 2 bullets."}
    ]
)

print(completion.choices[0].message.content)
```

## Streaming Pattern

```python
stream = client.chat.completions.create(
    model="gpt-5.2",
    messages=[{"role": "user", "content": "List 5 SRE runbook checks."}],
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta
    if delta and delta.content:
        print(delta.content, end="", flush=True)
```

## When to Keep Chat Completions

- existing production systems with stable message middleware
- deeply integrated toolchains using current message schemas
- migration phases where Responses API adoption is incremental

## When to Prefer Responses

- new services
- multimodal and unified response flows
- systems that need cleaner forward compatibility with current OpenAI platform direction

## Summary

You can now support legacy/interoperable message workflows while planning Responses-first migration.

Next: [Chapter 3: Embeddings and Search](03-embeddings-search.md)
