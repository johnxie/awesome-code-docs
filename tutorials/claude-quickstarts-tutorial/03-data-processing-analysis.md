---
layout: default
title: "Chapter 3: Data Processing and Analysis"
nav_order: 3
parent: Claude Quickstarts Tutorial
---

# Chapter 3: Data Processing and Analysis

Data quickstarts focus on turning raw data into trustworthy, structured insight.

## Typical Workflow

- ingest CSV/JSON or API output
- validate and profile data quality
- ask Claude for explanations and summaries
- return machine-readable structured output

## Structured Output Pattern

```json
{
  "summary": "Revenue grew 12% QoQ",
  "risks": ["higher churn in SMB"],
  "recommendations": ["run retention campaign"]
}
```

## Best Practices

- Keep schema strict for downstream systems.
- Include data-quality checks before inference.
- Separate analysis prompts from presentation prompts.

## Summary

You can now build reproducible Claude-driven analytics pipelines.

Next: [Chapter 4: Browser and Computer Use](04-browser-computer-use.md)
