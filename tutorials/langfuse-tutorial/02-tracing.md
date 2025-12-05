---
layout: default
title: "Langfuse Tutorial - Chapter 2: Tracing Fundamentals"
nav_order: 2
has_children: false
parent: Langfuse Tutorial
---

# Chapter 2: Tracing Fundamentals

> Capture traces, spans, and events with rich metadata to debug LLM flows.

## Overview

Langfuse traces represent a user request; spans represent steps (LLM calls, tools, DB). You can attach inputs/outputs, scores, tags, and user identifiers to make debugging easy.

## Core Concepts

- **Trace**: Root of a request or conversation.
- **Span**: A step within the trace (LLM call, tool, RAG retrieval).
- **Event**: A log or intermediate message.
- **Score**: A numeric value (0–1 or 0–100) for quality or success.

## Instrument a Multi-Step Flow

```python
from langfuse import Langfuse
from openai import OpenAI
import time

langfuse = Langfuse(public_key="pk-...", secret_key="sk-...", host="https://cloud.langfuse.com")
client = OpenAI()

trace = langfuse.trace(name="support-query", user_id="user_123", metadata={"plan": "pro"})

retrieval = trace.span(name="retrieval", input={"query": "reset password"}, tags=["rag"])
retrieval_output = ["Reset via settings", "Send reset email"]
time.sleep(0.1)
retrieval.end(output=retrieval_output)

llm = trace.span(name="llm-answer", input={"context": retrieval_output})
resp = client.responses.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Use this context to answer password reset question"}],
)
llm.end(output=resp.choices[0].message.content, usage=resp.usage.model_dump())

trace.score(name="helpfulness", value=0.92)
trace.end()
langfuse.flush()
```

## Attaching Metadata and Tags

```python
span = trace.span(
    name="tool-call",
    input={"cmd": "GET /users/123"},
    tags=["tool", "http"],
    metadata={"service": "users-api", "region": "us-east-1"},
)
```

Tags make searching and filtering easier in the UI.

## Logging Events

```python
event = trace.event(
    name="rerank",
    level="info",
    data={"before": 10, "after": 5},
)
```

Events are lightweight logs tied to a trace.

## Error Handling

```python
try:
    risky = trace.span(name="db-call")
    # do work...
    raise RuntimeError("timeout")
except Exception as e:
    risky.end(output={"error": str(e)}, status="error")
    trace.score(name="error", value=1, comment=str(e))
finally:
    trace.end()
    langfuse.flush()
```

Setting `status="error"` highlights failures in the UI.

## Tips

- Always set `user_id` to tie traces to users.
- Add `usage` for cost analysis.
- Use concise `name` values; they become filters in the UI.

Next: manage prompts with versions and releases. 
