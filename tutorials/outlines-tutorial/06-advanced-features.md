---
layout: default
title: "Outlines Tutorial - Chapter 6: Advanced Features & Performance"
nav_order: 6
has_children: false
parent: Outlines Tutorial
---

# Chapter 6: Advanced Features & Performance Optimization

Welcome to **Chapter 6: Advanced Features & Performance Optimization**. In this part of **Outlines Tutorial: Structured Text Generation with LLMs**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master advanced Outlines features - custom sampling, performance tuning, batch processing, and enterprise-grade optimization techniques.

## Advanced Sampling Strategies

### Custom Sampling Algorithms

```python
from outlines import models, generate, samplers
import torch
import numpy as np

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# Custom sampling with temperature control
class AdaptiveTemperatureSampler:
    """Sampler that adapts temperature based on sequence length."""

    def __init__(self, base_temperature: float = 0.7, min_temp: float = 0.1, max_temp: float = 2.0):
        self.base_temperature = base_temperature
        self.min_temp = min_temp
        self.max_temp = max_temp

    def __call__(self, logits: torch.Tensor, sequence_length: int) -> torch.Tensor:
        """Apply adaptive temperature sampling."""

        # Increase temperature for longer sequences to encourage diversity
        # Decrease temperature for shorter sequences for consistency
        length_factor = min(sequence_length / 50, 1.0)  # Normalize by expected length
        temperature = self.base_temperature * (1 + length_factor)

        # Clamp to valid range
        temperature = max(self.min_temp, min(self.max_temp, temperature))

        # Apply temperature
        return logits / temperature

# Use custom sampler
adaptive_sampler = AdaptiveTemperatureSampler()

# Generate with adaptive sampling
text_generator = generate.text(
    model,
    max_tokens=50,
    sampler=adaptive_sampler
)

result = text_generator("Write a creative story about")
print(f"Adaptive sampling result: {result}")
```

### Nucleus Sampling with Constraints

```python
class ConstrainedNucleusSampler:
    """Nucleus sampling that respects constraints."""

    def __init__(self, top_p: float = 0.9, temperature: float = 0.7):
        self.top_p = top_p
        self.temperature = temperature

    def __call__(self, logits: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        """Apply nucleus sampling with optional masking."""

        # Apply temperature
        logits = logits / self.temperature

        # Apply mask if provided (from Outlines constraints)
        if mask is not None:
            logits = torch.where(mask, logits, torch.tensor(float('-inf')))

        # Convert to probabilities
        probs = torch.softmax(logits, dim=-1)

        # Apply nucleus filtering
        sorted_probs, sorted_indices = torch.sort(probs, descending=True)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

        # Find cutoff point
        cutoff_mask = cumulative_probs > self.top_p
        if cutoff_mask.any():
            cutoff_idx = cutoff_mask.float().argmax().item()
            # Keep at least one token
            cutoff_idx = max(1, cutoff_idx)

            # Zero out probabilities beyond cutoff
            sorted_probs[cutoff_idx:] = 0

            # Renormalize
            sorted_probs = sorted_probs / sorted_probs.sum()

        # Reconstruct original order
        final_probs = torch.zeros_like(probs)
        final_probs.scatter_(dim=-1, index=sorted_indices, src=sorted_probs)

        return final_probs

# Use constrained nucleus sampling
nucleus_sampler = ConstrainedNucleusSampler(top_p=0.8, temperature=0.6)

choice_generator = generate.choice(
    model,
    ["red", "blue", "green", "yellow", "purple"],
    sampler=nucleus_sampler
)

colors = [choice_generator("Pick a color for") for _ in range(5)]
print("Constrained nucleus sampling results:", colors)

# Analyze diversity
from collections import Counter
distribution = Counter(colors)
print("Color distribution:", dict(distribution))
```

### Beam Search with Constraints

