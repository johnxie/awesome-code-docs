---
layout: default
title: "Chapter 3: Voice Input Processing"
nav_order: 3
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 3: Voice Input Processing

Voice quality and turn detection determine perceived intelligence and latency.

## Capture Microphone Audio

```ts
const stream = await navigator.mediaDevices.getUserMedia({
  audio: {
    echoCancellation: true,
    noiseSuppression: true,
    autoGainControl: true,
  },
});
```

## VAD Strategy

- Buffer small frames (for example 20 ms).
- Detect speech start and stop thresholds.
- Commit user turn when silence exceeds threshold.

## Input Guardrails

- Limit max utterance duration.
- Drop corrupted frames.
- Handle permission-denied fallback UX.

## Summary

You can now build stable voice ingestion and turn commit behavior.

Next: [Chapter 4: Conversational AI](04-conversational-ai.md)
