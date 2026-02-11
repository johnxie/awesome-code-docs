---
layout: default
title: "Chapter 4: Transcription and Translation"
nav_order: 4
parent: OpenAI Whisper Tutorial
---

# Chapter 4: Transcription and Translation

Whisper supports both same-language transcription and translation to English.

## Transcribe in Source Language

```python
result = model.transcribe(
    "meeting_es.wav",
    task="transcribe",
    language="es",
)
print(result["text"])
```

## Translate to English

```python
result = model.transcribe(
    "meeting_es.wav",
    task="translate",
)
print(result["text"])  # English output
```

## Segment-Level Timestamps

```python
for seg in result["segments"]:
    print(f"{seg['start']:.2f}s - {seg['end']:.2f}s :: {seg['text']}")
```

## Practical Guidelines

- Set explicit `language` for better stability when known.
- Use `task="translate"` for multilingual content pipelines.
- Persist segments for subtitle and search indexing.

## Summary

You can now run multilingual transcription and translation with timestamped segments.

Next: [Chapter 5: Fine-Tuning](05-fine-tuning.md)
