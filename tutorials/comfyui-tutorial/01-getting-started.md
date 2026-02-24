---
layout: default
title: "Chapter 1: Getting Started with ComfyUI"
parent: "ComfyUI Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with ComfyUI

Welcome to ComfyUI! If you've ever wanted complete control over AI image generation with the flexibility to create complex, professional workflows, you're in the right place. ComfyUI revolutionizes how we interact with AI image generation by providing a node-based interface that gives you unprecedented control over every aspect of the generation process.

## What Makes ComfyUI Revolutionary?

ComfyUI transforms AI image generation by:
- **Node-Based Architecture** - Visual workflow creation with drag-and-drop simplicity
- **Maximum Control** - Adjust every parameter and connection in your pipeline
- **Modular Design** - Mix and match components for custom workflows
- **Real-Time Preview** - See results instantly as you build workflows
- **Extensible System** - Add custom nodes and integrations
- **Performance Optimized** - Efficient memory usage and fast generation
- **Open-Source Freedom** - No restrictions, full customization

## Installation Options

### Option 1: Standalone Installation (Recommended)

```bash
# Clone the ComfyUI repository
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Install dependencies
pip install -r requirements.txt

# For GPU acceleration (if you have CUDA)
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121

# Launch ComfyUI
python main.py
```

### Option 2: Portable Installation (Windows)

```bash
# Download the portable version
# Visit: https://github.com/comfyanonymous/ComfyUI/releases
# Download: ComfyUI_windows_portable.zip

# Extract and run
unzip ComfyUI_windows_portable.zip
cd ComfyUI_windows_portable
run_nvidia_gpu.bat  # or run_cpu.bat for CPU-only
```

### Option 3: Docker Installation

```bash
# Run with Docker
docker run --gpus all -p 8188:8188 -v $(pwd)/models:/ComfyUI/models comfyanonymous/comfyui

# Or build from source
docker build -t comfyui .
docker run --gpus all -p 8188:8188 comfyui
```

## Your First Image Generation

Let's create your first AI-generated image:

### Step 1: Access the Interface

1. Open your browser and navigate to `http://127.0.0.1:8188`
2. You'll see the ComfyUI interface with a blank canvas
3. On the right side, you'll find the node library

### Step 2: Load a Basic Workflow

```python
# Click "Load Default" or manually add nodes:
# 1. Add a "CLIPTextEncode" node (for text encoding)
# 2. Add a "KSampler" node (for image generation)
# 3. Add an "Empty Latent Image" node (for image dimensions)
# 4. Add a "VAEDecode" node (for image decoding)
# 5. Add a "Save Image" node (for output)
```

### Step 3: Connect the Nodes

The basic workflow structure:
```
Text Input → CLIP Encoder → KSampler → VAE Decoder → Save Image
                    ↓
         Empty Latent Image
```

### Step 4: Configure Your Generation

```python
# In the CLIPTextEncode node:
positive_prompt = "a beautiful landscape, digital art, highly detailed"
negative_prompt = "blurry, low quality, distorted"

# In the Empty Latent Image node:
width = 512
height = 512
batch_size = 1

# In the KSampler node:
steps = 20
cfg_scale = 7.0
sampler_name = "euler"
scheduler = "normal"
denoise = 1.0
```

### Step 5: Generate Your Image

1. Click the "Queue" button
2. Watch the progress in the console
3. View your generated image in the output folder

## Understanding ComfyUI's Architecture

### Core Components

```
ComfyUI System
├── Frontend (Web Interface)
│   ├── Node Canvas (Drag & Drop Interface)
│   ├── Node Library (Available Components)
│   ├── Property Panel (Node Configuration)
│   └── Queue System (Batch Processing)
├── Backend (Python Engine)
│   ├── Model Manager (Checkpoint Loading)
│   ├── Node Executor (Workflow Processing)
│   ├── Cache System (Performance Optimization)
│   └── Extension System (Custom Nodes)
└── Models & Data
    ├── Checkpoints (Base Models)
    ├── LoRAs (Fine-tuned Adapters)
    ├── VAEs (Image Decoders)
    └── Embeddings (Textual Inversions)
```

### Node Types

#### Input Nodes
- **Text Input**: CLIP text encoding for prompts
- **Image Input**: Load existing images for processing
- **Model Loader**: Load Stable Diffusion checkpoints
- **LoRA Loader**: Apply fine-tuned adapters

#### Processing Nodes
- **KSampler**: Main diffusion sampling engine
- **ControlNet**: Precise pose and structure control
- **IP-Adapter**: Image-based prompt adaptation
- **Upscale**: High-resolution image enhancement

#### Output Nodes
- **Save Image**: Export generated images
- **Preview Image**: Real-time image preview
- **Image Grid**: Combine multiple images
- **Video Output**: Create animated sequences

## Essential Concepts

### 1. Latent Space

ComfyUI works in "latent space" for efficiency:
- Images are encoded into a compressed latent representation
- Generation happens in this compressed space
- Final images are decoded back to pixel space
- This allows for much faster generation and lower memory usage

### 2. Sampling Methods

Different sampling algorithms for different results:

```python
# Common samplers
samplers = {
    "euler": "Fast, good quality",
    "euler_ancestral": "Creative, varied results",
    "heun": "High quality, slower",
    "dpm_2": "Balanced quality/speed",
    "dpm_2_ancestral": "Very creative",
    "lms": "Consistent results",
    "ddim": "Fast, good for animations"
}
```

### 3. CFG Scale (Classifier-Free Guidance)

Controls how closely the AI follows your prompt:
- **Low (1-5)**: More creative, less prompt adherence
- **Medium (6-10)**: Balanced creativity and adherence
- **High (11-20)**: Strict prompt following, less creativity

