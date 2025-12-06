---
layout: default
title: "Semantic Kernel Tutorial - Chapter 4: AI Services"
nav_order: 4
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 4: AI Services & Connectors

> Connect OpenAI, Azure OpenAI, Hugging Face, and local models with retries, fallbacks, and routing.

## Registering Services (Python)

```python
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion


kernel = sk.Kernel()

# OpenAI
kernel.add_service(
    OpenAIChatCompletion(
        service_id="openai",
        ai_model_id="gpt-4o",
        api_key="OPENAI_KEY",
    )
)

# Azure OpenAI
kernel.add_service(
    AzureChatCompletion(
        service_id="azure",
        deployment_name="gpt-4o",
        endpoint="https://your-resource.openai.azure.com/",
        api_key="AZURE_KEY",
    )
)

# Hugging Face Inference
kernel.add_service(
    HuggingFaceTextCompletion(
        service_id="hf",
        model_id="gpt2",
        api_key="HF_KEY",
    )
)
```

## Service Selection & Routing

```python
def select_service(requirements: dict) -> str:
    if requirements.get("vision"):
        return "azure"
    if requirements.get("low_cost"):
        return "hf"
    return "openai"


async def run_with_routing(func, **kwargs):
    service_id = select_service(kwargs.get("requirements", {}))
    return await kernel.invoke(func, **kwargs, service_id=service_id)
```

## Retries, Timeouts, Circuit Breakers

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def safe_invoke(func, **kwargs):
    return await asyncio.wait_for(
        kernel.invoke(func, **kwargs),
        timeout=20,
    )
```

## Streaming Responses

```python
async for chunk in kernel.invoke_stream(
    some_function,
    input="Stream this response",
    service_id="openai",
):
    print(chunk, end="", flush=True)
```

## Observability

- Log **service_id**, model, latency, tokens, and error codes.
- Export traces/metrics to OpenTelemetry; attach request IDs for correlation.
- Record success/failure rates per provider to tune routing.

## Cost & Policy Controls

- Enforce model allowlists/denylists per environment.
- Cap `max_tokens`, set budget alerts per provider, and use cheaper models for non-critical paths.
- Add PII redaction before sending to third-party providers when required.

## Checklist

- [ ] Register at least two AI services (OpenAI + Azure or HF)
- [ ] Add retry/backoff + timeouts
- [ ] Enable streaming for long responses
- [ ] Log tokens/latency and tag with `service_id`
- [ ] Implement simple routing (quality vs cost vs capability)

Next: **[Chapter 5: Memory & Embeddings](05-memory.md)** to add semantic memory and retrieval. 🧠
