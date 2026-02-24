---
layout: default
title: "Chapter 6: Advanced Patterns"
parent: "Anthropic API Tutorial"
nav_order: 6
---

# Chapter 6: Advanced Patterns

Welcome to **Chapter 6: Advanced Patterns**. In this part of **Anthropic API Tutorial: Build Production Apps with Claude**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master prompt engineering, caching, batching, and optimization techniques for building sophisticated AI applications.

## Overview

This chapter covers advanced techniques for working with Claude effectively, including prompt engineering patterns, prompt caching for cost optimization, batch processing, and strategies for improving response quality.

## Prompt Engineering

### Chain of Thought Prompting

```python
import anthropic

client = anthropic.Anthropic()

# Basic chain of thought
def chain_of_thought(question: str) -> str:
    """Use chain of thought for complex reasoning."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Solve this problem step by step.

Problem: {question}

Think through this carefully:
1. First, identify what we know
2. Then, determine what we need to find
3. Work through the logic step by step
4. Finally, state your answer clearly

Show your reasoning at each step."""
            }
        ]
    )

    return message.content[0].text

# Structured chain of thought with XML tags
def structured_cot(question: str) -> dict:
    """Structured chain of thought with parseable output."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Solve this problem with detailed reasoning.

Problem: {question}

Structure your response as:
<analysis>
What we know and what we need to find
</analysis>

<steps>
Step-by-step reasoning (number each step)
</steps>

<answer>
Your final answer
</answer>

<confidence>
How confident are you? (high/medium/low) and why
</confidence>"""
            }
        ]
    )

    # Parse the structured response
    import re
    text = message.content[0].text

    return {
        "analysis": extract_tag(text, "analysis"),
        "steps": extract_tag(text, "steps"),
        "answer": extract_tag(text, "answer"),
        "confidence": extract_tag(text, "confidence")
    }

def extract_tag(text: str, tag: str) -> str:
    """Extract content from XML-style tags."""
    import re
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""
```

### Few-Shot Learning

```python
def few_shot_classification(text: str, examples: list[dict]) -> str:
    """Classify text using few-shot examples."""

    # Build examples string
    examples_text = "\n\n".join([
        f"Text: {ex['text']}\nCategory: {ex['category']}"
        for ex in examples
    ])

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"""Classify the following text into a category based on these examples:

{examples_text}

Now classify this text:
Text: {text}
Category:"""
            }
        ]
    )

    return message.content[0].text.strip()

# Usage
examples = [
    {"text": "The product arrived damaged", "category": "complaint"},
    {"text": "How do I reset my password?", "category": "support"},
    {"text": "Great service, very satisfied!", "category": "praise"},
    {"text": "Can I get a refund?", "category": "refund_request"}
]

category = few_shot_classification(
    "I've been waiting 3 weeks for my order",
    examples
)
```

### Role-Based Prompting

```python
def expert_response(question: str, expert_role: str, expertise_areas: list[str]) -> str:
    """Get response from a specified expert perspective."""

    expertise = ", ".join(expertise_areas)

    system_prompt = f"""You are a {expert_role} with deep expertise in {expertise}.

When answering questions:
- Draw on your specialized knowledge
- Use appropriate technical terminology
- Provide practical, actionable insights
- Acknowledge limitations of your expertise
- Cite relevant frameworks, research, or best practices when applicable"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return message.content[0].text

# Usage
response = expert_response(
    "How should I structure a microservices architecture?",
    expert_role="senior software architect",
    expertise_areas=["distributed systems", "cloud architecture", "API design"]
)
```

### Output Format Control

```python
import json

def get_structured_output(prompt: str, schema: dict) -> dict:
    """Get output conforming to a JSON schema."""

    schema_str = json.dumps(schema, indent=2)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""{prompt}

Return your response as valid JSON matching this schema:
```json
{schema_str}
```

Respond with only the JSON, no other text."""
            },
            {
                "role": "assistant",
                "content": "{"  # Prefill to ensure JSON output
            }
        ]
    )

    # Parse response (prepend the prefill)
    json_str = "{" + message.content[0].text
    return json.loads(json_str)

# Usage
schema = {
    "summary": "string - brief summary",
    "key_points": ["array of main points"],
    "sentiment": "positive | negative | neutral",
    "confidence": "number between 0 and 1"
}

result = get_structured_output(
    "Analyze this customer review: 'The product is okay but shipping was slow.'",
    schema
)
```

