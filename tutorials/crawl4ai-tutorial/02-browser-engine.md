---
layout: default
title: "Chapter 2: Browser Engine & Crawling"
parent: "Crawl4AI Tutorial"
nav_order: 2
---

# Chapter 2: Browser Engine & Crawling

Crawl4AI runs a real Chromium browser via Playwright to render pages exactly as a user would see them. This chapter covers how to configure the browser, execute JavaScript, handle authentication, manage cookies, and interact with dynamic page elements.

## Architecture: How the Browser Engine Works

```mermaid
flowchart TD
    A[AsyncWebCrawler] --> B[BrowserConfig]
    B --> C[Playwright Launcher]
    C --> D[Chromium Browser Process]
    D --> E[Browser Context<br/>cookies, storage, proxy]
    E --> F[Page / Tab]
    F --> G[Navigate to URL]
    G --> H[Wait Strategy]
    H --> I[JS Execution]
    I --> J[Content Ready]
    J --> K[Extraction Pipeline]

    classDef config fill:#fff3e0,stroke:#e65100
    classDef browser fill:#e1f5fe,stroke:#01579b
    classDef page fill:#f3e5f5,stroke:#4a148c

    class A,B config
    class C,D,E browser
    class F,G,H,I,J,K page
```

## Browser Configuration

Use `BrowserConfig` to control how the browser launches:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig

