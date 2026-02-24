---
layout: default
title: "vLLM Tutorial - Chapter 3: Basic Inference"
nav_order: 3
has_children: false
parent: vLLM Tutorial
---

# Chapter 3: Basic Inference - Text Generation and Sampling

Welcome to **Chapter 3: Basic Inference - Text Generation and Sampling**. In this part of **vLLM Tutorial: High-Performance LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master text generation with vLLM, including sampling strategies, parameter tuning, and controlling generation behavior.

## Overview

This chapter covers the core inference capabilities of vLLM - generating text with various sampling strategies, controlling output quality and diversity, and optimizing generation parameters for different use cases.

## Text Generation Basics

### Simple Text Generation

```python
from vllm import LLM, SamplingParams

# Initialize vLLM with a conversational model
llm = LLM(model="microsoft/DialoGPT-medium")

# Basic text generation
prompt = "Hello, how are you today?"
sampling_params = SamplingParams(max_tokens=50)

result = llm.generate([prompt], sampling_params)[0]

print("Prompt:", prompt)
print("Generated:", result.outputs[0].text)
print("Full response:", prompt + result.outputs[0].text)
```

### Batch Text Generation

```python
# Generate responses for multiple prompts
prompts = [
    "What is the capital of France?",
    "Explain photosynthesis in simple terms",
    "Write a haiku about artificial intelligence",
    "What are the benefits of regular exercise?",
    "Describe how rainbows form"
]

# Single batch call for efficiency
results = llm.generate(prompts, SamplingParams(max_tokens=100))

# Process results
for i, result in enumerate(results):
    print(f"\n--- Prompt {i+1} ---")
    print(f"Question: {prompts[i]}")
    print(f"Answer: {result.outputs[0].text.strip()}")
    print(f"Tokens generated: {len(result.outputs[0].token_ids)}")
```

### Controlling Generation Length

```python
# Different length controls
length_examples = {
    "short": SamplingParams(max_tokens=20, min_tokens=5),
    "medium": SamplingParams(max_tokens=100, min_tokens=30),
    "long": SamplingParams(max_tokens=200, min_tokens=50),
    "unlimited": SamplingParams(max_tokens=500)  # No minimum
}

test_prompt = "Explain the theory of relativity"

for length_name, params in length_examples.items():
    print(f"\n=== {length_name.upper()} RESPONSE ===")

    result = llm.generate([test_prompt], params)[0]
    response = result.outputs[0].text

    print(f"Length: {len(response)} characters")
    print(f"Tokens: {len(result.outputs[0].token_ids)}")
    print(f"Response: {response[:150]}{'...' if len(response) > 150 else ''}")
```

## Sampling Strategies

### Temperature Control

```python
# Temperature affects randomness/creativity
temperatures = [0.0, 0.3, 0.7, 1.0, 1.5]

prompt = "Write a creative story about a robot learning to paint"

print("Temperature Comparison:")
print("=" * 50)

for temp in temperatures:
    params = SamplingParams(
        temperature=temp,
        max_tokens=100,
        top_p=0.9
    )

    result = llm.generate([prompt], params)[0]
    response = result.outputs[0].text.strip()

    print(f"\nTemperature {temp}:")
    print(f"  {response[:120]}{'...' if len(response) > 120 else ''}")
```

### Top-K and Top-P Sampling

```python
# Compare Top-K and Top-P sampling
sampling_methods = {
    "Greedy": SamplingParams(temperature=0.0, top_k=1),
    "Top-K (10)": SamplingParams(temperature=0.7, top_k=10),
    "Top-K (50)": SamplingParams(temperature=0.7, top_k=50),
    "Top-P (0.5)": SamplingParams(temperature=0.7, top_p=0.5),
    "Top-P (0.9)": SamplingParams(temperature=0.7, top_p=0.9),
    "Top-P (0.99)": SamplingParams(temperature=0.7, top_p=0.99)
}

test_prompt = "The future of technology will"

for method_name, params in sampling_methods.items():
    print(f"\n=== {method_name} ===")

    # Generate multiple samples for comparison
    results = llm.generate([test_prompt] * 3, params)

    for i, result in enumerate(results):
        response = result.outputs[0].text.strip()
        print(f"  Sample {i+1}: {response[:80]}{'...' if len(response) > 80 else ''}")
```

### Nucleus Sampling (Top-P) Deep Dive

