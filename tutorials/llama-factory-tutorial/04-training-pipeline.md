---
layout: default
title: "Chapter 4: Training Pipeline"
parent: "LLaMA Factory Tutorial"
nav_order: 4
---

# Chapter 4: Training Pipeline

Welcome to the training phase! This chapter covers the complete training pipeline for LLaMA Factory, from data loading to model training, monitoring, and optimization. We'll explore distributed training, hyperparameter tuning, and best practices for successful fine-tuning.

## Setting Up the Training Environment

### Hardware Requirements and Optimization

```python
def check_training_requirements(model_size: str, batch_size: int, sequence_length: int):
    """Check if hardware meets training requirements"""

    # Model memory requirements (approximate)
    model_memory = {
        '7b': 14,    # GB VRAM
        '13b': 26,
        '30b': 60,
        '65b': 130
    }

    # Calculate training memory requirements
    base_memory = model_memory.get(model_size, 14)

    # Memory per sample
    memory_per_sample = (sequence_length * 2 * 4) / (1024**3)  # Rough estimate

    # Total memory calculation
    total_memory = base_memory + (batch_size * memory_per_sample * 2)  # *2 for gradients

    # Optimizer memory (AdamW)
    optimizer_memory = base_memory * 1.5

    total_required = base_memory + total_memory + optimizer_memory

    print(f"Estimated VRAM required: {total_required:.1f}GB")
    print(f"Model size: {base_memory}GB")
    print(f"Training data: {total_memory:.1f}GB")
    print(f"Optimizer: {optimizer_memory:.1f}GB")

    return total_required

# Usage
requirements = check_training_requirements('7b', batch_size=4, sequence_length=2048)
```

### Distributed Training Setup

```python
def setup_distributed_training(num_gpus: int, strategy: str = "ddp"):
    """Set up distributed training configuration"""

    if strategy == "ddp":
        # DataParallel configuration
        training_args = {
            "ddp_find_unused_parameters": False,
            "ddp_broadcast_buffers": False,
            "dataparallel_pin_memory": True,
        }
    elif strategy == "deepspeed":
        # DeepSpeed configuration
        training_args = {
            "deepspeed": "ds_config.json",
            "local_rank": -1,
        }

        # Create DeepSpeed config
        create_deepspeed_config(num_gpus)

    return training_args

def create_deepspeed_config(num_gpus: int):
    """Create DeepSpeed configuration for efficient training"""

    config = {
        "train_batch_size": 8 * num_gpus,
        "gradient_accumulation_steps": 1,
        "steps_per_print": 100,
        "optimizer": {
            "type": "AdamW",
            "params": {
                "lr": 2e-5,
                "weight_decay": 0.01,
                "betas": [0.9, 0.999],
                "eps": 1e-8
            }
        },
        "scheduler": {
            "type": "WarmupDecayLR",
            "params": {
                "warmup_min_lr": 0,
                "warmup_max_lr": 2e-5,
                "warmup_num_steps": 500,
                "total_num_steps": 10000
            }
        },
        "fp16": {
            "enabled": True,
            "loss_scale": 0,
            "loss_scale_window": 1000,
            "hysteresis": 2,
            "min_loss_scale": 1
        },
        "zero_optimization": {
            "stage": 2,
            "allgather_partitions": True,
            "reduce_scatter": True,
            "allgather_bucket_size": 2e8,
            "reduce_bucket_size": 2e8,
            "overlap_comm": True,
            "contiguous_gradients": True
        }
    }

    with open('ds_config.json', 'w') as f:
        json.dump(config, f, indent=2)
```

## Data Loading and Processing

### Efficient Data Pipeline

