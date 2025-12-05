---
layout: default
title: "llama.cpp Tutorial - Chapter 7: Advanced Features"
nav_order: 7
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 7: Advanced Features

> Explore grammar-based generation, embeddings, multimodal models, and custom extensions.

## Overview

Beyond basic text generation, llama.cpp supports advanced features like structured output, embeddings, and multimodal capabilities. This chapter covers these advanced use cases.

## Grammar-Based Generation

Control output format with GBNF (GGML BNF) grammars:

### Basic Grammar Example

```bash
# Create a grammar file (json.gbnf)
root ::= object
object ::= "{" ws string ":" ws value "}"
string ::= "\"" [a-zA-Z0-9 ]+ "\""
value ::= [0-9]+
ws ::= [ \t\n]*

# Use grammar for generation
./llama-cli -m model.gguf \
    --grammar-file json.gbnf \
    --prompt "Generate a JSON object with name and age:"
```

### Complex Grammars

```bnf
# function_call.gbnf - Function calling grammar
root ::= function_call
function_call ::= "{" ws "\"function\":\"" function_name "\"" ws ",\"arguments\":" ws object "}"
function_name ::= [a-zA-Z_][a-zA-Z0-9_]* | "\"" [a-zA-Z_][a-zA-Z0-9_]* "\""
object ::= "{" ws members? "}"
members ::= pair ("," ws pair)* | pair
pair ::= string ":" ws value
string ::= "\"" ([^"] | "\\\"")* "\""
value ::= string | number | "true" | "false" | "null" | object | array
array ::= "[" ws values? "]"
values ::= value ("," ws value)* | value
number ::= [0-9]+ ("." [0-9]+)?
ws ::= [ \t\n]*
```

### Practical Grammar Examples

```bnf
# email.gbnf - Email format
root ::= email
email ::= local "@" domain
local ::= [a-zA-Z0-9._-]+
domain ::= [a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# code.gbnf - Python function
root ::= function
function ::= "def " identifier "(" params ")" ":" "\n" body
identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
params ::= identifier ("," identifier)* | ""
body ::= "    " ("pass" | "return " expression)
expression ::= "\"" [^"]* "\"" | [0-9]+ | identifier
```

### Using Grammars Programmatically

```python
import subprocess

def generate_with_grammar(model_path, prompt, grammar_file):
    """Generate text with grammar constraints."""

    cmd = [
        "./llama-cli",
        "-m", model_path,
        "--grammar-file", grammar_file,
        "--prompt", prompt,
        "--n-predict", "200",
        "--temp", "0.7"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        # Extract generated text (remove prompt)
        output = result.stdout
        prompt_start = output.find(prompt)
        if prompt_start != -1:
            return output[prompt_start + len(prompt):].strip()

    return None

# Usage
json_output = generate_with_grammar(
    "model.gguf",
    "Create a person object:",
    "json.gbnf"
)
```

## Embeddings

Generate vector embeddings for semantic search:

### CLI Embeddings

```bash
# Generate embeddings for text
./llama-cli -m model.gguf \
    --embedding \
    --log-disable \
    --prompt "Your text here"

# Output format: JSON with embedding vector
```

### Server Embeddings

```bash
# Start server with embeddings
./llama-server -m model.gguf --embedding

# API call for embeddings
curl -X POST http://localhost:8080/v1/embeddings \
    -H "Content-Type: application/json" \
    -d '{
        "input": "Hello, world!",
        "model": "local-model"
    }'
```

### Python Embeddings

```python
import numpy as np
from typing import List

def get_embeddings(texts: List[str], model_path: str) -> List[List[float]]:
    """Get embeddings for multiple texts."""

    embeddings = []

    for text in texts:
        # Run embedding generation
        cmd = [
            "./llama-cli",
            "-m", model_path,
            "--embedding",
            "--log-disable",
            "--prompt", text,
            "--n-predict", "0"  # No generation, just embedding
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Parse JSON output
            try:
                output_json = result.stdout.strip()
                data = json.loads(output_json)
                embeddings.append(data["embedding"])
            except (json.JSONDecodeError, KeyError):
                print(f"Failed to parse embedding for: {text[:50]}...")

    return embeddings

# Usage
texts = [
    "The cat sits on the mat",
    "A feline rests on a rug",
    "Python is a programming language"
]

embeddings = get_embeddings(texts, "model.gguf")

# Calculate similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity = cosine_similarity(embeddings[0], embeddings[1])
print(f"Similarity between similar sentences: {similarity:.3f}")
```

## Semantic Search with Embeddings

```python
class SemanticSearch:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents: List[str]):
        """Add documents to the search index."""
        self.documents.extend(documents)
        new_embeddings = get_embeddings(documents, self.model_path)
        self.embeddings.extend(new_embeddings)

    def search(self, query: str, top_k: int = 5) -> List[tuple]:
        """Search for most similar documents."""
        query_embedding = get_embeddings([query], self.model_path)[0]

        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = cosine_similarity(query_embedding, doc_embedding)
            similarities.append((similarity, self.documents[i]))

        # Sort by similarity (descending)
        similarities.sort(reverse=True, key=lambda x: x[0])

        return similarities[:top_k]

# Usage
search = SemanticSearch("model.gguf")

# Add documents
docs = [
    "Python is a programming language",
    "Machine learning is a subset of AI",
    "The weather is sunny today",
    "Neural networks are inspired by the brain"
]

search.add_documents(docs)

# Search
results = search.search("artificial intelligence", top_k=2)
for similarity, doc in results:
    print(f"{similarity:.3f}: {doc}")
```

## Multimodal Models

### LLaVA Support

llama.cpp supports vision-language models:

```bash
# Build with multimodal support
cmake -B build -DLLAMA_VISION=ON
cmake --build build --config Release

# Run LLaVA model
./llama-cli -m llava-model.gguf \
    --mmproj llava-projector.gguf \
    --image image.jpg \
    --prompt "Describe this image:"
```

### Image Understanding

```python
def describe_image(image_path: str, model_path: str, projector_path: str) -> str:
    """Describe an image using LLaVA."""

    cmd = [
        "./llama-cli",
        "-m", model_path,
        "--mmproj", projector_path,
        "--image", image_path,
        "--prompt", "Describe this image in detail:",
        "--n-predict", "200",
        "--temp", "0.7"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        # Extract description (after prompt)
        output = result.stdout
        prompt = "Describe this image in detail:"
        prompt_pos = output.find(prompt)

        if prompt_pos != -1:
            return output[prompt_pos + len(prompt):].strip()

    return "Failed to describe image"

# Usage
description = describe_image("photo.jpg", "llava.gguf", "projector.gguf")
print(description)
```

## Custom Tokenizers

### Using Alternative Tokenizers

```python
# For models with custom tokenizers
from transformers import AutoTokenizer

class CustomTokenizer:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def encode(self, text: str) -> List[int]:
        return self.tokenizer.encode(text)

    def decode(self, tokens: List[int]) -> str:
        return self.tokenizer.decode(tokens)

# Integration with llama.cpp (advanced)
# Requires custom build modifications
```

## LoRA and Fine-tuning

### Applying LoRA Adapters

```bash
# Apply LoRA adapter (if supported)
./llama-cli -m base-model.gguf \
    --lora lora-adapter.gguf \
    --lora-scaled lora-adapter.gguf 1.0 \
    --prompt "Your prompt here"
```

### Exporting LoRA

```bash
# Export fine-tuned LoRA
./llama-export-lora \
    --model-base base-model.gguf \
    --model-out fine-tuned.gguf \
    --lora-scaled lora-adapter.gguf 1.0
```

## Model Merging

Combine multiple models:

```bash
# Merge models with different strengths
./llama-merge \
    --model-a coding-model.gguf \
    --model-b chat-model.gguf \
    --model-out merged-model.gguf \
    --tensor-type f16
```

## Custom Architectures

### Extending llama.cpp

For advanced users, llama.cpp can be extended:

```cpp
// custom_model.cpp - Example extension
#include "llama.h"

// Custom model implementation
class CustomModel : public llama_model {
    // Implement custom architecture
};

// Register custom model
LLAMA_MODEL_REGISTER("custom", CustomModel);
```

## Performance Profiling

### Detailed Profiling

```bash
# Enable detailed profiling
./llama-cli -m model.gguf \
    --prompt "Hello" \
    --perf \
    --verbose

# Profile specific operations
./llama-bench -m model.gguf \
    --profile \
    --output profile.json
```

### Custom Profiling

```python
import time
import psutil

class PerformanceProfiler:
    def __init__(self):
        self.start_time = None
        self.start_memory = None

    def start(self):
        self.start_time = time.time()
        self.start_memory = psutil.virtual_memory().used

    def stop(self):
        end_time = time.time()
        end_memory = psutil.virtual_memory().used

        duration = end_time - self.start_time
        memory_delta = end_memory - self.start_memory

        return {
            "duration_seconds": duration,
            "memory_delta_mb": memory_delta / (1024 * 1024),
            "tokens_per_second": None  # Would need token count
        }

# Usage
profiler = PerformanceProfiler()
profiler.start()

# Run inference
result = subprocess.run(["./llama-cli", "-m", "model.gguf", "--prompt", "Hello", "--n-predict", "100"],
                       capture_output=True, text=True)

stats = profiler.stop()
print(f"Inference took {stats['duration_seconds']:.2f}s")
print(f"Memory delta: {stats['memory_delta_mb']:.1f} MB")
```

## Plugin System

### Loading Custom Plugins

```bash
# Build with plugin support
cmake -B build -DLLAMA_PLUGINS=ON
cmake --build build --config Release

# Load custom plugin
./llama-cli -m model.gguf \
    --plugin my-plugin.so \
    --plugin-config config.json
```

## Advanced Server Features

### Custom Endpoints

```python
# server_extensions.py
from llama_cpp.server import create_app
from flask import request, jsonify

app = create_app()

@app.route("/custom/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")

    # Custom analysis logic
    analysis = {
        "length": len(text),
        "word_count": len(text.split()),
        "sentiment": "neutral"  # Would use actual model
    }

    return jsonify(analysis)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

### Middleware Integration

```python
# Custom middleware for logging/caching
class CustomMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Pre-processing
        print(f"Request: {environ['PATH_INFO']}")

        # Call original app
        return self.app(environ, start_response)

# Apply middleware
app.wsgi_app = CustomMiddleware(app.wsgi_app)
```

## Research Features

### Experimental Architectures

```bash
# Enable experimental features
cmake -B build \
    -DLLAMA_EXPERIMENTAL=ON \
    -DLLAMA_ATTENTION=ON \
    -DLLAMA_ROPE=ON

cmake --build build --config Release

# Use experimental features
./llama-cli -m model.gguf \
    --attention experimental \
    --rope-scaling dynamic
```

## Best Practices

1. **Grammar Usage**: Use grammars for structured output rather than prompt engineering
2. **Embedding Quality**: Normalize embeddings and consider dimensionality reduction
3. **Multimodal**: Test image quality and preprocessing for best results
4. **Performance**: Profile regularly and optimize bottlenecks
5. **Extensions**: Keep custom code modular and well-documented
6. **Updates**: Stay current with llama.cpp developments

These advanced features unlock sophisticated use cases beyond basic text generation, from structured data extraction to multimodal understanding. 