---
layout: default
title: "Chapter 4: JavaScript & Dynamic Content"
parent: "Firecrawl Tutorial"
nav_order: 4
---

# Chapter 4: JavaScript & Dynamic Content

Handle SPAs, infinite scroll, and Ajax-loaded data with Firecrawl’s rendering capabilities.

## Objectives
- Enable JavaScript rendering for SPAs
- Wait for network idle or selectors to appear
- Handle infinite scroll and pagination
- Extract Ajax-loaded content

## Rendering a SPA (Python)
```python
from firecrawl import Firecrawl

client = Firecrawl(api_key="YOUR_KEY")

result = client.scrape(
    "https://example-spa.com",
    output="markdown",
    render={"wait_for": "#app", "timeout_ms": 15000},
)
print(result["content"][:400])
```

## Waiting for Dynamic Selectors (Node.js)
```javascript
import { FirecrawlClient } from "firecrawl";

const client = new FirecrawlClient({ apiKey: process.env.FIRECRAWL_API_KEY });

const res = await client.scrape("https://example-spa.com/dashboard", {
  output: "json",
  render: {
    wait_for: ".card",
    wait_until: "networkidle",
    timeout_ms: 20000,
  },
});
console.log(res.content.slice(0, 300));
```

## Infinite Scroll Strategy
- Scroll in increments and wait for new content
- Stop after N pages or when no new items appear
- Debounce scroll events to reduce load

## Ajax-Fetched Data
- Inspect network calls; target JSON endpoints directly when possible
- If HTML only, render and parse after `wait_for` selector appears

## Troubleshooting
- Blank pages: increase `timeout_ms`; confirm selectors
- Partial content: add more scroll steps; reduce throttle
- Rate limits: slow down scrolling and batch requests

## Performance Notes
- Prefer targeting JSON APIs over full-page rendering
- Reuse sessions/cookies if allowed to avoid repeated auth
- Cap concurrent rendered scrapes (e.g., 2–3) to control resource usage

## Security Notes
- Do not scrape authenticated areas without permission
- Obey robots.txt and terms of service
- Avoid leaking session cookies in logs

## Next Steps
Move to Chapter 5 to clean and normalize extracted content for LLM-ready pipelines.
