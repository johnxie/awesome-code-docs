---
layout: default
title: "Chapter 4: Transcription and Translation"
nav_order: 4
parent: OpenAI Whisper Tutorial
---

# Chapter 4: Transcription and Translation

This chapter covers the two highest-value tasks: transcription and speech-to-English translation.

## Basic Transcription

```python
import whisper

model = whisper.load_model("small")
result = model.transcribe("meeting.wav")
print(result["text"])
```

## Translation Workflow

For non-English speech to English text, use a multilingual model and task override:

```python
result = model.transcribe("speech.wav", task="translate")
```

The official README warns that `turbo` is not translation-focused, so prefer other multilingual models when translation quality matters.

## Language Detection

Lower-level APIs allow explicit language detection and decoding control. This is useful for analytics pipelines that need language metadata.

## Timestamps and Subtitles

Whisper can produce segment timing data that supports subtitle generation and aligned transcript experiences.

## Evaluation Tips

- track WER/CER by language/domain
- review difficult audio categories separately
- compare model choices against real workload latency budgets

## Summary

You can now run robust transcription and translation workflows with explicit model/task choices.

Next: [Chapter 5: Fine-Tuning and Adaptation](05-fine-tuning.md)
