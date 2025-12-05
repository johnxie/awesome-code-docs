---
layout: default
title: "vLLM Tutorial - Chapter 2: Model Loading"
nav_order: 2
has_children: false
parent: vLLM Tutorial
---

# Chapter 2: Model Loading and Management

> Master loading different model formats, quantization techniques, and efficient model management in vLLM.

## Overview

vLLM supports a wide variety of model formats and loading strategies. This chapter covers loading models from HuggingFace, handling quantization, managing model weights, and optimizing loading performance.

## HuggingFace Model Loading

### Basic HuggingFace Loading

```python
from vllm import LLM

# Load models from HuggingFace Hub
models_to_load = [
    "microsoft/DialoGPT-small",     # 117M parameters
    "microsoft/DialoGPT-medium",    # 345M parameters
    "microsoft/DialoGPT-large",     # 762M parameters
    "gpt2",                         # 124M parameters
    "gpt2-medium",                  # 355M parameters
    "gpt2-large",                   # 774M parameters
    "gpt2-xl",                      # 1.5B parameters
]

for model_name in models_to_load:
    try:
        print(f"\nLoading {model_name}...")
        llm = LLM(model=model_name)

        # Test generation
        result = llm.generate(
            ["Hello, world!"],
            SamplingParams(max_tokens=20)
        )

        print(f"✅ Loaded successfully")
        print(f"Sample: {result[0].outputs[0].text}")

    except Exception as e:
        print(f"❌ Failed to load {model_name}: {e}")
```

### Advanced Loading Options

```python
# Advanced loading with custom options
llm = LLM(
    model="microsoft/DialoGPT-large",
    revision="main",                    # Specific model revision
    trust_remote_code=True,            # Allow custom code execution
    download_dir="./model_cache",      # Local cache directory
    load_format="auto",                # Auto-detect format
    dtype="half",                      # Use FP16 for memory efficiency
    max_model_len=1024,                # Maximum sequence length
    gpu_memory_utilization=0.8,        # GPU memory usage (80%)
    enforce_eager=False,               # Allow lazy loading
    seed=42                            # Reproducible initialization
)

print("Model loaded with custom configuration")
print(f"Max sequence length: {llm.llm_engine.model_config.max_model_len}")
print(f"Dtype: {llm.llm_engine.model_config.dtype}")
```

### Loading from Local Files

```python
import os
from pathlib import Path

# Load model from local directory
local_model_paths = [
    "./models/gpt2",
    "./models/dialogpt-medium",
    "/path/to/custom/model"
]

def load_local_model(model_path):
    """Load model from local path"""

    if not os.path.exists(model_path):
        print(f"Model path {model_path} does not exist")
        return None

    try:
        print(f"Loading model from {model_path}...")

        llm = LLM(
            model=model_path,
            trust_remote_code=True,
            download_dir=None  # Don't download, use local
        )

        # Verify loading
        result = llm.generate(
            ["Test prompt"],
            SamplingParams(max_tokens=10)
        )

        print("✅ Local model loaded successfully")
        return llm

    except Exception as e:
        print(f"❌ Failed to load local model: {e}")
        return None

# Test local loading
for path in local_model_paths:
    llm = load_local_model(path)
    if llm:
        break
```

## Quantization Techniques

### GPTQ Quantization

```python
# GPTQ (Generative Pre-trained Transformer Quantization)
gptq_models = [
    "TheBloke/Llama-2-7B-Chat-GPTQ",
    "TheBloke/Llama-2-13B-Chat-GPTQ",
    "TheBloke/CodeLlama-7B-Instruct-GPTQ",
    "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ"
]

for model_name in gptq_models:
    try:
        print(f"\nLoading GPTQ model: {model_name}")

        llm = LLM(
            model=model_name,
            quantization="gptq",      # Specify quantization method
            dtype="auto",            # Auto-detect appropriate dtype
            gpu_memory_utilization=0.7  # Use less GPU memory
        )

        # Test generation
        result = llm.generate(
            ["Explain quantum computing in simple terms"],
            SamplingParams(
                max_tokens=100,
                temperature=0.7
            )
        )

        print(f"✅ GPTQ model loaded")
        print(f"Response length: {len(result[0].outputs[0].text)} characters")

    except Exception as e:
        print(f"❌ Failed to load GPTQ model: {e}")
```

