---
layout: default
title: "LiteLLM Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 1: Getting Started with LiteLLM

Welcome to **Chapter 1: Getting Started with LiteLLM**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Install LiteLLM, configure your first provider, and make your initial LLM call with a unified interface.

## Overview

LiteLLM provides a single interface to call 100+ LLM providers. This chapter covers installation, basic setup, and your first cross-provider LLM call.

## Prerequisites

- Python 3.8+
- API keys for at least one LLM provider (OpenAI recommended for starters)
- Basic command line knowledge

## Installation

Install LiteLLM via pip:

```bash
pip install litellm
```

For development or to use the proxy server:

```bash
pip install litellm[proxy]
```

## Basic Setup

Set up environment variables for your LLM providers:

```bash
# OpenAI (recommended for getting started)
export OPENAI_API_KEY="sk-your-openai-key"

# Optional: Other providers
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
export COHERE_API_KEY="your-cohere-key"
```

## Your First LiteLLM Call

Use the OpenAI-compatible interface that works with any provider:

```python
import litellm

# Set your API key
litellm.openai_key = "sk-your-openai-key"

# Make a call (defaults to GPT-3.5-turbo)
response = litellm.completion(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello! How are you?"}
    ]
)

print(response.choices[0].message.content)
```

## Understanding the Response

LiteLLM returns responses in OpenAI format:

```python
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "Hello! I'm doing well, thank you for asking. How can I help you today?",
                "role": "assistant"
            }
        }
    ],
    "created": 1677652288,
    "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
    "model": "gpt-3.5-turbo-0613",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 23,
        "prompt_tokens": 13,
        "total_tokens": 36
    }
}
```

## Using Different Models

Call different models with the same interface:

```python
# GPT-4
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain quantum computing simply"}]
)

# GPT-3.5 Turbo (cheaper/faster)
response = litellm.completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a haiku about programming"}]
)

# Claude via Anthropic
response = litellm.completion(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "What are the benefits of renewable energy?"}]
)
```

## Model Naming Convention

LiteLLM uses consistent model naming:

```
# OpenAI models
"gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"

# Anthropic models
"claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"

# Google Vertex AI
"chat-bison", "chat-bison-32k", "codechat-bison"

# Cohere
"command", "command-light", "command-nightly"

# Azure OpenAI
"azure/gpt-4", "azure/gpt-3.5-turbo"

# Local models (Ollama)
"ollama/llama2", "ollama/codellama"
```

## Configuration Options

Customize your calls:

```python
response = litellm.completion(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to reverse a string"}
    ],
    max_tokens=150,           # Limit response length
    temperature=0.7,          # Control randomness (0.0-1.0)
    top_p=1.0,               # Nucleus sampling
    frequency_penalty=0.0,    # Reduce repetition
    presence_penalty=0.0,     # Encourage topic diversity
    stop=["\n\n", "###"]      # Stop sequences
)
```

## Error Handling

Handle API errors gracefully:

```python
import litellm

try:
    response = litellm.completion(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

except litellm.AuthenticationError:
    print("Invalid API key")

except litellm.RateLimitError:
    print("Rate limit exceeded, please try again later")

except litellm.APIError as e:
    print(f"API error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Logging and Debugging

Enable verbose logging:

```python
import litellm

# Enable debug logging
litellm.set_verbose = True

# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)

response = litellm.completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Test message"}]
)
```

## CLI Usage

Use LiteLLM from the command line:

```bash
# Set API key
export OPENAI_API_KEY="sk-your-key"

# Make a completion
litellm --model gpt-3.5-turbo --message "Explain recursion in simple terms"

# Interactive chat
litellm --model gpt-4 --interactive
```

## Environment Variables

Set all configuration via environment variables:

```bash
# Provider API keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
COHERE_API_KEY="..."
GOOGLE_API_KEY="..."

# LiteLLM settings
LITELLM_LOG="INFO"  # DEBUG, INFO, WARNING, ERROR
LITELLM_DROPPED_PARAMS="true"  # Log dropped parameters
```

## Testing Your Setup

Create a simple test script:

```python
#!/usr/bin/env python3
"""Test LiteLLM setup with multiple providers."""

import litellm

def test_provider(model_name, test_message="Hello, world!"):
    """Test a specific model/provider."""
    try:
        response = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": test_message}],
            max_tokens=50
        )
        print(f"✅ {model_name}: {response.choices[0].message.content.strip()}")
        return True
    except Exception as e:
        print(f"❌ {model_name}: {str(e)}")
        return False

if __name__ == "__main__":
    # Test different models
    models_to_test = [
        "gpt-3.5-turbo",
        "claude-3-haiku-20240307",  # if you have Anthropic key
        "command",  # if you have Cohere key
    ]

    for model in models_to_test:
        test_provider(model)
```

## Best Practices

1. **Start Simple**: Begin with OpenAI models to learn the interface
2. **Environment Variables**: Never hardcode API keys in your code
3. **Error Handling**: Always wrap API calls in try-catch blocks
4. **Cost Awareness**: Monitor token usage (covered in later chapters)
5. **Model Selection**: Choose appropriate models for your use case

## Troubleshooting

Common issues and solutions:

- **AuthenticationError**: Check your API key is correct and has proper permissions
- **RateLimitError**: You exceeded the provider's rate limits
- **NotFoundError**: The model name doesn't exist or isn't available
- **APIConnectionError**: Network issues or provider downtime

## Next Steps

Now that you can make basic LLM calls, let's explore how to configure multiple providers and switch between them seamlessly.

Run this to confirm everything works:

```bash
python -c "
import litellm
response = litellm.completion(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Say hello to LiteLLM!'}]
)
print('Response:', response.choices[0].message.content)
"
```

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- tutorial slug: **litellm-tutorial**
- chapter focus: **Chapter 1: Getting Started with LiteLLM**
- system context: **Litellm Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started with LiteLLM`.
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

1. Build a minimal end-to-end implementation for `Chapter 1: Getting Started with LiteLLM`.
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

### Scenario Playbook 1: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 1: Getting Started with LiteLLM

- tutorial context: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `litellm`, `model`, `content` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with LiteLLM` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `turbo`, `completion` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with LiteLLM` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `litellm`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `content`.
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
- search upstream code for `litellm` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Provider Configuration](02-providers.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
