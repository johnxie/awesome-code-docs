---
layout: default
title: "Chapter 7: Fine-tuning Models"
parent: "HuggingFace Transformers Tutorial"
nav_order: 7
---

# Chapter 7: Fine-tuning Models

> Customize pre-trained models for your specific tasks and domains.

## 🎯 Overview

This chapter covers fine-tuning techniques for adapting pre-trained Transformer models to specific tasks and domains. You'll learn to customize models for better performance on your data while avoiding common pitfalls.

## 🏗️ Fine-tuning Fundamentals

### When to Fine-tune

```python
# Decision framework for fine-tuning
def should_fine_tune(task_complexity, data_size, domain_similarity):
    """
    Determine if fine-tuning is appropriate

    Args:
        task_complexity: How specialized is your task?
        data_size: How much labeled data do you have?
        domain_similarity: How similar is your domain to pre-training data?

    Returns:
        Recommendation with confidence score
    """

    score = 0

    # Task complexity factor
    if task_complexity == "general":
        score += 0.2
    elif task_complexity == "specific":
        score += 0.5
    elif task_complexity == "highly_specialized":
        score += 0.8

    # Data size factor
    if data_size < 100:
        score += 0.1
    elif 100 <= data_size < 1000:
        score += 0.3
    elif 1000 <= data_size < 10000:
        score += 0.6
    else:  # 10000+
        score += 0.9

    # Domain similarity factor
    if domain_similarity == "very_similar":
        score += 0.1
    elif domain_similarity == "somewhat_similar":
        score += 0.4
    elif domain_similarity == "different":
        score += 0.7

    if score >= 0.8:
        return "Strongly recommend fine-tuning", score
    elif score >= 0.5:
        return "Consider fine-tuning", score
    else:
        return "Use pre-trained model as-is", score

# Example usage
recommendation, confidence = should_fine_tune(
    task_complexity="highly_specialized",
    data_size=5000,
    domain_similarity="somewhat_similar"
)
print(f"Recommendation: {recommendation} (confidence: {confidence:.2f})")
```

## 🔧 Basic Fine-tuning Setup

### Text Classification Fine-tuning

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import torch

class TextClassificationFineTuner:
    def __init__(self, model_name="bert-base-uncased", num_labels=2):
        self.model_name = model_name
        self.num_labels = num_labels

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels
        )

        # Add padding token if needed
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def prepare_dataset(self, texts, labels):
        """Prepare dataset for training"""
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=512
            )

        # Create dataset
        dataset = Dataset.from_dict({
            "text": texts,
            "label": labels
        })

        # Tokenize
        tokenized_dataset = dataset.map(tokenize_function, batched=True)

        # Set format for PyTorch
        tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

        return tokenized_dataset

    def fine_tune(self, train_dataset, eval_dataset=None, output_dir="./fine-tuned-model"):
        """Fine-tune the model"""
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch" if eval_dataset else "no",
            save_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
            compute_metrics=self._compute_metrics,
        )

        # Train the model
        trainer.train()

        # Save the model
        trainer.save_model(output_dir)

        return trainer

    def _compute_metrics(self, eval_pred):
        """Compute evaluation metrics"""
        predictions, labels = eval_pred
        predictions = predictions.argmax(axis=1)

        accuracy = (predictions == labels).mean()

        return {
            "accuracy": accuracy,
            "predictions": predictions,
            "labels": labels
        }

    def predict(self, texts):
        """Make predictions with fine-tuned model"""
        # Tokenize input
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        # Make predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits.argmax(dim=1)

        return predictions.tolist()

# Usage example
fine_tuner = TextClassificationFineTuner(model_name="bert-base-uncased", num_labels=3)

# Sample data
texts = [
    "This movie was excellent!",
    "I didn't like this product.",
    "The service was okay, nothing special.",
] * 10  # Repeat for more data

labels = [2, 0, 1] * 10  # 2=positive, 0=negative, 1=neutral

# Prepare dataset
dataset = fine_tuner.prepare_dataset(texts, labels)