```python
from torch.utils.data import DataLoader, Dataset
from transformers import DataCollatorForLanguageModeling
import torch

class InstructionDataset(Dataset):
    """Custom dataset for instruction tuning"""

    def __init__(self, data_path: str, tokenizer, max_length: int = 2048):
        self.tokenizer = tokenizer
        self.max_length = max_length

        # Load data
        with open(data_path, 'r') as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        # Format instruction and response
        if 'instruction' in item:
            # Alpaca format
            instruction = item['instruction']
            input_text = item.get('input', '')
            output = item['output']

            if input_text:
                prompt = f"Instruction: {instruction}\nInput: {input_text}\nResponse:"
            else:
                prompt = f"Instruction: {instruction}\nResponse:"
        else:
            # Conversation format
            messages = item['conversations']
            prompt = ""
            for msg in messages[:-1]:  # All except last
                prompt += f"{msg['from']}: {msg['value']}\n"
            prompt += f"{messages[-1]['from']}:"
            output = messages[-1]['value']

        # Tokenize
        full_text = prompt + output + self.tokenizer.eos_token

        tokenized = self.tokenizer(
            full_text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        # Create labels (mask instruction tokens for loss calculation)
        labels = tokenized['input_ids'].clone()
        instruction_tokens = self.tokenizer(prompt, return_tensors='pt')['input_ids']

        # Mask instruction part
        labels[:, :instruction_tokens.shape[1]] = -100

        return {
            'input_ids': tokenized['input_ids'].squeeze(),
            'attention_mask': tokenized['attention_mask'].squeeze(),
            'labels': labels.squeeze()
        }

def create_data_loader(data_path: str, tokenizer, batch_size: int, max_length: int = 2048):
    """Create optimized data loader"""

    dataset = InstructionDataset(data_path, tokenizer, max_length)

    # Custom collate function for efficient batching
    def collate_fn(batch):
        input_ids = torch.stack([item['input_ids'] for item in batch])
        attention_mask = torch.stack([item['attention_mask'] for item in batch])
        labels = torch.stack([item['labels'] for item in batch])

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

    data_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=4,
        pin_memory=True,
        prefetch_factor=2
    )

    return data_loader
```

## Training Loop Implementation

### Custom Training Loop with Monitoring

```python
import torch
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from transformers import get_linear_schedule_with_warmup
import wandb
from tqdm import tqdm

class LLaMATrainer:
    """Custom trainer for LLaMA fine-tuning"""

    def __init__(self, model, tokenizer, config):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config

        # Setup optimizer
        self.optimizer = AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )

        # Setup scheduler
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=config.warmup_steps,
            num_training_steps=config.num_training_steps
        )

        # Setup mixed precision
        self.scaler = torch.cuda.amp.GradScaler() if config.fp16 else None

        # Setup logging
        if config.use_wandb:
            wandb.init(project="llama-finetuning", config=config)

    def train(self, train_loader, eval_loader=None):
        """Main training loop"""

        self.model.train()
        best_loss = float('inf')

        for epoch in range(self.config.num_epochs):
            epoch_loss = 0
            progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}")

            for step, batch in enumerate(progress_bar):
                loss = self.training_step(batch)
                epoch_loss += loss.item()

                # Update progress bar
                progress_bar.set_postfix({'loss': f"{loss.item():.4f}"})

                # Logging
                if step % self.config.logging_steps == 0:
                    self.log_metrics({
                        'step': step,
                        'loss': loss.item(),
                        'learning_rate': self.scheduler.get_last_lr()[0],
                        'epoch': epoch
                    })

                # Evaluation
                if eval_loader and step % self.config.eval_steps == 0:
                    eval_loss = self.evaluate(eval_loader)
                    if eval_loss < best_loss:
                        best_loss = eval_loss
                        self.save_checkpoint(f"best_model_epoch_{epoch}")

                # Save checkpoint
                if step % self.config.save_steps == 0:
                    self.save_checkpoint(f"checkpoint_epoch_{epoch}_step_{step}")

            # End of epoch
            avg_epoch_loss = epoch_loss / len(train_loader)
            print(f"Epoch {epoch+1} completed. Average loss: {avg_epoch_loss:.4f}")

    def training_step(self, batch):
        """Single training step"""

        # Move to device
        batch = {k: v.to(self.config.device) for k, v in batch.items()}

        # Forward pass
        if self.scaler:
            with torch.cuda.amp.autocast():
                outputs = self.model(**batch)
                loss = outputs.loss

            # Backward pass
            self.scaler.scale(loss).backward()
            self.scaler.step(self.optimizer)
            self.scaler.update()
        else:
            outputs = self.model(**batch)
            loss = outputs.loss
            loss.backward()
            self.optimizer.step()

        self.optimizer.zero_grad()
        self.scheduler.step()

        return loss

    def evaluate(self, eval_loader):
        """Evaluate model on validation set"""

        self.model.eval()
        total_loss = 0

        with torch.no_grad():
            for batch in eval_loader:
                batch = {k: v.to(self.config.device) for k, v in batch.items()}
                outputs = self.model(**batch)
                total_loss += outputs.loss.item()

        avg_loss = total_loss / len(eval_loader)
        return avg_loss

    def log_metrics(self, metrics):
        """Log metrics to wandb and console"""

        if self.config.use_wandb:
            wandb.log(metrics)

        print(f"Step {metrics['step']}: Loss = {metrics['loss']:.4f}")

    def save_checkpoint(self, name: str):
        """Save model checkpoint"""

        checkpoint_path = f"{self.config.output_dir}/checkpoint_{name}"
        self.model.save_pretrained(checkpoint_path)
        self.tokenizer.save_pretrained(checkpoint_path)

        print(f"Checkpoint saved: {checkpoint_path}")
```

