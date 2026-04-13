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

## Source Code Walkthrough

Use the following upstream sources to verify streaming response implementation details while reading this chapter:

- [`packages/ai/src/stream-text/stream-text.ts`](https://github.com/vercel/ai/blob/HEAD/packages/ai/src/stream-text/stream-text.ts) — the `streamText` function implementation, providing the streaming counterpart to `generateText` with text delta, tool call, and finish event streams.
- [`packages/ai/src/ui/use-chat.ts`](https://github.com/vercel/ai/blob/HEAD/packages/ai/src/ui/use-chat.ts) — the `useChat` React hook that consumes the data stream protocol from `streamText` and exposes messages, input, and status state for UI integration.

Suggested trace strategy:
- trace `streamText` to understand the `textStream`, `toolCallStream`, and `fullStream` properties returned
- review how the data stream protocol format works by tracing the response body format from a Next.js route handler
- check `useChat` to see how streaming chunks are parsed and accumulated into the messages state array

## How These Components Connect

```mermaid
flowchart LR
    A[streamText in API route] --> B[Data stream protocol response]
    B --> C[useChat hook in React]
    C --> D[messages state updated incrementally]
    D --> E[UI renders streaming text]
```