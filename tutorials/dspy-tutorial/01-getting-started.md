---
layout: default
title: "DSPy Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: DSPy Tutorial
---

# Chapter 1: Getting Started with DSPy

> Install DSPy, understand core concepts, and build your first program that automatically optimizes itself.

## Overview

DSPy introduces a paradigm shift in how we work with language models. Instead of manually crafting prompts through trial and error, DSPy allows you to write programs that specify what you want to accomplish, and the framework automatically figures out the best way to accomplish it.

## Installation and Setup

### Installing DSPy

```bash
# Install DSPy via pip
pip install dspy-ai

# For development and latest features
pip install git+https://github.com/stanfordnlp/dspy.git

# Optional: Install with specific ML frameworks
pip install dspy-ai[all]  # Includes torch, transformers, etc.
```

### Setting up API Keys

DSPy works with various language model providers. Let's set up the most common ones:

```python
import os

# OpenAI API (most common)
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Anthropic Claude
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key"

# Google Vertex AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

# Cohere
os.environ["COHERE_API_KEY"] = "your-cohere-api-key"

# Local models (Ollama, etc.)
# No API key needed for local models
```

## Core Concepts

### Language Models (LMs)

In DSPy, language models are abstracted as simple callable objects:

```python
import dspy

# OpenAI GPT models
gpt3 = dspy.OpenAI(model="gpt-3.5-turbo")
gpt4 = dspy.OpenAI(model="gpt-4", max_tokens=300)

# Anthropic Claude
claude = dspy.Claude(model="claude-3-sonnet-20240229")

# Local models via Ollama
ollama = dspy.OllamaLocal(model="llama2")

# Configure DSPy to use a specific LM
dspy.settings.configure(lm=gpt4)
```

### Retrieval Models (RMs)

For retrieval-augmented generation, DSPy supports various retrieval systems:

```python
# ColBERTv2 (neural retrieval)
rm_colbert = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")

# Pinecone vector database
rm_pinecone = dspy.Pinecone(
    index="my-index",
    api_key="your-pinecone-key",
    dimension=768
)

# Weaviate
rm_weaviate = dspy.Weaviate(
    url="http://localhost:8080",
    class_name="Document"
)

# Configure retrieval model
dspy.settings.configure(rm=rm_colbert)
```

## Your First DSPy Program

### Basic Prediction

The simplest DSPy program uses the `Predict` module:

```python
import dspy

# Configure DSPy (do this once at the start)
lm = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=lm)

# Define a signature (input/output specification)
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""

    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Create a program
qa_program = dspy.Predict(BasicQA)

# Use the program
question = "What is the capital of France?"
result = qa_program(question=question)

print(f"Question: {question}")
print(f"Answer: {result.answer}")
```

### Understanding Signatures

Signatures are the core abstraction in DSPy. They define what goes into and comes out of your LM calls:

```python
# Simple signature
class SimpleSignature(dspy.Signature):
    input_text = dspy.InputField()
    output_text = dspy.OutputField()

# Signature with descriptions
class DescriptiveSignature(dspy.Signature):
    """Process text and generate a summary."""

    text = dspy.InputField(desc="the input text to process")
    summary = dspy.OutputField(desc="a concise summary, usually 1-3 sentences")

# Multi-field signature
class ComplexSignature(dspy.Signature):
    """Analyze sentiment and extract key information."""

    text = dspy.InputField(desc="the text to analyze")
    sentiment = dspy.OutputField(desc="positive, negative, or neutral")
    key_topics = dspy.OutputField(desc="comma-separated list of main topics")
    confidence = dspy.OutputField(desc="confidence score between 0 and 1")
```

### Using Different Modules

DSPy provides several built-in modules beyond `Predict`:

```python
# Chain of Thought reasoning
cot_program = dspy.ChainOfThought(BasicQA)

# Multiple choice selection
class MultipleChoice(dspy.Signature):
    question = dspy.InputField()
    options = dspy.InputField(desc="comma-separated options")
    selected = dspy.OutputField(desc="selected option letter")

mc_program = dspy.Predict(MultipleChoice)

# Program of Thought (for math/computation)
class MathProblem(dspy.Signature):
    problem = dspy.InputField()
    solution = dspy.OutputField(desc="step-by-step solution")

math_program = dspy.ProgramOfThought(MathProblem)
```

## Automatic Optimization

### What Makes DSPy Special

Unlike traditional prompting, DSPy can automatically improve your programs:

```python
# Create a simple program
class BasicQA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

program = dspy.Predict(BasicQA)

# Before optimization: Manual prompt
result1 = program(question="What is machine learning?")
print(f"Before: {result1.answer}")

# DSPy can optimize this automatically!
# (We'll see how in later chapters)

# After optimization: Better prompts, better results
# result2 = optimized_program(question="What is machine learning?")
# print(f"After: {result2.answer}")
```

### The Optimization Loop

DSPy's optimization process:

1. **Define your task** - Specify what you want to accomplish
2. **Provide examples** - Give input-output examples (optional but helpful)
3. **Define metrics** - Specify how to evaluate success
4. **Run optimization** - DSPy automatically improves your program
5. **Deploy** - Use the optimized program in production

