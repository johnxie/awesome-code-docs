---
layout: default
title: "LiteLLM Tutorial - Chapter 3: Completion API"
nav_order: 3
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 3: Completion API

> Master text and chat completions with advanced parameters, formatting, and multi-turn conversations.

## Overview

The completion API is the core of LiteLLM. This chapter covers how to craft effective prompts, use advanced parameters, and handle different types of completions across all providers.

## Basic Chat Completions

The standard chat completion format:

```python
import litellm

response = litellm.completion(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]
)

print(response.choices[0].message.content)
```

## Message Roles

Understanding conversation roles:

- **system**: Sets the AI's behavior and context
- **user**: Human messages
- **assistant**: AI responses (can include previous responses for context)

```python
messages = [
    {
        "role": "system",
        "content": "You are an expert Python programmer. Provide clear, well-commented code examples."
    },
    {
        "role": "user",
        "content": "Write a function to calculate fibonacci numbers recursively."
    }
]

response = litellm.completion(model="gpt-4", messages=messages)
```

## Advanced Parameters

Control model behavior with parameters:

```python
response = litellm.completion(
    model="gpt-4",
    messages=messages,
    max_tokens=500,          # Maximum response length
    temperature=0.7,         # Randomness (0.0-1.0)
    top_p=0.9,              # Nucleus sampling
    frequency_penalty=0.0,   # Reduce repetition (-2.0 to 2.0)
    presence_penalty=0.0,    # Encourage new topics (-2.0 to 2.0)
    stop=["\n\n", "###"],    # Stop sequences
    n=1,                    # Number of completions to generate
    logit_bias={},          # Bias token probabilities
)
```

### Parameter Guide

| Parameter | Range | Description | Use Case |
|-----------|-------|-------------|----------|
| `temperature` | 0.0-2.0 | Randomness in output | Creative writing (high), Code (low) |
| `top_p` | 0.0-1.0 | Nucleus sampling | Alternative to temperature |
| `max_tokens` | 1+ | Maximum response length | Control costs and length |
| `frequency_penalty` | -2.0-2.0 | Reduce token repetition | Avoid loops in text |
| `presence_penalty` | -2.0-2.0 | Encourage new topics | Diverse responses |
| `stop` | strings | Stop generation at these strings | Structured outputs |

## Multi-Turn Conversations

Maintain context across multiple exchanges:

```python
conversation = [
    {"role": "system", "content": "You are a helpful coding tutor."},
    {"role": "user", "content": "How do I reverse a string in Python?"},
]

# First response
response1 = litellm.completion(model="gpt-4", messages=conversation)
print("Assistant:", response1.choices[0].message.content)

# Continue conversation
conversation.append({
    "role": "assistant",
    "content": response1.choices[0].message.content
})
conversation.append({
    "role": "user",
    "content": "Can you show me a more efficient way using slicing?"
})

response2 = litellm.completion(model="gpt-4", messages=conversation)
print("Assistant:", response2.choices[0].message.content)
```

## Conversation Management Class

Create a helper class for managing conversations:

```python
class ConversationManager:
    def __init__(self, model="gpt-4", system_message=None):
        self.model = model
        self.messages = []

        if system_message:
            self.messages.append({"role": "system", "content": system_message})

    def add_message(self, role, content):
        """Add a message to the conversation."""
        self.messages.append({"role": role, "content": content})

    def send_message(self, user_message, **kwargs):
        """Send a user message and get response."""
        self.add_message("user", user_message)

        response = litellm.completion(
            model=self.model,
            messages=self.messages,
            **kwargs
        )

        assistant_message = response.choices[0].message.content
        self.add_message("assistant", assistant_message)

        return assistant_message, response

    def get_history(self):
        """Get conversation history."""
        return self.messages.copy()

    def clear_history(self):
        """Clear conversation history."""
        system_msg = None
        if self.messages and self.messages[0]["role"] == "system":
            system_msg = self.messages[0]
        self.messages = [system_msg] if system_msg else []

# Usage
chat = ConversationManager(
    model="gpt-4",
    system_message="You are a knowledgeable history teacher."
)

response, _ = chat.send_message("Tell me about the Roman Empire")
print("Response:", response[:200] + "...")

response, _ = chat.send_message("What were their biggest achievements?")
print("Follow-up:", response[:200] + "...")
```

## Structured Outputs

Force specific output formats:

```python
# JSON output
json_prompt = """
Extract the following information from the text and return as JSON:
- Name
- Age
- Occupation

Text: John Smith is a 35-year-old software engineer from San Francisco.

Return only valid JSON.
"""

response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": json_prompt}],
    temperature=0.1  # Lower temperature for consistent formatting
)

import json
try:
    data = json.loads(response.choices[0].message.content)
    print("Extracted:", data)
except json.JSONDecodeError:
    print("Failed to parse JSON response")
```

## Code Generation

Specialized prompts for code:

```python
def generate_code(requirement, language="python"):
    """Generate code based on requirements."""

    prompt = f"""
Write a {language} function that {requirement}.

Requirements:
- Include docstring
- Add type hints
- Handle edge cases
- Include example usage

Return only the code, no explanation.
"""

    response = litellm.completion(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,  # Low temperature for code
        stop=["```"]      # Stop at code blocks
    )

    return response.choices[0].message.content

