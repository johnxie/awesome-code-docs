---
layout: default
title: "Langfuse Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Langfuse Tutorial
---

# Chapter 1: Getting Started with Langfuse

> Install Langfuse, connect your first app, and capture the first trace.

## Overview

Langfuse gives you tracing and analytics for LLM apps. In this chapter you will:

- Create a Langfuse project (Cloud or self-host).
- Install the SDK.
- Send your first trace with minimal code.

## Prerequisites

- Python 3.9+ (examples use Python; JS/TS also supported).
- Provider key (OpenAI/Anthropic/etc.) for your app.
- Langfuse API key & public key (from Cloud or self-hosted UI).

## Option A: Langfuse Cloud (fastest)

1. Sign up at <https://cloud.langfuse.com>.
2. Create a project and copy the **Public Key** and **Secret Key**.
3. Note your base URL (e.g., `https://cloud.langfuse.com`).

## Option B: Self-Host with Docker Compose

```yaml
# docker-compose.yml (minimal)
version: "3.9"
services:
  langfuse:
    image: ghcr.io/langfuse/langfuse:latest
    environment:
      - DATABASE_URL=postgresql://langfuse:langfuse@db:5432/langfuse
      - NEXTAUTH_SECRET=change-me
      - SALT=change-me
    ports:
      - "3000:3000"
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=langfuse
      - POSTGRES_USER=langfuse
      - POSTGRES_PASSWORD=langfuse
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata: {}
```

Run: `docker compose up -d`, then open `http://localhost:3000` to create your admin user and API keys.

## Install the SDK

```bash
pip install langfuse
# or
npm install langfuse
```

## Your First Trace (Python)

```python
# app.py
from langfuse import Langfuse
from openai import OpenAI

client = OpenAI()
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com",  # or http://localhost:3000 if self-hosted
)

trace = langfuse.trace(name="hello-world")
span = trace.span(name="llm-call", input="Say hi to Langfuse")

resp = client.responses.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Introduce Langfuse in one sentence"}],
)

span.end(output=resp.choices[0].message.content)
trace.end()

langfuse.flush()  # send events
```

Open the Langfuse UI and confirm the trace appears under your project.

## Troubleshooting

- **401 Unauthorized**: Verify keys and host URL; Cloud vs self-host mismatch is common.
- **No traces visible**: Ensure `langfuse.flush()` is called, or enable `LANGFUSE_DEBUG=1` to see logs.
- **CORS errors (JS)**: Use server-side tracing; avoid exposing secret keys to the browser.

Next: instrument traces properly with spans, events, and metadata. 
