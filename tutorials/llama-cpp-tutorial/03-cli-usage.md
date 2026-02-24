---
layout: default
title: "llama.cpp Tutorial - Chapter 3: CLI Usage"
nav_order: 3
has_children: false
parent: llama.cpp Tutorial
---

# Chapter 3: Command Line Interface

Welcome to **Chapter 3: Command Line Interface**. In this part of **llama.cpp Tutorial: Local LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master llama-cli with advanced options, interactive modes, and conversation management.

## Overview

The llama-cli tool provides comprehensive control over model inference. This chapter covers all major options, interactive modes, and advanced usage patterns.

## Basic Command Structure

```bash
llama-cli [options] -m model.gguf [prompt_options]
```

## Essential Options

### Model and Context

```bash
# Specify model file
-m, --model <path>              # Path to GGUF model file

# Context management
-c, --ctx-size <n>              # Context size (default: 4096)
-n, --n-predict <n>             # Number of tokens to predict (default: -1, unlimited)
--keep <n>                     # Number of tokens to keep from initial prompt

# Memory management
--memory-f32                    # Use f32 instead of f16 for memory KV
--mlock                         # Force system to keep model in RAM
--no-mmap                       # Don't memory-map model (slower but uses less RAM)
```

### Generation Parameters

```bash
# Sampling parameters
--temp <float>                  # Temperature (0.0-2.0, default: 0.8)
--top-k <int>                   # Top-k sampling (default: 40)
--top-p <float>                 # Top-p (nucleus) sampling (default: 0.9)
--min-p <float>                 # Minimum probability (default: 0.0)
--tfs-z <float>                 # Tail free sampling (default: 1.0)
--typical-p <float>             # Typical sampling (default: 1.0)

# Penalty parameters
--repeat-last-n <int>           # Lookback for repetition penalty (default: 64)
--repeat-penalty <float>        # Repetition penalty (default: 1.1)
--presence-penalty <float>      # Presence penalty (default: 0.0)
--frequency-penalty <float>     # Frequency penalty (default: 0.0)

# Mirostat sampling (alternative to top-k/top-p)
--mirostat <int>                # Use Mirostat sampling (1 or 2)
--mirostat-lr <float>           # Mirostat learning rate (default: 0.1)
--mirostat-ent <float>          # Mirostat target entropy (default: 5.0)
```

## Interactive Modes

### Basic Interactive Chat

```bash
# Start interactive session
./llama-cli -m model.gguf --interactive

# With custom settings
./llama-cli -m model.gguf \
    --interactive \
    --ctx-size 4096 \
    --temp 0.8 \
    --top-k 40 \
    --top-p 0.9 \
    --repeat-penalty 1.1 \
    --color  # Enable colored output
```

### Conversation Mode

```bash
# Start conversation with system prompt
./llama-cli -m model.gguf \
    --interactive \
    --conversation \
    --in-prefix "Human: " \
    --out-prefix "Assistant: "
```

### Chat Template Mode

```bash
# Use chat templates (for chat models)
./llama-cli -m model.gguf \
    --interactive \
    --chat-template chatml  # or llama2, mistral, etc.
```

## Input Methods

### Direct Prompt

```bash
# Simple prompt
./llama-cli -m model.gguf --prompt "Hello, how are you?"

# Multi-line prompt
./llama-cli -m model.gguf \
    --prompt "You are a helpful assistant.
User: What is the capital of France?
Assistant: The capital of France is Paris.
User: What about Italy?
Assistant:"
```

### File Input

```bash
# Read prompt from file
./llama-cli -m model.gguf --file prompt.txt

# Read from stdin
echo "What is machine learning?" | ./llama-cli -m model.gguf

# Process multiple files
for file in prompts/*.txt; do
    echo "Processing $file..."
    ./llama-cli -m model.gguf --file "$file" --n-predict 100
done
```

### Reverse Prompt (Stopping)

```bash
# Stop generation when certain text appears
./llama-cli -m model.gguf \
    --prompt "Write a function to sort an array" \
    --reverse-prompt "```"  # Stop when code block ends

# Multiple reverse prompts
./llama-cli -m model.gguf \
    --prompt "Explain photosynthesis" \
    --reverse-prompt "Human:" \
    --reverse-prompt "AI:"
