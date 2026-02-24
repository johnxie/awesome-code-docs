---
layout: default
title: "llama.cpp Tutorial - Chapter 2: Model Formats"
nav_order: 2
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 2: Model Formats and GGUF

Welcome to **Chapter 2: Model Formats and GGUF**. In this part of **llama.cpp Tutorial: Local LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understand GGUF format, quantization levels, and how to choose the right model for your hardware.

## Overview

llama.cpp uses the GGUF format for models. This chapter explains what GGUF is, different quantization options, and how to select models that fit your hardware constraints.

## What is GGUF?

GGUF (GPT-Generated Unified Format) is the successor to GGML format, designed specifically for llama.cpp. It contains:

- **Model weights** in optimized format
- **Metadata** about architecture, vocabulary, and quantization
- **Tokenizer information** for text encoding/decoding
- **Hyperparameters** like context length, embedding size

### GGUF vs Other Formats

| Format | Pros | Cons | Use Case |
|--------|------|------|----------|
| GGUF | Optimized for llama.cpp, fast loading | llama.cpp only | Production inference |
| GGML | Legacy format | Slower, deprecated | Migration only |
| PyTorch | Flexible, easy conversion | Large files, slow inference | Development/training |
| SafeTensors | Safe loading, multi-platform | Requires conversion | Model storage |

## Quantization Explained

Quantization reduces model precision to save memory and improve speed:

### Quantization Levels

| Type | Bits | Memory | Speed | Quality |
|------|------|--------|-------|---------|
| F32 | 32 | 100% | Slowest | Best |
| F16 | 16 | 50% | Slow | Very Good |
| Q8_0 | 8 | 50% | Good | Excellent |
| Q6_K | 6 | 37.5% | Fast | Very Good |
| Q5_K | 5 | 31.25% | Faster | Good |
| Q4_K | 4 | 25% | Fast | Good |
| Q3_K | 3 | 18.75% | Very Fast | Acceptable |
| Q2_K | 2 | 12.5% | Fastest | Basic |

### Understanding K-Quants

K-quantization uses advanced techniques:

- **Q4_K**: Balances quality and speed, recommended for most use
- **Q5_K**: Better quality, slightly slower than Q4_K
- **Q6_K**: High quality, good for creative tasks
- **Q8_0**: Maximum quality, minimal compression

## Memory Requirements

Calculate VRAM/RAM needed:

```python
def calculate_memory_gb(parameters, quantization, context_length=2048):
    """Estimate memory requirements in GB."""

    # Base calculation (rough approximation)
    if quantization == "F16":
        bytes_per_param = 2
    elif quantization == "Q8_0":
        bytes_per_param = 1
    elif quantization == "Q6_K":
        bytes_per_param = 0.75
    elif quantization == "Q5_K":
        bytes_per_param = 0.625
    elif quantization == "Q4_K":
        bytes_per_param = 0.5
    elif quantization == "Q3_K":
        bytes_per_param = 0.375
    elif quantization == "Q2_K":
        bytes_per_param = 0.25
    else:
        bytes_per_param = 2  # Default F16

    # Model weights
    model_memory = (parameters * bytes_per_param) / (1024**3)

    # KV cache (context)
    kv_memory = (parameters * 2 * context_length * bytes_per_param) / (1024**3)

    # Overhead
    overhead = 0.5  # GB

    return model_memory + kv_memory + overhead

# Examples
print(f"Llama-2-7B Q4_K: {calculate_memory_gb(7e9, 'Q4_K'):.1f} GB")
print(f"Llama-2-13B Q4_K: {calculate_memory_gb(13e9, 'Q4_K'):.1f} GB")
print(f"Llama-2-70B Q4_K: {calculate_memory_gb(70e9, 'Q4_K'):.1f} GB")
```

Typical memory requirements:
- **7B model, Q4_K**: ~4-5 GB
- **13B model, Q4_K**: ~8-9 GB
- **30B model, Q4_K**: ~18-20 GB

## Choosing the Right Model

### Hardware-Based Selection

```python
def recommend_quantization(ram_gb, has_gpu=False, gpu_vram_gb=None):
    """Recommend quantization based on hardware."""

    if has_gpu and gpu_vram_gb:
        available_memory = gpu_vram_gb
    else:
        available_memory = ram_gb

    if available_memory >= 24:
        return "Q4_K"  # Best quality
    elif available_memory >= 16:
        return "Q5_K"  # Good balance
    elif available_memory >= 12:
        return "Q6_K"  # Quality over speed
    elif available_memory >= 8:
        return "Q8_0"  # Maximum quality
    elif available_memory >= 6:
        return "Q3_K"  # Acceptable quality
    else:
        return "Q2_K"  # Basic functionality

# Usage
ram_gb = 16
quant = recommend_quantization(ram_gb)
print(f"With {ram_gb}GB RAM, use {quant} quantization")
```

### Use Case-Based Selection

| Use Case | Recommended Quant | Model Size | Notes |
|----------|-------------------|------------|-------|
| Code completion | Q4_K - Q6_K | 7B - 13B | Quality matters |
| Chat/conversation | Q4_K | 7B - 13B | Balance speed/quality |
| Creative writing | Q5_K - Q6_K | 13B+ | Higher quality helps |
| Simple Q&A | Q3_K - Q4_K | 7B | Speed prioritized |
| Analysis/research | Q4_K - Q5_K | 13B+ | Complex reasoning |

