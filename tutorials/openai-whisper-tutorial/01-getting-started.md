---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Whisper Tutorial
---

# Chapter 1: Getting Started

This chapter sets up Whisper locally and validates the baseline transcription workflow.

## Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -U openai-whisper
```

Install `ffmpeg` using your platform package manager (required for most audio inputs).

## Quick CLI Test

```bash
whisper sample_audio.wav --model turbo
```

If the model downloads and transcription completes, your baseline setup is working.

## Quick Python Test

```python
import whisper

model = whisper.load_model("turbo")
result = model.transcribe("sample_audio.wav")
print(result["text"])
```

## Model Selection Snapshot

| Model | Typical Use |
|:------|:------------|
| tiny/base | Fast, resource-limited environments |
| small/medium | Balanced quality and speed |
| large | Highest quality, high compute cost |
| turbo | Fast transcription-focused workflows |

## Important Constraint

The official README notes that `turbo` is not trained for translation tasks. Use multilingual non-turbo models when you need speech-to-English translation.

## Summary

You now have a working Whisper setup and know how to choose a baseline model for your environment.

Next: [Chapter 2: Model Architecture](02-model-architecture.md)
