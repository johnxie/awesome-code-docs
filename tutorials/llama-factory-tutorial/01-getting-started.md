---
layout: default
title: "Chapter 1: Getting Started with LLaMA-Factory"
parent: "LLaMA-Factory Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with LLaMA-Factory

Welcome to LLaMA-Factory! If you've ever wanted to train, fine-tune, or deploy large language models with a unified, easy-to-use framework, you're in the right place. LLaMA-Factory makes advanced LLM development accessible to everyone.

## What Makes LLaMA-Factory Powerful?

LLaMA-Factory revolutionizes LLM development by:
- **Unified Interface** - Single framework for training, fine-tuning, and deployment
- **Multiple Model Support** - Works with LLaMA, Qwen, and other architectures
- **Efficient Fine-tuning** - LoRA and other parameter-efficient methods
- **Production Ready** - Built for real-world deployment scenarios
- **Extensible Architecture** - Easy to add custom models and datasets
- **Research Friendly** - Supports latest training techniques

## Installation

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory

# Install dependencies
pip install -e .
```

### GPU Installation (Recommended)

```bash
# Install with CUDA support
pip install -e .[torch,metrics]
# or for specific CUDA version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Docker Installation

```bash
# Build Docker image
docker build -t llama-factory .

# Run container
docker run --gpus all -v $(pwd):/app llama-factory
```

## Your First Model Training

Let's train your first language model:

### Step 1: Prepare Dataset

```bash
# Create data directory
mkdir -p data

# Create a simple training dataset
cat > data/train.json << 'EOF'
[
  {"instruction": "What is 2+2?", "output": "4"},
  {"instruction": "What is the capital of France?", "output": "Paris"},
  {"instruction": "Explain machine learning", "output": "Machine learning is a subset of AI that enables computers to learn from data without being explicitly programmed."}
]
EOF
```

### Step 2: Configure Training

```python
# Create training configuration
import json

config = {
    "model_name_or_path": "microsoft/DialoGPT-small",
    "dataset": "your_dataset",
    "stage": "sft",  # Supervised Fine-Tuning
    "do_train": True,
    "finetuning_type": "lora",
    "lora_target": "all",
    "output_dir": "output",
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "lr_scheduler_type": "cosine",
    "logging_steps": 10,
    "save_steps": 100,
    "learning_rate": 5e-5,
    "num_train_epochs": 3,
    "max_samples": 1000,
    "max_grad_norm": 1.0,
    "warmup_steps": 0,
    "dataloader_num_workers": 0,
    "save_total_limit": 3
}

with open('train_config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

### Step 3: Start Training

```bash
# Train the model
llamafactory-cli train train_config.json

# Or use Python API
python -c "
from llamafactory.train.tuner import run_exp
run_exp('train_config.json')
"
```

### Step 4: Test Your Model

```python
# Load and test the trained model
from llamafactory.chat import ChatModel
from llamafactory.hparams import get_infer_args

# Load model
args = get_infer_args()
args.model_name_or_path = 'output'
args.adapter_name_or_path = 'output'

chat_model = ChatModel(args)

# Start chat
messages = []
while True:
    user_input = input('User: ')
    if user_input.lower() == 'quit':
        break

    messages.append({'role': 'user', 'content': user_input})
    response = chat_model.chat(messages)
    print(f'Assistant: {response}')
    messages.append({'role': 'assistant', 'content': response})
```

## Understanding LLaMA-Factory Architecture

### Core Components

```
LLaMA-Factory System
├── Data Processing
│   ├── Dataset Loading
│   ├── Text Tokenization
│   └── Data Formatting
├── Model Training
│   ├── Base Model Loading
│   ├── LoRA Adaptation
│   └── Training Loop
├── Inference Engine
│   ├── Model Loading
│   ├── Chat Interface
│   └── API Server
└── Utilities
    ├── Configuration
    ├── Logging
    └── Evaluation
```

### Supported Models

```python
# Supported model families
supported_models = {
    'LLaMA': ['llama-7b', 'llama-13b', 'llama-30b', 'llama-65b'],
    'Qwen': ['qwen-7b', 'qwen-14b', 'qwen-72b'],
    'Baichuan': ['baichuan-7b', 'baichuan-13b'],
    'ChatGLM': ['chatglm2-6b', 'chatglm3-6b'],
    'Other': ['bloom', 'gpt2', 'bert', 't5']
}
```

### Training Stages

```python
# Available training stages
stages = {
    'pt': 'Pre-training',
    'sft': 'Supervised Fine-tuning',
    'rm': 'Reward Modeling',
    'ppo': 'Proximal Policy Optimization',
    'dpo': 'Direct Preference Optimization'
}
```

## Command Line Interface

### Basic Commands

```bash
# Train a model
llamafactory-cli train config.json

