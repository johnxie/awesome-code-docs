---
layout: default
title: "Ollama Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Ollama Tutorial
---

# Chapter 1: Getting Started with Ollama

> Install Ollama, pull your first model, and run a local chat with an OpenAI-compatible API.

## Overview

Ollama runs LLMs locally with zero cloud dependency. It exposes a simple CLI and an OpenAI-style HTTP API, works on macOS/Linux/Windows (WSL), and supports both CPU and GPU inference.

## Prerequisites

- macOS 12+/Linux (Ubuntu/Debian/RHEL/Arch) or Windows 10/11 via WSL2
- 8 GB RAM minimum (16 GB recommended for 7B models)
- Optional: NVIDIA GPU with recent drivers (or Apple Silicon GPU)
- `curl` for API tests

## Install Ollama

### macOS
```bash
brew install ollama/tap/ollama
ollama --version
```

### Linux (official script)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

### Windows (via WSL)
- Install WSL2 + Ubuntu
- Run the Linux install script inside WSL

## Start the Ollama Service

```bash
ollama serve  # starts the background server on port 11434
```
- Default API: `http://localhost:11434`
- Logs: `~/.ollama/logs` (per platform)

## Pull Your First Model

```bash
ollama pull llama2:7b
ollama list          # verify
```
Popular quick models:
- `phi3:mini` (fast, small)
- `mistral` (balanced quality/speed)
- `llama3` (strong general model)

## Run Your First Chat

Interactive chat:
```bash
ollama run llama2 "Hello!"              # one-off prompt
ollama run llama2                       # enters REPL; type your messages
```

## Call the HTTP API (OpenAI-Compatible)

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "Tell me a short joke"}
  ]
}'
```
The response mirrors OpenAI chat completions (`choices`, `message`, `usage`).

## Python Quickstart

```python
import requests

resp = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama2",
    "messages": [{"role": "user", "content": "Explain RAG in 3 bullets"}],
    "stream": False
})
print(resp.json()["message"]["content"])
```

## Node.js Quickstart

```bash
npm install openai
```
```javascript
import OpenAI from "openai";
const client = new OpenAI({ baseURL: "http://localhost:11434/v1", apiKey: "ollama" });

const chat = await client.chat.completions.create({
  model: "llama2",
  messages: [{ role: "user", content: "Summarize Ollama in one sentence" }],
});
console.log(chat.choices[0].message.content);
```

## Key CLI Commands

```bash
ollama list                # models installed
ollama pull <model>        # download
ollama run <model>         # chat / completion
ollama show <model>        # metadata
ollama rm <model>          # remove
ollama cp <src> <dst>      # copy/rename a model
```

## Files & Paths

- **Models**: `~/.ollama/models` (Linux/macOS), `%USERPROFILE%\.ollama\models` (Windows)
- **Config**: `~/.ollama/config.json` (rarely needed; defaults are fine)

## Troubleshooting

- **Service not running**: `ollama serve` then retry
- **Port conflict**: set `OLLAMA_HOST=0.0.0.0:11434` to change bind address
- **Slow downloads**: retry or use a mirror if available

Next: explore the model gallery, Modelfiles, and model management.
