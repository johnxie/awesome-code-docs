---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Python SDK Tutorial
---

# Chapter 1: Getting Started

This chapter sets up the OpenAI Python SDK and walks through your first successful API call.

## Goals

- Install the SDK in an isolated environment.
- Configure authentication safely.
- Make your first text-generation request.
- Understand response objects and common errors.

## Install and Configure

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai
```

Set your API key through environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## First Request

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a one-sentence summary of why typed APIs help in production."
)

print(response.output_text)
```

## Async Variant

```python
import asyncio
from openai import AsyncOpenAI

async def main() -> None:
    client = AsyncOpenAI()
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input="Give three short tips for robust API clients."
    )
    print(response.output_text)

asyncio.run(main())
```

## Response Basics

- `response.output_text`: convenient flattened text output.
- `response.id`: request identifier useful for support/debugging.
- `response.usage`: token usage metadata for cost tracking.

## Security and Ops Basics

- Never hardcode API keys in source files.
- Rotate keys and use environment-specific credentials.
- Add request logging with redaction for sensitive content.
- Use timeouts and retries in production paths.

## Common Errors

| Error | Cause | Fix |
|:------|:------|:----|
| `401 Unauthorized` | Missing/invalid API key | Re-export key and retry |
| `429 Too Many Requests` | Rate limit exceeded | Backoff + retry policy |
| `400 Bad Request` | Invalid request shape | Validate payload and model name |

## Quick Troubleshooting

```python
from openai import OpenAI

client = OpenAI(timeout=30.0)

try:
    r = client.responses.create(model="gpt-4.1-mini", input="health check")
    print(r.id)
except Exception as exc:
    print(type(exc).__name__, str(exc))
```

## Summary

You now have a working SDK installation, secure key loading, and both sync and async first calls.

Next: [Chapter 2: Chat Completions](02-chat-completions.md)