### 4. Denoising Strength

For image-to-image workflows:
- **0.0**: No change to input image
- **0.5**: Moderate change
- **1.0**: Complete transformation

## Model Management

### Downloading Models

```bash
# Create models directory
mkdir -p models/checkpoints
mkdir -p models/loras
mkdir -p models/vae

# Download base models (example)
# Visit: https://huggingface.co/runwayml/stable-diffusion-v1-5
# or https://civitai.com/ for community models

# Place model files in appropriate directories
# - Checkpoints: models/checkpoints/
# - LoRAs: models/loras/
# - VAEs: models/vae/
```

### Model Configuration

```python
# In ComfyUI, load models using these nodes:
# - CheckpointLoaderSimple (for base models)
# - LoraLoader (for LoRA adapters)
# - VAELoader (for custom VAEs)

# Example model loading workflow:
# 1. CheckpointLoaderSimple → Select your .safetensors file
# 2. LoraLoader → Apply style adaptations
# 3. VAELoader → Use custom decoder (optional)
```

## Creating Your First Custom Workflow

Let's build a complete text-to-image workflow:

### Step 1: Add Core Nodes

```python
# Right-click on canvas and add:
# 1. "Load Checkpoint" - For model loading
# 2. "CLIP Text Encode" - For prompt processing
# 3. "Empty Latent Image" - For image dimensions
# 4. "KSampler" - For generation
# 5. "VAE Decode" - For image reconstruction
# 6. "Save Image" - For output
```

### Step 2: Connect the Nodes

```python
# Connect in this order:
# Load Checkpoint → CLIP Text Encode (MODEL)
# Load Checkpoint → KSampler (MODEL)
# CLIP Text Encode → KSampler (CONDITIONING)
# Empty Latent Image → KSampler (LATENT)
# KSampler → VAE Decode (LATENT)
# Load Checkpoint → VAE Decode (VAE)
# VAE Decode → Save Image (IMAGE)
```

### Step 3: Configure Parameters

```python
# CLIP Text Encode:
text = "masterpiece, best quality, highly detailed digital art of a cyberpunk city at night, neon lights, flying cars, 8k resolution"

# Empty Latent Image:
width = 1024
height = 1024

# KSampler:
steps = 25
cfg = 8.0
sampler_name = "euler_ancestral"
scheduler = "karras"
denoise = 1.0
seed = 12345  # For reproducible results
```

### Step 4: Execute the Workflow

1. Click "Queue Prompt"
2. Monitor progress in the console
3. View results in the output directory

## Advanced Features

### Custom Node Installation

```bash
# Install custom nodes from GitHub
cd ComfyUI/custom_nodes

# Example: Install ControlNet extension
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git

# Restart ComfyUI to load new nodes
```

### Workflow Templates

```python
# Save and load workflow templates
# 1. Build your workflow
# 2. Click "Save" to export as JSON
# 3. Click "Load" to import saved workflows

# Template structure:
workflow = {
    "nodes": [...],  # Node definitions
    "links": [...],  # Node connections
    "groups": [...], # Node groups
    "config": {...}  # Workflow settings
}
```

### Batch Processing

```python
# Process multiple prompts/images
# 1. Use "Text Batch" node for multiple prompts
# 2. Use "Image Batch" node for multiple inputs
# 3. Configure batch size in KSampler
# 4. Queue for automatic processing
```

## Performance Optimization

### Memory Management

```python
# Optimize for your hardware
memory_settings = {
    "batch_size": 1,  # Reduce for low VRAM
    "resolution": (512, 512),  # Lower for faster generation
    "precision": "fp16",  # Use half precision
    "attention_slicing": True,  # Reduce memory usage
    "xformers": True  # Faster attention (if available)
}
```

### GPU Acceleration

```python
# Ensure CUDA is properly configured
# Check GPU usage in task manager
# Use appropriate batch sizes for your GPU
# Monitor VRAM usage during generation
```

## Troubleshooting Common Issues

### Model Loading Errors

```python
# Check model file paths
# Verify model compatibility
# Update ComfyUI to latest version
# Check console for detailed error messages
```

### Out of Memory Errors

```python
# Reduce batch size
# Lower resolution
# Use smaller models
# Enable attention slicing
# Close other applications
```

### Node Connection Issues

```python
# Check node compatibility
# Verify input/output types
# Update custom nodes
# Check console for connection errors
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed ComfyUI** and launched the interface
2. **Created your first AI-generated image** using the node-based workflow
3. **Learned the core architecture** and component relationships
4. **Understood essential concepts** like latent space and sampling
5. **Set up model management** and configuration
6. **Built a complete custom workflow** from scratch
7. **Explored advanced features** like custom nodes and batch processing
8. **Optimized performance** for your hardware setup

## Next Steps

Now that you have ComfyUI running and understand the basics, let's dive deeper into the node system and workflow creation. In [Chapter 2: Understanding Nodes & Workflows](02-nodes-workflows.md), we'll explore the vast library of nodes available and learn how to create more sophisticated workflows.

---

**Practice what you've learned:**
1. Experiment with different prompts and parameters
2. Try different sampling methods and CFG scales
3. Create variations of your basic workflow
4. Explore the node library and try new components

*What's the most impressive AI-generated image you've seen, and how would you recreate it in ComfyUI?* 🎨

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `models`, `Image`, `ComfyUI` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with ComfyUI` as an operating subsystem inside **ComfyUI Tutorial: Mastering AI Image Generation Workflows**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `node`, `KSampler`, `Node` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with ComfyUI` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `models`.
2. **Input normalization**: shape incoming data so `Image` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `ComfyUI`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/comfyanonymous/ComfyUI)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `models` and `Image` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Understanding Nodes & Workflows](02-nodes-workflows.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
