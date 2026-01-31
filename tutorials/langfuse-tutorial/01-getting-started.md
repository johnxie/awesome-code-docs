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

Langfuse gives you tracing and analytics for LLM apps. Think of it as the observability layer that sits between your application code and the insights you need to ship reliable AI features. In this chapter you will:

- Understand how Langfuse fits into your stack.
- Create a Langfuse project (Cloud or self-host).
- Install the SDK in Python **and** TypeScript/JavaScript.
- Send your first trace with minimal code.
- Navigate the Langfuse UI with confidence.

## How Langfuse Works

Before writing any code, it helps to see the big picture. Langfuse has four main layers:

```mermaid
graph LR
    A[Your App + SDK] -->|HTTPS / Batch| B[Langfuse API]
    B --> C[PostgreSQL Database]
    C --> D[Langfuse Web UI]
    D -->|Dashboards & Traces| E[You / Your Team]

    style A fill:#e0f2fe,stroke:#0284c7
    style B fill:#fef3c7,stroke:#d97706
    style C fill:#f3e8ff,stroke:#9333ea
    style D fill:#dcfce7,stroke:#16a34a
    style E fill:#fce7f3,stroke:#db2777
```

1. **SDK** -- lightweight client in your application that batches events and sends them asynchronously.
2. **API** -- ingestion endpoint that validates, enriches, and writes events.
3. **Database** -- PostgreSQL stores traces, spans, scores, prompts, and project metadata.
4. **Web UI** -- Next.js dashboard where you browse traces, manage prompts, view analytics, and configure evaluations.

Because the SDK sends data asynchronously, your application's latency is virtually unaffected.

## Prerequisites

- **Python 3.9+** or **Node.js 18+** (examples cover both).
- A provider API key (OpenAI, Anthropic, etc.) for the LLM your app calls.
- Langfuse API keys -- a **Public Key** and a **Secret Key** -- obtained from the Cloud dashboard or your self-hosted instance.

## Option A: Langfuse Cloud (Fastest Start)

The managed cloud service is the quickest way to get going:

1. Sign up at <https://cloud.langfuse.com>.
2. Create a new **Project** (e.g., "my-chatbot").
3. Open **Settings > API Keys** and copy your **Public Key** (`pk-...`) and **Secret Key** (`sk-...`).
4. Note your host URL: `https://cloud.langfuse.com`.

That is all you need. Skip ahead to *Install the SDK* below.

## Option B: Self-Host with Docker Compose

Self-hosting gives you full data control. The minimal setup requires Docker and Docker Compose.

### Minimal Docker Compose File

```yaml
# docker-compose.yml
version: "3.9"
services:
  langfuse:
    image: ghcr.io/langfuse/langfuse:latest
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://langfuse:langfuse@db:5432/langfuse
      - NEXTAUTH_SECRET=change-me-to-a-random-string
      - SALT=change-me-to-another-random-string
      - NEXTAUTH_URL=http://localhost:3000
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

Start everything:

```bash
docker compose up -d
```

Open `http://localhost:3000`, create your admin account, and generate API keys under **Settings > API Keys**.

### Full Environment Variable Reference

Below is a reference of the most important environment variables you can set on the `langfuse` container. Only `DATABASE_URL`, `NEXTAUTH_SECRET`, and `SALT` are strictly required.

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string. |
| `NEXTAUTH_SECRET` | Yes | Random string used to encrypt session tokens. Generate with `openssl rand -base64 32`. |
| `SALT` | Yes | Random string used for hashing API keys. Generate with `openssl rand -base64 32`. |
| `NEXTAUTH_URL` | Recommended | The canonical URL of your Langfuse instance (e.g., `https://langfuse.mycompany.com`). |
| `PORT` | No | Port the server listens on (default `3000`). |
| `LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES` | No | Set to `true` to opt into beta features. |
| `SMTP_CONNECTION_URL` | No | SMTP connection string for email invitations (e.g., `smtps://user:pass@smtp.example.com:465`). |
| `EMAIL_FROM_ADDRESS` | No | Sender address for emails (e.g., `langfuse@mycompany.com`). |
| `AUTH_DISABLE_SIGNUP` | No | Set to `true` to prevent new user sign-ups after initial setup. |
| `LANGFUSE_DEFAULT_PROJECT_ROLE` | No | Default role assigned to new project members (`ADMIN`, `MEMBER`, `VIEWER`). |
| `LANGFUSE_LOG_LEVEL` | No | Logging verbosity: `debug`, `info`, `warn`, `error`. |
| `LANGFUSE_S3_EVENT_UPLOAD_BUCKET` | No | S3 bucket for large event payloads (optional, for high-volume setups). |

### Production Hardening Tips

- Put Langfuse behind a reverse proxy (NGINX / Caddy) with TLS.
- Use a managed PostgreSQL instance (AWS RDS, Supabase, Neon) for durability.
- Set `AUTH_DISABLE_SIGNUP=true` after creating your team accounts.
- Store secrets (`NEXTAUTH_SECRET`, `SALT`, database password) in a vault or secrets manager rather than plain-text environment files.