## Popular GGUF Models

### Llama 2 Series

```bash
# Download Llama 2 models (requires license agreement)
# Visit: https://huggingface.co/meta-llama

# 7B Chat Model
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# 13B Chat Model
wget https://huggingface.co/TheBloke/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.Q4_K_M.gguf
```

### Mistral Series

```bash
# Mistral 7B Instruct (excellent quality/speed balance)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf

# Mixtral 8x7B (MoE model, high quality)
wget https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf
```

### Code Models

```bash
# CodeLlama 7B Instruct
wget https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf

# DeepSeek Coder 6.7B
wget https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF/resolve/main/deepseek-coder-6.7b-instruct.Q4_K_M.gguf
```

### Small/Fast Models

```bash
# Phi-2 (2.7B parameters, great quality for size)
wget https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf

# TinyLlama 1.1B (very fast, basic quality)
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

## Inspecting GGUF Files

Check model information:

```bash
# Use llama.cpp to inspect model
./llama-cli -m model.gguf --verbose-prompt --prompt ""

# Or use Python script
python3 -c "
import sys
sys.path.insert(0, '.')
from llama_cpp import Llama
model = Llama('model.gguf', verbose=False)
print('Model info:')
print(f'  Vocab size: {model.n_vocab()}')
print(f'  Context length: {model.n_ctx()}')
print(f'  Embedding size: {model.n_embd()}')
print(f'  Layers: {model.n_layer()}')
"
```

## Converting Models to GGUF

Convert from PyTorch/SafeTensors (covered in Chapter 6):

```bash
# Basic conversion (simplified)
python convert.py model_path \
    --outfile model.gguf \
    --outtype f16  # Convert to F16 first

# Then quantize
./llama-quantize model.gguf model-Q4_K.gguf Q4_K
```

## Model Storage and Organization

Organize your model collection:

```bash
# Create organized structure
mkdir -p models/{llama,mistral,code,small}

# Download with descriptive names
cd models/llama
wget -O llama-2-7b-chat-Q4_K.gguf \
    https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Create inventory
find models -name "*.gguf" -exec ls -lh {} \; | \
    awk '{print $5, $9}' > model_inventory.txt
```

## Model Testing and Validation

Test model quality:

```bash
#!/bin/bash
# test_models.sh

MODELS=("models/small/phi-2-Q4_K.gguf" "models/llama/llama-2-7b-chat-Q4_K.gguf")
TEST_PROMPT="Explain quantum computing in one sentence."

for model in "${MODELS[@]}"; do
    if [ -f "$model" ]; then
        echo "Testing $model..."
        timeout 30s ./llama-cli -m "$model" \
            --prompt "$TEST_PROMPT" \
            --n-predict 50 \
            --temp 0.1 \
            --seed 42  # Deterministic output
        echo "---"
    fi
done
```

## Performance Comparison

Benchmark different quantizations:

```bash
#!/bin/bash
# benchmark_quantizations.sh

MODEL_BASE="llama-2-7b-chat"
QUANTS=("Q2_K" "Q3_K" "Q4_K" "Q5_K" "Q6_K")

echo "Quantization | Memory | Tokens/sec | Quality"
echo "-------------|--------|------------|--------"

for quant in "${QUANTS[@]}"; do
    model_file="${MODEL_BASE}.${quant}.gguf"

    if [ -f "$model_file" ]; then
        # Quick benchmark
        result=$(./llama-bench -m "$model_file" -p 10 -n 64 -t 4 2>/dev/null | \
                 grep "tokens/sec" | head -1)

        if [ ! -z "$result" ]; then
            tokens_sec=$(echo $result | grep -o "[0-9.]* tokens/sec")
            memory=$(ls -lh "$model_file" | awk '{print $5}')
            echo "$quant | $memory | $tokens_sec | TBD"
        fi
    fi
done
```

## Best Practices

1. **Match Hardware to Needs**: Choose quantization based on your RAM/VRAM
2. **Test Quality**: Always test model outputs for your specific use case
3. **Monitor Performance**: Track tokens/second and memory usage
4. **Update Models**: Newer GGUF conversions often have better quality
5. **Backup Models**: Keep multiple quantizations for different scenarios
6. **Version Control**: Track which model versions work best for your use cases

## Troubleshooting Model Issues

### Common Problems

**Model won't load:**
```
# Check file path and permissions
ls -la model.gguf

# Verify GGUF format
file model.gguf  # Should show "GGUF" format
```

**Poor quality output:**
```
# Try higher quantization
# Increase temperature/top_p for creativity
# Use models specifically fine-tuned for your task
```

**Slow inference:**
```
# Use lower quantization (Q2_K, Q3_K)
# Reduce context size
# Enable GPU acceleration (Chapter 5)
# Use smaller models
```

Next: Master the command-line interface with advanced options and interactive modes.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `gguf`, `model`, `llama` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Model Formats and GGUF` as an operating subsystem inside **llama.cpp Tutorial: Local LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Q4_K`, `quantization`, `print` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Model Formats and GGUF` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `gguf`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `llama`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ggerganov/llama.cpp)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `gguf` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with llama.cpp](01-getting-started.md)
- [Next Chapter: Chapter 3: Command Line Interface](03-cli-usage.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