```python
class ConstrainedBeamSearch:
    """Beam search that respects structural constraints."""

    def __init__(self, beam_width: int = 3, max_steps: int = 50):
        self.beam_width = beam_width
        self.max_steps = max_steps

    def search(self, model, initial_prompt: str, constraint_processor):
        """Perform constrained beam search."""

        # Initialize beams
        beams = [{
            'tokens': model.tokenizer.encode(initial_prompt),
            'score': 0.0,
            'finished': False
        }]

        for step in range(self.max_steps):
            if all(beam['finished'] for beam in beams):
                break

            candidates = []

            for beam in beams:
                if beam['finished']:
                    candidates.append(beam)
                    continue

                # Get next token probabilities
                inputs = torch.tensor([beam['tokens']])
                with torch.no_grad():
                    outputs = model.model(inputs)
                    logits = outputs.logits[0, -1, :]

                # Apply constraints
                mask = constraint_processor.get_mask(model.tokenizer, inputs[0])
                if mask is not None:
                    logits[~mask] = float('-inf')

                # Get top beam_width candidates
                probs = torch.softmax(logits, dim=-1)
                top_probs, top_tokens = torch.topk(probs, self.beam_width)

                for prob, token in zip(top_probs, top_tokens):
                    new_tokens = beam['tokens'] + [token.item()]
                    new_score = beam['score'] + prob.item()

                    # Check if sequence is complete
                    finished = constraint_processor.is_finished(torch.tensor(new_tokens))

                    candidates.append({
                        'tokens': new_tokens,
                        'score': new_score,
                        'finished': finished
                    })

            # Select top beam_width candidates
            candidates.sort(key=lambda x: x['score'], reverse=True)
            beams = candidates[:self.beam_width]

        # Return best beam
        best_beam = max(beams, key=lambda x: x['score'])
        result = model.tokenizer.decode(best_beam['tokens'], skip_special_tokens=True)

        # Remove original prompt
        if result.startswith(initial_prompt):
            result = result[len(initial_prompt):].strip()

        return result

# Usage with beam search
beam_search = ConstrainedBeamSearch(beam_width=2, max_steps=30)

# This would integrate with Outlines constraint processors
# For demonstration, we'll use a simple choice constraint
choice_options = ["The cat", "The dog", "The bird", "The fish"]
# Note: Implementation would need access to internal processors
```

## Performance Optimization Techniques

### Model Quantization

```python
from transformers import BitsAndBytesConfig
import torch

def load_quantized_model(model_name: str):
    """Load model with quantization for better performance."""

    # 4-bit quantization configuration
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )

    # Load model with quantization
    model = models.transformers(
        model_name,
        device_map="auto",
        quantization_config=quantization_config,
        torch_dtype=torch.float16
    )

    return model

def load_8bit_model(model_name: str):
    """Load model with 8-bit quantization."""

    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0  # Lower threshold for more aggressive quantization
    )

    model = models.transformers(
        model_name,
        device_map="auto",
        quantization_config=quantization_config
    )

    return model

# Compare performance
import time

def benchmark_generation(model, prompt: str, iterations: int = 5) -> dict:
    """Benchmark generation performance."""

    generator = generate.text(model, max_tokens=20)

    start_time = time.time()
    results = []

    for _ in range(iterations):
        result = generator(prompt)
        results.append(result)

    end_time = time.time()

    return {
        "total_time": end_time - start_time,
        "avg_time": (end_time - start_time) / iterations,
        "results": results
    }

# Benchmark different configurations
print("Performance comparison:")

# Standard model
standard_model = models.transformers("microsoft/DialoGPT-small")
standard_perf = benchmark_generation(standard_model, "Hello, how are you?")
print(f"Standard: {standard_perf['avg_time']:.3f}s per generation")

# Free memory
del standard_model
torch.cuda.empty_cache()

# Quantized model (if GPU available)
try:
    quantized_model = load_8bit_model("microsoft/DialoGPT-small")
    quantized_perf = benchmark_generation(quantized_model, "Hello, how are you?")
    print(f"8-bit quantized: {quantized_perf['avg_time']:.3f}s per generation")
    print(f"Speedup: {standard_perf['avg_time'] / quantized_perf['avg_time']:.2f}x")

    del quantized_model
    torch.cuda.empty_cache()

except Exception as e:
    print(f"Quantization not available: {e}")
```

### KV Cache Optimization

