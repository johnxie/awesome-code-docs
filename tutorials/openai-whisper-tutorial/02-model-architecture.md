---
layout: default
title: "Chapter 2: Model Architecture"
nav_order: 2
parent: OpenAI Whisper Tutorial
---

# Chapter 2: Model Architecture

Whisper uses a Transformer encoder-decoder pipeline that maps audio to text tokens.

## End-to-End Pipeline

1. Decode and resample audio to 16 kHz.
2. Convert waveform to log-Mel spectrogram.
3. Feed spectrogram into the encoder.
4. Autoregressively decode text tokens.

## Core Building Blocks

- **Encoder**: consumes Mel frames and builds contextual acoustic features.
- **Decoder**: generates transcript tokens conditioned on encoder states.
- **Special tokens**: language, task (`transcribe` or `translate`), and timestamps.

## Why Whisper Generalizes Well

- Trained on large multilingual, multitask audio-text pairs.
- Learns accents, domain terms, and noisy audio patterns.
- Uses the same architecture for transcription and translation.

## Decode Controls

```python
result = model.transcribe(
    "sample_audio.mp3",
    language="en",
    task="transcribe",
    temperature=0.0,
    beam_size=5,
)
```

- `temperature=0.0` improves determinism.
- `beam_size` can improve accuracy at higher latency.

## Summary

You understand how audio becomes text and which decode parameters drive behavior.

Next: [Chapter 3: Audio Preprocessing](03-audio-preprocessing.md)
