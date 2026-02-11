---
layout: default
title: "Chapter 2: Realtime API Fundamentals"
nav_order: 2
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 2: Realtime API Fundamentals

Realtime systems are event systems first and prompt systems second.

## Session Lifecycle

A typical sequence is:

1. client requests short-lived session credentials
2. client opens realtime connection
3. session config is updated (modalities, behavior)
4. conversation items are created
5. response generation events stream back

## Transport Choices

- **WebRTC**: preferred for browser voice latency and media handling
- **WebSocket**: useful for server-side or custom client pipelines

Both rely on client and server event streams.

## Event Model

Client events often include:

- session updates
- new conversation items
- response creation requests

Server events include:

- response deltas
- tool call requests/results
- response completion/failure markers

## GA Migration Practicalities

As of February 11, 2026, OpenAI documentation indicates GA-first Realtime usage and deprecation timelines for beta interfaces. Build new integrations against current GA docs and event contracts to avoid near-term migration debt.

## Validation Checklist

- log every event type during development
- verify event ordering assumptions with real traces
- treat unknown events as non-fatal until classified
- isolate transport issues from prompt issues

## Summary

You now understand the realtime lifecycle and why event observability is essential for stable voice applications.

Next: [Chapter 3: Voice Input Processing](03-voice-input-processing.md)
