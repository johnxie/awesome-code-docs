---
layout: default
title: "Instructor Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Instructor Tutorial
---

# Chapter 1: Getting Started with Instructor

> Install Instructor, patch your LLM client, and return your first typed object with Pydantic validation.

## Overview

Instructor wraps your LLM client (OpenAI, Anthropic, etc.) so that prompts return structured, validated objects instead of free-form text. You define a Pydantic model, Instructor enforces it, and retries until the response matches the schema.

### What You Will Build

- Install and patch the OpenAI client with Instructor.
- Define your first `BaseModel`.
- Call the LLM and receive a validated Python object instead of raw JSON strings.

## Prerequisites

- Python 3.9+
- An API key for your chosen provider (OpenAI in this chapter)
- `pipx` or `pip` for installation

## Install Instructor

```bash
pip install instructor openai pydantic>=2.6
```

If you prefer isolation:

```bash
python -m venv .venv
source .venv/bin/activate
pip install instructor openai pydantic>=2.6
```

## Patch the OpenAI Client

Instructor patches the client to add a `responses` helper that returns typed objects.

```python
# app.py
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

# Patch the OpenAI client
client = instructor.from_openai(OpenAI(api_key="sk-..."))

class Todo(BaseModel):
    title: str = Field(..., description="short task title")
    priority: str = Field(..., description="one of: low, medium, high")
    done: bool = False

resp = client.responses.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Add a todo for shipping docs, high priority"}],
    response_model=Todo,
)

print(resp)
# Todo(title='Ship docs', priority='high', done=False)
print(resp.model_dump())
# {'title': 'Ship docs', 'priority': 'high', 'done': False}
```

## How It Works

1. Instructor wraps the client and injects a guardrail to enforce `response_model`.
2. The LLM is prompted with your schema and asked to comply.
3. The raw LLM output is validated by Pydantic.
4. If validation fails, Instructor retries with error hints until it succeeds or reaches the retry limit.

## Quick CLI Smoke Test

```bash
python app.py
```

If you see a `Todo(...)` object printed, your setup is working.

## Troubleshooting

- **401 Unauthorized**: Ensure `OPENAI_API_KEY` is set and not expired.
- **Validation errors**: Confirm the schema matches your expectations; add field descriptions to guide the model.
- **Model selection**: Use a reliable model (e.g., `gpt-4o` or `gpt-4o-mini`). Smaller models may need clearer descriptions.

Next: dive deeper into designing Pydantic models that make LLM outputs precise and reliable.
