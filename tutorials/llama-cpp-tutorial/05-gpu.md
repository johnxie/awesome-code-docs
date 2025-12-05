---
layout: default
title: "llama.cpp Tutorial - Chapter 5: GPU Acceleration"
nav_order: 5
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 5: GPU Acceleration

> Enable GPU acceleration with CUDA, Metal, and ROCm for dramatically faster inference.

## Overview

GPU acceleration can provide 5-10x speed improvements over CPU-only inference. llama.cpp supports multiple GPU platforms: NVIDIA CUDA, Apple Metal, and AMD ROCm.

## Hardware Requirements

### NVIDIA CUDA

- **GPU**: Pascal architecture or newer (GTX 1000 series, RTX series, Tesla, etc.)
- **VRAM**: At least 4GB for 7B models, 8GB+ recommended
- **Driver**: Latest NVIDIA drivers
- **CUDA Toolkit**: 11.0 or higher

### Apple Metal

- **Hardware**: Apple Silicon (M1, M2, M3 chips)
- **macOS**: 12.3 or higher
- **Xcode**: Command Line Tools installed

### AMD ROCm

- **GPU**: RDNA architecture GPUs (RX 5000/6000/7000 series)
- **Linux**: Ubuntu 20.04+ or RHEL/CentOS
- **ROCm**: Version 5.0 or higher

## Building with GPU Support

### NVIDIA CUDA (Linux/Windows)

```bash
# Install CUDA toolkit (Ubuntu)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run

# Build llama.cpp with CUDA
cd llama.cpp
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_CUDA=ON
make -j$(nproc)
```

### Apple Metal (macOS)

```bash
# Build with Metal support (automatically enabled on Apple Silicon)
cd llama.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_METAL=ON
cmake --build build --config Release -j$(sysctl -n hw.ncpu)

# Copy Metal shader
cp build/bin/ggml-metal.metal .
```

### AMD ROCm (Linux)

```bash
# Install ROCm (Ubuntu)
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add -
echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/5.4/ ubuntu main' | sudo tee /etc/apt/sources.list.d/rocm.list
sudo apt update
sudo apt install rocm-dev

# Build with ROCm
cd llama.cpp
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_HIPBLAS=ON -DAMDGPU_TARGETS=gfx1030,gfx1031,gfx1032
make -j$(nproc)
```

## GPU Inference Basics

### CUDA Usage

```bash
# Basic GPU inference
./llama-cli -m model.gguf \
    --gpu-layers 35 \    # Number of layers to offload to GPU
    --main-gpu 0         # Primary GPU device

# Multi-GPU setup
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --main-gpu 0 \
    --tensor-split 0.5,0.5  # Split across 2 GPUs
```

### Metal Usage (macOS)

```bash
# Metal acceleration (automatic on Apple Silicon)
./llama-cli -m model.gguf \
    --gpu-layers 35     # Offload to GPU

# Check Metal usage
./llama-cli -m model.gguf --prompt "Hello" --gpu-layers 35 --verbose-prompt
```

### ROCm Usage

```bash
# ROCm acceleration
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --main-gpu 0
```

## Optimizing GPU Performance

### Layer Offloading Strategy

```python
def calculate_optimal_gpu_layers(model_size_gb, vram_gb, safety_margin=0.8):
    """
    Calculate optimal number of layers to offload.

    model_size_gb: Model size in GB
    vram_gb: Available VRAM in GB
    safety_margin: Leave some VRAM for KV cache and overhead
    """
    available_vram = vram_gb * safety_margin

    # Rough estimate: each layer needs about model_size / num_layers GB
    # For 7B models (32 layers), each layer ~ 0.2-0.3 GB
    # For 13B models (40 layers), each layer ~ 0.3-0.4 GB

    if model_size_gb <= 4:  # 7B models
        layers_per_gb = 32 / model_size_gb
        optimal_layers = int(available_vram * layers_per_gb)
    elif model_size_gb <= 8:  # 13B models
        layers_per_gb = 40 / model_size_gb
        optimal_layers = int(available_vram * layers_per_gb)
    else:  # Larger models
        # Conservative estimate
        optimal_layers = int(available_vram * 2.5)

    return max(0, min(optimal_layers, 60))  # Cap at reasonable maximum

# Usage
model_size = 4.5  # GB for 7B Q4_K model
vram = 8  # GB VRAM
gpu_layers = calculate_optimal_gpu_layers(model_size, vram)
print(f"Optimal GPU layers: {gpu_layers}")
```

