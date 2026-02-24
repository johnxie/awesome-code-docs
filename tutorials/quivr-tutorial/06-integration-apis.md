---
layout: default
title: "Chapter 6: Integration APIs"
parent: "Quivr Tutorial"
nav_order: 6
---

# Chapter 6: Integration APIs

Welcome to **Chapter 6: Integration APIs**. In this part of **Quivr Tutorial: Open-Source RAG Framework for Document Ingestion**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In [Chapter 5](05-knowledge-bases.md), you organized your documents into governed knowledge bases. Now it is time to make that knowledge accessible to the rest of your organization. Whether you are building a Slack bot, embedding a search widget in your internal portal, or feeding answers into a CI/CD pipeline, Quivr's APIs are how you connect.

This chapter covers the full spectrum of integration patterns: REST API endpoints for document ingestion and querying, streaming responses via Server-Sent Events, webhook notifications, the Python SDK for programmatic access, and authentication best practices for securing every call.

## API Architecture

```mermaid
flowchart TD
    A[External Applications] --> B[API Gateway]
    B --> C{Authentication}
    C -->|Valid Token| D[Rate Limiter]
    C -->|Invalid| E[401 Unauthorized]
    D --> F{Route}
    F -->|/ingest| G[Ingestion Service]
    F -->|/query| H[Query Service]
    F -->|/kb| I[KB Management Service]
    F -->|/stream| J[Streaming Service]
    F -->|/webhook| K[Webhook Manager]

    G --> L[Document Pipeline]
    H --> M[Retrieval + LLM]
    I --> N[CRUD Operations]
    J --> O[SSE / WebSocket]
    K --> P[Event Dispatch]

    classDef external fill:#e1f5fe,stroke:#01579b
    classDef gateway fill:#f3e5f5,stroke:#4a148c
    classDef service fill:#fff3e0,stroke:#ef6c00
    classDef backend fill:#e8f5e8,stroke:#1b5e20

    class A external
    class B,C,D,F gateway
    class G,H,I,J,K service
    class L,M,N,O,P backend
```

## REST API Reference

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/ingest` | Upload a document to a knowledge base | Yes |
| `POST` | `/api/v1/ingest/batch` | Upload multiple documents | Yes |
| `POST` | `/api/v1/query` | Ask a question against a knowledge base | Yes |
| `POST` | `/api/v1/query/stream` | Stream a response via SSE | Yes |
| `GET` | `/api/v1/kb` | List knowledge bases | Yes |
| `POST` | `/api/v1/kb` | Create a knowledge base | Yes |
| `GET` | `/api/v1/kb/{id}` | Get knowledge base details | Yes |
| `DELETE` | `/api/v1/kb/{id}` | Delete a knowledge base | Yes |
| `GET` | `/api/v1/kb/{id}/documents` | List documents in a KB | Yes |
| `DELETE` | `/api/v1/kb/{id}/documents/{doc_id}` | Delete a document | Yes |
| `GET` | `/api/v1/health` | Health check | No |

### Document Ingestion

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {
    "Authorization": "Bearer your-api-key"
}

# Upload a single document
with open("docs/report.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/ingest",
        headers=HEADERS,
        files={"file": ("report.pdf", f, "application/pdf")},
        data={
            "knowledge_base_id": "kb-123",
            "metadata": '{"team": "engineering", "doc_type": "report"}',
            "chunk_size": 1000,
            "chunk_overlap": 200
        }
    )

result = response.json()
print(f"Status: {response.status_code}")
print(f"Document ID: {result['document_id']}")
print(f"Chunks created: {result['chunk_count']}")
print(f"Processing time: {result['processing_time_ms']}ms")
```

### Batch Ingestion

