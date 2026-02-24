---
layout: default
title: "Chapter 2: Messages API"
parent: "Anthropic API Tutorial"
nav_order: 2
---

# Chapter 2: Messages API

Welcome to **Chapter 2: Messages API**. In this part of **Anthropic API Tutorial: Build Production Apps with Claude**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master the core Messages API for building conversations with Claude, including multi-turn dialogues, system prompts, and message handling patterns.

## Overview

The Messages API is the foundation of all interactions with Claude. This chapter covers how to structure conversations, manage context, use system prompts effectively, and handle different response types.

## Message Structure

### Basic Message Format

```python
import anthropic

client = anthropic.Anthropic()

# Single message request
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
)

print(message.content[0].text)
# Output: The capital of France is Paris.
```

### Message Roles

```python
# Messages have two roles: "user" and "assistant"
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there! How can I help you today?"},
    {"role": "user", "content": "Tell me about Python."}
]

# The conversation must:
# - Start with a "user" message
# - Alternate between "user" and "assistant"
# - End with a "user" message (for the API to respond)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)
```

### Content Blocks

```python
# Content can be a string or array of content blocks
# String format (simple)
messages = [
    {"role": "user", "content": "Hello!"}
]

# Content blocks format (for mixed content)
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": "base64_encoded_image_data"
                }
            }
        ]
    }
]
```

## Multi-Turn Conversations

### Building Conversation History

```python
class ConversationManager:
    """Manage multi-turn conversations with Claude."""

    def __init__(self, model="claude-sonnet-4-20250514", system=None):
        self.client = anthropic.Anthropic()
        self.model = model
        self.system = system
        self.messages = []

    def send(self, user_message: str) -> str:
        """Send a message and get a response."""

        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Make API call
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system,
            messages=self.messages
        )

        # Extract assistant response
        assistant_message = response.content[0].text

        # Add to history
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear(self):
        """Clear conversation history."""
        self.messages = []

    def get_history(self):
        """Get full conversation history."""
        return self.messages

# Usage
conversation = ConversationManager(
    system="You are a helpful Python tutor."
)

print(conversation.send("What are list comprehensions?"))
print(conversation.send("Can you show me an example?"))
print(conversation.send("How do I add conditions to them?"))
```

### Prefilling Assistant Responses

```python
# You can prefill the assistant's response to guide output format
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is 2+2? Reply with just the number."},
        {"role": "assistant", "content": "The answer is: "}  # Prefill
    ]
)

# Claude will continue from the prefill
print(message.content[0].text)  # Output: 4

# Use prefill for JSON output
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "List 3 programming languages as JSON with name and year."
        },
        {"role": "assistant", "content": "["}  # Force JSON array output
    ]
)

# Parse the JSON (prepend the prefill)
import json
json_str = "[" + message.content[0].text
data = json.loads(json_str)
```

## System Prompts

### Basic System Prompts

```python
# System prompts set Claude's behavior and context
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant that speaks like a pirate.",
    messages=[
        {"role": "user", "content": "How do I learn programming?"}
    ]
)

# Claude responds in pirate speak
```

### Structured System Prompts

```python
# Multi-section system prompt
system_prompt = """You are an expert code reviewer.

## Your Role
- Review code for bugs, security issues, and best practices
- Provide constructive feedback
- Suggest improvements with examples

## Response Format
For each issue found:
1. Severity: HIGH/MEDIUM/LOW
2. Location: file and line number
3. Issue: Description of the problem
4. Fix: Suggested solution with code

## Guidelines
- Be thorough but not pedantic
- Focus on significant issues first
- Explain why something is problematic
- Provide working code examples
"""

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    system=system_prompt,
    messages=[
        {"role": "user", "content": f"Review this code:\n```python\n{code}\n```"}
    ]
)
```

### System Prompt with Context

```python
def create_assistant_with_context(documents: list[str], user_info: dict):
    """Create a contextual assistant with document knowledge."""

    context = "\n\n".join([f"Document {i+1}:\n{doc}"
                          for i, doc in enumerate(documents)])

    system = f"""You are a helpful assistant for {user_info['name']}.

## User Context
- Name: {user_info['name']}
- Role: {user_info['role']}
- Preferences: {user_info.get('preferences', 'None specified')}

## Available Knowledge
{context}

## Instructions
- Answer questions based on the provided documents
- If information isn't in the documents, say so clearly
- Personalize responses based on user context
- Be concise but thorough
"""

    return system

# Usage
system = create_assistant_with_context(
    documents=["Product manual...", "FAQ document..."],
    user_info={"name": "Alice", "role": "Developer"}
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=system,
    messages=[{"role": "user", "content": "How do I reset my password?"}]
)
```