### Practical GPU Configuration

```bash
# Conservative (good for most cases)
./llama-cli -m model.gguf \
    --gpu-layers 28 \
    --batch-size 512 \
    --ubatch-size 512

# Aggressive (for high-end GPUs)
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --batch-size 1024 \
    --ubatch-size 512 \
    --flash-attn

# Multi-GPU (NVIDIA)
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --tensor-split 0.7,0.3  # 70% on GPU 0, 30% on GPU 1

# Memory efficient
./llama-cli -m model.gguf \
    --gpu-layers 20 \
    --ctx-size 2048 \
    --memory-f32
```

## Server Mode with GPU

```bash
# GPU-accelerated server
./llama-server -m model.gguf \
    --gpu-layers 35 \
    --host 0.0.0.0 \
    --port 8080 \
    --threads 8 \
    --batch-size 1024 \
    --ubatch-size 512 \
    --flash-attn \
    --ctx-size 4096
```

## Performance Benchmarking

### Benchmark Script

```bash
#!/bin/bash
# gpu_benchmark.sh

model="$1"
gpu_layers="$2"

echo "Benchmarking $model with $gpu_layers GPU layers"

# CPU baseline
echo "CPU baseline:"
./llama-bench -m "$model" -p 10 -n 128 -t $(nproc) 2>/dev/null | grep "tokens/sec"

# GPU test
echo "GPU ($gpu_layers layers):"
./llama-bench -m "$model" -p 10 -n 128 -t 1 -ngl "$gpu_layers" 2>/dev/null | grep "tokens/sec"

# Memory usage
echo "Memory usage:"
./llama-cli -m "$model" -ngl "$gpu_layers" --prompt "Hello" --n-predict 1 2>&1 | grep "VRAM\|RAM"
```

### Comparative Performance

Typical performance improvements:

| Configuration | Tokens/sec | Speedup |
|---------------|------------|---------|
| CPU only (i7-12700K) | 25-35 | 1x |
| CUDA RTX 3060 | 60-80 | 2.5x |
| CUDA RTX 4070 | 120-150 | 5x |
| CUDA RTX 4090 | 180-220 | 7x |
| Apple M2 Metal | 40-60 | 2x |
| Apple M3 Metal | 80-100 | 3.5x |

## GPU Memory Management

### VRAM Optimization

```bash
# Monitor VRAM usage
nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# Memory-efficient settings
./llama-cli -m model.gguf \
    --gpu-layers 25 \      # Leave VRAM for KV cache
    --ctx-size 2048 \      # Smaller context saves VRAM
    --memory-f32 \         # Use f32 for KV cache
    --no-mmap              # Avoid memory mapping overhead

# Large context optimization
./llama-cli -m model.gguf \
    --gpu-layers 20 \
    --ctx-size 8192 \
    --rope-scaling yarn \
    --rope-scale 2.0
```

### Multi-GPU Strategies

```bash
# Load balancing
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --tensor-split 0.6,0.4  # 60/40 split

# Dedicated GPUs
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --main-gpu 1 \         # Use GPU 1 as primary
    --tensor-split 0,1     # All work on GPU 1

# PCIe optimization
export CUDA_VISIBLE_DEVICES=0,1  # Only expose specific GPUs
./llama-cli -m model.gguf --gpu-layers 35 --tensor-split 0.5,0.5
```

## Troubleshooting GPU Issues

### CUDA Issues

**"CUDA out of memory":**
```bash
# Reduce GPU layers
./llama-cli -m model.gguf --gpu-layers 20

# Use smaller context
./llama-cli -m model.gguf --ctx-size 2048

# Check VRAM usage
nvidia-smi
```

**"CUDA error":**
```bash
# Update NVIDIA drivers
sudo apt update && sudo apt install nvidia-driver-XXX

# Check CUDA installation
nvcc --version
nvidia-smi
```

**Slow CUDA performance:**
```bash
# Enable TensorRT (if available)
export LLAMA_CUDA_USE_TENSORRT=1

# Use flash attention
./llama-cli -m model.gguf --gpu-layers 35 --flash-attn
```

### Metal Issues (macOS)

**"Metal not available":**
```bash
# Check macOS version
sw_vers

# Ensure Xcode tools
xcode-select --install

# Check Metal support
system_profiler SPDisplaysDataType | grep Metal
```

**Poor Metal performance:**
```bash
# Limit GPU layers
./llama-cli -m model.gguf --gpu-layers 25

# Check Activity Monitor for GPU usage
```

### ROCm Issues (Linux)

