---
layout: default
title: "Chapter 7: Customization"
parent: "Quivr Tutorial"
nav_order: 7
---

# Chapter 7: Customization

Extend Quivr with custom pipelines, rerankers, and UI tweaks.

## Objectives
- Add custom preprocessing/cleaning steps
- Plug in custom rerankers
- Customize UI for chat/search

## Custom Preprocessing
```python
def strip_tables(text):
    # demo cleaner
    return "\n".join([line for line in text.splitlines() if "|" not in line])

cleaned = strip_tables(raw_text)
```

## Custom Reranker
```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

scores = reranker.predict([(query, doc) for doc in context])
# reorder context by scores
```

## UI Tweaks
- Add source badges and confidence scores
- Provide feedback buttons to improve reranker

## Troubleshooting
- Reranker slow: batch inputs; use smaller model
- UI latency: stream tokens; prefetch context

## Next Steps
Finalize with Chapter 8 on production deployment.
