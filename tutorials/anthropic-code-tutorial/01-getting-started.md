---
layout: default
title: "Chapter 1: Getting Started with the Anthropic API"
parent: "Anthropic API Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with the Anthropic API

Welcome to **Chapter 1: Getting Started with the Anthropic API**. In this part of **Anthropic API Tutorial: Build Production Apps with Claude**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Set up your development environment, authenticate with Anthropic, and make your first API call to Claude.

## Overview

This chapter guides you through setting up the Anthropic API and SDKs, obtaining authentication credentials, and making your first successful API call. By the end, you'll have a working development environment ready for building AI applications with Claude.

## Getting Your API Key

### Create an Anthropic Account

```bash
# Step 1: Visit the Anthropic Console
# Navigate to: https://console.anthropic.com/

# Step 2: Sign up or log in
# - Use email/password or OAuth providers
# - Verify your email address

# Step 3: Navigate to API Keys
# Console > Settings > API Keys

# Step 4: Create a new API key
# - Click "Create Key"
# - Give it a descriptive name (e.g., "development-key")
# - Copy the key immediately (shown only once!)
```

### API Key Security

```bash
# NEVER commit API keys to version control
# Add to .gitignore
echo "*.env" >> .gitignore
echo ".env.local" >> .gitignore

# Store in environment variable
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Or use a .env file
echo 'ANTHROPIC_API_KEY=sk-ant-api03-...' > .env

# Verify it's set
echo $ANTHROPIC_API_KEY | head -c 20  # Shows first 20 chars only
```

## Installing the SDKs

### Python SDK

```bash
# Install the official Python SDK
pip install anthropic

# Or with specific version
pip install anthropic==0.40.0

# Install with optional dependencies
pip install anthropic[bedrock]  # For AWS Bedrock
pip install anthropic[vertex]   # For Google Vertex AI

# Verify installation
python -c "import anthropic; print(anthropic.__version__)"
```

### TypeScript/Node.js SDK

```bash
# Using npm
npm install @anthropic-ai/sdk

# Using yarn
yarn add @anthropic-ai/sdk

# Using pnpm
pnpm add @anthropic-ai/sdk

# Verify installation
node -e "const Anthropic = require('@anthropic-ai/sdk'); console.log('SDK loaded')"
```

### Other Languages

```bash
# Go (community SDK)
go get github.com/anthropics/anthropic-sdk-go

# Rust (community SDK)
cargo add anthropic

# Java/Kotlin (community SDK)
# Add to build.gradle:
# implementation 'com.anthropic:anthropic-java:1.0.0'

# Direct HTTP (any language)
# The API is REST-based - use any HTTP client
```

## Your First API Call

### Python Example

```python
import anthropic

# Create client (uses ANTHROPIC_API_KEY env var automatically)
client = anthropic.Anthropic()

# Make your first API call
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello! What can you help me with today?"
        }
    ]
)

# Print the response
print(message.content[0].text)

# Inspect the full response
print(f"Model: {message.model}")
print(f"Stop reason: {message.stop_reason}")
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
```

### TypeScript Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

// Create client
const client = new Anthropic();

async function main() {
    const message = await client.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        messages: [
            {
                role: "user",
                content: "Hello! What can you help me with today?"
            }
        ]
    });

    // Print the response
    if (message.content[0].type === 'text') {
        console.log(message.content[0].text);
    }

    // Inspect usage
    console.log(`Input tokens: ${message.usage.input_tokens}`);
    console.log(`Output tokens: ${message.usage.output_tokens}`);
}

main();
```

### cURL Example

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "Hello! What can you help me with today?"
      }
    ]
  }'
```

## Understanding the Response

### Response Structure

```python
# The message response contains:
{
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "Hello! I'm Claude, an AI assistant..."
        }
    ],
    "model": "claude-sonnet-4-20250514",
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {
        "input_tokens": 12,
        "output_tokens": 87
    }
}
```

### Parsing Responses

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku about Python"}]
)

# Access the text response
response_text = message.content[0].text
print(response_text)

# Check stop reason
if message.stop_reason == "end_turn":
    print("Claude finished naturally")
elif message.stop_reason == "max_tokens":
    print("Hit token limit - response may be truncated")
elif message.stop_reason == "stop_sequence":
    print(f"Stopped at: {message.stop_sequence}")

