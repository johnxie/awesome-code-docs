---
layout: default
title: "Vercel AI Tutorial"
nav_order: 20
has_children: true
---

# Vercel AI SDK Tutorial: TypeScript AI Apps and Agents

> Build production AI features with `vercel/ai`, the provider-agnostic TypeScript toolkit behind modern streaming and agent-style app experiences.

[![Stars](https://img.shields.io/github/stars/vercel/ai?style=social)](https://github.com/vercel/ai)
[![License](https://img.shields.io/badge/License-Hybrid-yellow.svg)](https://github.com/vercel/ai)
[![Package](https://img.shields.io/badge/npm-ai-blue)](https://www.npmjs.com/package/ai)

## What is the AI SDK?

The AI SDK provides unified primitives for generating text/structured outputs, streaming UI updates, integrating tool loops, and routing models across multiple providers from one TypeScript interface.

Current official docs emphasize:

- unified provider architecture
- AI SDK UI hooks for framework integration
- agent/tool-loop capabilities
- compatibility with modern runtimes and frameworks

## Current Snapshot (February 11, 2026)

- repository: `vercel/ai`
- stars: ~21K
- active release stream: AI SDK `6.0.x`
- Node support in repo tooling includes modern LTS/current lines
- docs and reference are published at `ai-sdk.dev`

## Tutorial Chapters

1. **[Chapter 1: Getting Started with Vercel AI](01-getting-started.md)** - Installation and first generation calls
2. **[Chapter 2: Text Generation](02-text-generation.md)** - Provider-agnostic generation patterns
3. **[Chapter 3: Streaming Responses](03-streaming-responses.md)** - Real-time UX with streamed outputs
4. **[Chapter 4: Function Calling](04-function-calling.md)** - Tool integrations and execution loops
5. **[Chapter 5: Structured Outputs](05-structured-outputs.md)** - Typed schema-driven AI responses
6. **[Chapter 6: React Integration](06-react-integration.md)** - Hooks and component-level AI UX
7. **[Chapter 7: Next.js Applications](07-nextjs-applications.md)** - Full-stack AI app architecture
8. **[Chapter 8: Production Deployment](08-production-deployment.md)** - Scaling, observability, and reliability

## What You'll Learn

- build AI features with provider flexibility and type safety
- implement streaming-first user experiences
- design tool-calling workflows with robust validation
- ship and operate AI SDK applications in production

## Related Tutorials

- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/)
- [OpenAI Realtime Agents Tutorial](../openai-realtime-agents-tutorial/)
- [bolt.diy Tutorial](../bolt-diy-tutorial/)
- [Dyad Tutorial](../dyad-tutorial/)

---

Ready to begin? Continue to [Chapter 1: Getting Started](01-getting-started.md).