### AWQ Quantization

```python
# AWQ (Activation-aware Weight Quantization)
awq_models = [
    "TheBloke/Llama-2-7B-Chat-AWQ",
    "TheBloke/Mistral-7B-Instruct-v0.2-AWQ",
    "casperhansen/llama-3-8b-instruct-awq"
]

for model_name in awq_models:
    try:
        print(f"\nLoading AWQ model: {model_name}")

        llm = LLM(
            model=model_name,
            quantization="awq",
            dtype="auto",
            gpu_memory_utilization=0.6  # AWQ is very memory efficient
        )

        # Benchmark performance
        import time
        start_time = time.time()

        result = llm.generate(
            ["Write a Python function to reverse a string"] * 5,  # Batch of 5
            SamplingParams(max_tokens=50)
        )

        end_time = time.time()

        print(f"✅ AWQ model loaded and tested")
        print(".3f")
        print(".2f")

    except Exception as e:
        print(f"❌ Failed to load AWQ model: {e}")
```

### SqueezeLLM Quantization

```python
# SqueezeLLM - Non-uniform quantization
def load_squeezellm_model(model_name):
    """Load model with SqueezeLLM quantization"""

    try:
        llm = LLM(
            model=model_name,
            quantization="squeezellm",  # SqueezeLLM quantization
            dtype="auto",
            gpu_memory_utilization=0.8
        )

        print(f"✅ SqueezeLLM model loaded: {model_name}")
        return llm

    except Exception as e:
        print(f"❌ Failed to load SqueezeLLM model: {e}")
        return None

# Test SqueezeLLM
squeezellm_llm = load_squeezellm_model("TheBloke/Llama-2-7B-Chat-GPTQ")
if squeezellm_llm:
    result = squeezellm_llm.generate(
        ["What is the capital of Japan?"],
        SamplingParams(max_tokens=20)
    )
    print(f"Answer: {result[0].outputs[0].text.strip()}")
```

### Quantization Comparison

```python
import torch

def compare_quantization_methods():
    """Compare different quantization approaches"""

    base_model = "microsoft/DialoGPT-large"
    test_prompt = "Explain machine learning briefly"

    methods = {
        "No Quantization": {
            "quantization": None,
            "gpu_memory_utilization": 0.9
        },
        "GPTQ": {
            "quantization": "gptq",
            "gpu_memory_utilization": 0.7
        },
        "AWQ": {
            "quantization": "awq",
            "gpu_memory_utilization": 0.6
        }
    }

    results = {}

    for method_name, config in methods.items():
        try:
            print(f"\nTesting {method_name}...")

            # Measure memory before loading
            if torch.cuda.is_available():
                torch.cuda.reset_peak_memory_stats()
                memory_before = torch.cuda.memory_allocated() / 1024**3

            llm = LLM(model=base_model, **config)

            # Measure memory after loading
            if torch.cuda.is_available():
                memory_after = torch.cuda.memory_allocated() / 1024**3
                memory_used = memory_after - memory_before
                print(".2f")

            # Test generation performance
            import time
            start_time = time.time()

            result = llm.generate(
                [test_prompt] * 3,  # Small batch
                SamplingParams(max_tokens=50, temperature=0.7)
            )

            end_time = time.time()
            generation_time = end_time - start_time

            print(".3f")
            print(".2f")

            results[method_name] = {
                "success": True,
                "memory_gb": memory_used if torch.cuda.is_available() else None,
                "time_seconds": generation_time,
                "throughput": 3 / generation_time  # prompts per second
            }

        except Exception as e:
            print(f"❌ Failed: {e}")
            results[method_name] = {"success": False, "error": str(e)}

    return results

# Run comparison
comparison_results = compare_quantization_methods()

print("\n=== QUANTIZATION COMPARISON SUMMARY ===")
for method, result in comparison_results.items():
    if result["success"]:
        print(f"{method}:")
        if result.get("memory_gb"):
            print(".2f")
        print(".2f")
        print(".2f")
    else:
        print(f"{method}: Failed - {result.get('error', 'Unknown error')}")
```