```python
# Understanding Top-P (nucleus sampling)
top_p_values = [0.1, 0.5, 0.7, 0.9, 0.99]

explanation_prompt = "Quantum computing is"

print("Top-P (Nucleus Sampling) Examples:")
print("Lower values = more focused, higher values = more diverse")
print("=" * 60)

for p in top_p_values:
    params = SamplingParams(
        temperature=0.8,
        top_p=p,
        max_tokens=80
    )

    results = llm.generate([explanation_prompt] * 2, params)

    print(f"\nTop-P = {p}:")
    for i, result in enumerate(results):
        response = result.outputs[0].text.strip()
        print(f"  {i+1}: {response[:100]}{'...' if len(response) > 100 else ''}")
```

## Stop Sequences and Response Control

### Basic Stop Sequences

```python
# Control when generation stops
stop_examples = {
    "sentence_end": SamplingParams(
        max_tokens=100,
        stop=[".", "!", "?"]
    ),
    "paragraph_end": SamplingParams(
        max_tokens=200,
        stop=["\n\n", "\n\n\n"]
    ),
    "code_block": SamplingParams(
        max_tokens=150,
        stop=["```"]
    ),
    "custom_marker": SamplingParams(
        max_tokens=100,
        stop=["END_RESPONSE", "FINISHED"]
    )
}

prompts = [
    "Tell me a joke",
    "Write a short paragraph about climate change",
    "Write a Python function to calculate factorial",
    "Explain recursion"
]

for i, (stop_type, params) in enumerate(stop_examples.items()):
    print(f"\n=== {stop_type.upper()} STOP ===")

    result = llm.generate([prompts[i]], params)[0]
    response = result.outputs[0].text

    print(f"Prompt: {prompts[i]}")
    print(f"Response: {response}")
    print(f"Stopped at: '{response[-20:]}'")
```

### Advanced Stop Sequence Patterns

```python
# Multiple stop sequences with priorities
advanced_stop = SamplingParams(
    max_tokens=200,
    stop=[
        "END_OF_RESPONSE",  # Custom marker
        "\n## ",            # Section break
        "\n### ",           # Subsection break
        "\n\n",             # Paragraph break
        "References:",      # Bibliography section
    ]
)

research_prompt = """Explain the impact of artificial intelligence on healthcare.
Include benefits, challenges, and future prospects.
END_OF_RESPONSE"""

result = llm.generate([research_prompt], advanced_stop)[0]
response = result.outputs[0].text

print("Advanced Stop Sequence Response:")
print("=" * 40)
print(response)

# Check which stop sequence was triggered
if response.endswith("END_OF_RESPONSE"):
    print("Stopped at: Custom marker")
elif response.endswith("\n## "):
    print("Stopped at: Section break")
else:
    print("Stopped at: Other condition")
```

## Repetition Control

### Repetition Penalty

```python
# Control repetitive text generation
repetition_examples = {
    "no_penalty": SamplingParams(
        max_tokens=100,
        temperature=0.8,
        repetition_penalty=1.0  # No penalty
    ),
    "light_penalty": SamplingParams(
        max_tokens=100,
        temperature=0.8,
        repetition_penalty=1.1  # Light penalty
    ),
    "strong_penalty": SamplingParams(
        max_tokens=100,
        temperature=0.8,
        repetition_penalty=1.3  # Strong penalty
    )
}

repetitive_prompt = "The cat sat on the mat. The cat was"

for penalty_name, params in repetition_examples.items():
    print(f"\n=== {penalty_name.upper()} ===")

    results = llm.generate([repetitive_prompt] * 2, params)

    for i, result in enumerate(results):
        response = result.outputs[0].text
        print(f"  Sample {i+1}: {repetitive_prompt}{response[:80]}...")
```

### Frequency and Presence Penalties

```python
# OpenAI-style penalties
penalty_configs = {
    "neutral": SamplingParams(
        max_tokens=80,
        temperature=0.8,
        repetition_penalty=1.0
    ),
    "reduce_repetition": SamplingParams(
        max_tokens=80,
        temperature=0.8,
        repetition_penalty=1.2
    ),
    "encourage_diversity": SamplingParams(
        max_tokens=80,
        temperature=0.9,
        repetition_penalty=0.8  # Encourage repetition for cohesion
    )
}

story_prompt = "Once upon a time in a magical forest"

for config_name, params in penalty_configs.items():
    print(f"\n=== {config_name.upper()} ===")

    result = llm.generate([story_prompt], params)[0]
    response = result.outputs[0].text

    print(f"Story: {story_prompt}{response}")

    # Analyze repetition
    words = response.lower().split()
    unique_words = set(words)
    repetition_ratio = len(words) / len(unique_words) if unique_words else 0

    print(".2f")
