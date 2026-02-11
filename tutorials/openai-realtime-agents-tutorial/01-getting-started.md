---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 1: Getting Started

This chapter sets up a local voice-agent project and validates a working realtime session.

## Prerequisites

- Node.js 20+
- OpenAI API key with Realtime access
- Browser with microphone permission support

## Project Setup

```bash
git clone https://github.com/openai/openai-realtime-agents.git
cd openai-realtime-agents
npm install
cp .env.example .env.local
```

Set credentials in `.env.local`.

```bash
OPENAI_API_KEY=your_key_here
```

## Run Locally

```bash
npm run dev
```

Open `http://localhost:3000`, allow microphone access, and start a session.

## First Success Criteria

- Agent connects without WebSocket errors.
- Voice input is captured.
- Assistant returns audible output.

## Summary

You now have a local realtime voice agent running end to end.

Next: [Chapter 2: Realtime API Fundamentals](02-realtime-api-fundamentals.md)