## Custom Model Loading

### Loading from Checkpoints

```python
def load_from_checkpoint(checkpoint_path, config_path=None):
    """Load model from training checkpoints"""

    try:
        from transformers import AutoConfig, AutoModelForCausalLM

        # Load config if provided
        if config_path:
            config = AutoConfig.from_pretrained(config_path)
        else:
            config = AutoConfig.from_pretrained(checkpoint_path)

        # Load model weights
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint_path,
            config=config,
            torch_dtype=torch.float16,  # Use FP16 for memory efficiency
            device_map="auto"  # Automatic device placement
        )

        # Create vLLM-compatible model
        # Note: This is a simplified example
        # In practice, you might need to convert the model format

        print("✅ Custom model loaded from checkpoint")
        return model

    except Exception as e:
        print(f"❌ Failed to load from checkpoint: {e}")
        return None

# Example usage (would need actual checkpoint paths)
# custom_model = load_from_checkpoint("./my_model_checkpoint")
```

### Model Conversion and Optimization

```python
def convert_and_optimize_model(original_model_path, output_path):
    """Convert and optimize model for vLLM"""

    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print(f"Converting model: {original_model_path}")

        # Load original model
        model = AutoModelForCausalLM.from_pretrained(
            original_model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        tokenizer = AutoTokenizer.from_pretrained(original_model_path)

        # Apply optimizations
        model.eval()  # Set to evaluation mode

        # Fuse layers if possible (model-specific)
        # This is highly model-dependent and may not apply to all models

        # Save optimized model
        model.save_pretrained(output_path)
        tokenizer.save_pretrained(output_path)

        print(f"✅ Model converted and saved to: {output_path}")

        # Now load with vLLM
        llm = LLM(model=output_path)

        return llm

    except Exception as e:
        print(f"❌ Model conversion failed: {e}")
        return None

# Example conversion (would need actual model paths)
# optimized_llm = convert_and_optimize_model(
#     "microsoft/DialoGPT-medium",
#     "./optimized_models/dialogpt_medium"
# )
```

## Model Management and Caching

### Model Caching Strategies