# Split into train/eval
train_dataset = dataset.select(range(len(dataset) // 2))
eval_dataset = dataset.select(range(len(dataset) // 2, len(dataset)))

# Fine-tune
trainer = fine_tuner.fine_tune(train_dataset, eval_dataset, "./sentiment-model")

# Make predictions
test_texts = ["This is amazing!", "I hate this.", "It's decent."]
predictions = fine_tuner.predict(test_texts)
print(f"Predictions: {predictions}")
```

## 🎯 Advanced Fine-tuning Techniques

### LoRA (Low-Rank Adaptation)

```python
from peft import LoraConfig, get_peft_model, TaskType

class LoRAFineTuner:
    def __init__(self, base_model_name="gpt2", lora_rank=8):
        self.base_model_name = base_model_name
        self.lora_rank = lora_rank

        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(base_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)

        # Configure LoRA
        self.lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=lora_rank,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["c_attn", "c_proj", "c_fc"]  # GPT-2 specific
        )

        # Apply LoRA
        self.model = get_peft_model(self.model, self.lora_config)

        print(f"Trainable parameters: {self.model.print_trainable_parameters()}")

    def prepare_generation_dataset(self, texts):
        """Prepare dataset for generation fine-tuning"""
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=512,
                return_tensors="pt"
            )

        dataset = Dataset.from_dict({"text": texts})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask"])

        return tokenized_dataset

    def fine_tune_generation(self, train_dataset, output_dir="./lora-model"):
        """Fine-tune with LoRA for generation"""
        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            num_train_epochs=3,
            learning_rate=2e-4,
            fp16=True,  # Use mixed precision
            logging_steps=10,
            save_steps=500,
            save_total_limit=2,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=self._data_collator,
        )

        trainer.train()
        trainer.save_model(output_dir)

        return trainer

    def _data_collator(self, features):
        """Custom data collator for generation"""
        batch = self.tokenizer.pad(features, return_tensors="pt")

        # Create labels for language modeling
        batch["labels"] = batch["input_ids"].clone()

        return batch

    def generate_with_lora(self, prompt, max_length=100):
        """Generate text with fine-tuned LoRA model"""
        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text

# Usage
lora_tuner = LoRAFineTuner(base_model_name="gpt2-medium", lora_rank=16)

# Sample training data
training_texts = [
    "The future of AI is bright because",
    "Machine learning helps us",
    "Natural language processing enables",
] * 50  # Repeat for more data

train_dataset = lora_tuner.prepare_generation_dataset(training_texts)
trainer = lora_tuner.fine_tune_generation(train_dataset, "./lora-ai-writer")

# Generate text
prompt = "The benefits of artificial intelligence include"
generated = lora_tuner.generate_with_lora(prompt)
print(f"Generated: {generated}")
```

### Quantization-Aware Training

```python
from torch.quantization import QuantStub, DeQuantStub
import torch.quantization as quant

class QuantizationAwareFineTuner:
    def __init__(self, model_name="bert-base-uncased"):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Prepare model for quantization
        self.model.qconfig = quant.get_default_qat_qconfig('fbgemm')
        quant.prepare_qat(self.model, inplace=True)

    def fine_tune_with_quantization(self, train_dataset, eval_dataset):
        """Fine-tune with quantization awareness"""
        training_args = TrainingArguments(
            output_dir="./quantized-model",
            per_device_train_batch_size=8,
            num_train_epochs=2,
            learning_rate=1e-5,  # Lower learning rate for QAT
            logging_steps=10,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )

        # Fine-tune with quantization
        trainer.train()

        # Convert to quantized model
        quantized_model = quant.convert(self.model.eval(), inplace=False)

        return quantized_model

    def save_quantized_model(self, model, path="./quantized-model"):
        """Save quantized model"""
        torch.save(model.state_dict(), f"{path}/pytorch_model_quantized.bin")

        # Save tokenizer
        self.tokenizer.save_pretrained(path)

        # Save quantization config
        with open(f"{path}/quantization_config.json", "w") as f:
            json.dump({
                "quantization": "dynamic",
                "bits": 8
            }, f)
```

## 📊 Domain Adaptation

### Continued Pre-training

```python
class DomainAdapter:
    def __init__(self, base_model_name="bert-base-uncased"):
        self.model = AutoModelForMaskedLM.from_pretrained(base_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    def continued_pretraining(self, domain_texts, output_dir="./domain-adapted-model"):
        """Continue pre-training on domain-specific data"""
        # Prepare dataset
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=512,
                return_special_tokens_mask=True
            )

        dataset = Dataset.from_dict({"text": domain_texts})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)

        # Data collator for masked LM
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=True,
            mlm_probability=0.15
        )

        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=8,
            num_train_epochs=1,  # Usually 1 epoch for continued pre-training
            learning_rate=5e-5,
            weight_decay=0.01,
            save_steps=500,
            save_total_limit=2,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )

        trainer.train()
        trainer.save_model(output_dir)

        return trainer

