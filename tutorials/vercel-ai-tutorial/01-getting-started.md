---
layout: default
title: "Chapter 1: Getting Started with Vercel AI"
parent: "Vercel AI Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Vercel AI

Welcome to Vercel AI! If you've ever wanted to build AI-powered applications with TypeScript and React, you're in the right place. Vercel AI is the comprehensive toolkit created by the makers of Next.js for building modern AI applications with type safety, streaming responses, and seamless integration.

## What Makes Vercel AI Special?

Vercel AI revolutionizes AI application development by:

- **Type-Safe AI** - Full TypeScript support with type-safe AI interactions
- **Streaming First** - Built-in support for real-time streaming responses
- **Provider Agnostic** - Works with OpenAI, Anthropic, and other AI providers
- **React Integration** - Seamless integration with React and Next.js
- **Tool Calling** - Native support for function calling and tool integration
- **Production Ready** - Built for scale with proper error handling

## Installing Vercel AI

### Basic Installation

```bash
# Create a new Next.js project
npx create-next-app@latest my-ai-app --typescript --tailwind --eslint --app
cd my-ai-app

# Install Vercel AI
npm install ai

# Install AI provider SDKs (choose what you need)
npm install openai anthropic @google/gemini-sdk
```

### Environment Setup

```bash
# Create environment variables
echo "OPENAI_API_KEY=your-openai-key" > .env.local
echo "ANTHROPIC_API_KEY=your-anthropic-key" >> .env.local
```

## Your First AI Application

Let's create your first AI-powered application:

```typescript
// app/api/chat/route.ts
import { openai } from '@ai-sdk/openai'
import { streamText } from 'ai'

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
  })

  return result.toDataStreamResponse()
}
```

```tsx
// app/page.tsx
'use client'

import { useChat } from 'ai/react'

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat()

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-auto p-4">
        {messages.map(m => (
          <div key={m.id} className="mb-4">
            <strong>{m.role}:</strong> {m.content}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Say something..."
          className="w-full p-2 border rounded"
        />
      </form>
    </div>
  )
}
```

## Understanding Vercel AI Concepts

### Core Components

```typescript
// The generateText function for non-streaming responses
import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'

const { text } = await generateText({
  model: openai('gpt-4'),
  prompt: 'Write a haiku about TypeScript'
})

// The streamText function for real-time responses
import { streamText } from 'ai'

const result = await streamText({
  model: openai('gpt-4'),
  prompt: 'Explain quantum computing'
})

for await (const delta of result.textStream) {
  console.log(delta) // Stream text in real-time
}
```

### Provider Configuration

```typescript
// OpenAI provider
import { openai } from '@ai-sdk/openai'

const openaiModel = openai('gpt-4', {
  // Additional configuration
})

// Anthropic provider
import { anthropic } from '@ai-sdk/anthropic'

const claudeModel = anthropic('claude-3-sonnet-20240229', {
  // Configuration options
})

// Multiple providers
const models = {
  gpt4: openai('gpt-4'),
  claude: anthropic('claude-3-sonnet-20240229'),
  // Add more providers as needed
}
```

## Building a Simple Chat Interface

```tsx
// components/ChatInterface.tsx
'use client'

import { useChat } from 'ai/react'
import { useState } from 'react'

export function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    onError: (error) => {
      console.error('Chat error:', error)
    }
  })

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">AI Chat</h2>

        <div className="h-96 overflow-auto mb-4 p-4 border rounded">
          {messages.length === 0 && (
            <p className="text-gray-500">Start a conversation...</p>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`mb-4 p-3 rounded ${
                message.role === 'user'
                  ? 'bg-blue-100 ml-12'
                  : 'bg-gray-100 mr-12'
              }`}
            >
              <strong className="block mb-1">
                {message.role === 'user' ? 'You' : 'AI'}:
              </strong>
              {message.content}
            </div>
          ))}

          {isLoading && (
            <div className="text-gray-500 italic">AI is thinking...</div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

## Advanced Configuration

### Custom API Routes

```typescript
// app/api/generate/route.ts
import { openai } from '@ai-sdk/openai'
import { generateText } from 'ai'