```

## Output Control

### Formatting

```bash
# Enable colored output
./llama-cli -m model.gguf --color

# Show timing information
./llama-cli -m model.gguf --prompt "Hello" --verbose-prompt

# Show token probabilities
./llama-cli -m model.gguf --prompt "Hello" --logits

# JSON output mode
./llama-cli -m model.gguf --prompt "Hello" --simple-io
```

### Logging and Debugging

```bash
# Enable debug logging
./llama-cli -m model.gguf --log-disable  # Actually enables more logging

# Show system information
./llama-cli -m model.gguf --verbose-prompt

# Performance profiling
./llama-cli -m model.gguf --prompt "Hello" --perf
```

## Advanced Features

### Multi-Turn Conversation

```bash
# Manual conversation management
./llama-cli -m model.gguf \
    --prompt "You are a helpful assistant. Human: Hello\nAssistant:" \
    --keep 50  # Keep first 50 tokens

# Interactive with history
./llama-cli -m model.gguf \
    --interactive \
    --ctx-size 2048 \
    --keep 256  # Keep system prompt and some history
```

### Grammar-Based Generation

```bash
# Use GBNF grammar (covered in Chapter 7)
./llama-cli -m model.gguf \
    --grammar-file grammar.gbnf \
    --prompt "Generate a JSON object with name and age"

# Example grammar file (grammar.gbnf)
root ::= object
object ::= "{" ws string ":" ws value "}"
string ::= "\"" [a-zA-Z0-9 ]+ "\""
value ::= [0-9]+
ws ::= [ \t\n]*
```

### Seed Control

```bash
# Deterministic output
./llama-cli -m model.gguf \
    --prompt "Write a haiku" \
    --seed 42 \
    --temp 0.8

# Different seeds for variety
for seed in 1 2 3; do
    echo "Seed $seed:"
    ./llama-cli -m model.gguf --prompt "Joke about programming" --seed $seed --n-predict 50
    echo
done
```

## Batch Processing

### Multiple Prompts

```bash
# Process multiple prompts
cat prompts.txt | while read prompt; do
    echo "Prompt: $prompt"
    echo "Response:"
    ./llama-cli -m model.gguf --prompt "$prompt" --n-predict 100
    echo "---"
done
```

### Parallel Processing

```bash
#!/bin/bash
# parallel_inference.sh

model="model.gguf"
prompts=("prompt1.txt" "prompt2.txt" "prompt3.txt")

# Process in parallel (adjust based on your CPU)
for prompt_file in "${prompts[@]}"; do
    ./llama-cli -m "$model" --file "$prompt_file" --n-predict 200 &
done

wait  # Wait for all to complete
```

## Performance Optimization

### CPU Settings

```bash
# Use all available threads
threads=$(nproc)
./llama-cli -m model.gguf --threads $threads

# Batch processing for better throughput
./llama-cli -m model.gguf --batch-size 512

# CPU-specific optimizations
./llama-cli -m model.gguf --threads $threads --batch-size 512
```

### Memory Optimization

```bash
# For large models with limited RAM
./llama-cli -m model.gguf \
    --ctx-size 1024 \      # Smaller context
    --no-mmap \           # Don't memory map
    --memory-f32 \        # Use f32 for KV cache
    --mlock               # Lock in RAM if you have enough

# Monitor memory usage
./llama-cli -m model.gguf --prompt "Hello" --perf
```

## Custom Scripts and Automation

### Response Quality Checker

```bash
#!/bin/bash
# quality_check.sh

model="$1"
prompt="$2"
min_length=50

response=$(./llama-cli -m "$model" --prompt "$prompt" --n-predict 200 --simple-io)