# Calculate costs (approximate)
input_cost = message.usage.input_tokens * 0.003 / 1000  # $3/MTok for Sonnet
output_cost = message.usage.output_tokens * 0.015 / 1000  # $15/MTok for Sonnet
print(f"Estimated cost: ${input_cost + output_cost:.6f}")
```

## Configuration Options

### Client Configuration

```python
import anthropic

# Basic client with API key from environment
client = anthropic.Anthropic()

# Explicit API key
client = anthropic.Anthropic(api_key="sk-ant-api03-...")

# Custom base URL (for proxies or enterprise)
client = anthropic.Anthropic(
    api_key="sk-ant-api03-...",
    base_url="https://api.anthropic.proxy.example.com"
)

# Custom timeout settings
client = anthropic.Anthropic(
    timeout=60.0,  # 60 seconds
    max_retries=3  # Retry failed requests
)

# Custom HTTP client (advanced)
import httpx
custom_client = httpx.Client(
    limits=httpx.Limits(max_connections=100)
)
client = anthropic.Anthropic(http_client=custom_client)
```

### Request Options

```python
# Full request with all options
message = client.messages.create(
    # Required parameters
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],

    # Optional parameters
    system="You are a helpful coding assistant.",
    temperature=0.7,           # 0.0-1.0, controls randomness
    top_p=0.9,                 # Nucleus sampling parameter
    top_k=50,                  # Top-k sampling parameter
    stop_sequences=["END"],    # Stop generation at these strings
    metadata={"user_id": "123"},  # Track requests

    # Streaming (covered in Chapter 5)
    # stream=True
)
```

## Model Selection

### Available Models

```python
# Claude Opus 4.5 - Most capable, complex reasoning
model = "claude-opus-4-20250514"
# Best for: Complex analysis, creative writing, research

# Claude Sonnet 4 - Balanced performance
model = "claude-sonnet-4-20250514"
# Best for: General tasks, coding, conversation

# Claude Haiku 3.5 - Fast and cost-effective
model = "claude-3-5-haiku-20241022"
# Best for: Quick responses, high volume, simple tasks
```

### Choosing the Right Model

```python
def choose_model(task_type: str, priority: str) -> str:
    """Select the appropriate Claude model based on task and priority."""

    if priority == "quality":
        return "claude-opus-4-20250514"

    if priority == "speed":
        return "claude-3-5-haiku-20241022"

    # Balanced selection based on task
    complex_tasks = ["analysis", "research", "creative_writing", "complex_coding"]
    simple_tasks = ["summarization", "classification", "simple_qa"]

    if task_type in complex_tasks:
        return "claude-opus-4-20250514"
    elif task_type in simple_tasks:
        return "claude-3-5-haiku-20241022"
    else:
        return "claude-sonnet-4-20250514"  # Default balanced choice

# Usage
model = choose_model("coding", "balanced")
```

## Error Handling

### Common Errors

```python
import anthropic
from anthropic import APIError, AuthenticationError, RateLimitError

client = anthropic.Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print("Check your API key is valid and has credits")

except RateLimitError as e:
    print(f"Rate limited: {e}")
    print("Wait and retry, or reduce request frequency")

except anthropic.BadRequestError as e:
    print(f"Invalid request: {e}")
    print("Check your request parameters")

except anthropic.APIConnectionError as e:
    print(f"Connection failed: {e}")
    print("Check your network connection")

except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
```

### Retry Logic

```python
import time
import anthropic
from anthropic import RateLimitError, APIConnectionError

def call_with_retry(client, max_retries=3, **kwargs):
    """Make API call with exponential backoff retry."""

    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)

        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 1, 2, 4 seconds
            print(f"Rate limited. Waiting {wait_time}s before retry...")
            time.sleep(wait_time)

        except APIConnectionError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Connection failed. Waiting {wait_time}s before retry...")
            time.sleep(wait_time)

    raise Exception("Max retries exceeded")

