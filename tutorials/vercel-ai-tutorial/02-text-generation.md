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

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- tutorial slug: **vercel-ai-tutorial**
- chapter focus: **Chapter 2: Text Generation**
- system context: **Vercel Ai Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 2: Text Generation`.
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

1. Build a minimal end-to-end implementation for `Chapter 2: Text Generation`.
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

### Scenario Playbook 1: Chapter 2: Text Generation

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 2: Text Generation

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 2: Text Generation

- tutorial context: **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `text`, `prompt`, `temperature` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Text Generation` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model`, `models`, `className` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Text Generation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `text`.
2. **Input normalization**: shape incoming data so `prompt` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `temperature`.
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
- search upstream code for `text` and `prompt` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Vercel AI](01-getting-started.md)
- [Next Chapter: Chapter 3: Streaming Responses](03-streaming-responses.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
