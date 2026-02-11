---
layout: default
title: "OpenAI Python SDK Tutorial"
nav_order: 93
has_children: true
---

# OpenAI Python SDK Tutorial: Production API Patterns

> Build reliable Python applications with the official OpenAI SDK using Responses-first workflows, with clear migration guidance for legacy APIs.

[![Stars](https://img.shields.io/github/stars/openai/openai-python?style=social)](https://github.com/openai/openai-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://github.com/openai/openai-python)

## What is current in the SDK

According to the official `openai-python` README:

- **Responses API** is the primary interface for model interaction.
- **Chat Completions API** remains supported for existing systems.
- Sync and async clients are both first-class.
- Realtime and streaming interfaces are available through SDK-supported channels.

## Migration Notes (February 11, 2026)

OpenAI documentation indicates:

- target sunset for Assistants API around **August 26, 2026**
- migration path centered on Responses API + Agents platform patterns

If you are starting new development now, default to Responses-first architecture.

## Tutorial Structure

| Chapter | Topic | What You Will Learn |
|:--------|:------|:--------------------|
| [1. Getting Started](01-getting-started.md) | Setup | Install, authenticate, and make first Responses API calls |
| [2. Chat Completions](02-chat-completions.md) | Legacy + Interop | Use message-based flows and decide when to keep them |
| [3. Embeddings and Search](03-embeddings-search.md) | Retrieval | Build semantic retrieval pipelines and RAG foundations |
| [4. Agents and Assistants](04-assistants-api.md) | Transition | Operate current assistant patterns while planning migration |
| [5. Batch Processing](05-batch-processing.md) | Scale | Run large asynchronous jobs with traceable artifacts |
| [6. Fine-Tuning](06-fine-tuning.md) | Specialization | Curate datasets, train models, and evaluate quality |
| [7. Advanced Patterns](07-advanced-patterns.md) | Production | Reliability, observability, and cost control patterns |
| [8. Integration Examples](08-integration-examples.md) | Applications | FastAPI, retrieval services, and tool-enabled endpoints |

## Prerequisites

- Python 3.9+
- OpenAI API credentials
- Basic REST/JSON understanding
- Familiarity with async programming (recommended)

## Related Tutorials

**Complementary:**
- [tiktoken Tutorial](../tiktoken-tutorial/) - token accounting and budgeting
- [OpenAI Realtime Agents Tutorial](../openai-realtime-agents-tutorial/) - voice and low-latency orchestration
- [OpenAI Whisper Tutorial](../openai-whisper-tutorial/) - speech processing pipelines

---

Ready to begin? Start with [Chapter 1: Getting Started](01-getting-started.md).

---

*Built from the official [openai/openai-python repository](https://github.com/openai/openai-python) and OpenAI platform migration/deprecation documentation.*
