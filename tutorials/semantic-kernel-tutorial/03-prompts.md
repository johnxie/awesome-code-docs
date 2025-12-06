---
layout: default
title: "Semantic Kernel Tutorial - Chapter 3: Prompt Engineering"
nav_order: 3
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 3: Prompt Engineering

> Design resilient prompt templates with variables, few-shot examples, safety rails, and output controls.

## Prompt Template Basics

```python
import semantic_kernel as sk

qa_template = sk.PromptTemplateConfig(
    template="""
    You are an expert support assistant.
    Answer the user's question using the provided context.

    Context:
    {{$context}}

    Question: {{$question}}
    Answer in {{$style}} tone and keep it under {{$words}} words.
    """,
    input_variables=[
        {"name": "context", "description": "Grounding context"},
        {"name": "question", "description": "User question"},
        {"name": "style", "description": "Tone", "default": "concise"},
        {"name": "words", "description": "Word budget", "default": "120"},
    ],
    execution_settings=sk.PromptExecutionSettings(
        max_tokens=256,
        temperature=0.3,
        top_p=0.9,
    ),
)

qa = kernel.create_function_from_prompt(
    function_name="qa",
    plugin_name="Support",
    prompt_template_config=qa_template,
)
```

## Few-Shot & Style Control

```python
style_template = sk.PromptTemplateConfig(
    template="""
    You rewrite text to match the requested style.

    Examples:
    - Style: formal | Input: Thanks for the info! | Output: Thank you for the information.
    - Style: casual | Input: Please provide details. | Output: Hey, can you share more details?

    Now rewrite:
    Style: {{$style}}
    Input: {{$text}}
    """,
)

rewrite = kernel.create_function_from_prompt(
    function_name="rewrite",
    plugin_name="Stylist",
    prompt_template_config=style_template,
)

result = await kernel.invoke(rewrite, style="enthusiastic", text="Welcome to Semantic Kernel.")
```

## Grounded Generation Pattern

```python
grounded_template = sk.PromptTemplateConfig(
    template="""
    Use ONLY the provided sources to answer.
    If the answer is not present, say "I don't know based on the sources."

    Sources:
    {{$sources}}

    Question: {{$question}}
    """,
    execution_settings=sk.PromptExecutionSettings(
        max_tokens=200,
        temperature=0.2,
        frequency_penalty=0,
    ),
)
```

## Safety & Guardrails

- Add explicit **behavior rules**: refusal policy, PII handling, brand tone.
- Constrain outputs: word/character limits, bullet lists, JSON schema when needed.
- Set conservative **temperature** for factual tasks; raise for creative tasks.
- Include **"If unsure, say you are unsure"** to avoid hallucinations.

## Prompt Debugging Tips

- Log rendered prompts (with sensitive data redacted) for reproducibility.
- Capture latency and token usage per prompt for cost/SLAs.
- A/B test prompt variants; keep evaluation sets for regression.
- Use tracing (e.g., LangSmith/OpenTelemetry exporters) to follow prompt chains.

## Checklist

- [ ] Define input variables with defaults and descriptions
- [ ] Set execution settings (temperature, max tokens, stop sequences)
- [ ] Add examples for few-shot style control
- [ ] Add grounding instructions and refusal behavior
- [ ] Log prompts and measure token/latency for tuning

Next: **[Chapter 4: AI Services](04-services.md)** to connect OpenAI, Azure, and local models. 🛰️