## Prompt Caching

### Basic Prompt Caching

```python
import anthropic

client = anthropic.Anthropic()

# Large system prompt that will be cached
LARGE_SYSTEM_PROMPT = """You are an expert legal assistant...
[imagine 10,000+ tokens of legal knowledge, procedures, and guidelines]
"""

# First request - creates cache
message1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": LARGE_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}  # Enable caching
        }
    ],
    messages=[
        {"role": "user", "content": "What are the requirements for filing a patent?"}
    ]
)

# Check cache usage
print(f"Cache created: {message1.usage.cache_creation_input_tokens} tokens")
print(f"Cache read: {message1.usage.cache_read_input_tokens} tokens")

# Second request - uses cache
message2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": LARGE_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "How long does trademark registration take?"}
    ]
)

print(f"Cache read: {message2.usage.cache_read_input_tokens} tokens")  # Should show cache hit
```

### Caching Strategy

```python
class CachedAssistant:
    """Assistant with prompt caching for cost optimization."""

    def __init__(self, system_prompt: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.system_prompt = system_prompt
        self.conversation = []
        self.cache_stats = {
            "created": 0,
            "read": 0,
            "total_saved": 0
        }

    def _get_system_with_cache(self):
        """Get system prompt with cache control."""
        return [
            {
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"}
            }
        ]

    def chat(self, user_message: str) -> str:
        """Send message and track cache usage."""

        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self._get_system_with_cache(),
            messages=self.conversation
        )

        # Track cache stats
        usage = response.usage
        if hasattr(usage, 'cache_creation_input_tokens'):
            self.cache_stats["created"] += usage.cache_creation_input_tokens
        if hasattr(usage, 'cache_read_input_tokens'):
            self.cache_stats["read"] += usage.cache_read_input_tokens
            # Cache reads are 90% cheaper
            self.cache_stats["total_saved"] += usage.cache_read_input_tokens * 0.9

        assistant_message = response.content[0].text
        self.conversation.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def get_cache_stats(self) -> dict:
        """Get cache usage statistics."""
        return self.cache_stats

# Usage
assistant = CachedAssistant(LARGE_SYSTEM_PROMPT)

print(assistant.chat("First question..."))
print(assistant.chat("Second question..."))
print(assistant.chat("Third question..."))

print(f"Cache stats: {assistant.get_cache_stats()}")
```

### Multi-Turn Caching

```python
def cached_conversation_with_context(documents: list[str], questions: list[str]):
    """Cache large context documents across multiple questions."""

    client = anthropic.Anthropic()

    # Combine documents into cacheable context
    context = "\n\n---\n\n".join([
        f"Document {i+1}:\n{doc}"
        for i, doc in enumerate(documents)
    ])

    system = [
        {
            "type": "text",
            "text": f"""You are a helpful assistant with access to these documents:

{context}

Answer questions based on the documents. Cite specific documents when relevant.""",
            "cache_control": {"type": "ephemeral"}
        }
    ]

    results = []
    conversation = []

    for question in questions:
        conversation.append({"role": "user", "content": question})

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system,
            messages=conversation
        )

        answer = response.content[0].text
        conversation.append({"role": "assistant", "content": answer})

        results.append({
            "question": question,
            "answer": answer,
            "cache_read": getattr(response.usage, 'cache_read_input_tokens', 0)
        })

    return results
```

## Batch Processing

### Message Batches API

```python
import anthropic
import time

client = anthropic.Anthropic()

def create_batch(requests: list[dict]) -> str:
    """Create a batch of requests."""

    batch = client.batches.create(
        requests=[
            {
                "custom_id": req["id"],
                "params": {
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": req.get("max_tokens", 1024),
                    "messages": req["messages"]
                }
            }
            for req in requests
        ]
    )

    return batch.id


def wait_for_batch(batch_id: str, poll_interval: int = 10) -> dict:
    """Wait for batch completion and return results."""

    while True:
        batch = client.batches.retrieve(batch_id)

        if batch.processing_status == "ended":
            break

        print(f"Batch status: {batch.processing_status}")
        print(f"  Completed: {batch.request_counts.completed}")
        print(f"  Processing: {batch.request_counts.processing}")

        time.sleep(poll_interval)

    # Get results
    results = {}
    for result in client.batches.results(batch_id):
        results[result.custom_id] = {
            "success": result.result.type == "succeeded",
            "response": result.result.message if result.result.type == "succeeded" else None,
            "error": result.result.error if result.result.type == "errored" else None
        }

    return results


# Usage
requests = [
    {"id": "req_1", "messages": [{"role": "user", "content": "Summarize AI"}]},
    {"id": "req_2", "messages": [{"role": "user", "content": "Summarize ML"}]},
    {"id": "req_3", "messages": [{"role": "user", "content": "Summarize DL"}]},
]

batch_id = create_batch(requests)
print(f"Created batch: {batch_id}")

results = wait_for_batch(batch_id)
for req_id, result in results.items():
    if result["success"]:
        print(f"{req_id}: {result['response'].content[0].text[:100]}...")
```

