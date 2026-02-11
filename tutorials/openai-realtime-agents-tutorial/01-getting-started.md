---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 1: Getting Started

This chapter gets the official demo running locally so you can inspect real event flow and agent orchestration.

## Local Setup

```bash
git clone https://github.com/openai/openai-realtime-agents.git
cd openai-realtime-agents
npm install
cp .env.sample .env
# add OPENAI_API_KEY
npm run dev
```

Open `http://localhost:3000` and test both built-in scenarios.

## What You Should Verify First

- Session initialization succeeds and ephemeral credentials are returned.
- Audio input is captured and pushed to the realtime pipeline.
- Tool calls appear in logs when scenarios require them.
- Agent switches are visible in transcript or event stream.

## Architecture in Practice

The demo combines:

1. Browser UI for voice I/O and logs
2. API route to mint short-lived session credentials
3. Realtime transport channel for streaming events
4. Agent config modules defining instructions, tools, and handoff graph

## Initial Debug Checklist

| Check | Symptom if Broken |
|:------|:------------------|
| API key loaded | session endpoint returns auth errors |
| Mic permissions granted | no input events or silent transcripts |
| Realtime channel established | events panel shows no server messages |
| Agent config selected | handoffs never occur |

## Development Tip

Start by understanding one scenario end-to-end before editing prompts or adding tools. Most latency and correctness issues are easier to diagnose when baseline behavior is known.

## Summary

You now have a running reference app and a concrete baseline for deeper protocol and orchestration work.

Next: [Chapter 2: Realtime API Fundamentals](02-realtime-api-fundamentals.md)
