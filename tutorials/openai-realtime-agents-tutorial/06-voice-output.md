---
layout: default
title: "Chapter 6: Voice Output"
nav_order: 6
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 6: Voice Output

Output quality in voice systems is a mix of timing, clarity, and interruption behavior.

## Output Pipeline

1. model emits response deltas
2. audio stream is synthesized
3. client buffers/playbacks frames
4. playback is interrupted or completed based on user behavior

## Voice UX Guidelines

- Keep responses shorter than text chat equivalents.
- Prefer plain wording over dense lists.
- Use brief verbal markers for transitions (for example: "Checking that now").
- Avoid long unbroken monologues.

## Barge-In Handling

When user starts speaking while output audio is playing:

- stop playback quickly
- preserve minimal assistant state
- prioritize new user turn

Fast barge-in handling is one of the strongest predictors of perceived quality.

## Audio Quality Monitoring

Track:

- time-to-first-audio
- synthesis completion latency
- interruption rate
- playback error rate

These metrics catch regressions earlier than subjective feedback alone.

## Summary

You now understand how to make realtime voice output feel responsive and controllable.

Next: [Chapter 7: Advanced Patterns](07-advanced-patterns.md)