browser_config = BrowserConfig(
    headless=True,             # False to see the browser (debugging)
    browser_type="chromium",   # "chromium", "firefox", or "webkit"
    viewport_width=1280,
    viewport_height=720,
    verbose=True,
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(url="https://example.com")
```

### Key BrowserConfig Options

| Parameter | Default | Description |
|---|---|---|
| `headless` | `True` | Run without visible window |
| `browser_type` | `"chromium"` | Browser engine to use |
| `viewport_width` | `1080` | Page width in pixels |
| `viewport_height` | `600` | Page height in pixels |
| `user_agent` | Auto | Custom User-Agent string |
| `proxy` | `None` | Proxy server URL |
| `ignore_https_errors` | `True` | Skip SSL certificate errors |
| `java_script_enabled` | `True` | Enable/disable JS execution |
| `text_mode` | `False` | Disable images for faster crawling |

## Running JavaScript on Pages

Many pages require interaction before content is visible. Use the `js_code` parameter to execute JavaScript after the page loads:

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

config = CrawlerRunConfig(
    js_code="""
    // Click a "Load More" button
    const btn = document.querySelector('button.load-more');
    if (btn) btn.click();
    """,
    wait_for="css:.loaded-content",  # wait for result to appear
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com/articles", config=config)
    print(result.markdown[:500])
```

### Executing Multiple JS Steps

For multi-step interactions, pass a list of JavaScript snippets:

```python
config = CrawlerRunConfig(
    js_code=[
        # Step 1: Close cookie banner
        "document.querySelector('.cookie-accept')?.click();",
        # Step 2: Scroll to bottom to trigger lazy loading
        "window.scrollTo(0, document.body.scrollHeight);",
        # Step 3: Wait a moment then click "Show All"
        "await new Promise(r => setTimeout(r, 1000)); "
        "document.querySelector('#show-all')?.click();",
    ],
    wait_for="css:#all-content-loaded",
)
```

## Wait Strategies

Crawl4AI needs to know when a page is "ready." The `wait_for` parameter controls this:

```python
# Wait for a CSS selector to appear
config = CrawlerRunConfig(wait_for="css:#main-content")

# Wait for JavaScript condition to be true
config = CrawlerRunConfig(wait_for="js:() => document.querySelectorAll('.item').length > 10")

# Just wait for network idle (default behavior)
config = CrawlerRunConfig(page_timeout=60000)
```

```mermaid
flowchart LR
    A[Page Load] --> B{Wait Strategy}
    B -->|css:selector| C[Poll for element]
    B -->|js:condition| D[Poll JS expression]
    B -->|default| E[Network idle]
    C --> F[Content Ready]
    D --> F
    E --> F

    classDef decision fill:#fff3e0,stroke:#e65100
    class B decision
```

## Handling Authentication

### Basic HTTP Auth

```python
browser_config = BrowserConfig(
    headers={
        "Authorization": "Basic dXNlcjpwYXNz"  # base64 user:pass
    }
)
```

### Cookie-Based Auth

If a site requires login, inject cookies directly:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig

browser_config = BrowserConfig(
    cookies=[
        {
            "name": "session_id",
            "value": "abc123xyz",
            "domain": ".example.com",
            "path": "/",
        }
    ]
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(url="https://example.com/dashboard")
```

### Login via JavaScript

For sites that need form-based login, use JS execution:

```python
config = CrawlerRunConfig(
    js_code="""
    document.querySelector('#username').value = 'myuser';
    document.querySelector('#password').value = 'mypass';
    document.querySelector('#login-form').submit();
    """,
    wait_for="css:.dashboard-content",
    page_timeout=30000,
)

async with AsyncWebCrawler() as crawler:
    # First crawl: perform login
    login_result = await crawler.arun(
        url="https://example.com/login",
        config=config,
    )
    # Second crawl: session cookies are preserved in the same context
    result = await crawler.arun(url="https://example.com/dashboard")
```

## Using Proxies

Route traffic through a proxy for geo-targeting or IP rotation:

```python
browser_config = BrowserConfig(
    proxy="http://user:pass@proxy.example.com:8080"
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(url="https://example.com")
    print(f"Crawled from proxy, status: {result.status_code}")
```

## Custom Headers and User Agents

```python
browser_config = BrowserConfig(
    headers={
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
    },
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/120.0.0.0 Safari/537.36",
)
```

## Screenshot and PDF Capture

Crawl4AI can take screenshots or generate PDFs alongside content extraction:

```python
config = CrawlerRunConfig(
    screenshot=True,      # capture a PNG screenshot
    pdf=True,             # generate a PDF of the page
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com", config=config)

    # Screenshot is base64-encoded
    if result.screenshot:
        import base64
        with open("page.png", "wb") as f:
            f.write(base64.b64decode(result.screenshot))

    # PDF is also base64-encoded
    if result.pdf:
        import base64
        with open("page.pdf", "wb") as f:
            f.write(base64.b64decode(result.pdf))
```

## Text Mode: Fast Crawling Without Images

When you only need text content, enable text mode to skip image loading:

```python
browser_config = BrowserConfig(
    text_mode=True,   # disables image loading
    headless=True,
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(url="https://example.com")
    # Faster crawl, same markdown quality
```

## Handling Infinite Scroll Pages

Some pages load content as you scroll. Combine JS execution with wait strategies:

```python
config = CrawlerRunConfig(
    js_code="""
    async function scrollToBottom() {
        let prev = 0;
        while (document.body.scrollHeight > prev) {
            prev = document.body.scrollHeight;
            window.scrollTo(0, document.body.scrollHeight);
            await new Promise(r => setTimeout(r, 2000));
        }
    }
    await scrollToBottom();
    """,
    page_timeout=120000,  # allow up to 2 minutes
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com/infinite-feed",
        config=config,
    )
    print(f"Extracted {len(result.markdown)} chars of content")
```

## Summary

The browser engine is the foundation of Crawl4AI. You now know how to:

- Configure browser launch options (headless, viewport, user agent)
- Execute JavaScript for page interaction and dynamic content
- Use wait strategies to ensure content is fully loaded
- Handle authentication via cookies, headers, or form login
- Route traffic through proxies
- Capture screenshots and PDFs
- Optimize speed with text mode

**Next up:** [Chapter 3: Content Extraction](03-content-extraction.md) — learn how to precisely target the content you want using CSS selectors, XPath, cosine similarity, and custom strategies.

---

[Previous: Chapter 1: Getting Started](01-getting-started.md) | [Back to Tutorial Home](README.md) | [Next: Chapter 3: Content Extraction](03-content-extraction.md)
