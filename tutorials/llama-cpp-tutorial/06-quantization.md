---
layout: default
title: "llama.cpp Tutorial - Chapter 6: Quantization"
nav_order: 6
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 6: Quantization

Welcome to **Chapter 6: Quantization**. In this part of **llama.cpp Tutorial: Local LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Convert and quantize models to reduce memory usage while maintaining quality.

## Overview

Quantization reduces model precision to save memory and improve speed. This chapter covers converting PyTorch models to GGUF and applying different quantization schemes.

## Understanding Quantization

### Why Quantize?

- **Memory Reduction**: 50-87% less RAM/VRAM required
- **Speed Improvement**: Faster inference due to smaller data types
- **Broader Compatibility**: Run larger models on limited hardware
- **Cost Efficiency**: Lower hardware requirements

### Quantization Types

| Type | Bits/Weight | Memory | Quality | Speed |
|------|-------------|--------|---------|-------|
| F32 | 32 | 100% | Excellent | Slowest |
| F16 | 16 | 50% | Very Good | Slow |
| Q8_0 | 8 | 50% | Very Good | Good |
| Q6_K | 6 | 37.5% | Good | Fast |
| Q5_K | 5 | 31.25% | Good | Faster |
| Q4_K | 4 | 25% | Good | Fast |
| Q3_K | 3 | 18.75% | Acceptable | Very Fast |
| Q2_K | 2 | 12.5% | Basic | Fastest |

## Converting to GGUF

### From PyTorch/HuggingFace

```bash
# Install conversion dependencies
pip install torch transformers sentencepiece protobuf

# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Convert PyTorch model to GGUF (FP16 first)
python convert.py /path/to/pytorch/model \
    --outfile model.gguf \
    --outtype f16

# Quantize to different formats
./llama-quantize model.gguf model-Q4_K.gguf Q4_K
./llama-quantize model.gguf model-Q5_K.gguf Q5_K
./llama-quantize model.gguf model-Q8_0.gguf Q8_0
```

### Supported Model Architectures

llama.cpp supports conversion from:

- **Llama**: Llama 2, Llama 3, Code Llama, Llama Guard
- **Mistral**: Mistral 7B, Mixtral 8x7B, Mistral Large
- **Phi**: Phi-2, Phi-3
- **Qwen**: Qwen 1.5, Qwen 2
- **Gemma**: Google's Gemma models
- **Other**: Falcon, GPT-2, GPT-J, many more

### Batch Conversion Script

```bash
#!/bin/bash
# convert_and_quantize.sh

model_dir="$1"
output_dir="${2:-quantized_models}"

mkdir -p "$output_dir"

# Convert to GGUF (F16)
echo "Converting to GGUF (F16)..."
python convert.py "$model_dir" \
    --outfile "$output_dir/model.gguf" \
    --outtype f16

# Generate multiple quantizations
quantizations=("Q2_K" "Q3_K" "Q4_K" "Q5_K" "Q6_K" "Q8_0")

for quant in "${quantizations[@]}"; do
    echo "Quantizing to $quant..."
    ./llama-quantize "$output_dir/model.gguf" \
        "$output_dir/model-$quant.gguf" \
        "$quant"
done

echo "Conversion complete!"
ls -lh "$output_dir/"
```

## Advanced Quantization

### K-Quantization Options

```bash
# High quality quantization (best for 13B+ models)
./llama-quantize model.gguf model-Q5_K_M.gguf Q5_K_M

# Balanced quality/speed (recommended for most cases)
./llama-quantize model.gguf model-Q4_K_M.gguf Q4_K_M

# Size optimized (minimal quality loss)
./llama-quantize model.gguf model-Q3_K_L.gguf Q3_K_L

# Ultra compressed (significant quality loss)
./llama-quantize model.gguf model-Q2_K.gguf Q2_K
```

### Custom Quantization

```python
# Python quantization (experimental)
import gguf
from llama_cpp import Llama

# Load model
model = Llama("model.gguf", verbose=False)

# Apply custom quantization
# (Advanced usage - requires deep understanding)
```

## Quality Assessment

### Comparative Testing

