---
layout: default
title: "Instructor Tutorial - Chapter 6: Multiple Providers"
nav_order: 6
has_children: false
parent: Instructor Tutorial
---

# Chapter 6: Using Multiple Providers

> Swap between OpenAI, Anthropic, Google, and local models (Ollama) without changing schemas.

## Overview

Instructor supports multiple backends with a consistent API. You can route traffic by tenant, fallback between providers, or develop locally with Ollama.

## OpenAI (recap)

```python
import instructor
from openai import OpenAI
client = instructor.from_openai(OpenAI())
```

## Anthropic (Claude)

```python
import instructor
from anthropic import Anthropic

client = instructor.from_anthropic(Anthropic())

result = client.responses.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Summarize this release note"}],
    response_model=MyModel,
)
```

## Google (Gemini)

```python
import instructor
from google import genai

client = instructor.from_gemini(genai.Client())
```

Usage mirrors OpenAI: call `responses.create` with `response_model`.

## Local Development with Ollama

```python
import instructor
from openai import OpenAI

# Point OpenAI-compatible client to Ollama
ollama = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # placeholder
)

client = instructor.from_openai(ollama)

resp = client.responses.create(
    model="llama3.1",
    messages=[{"role": "user", "content": "Extract 3 key points"}],
    response_model=list[str],
)
```

## Routing by Tenant

```python
def client_for_tenant(tenant: str):
    if tenant == "enterprise":
        return instructor.from_anthropic(Anthropic())
    return instructor.from_openai(OpenAI())

client = client_for_tenant("enterprise")
```

## Fallback Strategy

```python
def safe_generate():
    try:
        return primary.responses.create(..., model="gpt-4o")
    except Exception:
        return backup.responses.create(..., model="claude-3-opus-20240229")
```

Keep schemas identical; only the client and model string change.

## Tips

- Match model strengths to tasks: fast models for routing, high-quality models for critical extraction.
- Normalize provider-specific errors; wrap with your own exceptions.
- Store provider/model choice in config to switch without code changes.

Next: advanced patterns to squeeze more reliability from Instructor. 
