---
layout: default
title: "Chapter 2: Model Architecture"
nav_order: 2
parent: OpenAI Whisper Tutorial
---

# Chapter 2: Model Architecture

Understanding Whisper internals helps explain its strengths and limitations.

## High-Level Design

Whisper uses a transformer encoder-decoder setup:

1. audio is converted to log-Mel spectrogram features
2. encoder processes acoustic representation
3. decoder predicts token sequences conditioned on encoder states

## Multitask Token Strategy

Whisper uses special tokens to steer behavior for:

- transcription
- translation
- language identification
- timestamp prediction

This unified token-driven design replaces many separate ASR pipeline stages.

## Why This Matters Operationally

- a single model can handle multiple speech tasks
- prompt/token settings influence behavior directly
- decoding configuration affects latency and output style

## Sliding Window Behavior

The standard transcription API processes longer audio with sliding windows, which can introduce boundary artifacts if segmentation and stitching are not handled carefully.

## Practical Implications

| Architectural Trait | Operational Effect |
|:--------------------|:-------------------|
| Unified multitask decoder | Flexible but sensitive to token/config choices |
| Large model family | Strong quality/speed tradeoff control |
| Windowed inference | Requires careful chunk handling for long recordings |

## Summary

You now understand the core mechanics behind Whisper's multilingual and multitask behavior.

Next: [Chapter 3: Audio Preprocessing](03-audio-preprocessing.md)