## Request Parameters

### Token Limits

```python
# max_tokens controls response length
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,  # Short response
    messages=[{"role": "user", "content": "Explain machine learning."}]
)

# Check if response was truncated
if message.stop_reason == "max_tokens":
    print("Response was truncated due to token limit")
else:
    print("Response completed naturally")
```

### Temperature and Sampling

```python
# Temperature controls randomness (0.0 = deterministic, 1.0 = creative)
# For factual tasks
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.0,  # Most deterministic
    messages=[{"role": "user", "content": "What is the boiling point of water?"}]
)

# For creative tasks
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.9,  # More creative
    messages=[{"role": "user", "content": "Write a creative poem about coding."}]
)

# Top-p (nucleus sampling) - alternative to temperature
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    top_p=0.9,  # Consider tokens with cumulative probability of 0.9
    messages=[{"role": "user", "content": "Tell me a story."}]
)

# Top-k sampling
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    top_k=50,  # Only consider top 50 tokens at each step
    messages=[{"role": "user", "content": "Generate a random name."}]
)
```

### Stop Sequences

```python
# Stop generation when specific strings are encountered
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    stop_sequences=["END", "STOP", "---"],
    messages=[
        {
            "role": "user",
            "content": "List 3 items, then write END"
        }
    ]
)

# Check what caused the stop
if message.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {message.stop_sequence}")
```

## Response Handling

### Content Block Types

```python
# Responses can contain multiple content blocks
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain recursion with code."}]
)

for block in message.content:
    if block.type == "text":
        print(f"Text: {block.text}")
    elif block.type == "tool_use":
        print(f"Tool call: {block.name}")
        print(f"Input: {block.input}")
```

### Extracting Structured Data

```python
import json

def extract_json_response(content: str) -> dict:
    """Extract JSON from Claude's response."""

    # Try to parse the entire response as JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try to find JSON in code blocks
    import re
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find JSON objects/arrays
    json_patterns = [
        r'\{[\s\S]*\}',  # Objects
        r'\[[\s\S]*\]'   # Arrays
    ]

    for pattern in json_patterns:
        match = re.search(pattern, content)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                continue

    raise ValueError("No valid JSON found in response")

# Usage
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Return a JSON object with name, age, and city for a fictional person."
        }
    ]
)

data = extract_json_response(message.content[0].text)
print(data)
```

### Response Validation

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIResponse:
    """Structured API response with metadata."""
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    stop_reason: str
    is_truncated: bool

def make_validated_request(client, **kwargs) -> APIResponse:
    """Make API request with response validation."""

    message = client.messages.create(**kwargs)

    # Extract text content
    text_content = ""
    for block in message.content:
        if block.type == "text":
            text_content += block.text

    return APIResponse(
        text=text_content,
        model=message.model,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
        stop_reason=message.stop_reason,
        is_truncated=message.stop_reason == "max_tokens"
    )

# Usage
response = make_validated_request(
    client,
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

print(f"Response: {response.text}")
print(f"Tokens used: {response.input_tokens} in, {response.output_tokens} out")
if response.is_truncated:
    print("Warning: Response was truncated")
```

## Context Management

### Token Counting

```python
# The API returns token counts in the response
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, world!"}]
)

print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")

# Estimate tokens before sending (approximate)
def estimate_tokens(text: str) -> int:
    """Rough estimate: ~4 characters per token for English."""
    return len(text) // 4

estimated = estimate_tokens("Hello, world!")
print(f"Estimated tokens: {estimated}")
```

### Context Window Management

```python
class ContextManager:
    """Manage conversation context within token limits."""

    def __init__(self, max_context_tokens=180000):  # Leave room for response
        self.max_tokens = max_context_tokens
        self.messages = []
        self.system = ""
        self.system_tokens = 0

    def set_system(self, system: str):
        """Set system prompt."""
        self.system = system
        self.system_tokens = len(system) // 4  # Rough estimate

    def add_message(self, role: str, content: str):
        """Add message to context."""
        self.messages.append({"role": role, "content": content})

    def get_context(self) -> list:
        """Get messages that fit within context window."""
        total_tokens = self.system_tokens
        valid_messages = []

        # Work backwards from most recent
        for msg in reversed(self.messages):
            msg_tokens = len(msg["content"]) // 4
            if total_tokens + msg_tokens > self.max_tokens:
                break
            valid_messages.insert(0, msg)
            total_tokens += msg_tokens

        return valid_messages

    def summarize_old_context(self, client) -> str:
        """Summarize older messages to preserve context."""
        if len(self.messages) < 10:
            return ""

        old_messages = self.messages[:-5]  # Keep last 5 intact
        old_text = "\n".join([f"{m['role']}: {m['content']}"
                             for m in old_messages])

        summary_response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation briefly:\n{old_text}"
            }]
        )

        return summary_response.content[0].text
