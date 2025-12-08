---
layout: default
title: "Chapter 3: Advanced Data Extraction"
parent: "Firecrawl Tutorial"
nav_order: 3
---

# Chapter 3: Advanced Data Extraction

Design schema-driven extraction pipelines that return clean structured data with metadata.

## Objectives
- Define extraction schemas and reusable rules
- Handle multiple content types (articles, docs, product pages)
- Validate and clean extracted data
- Enrich outputs with metadata

## Schema-First Extraction (Python)
```python
from firecrawl import Firecrawl

client = Firecrawl(api_key="YOUR_KEY")

ARTICLE_SCHEMA = {
    "title": "string",
    "author": "string",
    "published": "date",
    "summary": "string",
    "body": "markdown",
}

result = client.extract(
    "https://example.com/blog/ai-news",
    schema=ARTICLE_SCHEMA,
    output="json",
)
print(result)
```

## Custom Rules (Node.js)
```javascript
import { FirecrawlClient } from "firecrawl";

const client = new FirecrawlClient({ apiKey: process.env.FIRECRAWL_API_KEY });

const rules = {
  title: "h1",
  summary: "meta[name=description]@content",
  paragraphs: "article p",
};

const res = await client.extract("https://example.com/post", { rules, output: "json" });
console.log(res);
```

## Cleaning Pipeline
- Strip navigation, ads, footers
- Normalize whitespace and encoding
- Remove duplicate paragraphs
- Convert relative links to absolute
- Preserve headings for semantic structure

## Metadata Enrichment
- Add `source_url`, `fetched_at`, `language`
- Detect primary author and publication date
- Optional sentiment or topic classification downstream

## Validation Checklist
- Ensure required fields are present
- Enforce type constraints (date, number, string)
- Reject empty bodies or very short articles

## Troubleshooting
- Missing fields: adjust selectors; inspect DOM with a headless browser
- Wrong language/encoding: force UTF-8 decoding; drop invalid bytes
- Repeated content: deduplicate paragraphs by hash or similarity

## Performance Notes
- Cache CSS selector rules for reuse
- Batch similar page types together for efficiency
- Store cleaned Markdown for downstream embeddings

## Security Notes
- Avoid executing untrusted scripts; rely on sanitized HTML
- Log and redact PII when scraping user-generated content

## Next Steps
Proceed to Chapter 4 to handle JavaScript-heavy and dynamic sites reliably.