```

## Log Probability Analysis

### Understanding Model Confidence

```python
# Analyze token probabilities
confidence_prompt = "The capital of France is"
confidence_params = SamplingParams(
    max_tokens=10,
    temperature=0.1,  # Low temperature for confidence
    logprobs=5        # Return top 5 probabilities per token
)

result = llm.generate([confidence_prompt], confidence_params)[0]

print("Token Probability Analysis:")
print("=" * 40)
print(f"Prompt: {confidence_prompt}")

response = result.outputs[0]
for i, (token_id, token_text, logprob_data) in enumerate(zip(
    response.token_ids,
    response.outputs[0].text.split(),  # Approximate tokenization
    response.outputs[0].logprobs
)):
    # Convert log probability to probability
    probability = math.exp(logprob_data.most_likely_logprob) if logprob_data else 0

    print(f"Token {i}: '{token_text}' (prob: {probability:.3f})")

    # Show alternative high-probability tokens
    if logprob_data and hasattr(logprob_data, 'top_logprobs'):
        print("  Alternatives:")
        for token_id_alt, logprob_alt in list(logprob_data.top_logprobs.items())[:3]:
            prob_alt = math.exp(logprob_alt)
            print(".3f")

# Overall response confidence
total_logprob = sum(math.exp(lp.most_likely_logprob) for lp in response.outputs[0].logprobs if lp)
avg_confidence = total_logprob / len(response.outputs[0].logprobs) if response.outputs[0].logprobs else 0

print(".3f")
```

### Confidence-Based Response Filtering

```python
def generate_with_confidence_filter(prompt, min_confidence=0.7, max_attempts=3):
    """Generate response only if model is confident enough"""

    for attempt in range(max_attempts):
        params = SamplingParams(
            max_tokens=50,
            temperature=0.7,
            logprobs=1  # Get log probabilities
        )

        result = llm.generate([prompt], params)[0]
        response = result.outputs[0]

        # Calculate average confidence
        if response.logprobs:
            confidences = [math.exp(lp.most_likely_logprob) for lp in response.logprobs if lp]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        else:
            avg_confidence = 0.5  # Default if no logprobs

        print(f"Attempt {attempt + 1}: Confidence = {avg_confidence:.3f}")

        if avg_confidence >= min_confidence:
            return {
                "response": response.text,
                "confidence": avg_confidence,
                "attempts": attempt + 1
            }

        # Try with lower temperature for higher confidence
        params.temperature = max(0.1, params.temperature - 0.2)

    # Return best attempt if confidence threshold not met
    return {
        "response": response.text,
        "confidence": avg_confidence,
        "attempts": max_attempts,
        "warning": "Confidence threshold not met"
    }

# Test confidence filtering
test_prompts = [
    "What is 2+2?",  # Should be high confidence
    "What is the meaning of life?",  # Should be lower confidence
]

for prompt in test_prompts:
    result = generate_with_confidence_filter(prompt, min_confidence=0.8)
    print(f"\nPrompt: {prompt}")
    print(f"Response: {result['response'][:100]}...")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Attempts: {result['attempts']}")
    if 'warning' in result:
        print(f"Warning: {result['warning']}")
```

## Custom Generation Patterns

### Structured Output Generation

```python
# Generate structured data
structured_prompt = """Generate a JSON object for a person with the following structure:
{
  "name": "string",
  "age": "number",
  "occupation": "string",
  "skills": ["array", "of", "strings"],
  "contact": {
    "email": "string",
    "phone": "string"
  }
}

Person details: John Doe, 30 years old, Software Engineer, skills in Python, JavaScript, React, email john@example.com, phone 555-0123"""

structured_params = SamplingParams(
    max_tokens=200,
    temperature=0.1,  # Low temperature for structured output
    stop=["}"]         # Stop at closing brace
)

result = llm.generate([structured_prompt], structured_params)[0]
response = result.outputs[0].text

print("Structured JSON Generation:")
print(response)

# Attempt to parse as JSON
try:
    import json
    # Extract JSON from response
    json_start = response.find('{')
    json_end = response.rfind('}') + 1
    json_str = response[json_start:json_end]

    parsed = json.loads(json_str)
    print("✅ Valid JSON generated")
    print(f"Name: {parsed.get('name')}")
    print(f"Skills: {parsed.get('skills')}")