export async function POST(req: Request) {
  const { prompt, temperature = 0.7, maxTokens = 1000 } = await req.json()

  try {
    const { text } = await generateText({
      model: openai('gpt-4'),
      prompt,
      temperature,
      maxTokens,
    })

    return Response.json({ success: true, text })
  } catch (error) {
    return Response.json(
      { success: false, error: error.message },
      { status: 500 }
    )
  }
}
```

### Error Handling

```typescript
// utils/ai-error-handler.ts
export class AIError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message)
    this.name = 'AIError'
  }
}

export function handleAIError(error: any): AIError {
  if (error?.response?.status === 429) {
    return new AIError('Rate limit exceeded', 'RATE_LIMIT', 429)
  }

  if (error?.response?.status === 401) {
    return new AIError('Invalid API key', 'INVALID_API_KEY', 401)
  }

  if (error?.code === 'ECONNREFUSED') {
    return new AIError('AI service unavailable', 'SERVICE_UNAVAILABLE', 503)
  }

  return new AIError(
    error?.message || 'Unknown AI error',
    'UNKNOWN_ERROR',
    500
  )
}
```

### Logging and Monitoring

```typescript
// utils/ai-logger.ts
import { NextRequest } from 'next/server'

export function logAIRequest(req: NextRequest, prompt: string) {
  console.log(`[${new Date().toISOString()}] AI Request:`, {
    method: req.method,
    url: req.url,
    prompt: prompt.substring(0, 100) + '...',
    userAgent: req.headers.get('user-agent'),
    ip: req.ip
  })
}

export function logAIResponse(response: any, duration: number) {
  console.log(`[${new Date().toISOString()}] AI Response:`, {
    success: response.success,
    duration: `${duration}ms`,
    tokens: response.usage?.totalTokens,
    model: response.model
  })
}
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed Vercel AI** and set up your development environment
2. **Created your first AI chat application** with streaming responses
3. **Built a React chat interface** with real-time AI interactions
4. **Implemented error handling** and logging for production readiness
5. **Configured multiple AI providers** for flexible deployment
6. **Set up TypeScript types** for type-safe AI interactions

## Next Steps

Now that you understand Vercel AI basics, let's explore text generation in depth. In [Chapter 2: Text Generation](02-text-generation.md), we'll dive into different generation patterns, prompt engineering, and working with various AI models.

---

**Practice what you've learned:**
1. Create a custom chat application with your preferred styling
2. Add support for multiple AI providers with fallback logic
3. Implement conversation history and context management
4. Build a simple AI writing assistant
5. Add rate limiting and request throttling

*What kind of AI application will you build first?* 🤖

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- tutorial slug: **vercel-ai-tutorial**
- chapter focus: **Chapter 1: Getting Started with Vercel AI**
- system context: **Vercel Ai Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started with Vercel AI`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [AI SDK Repository](https://github.com/vercel/ai)
- [AI SDK Releases](https://github.com/vercel/ai/releases)
- [AI SDK Docs](https://ai-sdk.dev)

### Cross-Tutorial Connection Map

- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/)
- [OpenAI Realtime Agents Tutorial](../openai-realtime-agents-tutorial/)
- [Dyad Tutorial](../dyad-tutorial/)
- [bolt.diy Tutorial](../bolt-diy-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 1: Getting Started with Vercel AI`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

### Scenario Playbook 1: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 1: Getting Started with Vercel AI

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `openai`, `className`, `error` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Vercel AI` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `message`, `text`, `messages` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Vercel AI` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `openai`.
2. **Input normalization**: shape incoming data so `className` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `error`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [AI SDK Repository](https://github.com/vercel/ai)
  Why it matters: authoritative reference on `AI SDK Repository` (github.com).
- [AI SDK Releases](https://github.com/vercel/ai/releases)
  Why it matters: authoritative reference on `AI SDK Releases` (github.com).
- [AI SDK Docs](https://ai-sdk.dev)
  Why it matters: authoritative reference on `AI SDK Docs` (ai-sdk.dev).

Suggested trace strategy:
- search upstream code for `openai` and `className` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Text Generation](02-text-generation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
