---
layout: default
title: "vLLM Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: vLLM Tutorial
---

# Chapter 1: Getting Started with vLLM

Welcome to **Chapter 1: Getting Started with vLLM**. In this part of **vLLM Tutorial: High-Performance LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Install vLLM, understand its architecture, and run your first high-performance LLM inference.

## Overview

vLLM is a high-performance, memory-efficient inference engine for large language models. This chapter covers installation, basic concepts, and your first experience with vLLM's blazing-fast inference capabilities.

## Installation and Setup

### System Requirements

```bash
# Minimum requirements
- Python 3.8+
- CUDA 11.8+ (for GPU acceleration)
- 16GB RAM (32GB+ recommended)
- NVIDIA GPU with 8GB+ VRAM (A100, V100, RTX 30/40 series)

# Recommended for production
- CUDA 12.0+
- 64GB+ RAM
- NVIDIA A100/H100 or equivalent
- High-speed NVMe storage
```

### Installing vLLM

```bash
# Basic installation
pip install vllm

# GPU acceleration (recommended)
pip install vllm[cuda]

# CPU-only version
pip install vllm[cpu]

# Development version with latest features
pip install git+https://github.com/vllm-project/vllm.git

# Install with additional dependencies
pip install vllm[all]
```

### Verifying Installation

```python
import vllm
print(f"vLLM version: {vllm.__version__}")

# Check available devices
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU count: {torch.cuda.device_count()}")
    print(f"Current GPU: {torch.cuda.get_device_name()}")
```

## Core Concepts

### PagedAttention - The Secret Sauce

vLLM's core innovation is PagedAttention, which manages KV cache in non-contiguous memory blocks:

```python
# Traditional attention (contiguous memory)
# KV cache grows linearly, causes fragmentation
# Memory: [Token1_KV][Token2_KV][Token3_KV]...[TokenN_KV]

# PagedAttention (non-contiguous blocks)
# Memory divided into fixed-size blocks
# KV cache: Block0 -> Block5 -> Block2 -> Block8
# Much more memory efficient and reduces fragmentation
```

### Continuous Batching

Dynamic batching of requests for optimal GPU utilization:

```python
# Traditional batching: Fixed batch size
# Requests wait for full batch, wasted compute

# Continuous batching: Dynamic batching
# New requests added immediately as space becomes available
# Optimal GPU utilization, lower latency
```

## Your First vLLM Inference

### Basic Text Generation

```python
from vllm import LLM, SamplingParams

# Initialize vLLM with a small model
llm = LLM(model="microsoft/DialoGPT-small")

# Configure sampling parameters
sampling_params = SamplingParams(
    temperature=0.8,      # Creativity (0.0 = deterministic, 1.0 = very creative)
    top_p=0.95,          # Nucleus sampling
    max_tokens=50,       # Maximum response length
    stop=["\n"]          # Stop sequences
)

# Generate text
prompts = ["Hello, how are you today?"]
outputs = llm.generate(prompts, sampling_params)

# Print results
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt}")
    print(f"Generated: {generated_text}")
    print(f"Tokens used: {len(output.outputs[0].token_ids)}")
```

### Understanding the Output

```python
# The output object contains detailed information
output = outputs[0]

print(f"Original prompt: {output.prompt}")
print(f"Generated text: {output.outputs[0].text}")
print(f"Full response: {output.prompt + output.outputs[0].text}")

# Token-level information
print(f"Token IDs: {output.outputs[0].token_ids}")
print(f"Log probabilities: {output.outputs[0].logprobs}")

# Performance metrics
print(f"Generation time: {output.metrics.get('generation_time', 'N/A')}")
print(f"Tokens per second: {output.metrics.get('tokens_per_sec', 'N/A')}")

# Cumulative log probability
cumulative_logprob = sum(output.outputs[0].logprobs.values())
print(f"Cumulative log probability: {cumulative_logprob}")
```

## Model Loading Options

### HuggingFace Models

```python
# Load any HuggingFace model
models_to_try = [
    "microsoft/DialoGPT-medium",    # Conversational AI
    "gpt2",                         # General purpose
    "microsoft/DialoGPT-large",     # Larger conversational model
    "distilgpt2"                    # Smaller, faster model
]

for model_name in models_to_try:
    try:
        print(f"\nLoading {model_name}...")
        llm = LLM(model=model_name)
        print(f"✅ Successfully loaded {model_name}")

        # Quick test
        result = llm.generate(["Hello"], SamplingParams(max_tokens=10))
        print(f"Sample output: {result[0].outputs[0].text[:50]}...")

    except Exception as e:
        print(f"❌ Failed to load {model_name}: {e}")
```

### Quantized Models