```python
class KVCachingManager:
    """Manage KV cache for efficient generation."""

    def __init__(self, model):
        self.model = model
        self.kv_cache = {}

    def get_cached_kv(self, prompt_hash: str):
        """Get cached KV states for prompt."""
        return self.kv_cache.get(prompt_hash)

    def store_kv_cache(self, prompt_hash: str, kv_states):
        """Store KV states for prompt."""
        self.kv_cache[prompt_hash] = kv_states

        # Limit cache size
        if len(self.kv_cache) > 100:
            # Remove oldest entry (simple implementation)
            oldest_key = next(iter(self.kv_cache))
            del self.kv_cache[oldest_key]

    def generate_with_cache(self, prompt: str, max_new_tokens: int = 20) -> str:
        """Generate with KV caching."""

        import hashlib
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()

        # Tokenize
        input_ids = self.model.tokenizer.encode(prompt, return_tensors="pt")

        # Check for cached KV
        cached_kv = self.get_cached_kv(prompt_hash)

        generated_ids = input_ids[0]

        with torch.no_grad():
            for _ in range(max_new_tokens):
                # Forward pass
                outputs = self.model.model(generated_ids.unsqueeze(0), past_key_values=cached_kv)

                # Get next token logits
                next_token_logits = outputs.logits[:, -1, :]

                # Sample next token (simplified - greedy)
                next_token = torch.argmax(next_token_logits, dim=-1)

                # Append to sequence
                generated_ids = torch.cat([generated_ids, next_token], dim=-1)

                # Update cache
                cached_kv = outputs.past_key_values

        # Decode result
        result = self.model.tokenizer.decode(generated_ids, skip_special_tokens=True)

        # Cache final KV states
        self.store_kv_cache(prompt_hash, cached_kv)

        # Return only new tokens
        if result.startswith(prompt):
            result = result[len(prompt):].strip()

        return result

# Usage
kv_manager = KVCachingManager(model)

# First generation (will cache)
result1 = kv_manager.generate_with_cache("The weather today is", max_new_tokens=10)
print(f"First generation: {result1}")

# Second generation with same prefix (will use cache)
result2 = kv_manager.generate_with_cache("The weather today is", max_new_tokens=10)
print(f"Cached generation: {result2}")
```

## Batch Processing & Parallelization

### Concurrent Generation

```python
import asyncio
from typing import List, Dict, Any
import concurrent.futures

class BatchGenerator:
    """Handle batch generation with constraints."""

    def __init__(self, model, max_concurrent: int = 4):
        self.model = model
        self.max_concurrent = max_concurrent
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent)

    def generate_batch_text(self, prompts: List[str], max_tokens: int = 50) -> List[str]:
        """Generate text for multiple prompts."""

        generator = generate.text(self.model, max_tokens=max_tokens)

        # Use ThreadPoolExecutor for parallelism
        futures = [
            self.executor.submit(generator, prompt)
            for prompt in prompts
        ]

        # Collect results
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(f"Error: {e}")

        # Maintain order
        ordered_results = [None] * len(prompts)
        completed_futures = list(concurrent.futures.as_completed(futures))

        for i, future in enumerate(futures):
            for j, completed in enumerate(completed_futures):
                if completed == future:
                    ordered_results[i] = future.result()
                    break

        return ordered_results

    def generate_batch_structured(self, prompts: List[str], schema: dict) -> List[Dict[str, Any]]:
        """Generate structured data for multiple prompts."""

        json_generator = generate.json(self.model, schema)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [executor.submit(json_generator, prompt) for prompt in prompts]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        return results

    def generate_batch_choices(self, prompts: List[str], choices: List[str]) -> List[str]:
        """Generate choices for multiple prompts."""

        choice_generator = generate.choice(self.model, choices)

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [executor.submit(choice_generator, prompt) for prompt in prompts]

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(f"Error: {e}")

        return results

# Usage
batch_gen = BatchGenerator(model, max_concurrent=2)

# Batch text generation
prompts = [
    "Write a haiku about coding",
    "Explain quantum computing simply",
    "Describe your favorite programming language"
]

text_results = batch_gen.generate_batch_text(prompts, max_tokens=30)
print("Batch text generation:")
for prompt, result in zip(prompts, text_results):
    print(f"Prompt: {prompt}")
    print(f"Result: {result[:50]}...")
    print("-" * 50)

# Batch structured generation
person_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name"]
}

person_prompts = ["Generate person 1", "Generate person 2", "Generate person 3"]
person_results = batch_gen.generate_batch_structured(person_prompts, person_schema)

print("Batch structured generation:")
for prompt, person in zip(person_prompts, person_results):
    print(f"{prompt}: {person}")
```

### Async Generation with Constraints

