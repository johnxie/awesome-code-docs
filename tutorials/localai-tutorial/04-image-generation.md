---
layout: default
title: "LocalAI Tutorial - Chapter 4: Image Generation"
nav_order: 4
has_children: false
parent: LocalAI Tutorial
---

# Chapter 4: Image Generation with Stable Diffusion

> Generate images locally using Stable Diffusion models through LocalAI's OpenAI-compatible API.

## Overview

LocalAI supports image generation using Stable Diffusion models, providing an OpenAI DALL-E compatible API that runs entirely on your local hardware.

## Installing Image Models

### Stable Diffusion Models

```bash
# Install Stable Diffusion 1.5
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "stablediffusion"}'

# Install SDXL (better quality, requires more VRAM)
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "stablediffusion-xl"}'
```

### Custom Model Installation

```bash
# Download model files
mkdir -p models/stablediffusion
cd models/stablediffusion

# Download Stable Diffusion 1.5
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/model_index.json

# Create model configuration
cat > ../stablediffusion.yaml << EOF
name: stablediffusion
backend: stablediffusion
parameters:
  model: stablediffusion/v1-5-pruned-emaonly.safetensors
  height: 512
  width: 512
  steps: 20
  guidance_scale: 7.5
EOF
```

## Basic Image Generation

### OpenAI-Compatible API

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

response = client.images.generate(
    model="stablediffusion",
    prompt="A beautiful sunset over mountains, digital art",
    size="512x512",
    n=1
)

# Get image URL
image_url = response.data[0].url
print(f"Generated image: {image_url}")
```

### Direct API Call

```bash
curl -X POST http://localhost:8080/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stablediffusion",
    "prompt": "A futuristic city at night, cyberpunk style",
    "size": "512x512",
    "n": 1
  }'
```

## Advanced Parameters

### Generation Control

```python
response = client.images.generate(
    model="stablediffusion",
    prompt="A serene lake surrounded by autumn trees",
    size="768x512",           # Width x Height
    n=1,                      # Number of images
    steps=30,                 # Inference steps (higher = better quality, slower)
    guidance_scale=7.5,       # How closely to follow prompt (1-20)
    seed=42,                  # Random seed for reproducibility
    negative_prompt="blurry, low quality, distorted"  # What to avoid
)
```

### Parameter Optimization

```python
# Quality-focused generation
high_quality = client.images.generate(
    model="stablediffusion",
    prompt="Professional portrait, studio lighting, 8k",
    size="1024x1024",
    steps=50,
    guidance_scale=12.0,
    negative_prompt="blurry, ugly, poorly lit"
)

# Fast generation
fast_generation = client.images.generate(
    model="stablediffusion",
    prompt="Simple landscape",
    size="256x256",
    steps=10,
    guidance_scale=3.0
)
```

## Image Variations

### Prompt Engineering

```python
# Detailed prompts for better results
detailed_prompts = [
    "A majestic eagle soaring over dramatic mountain peaks at golden hour, highly detailed, photorealistic, 8k resolution",
    "Cyberpunk city street at night with neon lights and flying cars, digital art, vibrant colors, detailed architecture",
    "A peaceful Japanese garden with cherry blossoms, traditional architecture, soft morning light, serene atmosphere",
    "Steampunk airship floating above Victorian London, detailed mechanical parts, foggy atmosphere, dramatic lighting"
]

for prompt in detailed_prompts:
    response = client.images.generate(
        model="stablediffusion",
        prompt=prompt,
        size="512x512",
        steps=25,
        guidance_scale=7.5
    )
    print(f"Generated: {response.data[0].url}")
```

### Negative Prompts

```python
# Use negative prompts to avoid unwanted elements
response = client.images.generate(
    model="stablediffusion",
    prompt="A beautiful woman, portrait, professional photography",
    negative_prompt="ugly, deformed, blurry, low quality, text, watermark, signature",
    size="512x512",
    steps=30,
    guidance_scale=8.0
)
```

## SDXL Support

### SDXL Models (Higher Quality)

```python
# SDXL generates higher resolution images
sdxl_response = client.images.generate(
    model="stablediffusion-xl",
    prompt="A breathtaking landscape, hyperrealistic, 8k",
    size="1024x1024",         # SDXL supports higher resolutions
    steps=40,
    guidance_scale=9.0
)

# SDXL with refiner (if available)
refined_response = client.images.generate(
    model="stablediffusion-xl",
    prompt="Portrait of a person, highly detailed face",
    size="1024x1024",
    steps=25,
    guidance_scale=6.0,
    # Additional SDXL parameters
    denoising_strength=0.3
)
```

## Custom Models and LoRA

### Using Custom Checkpoints

```yaml
# Custom model configuration
name: custom-sd-model
backend: stablediffusion
parameters:
  model: custom-models/realistic-vision.safetensors
  vae: custom-models/vae-ft-mse.safetensors  # Optional VAE
  clip_model: openai/clip-vit-large-patch14  # CLIP model
  height: 512
  width: 768
  steps: 25
  guidance_scale: 7.0
