---
layout: default
title: "LiteLLM Tutorial - Chapter 2: Provider Configuration"
nav_order: 2
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 2: Provider Configuration

Welcome to **Chapter 2: Provider Configuration**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Set up and manage multiple LLM providers with proper authentication and routing.

## Overview

LiteLLM supports 100+ LLM providers. This chapter covers how to configure different providers, manage API keys securely, and route requests intelligently.

## Supported Providers

LiteLLM supports these major categories:

### Cloud Providers
- **OpenAI**: GPT-4, GPT-3.5, DALL-E
- **Anthropic**: Claude 3, Claude 2
- **Google**: Vertex AI, PaLM, Gemini
- **Microsoft**: Azure OpenAI, Azure Cognitive Services
- **Amazon**: Bedrock (supports 40+ models)
- **Cohere**: Command, Embed
- **AI21 Labs**: Jurassic models
- **Together AI**: Open-source models
- **Replicate**: Any model on Replicate

### Local Providers
- **Ollama**: Run models locally
- **LM Studio**: Local model server
- **Hugging Face**: Inference endpoints
- **vLLM**: High-performance local inference
- **Text Generation WebUI**: Local web interface

## API Key Management

### Environment Variables (Recommended)

```bash
# .env file
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
COHERE_API_KEY="..."
GOOGLE_API_KEY="..."
AZURE_API_KEY="..."
AZURE_API_BASE="https://your-resource.openai.azure.com/"
AZURE_API_VERSION="2023-12-01-preview"
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_REGION_NAME="us-east-1"
```

### Programmatic Configuration

```python
import litellm
import os

# Set API keys programmatically
litellm.openai_key = os.getenv("OPENAI_API_KEY")
litellm.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
litellm.cohere_key = os.getenv("COHERE_API_KEY")

# Or use the set_api_key method
litellm.set_api_key("openai", os.getenv("OPENAI_API_KEY"))
litellm.set_api_key("anthropic", os.getenv("ANTHROPIC_API_KEY"))
```

## Provider-Specific Configuration

### OpenAI

```python
import litellm

# Basic setup
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    api_key=os.getenv("OPENAI_API_KEY")  # Optional if set globally
)

# Custom base URL (for proxies or custom deployments)
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    api_base="https://your-proxy.openai.com/v1"
)
```

### Anthropic (Claude)

```python
# Claude 3 models
response = litellm.completion(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Explain quantum physics"}],
    max_tokens=1000,
    temperature=0.7
)

# Claude 2 (legacy)
response = litellm.completion(
    model="claude-2",
    messages=[{"role": "user", "content": "Write a story"}],
    max_tokens_to_sample=500
)
```

### Google Vertex AI

```python
# Set up Google credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service-account.json"

# Or set project and location
litellm.vertex_project = "your-gcp-project"
litellm.vertex_location = "us-central1"

response = litellm.completion(
    model="chat-bison",
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### AWS Bedrock

```python
import boto3

# Configure AWS credentials
litellm.bedrock_aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
litellm.bedrock_aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
litellm.bedrock_aws_region_name = os.getenv("AWS_REGION_NAME", "us-east-1")

# Available models
response = litellm.completion(
    model="bedrock/anthropic.claude-v2",
    messages=[{"role": "user", "content": "Analyze this data"}]
)

# Other Bedrock models
# "bedrock/meta.llama2-13b-chat-v1"
# "bedrock/cohere.command-text-v14"
# "bedrock/amazon.titan-text-express-v1"
```

### Azure OpenAI

```python
# Configure Azure
litellm.azure_key = os.getenv("AZURE_API_KEY")
litellm.azure_api_base = os.getenv("AZURE_API_BASE")
litellm.azure_api_version = os.getenv("AZURE_API_VERSION", "2023-12-01-preview")

response = litellm.completion(
    model="azure/gpt-4",  # or "azure/gpt-35-turbo"
    messages=[{"role": "user", "content": "Hello from Azure"}],
    deployment_id="your-deployment-name"  # Optional
)
```

### Local Models with Ollama

```python
# First, install and run Ollama locally
# Then pull models: ollama pull llama2

