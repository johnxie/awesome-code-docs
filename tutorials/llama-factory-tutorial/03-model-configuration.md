---
layout: default
title: "Chapter 3: Model Configuration"
parent: "LLaMA Factory Tutorial"
nav_order: 3
---

# Chapter 3: Model Configuration

Welcome to the heart of fine-tuning! This chapter covers everything you need to know about configuring LLaMA models for optimal performance. We'll explore model selection, parameter tuning, quantization, and deployment strategies.

## Understanding LLaMA Architecture

LLaMA models come in different sizes and variants, each optimized for specific use cases:

### Model Variants and Capabilities

```python
# Available LLaMA model configurations
MODEL_CONFIGS = {
    'llama-7b': {
        'parameters': 7_000_000_000,
        'context_length': 4096,
        'memory_requirements': '14GB VRAM',
        'use_cases': ['text generation', 'chat', 'instruction following']
    },
    'llama-13b': {
        'parameters': 13_000_000_000,
        'context_length': 4096,
        'memory_requirements': '26GB VRAM',
        'use_cases': ['complex reasoning', 'code generation', 'analysis']
    },
    'llama-30b': {
        'parameters': 30_000_000_000,
        'context_length': 4096,
        'memory_requirements': '60GB VRAM',
        'use_cases': ['enterprise applications', 'advanced reasoning']
    },
    'llama-65b': {
        'parameters': 65_000_000_000,
        'context_length': 4096,
        'memory_requirements': '130GB VRAM',
        'use_cases': ['cutting-edge research', 'large-scale applications']
    }
}
```

## Model Selection Strategy

### Choosing the Right Model Size

```python
def select_optimal_model(task_requirements: dict) -> str:
    """
    Select the best LLaMA model based on task requirements

    Args:
        task_requirements: Dict containing task specifications
    Returns:
        Recommended model name
    """

    # Extract requirements
    max_context = task_requirements.get('max_context_length', 2048)
    complexity = task_requirements.get('task_complexity', 'medium')
    available_vram = task_requirements.get('available_vram_gb', 24)
    latency_requirement = task_requirements.get('latency_ms', 1000)

    # Model selection logic
    if complexity == 'simple' and available_vram >= 14:
        return 'llama-7b'
    elif complexity == 'medium' and available_vram >= 26:
        return 'llama-13b'
    elif complexity == 'high' and available_vram >= 60:
        return 'llama-30b'
    elif complexity == 'extreme' and available_vram >= 130:
        return 'llama-65b'
    else:
        # Fallback with quantization
        return 'llama-13b-quantized'

# Usage
requirements = {
    'max_context_length': 4096,
    'task_complexity': 'medium',
    'available_vram_gb': 24,
    'latency_ms': 500
}

recommended_model = select_optimal_model(requirements)
print(f"Recommended model: {recommended_model}")
```

## Configuration Files

### LLaMA Factory Training Configuration

```python
# train_config.yaml
model_name_or_path: meta-llama/Llama-2-7b-hf
data_path: ./data/train.json
eval_data_path: ./data/eval.json
output_dir: ./output/llama-2-7b-finetuned
overwrite_output_dir: true

# Model configuration
model_max_length: 2048
use_fast_tokenizer: true
trust_remote_code: true

# Training hyperparameters
per_device_train_batch_size: 4
per_device_eval_batch_size: 4
gradient_accumulation_steps: 8
learning_rate: 2.0e-5
weight_decay: 0.01
adam_beta1: 0.9
adam_beta2: 0.999
adam_epsilon: 1.0e-8
lr_scheduler_type: cosine
warmup_ratio: 0.1
num_train_epochs: 3
max_steps: -1
save_steps: 500
eval_steps: 500
logging_steps: 100

# Precision and optimization
fp16: true
bf16: false
gradient_checkpointing: true
optim: adamw_torch

# Data processing
preprocessing_num_workers: 4
dataloader_num_workers: 4
dataloader_pin_memory: true

# Validation and early stopping
evaluation_strategy: steps
save_strategy: steps
load_best_model_at_end: true
metric_for_best_model: eval_loss
greater_is_better: false

# LoRA configuration
use_lora: true
lora_rank: 8
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
```

### Advanced Configuration Options

```yaml
# advanced_config.yaml
# Memory optimization
gradient_checkpointing: true
optim: adamw_bnb_8bit  # 8-bit optimizer for memory efficiency

# Quantization
quantization_bit: 8
quantization_type: nf4
double_quantization: true

# Advanced LoRA
lora_rank: 16
lora_alpha: 32
lora_dropout: 0.1
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj
  - embed_tokens
  - lm_head

# Task-specific configurations
task_type: instruction_tuning
instruction_template: alpaca
response_template: <|assistant|>

# Multi-task learning
task_weights:
  instruction_tuning: 1.0
  continuation: 0.3
  summarization: 0.2

# Custom tokenization
additional_special_tokens: ["<|system|>", "<|user|>", "<|assistant|>"]
tokenizer_padding_side: left
tokenizer_truncation_side: right
```