```python
# Example optimization setup (detailed in later chapters)
from dspy.teleprompt import BootstrapFewShot

# Define a simple metric
def validate_answer(example, prediction, trace=None):
    # Check if answer contains expected keywords
    return "machine" in prediction.answer.lower()

# Create optimizer
optimizer = BootstrapFewShot(metric=validate_answer)

# Optimize program (requires training data)
# optimized_program = optimizer.compile(program, trainset=train_examples)
```

## Working with Data

### Creating Datasets

DSPy works with simple Python data structures:

```python
# Create training examples
train_examples = [
    dspy.Example(question="What is AI?", answer="Artificial Intelligence"),
    dspy.Example(question="What is ML?", answer="Machine Learning"),
    dspy.Example(question="What is NLP?", answer="Natural Language Processing"),
]

# Create test examples
test_examples = [
    dspy.Example(question="What is CV?", answer="Computer Vision"),
    dspy.Example(question="What is RL?", answer="Reinforcement Learning"),
]

# DSPy can also load from various formats
# examples = dspy.load_dataset("path/to/data.json")
```

### Evaluation

Basic evaluation without optimization:

```python
# Evaluate program on test set
evaluator = dspy.Evaluate(
    devset=test_examples,
    metric=lambda ex, pred: pred.answer.lower() in ex.answer.lower(),
    num_threads=4
)

# Run evaluation
results = evaluator(program)
print(f"Accuracy: {results['accuracy']}")
```

## Advanced Configuration

### Custom Language Model Configuration

```python
# Advanced OpenAI configuration
lm_advanced = dspy.OpenAI(
    model="gpt-4",
    api_key="your-key",
    api_base="https://api.openai.com/v1",  # Custom endpoint
    max_tokens=1000,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model_type="chat"  # or "text" for completion models
)

# Using multiple LMs with automatic fallback
lm_fallback = dspy.OpenAI(
    model=["gpt-4", "gpt-3.5-turbo"],  # Try GPT-4 first, fallback to 3.5
    api_key="your-key"
)
```

### Caching and Performance

```python
# Enable caching for development
dspy.settings.configure(
    lm=lm,
    cache=True,  # Cache LM responses
    cache_dir="./dspy_cache"
)

# Disable caching for fresh results
dspy.settings.configure(lm=lm, cache=False)
```

### Debugging and Logging

```python
import logging

# Enable DSPy logging
logging.basicConfig(level=logging.INFO)
dspy_logger = logging.getLogger("dspy")
dspy_logger.setLevel(logging.DEBUG)

# View intermediate steps
with dspy.settings.trace():
    result = program(question="What is DSPy?")
    print("Trace:", dspy.settings.trace)  # Shows intermediate LM calls
```

## Common Patterns and Best Practices

### Error Handling

```python
def safe_predict(program, **kwargs):
    """Safe prediction with error handling"""
    try:
        result = program(**kwargs)
        return result
    except Exception as e:
        print(f"Error in prediction: {e}")
        # Return a default response or retry
        return type('Response', (), {'answer': 'I apologize, but I encountered an error.'})()

# Usage
result = safe_predict(qa_program, question="What is the capital of France?")
```

### Batch Processing

```python
def batch_predict(program, questions, batch_size=10):
    """Process multiple questions efficiently"""
    results = []

    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]

        for question in batch:
            try:
                result = program(question=question)
                results.append(result.answer)
            except Exception as e:
                results.append(f"Error: {e}")

    return results

# Usage
questions = ["What is AI?", "What is ML?", "What is DL?"]
answers = batch_predict(qa_program, questions)
for q, a in zip(questions, answers):
    print(f"Q: {q} -> A: {a}")
```

### Configuration Management

```python
# Centralized configuration
class DSPyConfig:
    def __init__(self):
        self.lm_configs = {
            "development": dspy.OpenAI(model="gpt-3.5-turbo", temperature=0.7),
            "production": dspy.OpenAI(model="gpt-4", temperature=0.1),
            "experimental": dspy.Claude(model="claude-3-sonnet-20240229")
        }

        self.current_config = "development"

    def set_config(self, config_name):
        """Switch configurations"""
        if config_name in self.lm_configs:
            lm = self.lm_configs[config_name]
            dspy.settings.configure(lm=lm)
            self.current_config = config_name
            print(f"Switched to {config_name} configuration")
        else:
            raise ValueError(f"Unknown configuration: {config_name}")

# Usage
config = DSPyConfig()
config.set_config("production")  # Switch to production settings
```

## Summary

In this chapter, we've covered:

- **Installation and Setup** - Getting DSPy running with your preferred LM provider
- **Core Concepts** - Language models, retrieval models, and DSPy settings
- **Basic Programs** - Creating your first DSPy programs with signatures and modules
- **Configuration** - Advanced LM setup, caching, and debugging
- **Best Practices** - Error handling, batch processing, and configuration management

DSPy represents a fundamental shift from manual prompt engineering to programmatic, optimizable LM interactions. The real power comes in the next chapters where we'll explore automatic optimization.

## Key Takeaways

1. **Declarative Programming**: Specify what you want, let DSPy optimize how
2. **Signatures**: Define input/output contracts for LM calls
3. **Modules**: Reusable components for common LM patterns
4. **Configuration**: Flexible setup for different environments
5. **Optimization**: DSPy can automatically improve your programs

Next, we'll dive deep into **signatures** - the foundation of DSPy programming.

---

**Ready for the next chapter?** [Chapter 2: Signatures](02-signatures.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*