### Parallel Processing (Non-Batch)

```python
import asyncio
import anthropic

async def process_prompts_parallel(prompts: list[str], max_concurrent: int = 5):
    """Process multiple prompts with controlled concurrency."""

    client = anthropic.AsyncAnthropic()
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(prompt: str, index: int):
        async with semaphore:
            try:
                response = await client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                return index, response.content[0].text, None
            except Exception as e:
                return index, None, str(e)

    tasks = [process_one(prompt, i) for i, prompt in enumerate(prompts)]
    results = await asyncio.gather(*tasks)

    # Sort by original index
    return sorted(results, key=lambda x: x[0])


# Usage
prompts = [f"Explain concept {i}" for i in range(20)]
results = asyncio.run(process_prompts_parallel(prompts, max_concurrent=5))
```

## Response Quality Optimization

### Self-Consistency

```python
import anthropic
from collections import Counter

def self_consistent_answer(question: str, num_samples: int = 5, temperature: float = 0.7) -> dict:
    """Get multiple answers and return the most consistent one."""

    client = anthropic.Anthropic()
    answers = []

    for _ in range(num_samples):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": f"""Answer this question concisely. Give only the direct answer.

Question: {question}
Answer:"""
                }
            ]
        )
        answers.append(response.content[0].text.strip())

    # Find most common answer (simplified - real implementation would use semantic similarity)
    answer_counts = Counter(answers)
    most_common = answer_counts.most_common(1)[0]

    return {
        "answer": most_common[0],
        "confidence": most_common[1] / num_samples,
        "all_answers": answers
    }
```

### Iterative Refinement

```python
def iterative_refinement(task: str, max_iterations: int = 3) -> str:
    """Iteratively refine a response through self-critique."""

    client = anthropic.Anthropic()

    # Initial response
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": task}]
    )
    current_output = response.content[0].text

    for i in range(max_iterations):
        # Critique the current output
        critique_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""Review this output and identify specific improvements:

Task: {task}

Current Output:
{current_output}

List 3-5 specific, actionable improvements. If the output is already excellent, say "NO_IMPROVEMENTS_NEEDED"."""
                }
            ]
        )
        critique = critique_response.content[0].text

        if "NO_IMPROVEMENTS_NEEDED" in critique:
            break

        # Refine based on critique
        refined_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": f"""Improve this output based on the feedback:

Original Task: {task}

Current Output:
{current_output}

Feedback:
{critique}

Provide an improved version:"""
                }
            ]
        )
        current_output = refined_response.content[0].text

    return current_output
```

### Decomposition and Synthesis

```python
def decompose_and_synthesize(complex_task: str) -> str:
    """Break down complex tasks and synthesize results."""

    client = anthropic.Anthropic()

    # Step 1: Decompose the task
    decompose_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Break this complex task into 3-5 simpler subtasks:

Task: {complex_task}

List each subtask on a new line, numbered 1-5."""
            }
        ]
    )

    subtasks = decompose_response.content[0].text.strip().split('\n')
    subtasks = [s.strip() for s in subtasks if s.strip()]

    # Step 2: Solve each subtask
    subtask_results = []
    for subtask in subtasks:
        result = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Complete this subtask thoroughly:\n\n{subtask}"
                }
            ]
        )
        subtask_results.append({
            "task": subtask,
            "result": result.content[0].text
        })

    # Step 3: Synthesize results
    results_text = "\n\n".join([
        f"Subtask: {r['task']}\nResult: {r['result']}"
        for r in subtask_results
    ])

    synthesis_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Synthesize these subtask results into a comprehensive response:

Original Task: {complex_task}

Subtask Results:
{results_text}

Provide a unified, coherent response that addresses the original task."""
            }
        ]
    )

    return synthesis_response.content[0].text
```