## Quantization Strategies

### 4-bit Quantization Setup

```python
from transformers import BitsAndBytesConfig
import torch

def create_quantization_config(quantization_type: str = "nf4"):
    """Create quantization configuration for memory efficiency"""

    if quantization_type == "nf4":
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    elif quantization_type == "fp4":
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="fp4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    else:
        return BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_compute_dtype=torch.float16
        )

# Usage in training script
quantization_config = create_quantization_config("nf4")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto",
    trust_remote_code=True
)
```

### Dynamic Quantization

```python
def apply_dynamic_quantization(model, quantization_type: str = "dynamic"):
    """Apply dynamic quantization for inference optimization"""

    if quantization_type == "dynamic":
        # Dynamic quantization
        model = torch.quantization.quantize_dynamic(
            model,
            {torch.nn.Linear},  # Quantize linear layers
            dtype=torch.qint8
        )
    elif quantization_type == "static":
        # Static quantization (more complex setup required)
        model.eval()
        model = torch.quantization.prepare(model, inplace=False)
        # Calibration step would go here
        model = torch.quantization.convert(model, inplace=False)

    return model

# Memory usage comparison
print("Original model memory:", get_model_memory_usage(model))
quantized_model = apply_dynamic_quantization(model)
print("Quantized model memory:", get_model_memory_usage(quantized_model))
```

## LoRA Configuration

### Advanced LoRA Setup

```python
from peft import LoraConfig, get_peft_model

def create_advanced_lora_config(model_name: str):
    """Create optimized LoRA configuration"""

    # Determine target modules based on model architecture
    if "llama" in model_name.lower():
        target_modules = [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ]
    elif "mistral" in model_name.lower():
        target_modules = [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ]
    else:
        # Generic target modules
        target_modules = ["query", "key", "value", "dense"]

    lora_config = LoraConfig(
        r=16,  # Rank
        lora_alpha=32,  # Alpha parameter
        lora_dropout=0.1,  # Dropout probability
        bias="none",  # Bias configuration
        task_type="CAUSAL_LM",  # Task type
        target_modules=target_modules,
        modules_to_save=["embed_tokens", "lm_head"]  # Save specific modules
    )

    return lora_config

# Apply LoRA to model
lora_config = create_advanced_lora_config("meta-llama/Llama-2-7b-hf")
model = get_peft_model(model, lora_config)

# Print trainable parameters
model.print_trainable_parameters()
```

### LoRA Hyperparameter Tuning

```python
def tune_lora_hyperparameters(train_dataset, eval_dataset):
    """Tune LoRA hyperparameters using grid search"""

    lora_configs = [
        {"r": 8, "lora_alpha": 16, "lora_dropout": 0.05},
        {"r": 16, "lora_alpha": 32, "lora_dropout": 0.1},
        {"r": 32, "lora_alpha": 64, "lora_dropout": 0.1},
        {"r": 64, "lora_alpha": 128, "lora_dropout": 0.2}
    ]

    best_config = None
    best_score = float('inf')

    for config in lora_configs:
        print(f"Testing LoRA config: {config}")

        # Train with current config
        trainer = create_trainer_with_config(config)
        trainer.train()

        # Evaluate
        eval_results = trainer.evaluate()
        score = eval_results["eval_loss"]

        if score < best_score:
            best_score = score
            best_config = config

    print(f"Best LoRA config: {best_config}")
    return best_config
```

## Training Optimization

### Memory-Efficient Training

```python
def optimize_training_memory(model, training_args):
    """Apply memory optimization techniques"""

    # Gradient checkpointing
    if hasattr(model, "gradient_checkpointing_enable"):
        model.gradient_checkpointing_enable()

    # Use 8-bit optimizer
    if training_args.optim == "adamw_bnb_8bit":
        try:
            import bitsandbytes as bnb
            training_args.optim = bnb.optim.AdamW8bit
        except ImportError:
            print("bitsandbytes not available, falling back to regular AdamW")

    # Enable FP16/BF16 training
    if torch.cuda.is_available():
        if torch.cuda.get_device_capability()[0] >= 8:  # Ampere or newer
            training_args.bf16 = True
        else:
            training_args.fp16 = True

    return model, training_args

# Memory monitoring
def monitor_training_memory():
    """Monitor GPU memory usage during training"""

    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3
        reserved = torch.cuda.memory_reserved() / 1024**3

        print(".2f")
        print(".2f")
        print(".2f")

    else:
        print("CUDA not available for memory monitoring")
```

## Model Evaluation and Validation

### Comprehensive Evaluation Suite

