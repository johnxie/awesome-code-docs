---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Python SDK Tutorial
---

# Chapter 1: Getting Started

This chapter gets you to a stable baseline with Responses API-first code.

## Install and Configure

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai
export OPENAI_API_KEY="your_api_key_here"
```

## First Responses API Call

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input="Summarize why idempotency matters in API design in 3 bullets."
)

print(response.output_text)
```

## Async Variant

```python
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI()
    resp = await client.responses.create(
        model="gpt-5.2",
        input="Give 3 tips for reliable background jobs."
    )
    print(resp.output_text)

asyncio.run(main())
```

## Baseline Production Controls

- set explicit client timeouts
- capture request IDs in logs
- keep secrets out of source control
- fail fast on invalid configuration

## Summary

You now have a working SDK setup with both sync and async Responses API calls.

Next: [Chapter 2: Chat Completions](02-chat-completions.md)