```bash
#!/bin/bash
# compare_quantizations.sh

model_base="llama-2-7b-chat"
quantizations=("Q2_K" "Q3_K" "Q4_K" "Q5_K" "Q8_0")
test_prompt="Explain the concept of recursion in programming."

echo "Quantization | File Size | Tokens/sec | Quality Score"
echo "-------------|-----------|------------|--------------"

for quant in "${quantizations[@]}"; do
    model_file="${model_base}-${quant}.gguf"

    if [ -f "$model_file" ]; then
        # Get file size
        size=$(ls -lh "$model_file" | awk '{print $5}')

        # Quick benchmark
        tokens_sec=$(./llama-bench -m "$model_file" -p 5 -n 64 -t 4 2>/dev/null | \
                    grep "tokens/sec" | head -1 | grep -o "[0-9.]*")

        # Generate sample output for quality assessment
        output=$(./llama-cli -m "$model_file" \
                 --prompt "$test_prompt" \
                 --n-predict 100 \
                 --temp 0.1 \
                 --seed 42 \
                 --simple-io 2>/dev/null)

        # Simple quality score (word count as proxy)
        quality=$(echo "$output" | wc -w)

        echo "$quant | $size | ${tokens_sec:-N/A} | $quality"
    fi
done
```

### Perplexity Testing

```bash
# Calculate perplexity (measure of model quality)
./llama-perplexity -m model-Q4_K.gguf \
    --ctx-size 4096 \
    --batch-size 512 \
    --ubatch-size 512 \
    --chunks 100 \
    -f wiki.test.raw

# Compare perplexity across quantizations
# Lower perplexity = better quality
```

## Model Merging and LoRA

### Merge Quantized Models

```bash
# Merge base model with LoRA adapter
./llama-export-lora \
    --model-base model.gguf \
    --model-out model-merged.gguf \
    --lora-scaled model-lora.gguf 1.0

# Quantize merged model
./llama-quantize model-merged.gguf model-merged-Q4_K.gguf Q4_K
```

## Hardware-Specific Optimization

### CPU Optimization

```bash
# Quantize with CPU instruction set in mind
./llama-quantize model.gguf model-CPU.gguf Q4_K

# Test with different CPU features
./llama-cli -m model-CPU.gguf --prompt "Hello" --threads $(nproc)
```

### GPU Optimization

```bash
# GPU-friendly quantization
./llama-quantize model.gguf model-GPU.gguf Q4_K

# Test GPU performance
./llama-cli -m model-GPU.gguf --gpu-layers 35 --prompt "Hello"
```

## Converting Popular Models

### Llama 2/3 Models

```bash
# Download from HuggingFace (requires token)
huggingface-cli download meta-llama/Llama-2-7b-chat-hf \
    --local-dir llama-2-7b-chat

# Convert to GGUF
python convert.py llama-2-7b-chat \
    --outfile llama-2-7b-chat.gguf \
    --outtype f16

# Quantize
./llama-quantize llama-2-7b-chat.gguf llama-2-7b-chat-Q4_K.gguf Q4_K
```

### Mistral Models

```bash
# Mistral 7B
python convert.py mistral-7b-instruct \
    --outfile mistral-7b.gguf \
    --outtype f16

./llama-quantize mistral-7b.gguf mistral-7b-Q4_K.gguf Q4_K
```

### CodeLlama

```bash
# CodeLlama conversion
python convert.py CodeLlama-7b-Instruct-hf \
    --outfile codellama-7b.gguf \
    --outtype f16

./llama-quantize codellama-7b.gguf codellama-7b-Q4_K.gguf Q4_K
```

## Quantization Best Practices

### Quality Preservation

1. **Start with F16**: Always convert to F16 first, then quantize
2. **Test Quality**: Compare outputs across quantization levels
3. **Use Q4_K**: Best balance of quality/speed for most use cases
4. **Avoid Q2_K**: Significant quality loss for general use
5. **Fine-tune Threshold**: Test your specific use case at each level

### Memory Optimization

```python
def optimize_quantization_for_hardware(ram_gb, use_case):
    """Recommend quantization based on hardware and use case."""

    recommendations = {
        "chat": {
            4: "Q2_K",      # Very limited RAM
            8: "Q3_K",      # Basic chat
            16: "Q4_K",     # Good chat quality
            24: "Q5_K",     # High quality chat
            32: "Q6_K"      # Maximum quality
        },
        "code": {
            4: "Q3_K",      # Basic code completion
            8: "Q4_K",      # Good code quality
            16: "Q5_K",     # Excellent code quality
            24: "Q6_K",     # Maximum code quality
            32: "Q8_0"
        },
        "creative": {
            4: "Q3_K",      # Basic creative writing
            8: "Q4_K",      # Good creative quality
            16: "Q5_K",     # High creative quality
            24: "Q6_K",     # Excellent creative quality
            32: "Q8_0"
        }
    }

    # Find closest RAM match
    ram_options = sorted(recommendations[use_case].keys())
    closest_ram = min(ram_options, key=lambda x: abs(x - ram_gb))

    return recommendations[use_case][closest_ram]

# Usage
ram_gb = 16
use_case = "chat"  # "chat", "code", or "creative"
recommended_quant = optimize_quantization_for_hardware(ram_gb, use_case)
print(f"Recommended quantization: {recommended_quant}")
```

