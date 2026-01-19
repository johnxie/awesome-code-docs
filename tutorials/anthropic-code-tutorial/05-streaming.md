---
layout: default
title: "Chapter 5: Streaming"
parent: "Anthropic API Tutorial"
nav_order: 5
---

# Chapter 5: Streaming

> Implement real-time response streaming for responsive user experiences with server-sent events and async patterns.

## Overview

Streaming allows Claude's responses to be delivered token-by-token as they're generated, rather than waiting for the complete response. This creates more responsive applications, enables progress indicators, and allows for early termination of requests.

## Basic Streaming

### Python Streaming

```python
import anthropic

client = anthropic.Anthropic()

# Stream a response
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short poem about coding."}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # Newline at end
```

### TypeScript Streaming

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

async function streamResponse() {
    const stream = await client.messages.stream({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        messages: [
            { role: "user", content: "Write a short poem about coding." }
        ]
    });

    for await (const event of stream) {
        if (event.type === 'content_block_delta' &&
            event.delta.type === 'text_delta') {
            process.stdout.write(event.delta.text);
        }
    }

    console.log();  // Newline at end
}

streamResponse();
```

### Raw Server-Sent Events

```python
import anthropic

client = anthropic.Anthropic()

# Low-level streaming with raw events
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
) as stream:
    for event in stream:
        print(f"Event type: {event.type}")

        if event.type == "message_start":
            print(f"Message ID: {event.message.id}")

        elif event.type == "content_block_start":
            print(f"Content block: {event.index}")

        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(f"Text: {event.delta.text}")

        elif event.type == "message_delta":
            print(f"Stop reason: {event.delta.stop_reason}")
            print(f"Output tokens: {event.usage.output_tokens}")

        elif event.type == "message_stop":
            print("Stream complete")
```

## Stream Event Types

### Event Structure

```python
# Server-sent event types:

# 1. message_start - Beginning of message
{
    "type": "message_start",
    "message": {
        "id": "msg_...",
        "type": "message",
        "role": "assistant",
        "content": [],
        "model": "claude-sonnet-4-20250514",
        "stop_reason": None,
        "usage": {"input_tokens": 25, "output_tokens": 1}
    }
}

# 2. content_block_start - Start of content block
{
    "type": "content_block_start",
    "index": 0,
    "content_block": {"type": "text", "text": ""}
}

# 3. content_block_delta - Content chunk
{
    "type": "content_block_delta",
    "index": 0,
    "delta": {"type": "text_delta", "text": "Hello"}
}

# 4. content_block_stop - End of content block
{
    "type": "content_block_stop",
    "index": 0
}

# 5. message_delta - Message metadata update
{
    "type": "message_delta",
    "delta": {"stop_reason": "end_turn"},
    "usage": {"output_tokens": 42}
}

# 6. message_stop - End of message
{
    "type": "message_stop"
}
```

### Handling Different Content Types

```python
def handle_stream_events(stream):
    """Handle all stream event types."""

    full_response = {
        "id": None,
        "content": [],
        "usage": {"input_tokens": 0, "output_tokens": 0},
        "stop_reason": None
    }

    current_block = None

    for event in stream:
        if event.type == "message_start":
            full_response["id"] = event.message.id
            full_response["usage"]["input_tokens"] = event.message.usage.input_tokens

        elif event.type == "content_block_start":
            block_type = event.content_block.type
            if block_type == "text":
                current_block = {"type": "text", "text": ""}
            elif block_type == "tool_use":
                current_block = {
                    "type": "tool_use",
                    "id": event.content_block.id,
                    "name": event.content_block.name,
                    "input": ""
                }

        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                current_block["text"] += event.delta.text
                yield {"type": "text", "text": event.delta.text}

            elif event.delta.type == "input_json_delta":
                current_block["input"] += event.delta.partial_json
                yield {"type": "tool_input", "partial": event.delta.partial_json}

        elif event.type == "content_block_stop":
            if current_block["type"] == "tool_use":
                import json
                current_block["input"] = json.loads(current_block["input"])
            full_response["content"].append(current_block)
            yield {"type": "block_complete", "block": current_block}

        elif event.type == "message_delta":
            full_response["stop_reason"] = event.delta.stop_reason
            full_response["usage"]["output_tokens"] = event.usage.output_tokens

        elif event.type == "message_stop":
            yield {"type": "complete", "response": full_response}
```

## Async Streaming

### Python Async

```python
import anthropic
import asyncio

async def stream_async():
    """Async streaming with the Anthropic API."""

    client = anthropic.AsyncAnthropic()

    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Explain quantum computing briefly."}
        ]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

    print()

# Run async function
asyncio.run(stream_async())
```

### Concurrent Streams

```python
import anthropic
import asyncio

async def process_prompt(client, prompt: str, stream_id: int):
    """Process a single prompt with streaming."""

    result = []
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            result.append(text)

    return stream_id, "".join(result)