```python
import asyncio
import aiohttp
from typing import List, Dict, Any

class AsyncBatchGenerator:
    """Async batch generation for high-throughput scenarios."""

    def __init__(self, model, semaphore_limit: int = 5):
        self.model = model
        self.semaphore = asyncio.Semaphore(semaphore_limit)

    async def generate_batch_async(self, prompts: List[str], constraint_type: str,
                                 constraint_config: Any) -> List[Any]:
        """Generate batch with async processing."""

        async def generate_single(prompt: str):
            async with self.semaphore:
                # Simulate async generation (in practice, use async model)
                await asyncio.sleep(0.01)  # Small delay for concurrency demo

                if constraint_type == "text":
                    generator = generate.text(self.model, **constraint_config)
                elif constraint_type == "choice":
                    generator = generate.choice(self.model, constraint_config)
                elif constraint_type == "json":
                    generator = generate.json(self.model, constraint_config)
                else:
                    raise ValueError(f"Unknown constraint type: {constraint_type}")

                return generator(prompt)

        # Generate all concurrently
        tasks = [generate_single(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(f"Error: {result}")
            else:
                processed_results.append(result)

        return processed_results

# Usage
async_batch_gen = AsyncBatchGenerator(model)

# Async batch generation
async def run_async_batch():
    prompts = [f"Generate item {i}" for i in range(10)]

    results = await async_batch_gen.generate_batch_async(
        prompts,
        constraint_type="choice",
        constraint_config=["red", "blue", "green"]
    )

    print("Async batch results:")
    for prompt, result in zip(prompts, results):
        print(f"{prompt}: {result}")

# Run async batch
await run_async_batch()
```

## Memory Management & Optimization

### Gradient Checkpointing

```python
class MemoryOptimizedGenerator:
    """Generator with memory optimization techniques."""

    def __init__(self, model, enable_checkpointing: bool = True):
        self.model = model
        self.enable_checkpointing = enable_checkpointing

        if enable_checkpointing:
            # Enable gradient checkpointing for memory efficiency
            self.model.model.gradient_checkpointing_enable()

    def generate_efficient(self, prompt: str, max_tokens: int = 50, use_cache: bool = True) -> str:
        """Generate with memory optimizations."""

        # Clear cache before generation
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # Use smaller batch size
        input_ids = self.model.tokenizer.encode(prompt, return_tensors="pt")

        # Generate with memory-efficient settings
        with torch.no_grad():
            # Use autocast for mixed precision if available
            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                outputs = self.model.model.generate(
                    input_ids,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.model.tokenizer.eos_token_id,
                    use_cache=use_cache,
                    # Memory optimization settings
                    num_beams=1,  # Greedy decoding uses less memory
                    early_stopping=False,
                )

        result = self.model.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove original prompt
        if result.startswith(prompt):
            result = result[len(prompt):].strip()

        return result

# Usage
memory_gen = MemoryOptimizedGenerator(model)

# Monitor memory usage
def get_memory_usage():
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / 1024**2  # MB
    return 0

print(f"Memory before generation: {get_memory_usage():.1f} MB")

result = memory_gen.generate_efficient("Write a short story about", max_tokens=100)

print(f"Memory after generation: {get_memory_usage():.1f} MB")
print(f"Generated: {result}")
```

### Model Sharding

```python
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

class ShardedModelManager:
    """Manage model sharding for large models."""

    def __init__(self, model_name: str, device_map: str = "auto"):
        self.model_name = model_name
        self.device_map = device_map
        self.model = None

    def load_sharded_model(self):
        """Load model with sharding across devices."""

        print("Loading sharded model...")

        # Initialize empty model
        with init_empty_weights():
            from transformers import AutoModelForCausalLM, AutoTokenizer
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # Load with device mapping
        model = load_checkpoint_and_dispatch(
            model,
            self.model_name,
            device_map=self.device_map,
            no_split_module_classes=["GPTJBlock"]  # Adjust based on model
        )

        self.model = models.transformers(model, tokenizer)
        print("Sharded model loaded successfully")

        return self.model

    def get_generation_stats(self) -> dict:
        """Get memory and device usage statistics."""

        stats = {
            "devices": [],
            "total_memory": 0
        }

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                device_stats = {
                    "device": i,
                    "name": torch.cuda.get_device_name(i),
                    "memory_allocated": torch.cuda.memory_allocated(i) / 1024**3,  # GB
                    "memory_reserved": torch.cuda.memory_reserved(i) / 1024**3     # GB
                }
                stats["devices"].append(device_stats)
                stats["total_memory"] += device_stats["memory_allocated"]

        return stats

# Usage (requires accelerate library)
# sharded_manager = ShardedModelManager("microsoft/DialoGPT-large")
# sharded_model = sharded_manager.load_sharded_model()
#
# stats = sharded_manager.get_generation_stats()
# print("Sharding stats:", stats)
```

