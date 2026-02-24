---
layout: default
title: "Chapter 3: Streaming Responses"
parent: "Vercel AI Tutorial"
nav_order: 3
---

# Chapter 3: Streaming Responses

Welcome to the world of real-time AI! Streaming responses are what make modern AI applications feel alive and responsive. Instead of waiting for the complete response, users see text appear character by character, creating an engaging, interactive experience.

## Why Streaming Matters

Imagine the difference between:
- **Traditional responses**: User waits 5-10 seconds, then sees the entire response
- **Streaming responses**: User sees text appear immediately, feels like a real conversation

Streaming creates better user experience, reduces perceived latency, and makes AI feel more human-like.

## Basic Streaming with Vercel AI

Let's start with the fundamentals:

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

### Understanding the Stream

The `streamText` function returns a result with multiple streaming capabilities:

```typescript
const result = await streamText({
  model: openai('gpt-4'),
  messages,
})

// Text stream - for real-time text display
for await (const delta of result.textStream) {
  console.log('New text:', delta)
}

// Full response stream - includes metadata
for await (const delta of result.fullStream) {
  if (delta.type === 'text-delta') {
    console.log('Text delta:', delta.textDelta)
  }
}
```

## Building a Streaming Chat Interface

Let's create a modern chat interface with real-time streaming:

```tsx
// components/StreamingChat.tsx
'use client'

import { useState, useRef, useEffect } from 'react'
import { Message } from '@/types/chat'

interface StreamingChatProps {
  messages: Message[]
  onSendMessage: (content: string) => void
  isLoading: boolean
}

export function StreamingChat({ messages, onSendMessage, isLoading }: StreamingChatProps) {
  const [input, setInput] = useState('')
  const [streamingMessage, setStreamingMessage] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingMessage])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    onSendMessage(input)
    setInput('')
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Messages Area */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {/* Streaming Message */}
        {streamingMessage && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
              {streamingMessage}
              <span className="animate-pulse">|</span>
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        {isLoading && !streamingMessage && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                <span>AI is thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}
```

## Implementing Streaming on the Frontend

Now let's connect the streaming to the frontend:

```tsx
// hooks/useStreamingChat.ts
import { useState, useCallback } from 'react'
import { Message } from '@/types/chat'

export function useStreamingChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [streamingMessage, setStreamingMessage] = useState('')

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setStreamingMessage('')

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [...messages, userMessage],
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('No response stream available')
      }

      let accumulatedMessage = ''

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)

            if (data === '[DONE]') {
              // Stream complete
              const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: accumulatedMessage,
              }
              setMessages(prev => [...prev, aiMessage])
              setStreamingMessage('')
              break
            }

            try {
              const parsed = JSON.parse(data)
              if (parsed.choices?.[0]?.delta?.content) {
                const content = parsed.choices[0].delta.content
                accumulatedMessage += content
                setStreamingMessage(accumulatedMessage)
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [messages])

  return {
    messages,
    isLoading,
    streamingMessage,
    sendMessage,
  }
}
```

## Advanced Streaming Features

### Streaming with Tool Calls

```typescript
// app/api/chat-with-tools/route.ts
import { openai } from '@ai-sdk/openai'
import { streamText, tool } from 'ai'
import { z } from 'zod'

// Define tools
const weatherTool = tool({
  description: 'Get current weather for a location',
  parameters: z.object({
    location: z.string().describe('The city or location to get weather for'),
  }),
  execute: async ({ location }) => {
    // Simulate weather API call
    return {
      location,
      temperature: Math.floor(Math.random() * 30) + 10,
      condition: 'Sunny',
    }
  },
})

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
    tools: {
      weather: weatherTool,
    },
  })

  return result.toDataStreamResponse()
}
```

### Streaming with Custom Formatting

```typescript
// app/api/formatted-stream/route.ts
import { openai } from '@ai-sdk/openai'
import { streamText } from 'ai'

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
    onChunk: ({ chunk }) => {
      // Custom processing for each chunk
      console.log('Processing chunk:', chunk)
    },
    onFinish: ({ text }) => {
      // Post-processing
      console.log('Stream finished, total length:', text.length)
    },
  })

  return result.toDataStreamResponse()
}
```

## Handling Stream Errors

```typescript
// utils/stream-error-handler.ts
export class StreamError extends Error {
  constructor(
    message: string,
    public code: string,
    public recoverable: boolean = false
  ) {
    super(message)
    this.name = 'StreamError'
  }
}

export function handleStreamError(error: any): StreamError {
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    return new StreamError(
      'Network connection lost. Please check your internet connection.',
      'NETWORK_ERROR',
      true
    )
  }

  if (error.message.includes('rate limit')) {
    return new StreamError(
      'Too many requests. Please wait a moment before trying again.',
      'RATE_LIMIT',
      true
    )
  }

  return new StreamError(
    'An unexpected error occurred during streaming.',
    'UNKNOWN_ERROR',
    false
  )
}
```

## Optimizing Streaming Performance