```

## Metadata and Tracking

### Request Metadata

```python
# Add metadata for tracking and analytics
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    metadata={
        "user_id": "user_123",
        "session_id": "session_456",
        "request_type": "chat"
    },
    messages=[{"role": "user", "content": "Hello!"}]
)

# Metadata is stored with the request for tracking
```

### Logging and Debugging

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_request(client, **kwargs):
    """Make API request with logging."""

    start_time = datetime.now()
    request_id = f"req_{start_time.timestamp()}"

    logger.info(f"[{request_id}] Starting request to {kwargs.get('model')}")
    logger.debug(f"[{request_id}] Messages: {kwargs.get('messages')}")

    try:
        message = client.messages.create(**kwargs)

        duration = (datetime.now() - start_time).total_seconds()

        logger.info(
            f"[{request_id}] Completed in {duration:.2f}s - "
            f"Tokens: {message.usage.input_tokens} in, "
            f"{message.usage.output_tokens} out"
        )

        return message

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"[{request_id}] Failed after {duration:.2f}s: {e}")
        raise

# Usage
message = logged_request(
    client,
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Best Practices

### Conversation Design

```python
# 1. Keep system prompts focused
system = """You are a customer service agent for TechCorp.
- Be helpful and professional
- If you can't help, provide contact information
- Never discuss competitor products"""

# 2. Maintain conversation coherence
# Good: Include relevant context
messages = [
    {"role": "user", "content": "I bought Product X last week"},
    {"role": "assistant", "content": "Thank you for purchasing Product X! How can I help you with it?"},
    {"role": "user", "content": "It stopped working"}  # Context maintained
]

# 3. Use clear, specific prompts
# Instead of: "Help me with code"
# Use: "Fix the null pointer exception in this Python function: [code]"
```

### Error Recovery

```python
def resilient_conversation(client, messages, max_retries=3):
    """Handle conversation with error recovery."""

    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=messages
            )
        except anthropic.RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
        except anthropic.BadRequestError as e:
            # Try to fix common issues
            if "messages" in str(e).lower():
                # Might be a message format issue
                messages = fix_message_format(messages)
                continue
            raise

def fix_message_format(messages):
    """Fix common message format issues."""
    fixed = []
    last_role = None

    for msg in messages:
        # Skip empty messages
        if not msg.get("content"):
            continue

        # Ensure alternating roles
        if msg["role"] == last_role:
            # Merge consecutive same-role messages
            fixed[-1]["content"] += "\n" + msg["content"]
        else:
            fixed.append(msg)
            last_role = msg["role"]

    # Ensure starts with user
    if fixed and fixed[0]["role"] != "user":
        fixed.insert(0, {"role": "user", "content": "Continue."})

    return fixed
```

## Summary

In this chapter, you've learned:

- **Message Structure**: How to format messages and content blocks
- **Multi-Turn Conversations**: Building and managing conversation history
- **System Prompts**: Configuring Claude's behavior and context
- **Request Parameters**: Controlling response length, temperature, and stopping
- **Response Handling**: Parsing and validating API responses
- **Context Management**: Working within token limits effectively
- **Metadata**: Tracking requests for analytics and debugging

## Key Takeaways

1. **Alternate Roles**: Messages must alternate between user and assistant
2. **System Prompts**: Use them to set consistent behavior and context
3. **Prefilling**: Guide output format by prefilling assistant responses
4. **Token Awareness**: Monitor and manage token usage
5. **Validate Responses**: Check stop_reason and handle truncation

## Next Steps

Now that you understand the Messages API, let's explore Tool Use in Chapter 3, where Claude can call functions and interact with external systems.

---

**Ready for Chapter 3?** [Tool Use](03-tool-use.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `messages`, `content`, `self` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Messages API` as an operating subsystem inside **Anthropic API Tutorial: Build Production Apps with Claude**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `user`, `message`, `role` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Messages API` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `messages`.
2. **Input normalization**: shape incoming data so `content` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `self`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
  Why it matters: authoritative reference on `Anthropic Python SDK` (github.com).
- [Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
  Why it matters: authoritative reference on `Anthropic TypeScript SDK` (github.com).
- [Anthropic Docs](https://docs.anthropic.com/)
  Why it matters: authoritative reference on `Anthropic Docs` (docs.anthropic.com).

Suggested trace strategy:
- search upstream code for `messages` and `content` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with the Anthropic API](01-getting-started.md)
- [Next Chapter: Chapter 3: Tool Use](03-tool-use.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
