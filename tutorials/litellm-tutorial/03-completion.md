---
layout: default
title: "LiteLLM Tutorial - Chapter 3: Completion API"
nav_order: 3
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 3: Completion API

Welcome to **Chapter 3: Completion API**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- tutorial slug: **litellm-tutorial**
- chapter focus: **Chapter 3: Completion API**
- system context: **Litellm Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 3: Completion API`.
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

1. Build a minimal end-to-end implementation for `Chapter 3: Completion API`.
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

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `messages`, `content`, `response` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Completion API` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `self`, `role`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Completion API` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `messages`.
2. **Input normalization**: shape incoming data so `content` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `response`.
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
- search upstream code for `messages` and `content` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Provider Configuration](02-providers.md)
- [Next Chapter: Chapter 4: Streaming & Async](04-streaming.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