```python
import requests
import json

# Upload multiple documents in one request
files = [
    ("files", ("doc1.pdf", open("docs/doc1.pdf", "rb"), "application/pdf")),
    ("files", ("doc2.txt", open("docs/doc2.txt", "rb"), "text/plain")),
    ("files", ("doc3.md", open("docs/doc3.md", "rb"), "text/markdown")),
]

response = requests.post(
    f"{BASE_URL}/ingest/batch",
    headers=HEADERS,
    files=files,
    data={
        "knowledge_base_id": "kb-123",
        "metadata": json.dumps({
            "team": "engineering",
            "status": "published"
        }),
        "on_error": "continue"    # "continue" or "abort"
    }
)

result = response.json()
print(f"Successful: {result['successful']}")
print(f"Failed: {result['failed']}")
for doc in result['documents']:
    print(f"  {doc['filename']}: {doc['status']} ({doc['chunk_count']} chunks)")
```

### Querying

```python
import requests

# Ask a question
response = requests.post(
    f"{BASE_URL}/query",
    headers={
        **HEADERS,
        "Content-Type": "application/json"
    },
    json={
        "knowledge_base_id": "kb-123",
        "question": "How do we handle database migrations?",
        "top_k": 5,
        "score_threshold": 0.7,
        "filters": {
            "doc_type": {"$in": ["runbook", "guide"]},
            "status": "published"
        },
        "include_sources": True,
        "model": "gpt-4-turbo-preview",
        "temperature": 0.3,
        "max_tokens": 1000
    }
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
print(f"Sources:")
for source in result['sources']:
    print(f"  - {source['filename']} (page {source['page']}, "
          f"score: {source['score']:.4f})")
print(f"Tokens used: {result['usage']['total_tokens']}")
print(f"Latency: {result['latency_ms']}ms")
```

## Streaming Responses

For real-time user interfaces, Quivr supports streaming via Server-Sent Events (SSE).

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API Gateway
    participant R as Retrieval Engine
    participant L as LLM

    C->>A: POST /query/stream
    A->>R: Retrieve context
    R-->>A: Context chunks
    A->>L: Generate (stream=True)

    loop Token Stream
        L-->>A: Token chunk
        A-->>C: SSE: data: {"token": "..."}
    end

    A-->>C: SSE: data: {"sources": [...]}
    A-->>C: SSE: event: done
```

### SSE Streaming Client

```python
import requests
import json

def stream_query(question, kb_id):
    """Stream a response from Quivr using Server-Sent Events."""
    response = requests.post(
        f"{BASE_URL}/query/stream",
        headers={
            **HEADERS,
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        },
        json={
            "knowledge_base_id": kb_id,
            "question": question,
            "top_k": 5,
            "model": "gpt-4-turbo-preview"
        },
        stream=True
    )

    full_answer = ""
    sources = []

    for line in response.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue

        data = json.loads(line[6:])  # Strip "data: " prefix

        if data.get("type") == "token":
            token = data["token"]
            full_answer += token
            print(token, end="", flush=True)

        elif data.get("type") == "sources":
            sources = data["sources"]

        elif data.get("type") == "done":
            break

    print(f"\n\nSources: {len(sources)}")
    for s in sources:
        print(f"  - {s['filename']} (score: {s['score']:.4f})")

    return full_answer, sources

answer, sources = stream_query(
    "How do we deploy to production?",
    "kb-123"
)
```

### WebSocket Streaming

```python
import asyncio
import websockets
import json

async def ws_query(question, kb_id):
    """Stream responses via WebSocket for bidirectional communication."""
    uri = f"ws://localhost:8000/api/v1/ws/query"

    async with websockets.connect(
        uri,
        extra_headers={"Authorization": f"Bearer your-api-key"}
    ) as ws:
        # Send query
        await ws.send(json.dumps({
            "knowledge_base_id": kb_id,
            "question": question,
            "top_k": 5
        }))

        full_answer = ""

        # Receive streamed response
        async for message in ws:
            data = json.loads(message)

            if data["type"] == "token":
                full_answer += data["token"]
                print(data["token"], end="", flush=True)

            elif data["type"] == "sources":
                print(f"\n\nSources: {data['sources']}")

            elif data["type"] == "error":
                print(f"\nError: {data['message']}")
                break

            elif data["type"] == "done":
                break

        return full_answer

asyncio.run(ws_query("Explain our CI/CD pipeline", "kb-123"))
```

## Python SDK

The Quivr Python SDK wraps the REST API with a clean, Pythonic interface.

```python
from quivr import QuivrClient

