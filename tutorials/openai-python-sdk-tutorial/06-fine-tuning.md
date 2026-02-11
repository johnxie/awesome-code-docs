---
layout: default
title: "Chapter 6: Fine-Tuning"
nav_order: 6
parent: OpenAI Python SDK Tutorial
---

# Chapter 6: Fine-Tuning

Fine-tuning is valuable when prompt engineering alone cannot deliver consistent domain behavior.

## Dataset Quality Rules

- keep labels consistent and unambiguous
- remove contradictory samples
- include hard negatives and edge cases
- maintain a held-out evaluation set

## Job Submission Pattern

```python
from openai import OpenAI

client = OpenAI()

train_file = client.files.create(file=open("train.jsonl", "rb"), purpose="fine-tune")
job = client.fine_tuning.jobs.create(
    training_file=train_file.id,
    model="gpt-4.1-mini"
)
print(job.id, job.status)
```

## Evaluation Focus

Measure:

- task accuracy on held-out data
- failure-type distribution
- cost/latency impact vs base model
- regression risk on adjacent tasks

## Summary

You now have a pragmatic fine-tuning workflow from data curation to job monitoring and evaluation.

Next: [Chapter 7: Advanced Patterns](07-advanced-patterns.md)