```python
from evaluate import load
import numpy as np

class ModelEvaluator:
    """Comprehensive model evaluation"""

    def __init__(self):
        self.metrics = {
            "perplexity": load("perplexity"),
            "rouge": load("rouge"),
            "bleu": load("bleu"),
            "bertscore": load("bertscore")
        }

    def evaluate_model(self, model, tokenizer, eval_dataset):
        """Run comprehensive evaluation"""

        results = {}

        # Perplexity evaluation
        perplexity = self.metrics["perplexity"].compute(
            model=model,
            tokenizer=tokenizer,
            data=eval_dataset
        )
        results["perplexity"] = perplexity["mean_perplexity"]

        # Generation quality metrics
        generated_texts = self.generate_sample_outputs(model, tokenizer, eval_dataset)

        # ROUGE scores
        rouge_scores = self.metrics["rouge"].compute(
            predictions=generated_texts["predictions"],
            references=generated_texts["references"]
        )
        results["rouge"] = rouge_scores

        # BLEU scores
        bleu_scores = self.metrics["bleu"].compute(
            predictions=generated_texts["predictions"],
            references=generated_texts["references"]
        )
        results["bleu"] = bleu_scores

        return results

    def generate_sample_outputs(self, model, tokenizer, dataset, num_samples=100):
        """Generate sample outputs for evaluation"""

        predictions = []
        references = []

        for i, sample in enumerate(dataset):
            if i >= num_samples:
                break

            # Generate prediction
            inputs = tokenizer(sample["instruction"], return_tensors="pt")
            outputs = model.generate(**inputs, max_length=100)
            prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)

            predictions.append(prediction)
            references.append(sample["output"])

        return {"predictions": predictions, "references": references}

# Usage
evaluator = ModelEvaluator()
results = evaluator.evaluate_model(model, tokenizer, eval_dataset)

print("Evaluation Results:")
for metric, score in results.items():
    print(f"{metric}: {score}")
```

## Production Model Preparation

### Model Export and Optimization

```python
def prepare_model_for_production(model_path: str, output_path: str):
    """Prepare model for production deployment"""

    # Load trained model
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Apply optimizations
    model = optimize_for_inference(model)

    # Quantize for production
    model = quantize_model(model, quantization_type="dynamic")

    # Save optimized model
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)

    # Create model card
    create_model_card(output_path, model_info={
        "base_model": "meta-llama/Llama-2-7b-hf",
        "task": "instruction-tuning",
        "fine_tuned_on": "custom_dataset",
        "quantization": "dynamic"
    })

    print(f"Production model saved to: {output_path}")

def optimize_for_inference(model):
    """Apply inference optimizations"""

    # Fuse layers where possible
    if hasattr(model, "fuse"):
        model.fuse()

    # Set to evaluation mode
    model.eval()

    # Disable gradient computation
    for param in model.parameters():
        param.requires_grad = False

    return model

def create_model_card(output_path: str, model_info: dict):
    """Create a model card for the fine-tuned model"""

    model_card = f"""
# Fine-tuned LLaMA Model

This model is a fine-tuned version of {model_info['base_model']} for {model_info['task']}.

## Model Details
- **Base Model**: {model_info['base_model']}
- **Task**: {model_info['task']}
- **Fine-tuned on**: {model_info['fine_tuned_on']}
- **Quantization**: {model_info['quantization']}

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("{output_path}")
tokenizer = AutoTokenizer.from_pretrained("{output_path}")

# Use the model for inference
```

## Training Details
- LoRA fine-tuning applied
- Quantized for efficient inference
- Optimized for production deployment
"""

    with open(f"{output_path}/README.md", "w") as f:
        f.write(model_card)
```

## What We've Accomplished

Excellent! 🚀 You've mastered model configuration for LLaMA Factory:

1. **Model selection** - Choosing optimal model sizes and variants
2. **Configuration files** - Advanced training and LoRA configurations
3. **Quantization strategies** - Memory-efficient model optimization
4. **LoRA setup** - Advanced parameter-efficient fine-tuning
5. **Training optimization** - Memory-efficient and fast training
6. **Model evaluation** - Comprehensive performance assessment
7. **Production preparation** - Optimized model deployment

## Next Steps

Ready to start training? In [Chapter 4: Training Pipeline](04-training-pipeline.md), we'll dive into the actual training process and monitoring!

---

**Practice what you've learned:**
1. Configure a model for your specific use case and hardware constraints
2. Experiment with different LoRA configurations and quantization levels
3. Set up comprehensive evaluation metrics for your task
4. Optimize a model for production deployment with quantization
5. Create automated model configuration scripts

*What's the most complex model configuration you've set up?* ⚙️

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `torch`, `llama` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Model Configuration` as an operating subsystem inside **LLaMA-Factory Tutorial: Unified Framework for LLM Training and Fine-tuning**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `print`, `quantization`, `tokenizer` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Model Configuration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `torch` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `llama`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/hiyouga/LLaMA-Factory)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `model` and `torch` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Data Preparation](02-data-preparation.md)
- [Next Chapter: Chapter 4: Training Pipeline](04-training-pipeline.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
