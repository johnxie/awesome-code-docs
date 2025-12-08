---
layout: default
title: "Chapter 2: Basic Web Scraping"
parent: "Firecrawl Tutorial"
nav_order: 2
---

# Chapter 2: Basic Web Scraping

Learn how to run your first Firecrawl scrapes, handle batches, and return clean structured output.

## Objectives
- Run single-page and multi-page scrapes
- Choose output formats (JSON, Markdown, HTML)
- Implement basic error handling and retries
- Respect rate limits while batching requests

## Prerequisites
- Completed Chapter 1 setup
- Python 3.8+ or Node.js 16+
- Firecrawl API key or local configuration

## Single Page Scrape (Python)
```python
import asyncio
from firecrawl import Firecrawl

client = Firecrawl(api_key="YOUR_KEY")

async def scrape_url(url: str):
    result = await client.scrape(url, output="json")
    print(result["content"][:500])

asyncio.run(scrape_url("https://example.com"))
```

## Batch Scrape (Node.js)
```javascript
import { FirecrawlClient } from "firecrawl";

const client = new FirecrawlClient({ apiKey: process.env.FIRECRAWL_API_KEY });

async function batchScrape(urls) {
  const results = [];
  for (const url of urls) {
    const res = await client.scrape(url, { output: "markdown" });
    results.push({ url, content: res.content });
  }
  return results;
}

batchScrape([
  "https://example.com",
  "https://news.ycombinator.com",
]).then(console.log).catch(console.error);
```

## Retry and Backoff (Python)
```python
import asyncio
import random
from firecrawl import Firecrawl

client = Firecrawl(api_key="YOUR_KEY")

async def scrape_with_retry(url, retries=3):
    delay = 1
    for attempt in range(1, retries + 1):
        try:
            return await client.scrape(url, output="json")
        except Exception as exc:
            if attempt == retries:
                raise
            await asyncio.sleep(delay)
            delay *= 2 + random.random()

asyncio.run(scrape_with_retry("https://example.com"))
```

## Rate Limiting Basics
- Prefer small batches (≤10 concurrent requests)
- Add jittered backoff between batches
- Cache results to avoid duplicate scrapes

## Output Formats
- `json`: structured content for downstream processing
- `markdown`: human-readable with headers preserved
- `html`: raw HTML when you need full fidelity

## Troubleshooting
- 403/429 errors: reduce concurrency, add backoff, rotate IP if available
- Empty content: ensure JavaScript rendering is enabled in later chapters; check robots.txt
- Slow responses: lower batch size; verify network egress limits

## Performance Notes
- Parallelize with bounded semaphores (asyncio) or worker pools
- Deduplicate URLs before scraping
- Compress outputs when storing large batches

## Security Notes
- Respect site terms and robots.txt
- Avoid scraping authenticated pages without explicit permission
- Do not store secrets in code; use environment variables

## Next Steps
Continue to Chapter 3 to build structured extraction rules and schema-driven outputs.