client = QuivrClient(
    api_key="your-api-key",
    base_url="http://localhost:8000",
    timeout=60,
    max_retries=3
)

# List knowledge bases
kbs = client.knowledge_bases.list()
for kb in kbs:
    print(f"{kb.name}: {kb.document_count} documents")

# Upload a document
doc = client.documents.upload(
    knowledge_base_id="kb-123",
    file_path="docs/guide.pdf",
    metadata={"team": "platform", "doc_type": "guide"}
)
print(f"Uploaded: {doc.id} ({doc.chunk_count} chunks)")

# Ask a question
response = client.query(
    knowledge_base_id="kb-123",
    question="How do we handle incidents?",
    top_k=5,
    filters={"status": "published"}
)

print(f"Answer: {response.answer}")
for source in response.sources:
    print(f"  Source: {source.filename} (score: {source.score:.4f})")
```

### Async SDK

```python
import asyncio
from quivr import AsyncQuivrClient

async def main():
    client = AsyncQuivrClient(
        api_key="your-api-key",
        base_url="http://localhost:8000"
    )

    # Concurrent queries across multiple knowledge bases
    tasks = [
        client.query(
            knowledge_base_id=kb_id,
            question="What are the key metrics to monitor?"
        )
        for kb_id in ["kb-eng", "kb-ops", "kb-sre"]
    ]

    results = await asyncio.gather(*tasks)

    for kb_id, result in zip(["kb-eng", "kb-ops", "kb-sre"], results):
        print(f"[{kb_id}] {result.answer[:100]}...")

    await client.close()

asyncio.run(main())
```

## Webhooks

Webhooks notify external systems when events occur in Quivr.

### Webhook Events

| Event | Trigger | Payload |
|-------|---------|---------|
| `document.uploaded` | New document ingested | Document ID, filename, chunk count |
| `document.deleted` | Document removed | Document ID, filename |
| `document.updated` | Document re-processed | Document ID, old/new chunk count |
| `kb.created` | New knowledge base created | KB ID, name, creator |
| `kb.deleted` | Knowledge base deleted | KB ID, name |
| `query.completed` | Query answered | Query text, latency, source count |
| `sync.completed` | Source sync finished | KB ID, added/updated/deleted counts |
| `error.ingestion` | Ingestion failure | File path, error message |

### Registering Webhooks

```python
from quivr import QuivrClient

client = QuivrClient(api_key="your-api-key")

# Register a webhook
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/quivr",
    events=[
        "document.uploaded",
        "document.deleted",
        "error.ingestion",
        "sync.completed"
    ],
    secret="your-webhook-secret",  # For signature verification
    active=True
)

print(f"Webhook ID: {webhook.id}")
print(f"Events: {webhook.events}")

# List registered webhooks
webhooks = client.webhooks.list()
for wh in webhooks:
    print(f"{wh.id}: {wh.url} ({', '.join(wh.events)})")
```

### Webhook Handler

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your-webhook-secret"

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify the webhook signature."""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

@app.route("/webhooks/quivr", methods=["POST"])
def handle_webhook():
    # Verify signature
    signature = request.headers.get("X-Quivr-Signature")
    if not verify_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    event = request.json
    event_type = event["type"]

    if event_type == "document.uploaded":
        doc = event["data"]
        print(f"New document: {doc['filename']} ({doc['chunk_count']} chunks)")
        # Notify Slack, update dashboard, etc.

    elif event_type == "error.ingestion":
        error = event["data"]
        print(f"Ingestion error: {error['file_path']} - {error['message']}")
        # Alert on-call engineer

    elif event_type == "sync.completed":
        sync = event["data"]
        print(f"Sync completed: +{sync['added']}, "
              f"~{sync['updated']}, -{sync['deleted']}")

    return jsonify({"status": "ok"}), 200
```

## Integration Patterns

### Slack Bot Integration

