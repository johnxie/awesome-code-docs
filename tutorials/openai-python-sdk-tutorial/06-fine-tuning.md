---
layout: default
title: "Chapter 6: Fine-Tuning"
nav_order: 6
parent: OpenAI Python SDK Tutorial
---

# Chapter 6: Fine-Tuning

Fine-tuning helps adapt behavior to stable, repeatable patterns in your domain.

## Training Data Shape

Use JSONL examples with clear input-output behavior.

```json
{"messages": [{"role": "system", "content": "You are a support classifier."}, {"role": "user", "content": "Refund not received"}, {"role": "assistant", "content": "billing"}]}
{"messages": [{"role": "system", "content": "You are a support classifier."}, {"role": "user", "content": "Password reset loop"}, {"role": "assistant", "content": "auth"}]}
```

## Start a Job

```python
from openai import OpenAI

client = OpenAI()

train_file = client.files.create(file=open("train.jsonl", "rb"), purpose="fine-tune")

job = client.fine_tuning.jobs.create(
    training_file=train_file.id,
    model="gpt-4.1-mini",
)

print(job.id, job.status)
```

## Monitor and Evaluate

```python
job = client.fine_tuning.jobs.retrieve(job.id)
print(job.status)

for event in client.fine_tuning.jobs.list_events(job.id).data[:5]:
    print(event.message)
```

## Best Practices

- Keep labels consistent and unambiguous.
- Remove contradictory examples.
- Hold out a validation set for regression checks.
- Compare tuned vs base model on production-like tasks.

## Common Issues

| Issue | Mitigation |
|:------|:-----------|
| Label noise | Curate and relabel low-quality samples |
| Overfitting | Increase data diversity, simplify targets |
| Drift after deployment | Continuous eval and retraining cadence |

## Summary

You now have the fine-tuning workflow from dataset prep to job monitoring.

Next: [Chapter 7: Advanced Patterns](07-advanced-patterns.md)