## Advanced System Prompts

### Dynamic System Prompts

```python
from datetime import datetime

def build_dynamic_system_prompt(user_context: dict) -> str:
    """Build a system prompt that adapts to context."""

    current_time = datetime.now()
    time_of_day = "morning" if current_time.hour < 12 else "afternoon" if current_time.hour < 17 else "evening"

    prompt_parts = [
        f"Current date and time: {current_time.strftime('%Y-%m-%d %H:%M')}",
        f"Good {time_of_day}!",
        "",
        "You are a helpful assistant.",
    ]

    # Add user-specific context
    if user_context.get("name"):
        prompt_parts.append(f"You are helping {user_context['name']}.")

    if user_context.get("expertise_level"):
        level = user_context["expertise_level"]
        if level == "beginner":
            prompt_parts.append("Explain concepts simply, avoiding jargon.")
        elif level == "expert":
            prompt_parts.append("Use technical terminology freely.")

    if user_context.get("preferences"):
        prefs = user_context["preferences"]
        if prefs.get("concise"):
            prompt_parts.append("Keep responses brief and to the point.")
        if prefs.get("examples"):
            prompt_parts.append("Include practical examples when helpful.")

    # Add any domain-specific knowledge
    if user_context.get("domain"):
        prompt_parts.append(f"\nDomain context: {user_context['domain']}")

    return "\n".join(prompt_parts)


# Usage
system_prompt = build_dynamic_system_prompt({
    "name": "Alice",
    "expertise_level": "intermediate",
    "preferences": {"concise": True, "examples": True},
    "domain": "Machine learning for healthcare applications"
})
```

### Multi-Persona System

```python
def multi_persona_analysis(topic: str, personas: list[dict]) -> dict:
    """Get perspectives from multiple expert personas."""

    client = anthropic.Anthropic()
    results = {}

    for persona in personas:
        system = f"""You are a {persona['role']} with expertise in {persona['expertise']}.

Background: {persona.get('background', 'Extensive experience in the field.')}

Approach: {persona.get('approach', 'Analytical and thorough.')}

When analyzing topics, provide your unique perspective based on your expertise."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this topic from your expert perspective: {topic}"
                }
            ]
        )

        results[persona['role']] = response.content[0].text

    # Synthesize perspectives
    perspectives_text = "\n\n".join([
        f"**{role}:**\n{analysis}"
        for role, analysis in results.items()
    ])

    synthesis = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Synthesize these expert perspectives into a balanced analysis:

{perspectives_text}

Identify areas of agreement, disagreement, and provide a balanced conclusion."""
            }
        ]
    )

    results["synthesis"] = synthesis.content[0].text
    return results


# Usage
personas = [
    {"role": "Software Architect", "expertise": "system design"},
    {"role": "Security Expert", "expertise": "cybersecurity"},
    {"role": "Product Manager", "expertise": "user needs and business value"}
]

analysis = multi_persona_analysis("Implementing a new authentication system", personas)
```

## Summary

In this chapter, you've learned:

- **Prompt Engineering**: Chain of thought, few-shot learning, and role-based prompting
- **Output Control**: Structured outputs and format enforcement
- **Prompt Caching**: Reducing costs with cached system prompts
- **Batch Processing**: Efficient handling of multiple requests
- **Quality Optimization**: Self-consistency, iterative refinement, decomposition
- **Advanced Systems**: Dynamic and multi-persona system prompts

## Key Takeaways

1. **Structure Prompts**: Clear structure improves response quality
2. **Cache Strategically**: Large, repeated prompts benefit from caching
3. **Batch When Possible**: Use batches for non-time-sensitive workloads
4. **Iterate for Quality**: Refinement can significantly improve outputs
5. **Match Persona to Task**: Expert personas provide focused insights

## Next Steps

Now that you understand advanced patterns, let's explore Production Best Practices in Chapter 7 for building reliable, scalable applications.

---

**Ready for Chapter 7?** [Production Best Practices](07-production.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `content`, `text`, `messages` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Advanced Patterns` as an operating subsystem inside **Anthropic API Tutorial: Build Production Apps with Claude**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `client`, `role`, `response` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Advanced Patterns` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `content`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `messages`.
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
- search upstream code for `content` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Streaming](05-streaming.md)
- [Next Chapter: Chapter 7: Production Best Practices](07-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