### Connection Pooling

```typescript
// lib/stream-pool.ts
class StreamPool {
  private activeStreams = new Set<ReadableStream>()

  async createStream(url: string, options: RequestInit) {
    const response = await fetch(url, options)
    const stream = response.body

    if (stream) {
      this.activeStreams.add(stream)

      // Clean up when stream ends
      stream.getReader().read().finally(() => {
        this.activeStreams.delete(stream)
      })
    }

    return response
  }

  getActiveStreamCount() {
    return this.activeStreams.size
  }

  async closeAllStreams() {
    for (const stream of this.activeStreams) {
      try {
        await stream.cancel()
      } catch (error) {
        console.warn('Error closing stream:', error)
      }
    }
    this.activeStreams.clear()
  }
}

export const streamPool = new StreamPool()
```

### Adaptive Streaming

```typescript
// utils/adaptive-streaming.ts
export function createAdaptiveStreamer(options: {
  slowStart?: boolean
  batchSize?: number
  delayBetweenBatches?: number
} = {}) {
  const { slowStart = true, batchSize = 10, delayBetweenBatches = 50 } = options

  return async function* adaptiveStream(text: string) {
    const chunks = text.split('')
    let currentBatch = 0

    for (let i = 0; i < chunks.length; i += batchSize) {
      const batch = chunks.slice(i, i + batchSize)
      const batchText = batch.join('')

      yield batchText

      // Adaptive delay - slower at start, faster later
      if (slowStart && currentBatch < 5) {
        await new Promise(resolve => setTimeout(resolve, delayBetweenBatches * 2))
      } else {
        await new Promise(resolve => setTimeout(resolve, delayBetweenBatches))
      }

      currentBatch++
    }
  }
}
```

## Building a Streaming Progress Indicator

```tsx
// components/StreamingProgress.tsx
'use client'

interface StreamingProgressProps {
  isActive: boolean
  messageCount: number
}

export function StreamingProgress({ isActive, messageCount }: StreamingProgressProps) {
  if (!isActive) return null

  return (
    <div className="fixed top-4 right-4 bg-white rounded-lg shadow-lg p-4 min-w-64">
      <div className="flex items-center space-x-3">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
        <div>
          <div className="font-medium text-gray-900">Streaming Response</div>
          <div className="text-sm text-gray-600">
            Processing message {messageCount}
          </div>
        </div>
      </div>

      <div className="mt-3">
        <div className="flex space-x-1">
          <div className="flex-1 h-2 bg-gray-200 rounded">
            <div className="h-2 bg-blue-500 rounded animate-pulse"></div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Real-World Streaming Example

Let's build a complete streaming chat application:

```tsx
// pages/index.tsx
'use client'

import { StreamingChat } from '@/components/StreamingChat'
import { StreamingProgress } from '@/components/StreamingProgress'
import { useStreamingChat } from '@/hooks/useStreamingChat'

export default function Home() {
  const { messages, isLoading, streamingMessage, sendMessage } = useStreamingChat()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            AI Streaming Chat
          </h1>
          <p className="text-gray-600">
            Experience real-time AI conversations
          </p>
        </div>
      </header>

      <main className="flex-1">
        <StreamingChat
          messages={messages}
          onSendMessage={sendMessage}
          isLoading={isLoading}
        />
      </main>

      <StreamingProgress
        isActive={isLoading}
        messageCount={messages.length}
      />
    </div>
  )
}
```

## What We've Accomplished

Fantastic! 🎉 You've mastered streaming responses:

1. **Basic streaming setup** with Vercel AI's `streamText`
2. **Real-time chat interface** with smooth text appearance
3. **Error handling** for robust streaming connections
4. **Performance optimization** with connection pooling
5. **Advanced features** like tool calling during streams
6. **Progress indicators** for better user experience
7. **Adaptive streaming** for optimal performance

## Next Steps

Ready for more advanced AI capabilities? In [Chapter 4: Function Calling](04-function-calling.md), we'll explore how to connect your AI to external tools and APIs for even more powerful applications!

---

**Practice what you've learned:**
1. Add typing indicators during streaming
2. Implement stream interruption and resumption
3. Create different streaming speeds for different content types
4. Add streaming analytics and performance monitoring
5. Build a collaborative streaming chat with multiple users

*How will you use streaming to enhance your AI applications?* ⚡

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- tutorial slug: **vercel-ai-tutorial**
- chapter focus: **Chapter 3: Streaming Responses**
- system context: **Vercel Ai Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 3: Streaming Responses`.
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

1. Build a minimal end-to-end implementation for `Chapter 3: Streaming Responses`.
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

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `className`, `messages`, `text` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Streaming Responses` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `stream`, `flex`, `gray` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Streaming Responses` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `className`.
2. **Input normalization**: shape incoming data so `messages` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `text`.
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
- search upstream code for `className` and `messages` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Text Generation](02-text-generation.md)
- [Next Chapter: Chapter 4: Function Calling](04-function-calling.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
