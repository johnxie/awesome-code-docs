---
layout: default
title: "Ollama Tutorial - Chapter 5: Modelfiles & Custom Models"
nav_order: 5
has_children: false
parent: Ollama Tutorial
---

# Chapter 5: Modelfiles, Templates, and Custom Models

> Build tailored models with custom system prompts, templates, parameters, and adapters.

## Modelfile Basics

A Modelfile defines how to build a model in Ollama.

Example:
```
FROM llama3
SYSTEM "You are a precise technical assistant."
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
FORMAT json
```
Build & run:
```bash
ollama create tech-assistant -f Modelfile
ollama run tech-assistant
```

## Common Directives

- `FROM <base>`: base model (e.g., `llama3`, `mistral`)
- `SYSTEM "..."`: default system prompt
- `TEMPLATE "..."`: custom prompt formatting
- `PARAMETER <name> <value>`: default runtime parameters
- `ADAPTER <path>`: apply LoRA/adapter weights
- `LICENSE`, `TAGS`, `DESCRIPTION`: metadata
- `EMBEDDING true`: mark as embedding-only model

## Prompt Templates

Example chat-style template:
```
TEMPLATE """
{{ if .System }}[INST] <<SYS>>{{ .System }}<</SYS>> {{ end }}
{{ .Prompt }} [/INST]
"""
```

JSON-friendly template:
```
FORMAT json
PARAMETER temperature 0.1
```

## Applying Adapters / LoRA

```
FROM llama3
ADAPTER ./adapters/codellama-lora.bin
SYSTEM "You are a coding assistant."
PARAMETER temperature 0.2
```

## Context and Quality Controls

- `PARAMETER num_ctx 8192` (context window)
- `PARAMETER temperature 0.1-0.7`
- `PARAMETER repeat_penalty 1.1`
- `PARAMETER top_p 0.9`
- `PARAMETER top_k 40`
- `PARAMETER num_predict 512`

## Building Domain-Personas

```
FROM llama3
SYSTEM "You are a senior SRE. Respond with concise runbooks."
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
```

## Versioning and Promotion

```bash
ollama create finance-bot:v1 -f Modelfile
ollama cp finance-bot:v1 finance-bot:prod
ollama rm finance-bot:v1   # keep only prod tag if desired
```

## Inspecting Models

```bash
ollama show finance-bot
ollama show finance-bot --license
```

## Distributing Models

- Share Modelfile + adapters (small) rather than full weights
- Back up `~/.ollama/models` for custom builds

## Best Practices

- Keep system prompts short and specific
- Use `FORMAT json` for structured workflows
- Pin base versions (e.g., `llama3:8b`) for reproducibility
- Separate personas into distinct models instead of overloading one
- Document defaults in the Modelfile for your team

Next: optimize performance with GPU/CPU tuning and quantization choices.