# Chat with a model
llamafactory-cli chat --model_path output

# Export model
llamafactory-cli export --model_path output --export_path model.bin

# Evaluate model
llamafactory-cli eval --model_path output --dataset test.json
```

### Advanced Usage

```bash
# Multi-GPU training
llamafactory-cli train config.json --num_processes 4

# Resume training
llamafactory-cli train config.json --resume_from_checkpoint checkpoint-1000

# Custom dataset
llamafactory-cli train config.json --dataset your_custom_dataset
```

## Web Interface

LLaMA-Factory includes a web-based training interface:

```bash
# Start web UI
llamafactory-cli webui

# Access at http://localhost:7860
```

Features:
- **Visual Configuration** - GUI for training parameters
- **Real-time Monitoring** - Training progress and metrics
- **Model Management** - Upload and manage models
- **Dataset Browser** - Explore and validate datasets

## Configuration Deep Dive

### Training Configuration

```python
# Complete training configuration
full_config = {
    # Model settings
    "model_name_or_path": "microsoft/DialoGPT-small",
    "adapter_name_or_path": None,

    # Dataset settings
    "dataset": "alpaca_en_demo",
    "template": "default",
    "cutoff_len": 1024,
    "max_samples": 1000,

    # Training settings
    "stage": "sft",
    "do_train": True,
    "do_eval": False,
    "finetuning_type": "lora",

    # LoRA settings
    "lora_target": "all",
    "lora_rank": 8,
    "lora_alpha": 16,

    # Training hyperparameters
    "learning_rate": 5e-5,
    "num_train_epochs": 3.0,
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "warmup_steps": 0,
    "max_grad_norm": 1.0,
    "lr_scheduler_type": "cosine",

    # Output settings
    "output_dir": "output",
    "logging_steps": 10,
    "save_steps": 500,
    "save_total_limit": 3,
    "overwrite_output_dir": True,

    # Hardware settings
    "dataloader_num_workers": 0,
    "preprocessing_num_workers": 1,
    "fp16": True,
    "bf16": False
}
```

### Dataset Formats

```python
# Supported dataset formats
dataset_formats = {
    'alpaca': {
        'instruction': 'Human instruction',
        'input': 'Additional context (optional)',
        'output': 'Assistant response'
    },
    'sharegpt': {
        'conversations': [
            {'from': 'human', 'value': 'Question'},
            {'from': 'assistant', 'value': 'Answer'}
        ]
    }
}
```

## Performance Optimization

### Memory Optimization

```python
# Memory-efficient training settings
memory_config = {
    "per_device_train_batch_size": 1,
    "gradient_accumulation_steps": 8,
    "gradient_checkpointing": True,
    "fp16": True,
    "optim": "adamw_torch_fused"
}
```

### Multi-GPU Training

```python
# Distributed training configuration
distributed_config = {
    "num_processes": 4,
    "deepspeed_config": "ds_config.json"
}
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed LLaMA-Factory** and set up the development environment
2. **Created your first training dataset** with proper formatting
3. **Configured and trained a language model** using LoRA fine-tuning
4. **Tested the trained model** with an interactive chat interface
5. **Explored the command-line interface** and web UI
6. **Learned configuration options** for different training scenarios
7. **Understood performance optimization** techniques
8. **Set up the foundation** for advanced LLM development

## Next Steps

Now that you have LLaMA-Factory running, let's explore data preparation and processing. In [Chapter 2: Data Preparation & Processing](02-data-preparation.md), we'll dive into dataset formatting, preprocessing techniques, and data quality optimization.

---

**Practice what you've learned:**
1. Experiment with different model architectures
2. Try various training configurations and parameters
3. Create custom datasets for specific domains
4. Explore the web interface for visual training setup

*What kind of model are you most excited to train with LLaMA-Factory?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `json`, `llamafactory`, `output` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with LLaMA-Factory` as an operating subsystem inside **LLaMA-Factory Tutorial: Unified Framework for LLM Training and Fine-tuning**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `training`, `model`, `dataset` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with LLaMA-Factory` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `json`.
2. **Input normalization**: shape incoming data so `llamafactory` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `output`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/hiyouga/LLaMA-Factory)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `json` and `llamafactory` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Data Preparation](02-data-preparation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
