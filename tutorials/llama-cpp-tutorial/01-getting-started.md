---
layout: default
title: "llama.cpp Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 1: Getting Started with llama.cpp

> Build llama.cpp from source and run your first LLM locally with optimized C/C++ inference.

## Overview

llama.cpp enables fast, local LLM inference without Python dependencies. This chapter covers building the project and running your first model on CPU.

## Prerequisites

- **C++ Compiler**: GCC 7+ or Clang 6+ (MSVC on Windows)
- **CMake**: Version 3.12 or higher
- **Git**: For cloning the repository
- **GGUF Model File**: A quantized model (we'll get one in this chapter)

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4GB | 16GB+ |
| Storage | 2GB free | 10GB+ for models |
| CPU | x64 with AVX2 | Modern CPU with AVX-512 |

## Building llama.cpp

### Clone and Build

```bash
# Clone the repository
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build with CMake (recommended)
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Or use the build script (alternative)
cd ..
./scripts/build.sh
```

### Platform-Specific Instructions

#### macOS (Apple Silicon)

```bash
# Install dependencies
brew install cmake

# Clone and build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build with Metal support (M1/M2/M3)
cmake -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_METAL=ON
cmake --build build --config Release -j$(sysctl -n hw.ncpu)

# Copy Metal shader
cp build/bin/ggml-metal.metal .
```

#### Linux (Ubuntu/Debian)

```bash
# Install build dependencies
sudo apt update
sudo apt install build-essential cmake git

# Clone and build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build with CPU optimizations
cmake -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_AVX=ON -DLLAMA_AVX2=ON -DLLAMA_AVX512=ON
cmake --build build --config Release -j$(nproc)
```

#### Windows (MSVC)

```powershell
# Install dependencies (via Chocolatey or manual)
# choco install cmake git

# Clone and build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Build with Visual Studio
cmake -B build -G "Visual Studio 17 2022"
cmake --build build --config Release --parallel
```

## Getting a Model

Download a small GGUF model for testing:

```bash
# Create models directory
mkdir -p models

# Download a small Llama 2 model (1.1B parameters, quantized)
cd models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf

# Or download an even smaller model for testing
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/ggml-model.bin
# Note: This is not GGUF format, just for initial testing
```

### Popular Model Sources

- **Hugging Face**: Search for "GGUF" models
- **TheBloke on HuggingFace**: Pre-quantized models
- **Local Model Conversion**: Convert from PyTorch (covered in Chapter 6)

## Your First Inference

Run inference with the CLI:

```bash
# Basic chat completion
cd llama.cpp/build/bin
./llama-cli -m ../../models/llama-2-7b-chat.Q2_K.gguf \
    --prompt "Hello! How are you?" \
    --n-predict 128 \
    --temp 0.8

# Interactive chat mode
./llama-cli -m ../../models/llama-2-7b-chat.Q2_K.gguf \
    --interactive \
    --ctx-size 2048 \
    --temp 0.7 \
    --top-k 40 \
    --top-p 0.9 \
    --repeat-penalty 1.1
```

### Understanding the Output

```
system_info: n_threads = 8 / 16 | AVX = 1 | AVX2 = 1 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 0 | SSE3 = 1 | SSSE3 = 1 | VSX = 0 |

sampling: 
        repeat_last_n = 64, repeat_penalty = 1.100, frequency_penalty = 0.000, presence_penalty = 0.000
        top_k = 40, tfs_z = 1.000, top_p = 0.950, min_p = 0.050, typical_p = 1.000, temp = 0.800
        mirostat = 0, mirostat_lr = 0.100, mirostat_ent = 5.000

generate: n_ctx = 2048, n_batch = 512, n_predict = -1, n_keep = 1

Hello! How are you?

I'm doing well, thank you for asking! I'm Grok, a helpful and maximally truthful AI built by xAI. I'm here to assist you with any questions or tasks you might have. What can I help you with today?
```

## Performance Tuning

### CPU Optimization

```bash
# Use all CPU cores
./llama-cli -m model.gguf --threads $(nproc) --prompt "Hello"

# Adjust context size based on RAM
./llama-cli -m model.gguf --ctx-size 4096 --prompt "Hello"

# Batch processing for better throughput
./llama-cli -m model.gguf --batch-size 512 --prompt "Hello"
```

### Memory Management

```bash
# Check model memory requirements
./llama-cli -m model.gguf --verbose-prompt

# Monitor memory usage
./llama-cli -m model.gguf --mlock  # Lock model in RAM (faster but uses more memory)
```

## Common Issues and Solutions

### Build Issues

**CMake not found:**
```bash
# Install CMake
sudo apt install cmake  # Linux
brew install cmake      # macOS
```

**Compiler too old:**
```bash
# Check compiler version
gcc --version

# Update or install newer compiler
sudo apt install gcc-11 g++-11
export CC=gcc-11 CXX=g++-11
```

### Runtime Issues

**Out of memory:**
```
# Reduce context size
./llama-cli -m model.gguf --ctx-size 1024

# Use smaller model or higher quantization
# Try Q3_K or Q4_K models instead of Q2_K
```

**Slow inference:**
```
# Enable CPU optimizations
./llama-cli -m model.gguf --threads $(nproc)

# Use Metal on macOS
./llama-cli -m model.gguf --n-gpu-layers 1
```

**Model not found:**
```
# Check model path
ls -la /path/to/model.gguf

# Use absolute path
./llama-cli -m /full/path/to/model.gguf
```

## Testing Your Setup

Create a test script:

```bash
#!/bin/bash
# test_llama.sh

MODEL_PATH="../../models/llama-2-7b-chat.Q2_K.gguf"
EXECUTABLE="./llama-cli"

echo "Testing llama.cpp setup..."

# Check if executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "❌ llama-cli not found. Build llama.cpp first."
    exit 1
fi

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Model file not found. Download a model first."
    exit 1
fi

# Test basic inference
echo "🧪 Running basic inference test..."
timeout 30s $EXECUTABLE -m "$MODEL_PATH" --prompt "Say hello in 10 words." --n-predict 20

if [ $? -eq 0 ]; then
    echo "✅ Basic test passed!"
else
    echo "❌ Basic test failed!"
    exit 1
fi

echo "🎉 llama.cpp is working correctly!"
```

## Performance Benchmarks

Compare performance across systems:

```bash
# Benchmark script
./llama-bench -m model.gguf -p 20 -n 128 -t $(nproc)

# Output shows tokens/second, memory usage, etc.
```

Typical performance (approximate):
- **MacBook M2**: 30-50 tokens/sec (7B model, Q4_K)
- **Intel i7-12700K**: 20-35 tokens/sec
- **AMD Ryzen 9 5950X**: 25-40 tokens/sec

## Next Steps

Now that you can run models locally, let's explore model formats and quantization in the next chapter to understand how to choose and optimize models for your hardware.

## Example Commands

```bash
# Quick test with small prompt
./llama-cli -m model.gguf --prompt "The capital of France is" --n-predict 10

# Interactive mode with custom settings
./llama-cli -m model.gguf --interactive --temp 0.8 --top-k 40 --ctx-size 2048

# Benchmark performance
./llama-bench -m model.gguf -n 128 -t 8

# Get model info
./llama-cli -m model.gguf --verbose-prompt --prompt ""
```

This setup gives you a fast, local LLM inference engine that works offline and respects your privacy. The pure C/C++ implementation means quick startup times and efficient resource usage. 