# Usage
domain_texts = [
    "Machine learning algorithms optimize model performance.",
    "Neural networks process data through interconnected layers.",
    "Deep learning uses multiple hidden layers for complex pattern recognition.",
] * 100  # Domain-specific texts

adapter = DomainAdapter()
trainer = adapter.continued_pretraining(domain_texts, "./ml-domain-model")
```

## 🔍 Evaluation and Validation

### Comprehensive Model Evaluation

```python
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class ModelEvaluator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def evaluate_model(self, test_dataset, task_type="classification"):
        """Comprehensive model evaluation"""
        predictions, labels = self._get_predictions_and_labels(test_dataset)

        # Calculate metrics
        if task_type == "classification":
            report = classification_report(labels, predictions, output_dict=True)
            cm = confusion_matrix(labels, predictions)

            return {
                "classification_report": report,
                "confusion_matrix": cm,
                "accuracy": report["accuracy"],
                "macro_f1": report["macro avg"]["f1-score"]
            }

        elif task_type == "generation":
            # Generation-specific metrics
            bleu_score = self._calculate_bleu(predictions, labels)
            perplexity = self._calculate_perplexity(test_dataset)

            return {
                "bleu_score": bleu_score,
                "perplexity": perplexity
            }

    def _get_predictions_and_labels(self, dataset):
        """Get predictions and true labels"""
        predictions = []
        labels = []

        self.model.eval()

        for batch in dataset:
            inputs = {k: v.to(self.model.device) for k, v in batch.items() if k != "label"}

            with torch.no_grad():
                outputs = self.model(**inputs)

            if hasattr(outputs, "logits"):  # Classification
                preds = outputs.logits.argmax(dim=1).cpu().numpy()
                predictions.extend(preds)
            else:  # Generation
                generated = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
                predictions.extend(generated)

            if "label" in batch:
                labels.extend(batch["label"].cpu().numpy())

        return predictions, labels

    def _calculate_bleu(self, predictions, references):
        """Calculate BLEU score for generation tasks"""
        from nltk.translate.bleu_score import corpus_bleu

        # Tokenize predictions and references
        pred_tokens = [pred.split() for pred in predictions]
        ref_tokens = [[ref.split()] for ref in references]

        bleu = corpus_bleu(ref_tokens, pred_tokens)
        return bleu

    def _calculate_perplexity(self, dataset):
        """Calculate perplexity for language models"""
        total_loss = 0
        total_tokens = 0

        for batch in dataset:
            inputs = {k: v.to(self.model.device) for k, v in batch.items()}

            with torch.no_grad():
                outputs = self.model(**inputs, labels=inputs["input_ids"])
                loss = outputs.loss

            total_loss += loss.item() * inputs["input_ids"].size(1)
            total_tokens += inputs["input_ids"].size(1)

        perplexity = torch.exp(torch.tensor(total_loss / total_tokens))
        return perplexity.item()

    def plot_confusion_matrix(self, cm, class_names):
        """Plot confusion matrix"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('./confusion_matrix.png')
        plt.show()

# Usage
evaluator = ModelEvaluator(model, tokenizer)

# For classification
results = evaluator.evaluate_model(test_dataset, task_type="classification")
print(f"Accuracy: {results['accuracy']:.3f}")
print(f"Macro F1: {results['macro_f1']:.3f}")

# Plot confusion matrix
class_names = ["negative", "neutral", "positive"]
evaluator.plot_confusion_matrix(results['confusion_matrix'], class_names)
```

## 🚀 Hyperparameter Optimization

### Automated Hyperparameter Tuning

```python
from transformers import TrainerCallback
import optuna

class HyperparameterOptimizer:
    def __init__(self, model_class, tokenizer, train_dataset, eval_dataset):
        self.model_class = model_class
        self.tokenizer = tokenizer
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset

    def optimize_hyperparameters(self, n_trials=20):
        """Optimize hyperparameters using Optuna"""
        def objective(trial):
            # Define hyperparameter search space
            learning_rate = trial.suggest_float("learning_rate", 1e-5, 5e-4, log=True)
            batch_size = trial.suggest_categorical("batch_size", [8, 16, 32])
            weight_decay = trial.suggest_float("weight_decay", 0.0, 0.3)
            num_epochs = trial.suggest_int("num_epochs", 2, 5)

            # Create model
            model = self.model_class.from_pretrained("bert-base-uncased", num_labels=3)

            # Training arguments
            training_args = TrainingArguments(
                output_dir="./optuna-trial",
                learning_rate=learning_rate,
                per_device_train_batch_size=batch_size,
                weight_decay=weight_decay,
                num_train_epochs=num_epochs,
                evaluation_strategy="epoch",
                save_strategy="no",
                logging_steps=50,
            )

            # Trainer
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=self.train_dataset,
                eval_dataset=self.eval_dataset,
                compute_metrics=lambda eval_pred: {
                    "accuracy": (eval_pred.predictions.argmax(axis=1) == eval_pred.label_ids).mean()
                }
            )

            # Train and evaluate
            trainer.train()
            eval_results = trainer.evaluate()

            return eval_results["eval_accuracy"]

        # Run optimization
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials)

        # Get best parameters
        best_params = study.best_params
        best_accuracy = study.best_value

        return best_params, best_accuracy

# Usage
optimizer = HyperparameterOptimizer(
    AutoModelForSequenceClassification,
    tokenizer,
    train_dataset,
    eval_dataset
)

best_params, best_accuracy = optimizer.optimize_hyperparameters(n_trials=10)
print(f"Best parameters: {best_params}")
print(f"Best accuracy: {best_accuracy:.4f}")
```

## 🛠️ Best Practices for Fine-tuning

### Data Preparation

1. **Quality over Quantity**: Ensure high-quality, relevant training data
2. **Data Augmentation**: Use techniques like back-translation for small datasets
3. **Balanced Classes**: Ensure balanced representation across classes
4. **Data Cleaning**: Remove noise, duplicates, and irrelevant content

### Training Strategies

1. **Progressive Learning Rates**: Start with smaller LR, increase gradually
2. **Early Stopping**: Monitor validation metrics to prevent overfitting
3. **Gradient Clipping**: Prevent gradient explosion in unstable training
4. **Mixed Precision**: Use FP16 for faster training and lower memory usage

### Model Optimization

1. **LoRA for Efficiency**: Use parameter-efficient fine-tuning
2. **Quantization**: Apply quantization for deployment efficiency
3. **Pruning**: Remove unnecessary parameters post-training
4. **Knowledge Distillation**: Compress large models into smaller ones

## 📈 Next Steps

With fine-tuning mastered, you're ready for:

- **[Chapter 8: Production Deployment](08-production-deployment.md)** - Deploy your fine-tuned models at scale

---

**Ready to deploy your custom AI models? Continue to [Chapter 8: Production Deployment](08-production-deployment.md)!** 🚀