```python
# Load quantized models for memory efficiency
quantized_models = [
    "TheBloke/Llama-2-7B-Chat-GPTQ",  # GPTQ quantized
    "TheBloke/Llama-2-13B-Chat-GGML", # GGML quantized
]

for model_name in quantized_models:
    try:
        print(f"\nLoading quantized model: {model_name}")
        llm = LLM(
            model=model_name,
            quantization="gptq",  # or "awq", "squeezellm"
            dtype="half"  # Use FP16 for memory efficiency
        )

        # Test generation
        result = llm.generate(
            ["Explain quantum computing in simple terms"],
            SamplingParams(max_tokens=100, temperature=0.7)
        )

        print(f"✅ Generated response: {result[0].outputs[0].text[:100]}...")

    except Exception as e:
        print(f"❌ Failed: {e}")
```

## Advanced Sampling Parameters

### Temperature and Creativity Control

```python
# Different creativity levels
sampling_configs = {
    "deterministic": SamplingParams(
        temperature=0.0,    # No randomness
        top_p=1.0,
        max_tokens=50
    ),
    "focused": SamplingParams(
        temperature=0.3,    # Low creativity, focused responses
        top_p=0.9,
        max_tokens=50
    ),
    "creative": SamplingParams(
        temperature=0.8,    # High creativity
        top_p=0.95,
        max_tokens=50
    ),
    "wild": SamplingParams(
        temperature=1.5,    # Very creative, potentially incoherent
        top_p=0.99,
        max_tokens=50
    )
}

prompt = "Write a short story about a robot learning to paint"

for config_name, params in sampling_configs.items():
    print(f"\n=== {config_name.upper()} ===")

    llm = LLM(model="gpt2")
    result = llm.generate([prompt], params)

    print(f"Temperature: {params.temperature}")
    print(f"Response: {result[0].outputs[0].text}")
```

### Nucleus and Top-K Sampling

```python
# Top-K vs Top-P comparison
comparison_prompts = ["The future of AI is"]

sampling_methods = {
    "greedy": SamplingParams(temperature=0.0, top_k=1),
    "top_k_10": SamplingParams(temperature=0.7, top_k=10),
    "top_k_50": SamplingParams(temperature=0.7, top_k=50),
    "top_p_09": SamplingParams(temperature=0.7, top_p=0.9),
    "top_p_05": SamplingParams(temperature=0.7, top_p=0.5),
}

llm = LLM(model="gpt2-medium")

for method_name, params in sampling_methods.items():
    print(f"\n=== {method_name.upper()} ===")

    results = llm.generate([comparison_prompts[0]] * 3, params)  # Generate 3 samples

    for i, result in enumerate(results):
        print(f"Sample {i+1}: {result.outputs[0].text[:60]}...")
```

### Stop Sequences and Length Control

```python
# Controlling response length and termination
control_examples = {
    "short_response": SamplingParams(
        max_tokens=20,
        stop=[".", "!", "?"],  # Stop at sentence end
        temperature=0.7
    ),
    "long_response": SamplingParams(
        max_tokens=200,
        stop=["END"],  # Custom stop token
        temperature=0.8
    ),
    "code_generation": SamplingParams(
        max_tokens=100,
        stop=["```"],  # Stop at code block end
        temperature=0.1  # Lower temperature for code
    )
}

prompts = [
    "Explain machine learning",
    "Write a Python function to calculate fibonacci numbers",
    "Describe the benefits of renewable energy"
]

llm = LLM(model="microsoft/DialoGPT-medium")

for i, (config_name, params) in enumerate(control_examples.items()):
    print(f"\n=== {config_name.upper()} ===")

    result = llm.generate([prompts[i]], params)
    response = result[0].outputs[0].text

    print(f"Prompt: {prompts[i][:50]}...")
    print(f"Response: {response}")
    print(f"Length: {len(response)} characters")
```

## Batch Processing

### Processing Multiple Prompts

```python
# Batch processing for efficiency
batch_prompts = [
    "What is the capital of France?",
    "Explain photosynthesis in simple terms",
    "Write a haiku about coding",
    "What are the benefits of exercise?",
    "Describe how a computer works"
]

# Single batch call (most efficient)
llm = LLM(model="microsoft/DialoGPT-medium")

sampling_params = SamplingParams(
    temperature=0.7,
    max_tokens=50,
    stop=[".", "!", "?"]
)

print("Processing batch of", len(batch_prompts), "prompts...")

import time
start_time = time.time()

batch_results = llm.generate(batch_prompts, sampling_params)

end_time = time.time()

print(".2f")
print(".2f")

# Process results
for i, result in enumerate(batch_results):
    print(f"\nPrompt {i+1}: {batch_prompts[i]}")
    print(f"Response: {result.outputs[0].text}")
```

### Memory Management

```python
# Managing GPU memory
def create_memory_efficient_llm(model_name, gpu_memory_utilization=0.8):
    """Create LLM with memory constraints"""

    llm = LLM(
        model=model_name,
        gpu_memory_utilization=gpu_memory_utilization,  # Use 80% of GPU memory
        max_model_len=2048,  # Limit context length to save memory
        dtype="half",  # Use FP16 instead of FP32
        enforce_eager=False  # Allow some lazy operations
    )

    return llm

