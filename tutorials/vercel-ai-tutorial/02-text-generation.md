---
layout: default
title: "Chapter 2: Text Generation"
parent: "Vercel AI Tutorial"
nav_order: 2
---


# Chapter 2: Text Generation

Welcome to **Chapter 2: Text Generation**. In this part of **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! Now that you have Vercel AI set up and running, it's time to dive deep into text generation. Think of text generation as the heart of AI applications - it's where you transform prompts into meaningful responses, stories, code, and more.

## Understanding Text Generation

Text generation is the process of creating human-like text from input prompts. Vercel AI makes this incredibly powerful with its type-safe approach and support for multiple AI providers.

### Why Text Generation Matters

Imagine you're building:
- **A writing assistant** that helps users craft better emails
- **A code generator** that creates boilerplate code
- **A content creator** that generates blog posts or social media content
- **A chatbot** that provides contextual responses

Each of these relies on sophisticated text generation techniques.

## Basic Text Generation

Let's start with the fundamentals:

```typescript
// app/api/generate/route.ts
import { openai } from '@ai-sdk/openai'
import { generateText } from 'ai'

export async function POST(req: Request) {
  const { prompt, model = 'gpt-4', temperature = 0.7 } = await req.json()

  try {
    const { text } = await generateText({
      model: openai(model),
      prompt,
      temperature,
      maxTokens: 1000,
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

### Temperature and Creativity

Temperature controls how "creative" your AI responses are:

```typescript
// Low temperature (0.1-0.3) - More focused and deterministic
const focusedResponse = await generateText({
  model: openai('gpt-4'),
  prompt: 'Explain quantum physics',
  temperature: 0.1, // Very focused
})

// Medium temperature (0.5-0.7) - Balanced creativity
const balancedResponse = await generateText({
  model: openai('gpt-4'),
  prompt: 'Write a short story',
  temperature: 0.7, // Creative but controlled
})

// High temperature (0.8-1.0) - Very creative
const creativeResponse = await generateText({
  model: openai('gpt-4'),
  prompt: 'Brainstorm app ideas',
  temperature: 0.9, // Highly creative
})
```

## Working with Multiple Providers

One of Vercel AI's strengths is provider flexibility:

```typescript
// utils/models.ts
import { openai } from '@ai-sdk/openai'
import { anthropic } from '@ai-sdk/anthropic'
import { google } from '@ai-sdk/google'

export const models = {
  // OpenAI models
  gpt4: openai('gpt-4'),
  gpt35: openai('gpt-3.5-turbo'),

  // Anthropic models
  claude: anthropic('claude-3-sonnet-20240229'),
  claudeHaiku: anthropic('claude-3-haiku-20240307'),

  // Google models
  gemini: google('models/gemini-pro'),
} as const

export type ModelKey = keyof typeof models
```

### Provider Router

```typescript
// app/api/chat/route.ts
import { models } from '@/utils/models'
import { generateText } from 'ai'

export async function POST(req: Request) {
  const { prompt, provider = 'gpt4' } = await req.json()

  const model = models[provider as keyof typeof models]

  if (!model) {
    return Response.json(
      { error: 'Invalid provider' },
      { status: 400 }
    )
  }

  const { text } = await generateText({
    model,
    prompt,
  })

  return Response.json({ text })
}
```

## Advanced Prompt Engineering

Effective prompts are crucial for good results:

```typescript
// Prompt templates
const promptTemplates = {
  codeReview: (code: string) => `
    You are an expert code reviewer. Review the following code for:
    - Best practices
    - Performance issues
    - Security concerns
    - Readability improvements

    Code to review:
    ${code}

    Provide specific, actionable feedback.
  `,

  creativeWriting: (topic: string, style: string) => `
    Write a compelling ${style} about ${topic}.
    Make it engaging and well-structured.
    Include vivid descriptions and emotional depth.
  `,

  technicalExplanation: (concept: string) => `
    Explain ${concept} to a developer with 2-3 years experience.
    Use analogies and practical examples.
    Include code snippets where relevant.
    Avoid oversimplification.
  `,
}

// Usage
const codeReviewPrompt = promptTemplates.codeReview(userCode)
const storyPrompt = promptTemplates.creativeWriting('space exploration', 'short story')
const explanationPrompt = promptTemplates.technicalExplanation('dependency injection')
```

### Few-Shot Learning

```typescript
const fewShotPrompt = `
Generate a function name for the following description.

Examples:
Description: "Calculate the average of an array of numbers"
Function: calculateAverage

Description: "Convert string to uppercase"
Function: convertToUppercase

Description: "Validate email format"
Function: validateEmail

Description: "${userDescription}"
Function:`
```

## Structured Text Generation

Sometimes you need structured output:

```typescript
// Generate structured data
const structuredPrompt = `
Generate a product description for a new smartphone.

Respond with valid JSON in this format:
{
  "name": "Product Name",
  "features": ["feature1", "feature2"],
  "price": 999,
  "category": "electronics"
}

Product idea: ${userIdea}
`

const { text } = await generateText({
  model: openai('gpt-4'),
  prompt: structuredPrompt,
})