response = litellm.completion(
    model="ollama/llama2",
    messages=[{"role": "user", "content": "Explain Docker"}],
    api_base="http://localhost:11434"  # Default Ollama port
)

# Other Ollama models
# "ollama/codellama", "ollama/mistral", "ollama/orca-mini"
```

## Configuration File

Use a configuration file for complex setups:

```python
# config.py
LITELLM_CONFIG = {
    "general_settings": {
        "database_url": "sqlite:///litellm.db",  # For cost tracking
        "log_level": "INFO"
    },
    "model_list": [
        {
            "model_name": "gpt-4",
            "litellm_params": {
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY")
            }
        },
        {
            "model_name": "claude-3",
            "litellm_params": {
                "model": "claude-3-opus-20240229",
                "api_key": os.getenv("ANTHROPIC_API_KEY")
            }
        },
        {
            "model_name": "bedrock-claude",
            "litellm_params": {
                "model": "bedrock/anthropic.claude-v2",
                "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
                "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "aws_region_name": os.getenv("AWS_REGION_NAME")
            }
        }
    ]
}

# Load configuration
import litellm
litellm.config = LITELLM_CONFIG
```

## Dynamic Provider Selection

Route requests based on criteria:

```python
def select_model_by_cost(message_length, complexity="simple"):
    """Select model based on cost and requirements."""
    if message_length < 100 and complexity == "simple":
        return "gpt-3.5-turbo"  # Cheap and fast
    elif complexity == "creative":
        return "claude-3-sonnet-20240229"  # Good for creative tasks
    elif message_length > 1000:
        return "gpt-4-turbo"  # Handles long contexts well
    else:
        return "gpt-4"  # Default high-quality

def smart_completion(messages, **kwargs):
    """Smart completion that chooses the right model."""
    message_length = sum(len(msg["content"]) for msg in messages)
    complexity = kwargs.get("complexity", "simple")

    model = select_model_by_cost(message_length, complexity)

    return litellm.completion(
        model=model,
        messages=messages,
        **{k: v for k, v in kwargs.items() if k != "complexity"}
    )

# Usage
response = smart_completion(
    messages=[{"role": "user", "content": "Write a short poem"}],
    complexity="creative"
)
```

## Provider Health Checks

Monitor provider availability:

```python
import asyncio
import time

async def check_provider_health(model_name, timeout=10):
    """Check if a provider is responding."""
    try:
        start_time = time.time()
        response = await litellm.acompletion(
            model=model_name,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
            timeout=timeout
        )
        latency = time.time() - start_time
        return {"status": "healthy", "latency": latency}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def health_check_all_providers():
    """Check all configured providers."""
    models_to_check = [
        "gpt-3.5-turbo",
        "claude-3-haiku-20240307",
        "command",
        "ollama/llama2"
    ]

    results = {}
    for model in models_to_check:
        print(f"Checking {model}...")
        results[model] = await check_provider_health(model)

    return results

# Run health checks
results = asyncio.run(health_check_all_providers())
for model, status in results.items():
    print(f"{model}: {status['status']} ({status.get('latency', 'N/A')}s)")
```

## Cost-Aware Routing

Route based on cost constraints:

```python
# Cost per 1K tokens (approximate, as of 2024)
MODEL_COSTS = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
}

def estimate_cost(model, input_tokens, output_tokens):
    """Estimate cost for a request."""
    if model not in MODEL_COSTS:
        return float('inf')  # Unknown cost

    costs = MODEL_COSTS[model]
    return (input_tokens * costs["input"] + output_tokens * costs["output"]) / 1000

