---
layout: default
title: "Chapter 8: Integration Examples"
nav_order: 8
parent: OpenAI Python SDK Tutorial
---

# Chapter 8: Integration Examples

This chapter shows composable integration patterns you can adapt directly.

## Example 1: FastAPI Inference Endpoint

```python
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client = OpenAI()

@app.post("/summarize")
def summarize(payload: dict):
    text = payload.get("text", "")
    r = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize in 3 bullet points:\n\n{text}",
    )
    return {"summary": r.output_text, "request_id": r.id}
```

## Example 2: Lightweight RAG Flow

```python
from openai import OpenAI

client = OpenAI()

def embed(texts):
    data = client.embeddings.create(model="text-embedding-3-small", input=texts).data
    return [x.embedding for x in data]

def answer(question, retrieved_context):
    prompt = f"Context:\n{retrieved_context}\n\nQuestion: {question}"
    r = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return r.output_text
```

## Example 3: Guarded Tool Execution Loop

```python
import json

def safe_weather_tool(args_json: str) -> str:
    args = json.loads(args_json)
    city = args.get("city", "")
    if not city or len(city) > 100:
        return "invalid city"
    return f"Weather for {city}: clear, 58F"
```

## Launch Checklist

- Contract tests for request/response payloads.
- Cost budget alerts and tenant-level quotas.
- Eval set for output quality and regressions.
- Incident runbook for degraded model/provider behavior.

## Final Summary

You now have end-to-end foundations: setup, chat, embeddings, assistants, batch, tuning, reliability, and app integration.

Related:
- [tiktoken Tutorial](../tiktoken-tutorial/)
- [OpenAI Whisper Tutorial](../openai-whisper-tutorial/)
- [OpenAI Realtime Agents Tutorial](../openai-realtime-agents-tutorial/)