```python
from slack_bolt import App
from quivr import QuivrClient

slack_app = App(token="xoxb-your-slack-token")
quivr = QuivrClient(api_key="your-api-key")

@slack_app.message("quivr:")
def handle_quivr_query(message, say):
    """Handle messages starting with 'quivr:' and return answers."""
    question = message["text"].replace("quivr:", "").strip()

    # Show typing indicator
    say("Searching knowledge base...")

    # Query Quivr
    response = quivr.query(
        knowledge_base_id="kb-eng",
        question=question,
        top_k=5
    )

    # Format response for Slack
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": response.answer
            }
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Sources: {', '.join(s.filename for s in response.sources)}"
                }
            ]
        }
    ]

    say(blocks=blocks)

slack_app.start(port=3000)
```

### FastAPI Middleware

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from quivr import QuivrClient

app = FastAPI()
security = HTTPBearer()
quivr = QuivrClient(api_key="your-api-key")

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verify the bearer token and return user context."""
    token = credentials.credentials
    # Validate token with your auth provider
    user = await validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.post("/api/ask")
async def ask_question(
    question: str,
    kb_id: str,
    user=Depends(verify_token)
):
    """Proxy question to Quivr with user context."""
    response = quivr.query(
        knowledge_base_id=kb_id,
        question=question,
        top_k=5,
        filters={"accessible_by": user.team}
    )

    return {
        "answer": response.answer,
        "sources": [
            {"filename": s.filename, "score": s.score}
            for s in response.sources
        ],
        "query_id": response.query_id
    }
```

### CI/CD Pipeline Integration

```python
#!/usr/bin/env python3
"""CI/CD script to sync documentation to Quivr after deployment."""

import subprocess
import glob
from quivr import QuivrClient

def sync_docs_to_quivr():
    client = QuivrClient(api_key="your-ci-cd-api-key")

    # Get changed files from the latest commit
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", "docs/"],
        capture_output=True, text=True
    )
    changed_files = result.stdout.strip().split("\n")
    changed_files = [f for f in changed_files if f]  # Remove empty strings

    if not changed_files:
        print("No documentation changes detected.")
        return

    print(f"Found {len(changed_files)} changed docs:")

    for file_path in changed_files:
        try:
            doc = client.documents.upload(
                knowledge_base_id="kb-eng",
                file_path=file_path,
                metadata={
                    "source": "ci-cd",
                    "commit": subprocess.run(
                        ["git", "rev-parse", "HEAD"],
                        capture_output=True, text=True
                    ).stdout.strip()[:8]
                },
                deduplicate=True       # Update if already exists
            )
            print(f"  Synced: {file_path} ({doc.chunk_count} chunks)")
        except Exception as e:
            print(f"  ERROR: {file_path} - {e}")

if __name__ == "__main__":
    sync_docs_to_quivr()
```

## Authentication and Security

### API Key Management

```python
from quivr.admin import APIKeyAdmin

admin = APIKeyAdmin(master_key="your-master-key")

# Create a key with specific scopes
key = admin.create_key(
    name="production-read",
    scopes=["query", "kb:read"],
    rate_limit={
        "requests_per_minute": 100,
        "tokens_per_day": 1000000
    },
    ip_restrictions=["10.0.0.0/8", "172.16.0.0/12"],
    expires_in_days=90
)

# Rotate a key (old key remains valid for grace period)
new_key = admin.rotate_key(
    key_id=key.id,
    grace_period_hours=24       # Old key works for 24 more hours
)

# Revoke a key immediately
admin.revoke_key(key_id=compromised_key.id)

# Audit key usage
usage = admin.get_key_usage(
    key_id=key.id,
    period_days=30
)
print(f"Requests: {usage.total_requests}")
print(f"Tokens consumed: {usage.total_tokens:,}")
print(f"Errors: {usage.error_count}")
print(f"Unique IPs: {usage.unique_ips}")
```

### Security Configuration Matrix

| Setting | Development | Staging | Production |
|---------|-------------|---------|------------|
| HTTPS | Optional | Required | Required |
| API key rotation | Manual | 90 days | 30 days |
| Rate limit (RPM) | Unlimited | 500 | 100 per key |
| IP restrictions | None | VPN only | VPN + allowlist |
| Token budget | Unlimited | 1M/day | Per-key limits |
| Audit logging | Optional | Enabled | Enabled + alerts |
| CORS origins | `*` | Staging URLs | Production URLs only |
| Request body limit | 100 MB | 50 MB | 25 MB |

## Error Handling

### Standard Error Responses

```python
from quivr import QuivrClient
from quivr.exceptions import (
    QuivrAuthError,
    QuivrRateLimitError,
    QuivrNotFoundError,
    QuivrValidationError,
    QuivrServerError
)

client = QuivrClient(api_key="your-api-key")

try:
    response = client.query(
        knowledge_base_id="kb-123",
        question="How do we deploy?"
    )
except QuivrAuthError as e:
    print(f"Authentication failed: {e.message}")
    # Refresh or rotate API key

except QuivrRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after_seconds}s")
    # Implement exponential backoff

except QuivrNotFoundError as e:
    print(f"Resource not found: {e.resource_type} {e.resource_id}")
    # Verify KB ID exists

except QuivrValidationError as e:
    print(f"Validation error: {e.field} - {e.message}")
    # Fix request parameters

except QuivrServerError as e:
    print(f"Server error ({e.status_code}): {e.message}")
    # Retry or alert on-call
```

### HTTP Status Code Reference

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Fix request parameters |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Verify permissions / KB access |
| 404 | Not Found | Verify resource ID |
| 409 | Conflict | Duplicate resource; use update instead |
| 429 | Rate Limited | Back off and retry after `Retry-After` header |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | System overloaded; retry later |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| 401 on every request | Expired or invalid API key | Regenerate key; check `Authorization` header format |
| 403 after key rotation | Old key revoked too soon | Use `grace_period_hours` during rotation |
| Slow streaming | Network latency or large context | Reduce `top_k`; use WebSocket instead of SSE |
| Webhook not firing | URL unreachable from Quivr | Check firewall rules; verify URL responds to POST |
| Webhook signature mismatch | Wrong secret or encoding | Verify secret matches; compare raw body (not parsed JSON) |
| Rate limit hit too early | Multiple services sharing one key | Create separate keys per service with individual limits |
| Large file upload timeout | Default timeout too short | Increase `timeout` to 120s; use batch endpoint for many files |

## Summary

Integration APIs are how Quivr delivers value beyond its own interface. In this chapter you learned:

- **REST API** endpoints for ingestion, querying, and knowledge base management
- **Streaming** via SSE and WebSockets for real-time response delivery
- **Python SDK** for clean programmatic access, including async support
- **Webhooks** for event-driven integrations with signature verification
- **Integration Patterns** for Slack bots, FastAPI middleware, and CI/CD pipelines
- **Authentication** with scoped API keys, rotation, and audit logging
- **Error Handling** with typed exceptions and retry strategies

## Key Takeaways

1. **Use streaming for user-facing applications** -- waiting for a full response before displaying anything feels slow.
2. **Create separate API keys per integration** -- one compromised key should not expose everything.
3. **Verify webhook signatures** -- never trust incoming webhook payloads without cryptographic verification.
4. **Implement retry logic** -- rate limits and transient errors are normal; handle them gracefully.
5. **Log and audit API usage** -- visibility into who is calling what and how often is essential for debugging and security.

## Next Steps

Your APIs are connected and secured. In [Chapter 7: Customization](07-customization.md), you will learn how to extend Quivr with custom preprocessing steps, reranking models, prompt templates, and UI components.

---

*Built with insights from the [Quivr](https://github.com/QuivrHQ/quivr) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `print`, `response`, `question` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Integration APIs` as an operating subsystem inside **Quivr Tutorial: Open-Source RAG Framework for Document Ingestion**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `result`, `quivr`, `sources` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Integration APIs` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `print`.
2. **Input normalization**: shape incoming data so `response` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `question`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/QuivrHQ/quivr)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `print` and `response` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Knowledge Bases](05-knowledge-bases.md)
- [Next Chapter: Chapter 7: Customization](07-customization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