## Hyperparameter Optimization

### Automated Hyperparameter Search

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

def hyperparameter_search(train_func, search_space, num_samples=10):
    """Run hyperparameter search using Ray Tune"""

    scheduler = ASHAScheduler(
        max_t=100,
        grace_period=10,
        reduction_factor=2
    )

    analysis = tune.run(
        train_func,
        config=search_space,
        num_samples=num_samples,
        scheduler=scheduler,
        resources_per_trial={"cpu": 4, "gpu": 1},
        metric="eval_loss",
        mode="min"
    )

    best_config = analysis.get_best_config(metric="eval_loss", mode="min")
    print(f"Best hyperparameters: {best_config}")

    return best_config

# Define search space
search_space = {
    "learning_rate": tune.loguniform(1e-5, 1e-3),
    "batch_size": tune.choice([2, 4, 8, 16]),
    "lora_rank": tune.choice([8, 16, 32, 64]),
    "lora_alpha": tune.choice([16, 32, 64]),
    "warmup_ratio": tune.uniform(0.01, 0.2),
    "weight_decay": tune.loguniform(1e-4, 1e-1)
}

# Run search
best_config = hyperparameter_search(train_function, search_space)
```

## Monitoring and Logging

### Comprehensive Training Monitor

```python
import psutil
import GPUtil
from datetime import datetime

class TrainingMonitor:
    """Monitor training progress and system resources"""

    def __init__(self, log_interval: int = 100):
        self.log_interval = log_interval
        self.start_time = datetime.now()
        self.metrics_history = []

    def log_step(self, step: int, loss: float, lr: float):
        """Log metrics for current training step"""

        # System metrics
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        gpu_metrics = {}
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                gpu_metrics = {
                    'gpu_utilization': gpu.load * 100,
                    'gpu_memory_used': gpu.memoryUsed,
                    'gpu_memory_total': gpu.memoryTotal,
                    'gpu_temperature': gpu.temperature
                }
        except:
            pass

        # Training metrics
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        steps_per_second = step / elapsed_time if elapsed_time > 0 else 0

        metrics = {
            'step': step,
            'loss': loss,
            'learning_rate': lr,
            'elapsed_time': elapsed_time,
            'steps_per_second': steps_per_second,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            **gpu_metrics
        }

        self.metrics_history.append(metrics)

        # Log to console
        print(f"Step {step}: Loss={loss:.4f}, LR={lr:.2e}, GPU={gpu_metrics.get('gpu_utilization', 0):.1f}%")

        # Save metrics periodically
        if step % (self.log_interval * 10) == 0:
            self.save_metrics()

    def save_metrics(self):
        """Save metrics to file"""

        import pandas as pd

        df = pd.DataFrame(self.metrics_history)
        df.to_csv('training_metrics.csv', index=False)

        print(f"Metrics saved to training_metrics.csv ({len(self.metrics_history)} steps)")

    def plot_metrics(self):
        """Generate training plots"""

        import matplotlib.pyplot as plt

        if not self.metrics_history:
            return

        df = pd.DataFrame(self.metrics_history)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # Loss curve
        axes[0, 0].plot(df['step'], df['loss'])
        axes[0, 0].set_title('Training Loss')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Loss')

        # Learning rate
        axes[0, 1].plot(df['step'], df['learning_rate'])
        axes[0, 1].set_title('Learning Rate')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Learning Rate')

        # GPU utilization
        if 'gpu_utilization' in df.columns:
            axes[1, 0].plot(df['step'], df['gpu_utilization'])
            axes[1, 0].set_title('GPU Utilization')
            axes[1, 0].set_xlabel('Step')
            axes[1, 0].set_ylabel('GPU %')

        # Memory usage
        if 'gpu_memory_used' in df.columns:
            memory_usage = df['gpu_memory_used'] / df['gpu_memory_total'] * 100
            axes[1, 1].plot(df['step'], memory_usage)
            axes[1, 1].set_title('GPU Memory Usage')
            axes[1, 1].set_xlabel('Step')
            axes[1, 1].set_ylabel('Memory %')

        plt.tight_layout()
        plt.savefig('training_plots.png', dpi=300, bbox_inches='tight')
        plt.show()