async def stream_multiple_prompts(prompts: list[str]):
    """Stream multiple prompts concurrently."""

    client = anthropic.AsyncAnthropic()

    tasks = [
        process_prompt(client, prompt, i)
        for i, prompt in enumerate(prompts)
    ]

    results = await asyncio.gather(*tasks)
    return dict(results)


# Usage
prompts = [
    "What is Python?",
    "What is JavaScript?",
    "What is Rust?"
]

results = asyncio.run(stream_multiple_prompts(prompts))
for i, response in results.items():
    print(f"Response {i}: {response[:100]}...")
```

## Streaming with Tools

### Tool Use Streaming

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

def stream_with_tools(user_message: str):
    """Stream a response that may include tool use."""

    messages = [{"role": "user", "content": user_message}]

    while True:
        tool_calls = []
        text_content = []

        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages
        ) as stream:
            current_tool = None

            for event in stream:
                if event.type == "content_block_start":
                    if event.content_block.type == "tool_use":
                        current_tool = {
                            "id": event.content_block.id,
                            "name": event.content_block.name,
                            "input": ""
                        }
                        print(f"\n[Calling tool: {current_tool['name']}]")

                elif event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        print(event.delta.text, end="", flush=True)
                        text_content.append(event.delta.text)

                    elif event.delta.type == "input_json_delta":
                        current_tool["input"] += event.delta.partial_json

                elif event.type == "content_block_stop":
                    if current_tool:
                        current_tool["input"] = json.loads(current_tool["input"])
                        tool_calls.append(current_tool)
                        current_tool = None

            # Get final message for stop_reason
            final = stream.get_final_message()

        # If no tool calls, we're done
        if final.stop_reason != "tool_use":
            break

        # Execute tools and continue
        # Build assistant message content
        assistant_content = []
        if text_content:
            assistant_content.append({
                "type": "text",
                "text": "".join(text_content)
            })
        for tool in tool_calls:
            assistant_content.append({
                "type": "tool_use",
                "id": tool["id"],
                "name": tool["name"],
                "input": tool["input"]
            })

        messages.append({"role": "assistant", "content": assistant_content})

        # Execute tools and add results
        tool_results = []
        for tool in tool_calls:
            result = execute_tool(tool["name"], tool["input"])
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool["id"],
                "content": json.dumps(result)
            })
            print(f"\n[Tool result: {result}]")

        messages.append({"role": "user", "content": tool_results})

    print()  # Final newline


def execute_tool(name: str, input_data: dict) -> dict:
    """Execute a tool (mock implementation)."""
    if name == "get_weather":
        return {"temperature": 72, "conditions": "sunny"}
    return {"error": "Unknown tool"}


# Usage
stream_with_tools("What's the weather in San Francisco?")
```

## Web Application Integration

### FastAPI Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import anthropic

app = FastAPI()
client = anthropic.Anthropic()

async def generate_stream(prompt: str):
    """Generator for streaming response."""

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            # Format as server-sent event
            yield f"data: {text}\n\n"

    yield "data: [DONE]\n\n"


