---
layout: default
title: "Chapter 2: Document Processing"
parent: "Quivr Tutorial"
nav_order: 2
---

# Chapter 2: Document Processing

Extract text from PDFs and other formats, normalize, and prepare for embeddings.

## Objectives
- Extract text from PDF/HTML/Text
- Clean and normalize content
- Split into chunks for embeddings

## Ingestion Pipeline (Python)
```python
from quivr.ingest import Ingestor

files = ["docs/report.pdf", "docs/notes.txt"]
text = Ingestor().load(files)
print(text[:500])
```

## Cleaning Tips
- Remove boilerplate (nav, footer) for HTML
- Normalize whitespace and unicode
- Keep headings for structure

## Chunking
```python
from quivr.chunk import chunk_text

chunks = chunk_text(text, chunk_size=800, overlap=120)
print(len(chunks), "chunks")
```

## Troubleshooting
- Garbled text: ensure OCR for scanned PDFs
- Empty chunks: adjust min length; filter non-text pages

## Next Steps
Move to Chapter 3 to embed and store vectors.