# Test different memory configurations
memory_configs = [
    {"gpu_memory_utilization": 0.5, "max_model_len": 1024},
    {"gpu_memory_utilization": 0.8, "max_model_len": 2048},
    {"gpu_memory_utilization": 0.9, "max_model_len": 4096}
]

for config in memory_configs:
    try:
        print(f"\nTesting config: {config}")
        llm = LLM(model="gpt2", **config)

        # Test generation
        result = llm.generate(
            ["Hello world"] * 5,  # Small batch
            SamplingParams(max_tokens=20)
        )

        print(f"✅ Success - Generated {len(result)} responses")

    except Exception as e:
        print(f"❌ Failed: {e}")
```

## Error Handling and Debugging

### Common Issues and Solutions

```python
def robust_vllm_generation(model_name, prompts, max_retries=3):
    """Robust vLLM generation with error handling"""

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}")

            # Initialize LLM
            llm = LLM(
                model=model_name,
                trust_remote_code=True,  # For custom models
                download_dir="./model_cache"  # Cache models locally
            )

            # Configure sampling
            sampling_params = SamplingParams(
                temperature=0.7,
                max_tokens=100,
                stop=["\n\n"]  # Stop at double newline
            )

            # Generate
            results = llm.generate(prompts, sampling_params)

            print("✅ Generation successful!")
            return results

        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                print("Retrying...")
                continue
            else:
                print("All attempts failed")
                raise e

# Test robust generation
try:
    results = robust_vllm_generation(
        "microsoft/DialoGPT-medium",
        ["Hello, how can I help you?"]
    )

    for result in results:
        print(f"Response: {result.outputs[0].text}")

except Exception as e:
    print(f"Final failure: {e}")
```

### Performance Monitoring

```python
import psutil
import GPUtil

def monitor_vllm_performance(llm, prompts, sampling_params):
    """Monitor system resources during vLLM inference"""

    # Get initial resource usage
    initial_cpu = psutil.cpu_percent()
    initial_memory = psutil.virtual_memory().percent

    try:
        gpus = GPUtil.getGPUs()
        initial_gpu = gpus[0].memoryUsed if gpus else 0
    except:
        initial_gpu = 0

    print("=== Initial Resource Usage ===")
    print(".1f")
    print(".1f")
    if initial_gpu > 0:
        print(".1f")

    # Perform generation
    import time
    start_time = time.time()

    results = llm.generate(prompts, sampling_params)

    end_time = time.time()

    # Get final resource usage
    final_cpu = psutil.cpu_percent()
    final_memory = psutil.virtual_memory().percent

    try:
        gpus = GPUtil.getGPUs()
        final_gpu = gpus[0].memoryUsed if gpus else 0
    except:
        final_gpu = 0

    generation_time = end_time - start_time

    print("\n=== Final Resource Usage ===")
    print(".1f")
    print(".1f")
    if final_gpu > 0:
        print(".1f")

    print("
=== Performance Metrics ===")
    print(".3f")
    print(".2f")
    print(".3f")

    return results

# Monitor performance
llm = LLM(model="gpt2")
prompts = ["Explain quantum computing"] * 5

results = monitor_vllm_performance(
    llm,
    prompts,
    SamplingParams(max_tokens=50, temperature=0.7)
)
```

## Summary

In this chapter, we've covered:

- **Installation and Setup** - Getting vLLM running with proper GPU support
- **Core Architecture** - Understanding PagedAttention and continuous batching
- **Basic Inference** - Your first text generation with vLLM
- **Model Loading** - Working with different model formats and quantization
- **Sampling Parameters** - Controlling creativity, length, and termination
- **Batch Processing** - Efficient processing of multiple prompts
- **Error Handling** - Robust generation with retry logic
- **Performance Monitoring** - Tracking resource usage and throughput

vLLM provides state-of-the-art inference performance while maintaining simplicity of use.

## Key Takeaways

1. **PagedAttention**: Revolutionary memory management for efficient inference
2. **Continuous Batching**: Dynamic batching for optimal GPU utilization
3. **Flexible Sampling**: Fine control over generation parameters
4. **Memory Efficiency**: Support for quantized models and memory optimization
5. **Production Ready**: Robust error handling and performance monitoring

Next, we'll explore **model loading** options - working with different model formats, quantization, and custom models.

---

**Ready for the next chapter?** [Chapter 2: Model Loading](02-model-loading.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `print`, `SamplingParams`, `output` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with vLLM` as an operating subsystem inside **vLLM Tutorial: High-Performance LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `temperature`, `outputs`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with vLLM` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `print`.
2. **Input normalization**: shape incoming data so `SamplingParams` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `output`.
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
- [Next Chapter: Chapter 2: Model Loading and Management](02-model-loading.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
