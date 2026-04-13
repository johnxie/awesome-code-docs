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

## Source Code Walkthrough

### `packages/ai/package.json`

The `for` interface in [`packages/ai/package.json`](https://github.com/vercel/ai/blob/HEAD/packages/ai/package.json) handles a key part of this chapter's functionality:

```json
  "name": "ai",
  "version": "7.0.0-beta.64",
  "description": "AI SDK by Vercel - build apps like ChatGPT, Claude, Gemini, and more with a single interface for any model using the Vercel AI Gateway or go direct to OpenAI, Anthropic, Google, or any other model provider.",
  "license": "Apache-2.0",
  "sideEffects": false,
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "source": "./src/index.ts",
  "files": [
    "dist/**/*",
    "docs/**/*",
    "src",
    "!src/**/*.test.ts",
    "!src/**/*.test-d.ts",
    "!src/**/__snapshots__",
    "CHANGELOG.md",
    "internal.d.ts",
    "README.md",
    "test.d.ts"
  ],
  "directories": {
    "doc": "./docs"
  },
  "scripts": {
    "build": "pnpm clean && tsup --tsconfig tsconfig.build.json",
    "build:watch": "pnpm clean && tsup --watch --tsconfig tsconfig.build.json",
    "clean": "del-cli dist docs *.tsbuildinfo",
    "prepack": "cp -r ../../content/docs ./docs",
    "postpack": "del-cli docs",
    "type-check": "tsc --build",
    "test": "pnpm test:node && pnpm test:edge",
```

This interface is important because it defines how Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[for]
```
