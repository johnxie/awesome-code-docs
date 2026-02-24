---
layout: default
title: "Chapter 5: Web Research and Browser Integration"
nav_order: 5
parent: Devika Tutorial
---

# Chapter 5: Web Research and Browser Integration

Welcome to **Chapter 5: Web Research and Browser Integration**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter covers how Devika's researcher agent uses Playwright to autonomously browse the web, extract relevant content, and store it in Qdrant for use by the coder agent.

## Learning Goals

- understand how the researcher agent generates and executes Playwright-driven web searches
- configure Playwright browser options for headless operation and rate-limiting compliance
- trace the research artifact lifecycle from web fetch to Qdrant storage to coder retrieval
- identify failure modes in browser automation and apply targeted countermeasures

## Fast Start Checklist

1. verify Playwright Chromium is installed and the researcher agent can launch a browser
2. submit a task with a clear technology context and observe the researcher's search queries in logs
3. inspect the Qdrant collection to confirm research artifacts are stored with correct metadata
4. verify the coder agent retrieves relevant chunks in subsequent steps

## Source References

- [Devika Researcher Agent Source](https://github.com/stitionai/devika/tree/main/src/agents/researcher)
- [Devika Browser Agent Source](https://github.com/stitionai/devika/tree/main/src/browser)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Playwright Python Documentation](https://playwright.dev/python/)

## Summary

You now understand how Devika's browser automation layer fetches, extracts, and stores web research that enriches code generation with up-to-date documentation and examples.

Next: [Chapter 6: Project Management and Workspaces](06-project-management-and-workspaces.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 5: Web Research and Browser Integration**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. The researcher agent receives a step description and generates one or more search query strings using the LLM; queries are optimized for technical documentation and code examples.
2. The browser module launches a Playwright Chromium instance in headless mode and navigates to a search engine (default: Bing) to retrieve a results page.
3. For each result URL, Playwright navigates to the page and extracts the visible text content using a content-stripping function that removes navigation, ads, and boilerplate.
4. Extracted text is chunked into segments of approximately 500-1000 tokens each and sent to an embedding model (configured in config.toml) to produce vector representations.
5. Embeddings are upserted into Qdrant under a collection keyed to the project and task; each chunk is stored with metadata including the source URL, step number, and task ID.
6. When the coder agent runs for a given step, it queries Qdrant with the step description as the query vector and retrieves the top-k most similar chunks.
7. Retrieved chunks are injected into the coder prompt in a structured "Research Context" block; the coder is instructed to prefer research-provided APIs and patterns.
8. The browser session is closed after each research invocation to prevent resource leaks; Playwright is re-launched per research step rather than maintained as a persistent session.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Browser mode | headless Chromium | headful Chromium for debugging research steps | invisibility vs observability |
| Search engine | default Bing search | custom search API (SerpAPI, Brave Search) | zero config vs rate limit control |
| Pages per query | single result page | crawl top 3-5 results per query | speed vs research breadth |
| Chunk size | default 500-token chunks | smaller 200-token chunks for precision | retrieval recall vs precision |
| Research scope | open internet | whitelist of trusted documentation sites only | breadth vs security |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Playwright browser fails to launch | `BrowserType.launch` error on research step | missing Chromium binary or sandbox restriction | run `playwright install chromium` and check sandbox flags for Docker environments |
| Search engine blocks automated requests | empty results or captcha page | search engine detects bot-like request patterns | add request delay, rotate user-agent, or use a search API key |
| Web page content extraction returns empty | empty research context in coder prompt | site uses heavy JavaScript rendering that Playwright can't extract | add `page.wait_for_load_state('networkidle')` before content extraction |
| Qdrant upsert fails silently | coder receives empty research chunks | Qdrant collection write error not propagated | add explicit error handling on Qdrant upsert and log chunk count per step |
| Research content is irrelevant | coder generates code for wrong API | search query too generic; retrieves unrelated documentation | improve query generation prompt to include library version and specific API names |
| Memory leak from unclosed browsers | process memory grows over multiple tasks | Playwright context not closed after research step | explicitly call `browser.close()` and `playwright.stop()` in a finally block |

### Implementation Runbook

1. Verify Playwright is installed: run `playwright install chromium` in the active virtualenv.
2. Submit a task that requires looking up a library API and observe the researcher's generated search queries in backend logs.
3. Inspect the Qdrant collection via the Qdrant web UI at `http://localhost:6333/dashboard` to confirm chunks are stored with correct metadata.
4. Add a debug log line in the coder agent that prints the number of Qdrant chunks retrieved for each step.
5. For Docker deployments, add `--no-sandbox` and `--disable-setuid-sandbox` Playwright launch arguments to handle Linux container restrictions.
6. Configure a search API (e.g., Bing Search API or SerpAPI) in config.toml to replace raw browser-based search for more reliable query handling.
7. Tune the `top_k` retrieval parameter in config.toml to balance research context richness against coder prompt size.
8. Add a URL allowlist configuration to restrict researcher browsing to documentation sites like `docs.python.org`, `developer.mozilla.org`, and package-specific docs.
9. Monitor Qdrant collection size over time and implement a TTL-based cleanup policy to prevent unbounded storage growth.

### Quality Gate Checklist

- [ ] Playwright Chromium is installed and launches without errors in headless mode
- [ ] researcher generates specific, targeted search queries rather than generic keyword searches
- [ ] Qdrant chunk count per step is logged and non-zero for all steps with `search_query` fields
- [ ] content extraction handles JavaScript-heavy sites by waiting for network idle state
- [ ] browser sessions are explicitly closed after each research step to prevent memory leaks
- [ ] coder agent logs confirm research context is retrieved and injected for research-enabled steps
- [ ] Qdrant storage is bounded by task/session TTL to prevent unbounded growth
- [ ] research scope is limited to trusted domains in production deployments

### Source Alignment

- [Devika Researcher Agent Source](https://github.com/stitionai/devika/tree/main/src/agents/researcher)
- [Devika Browser Module Source](https://github.com/stitionai/devika/tree/main/src/browser)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Playwright Python Docs](https://playwright.dev/python/)
- [Qdrant Python Client Docs](https://python-client.qdrant.tech/)

### Cross-Tutorial Connection Map

- [Playwright MCP Tutorial](../playwright-mcp-tutorial/) — deep dive on Playwright automation patterns directly applicable to Devika's browser module
- [Browser Use Tutorial](../browser-use-tutorial/) — alternative browser automation agent for comparison with Devika's approach
- [Firecrawl Tutorial](../firecrawl-tutorial/) — managed web crawling service that can replace Devika's direct Playwright scraping
- [Chroma Tutorial](../chroma-tutorial/) — alternative vector store for understanding Qdrant's role in the research pipeline
- [LanceDB Tutorial](../lancedb-tutorial/) — embedded vector database as an alternative to Qdrant for simpler deployments

### Advanced Practice Exercises

1. Replace Devika's built-in search engine scraping with a call to the Brave Search API and measure query result quality improvement.
2. Add a domain allowlist filter to the browser module that restricts research to official documentation sites for a given language ecosystem.
3. Implement a content quality filter that scores extracted chunks by relevance before upserting into Qdrant, discarding low-relevance content.
4. Run Devika's researcher agent in headed mode (non-headless) and screen-record a full research session to observe browsing behavior.
5. Build a Qdrant TTL cleanup job that purges research chunks older than 24 hours to keep the vector store bounded in size.

### Review Questions

1. How does the researcher agent decide what search queries to generate for a given plan step?
2. What Playwright event or state should be awaited before extracting content from a JavaScript-heavy page?
3. How are research chunks stored in Qdrant and what metadata fields enable per-task and per-step filtering?
4. What Playwright launch argument is required to run Chromium inside a Linux Docker container?
5. How does the coder agent retrieve the research chunks that are most relevant to its current step?

### Scenario Playbook 1: Playwright Fails in Docker Container

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: research steps fail with "No usable sandbox" error when Devika is deployed in Docker
- initial hypothesis: Chromium's sandbox mode requires kernel capabilities not available in the container
- immediate action: add `--no-sandbox` and `--disable-setuid-sandbox` to the Playwright launch args in the browser module
- engineering control: document the required Docker run flags (`--cap-add SYS_ADMIN`) or use the `--no-sandbox` approach in the Playwright config
- verification target: researcher agent completes a web fetch without sandbox errors in the Docker environment
- rollback trigger: running without sandbox in a multi-tenant environment creates security exposure; switch to isolated containers per task
- communication step: update Docker deployment docs with the sandbox configuration requirement
- learning capture: add a Docker-specific Playwright configuration preset to the config.toml example

### Scenario Playbook 2: Search Engine Returns Captcha Page

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: researcher agent returns empty research context; browser log shows captcha HTML in the response
- initial hypothesis: Bing or Google detects automated browsing and serves a bot verification page
- immediate action: configure a search API key (Bing Search API or SerpAPI) in config.toml to replace direct browser-based search
- engineering control: add a content validation check that detects captcha patterns in extracted text and raises an alert
- verification target: researcher completes 10 consecutive search queries via API without triggering bot detection
- rollback trigger: search API quota is insufficient for task volume; implement request queuing with rate limiting
- communication step: document the search API configuration option in the README and explain why it is recommended for production
- learning capture: add search API as the recommended configuration in the Docker Compose example

### Scenario Playbook 3: Qdrant Stores Empty Chunks

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: coder receives empty research context even though researcher agent ran without errors
- initial hypothesis: the web page content extraction returned empty string due to JavaScript-rendered content
- immediate action: add `page.wait_for_load_state('networkidle')` before content extraction in the browser module
- engineering control: add minimum content length validation: if extracted text is under 100 characters, retry with a different result URL
- verification target: Qdrant collection shows non-zero chunk count after each researcher invocation in logs
- rollback trigger: `networkidle` wait causes Playwright to hang on pages that never reach idle state; add a timeout
- communication step: document the JavaScript rendering issue and the `networkidle` solution in the browser module README
- learning capture: add a content extraction test with a known JavaScript-heavy documentation site

### Scenario Playbook 4: Research Content Pollutes Coder Context With Irrelevant Chunks

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: coder generates code using a completely wrong API because retrieved chunks were from unrelated documentation
- initial hypothesis: search queries are too generic and Qdrant's semantic similarity returns tangentially related content
- immediate action: inspect the search queries in logs and add more specific terms: library name, version, and exact API being used
- engineering control: add a minimum relevance score threshold to the Qdrant retrieval call to filter out low-similarity chunks
- verification target: coder context only contains chunks with similarity score above 0.75 for representative tasks
- rollback trigger: strict score threshold causes empty context on niche topics where all documentation has lower similarity
- communication step: document the relevance threshold tuning parameter in the configuration guide
- learning capture: build an offline evaluation dataset of task-research pairs to measure retrieval precision over time

### Scenario Playbook 5: Qdrant Storage Grows Unbounded

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: Qdrant disk usage grows continuously as teams run many tasks over days and weeks
- initial hypothesis: research chunks are never deleted after task completion
- immediate action: implement a post-task cleanup job that deletes Qdrant chunks tagged with completed task IDs
- engineering control: add a TTL metadata field to each chunk at upsert time and schedule a nightly cleanup job that deletes expired chunks
- verification target: Qdrant collection size is bounded and does not grow unboundedly over a week of normal team usage
- rollback trigger: aggressive cleanup deletes chunks that are still needed for in-progress tasks
- communication step: document the storage cleanup policy and the TTL configuration parameter
- learning capture: add Qdrant collection size as a monitored metric with an alert threshold in the observability dashboard

### What Problem Does This Solve?

Devika's browser research integration solves the knowledge cutoff and documentation freshness problem in LLM-based code generation. A model trained months or years ago has no knowledge of newly released library versions, breaking API changes, or new framework patterns. By autonomously researching the web before generating code, Devika produces code that uses current APIs and is aligned with the latest documentation, dramatically reducing the incidence of deprecated API usage that plagues static LLM code generation.

### How it Works Under the Hood

1. The researcher agent generates search query strings from the plan step description using an LLM prompt that emphasizes specificity.
2. The browser module launches a headless Playwright Chromium instance and navigates to the configured search engine.
3. Result URLs are extracted from the search results page; Playwright navigates to each URL and waits for network idle state.
4. Page text content is extracted using a custom extractor that removes navigation, headers, footers, and script tags.
5. Text is chunked and sent to the configured embedding model; resulting vectors are upserted into Qdrant with step and task metadata.
6. The coder agent queries Qdrant using the step description as the query text and retrieves the top-k chunks above a relevance threshold.

### Source Walkthrough

- [Devika Researcher Agent](https://github.com/stitionai/devika/tree/main/src/agents/researcher) — Why it matters: the query generation and Qdrant storage logic for the research pipeline.
- [Devika Browser Module](https://github.com/stitionai/devika/tree/main/src/browser) — Why it matters: the Playwright automation code for web navigation and content extraction.
- [Playwright Python Installation](https://playwright.dev/python/docs/intro) — Why it matters: official Playwright setup guide for installing browsers and understanding launch options.
- [Qdrant Python Client](https://python-client.qdrant.tech/) — Why it matters: the client library Devika uses for vector upsert and similarity search operations.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Task Planning and Code Generation](04-task-planning-and-code-generation.md)
- [Next Chapter: Chapter 6: Project Management and Workspaces](06-project-management-and-workspaces.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
