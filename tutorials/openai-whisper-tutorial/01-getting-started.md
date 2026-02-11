---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Whisper Tutorial
---

# Chapter 1: Getting Started

This chapter sets up Whisper locally and runs your first transcription.

## Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai-whisper torch
brew install ffmpeg  # macOS
```

If you are on Linux, install `ffmpeg` from your distro package manager.

## First Transcription

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("sample_audio.mp3")
print(result["text"])
```

## Model Size Selection

| Model | Speed | Accuracy | Typical Use |
|:------|:------|:---------|:------------|
| `tiny` | Fastest | Lowest | Real-time prototypes |
| `base` | Fast | Moderate | Dev and QA |
| `small` | Medium | Good | Balanced production |
| `medium` | Slower | Better | High-quality transcription |
| `large` | Slowest | Best | Offline batch quality |

## Device Configuration

```python
import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("small", device=device)
```

## Common Errors

| Error | Cause | Fix |
|:------|:------|:----|
| `FileNotFoundError` | Bad audio path | Verify file path and extension |
| `ffmpeg not found` | Missing system binary | Install `ffmpeg` and retry |
| CUDA OOM | Model too large | Use smaller model or CPU |

## Summary

You now have Whisper running locally with a repeatable baseline transcription flow.

Next: [Chapter 2: Model Architecture](02-model-architecture.md)