```python
import os
from pathlib import Path

class ModelCacheManager:
    def __init__(self, cache_dir="./model_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Cache metadata
        self.cache_metadata = self._load_metadata()

    def _load_metadata(self):
        """Load cache metadata"""
        metadata_file = self.cache_dir / "metadata.json"

        if metadata_file.exists():
            import json
            with open(metadata_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def _save_metadata(self):
        """Save cache metadata"""
        metadata_file = self.cache_dir / "metadata.json"
        import json

        with open(metadata_file, 'w') as f:
            json.dump(self.cache_metadata, f, indent=2)

    def is_cached(self, model_name):
        """Check if model is cached"""
        model_dir = self.cache_dir / model_name.replace('/', '_')
        return model_dir.exists() and model_dir.is_dir()

    def cache_model(self, model_name, force_download=False):
        """Cache model locally"""

        if self.is_cached(model_name) and not force_download:
            print(f"Model {model_name} already cached")
            return self.get_cached_path(model_name)

        try:
            print(f"Caching model: {model_name}")

            # Pre-download model (this warms up the cache)
            from transformers import AutoModelForCausalLM, AutoTokenizer

            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                cache_dir=str(self.cache_dir)
            )

            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=str(self.cache_dir)
            )

            # Update metadata
            self.cache_metadata[model_name] = {
                "cached_at": str(datetime.now()),
                "size_mb": self._get_model_size(model_name)
            }

            self._save_metadata()

            print(f"✅ Model cached: {model_name}")
            return self.get_cached_path(model_name)

        except Exception as e:
            print(f"❌ Failed to cache model: {e}")
            return None

    def get_cached_path(self, model_name):
        """Get path to cached model"""
        return str(self.cache_dir / model_name.replace('/', '_'))

    def _get_model_size(self, model_name):
        """Estimate model size in MB"""
        model_dir = self.cache_dir / model_name.replace('/', '_')

        if model_dir.exists():
            total_size = 0
            for file_path in model_dir.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size

            return total_size / (1024 * 1024)  # MB
        return 0

    def list_cached_models(self):
        """List all cached models"""
        cached_models = []

        for model_dir in self.cache_dir.iterdir():
            if model_dir.is_dir() and model_dir.name != "__pycache__":
                model_name = model_dir.name.replace('_', '/')
                metadata = self.cache_metadata.get(model_name, {})

                cached_models.append({
                    "name": model_name,
                    "path": str(model_dir),
                    "cached_at": metadata.get("cached_at", "Unknown"),
                    "size_mb": metadata.get("size_mb", 0)
                })

        return cached_models

    def clear_cache(self, model_name=None):
        """Clear cache for specific model or all models"""
        import shutil

        if model_name:
            model_dir = self.cache_dir / model_name.replace('/', '_')
            if model_dir.exists():
                shutil.rmtree(model_dir)
                print(f"✅ Cleared cache for {model_name}")
        else:
            # Clear all cache
            for model_dir in self.cache_dir.iterdir():
                if model_dir.is_dir() and model_dir.name not in ["__pycache__", "metadata.json"]:
                    shutil.rmtree(model_dir)
            print("✅ Cleared all model cache")

# Usage
cache_manager = ModelCacheManager()

# Cache a model
cached_path = cache_manager.cache_model("microsoft/DialoGPT-medium")

# Load from cache
if cached_path:
    llm = LLM(model=cached_path)

# List cached models
cached_models = cache_manager.list_cached_models()
for model in cached_models:
    print(f"Cached: {model['name']} ({model['size_mb']:.1f} MB)")
```

### Model Version Management

```python
class ModelVersionManager:
    def __init__(self, model_dir="./models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)

    def save_model_version(self, llm, model_name, version="latest", metadata=None):
        """Save model with version information"""

        version_dir = self.model_dir / model_name / version
        version_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Save model configuration
            config_path = version_dir / "config.json"
            with open(config_path, 'w') as f:
                import json
                json.dump({
                    "model_name": model_name,
                    "version": version,
                    "created_at": str(datetime.now()),
                    "metadata": metadata or {},
                    "vllm_config": {
                        "model": llm.llm_engine.model_config.model,
                        "dtype": str(llm.llm_engine.model_config.dtype),
                        "max_model_len": llm.llm_engine.model_config.max_model_len
                    }
                }, f, indent=2)

            print(f"✅ Model version saved: {model_name}/{version}")
            return str(version_dir)

        except Exception as e:
            print(f"❌ Failed to save model version: {e}")
            return None

    def load_model_version(self, model_name, version="latest"):
        """Load specific model version"""

        version_dir = self.model_dir / model_name / version

        if not version_dir.exists():
            print(f"Model version not found: {model_name}/{version}")
            return None

        try:
            config_path = version_dir / "config.json"
            with open(config_path, 'r') as f:
                import json
                config = json.load(f)

            # Load model with saved configuration
            llm = LLM(**config["vllm_config"])

            print(f"✅ Loaded model version: {model_name}/{version}")
            return llm

        except Exception as e:
            print(f"❌ Failed to load model version: {e}")
            return None

    def list_model_versions(self, model_name):
        """List all versions of a model"""

        model_dir = self.model_dir / model_name

        if not model_dir.exists():
            return []

        versions = []
        for version_dir in sorted(model_dir.iterdir()):
            if version_dir.is_dir():
                config_path = version_dir / "config.json"
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        import json
                        config = json.load(f)

                    versions.append({
                        "version": version_dir.name,
                        "created_at": config.get("created_at", "Unknown"),
                        "metadata": config.get("metadata", {})
                    })

        return versions

# Usage
version_manager = ModelVersionManager()

# Save model version
version_path = version_manager.save_model_version(
    llm, "microsoft/DialoGPT-medium", "v1.0",
    metadata={"accuracy": 0.85, "latency": "120ms"}
)

# Load specific version
old_llm = version_manager.load_model_version("microsoft/DialoGPT-medium", "v0.9")

# List versions
versions = version_manager.list_model_versions("microsoft/DialoGPT-medium")
for v in versions:
    print(f"Version: {v['version']} - Created: {v['created_at']}")
```

