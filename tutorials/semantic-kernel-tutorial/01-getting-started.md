---
layout: default
title: "Semantic Kernel Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 1: Getting Started with Semantic Kernel

> Install Semantic Kernel, wire up your first AI service, and run a simple plugin-powered prompt in minutes.

## Installation & Setup

### Python (recommended)

```bash
# Core SDK
pip install semantic-kernel

# OpenAI + Azure connectors
pip install semantic-kernel[openai]
pip install semantic-kernel[azure]

# Optional: vector stores for memory
pip install semantic-kernel[chroma] semantic-kernel[qdrant] semantic-kernel[pinecone]
```

Environment variables (add to `.env`):

```bash
OPENAI_API_KEY=sk-your-openai-key
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
DEFAULT_MODEL=gpt-4o
```

### .NET (C#)

```bash
dotnet new console -n sk-quickstart
cd sk-quickstart
dotnet add package Microsoft.SemanticKernel
dotnet add package Microsoft.SemanticKernel.Connectors.OpenAI
```

## Your First Kernel (Python)

```python
import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


async def main():
    kernel = sk.Kernel()

    # Register AI service
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id="gpt-4o",
            api_key="YOUR_OPENAI_KEY",
        )
    )

    # Create a semantic function (prompt template)
    summarize = kernel.create_function_from_prompt(
        function_name="summarize",
        plugin_name="Writer",
        prompt="""
        Summarize the following text in {{$style}} style:
        {{$input}}
        """
    )

    # Invoke with variables
    result = await kernel.invoke(
        summarize,
        input="Semantic Kernel is an orchestration SDK from Microsoft.",
        style="executive"
    )
    print(result)


asyncio.run(main())
```

## Minimal .NET Example

```csharp
using Microsoft.SemanticKernel;

var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-4o", apiKey: Environment.GetEnvironmentVariable("OPENAI_API_KEY"));
var kernel = builder.Build();

var result = await kernel.InvokePromptAsync(
    "Summarize Semantic Kernel in two sentences for an architect."
);

Console.WriteLine(result);
```

## Quick Troubleshooting

- **401/403 errors**: Verify API keys and model names; check Azure deployment name vs model name.
- **Rate limits**: Lower `max_tokens`, enable retries/backoff, and cache outputs.
- **Async issues**: Ensure you `await kernel.invoke(...)`; wrap in `asyncio.run` for scripts.
- **Missing connectors**: Install extras (`semantic-kernel[openai]`, etc.).

## Quick Start Checklist

- [ ] Install Semantic Kernel + connectors
- [ ] Set environment variables (`OPENAI_API_KEY`, Azure settings)
- [ ] Run the Python quickstart
- [ ] Verify first semantic function call
- [ ] Commit a `.env.example` (omit secrets) for your team

Next: **[Chapter 2: Plugins & Functions](02-plugins.md)** to build native and semantic plugins. 🚀