### Performance Optimization

```bash
# Fast inference quantization
./llama-quantize model.gguf model-fast.gguf Q4_K_S  # Small Q4_K

# Balanced quantization
./llama-quantize model.gguf model-balanced.gguf Q4_K_M  # Medium Q4_K

# Quality-focused quantization
./llama-quantize model.gguf model-quality.gguf Q5_K_M  # Medium Q5_K
```

## Troubleshooting Quantization

### Common Issues

**Conversion fails:**
```bash
# Check model compatibility
python convert.py --help

# Try different output types
python convert.py model --outfile model.gguf --outtype f32

# Check model architecture
python -c "from transformers import AutoConfig; print(AutoConfig.from_pretrained('model'))"
```

**Quantization errors:**
```bash
# Ensure input is F16 GGUF
./llama-cli -m model.gguf --verbose-prompt  # Check format

# Try different quantization methods
./llama-quantize model.gguf output.gguf Q4_0  # Alternative Q4
```

**Quality loss too high:**
```bash
# Use higher quantization
./llama-quantize model.gguf model-Q5_K.gguf Q5_K

# Test different K-types
./llama-quantize model.gguf model-Q4_K_S.gguf Q4_K_S  # Small
./llama-quantize model.gguf model-Q4_K_M.gguf Q4_K_M  # Medium
./llama-quantize model.gguf model-Q4_K_L.gguf Q4_K_L  # Large
```

## Advanced Techniques

### Imatrix Quantization

```bash
# Create importance matrix for better quantization
./llama-imatrix \
    -m model.gguf \
    -f calibration-dataset.txt \
    -o imatrix.dat

# Use imatrix for quantization
./llama-quantize \
    --imatrix imatrix.dat \
    model.gguf \
    model-imatrix-Q4_K.gguf \
    Q4_K
```

### Model Calibration

```bash
# Prepare calibration data
./llama-cli -m model.gguf \
    --file calibration-texts.txt \
    --export-imatrix imatrix.dat \
    --n-predict 0
```

## Automation Scripts

### Complete Pipeline

```bash
#!/bin/bash
# full_quantization_pipeline.sh

set -e

model_dir="$1"
output_dir="${2:-quantized}"
calibration_file="$3"

mkdir -p "$output_dir"

echo "=== Converting to GGUF ==="
python convert.py "$model_dir" \
    --outfile "$output_dir/model.gguf" \
    --outtype f16

echo "=== Generating Importance Matrix ==="
if [ -f "$calibration_file" ]; then
    ./llama-imatrix \
        -m "$output_dir/model.gguf" \
        -f "$calibration_file" \
        -o "$output_dir/imatrix.dat"
fi

echo "=== Creating Quantizations ==="
quantizations=("Q2_K" "Q3_K" "Q4_K" "Q5_K" "Q6_K" "Q8_0")

for quant in "${quantizations[@]}"; do
    echo "Quantizing to $quant..."

    if [ -f "$output_dir/imatrix.dat" ]; then
        ./llama-quantize \
            --imatrix "$output_dir/imatrix.dat" \
            "$output_dir/model.gguf" \
            "$output_dir/model-$quant.gguf" \
            "$quant"
    else
        ./llama-quantize \
            "$output_dir/model.gguf" \
            "$output_dir/model-$quant.gguf" \
            "$quant"
    fi
done

echo "=== Quantization Complete ==="
ls -lh "$output_dir/"
```

Quantization is essential for practical LLM deployment. It enables running large models on consumer hardware while maintaining good quality. Always test your specific use case at different quantization levels to find the best balance.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `gguf`, `llama` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Quantization` as an operating subsystem inside **llama.cpp Tutorial: Local LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `quantize`, `Q4_K`, `quality` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Quantization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `gguf` receives stable contracts.
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
- search upstream code for `model` and `gguf` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: GPU Acceleration](05-gpu.md)
- [Next Chapter: Chapter 7: Advanced Features](07-advanced.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