@app.get("/stream")
async def stream_endpoint(prompt: str):
    """Streaming endpoint."""

    return StreamingResponse(
        generate_stream(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

### Flask Streaming

```python
from flask import Flask, Response, request
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic()

def generate(prompt: str):
    """Generator for streaming response."""

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield f"data: {text}\n\n"

    yield "data: [DONE]\n\n"


@app.route('/stream')
def stream():
    prompt = request.args.get('prompt', 'Hello!')

    return Response(
        generate(prompt),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )
```

### Frontend JavaScript Client

```javascript
// EventSource for SSE
async function streamChat(prompt) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();  // Keep incomplete line

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') {
                    return;
                }
                // Update UI with new text
                appendToOutput(data);
            }
        }
    }
}

// React hook for streaming
function useStreamingChat() {
    const [response, setResponse] = useState('');
    const [isStreaming, setIsStreaming] = useState(false);

    const stream = async (prompt) => {
        setIsStreaming(true);
        setResponse('');

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            const reader = res.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const text = decoder.decode(value);
                setResponse(prev => prev + text);
            }
        } finally {
            setIsStreaming(false);
        }
    };

    return { response, isStreaming, stream };
}
```

## Stream Management

### Cancellation

```python
import anthropic
import signal
import sys

client = anthropic.Anthropic()

def handle_interrupt(signum, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\nStream cancelled by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

# Stream with cancellation support
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a very long story..."}]
) as stream:
    try:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    except KeyboardInterrupt:
        print("\n\nCancelled!")
```

### Progress Tracking

```python
class StreamProgress:
    """Track streaming progress."""

    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.tokens_received = 0
        self.text = ""
        self.start_time = None
        self.end_time = None

    def update(self, text_chunk: str, output_tokens: int = None):
        import time
        if self.start_time is None:
            self.start_time = time.time()

        self.text += text_chunk
        if output_tokens:
            self.tokens_received = output_tokens

    def complete(self, output_tokens: int):
        import time
        self.end_time = time.time()
        self.tokens_received = output_tokens

    @property
    def progress_percent(self) -> float:
        if self.max_tokens == 0:
            return 0
        return min(100, (self.tokens_received / self.max_tokens) * 100)

    @property
    def duration(self) -> float:
        import time
        if self.start_time is None:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time

    @property
    def tokens_per_second(self) -> float:
        if self.duration == 0:
            return 0
        return self.tokens_received / self.duration


# Usage
progress = StreamProgress(max_tokens=1024)

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story."}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                progress.update(event.delta.text)
                print(event.delta.text, end="", flush=True)

        elif event.type == "message_delta":
            progress.complete(event.usage.output_tokens)

print(f"\n\nTokens: {progress.tokens_received}")
print(f"Duration: {progress.duration:.2f}s")
print(f"Speed: {progress.tokens_per_second:.1f} tokens/sec")
```

### Buffering and Batching

```python
def stream_with_sentence_buffer(prompt: str):
    """Buffer stream output by sentences."""

    import re

    buffer = ""
    sentence_end = re.compile(r'[.!?]\s+')

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            buffer += text

            # Check for complete sentences
            while True:
                match = sentence_end.search(buffer)
                if not match:
                    break

                sentence = buffer[:match.end()]
                buffer = buffer[match.end():]

                # Yield complete sentence
                yield sentence

        # Yield remaining buffer
        if buffer:
            yield buffer


# Usage
for sentence in stream_with_sentence_buffer("Tell me three interesting facts."):
    print(f"Sentence: {sentence}")
```

## Best Practices

### Error Handling

```python
import anthropic
from anthropic import APIError, APIConnectionError

def robust_stream(prompt: str, max_retries: int = 3):
    """Stream with robust error handling."""

    client = anthropic.Anthropic()

    for attempt in range(max_retries):
        try:
            collected_text = []

            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    collected_text.append(text)
                    yield text

            return  # Success

        except APIConnectionError as e:
            if attempt == max_retries - 1:
                raise

            print(f"\nConnection error, retrying... ({attempt + 1}/{max_retries})")
            import time
            time.sleep(2 ** attempt)

            # Re-prompt with partial response context if needed
            if collected_text:
                partial = "".join(collected_text)
                prompt = f"Continue from: '{partial[-100:]}'"

        except APIError as e:
            print(f"\nAPI error: {e}")
            raise
```

### Memory Management

```python
def stream_large_response(prompt: str, chunk_callback=None):
    """Stream large responses without holding all in memory."""

    client = anthropic.Anthropic()
    total_tokens = 0

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=100000,  # Large response
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    # Process chunk immediately instead of accumulating
                    if chunk_callback:
                        chunk_callback(event.delta.text)
                    else:
                        print(event.delta.text, end="", flush=True)

            elif event.type == "message_delta":
                total_tokens = event.usage.output_tokens

    return total_tokens


# Write directly to file
with open("output.txt", "w") as f:
    tokens = stream_large_response(
        "Write a comprehensive guide...",
        chunk_callback=lambda text: f.write(text)
    )
```

### Timeout Handling

```python
import anthropic
import asyncio

async def stream_with_timeout(prompt: str, timeout_seconds: int = 60):
    """Stream with timeout protection."""

    client = anthropic.AsyncAnthropic()
    result = []

    async def do_stream():
        async with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text in stream.text_stream:
                result.append(text)
                print(text, end="", flush=True)

    try:
        await asyncio.wait_for(do_stream(), timeout=timeout_seconds)
    except asyncio.TimeoutError:
        print(f"\n\nStream timed out after {timeout_seconds}s")
        print(f"Received {len(result)} chunks before timeout")

    return "".join(result)


# Usage
response = asyncio.run(stream_with_timeout("Write a long essay...", timeout_seconds=30))
```

## Summary

In this chapter, you've learned:

- **Basic Streaming**: Implementing token-by-token response delivery
- **Event Types**: Understanding and handling all stream event types
- **Async Patterns**: Using async streaming for better concurrency
- **Tool Streaming**: Handling tool use in streaming responses
- **Web Integration**: Building streaming endpoints with FastAPI and Flask
- **Stream Management**: Cancellation, progress tracking, and buffering
- **Best Practices**: Error handling, memory management, and timeouts

## Key Takeaways

1. **Better UX**: Streaming provides immediate feedback to users
2. **Event-Driven**: Handle different event types appropriately
3. **Async Ready**: Use async for concurrent streaming operations
4. **Tool Support**: Tool use works seamlessly with streaming
5. **Robust Handling**: Implement proper error handling and timeouts

## Next Steps

Now that you can stream responses, let's explore Advanced Patterns in Chapter 6 for prompt engineering and optimization techniques.

---

**Ready for Chapter 6?** [Advanced Patterns](06-advanced-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
