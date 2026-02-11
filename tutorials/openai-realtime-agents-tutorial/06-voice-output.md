---
layout: default
title: "Chapter 6: Voice Output"
nav_order: 6
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 6: Voice Output

Output speech quality depends on chunking strategy and playback control.

## Stream and Play Audio Deltas

```ts
function handleAudioDelta(base64Chunk: string) {
  // decode chunk, enqueue PCM frames, feed audio output buffer
}
```

## Playback Controls

- Pause/resume output for interruptions.
- Flush buffered audio when context changes.
- Keep jitter buffers small to reduce delay.

## Voice UX Principles

- Start audio quickly, even before full response completion.
- Keep utterances concise for conversational feel.
- Handle TTS errors with text fallback.

## Summary

You can now deliver low-latency, interruptible voice output.

Next: [Chapter 7: Advanced Patterns](07-advanced-patterns.md)
