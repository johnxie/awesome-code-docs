---
layout: default
title: "Chapter 8: Integration Examples"
nav_order: 8
parent: OpenAI Python SDK Tutorial
---

# Chapter 8: Integration Examples

This chapter maps core SDK features to service-level integration patterns.

## Example 1: FastAPI Summarization Endpoint

```python
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client = OpenAI()

@app.post("/summarize")
def summarize(payload: dict):
    text = payload.get("text", "")
    resp = client.responses.create(
        model="gpt-5.2",
        input=f"Summarize in 3 bullet points:\n\n{text}",
    )
    return {"summary": resp.output_text, "request_id": resp.id}
```

## Example 2: Retrieval-Enhanced Endpoint

- retrieve top-k context from embeddings index
- construct compact context block
- generate answer with citation fields
- return both answer and source metadata

## Example 3: Tool-Gated Action Endpoint

- classify requested action risk
- require explicit confirmation for destructive operations
- run tool with bounded timeout
- log inputs and outputs for audit

## Final Launch Checklist

- contract tests for request/response schemas
- regression eval set for output quality
- budget alerts and rate-limit handling
- incident runbook for degraded provider behavior

## Final Summary

You now have an end-to-end blueprint for shipping Python SDK integrations that are reliable, observable, and migration-ready.

Related:
- [tiktoken Tutorial](../tiktoken-tutorial/)
- [OpenAI Realtime Agents Tutorial](../openai-realtime-agents-tutorial/)
- [OpenAI Whisper Tutorial](../openai-whisper-tutorial/)
