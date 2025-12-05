---
layout: default
title: "Langfuse Tutorial - Chapter 3: Prompt Management"
nav_order: 3
has_children: false
parent: Langfuse Tutorial
---

# Chapter 3: Prompt Management

> Version, release, and A/B test prompts directly from Langfuse.

## Overview

Langfuse lets you store prompts centrally, version them, and roll out changes without redeploying your app. You can fetch prompts at runtime and tag them with releases.

## Creating Prompts in Langfuse

In the UI, create a prompt named `support_reply` with variables:

```
Hello {{name}},
Thanks for reaching out about {{issue}}.
{{context}}
```

## Fetch and Use a Prompt (Python)

```python
from langfuse import Langfuse
from openai import OpenAI

langfuse = Langfuse(public_key="pk-...", secret_key="sk-...", host="https://cloud.langfuse.com")
client = OpenAI()

prompt = langfuse.get_prompt("support_reply", label="production")

messages = prompt.compile(
    {
        "name": "Alex",
        "issue": "billing error",
        "context": "We refunded invoice #123 and updated your card.",
    }
)

resp = client.responses.create(
    model="gpt-4o-mini",
    messages=messages,
)
```

- `label` selects a release (e.g., `production`, `beta`).
- `compile` renders the prompt with variables into chat messages.

## Versioning and Releases

- Each prompt change creates a new version.
- Labels (e.g., `production`, `staging`) point to versions; relabel to roll back instantly.
- Include the `prompt_version` in spans to track performance by version.

```python
trace.span(
    name="support-llm",
    input={"prompt_version": prompt.version},
)
```

## A/B Testing Prompts

```python
label = "production" if user_id % 2 == 0 else "beta"
prompt = langfuse.get_prompt("support_reply", label=label)
```

Use Langfuse analytics to compare response quality, latency, and cost by label.

## Prompt Safety Tips

- Keep variables well-defined; document types and examples in the prompt description.
- Avoid exposing secrets in prompt variables.
- Pair prompt changes with evaluation (Chapter 4) before rolling to `production`.

Next: evaluate outputs with LLM judges and human feedback. 
