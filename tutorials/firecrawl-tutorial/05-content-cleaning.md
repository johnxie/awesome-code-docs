---
layout: default
title: "Chapter 5: Content Cleaning & Processing"
parent: "Firecrawl Tutorial"
nav_order: 5
---

# Chapter 5: Content Cleaning & Processing

Transform scraped pages into clean, structured, LLM-ready text.

## Objectives
- Remove boilerplate and navigation
- Normalize text and links
- Deduplicate and score content quality
- Extract media and metadata safely

## Cleaning Pipeline (Python)
```python
from firecrawl import Firecrawl
from firecrawl.cleaning import clean_html

client = Firecrawl(api_key="YOUR_KEY")
raw = client.scrape("https://example.com", output="html")

clean = clean_html(
    raw["content"],
    remove_selectors=["nav", "footer", "script", "style"],
    resolve_links=True,
)
print(clean[:400])
```

## Deduplication by Hash
```python
import hashlib

def dedupe_paragraphs(paragraphs):
    seen = set()
    unique = []
    for p in paragraphs:
        h = hashlib.sha1(p.strip().encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(p)
    return unique
```

## Quality Scoring Ideas
- Length thresholds (e.g., >200 chars)
- Heading density vs. body ratio
- Language detection confidence
- Link-to-text ratio to catch nav-heavy sections

## Media Handling
- Download only whitelisted MIME types
- Store alt text for images; avoid hotlinking when disallowed
- Normalize relative URLs to absolute

## Troubleshooting
- Still seeing nav/ads: add site-specific selectors; strip iframes
- Garbled text: enforce UTF-8 decode; drop control characters
- Broken links: resolve relative paths; validate HTTP 200

## Performance Notes
- Stream-clean large documents instead of loading all into memory
- Cache cleaned Markdown for embedding to avoid rework

## Security Notes
- Sanitize HTML; drop scripts/iframes
- Respect copyright; store minimal necessary content

## Next Steps
Chapter 6 integrates cleaned content into RAG pipelines with embeddings and vector stores.