def select_model_by_budget(messages, max_budget=0.01, quality_preference="balanced"):
    """Select model within budget constraints."""
    # Estimate input tokens (rough approximation)
    input_text = " ".join([msg["content"] for msg in messages])
    estimated_input_tokens = len(input_text.split()) * 1.3  # Rough estimate

    candidates = []

    for model in MODEL_COSTS:
        # Assume output tokens similar to input
        estimated_cost = estimate_cost(model, estimated_input_tokens, estimated_input_tokens)

        if estimated_cost <= max_budget:
            candidates.append((model, estimated_cost))

    if not candidates:
        return "gpt-3.5-turbo"  # Fallback to cheapest

    # Sort by cost (ascending) or quality preference
    if quality_preference == "cheap":
        return min(candidates, key=lambda x: x[1])[0]
    elif quality_preference == "expensive":
        return max(candidates, key=lambda x: x[1])[0]
    else:  # balanced
        # Sort by cost but prefer quality within budget
        candidates.sort(key=lambda x: x[1])
        return candidates[len(candidates)//2][0]  # Middle option

# Usage
model = select_model_by_budget(
    messages=[{"role": "user", "content": "Short question"}],
    max_budget=0.005,
    quality_preference="balanced"
)

response = litellm.completion(model=model, messages=messages)
```

## Provider Fallback Configuration

Set up automatic fallbacks:

```python
# Define fallback chains
FALLBACK_CHAINS = {
    "high_quality": ["gpt-4", "claude-3-opus-20240229", "gpt-4-turbo"],
    "fast_cheap": ["gpt-3.5-turbo", "claude-3-haiku-20240307", "command"],
    "creative": ["claude-3-sonnet-20240229", "gpt-4", "claude-3-opus-20240229"]
}

def completion_with_fallbacks(messages, chain_name="high_quality", **kwargs):
    """Try providers in order until one succeeds."""
    chain = FALLBACK_CHAINS.get(chain_name, FALLBACK_CHAINS["high_quality"])

    last_error = None
    for model in chain:
        try:
            print(f"Trying {model}...")
            response = litellm.completion(
                model=model,
                messages=messages,
                **kwargs
            )
            print(f"Success with {model}")
            return response, model
        except Exception as e:
            print(f"Failed with {model}: {e}")
            last_error = e
            continue

    raise Exception(f"All providers in chain '{chain_name}' failed. Last error: {last_error}")

# Usage
response, used_model = completion_with_fallbacks(
    messages=[{"role": "user", "content": "Hello"}],
    chain_name="fast_cheap",
    max_tokens=100
)
```

## Security Best Practices

1. **Never Commit Keys**: Use environment variables or secret management
2. **Principle of Least Privilege**: Use API keys with minimal required permissions
3. **Rotate Keys Regularly**: Change API keys periodically
4. **Monitor Usage**: Track which providers and models are being used
5. **Rate Limiting**: Implement application-level rate limiting

## Testing Configuration

Create a test suite for your provider setup:

```python
# test_providers.py
import litellm
import asyncio

async def test_all_providers():
    """Test all configured providers."""
    test_message = {"role": "user", "content": "Say 'test' and nothing else."}
    test_models = [
        "gpt-3.5-turbo",
        "claude-3-haiku-20240307",
        "command",
        "ollama/llama2"
    ]

    results = {}
    for model in test_models:
        try:
            response = await litellm.acompletion(
                model=model,
                messages=[test_message],
                max_tokens=10,
                timeout=30
            )

            content = response.choices[0].message.content.strip().lower()
            success = "test" in content and len(content) < 20

            results[model] = {
                "status": "success" if success else "unexpected_response",
                "response": content
            }

        except Exception as e:
            results[model] = {
                "status": "error",
                "error": str(e)
            }

    return results

# Run tests
if __name__ == "__main__":
    results = asyncio.run(test_all_providers())

    print("Provider Test Results:")
    print("=" * 50)

    for model, result in results.items():
        status = result["status"]
        if status == "success":
            print(f"✅ {model}: Working correctly")
        elif status == "unexpected_response":
            print(f"⚠️  {model}: Unexpected response - '{result['response']}'")
        else:
            print(f"❌ {model}: Error - {result['error']}")
```

This comprehensive provider configuration gives you the flexibility to use any LLM provider while maintaining a consistent interface and handling provider-specific requirements.

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**
- tutorial slug: **litellm-tutorial**
- chapter focus: **Chapter 2: Provider Configuration**
- system context: **Litellm Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 2: Provider Configuration`.
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

1. Build a minimal end-to-end implementation for `Chapter 2: Provider Configuration`.
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

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `litellm`, `messages` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Provider Configuration` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `response`, `getenv` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Provider Configuration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `litellm` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `messages`.
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
- search upstream code for `model` and `litellm` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with LiteLLM](01-getting-started.md)
- [Next Chapter: Chapter 3: Completion API](03-completion.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
