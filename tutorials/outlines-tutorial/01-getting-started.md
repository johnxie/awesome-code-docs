---
layout: default
title: "Outlines Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Outlines Tutorial
---

# Chapter 1: Getting Started with Outlines

Welcome to **Chapter 1: Getting Started with Outlines**. In this part of **Outlines Tutorial: Structured Text Generation with LLMs**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master the fundamentals of constrained text generation with Outlines - install, configure, and generate your first structured outputs.

## Installation

### Basic Installation

```bash
# Install Outlines
pip install outlines

# For development with latest features
pip install git+https://github.com/outlines-dev/outlines.git

# Optional: Install with specific backends
pip install outlines[transformers]  # For Hugging Face models
pip install outlines[llamacpp]      # For llama.cpp models
pip install outlines[vllm]          # For vLLM models
```

### Environment Setup

```bash
# Create a virtual environment
python -m venv outlines_env
source outlines_env/bin/activate  # On Windows: outlines_env\Scripts\activate

# Install dependencies
pip install outlines torch transformers

# Verify installation
python -c "import outlines; print('Outlines version:', outlines.__version__)"
```

## Your First Constrained Generation

### Basic Setup

```python
import outlines
from outlines import models

# Load a model (using Transformers backend)
model = models.transformers("microsoft/DialoGPT-small")

# Create a generator with text constraints
generator = outlines.generate.text(model)

# Generate unconstrained text
unconstrained = generator("Hello, how are you?")
print("Unconstrained:", unconstrained)

# Generate with length constraints
length_generator = outlines.generate.text(model, max_tokens=10)
constrained = length_generator("Hello, how are you?")
print("Length constrained:", constrained)
```

### Choice Constraints

The most basic form of constrained generation is limiting outputs to a specific set of choices:

```python
from outlines import generate

# Define a model
model = models.transformers("microsoft/DialoGPT-small")

# Create a generator that only outputs specific choices
choices_generator = generate.choice(model, ["Yes", "No", "Maybe"])

# Generate responses
response1 = choices_generator("Should I go to the party?")
response2 = choices_generator("Is it going to rain tomorrow?")
response3 = choices_generator("Do you like pizza?")

print(f"Party: {response1}")
print(f"Rain: {response2}")
print(f"Pizza: {response3}")
```

## Understanding the Architecture

### How Outlines Works

```python
# Outlines generation pipeline
"""
1. User provides constraints (choices, regex, schema, etc.)
2. Outlines analyzes the model vocabulary and constraints
3. Creates a mask that only allows valid next tokens
4. Applies mask during generation to enforce constraints
5. Returns guaranteed valid output
"""

# Example: Under the hood
import torch
from outlines.processors import ChoiceProcessor

# Create processor for choices
processor = ChoiceProcessor(["red", "blue", "green"])

# The processor creates a mask for valid tokens
# Only tokens that can lead to valid completions are allowed
mask = processor.get_mask(model.tokenizer)

# During generation, only masked tokens are sampled
# This guarantees the output will be one of: "red", "blue", "green"
```

### Performance Characteristics

```python
import time
from outlines import models, generate

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# Test generation speeds
choices = ["positive", "negative", "neutral"]
choice_gen = generate.choice(model, choices)

# Benchmark constrained generation
start_time = time.time()
for _ in range(10):
    result = choice_gen("The movie was")
end_time = time.time()

print(f"Constrained generation: {(end_time - start_time)/10:.3f} seconds per query")

# Compare with unconstrained (approximate)
text_gen = generate.text(model, max_tokens=10)
start_time = time.time()
for _ in range(10):
    result = text_gen("The movie was")
end_time = time.time()

print(f"Unconstrained generation: {(end_time - start_time)/10:.3f} seconds per query")
```

## Different Model Backends

### Transformers Backend (Recommended for Getting Started)

```python
from outlines import models
from transformers import AutoTokenizer, AutoModelForCausalLM

# Method 1: Direct model loading
model = models.transformers("microsoft/DialoGPT-small")

# Method 2: Using pre-loaded model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
hf_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

model = models.transformers(hf_model, tokenizer)

# Method 3: With device specification
model = models.transformers(
    "microsoft/DialoGPT-small",
    device="cuda"  # or "cpu"
)
```

### Llama.cpp Backend

```python
from outlines import models

# Load GGUF model with llama.cpp
model = models.llamacpp(
    model_path="/path/to/model.gguf",
    tokenizer_path="/path/to/tokenizer.json"  # Optional
)

# The model is automatically loaded with llama.cpp
# Supports all Outlines constraints
generator = outlines.generate.choice(model, ["yes", "no"])
result = generator("Should I continue?")
```

### vLLM Backend

```python
from outlines import models

# For vLLM served models
model = models.vllm(
    model_name="microsoft/DialoGPT-small",
    tokenizer_name="microsoft/DialoGPT-small"
)

# Connect to running vLLM server
model = models.vllm(
    model_name="microsoft/DialoGPT-small",
    base_url="http://localhost:8000"  # vLLM server URL
)
```

## Error Handling and Debugging

### Common Issues and Solutions