except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}")
```

### Multi-Turn Conversations

```python
# Maintain conversation context
class ConversationManager:
    def __init__(self, llm):
        self.llm = llm
        self.conversation_history = []

    def add_message(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append(f"{role}: {content}")

    def generate_response(self, user_message, max_context_turns=5):
        """Generate response with conversation context"""

        # Add user message
        self.add_message("User", user_message)

        # Create prompt with recent context
        recent_messages = self.conversation_history[-max_context_turns:]
        context = "\n".join(recent_messages)
        prompt = f"{context}\nAssistant:"

        # Generate response
        params = SamplingParams(
            max_tokens=100,
            temperature=0.7,
            stop=["\nUser:", "\nAssistant:"]  # Stop at conversation boundaries
        )

        result = self.llm.generate([prompt], params)[0]
        response = result.outputs[0].text.strip()

        # Add assistant response
        self.add_message("Assistant", response)

        return response

# Test conversation
conv_manager = ConversationManager(llm)

messages = [
    "Hello, I'm interested in learning about machine learning",
    "Can you explain what supervised learning is?",
    "What's the difference between classification and regression?",
    "Can you give me an example of a classification problem?"
]

for message in messages:
    response = conv_manager.generate_response(message)
    print(f"User: {message}")
    print(f"Assistant: {response}")
    print("-" * 50)
```

## Performance Optimization

### Batch Size Optimization

```python
# Test different batch sizes for performance
batch_sizes = [1, 2, 4, 8, 16]

test_prompts = ["What is AI?"] * 16  # Enough for largest batch

print("Batch Size Performance Test:")
print("=" * 40)

for batch_size in batch_sizes:
    # Take subset for this batch size
    batch = test_prompts[:batch_size]

    import time
    start_time = time.time()

    results = llm.generate(batch, SamplingParams(max_tokens=20))

    end_time = time.time()

    total_time = end_time - start_time
    throughput = len(batch) / total_time

    print(f"Batch size {batch_size}: {total_time:.3f}s, Throughput: {throughput:.2f} req/s")
```

### Memory-Efficient Generation

```python
# Generate long text efficiently
def generate_long_text(prompt, target_length=1000, chunk_size=200):
    """Generate long text in chunks to manage memory"""

    full_response = ""
    current_prompt = prompt

    while len(full_response) < target_length:
        params = SamplingParams(
            max_tokens=min(chunk_size, target_length - len(full_response)),
            temperature=0.8
        )

        result = llm.generate([current_prompt], params)[0]
        chunk = result.outputs[0].text

        full_response += chunk

        # Update prompt for continuation
        current_prompt = full_response[-200:]  # Use last 200 chars as context

        if len(chunk) < chunk_size * 0.5:  # Generation is slowing down
            break

    return full_response

# Test long text generation
long_prompt = "Write a comprehensive guide about climate change:"
long_text = generate_long_text(long_prompt, target_length=800)

print(f"Generated {len(long_text)} characters")
print("Preview:")
print(long_text[:500] + "...")
```

## Summary

In this chapter, we've covered:

- **Basic Text Generation** - Simple and batch text generation with vLLM
- **Sampling Strategies** - Temperature, Top-K, Top-P, and nucleus sampling
- **Response Control** - Stop sequences, length limits, and repetition control
- **Confidence Analysis** - Log probabilities and confidence-based filtering
- **Structured Generation** - JSON output and conversation management
- **Performance Optimization** - Batch processing and memory-efficient generation

These techniques provide fine-grained control over vLLM's generation behavior and enable high-quality, controlled text generation.

## Key Takeaways

1. **Sampling Control**: Temperature, Top-K, and Top-P provide different creativity levels
2. **Response Shaping**: Stop sequences and length limits control output structure
3. **Quality Assurance**: Log probabilities help assess generation confidence
4. **Structured Output**: Generate JSON, code, and other structured formats
5. **Performance Tuning**: Batch processing and memory management for efficiency

Next, we'll explore **advanced features** - streaming, tool calling, and multi-modal models.

---

**Ready for the next chapter?** [Chapter 4: Advanced Features](04-advanced-features.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `print`, `SamplingParams`, `result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Basic Inference - Text Generation and Sampling` as an operating subsystem inside **vLLM Tutorial: High-Performance LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `max_tokens`, `outputs` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Basic Inference - Text Generation and Sampling` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `print`.
2. **Input normalization**: shape incoming data so `SamplingParams` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/vllm-project/vllm)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `print` and `SamplingParams` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Model Loading and Management](02-model-loading.md)
- [Next Chapter: Chapter 4: Advanced Features - Streaming, Tool Calling, and Multi-Modal](04-advanced-features.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