```

### LoRA Adapters

```yaml
# Model with LoRA adapter
name: sd-with-lora
backend: stablediffusion
parameters:
  model: stablediffusion/v1-5-pruned-emaonly.safetensors
  lora: lora-adapters/more-details.safetensors
  lora_scale: 0.8  # LoRA strength (0-1)
  height: 512
  width: 512
  steps: 20
```

## Image-to-Image

### Image Variation

```python
# Generate variation of existing image
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Load image
image_b64 = image_to_base64("input_image.jpg")

response = client.images.create_variation(
    image=image_b64,
    n=1,
    size="512x512",
    response_format="url"
)
```

### Inpainting (if supported)

```python
# Fill in masked parts of image
response = client.images.edit(
    image=image_b64,
    mask=mask_b64,  # Black and white mask
    prompt="Add a sunset background",
    size="512x512"
)
```

## Batch Generation

### Multiple Images

```python
def generate_batch(prompts, model="stablediffusion", size="512x512"):
    """Generate multiple images from different prompts."""
    results = []

    for prompt in prompts:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            n=1
        )
        results.append({
            "prompt": prompt,
            "url": response.data[0].url,
            "revised_prompt": getattr(response.data[0], 'revised_prompt', None)
        })

    return results

# Generate batch
prompts = [
    "A cat wearing sunglasses",
    "A dog playing poker",
    "A robot cooking dinner",
    "A dragon breathing fire"
]

batch_results = generate_batch(prompts)
for result in batch_results:
    print(f"Prompt: {result['prompt']}")
    print(f"Image: {result['url']}")
    print()
```

## Performance Optimization

### Hardware Acceleration

```yaml
# GPU acceleration
name: gpu-sd
backend: stablediffusion
parameters:
  model: stablediffusion/v1-5-pruned-emaonly.safetensors
  gpu_layers: -1  # Use all available GPU layers
  height: 512
  width: 512
  steps: 20
  # Hardware-specific optimizations
  attention: flash  # Flash attention
  precision: fp16   # Half precision
```

### Memory Optimization

```yaml
# Low VRAM configuration
name: low-vram-sd
backend: stablediffusion
parameters:
  model: stablediffusion/v1-5-pruned-emaonly.safetensors
  height: 256
  width: 256
  steps: 15
  guidance_scale: 5.0
  # Memory optimizations
  enable_attention_slicing: true
  enable_vae_slicing: true
  enable_cpu_offload: true
```

## Downloading Generated Images

```python
import requests

def download_image(image_url, filename):
    """Download generated image."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Saved image to {filename}")
    else:
        print(f"Failed to download image: {response.status_code}")

# Download generated images
for i, result in enumerate(batch_results):
    download_image(result['url'], f"generated_image_{i+1}.png")
```

## Troubleshooting

### Common Issues

**Out of memory:**
```bash
# Reduce image size
curl -X POST http://localhost:8080/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{"model": "stablediffusion", "prompt": "test", "size": "256x256", "steps": 10}'
```

**Slow generation:**
```bash
# Enable GPU acceleration (if available)
# Check GPU usage: nvidia-smi
# Reduce steps for faster generation
```

**Low quality images:**
```bash
# Increase steps and guidance scale
# Use better prompts with more detail
# Try SDXL models for higher quality
```

### Model Issues

```bash
# Check model status
curl http://localhost:8080/models/jobs/stablediffusion

# Restart if model failed to load
curl -X DELETE http://localhost:8080/models/stablediffusion
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "stablediffusion"}'
```

## Advanced Techniques

### Prompt Weighting

```python
# Use prompt weighting (if supported)
weighted_prompt = """
(masterpiece:1.2), (best quality:1.2),
detailed face, beautiful eyes,
professional photograph,
(sharp focus:1.1), (intricate details:1.1)
"""

response = client.images.generate(
    model="stablediffusion",
    prompt=weighted_prompt,
    size="512x512",
    steps=30
)
```

### ControlNet Integration

```yaml
# ControlNet for pose/edge control (if supported)
name: sd-controlnet
backend: stablediffusion
parameters:
  model: stablediffusion/v1-5-pruned-emaonly.safetensors
  controlnet: controlnet-models/canny.safetensors
  controlnet_conditioning_scale: 1.0
  height: 512
  width: 512
```

## Best Practices

1. **Prompt Engineering**: Detailed, descriptive prompts yield better results
2. **Resolution**: Use appropriate sizes (512x512 is good default)
3. **Steps vs Quality**: More steps = better quality but slower generation
4. **Guidance Scale**: 7-12 is good range; higher values = closer to prompt
5. **Negative Prompts**: Use them to avoid unwanted elements
6. **Batch Processing**: Generate multiple variations to find best results
7. **Hardware**: GPU acceleration dramatically improves speed

Next: Explore audio processing with Whisper transcription and text-to-speech. 