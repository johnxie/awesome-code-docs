---
layout: default
title: "LocalAI Tutorial - Chapter 2: Model Gallery"
nav_order: 2
has_children: false
parent: LocalAI Tutorial
---

# Chapter 2: Model Gallery and Management

> Discover available models, install different architectures, and manage your local model collection.

## Overview

LocalAI supports a wide variety of models through its gallery system. This chapter covers model discovery, installation, and management of different model types.

## Model Gallery

### Accessing the Gallery

```bash
# View available models
curl http://localhost:8080/models/available

# Get detailed model information
curl http://localhost:8080/models/gallery
```

### Model Categories

LocalAI supports several model types:

#### Large Language Models (LLMs)

```bash
# Install popular LLMs
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "mistral-7b-instruct"}'

curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "llama-2-7b-chat"}'

curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "codellama-7b-instruct"}'
```

#### Small and Fast Models

```bash
# Phi-2 (2.7B parameters, fast inference)
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "phi-2"}'

# TinyLlama (1.1B parameters, very fast)
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "tinyllama"}'

# Orca Mini (3B parameters, good quality/speed balance)
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "orca-mini"}'
```

### Model Status and Progress

```bash
# Check installation status
curl http://localhost:8080/models/jobs

# Get specific model status
curl http://localhost:8080/models/jobs/phi-2

# View installed models
curl http://localhost:8080/v1/models
```

## Manual Model Installation

### Downloading from HuggingFace

```bash
# Create models directory
mkdir -p models

# Download Phi-2 GGUF
cd models
wget https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf
wget https://huggingface.co/microsoft/phi-2/resolve/main/tokenizer.json
wget https://huggingface.co/microsoft/phi-2/resolve/main/tokenizer_config.json
```

### Creating Model Configuration

```yaml
# models/phi-2.yaml
name: phi-2
backend: llama
parameters:
  model: phi-2.Q4_K_M.gguf
  temperature: 0.7
  top_p: 0.9
  top_k: 40
  max_tokens: 512
  context_size: 2048

# For chat models
chat_template: chatml  # or llama2, mistral, etc.
```

### Model Configuration Options

```yaml
# Comprehensive model config
name: my-custom-model
backend: llama  # or gpt4all, transformers, etc.
parameters:
  model: model.gguf
  temperature: 0.8
  top_p: 0.95
  top_k: 50
  repeat_penalty: 1.1
  repeat_last_n: 64
  context_size: 4096
  max_tokens: 2048
  threads: 4
  batch_size: 512
  f16: false  # Use f32 for compatibility

# Backend-specific settings
backend_settings:
  mmap: true
  mlock: false
  gpu_layers: 0  # For GPU acceleration

# Chat template
chat_template: llama2
```

## Model Backends

### Llama.cpp Backend (GGUF Models)

Best for most LLM use cases:

```yaml
# GGUF model config
name: llama-model
backend: llama
parameters:
  model: llama-2-7b-chat.Q4_K_M.gguf
  context_size: 4096
  threads: 8
  batch_size: 512
```

### GPT4All Backend

For older GPT-J/GPT-NeoX models:

```yaml
name: gpt4all-model
backend: gpt4all
parameters:
  model: gpt4all-model.bin
  context_size: 2048
```

### Transformers Backend

For PyTorch models (slower, more memory):

```yaml
name: bert-model
backend: transformers
parameters:
  model: bert-base-uncased
  task: text-classification
```

## Model Management

### Listing Models

```bash
# Get all models
curl http://localhost:8080/v1/models

# Get specific model info
curl http://localhost:8080/v1/models/phi-2

# Check model health
curl http://localhost:8080/models/health/phi-2
```

### Updating Models

```bash
# Update model configuration
curl -X POST http://localhost:8080/models/config/phi-2 \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "temperature": 0.8,
      "max_tokens": 1024
    }
  }'
```

### Removing Models

```bash
# Remove model from memory
curl -X DELETE http://localhost:8080/models/phi-2

# Remove model files (manual)
rm -rf models/phi-2/
```

## Model Performance Tuning

### Memory Optimization

```yaml
# Low-memory configuration
name: phi-2-memory-optimized
backend: llama
parameters:
  model: phi-2.Q4_K_M.gguf
  context_size: 1024  # Smaller context
  threads: 2          # Fewer threads
  batch_size: 256     # Smaller batch
  f16: false          # Use f32
  mmap: true          # Memory mapping
  mlock: false        # Don't lock in RAM
```

### Speed Optimization

```yaml
# High-speed configuration
name: phi-2-fast
backend: llama
parameters:
  model: phi-2.Q4_K_M.gguf
  context_size: 2048
  threads: 8          # More threads
  batch_size: 1024    # Larger batch
  gpu_layers: 20      # GPU acceleration
  flash_attn: true    # Flash attention
```

### Quality Optimization

```yaml
# High-quality configuration
name: phi-2-quality
backend: llama
parameters:
  model: phi-2.Q4_K_M.gguf
  temperature: 0.1    # More deterministic
  top_p: 0.1          # Focused sampling
  repeat_penalty: 1.2 # Reduce repetition
  context_size: 4096  # Larger context
```

