---
layout: default
title: "Chapter 2: Chat Completions"
nav_order: 2
parent: OpenAI Python SDK Tutorial
---

# Chapter 2: Chat Completions

This chapter covers message-based interactions, streaming output, and tool/function calling patterns.

## Message-Based Requests

```python
from openai import OpenAI

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Explain exponential backoff in two bullets."},
]

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    temperature=0.2,
)

print(response.choices[0].message.content)
```

## Streaming

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "List five API reliability checks."}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta
    if delta and delta.content:
        print(delta.content, end="", flush=True)
print()
```

## Tool Calling Pattern

```python
import json
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather by city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}]

resp = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "What is the weather in Seattle?"}],
    tools=tools,
    tool_choice="auto",
)

choice = resp.choices[0].message
if choice.tool_calls:
    call = choice.tool_calls[0]
    args = json.loads(call.function.arguments)
    print("Tool requested:", call.function.name, args)
```

## Recommended Practices

- Keep system prompts short and explicit.
- Validate tool arguments before execution.
- Keep tool responses structured and bounded.
- Capture request IDs for incident triage.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|:--------|:--------|:----|
| Overlong prompts | Higher cost/latency | Summarize and chunk context |
| Missing tool schema validation | Runtime errors | Strict JSON schema checks |
| No streaming backpressure handling | UI freezes | Buffer and throttle rendering |

## Summary

You can now implement chat flows with streaming and function calls.

Next: [Chapter 3: Embeddings and Search](03-embeddings-search.md)
