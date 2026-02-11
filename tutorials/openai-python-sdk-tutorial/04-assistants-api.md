---
layout: default
title: "Chapter 4: Assistants API"
nav_order: 4
parent: OpenAI Python SDK Tutorial
---

# Chapter 4: Assistants API

Assistants provide persistent threads and orchestrated runs for tool-enabled workflows.

## Core Objects

- **Assistant**: model + instructions + tools.
- **Thread**: stateful conversation container.
- **Run**: execution instance over a thread.

## Create Assistant and Thread

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Ops Assistant",
    model="gpt-4.1-mini",
    instructions="You are an SRE assistant focused on reliability.",
)

thread = client.beta.threads.create()

client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Give me a pre-deploy reliability checklist.",
)
```

## Run and Poll

```python
from time import sleep

run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

while run.status in {"queued", "in_progress"}:
    sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

## Tooling Considerations

- Use clear tool descriptions and bounded schemas.
- Enforce input validation before external side effects.
- Persist run IDs for auditability.
- Define timeout and cancellation behavior.

## Failure Modes

| Failure | Pattern |
|:--------|:--------|
| Run stuck in progress | Add max wait + cancellation fallback |
| Invalid tool args | Schema validation + defensive parsing |
| Missing context | Summarize prior thread state periodically |

## Summary

You can now operate assistants with persistent thread state and polling logic.

Next: [Chapter 5: Batch Processing](05-batch-processing.md)
