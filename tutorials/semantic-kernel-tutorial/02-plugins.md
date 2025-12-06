---
layout: default
title: "Semantic Kernel Tutorial - Chapter 2: Plugins & Functions"
nav_order: 2
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 2: Plugins & Functions

> Build native and semantic functions, package them as plugins, and compose them for reusable AI capabilities.

## Plugin Types

- **Native functions**: Plain Python/C# methods decorated with `@kernel_function` (or C# attributes) for deterministic logic.
- **Semantic functions**: Prompt templates with variables and configuration (temperature, top_p, stop sequences).
- **Hybrid plugins**: Mix native utilities with semantic prompts in one plugin namespace.

## Creating Native Functions (Python)

```python
from semantic_kernel.functions import kernel_function


class MathPlugin:
    @kernel_function(name="add", description="Add two numbers")
    def add(self, a: float, b: float) -> float:
        return a + b

    @kernel_function(name="percent_change", description="Calculate percent change")
    def percent_change(self, old: float, new: float) -> float:
        return ((new - old) / old) * 100


# Register plugin
kernel.add_plugin(MathPlugin(), plugin_name="math")

# Invoke
result = await kernel.invoke(kernel.plugins["math"]["percent_change"], old=100, new=125)
print(result)
```

## Semantic Functions (Prompt Templates)

```python
import semantic_kernel as sk

email_template = sk.PromptTemplateConfig(
    template="""
    Draft a {{$tone}} email about {{$topic}} to {{$audience}}.
    Keep it under {{$words}} words and end with a clear CTA.
    """,
    input_variables=[
        {"name": "tone", "description": "Tone of voice", "default": "concise"},
        {"name": "topic", "description": "Main topic"},
        {"name": "audience", "description": "Target audience"},
        {"name": "words", "description": "Word limit", "default": "120"},
    ],
)

email = kernel.create_function_from_prompt(
    function_name="email",
    plugin_name="Writer",
    prompt_template_config=email_template,
)

draft = await kernel.invoke(
    email,
    topic="launching our new API",
    audience="developer community",
    tone="friendly",
    words=100,
)
```

## Organizing Plugins

```
plugins/
  Writer/
    email.yaml          # prompt config (semantic)
    outline.yaml
  Math/
    __init__.py         # native functions
    stats.py
```

- Keep prompts in YAML/JSON alongside code for versioning.
- Group related functions into plugin namespaces for discoverability.

## Best Practices

- **Deterministic core logic**: Use native functions for calculations, validation, and formatting; keep prompts for creativity.
- **Type safety**: Validate inputs/outputs; consider pydantic models for structured responses.
- **Guardrails**: Set `max_tokens`, `temperature`, and add safety instructions in prompts.
- **Streaming**: Use streaming APIs for long outputs; surface progress to callers.
- **Cancellation**: Propagate timeouts or cancellation tokens from the host app.

## Testing Plugins

```python
import pytest


@pytest.mark.asyncio
async def test_add():
    kernel = sk.Kernel()
    kernel.add_plugin(MathPlugin(), "math")
    result = await kernel.invoke(kernel.plugins["math"]["add"], a=2, b=3)
    assert result == 5
```

## Checklist

- [ ] Create at least one native plugin (`@kernel_function`)
- [ ] Create a semantic prompt function with variables
- [ ] Register plugins under clear namespaces
- [ ] Add tests for deterministic native functions
- [ ] Document inputs/outputs for your team

Next: **[Chapter 3: Prompt Engineering](03-prompts.md)** to design robust templates. 🎨
