---
layout: default
title: "LocalAI Tutorial - Chapter 3: Text Generation"
nav_order: 3
has_children: false
parent: LocalAI Tutorial
---

# Chapter 3: Text Generation and Chat Completions

Welcome to **Chapter 3: Text Generation and Chat Completions**. In this part of **LocalAI Tutorial: Self-Hosted OpenAI Alternative**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master text generation with LocalAI using OpenAI-compatible APIs, chat formats, and advanced parameters.

## Overview

LocalAI provides complete OpenAI API compatibility for text generation. This chapter covers chat completions, parameter tuning, and conversation management.

## Chat Completions API

### Basic Chat Completion

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

response = client.chat.completions.create(
    model="phi-2",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
```

### Response Structure

```python
{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "phi-2",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "The capital of France is Paris."
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 25,
        "completion_tokens": 7,
        "total_tokens": 32
    }
}
```

## Advanced Parameters

### Generation Control

```python
response = client.chat.completions.create(
    model="phi-2",
    messages=[{"role": "user", "content": "Write a creative story"}],
    max_tokens=500,          # Maximum response length
    temperature=0.8,         # Randomness (0.0-2.0)
    top_p=0.9,              # Nucleus sampling (0.0-1.0)
    top_k=40,               # Top-k sampling
    frequency_penalty=0.0,   # Reduce repetition (-2.0 to 2.0)
    presence_penalty=0.0,    # Encourage diversity (-2.0 to 2.0)
    repeat_penalty=1.1,      # Repetition penalty
    seed=42                  # For reproducible results
)
```

### Parameter Guide

| Parameter | Purpose | Recommended Values |
|-----------|---------|-------------------|
| `temperature` | Controls randomness | 0.1-0.3 (factual), 0.7-1.0 (creative) |
| `top_p` | Nucleus sampling | 0.1-0.5 (focused), 0.9-1.0 (diverse) |
| `top_k` | Top-k sampling | 10-50 (most use cases) |
| `max_tokens` | Response length limit | 100-2000 depending on use case |
| `frequency_penalty` | Reduce repetition | 0.0-0.5 (slight reduction) |
| `presence_penalty` | Encourage new topics | 0.0-0.3 (moderate encouragement) |

## Chat Formats and Templates

### Supported Chat Templates

LocalAI automatically detects and applies chat templates:

```python
# Llama 2 chat format (automatically applied)
response = client.chat.completions.create(
    model="llama-2-7b-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

# Mistral chat format
response = client.chat.completions.create(
    model="mistral-7b-instruct",
    messages=[
        {"role": "user", "content": "Explain recursion"}
    ]
)
```

### Custom Chat Templates

```yaml
# model-config.yaml
name: custom-model
backend: llama
parameters:
  model: model.gguf

# Custom chat template
chat_template: |
  {% for message in messages %}
  {% if message.role == "system" %}{{ message.content }}{% endif %}
  {% if message.role == "user" %}[INST] {{ message.content }} [/INST]{% endif %}
  {% if message.role == "assistant" %}{{ message.content }}{% endif %}
  {% endfor %}
```

## Streaming Responses

### Basic Streaming

```python
response = client.chat.completions.create(
    model="phi-2",
    messages=[{"role": "user", "content": "Tell me a long story"}],
    stream=True,
    max_tokens=1000
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # New line
```

### Streaming with Event Handling

```python
def stream_with_events():
    response = client.chat.completions.create(
        model="phi-2",
        messages=[{"role": "user", "content": "Explain machine learning"}],
        stream=True
    )

    full_response = ""
    for chunk in response:
        delta = chunk.choices[0].delta

        # Handle different content types
        if delta.content:
            content = delta.content
            print(content, end="", flush=True)
            full_response += content

        # Check for completion
        if chunk.choices[0].finish_reason:
            print(f"\n\nFinished: {chunk.choices[0].finish_reason}")

    return full_response

# Usage
result = stream_with_events()
```

## Conversation Management

### Multi-Turn Conversations

```python
class ConversationManager:
    def __init__(self, model="phi-2"):
        self.model = model
        self.messages = []

    def add_message(self, role, content):
        """Add a message to the conversation."""
        self.messages.append({"role": role, "content": content})

    def send_message(self, user_message):
        """Send user message and get AI response."""
        self.add_message("user", user_message)

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=500
        )

        ai_response = response.choices[0].message.content
        self.add_message("assistant", ai_response)

        return ai_response

    def get_history(self):
        """Get conversation history."""
        return self.messages.copy()

# Usage
chat = ConversationManager()

print("AI:", chat.send_message("Hello! My name is Alice."))
print("AI:", chat.send_message("What's my name?"))
print("AI:", chat.send_message("Can you remind me what we talked about?"))
```

### System Messages and Personas

```python
def create_persona_chat(persona_description, model="phi-2"):
    """Create a chat session with a specific persona."""

    chat_manager = ConversationManager(model)

    # Add system message
    chat_manager.add_message("system", persona_description)

    def chat(user_input):
        return chat_manager.send_message(user_input)

    return chat

# Create different personas
coding_assistant = create_persona_chat(
    "You are an expert Python programmer. Provide clear, well-commented code examples."
)

creative_writer = create_persona_chat(
    "You are a creative writing assistant. Help users develop stories and characters."
)

# Use personas
print("Coding Assistant:", coding_assistant("Write a function to reverse a string"))
print("Creative Writer:", creative_writer("Help me name a character for a sci-fi story"))
```

## Advanced Text Generation

### Structured Output

```python
def generate_structured_response(schema_description, user_query):
    """Generate responses that follow a specific structure."""

    system_prompt = f"""
    You must respond in a structured format. {schema_description}

    Always follow the exact format specified. Be concise but complete.
    """

    response = client.chat.completions.create(
        model="phi-2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.1  # Low temperature for consistency
    )

    return response.choices[0].message.content

# Examples
# JSON output
json_schema = "Respond with valid JSON containing 'name', 'age', and 'occupation' fields."
json_response = generate_structured_response(json_schema, "Create a profile for a software engineer")

# List format
list_schema = "Respond with a numbered list of exactly 5 items."
list_response = generate_structured_response(list_schema, "List the benefits of exercise")
```

### Few-Shot Prompting

```python
def few_shot_generation(examples, task_description, model="phi-2"):
    """Use few-shot prompting for better results."""

    system_message = "You are an AI that learns from examples. Respond in the same style as the examples."

    # Build prompt with examples
    prompt = "Here are some examples:\n\n"
    for example in examples:
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n\n"

    prompt += f"Now respond to: {task_description}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# Example usage
examples = [
    {
        "input": "The sky is blue",
        "output": "The sky appears blue due to light scattering"
    },
    {
        "input": "Plants need sunlight",
        "output": "Plants use sunlight for photosynthesis to create energy"
    }
]

result = few_shot_generation(
    examples,
    "Why do we have seasons?",
    model="phi-2"
)
```

### Chain of Thought Prompting

```python
def chain_of_thought_reasoning(problem, model="phi-2"):
    """Use chain of thought prompting for complex reasoning."""

    cot_prompt = f"""
    Solve this problem step by step. Show your reasoning clearly.

    Problem: {problem}

    Think through this systematically:
    1. Understand what is being asked
    2. Identify the key information provided
    3. Consider what approach or formula to use
    4. Perform the necessary calculations
    5. Provide the final answer

    Let's work through this step by step:
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": cot_prompt}],
        max_tokens=1000,
        temperature=0.3  # Balanced creativity and focus
    )

    return response.choices[0].message.content

# Usage
math_problem = "If a train travels at 60 mph for 2.5 hours, how far does it go?"
solution = chain_of_thought_reasoning(math_problem)

logic_problem = "All roses are flowers. Some flowers fade quickly. Can we conclude that some roses fade quickly?"
logic_solution = chain_of_thought_reasoning(logic_problem)
```

## Batch Processing

### Multiple Requests

```python
import asyncio
import aiohttp

async def async_chat_completion(session, model, messages, **kwargs):
    """Async chat completion."""
    async with session.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": model,
            "messages": messages,
            **kwargs
        }
    ) as response:
        return await response.json()

async def batch_process(prompts, model="phi-2"):
    """Process multiple prompts concurrently."""

    async with aiohttp.ClientSession() as session:
        tasks = []

        for prompt in prompts:
            messages = [{"role": "user", "content": prompt}]
            task = async_chat_completion(session, model, messages, max_tokens=200)
            tasks.append(task)

        # Wait for all to complete
        results = await asyncio.gather(*tasks)

        return [result["choices"][0]["message"]["content"] for result in results]

# Usage
prompts = [
    "Explain recursion simply",
    "What is machine learning?",
    "Write a Python hello world",
    "What are cloud services?",
    "Explain quantum computing"
]

results = await asyncio.run(batch_process(prompts))

for i, (prompt, result) in enumerate(zip(prompts, results)):
    print(f"{i+1}. {prompt}")
    print(f"   {result[:100]}...")
    print()
```

## Error Handling and Validation

### Robust API Calls

```python
import time
import requests
from typing import Optional

def robust_chat_completion(
    messages,
    model="phi-2",
    max_retries=3,
    timeout=30
):
    """Robust chat completion with error handling."""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                timeout=timeout
            )

            # Validate response
            if not response.choices:
                raise ValueError("No choices in response")

            content = response.choices[0].message.content
            if not content or not content.strip():
                raise ValueError("Empty response content")

            return response

        except client.APIError as e:
            if attempt == max_retries - 1:
                raise
            print(f"API error (attempt {attempt + 1}): {e}")
            time.sleep(2 ** attempt)  # Exponential backoff

        except client.RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Rate limited (attempt {attempt + 1}): {e}")
            time.sleep(5)  # Fixed delay for rate limits

        except Exception as e:
            print(f"Unexpected error (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

# Usage
try:
    response = robust_chat_completion([
        {"role": "user", "content": "Hello, world!"}
    ])
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print(f"Failed after retries: {e}")
```

## Performance Optimization

### Parameter Tuning

```python
# Fast generation (lower quality)
fast_response = client.chat.completions.create(
    model="phi-2",
    messages=[{"role": "user", "content": "Summarize this article"}],
    max_tokens=100,
    temperature=0.1,  # More deterministic
    top_p=0.5,        # Focused sampling
    top_k=20          # Smaller top-k
)

# Quality generation (slower)
quality_response = client.chat.completions.create(
    model="phi-2",
    messages=[{"role": "user", "content": "Write a detailed analysis"}],
    max_tokens=1000,
    temperature=0.8,  # More creative
    top_p=0.95,       # Diverse sampling
    top_k=50          # Larger top-k
)
```

### Context Management

```python
def manage_context(messages, max_context_length=4000, model_context=4096):
    """Manage conversation context to stay within limits."""

    # Reserve space for response
    available_context = model_context - 1000  # Leave room for response

    total_length = sum(len(msg["content"]) for msg in messages)

    if total_length <= available_context:
        return messages

    # Truncate older messages
    truncated_messages = []
    current_length = 0

    # Always keep system message if present
    system_msg = None
    if messages and messages[0]["role"] == "system":
        system_msg = messages[0]
        messages = messages[1:]
        truncated_messages.append(system_msg)
        current_length += len(system_msg["content"])

    # Add recent messages
    for msg in reversed(messages):
        msg_length = len(msg["content"])
        if current_length + msg_length <= available_context:
            truncated_messages.insert(-1 if system_msg else 0, msg)
            current_length += msg_length
        else:
            break

    return truncated_messages

# Usage
long_conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    # ... many messages ...
]

optimized_messages = manage_context(long_conversation)

response = client.chat.completions.create(
    model="phi-2",
    messages=optimized_messages
)
```

## Best Practices

1. **Parameter Tuning**: Start with conservative parameters and adjust based on results
2. **Context Management**: Monitor context length to avoid truncation
3. **Error Handling**: Always implement retry logic for production use
4. **Streaming**: Use streaming for better user experience with long responses
5. **Validation**: Validate response content and structure
6. **Performance**: Balance quality vs speed based on use case requirements

Next: Explore image generation capabilities with Stable Diffusion models.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `content`, `messages`, `model` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Text Generation and Chat Completions` as an operating subsystem inside **LocalAI Tutorial: Self-Hosted OpenAI Alternative**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `chat`, `role` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Text Generation and Chat Completions` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `content`.
2. **Input normalization**: shape incoming data so `messages` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/mudler/LocalAI)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `content` and `messages` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Model Gallery and Management](02-models.md)
- [Next Chapter: Chapter 4: Image Generation with Stable Diffusion](04-image-generation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
