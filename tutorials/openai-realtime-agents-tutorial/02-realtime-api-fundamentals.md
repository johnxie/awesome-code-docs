---
layout: default
title: "Chapter 2: Realtime API Fundamentals"
nav_order: 2
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 2: Realtime API Fundamentals

Realtime systems are event-driven: client audio in, model events out.

## Core Session Flow

1. Client creates a realtime session token.
2. Browser opens a WebSocket/WebRTC channel.
3. Audio frames stream continuously.
4. Server and model exchange structured events.

## Event Types to Track

- `session.created`
- `input_audio_buffer.append`
- `response.created`
- `response.output_audio.delta`
- `response.completed`

## Minimal Event Handler Pattern

```ts
function onEvent(evt: { type: string; [k: string]: unknown }) {
  switch (evt.type) {
    case "response.created":
      console.log("response started");
      break;
    case "response.completed":
      console.log("response finished");
      break;
  }
}
```

## Reliability Basics

- Reconnect with backoff on dropped sessions.
- Include session IDs in logs.
- Apply timeout guards for stalled responses.

## Summary

You understand the realtime event model and session lifecycle.

Next: [Chapter 3: Voice Input Processing](03-voice-input-processing.md)
