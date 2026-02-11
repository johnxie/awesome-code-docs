---
layout: default
title: "OpenAI Realtime Agents Tutorial"
nav_order: 95
has_children: true
---

# OpenAI Realtime Agents Tutorial: Voice-First AI Systems

> Build low-latency voice agents using OpenAI Realtime APIs and agent orchestration patterns from the official demo repository.

[![Stars](https://img.shields.io/github/stars/openai/openai-realtime-agents?style=social)](https://github.com/openai/openai-realtime-agents)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agents SDK](https://img.shields.io/badge/OpenAI-Agents_SDK-blue)](https://github.com/openai/openai-agents-js)

## What this tutorial covers

The `openai/openai-realtime-agents` repository demonstrates two high-impact voice-agent designs:

- **Chat-Supervisor**: a fast realtime front agent plus a stronger text supervisor for complex reasoning/tool calls
- **Sequential Handoff**: multiple specialized realtime agents transferring control by intent

These patterns are practical blueprints for customer support, sales assistants, and operational copilots.

## Current Platform Notes (February 11, 2026)

- OpenAI documentation now emphasizes the **GA Realtime interface** and migration away from beta semantics.
- OpenAI deprecation documentation references **February 27, 2026** as the Realtime beta shutdown date.
- New builds should target GA endpoints/models and avoid beta-only assumptions.

## Tutorial Structure

| Chapter | Topic | What You Will Learn |
|:--------|:------|:--------------------|
| [1. Getting Started](01-getting-started.md) | Setup | Run the official demo and understand baseline architecture |
| [2. Realtime API Fundamentals](02-realtime-api-fundamentals.md) | Protocol | Session lifecycle, event flow, and transport choices |
| [3. Voice Input Processing](03-voice-input-processing.md) | Audio In | Capture, VAD strategy, interruption handling, normalization |
| [4. Conversational AI](04-conversational-ai.md) | Dialogue | Turn management, memory boundaries, and response strategy |
| [5. Function Calling](05-function-calling.md) | Tooling | Real-time tool execution and safe result integration |
| [6. Voice Output](06-voice-output.md) | Audio Out | Streaming speech responses and barge-in behavior |
| [7. Advanced Patterns](07-advanced-patterns.md) | Orchestration | Chat-supervisor and sequential-handoff implementations |
| [8. Production Deployment](08-production-deployment.md) | Operations | Security, latency, reliability, and rollout controls |

## Prerequisites

- TypeScript/JavaScript comfort
- WebSocket/WebRTC fundamentals
- OpenAI platform credentials and API access
- Basic frontend debugging skills (browser devtools)

## Related Tutorials

**Prerequisites:**
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/) - API interaction fundamentals

**Complementary:**
- [OpenAI Whisper Tutorial](../openai-whisper-tutorial/) - speech transcription foundations
- [Swarm Tutorial](../swarm-tutorial/) - multi-agent routing concepts

---

Ready to begin? Start with [Chapter 1: Getting Started](01-getting-started.md).

---

*Built from the official [openai-realtime-agents repository](https://github.com/openai/openai-realtime-agents), OpenAI Python SDK documentation, and OpenAI Realtime migration guidance.*