**Installation problems:**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Check ROCm installation
/opt/rocm/bin/rocminfo

# Set environment variables
export ROCM_PATH=/opt/rocm
export HIP_VISIBLE_DEVICES=0
```

## GPU-Specific Optimizations

### NVIDIA Optimizations

```bash
# Enable CUDA graphs (faster kernel launches)
export LLAMA_CUDA_ENABLE_CUBLAS=1

# Use TensorRT for faster inference (experimental)
export LLAMA_CUDA_USE_TENSORRT=1

# Multi-stream processing
./llama-server -m model.gguf \
    --gpu-layers 35 \
    --parallel 4 \
    --cont-batching
```

### Apple Silicon Optimizations

```bash
# Enable Metal optimizations
export LLAMA_METAL_ENABLE_DEBUG=0

# Use unified memory efficiently
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --ctx-size 4096 \
    --mlock  # Lock in unified memory

# Check Neural Engine usage (if available)
powermetrics --samplers gpu_power | grep "Neural Engine"
```

### AMD Optimizations

```bash
# Set GPU device
export HIP_VISIBLE_DEVICES=0

# Enable HIP optimizations
export LLAMA_HIP_ROCM_VERSION=1

# Use ROCm-specific settings
./llama-cli -m model.gguf \
    --gpu-layers 35 \
    --main-gpu 0 \
    --threads 8
```

## Monitoring GPU Usage

### NVIDIA Monitoring

```bash
# Real-time GPU stats
nvidia-smi -l 1

# GPU utilization during inference
nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total --format=csv

# Power consumption
nvidia-smi --query-gpu=power.draw,power.limit --format=csv
```

### AMD Monitoring

```bash
# ROCm system management
rocm-smi

# GPU usage
rocm-smi --showuse

# Temperature and power
rocm-smi --showtemp --showpower
```

### Apple Monitoring

```bash
# Activity Monitor (GUI)
# Or command line
powermetrics --samplers gpu_power -n 1
```

## Cost-Benefit Analysis

### GPU vs CPU Comparison

```python
def gpu_vs_cpu_comparison(model_size_gb, vram_gb, electricity_cost_per_kwh=0.12):
    """
    Compare GPU vs CPU costs for inference.
    """

    # Assumptions
    cpu_tokens_per_second = 25
    gpu_tokens_per_second = 120  # RTX 4070 example

    gpu_power_watts = 200  # GPU power consumption
    cpu_power_watts = 125  # CPU power consumption

    # Calculate hourly costs
    gpu_hourly_power_cost = (gpu_power_watts / 1000) * electricity_cost_per_kwh
    cpu_hourly_power_cost = (cpu_power_watts / 1000) * electricity_cost_per_kwh

    # Performance comparison
    speedup = gpu_tokens_per_second / cpu_tokens_per_second
    gpu_efficiency = speedup / (gpu_power_watts / cpu_power_watts)

    print(f"GPU speedup: {speedup:.1f}x")
    print(f"GPU power cost per hour: ${gpu_hourly_power_cost:.3f}")
    print(f"CPU power cost per hour: ${cpu_hourly_power_cost:.3f}")
    print(f"GPU efficiency: {gpu_efficiency:.1f}x tokens per watt")

    # Break-even analysis
    gpu_initial_cost = 600  # Example GPU cost
    gpu_daily_usage_hours = 8
    gpu_daily_power_cost = gpu_hourly_power_cost * gpu_daily_usage_hours

    # Days to break even on power savings alone
    daily_savings = cpu_hourly_power_cost * gpu_daily_usage_hours - gpu_daily_power_cost
    if daily_savings > 0:
        breakeven_days = gpu_initial_cost / daily_savings
        print(f"Break-even period: {breakeven_days:.0f} days")
    else:
        print("GPU uses more power, focus on performance benefits")

gpu_vs_cpu_comparison(4.5, 12)
```

## Best Practices

1. **Right-size GPU layers**: Balance VRAM usage with performance
2. **Monitor temperatures**: GPUs can throttle when hot
3. **Use appropriate precision**: F16 for speed, F32 for accuracy
4. **Batch efficiently**: Larger batches improve GPU utilization
5. **Update drivers**: Keep GPU drivers and CUDA/ROCm current
6. **Test thoroughly**: Validate outputs match CPU results
7. **Power management**: Use appropriate power limits for stability

GPU acceleration dramatically improves inference speed and enables larger model usage. Choose the right GPU platform for your hardware and optimize layer offloading for maximum performance. 