## Custom Model Training

### Fine-tuning with Axolotl

```bash
# Install Axolotl
pip install axolotl

# Prepare dataset
# Train model
axolotl train config.yml

# Convert to GGUF
python convert.py /path/to/trained/model \
    --outfile fine-tuned.gguf \
    --outtype f16
```

### LoRA Training

```bash
# Use Unsloth for efficient LoRA training
pip install unsloth

# Train LoRA adapter
# Apply to base model
```

## Model Validation

### Testing Model Quality

```python
import openai

client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

def test_model(model_name):
    """Test model with various prompts."""

    test_cases = [
        "Explain quantum computing in simple terms",
        "Write a Python function to reverse a string",
        "What are the benefits of renewable energy?",
        "Tell me a joke about programming"
    ]

    for prompt in test_cases:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        print(f"Prompt: {prompt}")
        print(f"Response: {response.choices[0].message.content[:100]}...")
        print("-" * 50)

# Test different models
test_model("phi-2")
test_model("mistral-7b-instruct")
```

### Performance Benchmarking

```python
import time
import openai

client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

def benchmark_model(model_name, prompt, runs=5):
    """Benchmark model performance."""

    times = []
    token_counts = []

    for i in range(runs):
        start_time = time.time()

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        end_time = time.time()

        times.append(end_time - start_time)
        token_counts.append(response.usage.completion_tokens)

    avg_time = sum(times) / len(times)
    avg_tokens = sum(token_counts) / len(token_counts)
    tokens_per_sec = avg_tokens / avg_time

    print(f"Model: {model_name}")
    print(".2f")
    print(".1f")
    print(".1f")
    print("-" * 30)

# Benchmark models
benchmark_model("phi-2", "Write a haiku about artificial intelligence")
benchmark_model("mistral-7b-instruct", "Write a haiku about artificial intelligence")
```

## Model Gallery API

### Programmatic Model Management

```python
import requests

class LocalAIModelManager:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url

    def list_available_models(self):
        """List available models in gallery."""
        response = requests.get(f"{self.base_url}/models/available")
        return response.json()

    def install_model(self, model_id, config=None):
        """Install a model from gallery."""
        data = {"id": model_id}
        if config:
            data.update(config)

        response = requests.post(
            f"{self.base_url}/models/apply",
            json=data
        )
        return response.json()

    def get_model_status(self, model_id):
        """Get model installation status."""
        response = requests.get(f"{self.base_url}/models/jobs/{model_id}")
        return response.json()

    def list_installed_models(self):
        """List currently installed models."""
        response = requests.get(f"{self.base_url}/v1/models")
        return response.json()

    def delete_model(self, model_id):
        """Remove a model."""
        response = requests.delete(f"{self.base_url}/models/{model_id}")
        return response.status_code == 200

# Usage
manager = LocalAIModelManager()

# List available models
available = manager.list_available_models()
print("Available models:", len(available))

# Install a model
manager.install_model("phi-2")

# Check status
status = manager.get_model_status("phi-2")
print("Installation status:", status)

# List installed models
installed = manager.list_installed_models()
print("Installed models:", [m["id"] for m in installed["data"]])
```

## Troubleshooting Model Issues

### Common Installation Problems

```bash
# Check disk space
df -h

# Check download progress
curl http://localhost:8080/models/jobs

# Restart LocalAI if download stuck
docker restart localai-container

# Check logs for errors
docker logs localai-container 2>&1 | tail -50
```

### Model Loading Issues

```bash
# Verify model file exists
ls -la models/model.gguf

# Check model file integrity
file models/model.gguf

# Test with simple config
curl -X POST http://localhost:8080/models/config/test-model \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"model": "phi-2.Q4_K_M.gguf"}}'
```

### Performance Issues

```bash
# Monitor system resources
top -p $(pgrep localai)
free -h
nvidia-smi  # If using GPU

# Adjust model parameters
curl -X POST http://localhost:8080/models/config/model-name \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "threads": 4,
      "batch_size": 256,
      "context_size": 1024
    }
  }'
```

## Best Practices

1. **Start Small**: Begin with smaller models like Phi-2 or TinyLlama
2. **Monitor Resources**: Track RAM/VRAM usage when installing larger models
3. **Test Quality**: Always validate model outputs for your use case
4. **Version Control**: Keep track of model versions and configurations
5. **Backup Models**: Maintain backups of working model configurations
6. **Update Regularly**: Check for updated model versions in the gallery

## Model Compatibility Matrix

| Model Type | Backend | Requirements | Performance |
|------------|---------|--------------|-------------|
| GGUF (Llama/Mistral) | llama | CPU/GPU | Excellent |
| GPT4All format | gpt4all | CPU | Good |
| PyTorch models | transformers | CPU/GPU | Variable |
| Custom models | varies | depends | depends |

Next: Learn how to use LocalAI for text generation with different parameters and chat formats. 