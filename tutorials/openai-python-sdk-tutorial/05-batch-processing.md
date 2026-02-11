---
layout: default
title: "Chapter 5: Batch Processing"
nav_order: 5
parent: OpenAI Python SDK Tutorial
---

# Chapter 5: Batch Processing

Batch jobs are useful when latency is less important than throughput and cost control.

## Prepare a JSONL Batch File

```python
import json
from pathlib import Path

rows = [
    {
        "custom_id": "task-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": "Summarize release notes in one sentence."}],
        },
    },
    {
        "custom_id": "task-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": "Extract three risks from this migration plan."}],
        },
    },
]

path = Path("batch_input.jsonl")
with path.open("w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")
```

## Upload and Start Batch

```python
from openai import OpenAI

client = OpenAI()

upload = client.files.create(file=open("batch_input.jsonl", "rb"), purpose="batch")
batch = client.batches.create(input_file_id=upload.id, endpoint="/v1/chat/completions", completion_window="24h")

print(batch.id, batch.status)
```

## Poll and Download Results

```python
from time import sleep

while batch.status in {"validating", "in_progress", "finalizing"}:
    sleep(5)
    batch = client.batches.retrieve(batch.id)

print("final status:", batch.status)
```

## Operational Tips

- Use `custom_id` for deterministic reconciliation.
- Split very large jobs into bounded shards.
- Keep input payloads normalized and validated.
- Store both input and output artifacts for replay.

## Summary

You can now run large asynchronous workloads with traceable batch artifacts.

Next: [Chapter 6: Fine-Tuning](06-fine-tuning.md)
