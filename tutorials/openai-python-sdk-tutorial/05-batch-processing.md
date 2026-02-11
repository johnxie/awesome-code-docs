---
layout: default
title: "Chapter 5: Batch Processing"
nav_order: 5
parent: OpenAI Python SDK Tutorial
---

# Chapter 5: Batch Processing

Batch processing is useful for large asynchronous workloads where per-request latency is less important.

## Build Input File

```python
import json
from pathlib import Path

rows = [
    {
        "custom_id": "job-1",
        "method": "POST",
        "url": "/v1/responses",
        "body": {"model": "gpt-5.2", "input": "Summarize this incident report."}
    },
    {
        "custom_id": "job-2",
        "method": "POST",
        "url": "/v1/responses",
        "body": {"model": "gpt-5.2", "input": "Extract top 3 risks from this change plan."}
    }
]

path = Path("batch_input.jsonl")
with path.open("w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")
```

## Submit Batch

```python
from openai import OpenAI

client = OpenAI()

upload = client.files.create(file=open("batch_input.jsonl", "rb"), purpose="batch")
batch = client.batches.create(
    input_file_id=upload.id,
    endpoint="/v1/responses",
    completion_window="24h"
)
print(batch.id, batch.status)
```

## Operational Practices

- make `custom_id` deterministic for reconciliation
- shard very large jobs
- store both input and output artifacts
- alert on partial-failure rates

## Summary

You now have a scalable asynchronous processing pattern for bulk OpenAI workloads.

Next: [Chapter 6: Fine-Tuning](06-fine-tuning.md)
