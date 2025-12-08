---
layout: default
title: "Chapter 5: Knowledge Bases"
parent: "Quivr Tutorial"
nav_order: 5
---

# Chapter 5: Knowledge Bases

Organize documents into collections with metadata and access control.

## Objectives
- Create knowledge bases per project/team
- Tag documents with metadata (source, owner, permissions)
- Support multi-tenant separation

## Example Structure
- KB: `engineering-handbook`
  - Tags: `owner=eng`, `visibility=internal`
  - Docs: onboarding, architecture, runbooks

## Metadata Filters
```python
res = collection.query(
    query_embeddings=q_emb,
    n_results=5,
    where={"owner": "eng", "visibility": "internal"}
)
```

## Access Control
- Keep private KBs separate; use tenant-specific collections
- Enforce auth before query

## Troubleshooting
- Cross-tenant leakage: verify collection/where filters
- Stale docs: add `updated_at` and re-embed when changed

## Next Steps
Chapter 6 covers integration APIs for apps and services.
