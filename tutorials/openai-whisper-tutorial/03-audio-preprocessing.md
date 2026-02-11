---
layout: default
title: "Chapter 3: Audio Preprocessing"
nav_order: 3
parent: OpenAI Whisper Tutorial
---

# Chapter 3: Audio Preprocessing

Input quality strongly affects output quality. Standardize audio before inference.

## Normalize Audio with ffmpeg

```bash
ffmpeg -i input.m4a -ar 16000 -ac 1 -c:a pcm_s16le clean.wav
```

This converts to 16 kHz mono WAV, a stable format for ASR pipelines.

## Segment Long Files

```bash
ffmpeg -i long_call.wav -f segment -segment_time 300 -c copy chunk_%03d.wav
```

Chunking improves memory behavior and retry granularity.

## Python Preprocessing Pattern

```python
import subprocess
from pathlib import Path


def preprocess(src: str, dst: str) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", dst,
    ]
    subprocess.run(cmd, check=True)

preprocess("raw_audio.mp3", "ready.wav")
```

## Noise and Silence Strategy

- Remove long leading/trailing silence.
- Use VAD for streaming scenarios.
- Keep original audio for forensic reprocessing.

## Summary

You can now build a deterministic preprocessing step before Whisper inference.

Next: [Chapter 4: Transcription and Translation](04-transcription-translation.md)