## Install the SDK

### Python

```bash
pip install langfuse
```

### TypeScript / JavaScript

```bash
npm install langfuse
# or
yarn add langfuse
# or
pnpm add langfuse
```

## Environment Setup Best Practices

Rather than hard-coding keys in source files, export them as environment variables. Both SDKs will pick them up automatically.

```bash
# .env  (add to .gitignore!)
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com   # or http://localhost:3000
```

In Python, the SDK reads these automatically when you call `Langfuse()` with no arguments. In Node.js, pass them explicitly or use a library like `dotenv`:

```bash
# Node.js -- load .env at startup
node -r dotenv/config app.js
```

**Key rules to live by:**

- Never commit `.env` files to version control.
- Use separate projects (and separate keys) for development, staging, and production.
- Enable `LANGFUSE_DEBUG=true` locally to see SDK log output in your terminal.

## Your First Trace -- Python

```python
# app.py
import os
from langfuse import Langfuse
from openai import OpenAI

# SDK reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST from env
langfuse = Langfuse()
client = OpenAI()

# 1. Start a trace
trace = langfuse.trace(name="hello-world")

# 2. Create a span for the LLM call
span = trace.span(name="llm-call", input="Say hi to Langfuse")

# 3. Call your model
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Introduce Langfuse in one sentence."}],
)

# 4. Record the output
span.end(output=resp.choices[0].message.content)
trace.end()

# 5. Flush to make sure all events are sent before the process exits
langfuse.flush()

print("Trace sent! Check the Langfuse UI.")
```

Run the script:

```bash
python app.py
```

## Your First Trace -- TypeScript / JavaScript

```typescript
// app.ts
import Langfuse from "langfuse";
import OpenAI from "openai";

const langfuse = new Langfuse({
  publicKey: process.env.LANGFUSE_PUBLIC_KEY!,
  secretKey: process.env.LANGFUSE_SECRET_KEY!,
  baseUrl: process.env.LANGFUSE_HOST ?? "https://cloud.langfuse.com",
});

const openai = new OpenAI();

async function main() {
  // 1. Start a trace
  const trace = langfuse.trace({ name: "hello-world" });

  // 2. Create a span
  const span = trace.span({ name: "llm-call", input: "Say hi to Langfuse" });

  // 3. Call your model
  const resp = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "Introduce Langfuse in one sentence." }],
  });

  // 4. Record the output
  span.end({ output: resp.choices[0].message.content });
  trace.update({ output: resp.choices[0].message.content });

  // 5. Flush before exit
  await langfuse.flushAsync();

  console.log("Trace sent! Check the Langfuse UI.");
}

main();
```

Run with:

```bash
npx ts-node app.ts
# or compile and run
npx tsc && node dist/app.js
```

## Understanding the Langfuse UI

Once your first trace arrives, take a few minutes to explore the dashboard. Here are the key areas you will use throughout this tutorial series:

### Traces View

The **Traces** page is your home base. Each row represents one end-to-end request. You can click any trace to drill into its spans, see inputs and outputs, and check attached scores. Use the search bar and tag filters to narrow down results.

### Sessions View

If you set a `session_id` on your traces, Langfuse groups them into **Sessions** -- handy for multi-turn conversations or user journeys.

### Prompts Page

The **Prompts** page is where you create, version, and label prompts. We will cover this in detail in Chapter 3.

### Scores and Evaluation

The **Scores** tab gives you an overview of all numeric and categorical scores attached to traces. You can filter by score name, time range, and tags.

### Settings

Under **Settings** you manage API keys, team members, project configuration, and integrations.

### Quick Navigation Shortcuts

| Action | Where to find it |
|---|---|
| Search traces by name or tag | Traces page -- search bar at top |
| View a specific user's traces | Traces page -- filter by `user_id` |
| Compare prompt versions | Prompts page -- version history sidebar |
| Check cost and latency | Dashboard -- overview charts |
| Manage API keys | Settings > API Keys |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| **401 Unauthorized** | Wrong keys or host URL; Cloud vs self-host mismatch. | Double-check `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST`. |
| **No traces visible** | Events not flushed before process exit. | Call `langfuse.flush()` (Python) or `await langfuse.flushAsync()` (TS). |
| **CORS errors (JS)** | Secret key exposed in browser code. | Always trace from the server side; never send the secret key to the client. |
| **Connection refused (self-host)** | Container not ready or wrong port mapping. | Run `docker compose logs langfuse` and verify port 3000 is mapped. |
| **Database migration errors** | Langfuse version upgraded but DB schema outdated. | Langfuse runs migrations automatically on startup. Check logs for errors and ensure your PostgreSQL version is compatible. |

## What You Learned

- Langfuse architecture: SDK, API, Database, and UI.
- How to set up Langfuse via Cloud or Docker Compose with a full environment variable reference.
- How to install the SDK in both Python and TypeScript.
- How to send and view your first trace.
- How to navigate the Langfuse dashboard.

---

| [Previous: Tutorial Overview](./index.md) | [Next: Chapter 2 -- Tracing Fundamentals](./02-tracing.md) |