# Check response quality
if [ ${#response} -lt $min_length ]; then
    echo "❌ Response too short"
    exit 1
fi

if echo "$response" | grep -q "I don't know\|I cannot"; then
    echo "❌ Model refused to answer"
    exit 1
fi

echo "✅ Response quality check passed"
echo "$response"
```

### Benchmarking Script

```bash
#!/bin/bash
# benchmark.sh

model="$1"
prompts=("simple.txt" "medium.txt" "complex.txt")

echo "Benchmarking $model"
echo "Prompt | Tokens/sec | Total Time | Memory"

for prompt_file in "${prompts[@]}"; do
    if [ -f "$prompt_file" ]; then
        start_time=$(date +%s.%3N)

        # Run with performance logging
        ./llama-cli -m "$model" \
            --file "$prompt_file" \
            --n-predict 100 \
            --perf \
            --threads $(nproc) \
            > /dev/null 2>&1

        end_time=$(date +%s.%3N)
        duration=$(echo "$end_time - $start_time" | bc)

        echo "$prompt_file | TBD | ${duration}s | TBD"
    fi
done
```

## Error Handling

### Common Errors and Solutions

```bash
# Model file not found
if [ ! -f "$model" ]; then
    echo "Error: Model file $model not found"
    exit 1
fi

# Context too large
./llama-cli -m model.gguf --ctx-size 2048  # Reduce if getting errors

# Timeout handling
timeout 300 ./llama-cli -m model.gguf --prompt "Long prompt"

# Check exit codes
./llama-cli -m model.gguf --prompt "test"
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "llama-cli failed with exit code $exit_code"
    exit $exit_code
fi
```

## Configuration Files

Save common settings:

```bash
# Create config files for different use cases

# chat_config.txt
cat > chat_config.txt << EOF
--interactive
--ctx-size 4096
--temp 0.8
--top-k 40
--top-p 0.9
--repeat-penalty 1.1
--color
EOF

# code_config.txt
cat > code_config.txt << EOF
--temp 0.2
--top-k 20
--repeat-penalty 1.1
--ctx-size 2048
EOF

# Use configs
./llama-cli -m model.gguf $(cat chat_config.txt) --prompt "Hello"

# Or create wrapper scripts
cat > chat_model.sh << 'EOF'
#!/bin/bash
model="$1"
./llama-cli -m "$model" \
    --interactive \
    --ctx-size 4096 \
    --temp 0.8 \
    --color
EOF

chmod +x chat_model.sh
./chat_model.sh model.gguf
```

## Integration with Other Tools

### With fzf for Interactive Selection

```bash
#!/bin/bash
# interactive_model.sh

# List available models
model=$(find models -name "*.gguf" | fzf --prompt="Select model: ")

if [ -n "$model" ]; then
    echo "Selected: $model"
    ./llama-cli -m "$model" --interactive
fi
```

### With tmux for Persistent Sessions

```bash
#!/bin/bash
# persistent_chat.sh

session_name="llama-chat"

# Create new tmux session if it doesn't exist
tmux has-session -t $session_name 2>/dev/null
if [ $? != 0 ]; then
    tmux new-session -d -s $session_name "./llama-cli -m model.gguf --interactive"
fi

# Attach to session
tmux attach-session -t $session_name
```

## Best Practices

1. **Start Simple**: Use default parameters, then tune for your use case
2. **Test Parameters**: Always test parameter combinations on your specific model
3. **Monitor Performance**: Use `--perf` to understand bottlenecks
4. **Save Good Configs**: Keep working parameter sets for different tasks
5. **Batch When Possible**: Use batch processing for multiple requests
6. **Handle Errors**: Always check exit codes and handle failures
7. **Version Control**: Track which parameter combinations work best

## Quick Reference

### Most Used Options

```bash
# Chat mode
./llama-cli -m model.gguf --interactive --color

# Code generation
./llama-cli -m model.gguf --temp 0.2 --repeat-penalty 1.1

# Creative writing
./llama-cli -m model.gguf --temp 0.9 --top-p 0.95

# Analytical tasks
./llama-cli -m model.gguf --temp 0.1 --top-k 20

# Fast responses
./llama-cli -m model.gguf --temp 0.8 --top-k 40 --top-p 0.9
```

The CLI provides complete control over model behavior. Experiment with different parameters to find what works best for your specific use case and model.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `llama`, `gguf` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Command Line Interface` as an operating subsystem inside **llama.cpp Tutorial: Local LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `prompt`, `float`, `file` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Command Line Interface` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `llama` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `gguf`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ggerganov/llama.cpp)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `model` and `llama` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Model Formats and GGUF](02-model-formats.md)
- [Next Chapter: Chapter 4: Server Mode](04-server.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