# Usage
code = generate_code("calculates the factorial of a number with memoization")
print(code)
```

## Few-Shot Prompting

Provide examples for better results:

```python
def analyze_sentiment(text):
    """Analyze sentiment using few-shot examples."""

    examples = """
Here are examples of sentiment analysis:

Text: "I love this product, it's amazing!"
Sentiment: positive

Text: "This is terrible, I hate it."
Sentiment: negative

Text: "It's okay, nothing special."
Sentiment: neutral

Now analyze this text:
"""

    prompt = examples + text + "\n\nSentiment:"

    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=10
    )

    return response.choices[0].message.content.strip()

# Usage
sentiment = analyze_sentiment("This movie was fantastic!")
print(f"Sentiment: {sentiment}")
```

## Chain of Thought Prompting

Encourage step-by-step reasoning:

```python
def solve_problem(problem):
    """Solve a problem with chain of thought."""

    prompt = f"""
Solve this problem step by step. Show your work clearly.

Problem: {problem}

Think through this systematically:
1. Understand the problem
2. Identify the key information
3. Consider different approaches
4. Choose the best method
5. Execute the solution
6. Verify the answer

Final Answer: [Your final answer here]
"""

    response = litellm.completion(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content

# Usage
solution = solve_problem("If a train travels at 60 mph for 2 hours, how far does it go?")
print(solution)
```

## Multiple Completions

Generate multiple responses for comparison:

```python
def generate_multiple_responses(prompt, n=3, model="gpt-4"):
    """Generate multiple completions for the same prompt."""

    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        n=n,              # Number of completions
        temperature=0.8,  # Higher temperature for variety
        max_tokens=200
    )

    return [choice.message.content for choice in response.choices]

# Usage
responses = generate_multiple_responses(
    "Write a creative slogan for a coffee shop",
    n=5,
    model="claude-3-sonnet-20240229"
)

for i, response in enumerate(responses, 1):
    print(f"{i}. {response}")
```

## Provider-Specific Features

Leverage unique provider capabilities:

```python
# Anthropic's extended thinking (if available)
response = litellm.completion(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Solve this complex math problem..."}],
    max_tokens=4000,
    thinking_budget=2000  # Anthropic-specific parameter
)

# OpenAI's function calling
function_response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    functions=[
        {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    ],
    function_call="auto"
)

# Check if function was called
if hasattr(function_response.choices[0].message, 'function_call'):
    func_call = function_response.choices[0].message.function_call
    print(f"Function: {func_call.name}")
    print(f"Arguments: {func_call.arguments}")
```

## Error Handling and Validation

Robust completion handling:

```python
def safe_completion(model, messages, **kwargs):
    """Completion with comprehensive error handling."""

    # Default parameters
    defaults = {
        "max_tokens": 1000,
        "temperature": 0.7,
        "timeout": 30
    }
    defaults.update(kwargs)

    # Validate inputs
    if not messages or not isinstance(messages, list):
        raise ValueError("Messages must be a non-empty list")

    for msg in messages:
        if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
            raise ValueError("Each message must have 'role' and 'content' fields")

    try:
        response = litellm.completion(model=model, messages=messages, **defaults)

        # Validate response
        if not response.choices:
            raise ValueError("No choices returned in response")

        content = response.choices[0].message.content
        if not content or not content.strip():
            raise ValueError("Empty response content")

        return response

    except litellm.RateLimitError:
        print("Rate limit exceeded. Waiting and retrying...")
        time.sleep(60)  # Wait 1 minute
        return safe_completion(model, messages, **kwargs)  # Retry

    except litellm.AuthenticationError:
        raise ValueError(f"Invalid API key for {model}")

    except litellm.APIError as e:
        print(f"API error: {e}")
        # Could implement fallback to different model here
        raise

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

# Usage
try:
    response = safe_completion(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
```

## Cost Estimation

Estimate costs before making calls:

```python
def estimate_completion_cost(model, messages, max_tokens=1000):
    """Estimate cost for a completion request."""

    # Rough token estimation
    total_chars = sum(len(msg["content"]) for msg in messages)
    estimated_input_tokens = total_chars // 4  # Rough approximation
    estimated_output_tokens = max_tokens

    # Cost per 1K tokens (approximate)
    costs = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
        "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    }

    if model not in costs:
        return None  # Unknown cost

    model_costs = costs[model]
    input_cost = (estimated_input_tokens / 1000) * model_costs["input"]
    output_cost = (estimated_output_tokens / 1000) * model_costs["output"]

    return {
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "estimated_cost": input_cost + output_cost,
        "currency": "USD"
    }

# Usage
cost_estimate = estimate_completion_cost(
    "gpt-4",
    [{"role": "user", "content": "Write a 500-word essay about AI"}],
    max_tokens=1000
)

if cost_estimate:
    print(f"Estimated cost: ${cost_estimate['estimated_cost']:.4f}")
    print(f"Input tokens: {cost_estimate['estimated_input_tokens']}")
    print(f"Output tokens: {cost_estimate['estimated_output_tokens']}")
```

## Best Practices

1. **Temperature Tuning**: Use lower temperatures (0.1-0.3) for factual/coding tasks, higher (0.7-0.9) for creative tasks
2. **Max Tokens**: Set appropriate limits to control costs and response length
3. **System Messages**: Use system messages to set context and behavior
4. **Conversation Context**: Maintain conversation history for multi-turn interactions
5. **Error Handling**: Always wrap API calls in try-catch blocks
6. **Cost Monitoring**: Track usage and set budgets
7. **Prompt Engineering**: Craft clear, specific prompts for better results

The completion API is your primary interface to LLM capabilities. Mastering these patterns will enable you to build sophisticated AI applications across any provider. 