# Usage
client = anthropic.Anthropic()
message = call_with_retry(
    client,
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Environment Setup

### Development Environment

```bash
# Create a project directory
mkdir my-claude-app
cd my-claude-app

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic python-dotenv

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
EOF

# Create .gitignore
cat > .gitignore << EOF
.env
venv/
__pycache__/
*.pyc
EOF
```

### Loading Environment Variables

```python
# Using python-dotenv
from dotenv import load_dotenv
import os
import anthropic

# Load .env file
load_dotenv()

# API key is automatically read from environment
client = anthropic.Anthropic()

# Or explicitly
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)
```

## Testing Your Setup

### Verification Script

```python
#!/usr/bin/env python3
"""Verify Anthropic API setup is working correctly."""

import anthropic
import sys

def test_api_connection():
    """Test basic API connectivity."""
    print("Testing Anthropic API connection...")

    try:
        client = anthropic.Anthropic()

        # Simple test message
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",  # Use Haiku for quick test
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API working!' and nothing else."}]
        )

        response = message.content[0].text
        print(f"Response: {response}")

        # Check usage
        print(f"Input tokens: {message.usage.input_tokens}")
        print(f"Output tokens: {message.usage.output_tokens}")

        print("API connection successful!")
        return True

    except anthropic.AuthenticationError:
        print("ERROR: Authentication failed. Check your API key.")
        return False

    except anthropic.APIConnectionError:
        print("ERROR: Could not connect to API. Check your network.")
        return False

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return False

def test_models():
    """Test access to different models."""
    print("\nTesting model access...")

    client = anthropic.Anthropic()
    models = [
        "claude-3-5-haiku-20241022",
        "claude-sonnet-4-20250514",
        # "claude-opus-4-20250514",  # Uncomment if you have access
    ]

    for model in models:
        try:
            message = client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"  {model}: OK")
        except Exception as e:
            print(f"  {model}: FAILED - {e}")

if __name__ == "__main__":
    if test_api_connection():
        test_models()
        print("\nSetup complete! You're ready to build with Claude.")
        sys.exit(0)
    else:
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)
```

## Best Practices

### API Key Management

```python
# DO: Use environment variables
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")

# DO: Use secrets management in production
# AWS Secrets Manager, HashiCorp Vault, etc.

# DON'T: Hardcode API keys
# api_key = "sk-ant-api03-..."  # NEVER DO THIS

# DON'T: Commit .env files
# Add .env to .gitignore
```

### Request Optimization

```python
# Set appropriate max_tokens
# Don't set higher than needed - you pay for output tokens
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,  # Only what you need
    messages=[{"role": "user", "content": "Give me a one-sentence summary."}]
)

# Use system prompts for consistent behavior
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a concise assistant. Keep responses brief.",
    messages=[{"role": "user", "content": "Explain quantum computing."}]
)
```

### Cost Awareness

```python
def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost for a request."""

    # Pricing as of 2024 (check console for current)
    pricing = {
        "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
        "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
        "claude-3-5-haiku-20241022": {"input": 0.25, "output": 1.25},
    }

    rates = pricing.get(model, pricing["claude-sonnet-4-20250514"])
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]

    return input_cost + output_cost

# After a request
message = client.messages.create(...)
cost = estimate_cost(
    message.model,
    message.usage.input_tokens,
    message.usage.output_tokens
)
print(f"Request cost: ${cost:.6f}")
```

## Summary

In this chapter, you've learned:

- **API Key Setup**: Obtaining and securing your Anthropic API key
- **SDK Installation**: Installing Python and TypeScript SDKs
- **First API Call**: Making successful requests to Claude
- **Response Handling**: Parsing and understanding API responses
- **Model Selection**: Choosing the right Claude model for your task
- **Error Handling**: Managing common errors and implementing retries
- **Environment Setup**: Configuring development environments
- **Best Practices**: Security, optimization, and cost management

## Key Takeaways

1. **Secure Your Keys**: Never commit API keys to version control
2. **Choose Wisely**: Select models based on task complexity and cost
3. **Handle Errors**: Implement proper error handling and retries
4. **Monitor Costs**: Track token usage to manage expenses
5. **Test Thoroughly**: Verify your setup before building applications

## Next Steps

Now that you have a working API setup, let's dive deep into the Messages API in the next chapter, where you'll learn about multi-turn conversations, system prompts, and message handling patterns.

---

**Ready for Chapter 2?** [Messages API](02-messages-api.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `anthropic`, `print`, `message` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with the Anthropic API` as an operating subsystem inside **Anthropic API Tutorial: Build Production Apps with Claude**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `client`, `claude`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with the Anthropic API` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `anthropic`.
2. **Input normalization**: shape incoming data so `print` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `message`.
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
- search upstream code for `anthropic` and `print` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Messages API](02-messages-api.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