```

## Handling Training Issues

### Common Problems and Solutions

```python
class TrainingDebugger:
    """Debug and fix common training issues"""

    def __init__(self, model, optimizer):
        self.model = model
        self.optimizer = optimizer

    def detect_nan_loss(self, loss):
        """Detect NaN loss values"""
        if torch.isnan(loss):
            print("WARNING: NaN loss detected!")
            return True
        return False

    def fix_gradient_explosion(self):
        """Handle gradient explosion"""
        total_norm = 0
        for p in self.model.parameters():
            if p.grad is not None:
                param_norm = p.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
        total_norm = total_norm ** (1. / 2)

        if total_norm > 10:  # Threshold for explosion
            print(f"Gradient explosion detected: {total_norm}")
            # Clip gradients
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            return True

        return False

    def detect_overfitting(self, train_loss, val_loss, patience=5):
        """Detect overfitting based on train/val loss divergence"""

        if len(val_loss) < patience:
            return False

        # Check if validation loss is consistently increasing
        recent_val = val_loss[-patience:]
        if all(recent_val[i] > recent_val[i-1] for i in range(1, len(recent_val))):
            print("Overfitting detected - consider early stopping")
            return True

        return False

    def adjust_learning_rate(self, current_loss, previous_loss):
        """Adjust learning rate based on loss trend"""

        if current_loss > previous_loss * 1.1:  # Loss increased significantly
            print("Loss increased - reducing learning rate")

            for param_group in self.optimizer.param_groups:
                param_group['lr'] *= 0.5

            return True

        return False

    def check_memory_usage(self):
        """Monitor memory usage and suggest optimizations"""

        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1024**3
            reserved = torch.cuda.memory_reserved() / 1024**3

            if allocated > 0.9 * reserved:
                print(f"High memory usage: {allocated:.1f}GB allocated, {reserved:.1f}GB reserved")
                print("Consider reducing batch size or enabling gradient checkpointing")
                return True

        return False
```

## Training Best Practices

### Curriculum Learning Strategy

```python
def implement_curriculum_learning(dataset, stages):
    """Implement curriculum learning with progressive difficulty"""

    # Sort data by difficulty
    sorted_data = sort_by_difficulty(dataset)

    # Define training stages
    curriculum_stages = [
        {
            'name': 'easy',
            'data_fraction': 0.3,
            'epochs': 2,
            'learning_rate': 2e-5
        },
        {
            'name': 'medium',
            'data_fraction': 0.6,
            'epochs': 3,
            'learning_rate': 1e-5
        },
        {
            'name': 'hard',
            'data_fraction': 1.0,
            'epochs': 5,
            'learning_rate': 5e-6
        }
    ]

    for stage in curriculum_stages:
        print(f"Starting curriculum stage: {stage['name']}")

        # Select subset of data
        stage_size = int(len(sorted_data) * stage['data_fraction'])
        stage_data = sorted_data[:stage_size]

        # Update training configuration
        update_training_config(stage)

        # Train on this stage
        trainer = LLaMATrainer(model, tokenizer, stage)
        trainer.train(stage_data)

        print(f"Completed stage: {stage['name']}")

def sort_by_difficulty(dataset):
    """Sort dataset by task difficulty"""

    def calculate_difficulty(item):
        # Simple heuristic: length + complexity
        text = item.get('instruction', '') + item.get('output', '')
        length_score = len(text)
        complexity_score = text.count('?') + text.count('and') + text.count('or')

        return length_score + complexity_score * 10

    return sorted(dataset, key=calculate_difficulty)
```

## What We've Accomplished

Excellent! 🎯 You've mastered the training pipeline for LLaMA Factory:

1. **Environment setup** - Hardware requirements and distributed training
2. **Data pipeline** - Efficient loading and processing
3. **Custom training loop** - Full control over training process
4. **Hyperparameter optimization** - Automated parameter search
5. **Monitoring system** - Comprehensive training metrics and logging
6. **Issue handling** - Debugging and fixing common training problems
7. **Best practices** - Curriculum learning and optimization strategies

## Next Steps

Ready to evaluate your trained models? In [Chapter 5: Model Evaluation](05-model-evaluation.md), we'll explore comprehensive evaluation techniques and performance metrics!

---

**Practice what you've learned:**
1. Set up a distributed training pipeline for large models
2. Implement comprehensive monitoring and logging for training
3. Create automated hyperparameter optimization
4. Build a curriculum learning strategy for your dataset
5. Debug and fix common training issues in your pipeline

*What's the most complex training setup you've implemented?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `loss`, `config` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Training Pipeline` as an operating subsystem inside **LLaMA-Factory Tutorial: Unified Framework for LLM Training and Fine-tuning**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `step`, `item`, `print` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Training Pipeline` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `loss` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `config`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/hiyouga/LLaMA-Factory)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `loss` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Model Configuration](03-model-configuration.md)
- [Next Chapter: Chapter 5: Model Evaluation](05-model-evaluation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