## Enterprise Integration Features

### Metrics and Monitoring

```python
from prometheus_client import Counter, Histogram, Gauge
import time

class GenerationMetrics:
    """Comprehensive metrics for generation operations."""

    def __init__(self):
        # Request metrics
        self.generation_requests = Counter(
            'outlines_generation_requests_total',
            'Total generation requests',
            ['constraint_type', 'model_name']
        )

        self.generation_duration = Histogram(
            'outlines_generation_duration_seconds',
            'Generation duration in seconds',
            ['constraint_type', 'model_name']
        )

        self.generation_errors = Counter(
            'outlines_generation_errors_total',
            'Total generation errors',
            ['constraint_type', 'error_type']
        )

        # Resource metrics
        self.active_generations = Gauge(
            'outlines_active_generations',
            'Number of active generations'
        )

        self.memory_usage = Gauge(
            'outlines_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.gpu_memory_usage = Gauge(
            'outlines_gpu_memory_usage_bytes',
            'GPU memory usage in bytes'
        )

    def track_generation(self, constraint_type: str, model_name: str, duration: float, success: bool):
        """Track generation metrics."""

        self.generation_requests.labels(constraint_type, model_name).inc()
        self.generation_duration.labels(constraint_type, model_name).observe(duration)

        if not success:
            self.generation_errors.labels(constraint_type, "generation_failed").inc()

    def update_resource_metrics(self):
        """Update resource usage metrics."""

        # Memory usage
        import psutil
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)

        # GPU memory
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.memory_allocated()
            self.gpu_memory_usage.set(gpu_memory)

    def get_metrics_text(self) -> str:
        """Get metrics in Prometheus format."""
        from prometheus_client import generate_latest
        return generate_latest().decode('utf-8')

# Usage
metrics = GenerationMetrics()

class MonitoredGenerator:
    """Generator with built-in monitoring."""

    def __init__(self, model, constraint_type: str, metrics: GenerationMetrics):
        self.model = model
        self.constraint_type = constraint_type
        self.metrics = metrics

        # Create generator based on type
        if constraint_type == "text":
            self.generator = generate.text(model)
        elif constraint_type == "choice":
            self.generator = generate.choice(model, ["option1", "option2"])  # Would be parameterized
        else:
            self.generator = generate.text(model)

    def generate(self, prompt: str, **kwargs):
        """Generate with monitoring."""

        start_time = time.time()
        self.metrics.active_generations.inc()
        self.metrics.update_resource_metrics()

        try:
            result = self.generator(prompt, **kwargs)
            duration = time.time() - start_time

            self.metrics.track_generation(
                self.constraint_type,
                "DialoGPT-small",  # Would be dynamic
                duration,
                True
            )

            return result

        except Exception as e:
            duration = time.time() - start_time
            self.metrics.track_generation(
                self.constraint_type,
                "DialoGPT-small",
                duration,
                False
            )
            raise e

        finally:
            self.metrics.active_generations.dec()

# Usage
monitored_gen = MonitoredGenerator(model, "text", metrics)
result = monitored_gen.generate("Hello, world!")

print("Generated result:", result)
print("Metrics sample:")
print(metrics.get_metrics_text()[:500] + "...")
```

This advanced features chapter demonstrates sophisticated sampling strategies, performance optimizations, batch processing, and enterprise-grade monitoring capabilities that make Outlines suitable for production deployment. The next chapter covers integration with popular frameworks. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `model`, `result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Advanced Features & Performance Optimization` as an operating subsystem inside **Outlines Tutorial: Structured Text Generation with LLMs**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `torch`, `prompt`, `print` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Advanced Features & Performance Optimization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/outlines-dev/outlines)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Grammar-Based Generation & Context-Free Grammars](05-grammar-based.md)
- [Next Chapter: Chapter 7: Integration with AI Frameworks](07-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
