---
layout: default
title: "Ollama Tutorial - Chapter 2: Models & Modelfiles"
nav_order: 2
has_children: false
parent: Ollama Tutorial
---

# Chapter 2: Models, Pulling, and Modelfiles

> Discover, manage, and customize models with Modelfiles and parameters.

## Browsing & Pulling Models

```bash
ollama list                     # installed models
ollama pull llama3:8b           # download a specific tag
ollama pull mistral             # latest default tag
ollama pull phi3:mini           # small & fast
```

Common tags:
- `llama3`, `llama3:8b`, `llama3:70b`
- `mistral`, `mixtral:8x7b`
- `phi3:mini`, `phi3:medium`
- `qwen2`, `gemma`

Remove or rename:
```bash
ollama rm llama3:8b
ollama cp llama3:8b my-llama3
```

## Model Parameters (Runtime)

Use `options` in API calls or `-p`/`-o` in CLI:
- `temperature` (0-1.5)
- `top_p`, `top_k`
- `repeat_penalty`, `presence_penalty`, `frequency_penalty`
- `num_ctx` (context tokens)
- `num_gpu` (GPU layers auto-detected; override if needed)
- `num_predict` (max tokens)

Example (API):
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "mistral",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_ctx": 4096
  },
  "messages": [{"role": "user", "content": "Give me 3 startup ideas"}]
}'
```

## Modelfiles (Build Custom Models)

A Modelfile defines how a model is built and configured.

Example:
```
FROM llama3
SYSTEM "You are a concise engineering assistant."
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
```
Build and run:
```bash
ollama create eng-assistant -f Modelfile
ollama run eng-assistant
```

### Adding Templates and Formats

```
FROM mistral
TEMPLATE """
{{ if .System }}[INST] <<SYS>>{{ .System }}<</SYS>> {{ end }}
{{ .Prompt }} [/INST]
"""
FORMAT json
PARAMETER temperature 0.1
```
- `TEMPLATE`: custom prompt formatting
- `FORMAT json`: encourages JSON output

### Using LoRA / Adapters

```
FROM llama3
ADAPTER ./adapters/codellama-lora.bin
SYSTEM "You are a code helper."
```

### Model Metadata

```
PARAMETER num_ctx 8192
LICENSE "cc-by-nc"
TAGS "code,assistant"
```

## Managing Model Storage

- Models live under `~/.ollama/models`
- Use `ollama show <model>` to inspect metadata
- Cleanup old versions: `ollama rm <model>`

## Quantization Awareness

Most community models are GGUF with quantization baked in (e.g., `Q4_K_M`). Choose smaller quants for speed/memory, larger for quality:
- `Q2_K` / `Q3_K`: smallest, fastest, lower quality
- `Q4_K_M`: balanced default
- `Q5_K_M` / `Q6_K`: higher quality

## Best Practices

- Start with small models (phi3:mini) to validate pipeline
- Pin tags (e.g., `llama3:8b`) to avoid unexpected updates
- Use `FORMAT json` in Modelfiles for structured outputs
- Keep separate custom models for different personas/use-cases
- Back up `~/.ollama/models` if you maintain curated builds

Next: generate text and chat with advanced controls and streaming.