```python
from outlines import generate, models
import traceback

def safe_constrained_generation(model_name: str, constraint_type: str, constraint_value, prompt: str):
    """Safe constrained generation with comprehensive error handling."""

    try:
        # Load model
        model = models.transformers(model_name)

        # Create generator based on constraint type
        if constraint_type == "choice":
            generator = generate.choice(model, constraint_value)
        elif constraint_type == "regex":
            generator = generate.regex(model, constraint_value)
        elif constraint_type == "text":
            generator = generate.text(model, **constraint_value)
        else:
            raise ValueError(f"Unknown constraint type: {constraint_type}")

        # Generate with timeout
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError("Generation timed out")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30 second timeout

        try:
            result = generator(prompt)
            signal.alarm(0)  # Cancel timeout
            return {"success": True, "result": result}
        except TimeoutError:
            return {"success": False, "error": "Generation timed out"}

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# Usage with error handling
result = safe_constrained_generation(
    model_name="microsoft/DialoGPT-small",
    constraint_type="choice",
    constraint_value=["yes", "no", "maybe"],
    prompt="Will it rain tomorrow?"
)

if result["success"]:
    print(f"Generated: {result['result']}")
else:
    print(f"Error: {result['error']}")
```

## Advanced Getting Started Examples

### Multi-Choice with Probabilities

```python
from outlines import generate, models
import numpy as np

model = models.transformers("microsoft/DialoGPT-small")

# Create generator with custom sampling
generator = generate.choice(
    model,
    ["excellent", "good", "average", "poor"],
    sampler=outlines.samplers.multinomial(temperature=0.5)
)

# Generate multiple responses
responses = []
for _ in range(5):
    response = generator("Rate this tutorial:")
    responses.append(response)

print("Generated ratings:", responses)

# Analyze distribution
from collections import Counter
distribution = Counter(responses)
print("Rating distribution:", dict(distribution))
```

### JSON Output (Preview)

```python
from outlines import generate, models
import json

model = models.transformers("microsoft/DialoGPT-small")

# Simple JSON structure (more advanced in later chapters)
json_generator = generate.json(model, {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["sentiment"]
})

# Note: This is a simplified example
# Full JSON schema support comes in Chapter 3
prompt = "Analyze the sentiment of: 'This product is amazing!'"
# result = json_generator(prompt)  # Would work with full JSON support
```

## Performance Optimization

### Memory Management

```python
import torch
from outlines import models

# Optimize memory usage
torch.cuda.empty_cache()  # Clear CUDA cache

# Load model with memory optimization
model = models.transformers(
    "microsoft/DialoGPT-small",
    model_kwargs={
        "torch_dtype": torch.float16,  # Use half precision
        "load_in_8bit": True,          # 8-bit quantization
        "device_map": "auto"           # Automatic device placement
    }
)

# Monitor memory usage
def log_memory_usage():
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**2  # MB
        reserved = torch.cuda.memory_reserved() / 1024**2    # MB
        print(f"GPU Memory - Allocated: {allocated:.1f}MB, Reserved: {reserved:.1f}MB")
    else:
        print("Running on CPU")

log_memory_usage()
```

### Batch Processing

```python
from outlines import generate, models
import asyncio

async def batch_constrained_generation(model, prompts, constraints):
    """Generate multiple constrained outputs in parallel."""

    # Create generators for each constraint type
    generators = {}
    for constraint_type, constraint_value in constraints.items():
        if constraint_type == "choice":
            generators[constraint_type] = generate.choice(model, constraint_value)

    # Generate in batches
    tasks = []
    for prompt in prompts:
        # Select appropriate generator based on prompt
        if "rate" in prompt.lower():
            generator = generators.get("choice")
        else:
            generator = generate.text(model, max_tokens=50)

        if generator:
            task = asyncio.create_task(generator(prompt))
            tasks.append(task)

    # Wait for all generations to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results

# Usage
model = models.transformers("microsoft/DialoGPT-small")

prompts = [
    "Rate this product:",
    "Describe the weather:",
    "Choose a color:",
    "What's your opinion?"
]

constraints = {
    "choice": ["excellent", "good", "average", "poor"]
}

# Run batch generation
results = await batch_constrained_generation(model, prompts, constraints)

for prompt, result in zip(prompts, results):
    print(f"{prompt} -> {result}")
```

## Next Steps

Now that you understand the basics of constrained generation, let's explore:

- **[Chapter 2: Text Patterns](02-text-patterns.md)** - Regular expressions and string constraints
- **[Chapter 3: JSON Schema](03-json-schema.md)** - Structured data generation with schemas

## Quick Start Checklist

- [ ] Install Outlines and dependencies
- [ ] Load a model with Transformers backend
- [ ] Generate basic constrained choices
- [ ] Experiment with different model backends
- [ ] Implement error handling
- [ ] Try batch processing for performance

You're now ready to add structure and reliability to your LLM outputs! 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `models`, `outlines` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Outlines` as an operating subsystem inside **Outlines Tutorial: Structured Text Generation with LLMs**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `generator`, `generate`, `print` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Outlines` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `models` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `outlines`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/outlines-dev/outlines)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `model` and `models` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Text Patterns & Regular Expressions](02-text-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