// Parse the JSON response
try {
  const product = JSON.parse(text)
  console.log('Generated product:', product)
} catch (error) {
  console.error('Failed to parse JSON response')
}
```

## Building a Text Generation Playground

Let's create an interactive playground:

```tsx
// components/TextGenerator.tsx
'use client'

import { useState } from 'react'
import { generateText } from 'ai'
import { models } from '@/utils/models'

export function TextGenerator() {
  const [prompt, setPrompt] = useState('')
  const [provider, setProvider] = useState('gpt4')
  const [temperature, setTemperature] = useState(0.7)
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setLoading(true)
    try {
      const model = models[provider as keyof typeof models]
      const { text } = await generateText({
        model,
        prompt,
        temperature,
      })
      setResult(text)
    } catch (error) {
      setResult(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Text Generation Playground</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">
              AI Provider
            </label>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="w-full p-2 border rounded"
            >
              <option value="gpt4">GPT-4</option>
              <option value="gpt35">GPT-3.5 Turbo</option>
              <option value="claude">Claude 3</option>
              <option value="gemini">Gemini Pro</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">
              Temperature: {temperature}
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">
              Prompt
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt here..."
              className="w-full h-32 p-2 border rounded"
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !prompt.trim()}
            className="w-full px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Generate Text'}
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Generated Result
          </label>
          <div className="h-64 p-4 border rounded bg-gray-50 overflow-auto">
            {result || 'Your generated text will appear here...'}
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Error Handling and Retry Logic

```typescript
// utils/text-generation.ts
export async function generateWithRetry(
  model: any,
  prompt: string,
  options: {
    maxRetries?: number
    retryDelay?: number
    temperature?: number
  } = {}
) {
  const { maxRetries = 3, retryDelay = 1000, temperature = 0.7 } = options

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const { text } = await generateText({
        model,
        prompt,
        temperature,
      })
      return text
    } catch (error) {
      console.warn(`Attempt ${attempt} failed:`, error.message)

      if (attempt === maxRetries) {
        throw error
      }

      // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, retryDelay * attempt))
    }
  }
}
```

## Performance Optimization

### Caching Generated Content

```typescript
// utils/cache.ts
const cache = new Map<string, { text: string; timestamp: number }>()
const CACHE_DURATION = 1000 * 60 * 60 // 1 hour

export function getCachedText(prompt: string): string | null {
  const cached = cache.get(prompt)
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.text
  }
  return null
}

export function setCachedText(prompt: string, text: string) {
  cache.set(prompt, { text, timestamp: Date.now() })
}
```

### Batch Processing

```typescript
// For processing multiple prompts efficiently
export async function generateBatch(
  model: any,
  prompts: string[],
  options: { temperature?: number } = {}
) {
  const results = await Promise.allSettled(
    prompts.map(prompt =>
      generateText({
        model,
        prompt,
        temperature: options.temperature || 0.7,
      })
    )
  )

  return results.map((result, index) => ({
    prompt: prompts[index],
    success: result.status === 'fulfilled',
    text: result.status === 'fulfilled' ? result.value.text : null,
    error: result.status === 'rejected' ? result.reason : null,
  }))
}
```

## What We've Accomplished

Excellent work! 🎉 You've mastered:

1. **Basic text generation** with different temperature settings
2. **Multi-provider support** for flexible AI interactions
3. **Advanced prompt engineering** techniques
4. **Structured output generation** for consistent results
5. **Interactive playground** for testing different configurations
6. **Error handling and retry logic** for production reliability
7. **Performance optimization** with caching and batch processing

## Next Steps

Ready to take your AI applications to the next level? In [Chapter 3: Streaming Responses](03-streaming-responses.md), we'll explore real-time streaming - the secret sauce behind modern AI chat interfaces!

---

**Practice what you've learned:**
1. Build a prompt engineering tool with different templates
2. Create a multi-provider text comparison interface
3. Implement caching for frequently used prompts
4. Add batch processing for multiple text generation tasks
5. Experiment with different temperature settings for various use cases

*What's the most interesting text generation application you can think of?* 🤖

## Depth Expansion Playbook

## Source Code Walkthrough

Use the following upstream sources to verify text generation implementation details while reading this chapter:

- [`packages/ai/src/generate-text/generate-text.ts`](https://github.com/vercel/ai/blob/HEAD/packages/ai/src/generate-text/generate-text.ts) — the `generateText` function implementation, the primary non-streaming text generation entry point that wraps model provider calls, tool execution, and result assembly.
- [`packages/ai/src/generate-text/index.ts`](https://github.com/vercel/ai/blob/HEAD/packages/ai/src/generate-text/index.ts) — the package exports for the text generation surface, showing which types and functions are part of the public API.

Suggested trace strategy:
- trace `generateText` to understand how the provider abstraction, prompt formatting, and tool loop are composed
- review the `GenerateTextResult` type to understand all fields available after a generation call completes
- check `packages/ai/src/core/` for the shared model call infrastructure used by both `generateText` and `streamText`

## How These Components Connect

```mermaid
flowchart LR
    A[generateText call] --> B[Provider abstraction layer]
    B --> C[LLM API request]
    C --> D[GenerateTextResult returned]
    D --> E[text, usage, finishReason available]
```