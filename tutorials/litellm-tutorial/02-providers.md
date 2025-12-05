---
layout: default
title: "LiteLLM Tutorial - Chapter 2: Provider Configuration"
nav_order: 2
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 2: Provider Configuration

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