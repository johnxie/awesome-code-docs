---
layout: default
title: "LiteLLM Tutorial - Chapter 4: Streaming & Async"
nav_order: 4
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 4: Streaming & Async

Welcome to **Chapter 4: Streaming & Async**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement real-time streaming responses and asynchronous processing for better user experience and performance.

## Overview

Streaming allows you to receive responses in real-time as they're generated, while async processing enables concurrent requests. This chapter covers both patterns and how to implement them with LiteLLM.

## Basic Streaming

Receive responses token by token:

```python
import litellm

response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a short story about AI"}],
    stream=True  # Enable streaming
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # New line at end
```

## Understanding Stream Chunks

Stream responses contain partial content:

```python
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Count to 10 slowly"}],
    stream=True
)

for i, chunk in enumerate(response):
    print(f"Chunk {i}:")
    print(f"  Content: {chunk.choices[0].delta.content}")
    print(f"  Finish reason: {chunk.choices[0].finish_reason}")
    print(f"  Usage: {chunk.usage}")
    print()
```

## Building a Streaming Chat Interface

Create an interactive chat with real-time responses:

```python
import litellm
import time

class StreamingChat:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.conversation = []

    def send_message(self, user_message):
        """Send a message and stream the response."""
        self.conversation.append({"role": "user", "content": user_message})

        response = litellm.completion(
            model=self.model,
            messages=self.conversation,
            stream=True,
            max_tokens=500
        )

        full_response = ""
        print("Assistant: ", end="", flush=True)

        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
                time.sleep(0.01)  # Small delay for readability

        print()  # New line
        self.conversation.append({"role": "assistant", "content": full_response})
        return full_response

# Usage
chat = StreamingChat()

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit']:
        break

    chat.send_message(user_input)
```

## Async Streaming

Handle multiple streaming requests concurrently:

```python
import asyncio
import litellm

async def stream_completion_async(model, messages):
    """Async streaming completion."""
    response = await litellm.acompletion(
        model=model,
        messages=messages,
        stream=True,
        max_tokens=300
    )

    full_content = ""
    async for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_content += content

    return full_content

async def main():
    messages = [{"role": "user", "content": "Explain async programming"}]

    print("Streaming response:")
    content = await stream_completion_async("gpt-4", messages)
    print(f"\n\nFull content length: {len(content)} characters")

# Run async function
asyncio.run(main())
```

## Concurrent Requests

Process multiple requests simultaneously:

```python
async def process_multiple_requests():
    """Process multiple LLM requests concurrently."""

    tasks = [
        litellm.acompletion(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Tell me a fact about topic {i}"}],
            max_tokens=100
        )
        for i in range(5)
    ]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    for i, response in enumerate(responses):
        content = response.choices[0].message.content
        print(f"Topic {i}: {content[:50]}...")

# Run concurrent requests
asyncio.run(process_multiple_requests())
```

## Streaming with Error Handling

Robust streaming with fallbacks:

```python
async def streaming_with_fallback(messages, primary_model="gpt-4", fallback_model="gpt-3.5-turbo"):
    """Stream with automatic fallback."""

    try:
        response = await litellm.acompletion(
            model=primary_model,
            messages=messages,
            stream=True,
            timeout=30
        )

        full_content = ""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_content += content

        return full_content, primary_model

    except Exception as e:
        print(f"\nPrimary model failed ({primary_model}), trying fallback ({fallback_model})...")
        print("Fallback: ", end="", flush=True)

        # Fallback to non-streaming for simplicity
        response = await litellm.acompletion(
            model=fallback_model,
            messages=messages,
            max_tokens=300
        )

        content = response.choices[0].message.content
        print(content)
        return content, fallback_model

async def main():
    messages = [{"role": "user", "content": "Write a haiku about programming"}]

    content, model_used = await streaming_with_fallback(messages)
    print(f"\nUsed model: {model_used}")

asyncio.run(main())
```

## WebSocket Streaming

Implement WebSocket-based streaming for web applications:

```python
# server.py (using FastAPI)
from fastapi import FastAPI, WebSocket
import litellm
import json

app = FastAPI()

@app.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    # Initialize conversation
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    try:
        while True:
            # Receive user message
            user_message = await websocket.receive_text()
            conversation.append({"role": "user", "content": user_message})

            # Stream response
            response = await litellm.acompletion(
                model="gpt-4",
                messages=conversation,
                stream=True
            )

            full_response = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content

                    # Send chunk to client
                    await websocket.send_text(json.dumps({
                        "type": "chunk",
                        "content": content
                    }))

            # Send completion signal
            await websocket.send_text(json.dumps({
                "type": "done",
                "full_content": full_response
            }))

            # Add to conversation history
            conversation.append({"role": "assistant", "content": full_response})

    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e)
        }))

# client.js (frontend)
const ws = new WebSocket('ws://localhost:8000/chat');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === 'chunk') {
        // Append chunk to response area
        responseDiv.textContent += data.content;
    } else if (data.type === 'done') {
        // Handle completion
        console.log('Response complete');
    } else if (data.type === 'error') {
        // Handle error
        console.error('Error:', data.message);
    }
};

// Send message
function sendMessage(message) {
    ws.send(message);
}
```

## Progress Indicators

Show progress during long generations:

```python
import threading
import time

def show_progress_indicator():
    """Show a simple progress indicator."""
    symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not hasattr(show_progress_indicator, 'stop'):
        print(f"\r{symbols[i % len(symbols)]} Generating response...", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r✓ Response complete!     ")

def stream_with_progress(model, messages):
    """Stream with progress indicator."""

    # Start progress indicator in background
    progress_thread = threading.Thread(target=show_progress_indicator)
    progress_thread.start()

    try:
        response = litellm.completion(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=1000
        )

        full_content = ""
        print("\r", end="", flush=True)  # Clear progress indicator

        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_content += content

        print()  # New line
        return full_content

    finally:
        # Stop progress indicator
        show_progress_indicator.stop = True
        progress_thread.join()

# Usage
messages = [{"role": "user", "content": "Write a 500-word essay about artificial intelligence"}]
content = stream_with_progress("gpt-4", messages)
```

## Rate Limiting with Async

Implement rate limiting for concurrent requests:

```python
import asyncio
from collections import deque
import time

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Acquire permission to make a request."""
        async with self.lock:
            now = time.time()

            # Remove old requests outside the time window
            while self.requests and now - self.requests[0] > 60:
                self.requests.popleft()

            # Check if we can make another request
            if len(self.requests) >= self.requests_per_minute:
                # Wait until oldest request expires
                wait_time = 60 - (now - self.requests[0])
                if wait_time > 0:
                    await asyncio.sleep(wait_time)

            self.requests.append(now)

rate_limiter = RateLimiter(requests_per_minute=50)

async def rate_limited_completion(model, messages):
    """Completion with rate limiting."""
    await rate_limiter.acquire()

    return await litellm.acompletion(
        model=model,
        messages=messages
    )

async def batch_with_rate_limit():
    """Process batch with rate limiting."""
    tasks = []
    for i in range(10):
        messages = [{"role": "user", "content": f"Generate idea {i}"}]
        tasks.append(rate_limited_completion("gpt-3.5-turbo", messages))

    results = await asyncio.gather(*tasks)

    for i, response in enumerate(results):
        print(f"Idea {i}: {response.choices[0].message.content[:50]}...")

asyncio.run(batch_with_rate_limit())
```

## Streaming File Processing

Process large files with streaming:

```python
async def stream_file_processing(file_path, model="gpt-4"):
    """Process a large file with streaming."""

    # Read file in chunks
    with open(file_path, 'r') as f:
        content = f.read()

    # Split into manageable chunks
    chunk_size = 4000  # characters
    chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    full_analysis = ""

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")

        messages = [
            {"role": "system", "content": "You are analyzing a large document. Provide insights for this section."},
            {"role": "user", "content": f"Analyze this section of the document:\n\n{chunk}"}
        ]

        response = await litellm.acompletion(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=500
        )

        chunk_analysis = ""
        async for chunk_response in response:
            if chunk_response.choices[0].delta.content:
                content_piece = chunk_response.choices[0].delta.content
                print(content_piece, end="", flush=True)
                chunk_analysis += content_piece

        full_analysis += f"\n\n--- Section {i + 1} ---\n{chunk_analysis}"
        print("\n")  # Section separator

    return full_analysis

# Usage
analysis = await stream_file_processing("large_document.txt")
```

## Performance Optimization

Tips for streaming performance:

1. **Chunk Processing**: Process responses in chunks rather than individual tokens for UI updates
2. **Connection Pooling**: Reuse connections for multiple requests
3. **Concurrent Limits**: Limit concurrent streaming requests to avoid overwhelming the API
4. **Error Recovery**: Implement automatic retry logic for failed chunks
5. **Buffering**: Buffer chunks before displaying to reduce UI flicker

## Best Practices

1. **User Feedback**: Always show users that streaming is in progress
2. **Error Handling**: Handle streaming errors gracefully (connection drops, timeouts)
3. **Rate Limiting**: Respect API rate limits, especially with concurrent requests
4. **Resource Management**: Clean up resources properly in async code
5. **UI Responsiveness**: Update UI efficiently to avoid blocking the main thread
6. **Fallback Strategies**: Have non-streaming fallbacks for when streaming fails
7. **Progress Indication**: Show meaningful progress indicators for long operations

Streaming and async processing enable responsive, scalable AI applications. These patterns work across all LiteLLM-supported providers, giving you consistent real-time capabilities regardless of the underlying model.

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- tutorial slug: **litellm-tutorial**
- chapter focus: **Chapter 4: Streaming & Async**
- system context: **Litellm Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 4: Streaming & Async`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
- [LiteLLM Docs](https://docs.litellm.ai/)

### Cross-Tutorial Connection Map

- [Langfuse Tutorial](../langfuse-tutorial/)
- [Vercel AI SDK Tutorial](../vercel-ai-tutorial/)
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/)
- [Aider Tutorial](../aider-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 4: Streaming & Async`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `content`, `messages`, `chunk` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Streaming & Async` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `print`, `response`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Streaming & Async` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `content`.
2. **Input normalization**: shape incoming data so `messages` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `chunk`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
  Why it matters: authoritative reference on `LiteLLM Repository` (github.com).
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
  Why it matters: authoritative reference on `LiteLLM Releases` (github.com).
- [LiteLLM Docs](https://docs.litellm.ai/)
  Why it matters: authoritative reference on `LiteLLM Docs` (docs.litellm.ai).

Suggested trace strategy:
- search upstream code for `content` and `messages` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Completion API](03-completion.md)
- [Next Chapter: Chapter 5: Fallbacks & Retries](05-fallbacks.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