## Performance Optimization

### Memory Optimization Techniques

```python
def optimize_model_loading(model_name, target_memory_gb=None):
    """Load model with memory optimizations"""

    # Calculate available memory
    if torch.cuda.is_available():
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
        available_memory = total_memory * 0.9  # Leave 10% buffer
    else:
        available_memory = 16  # Assume 16GB for CPU

    target_memory = target_memory_gb or available_memory

    # Choose appropriate configuration
    if target_memory < 8:
        # Very constrained memory
        config = {
            "dtype": "half",  # FP16
            "max_model_len": 512,
            "gpu_memory_utilization": 0.5,
            "quantization": "gptq"
        }
    elif target_memory < 16:
        # Moderate memory
        config = {
            "dtype": "half",
            "max_model_len": 1024,
            "gpu_memory_utilization": 0.7,
            "quantization": "awq"
        }
    else:
        # High memory
        config = {
            "dtype": "auto",
            "max_model_len": 2048,
            "gpu_memory_utilization": 0.9,
            "quantization": None
        }

    print(f"Loading {model_name} with memory optimization...")
    print(f"Target memory: {target_memory:.1f}GB")
    print(f"Configuration: {config}")

    try:
        llm = LLM(model=model_name, **config)

        # Test memory usage
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / (1024**3)
            print(".2f")

        print("✅ Model loaded with optimization")
        return llm

    except Exception as e:
        print(f"❌ Failed to load optimized model: {e}")
        return None

# Test memory optimization
optimized_llm = optimize_model_loading("microsoft/DialoGPT-large")
```

## Summary

In this chapter, we've covered:

- **HuggingFace Loading** - Loading models from the Hub with custom options
- **Local Model Loading** - Working with models stored locally
- **Quantization Techniques** - GPTQ, AWQ, SqueezeLLM for memory efficiency
- **Custom Model Loading** - Loading from checkpoints and custom formats
- **Model Caching** - Efficient model storage and retrieval
- **Version Management** - Tracking and managing model versions
- **Memory Optimization** - Techniques for loading large models efficiently

These techniques enable loading and managing models of various sizes and formats while optimizing for memory usage and performance.

## Key Takeaways

1. **Quantization**: GPTQ, AWQ, and SqueezeLLM reduce memory requirements significantly
2. **Caching**: Local caching improves loading times and reduces network dependency
3. **Version Management**: Track model versions for reproducibility and rollback
4. **Memory Optimization**: Balance model size, precision, and available resources
5. **Flexible Loading**: Support for HuggingFace Hub, local files, and custom formats

Next, we'll explore **basic inference** - text generation, sampling strategies, and parameter tuning.

---

**Ready for the next chapter?** [Chapter 3: Basic Inference](03-basic-inference.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*