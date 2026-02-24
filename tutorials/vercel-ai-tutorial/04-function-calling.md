---
layout: default
title: "Chapter 4: Function Calling"
parent: "Vercel AI Tutorial"
nav_order: 4
---

# Chapter 4: Function Calling

Welcome to the world of AI agents! Function calling (also known as tool calling) is what transforms simple chatbots into powerful AI assistants that can interact with the real world. Instead of just generating text, your AI can now call APIs, execute code, and perform actions.

## Understanding Function Calling

Function calling allows AI models to:
- **Call external APIs** (weather, databases, payment systems)
- **Execute code** (calculations, data processing)
- **Access real-time data** (current events, user data)
- **Perform actions** (send emails, create files, trigger workflows)

Think of it as giving your AI superpowers beyond just conversation.

## Basic Function Calling Setup

Let's start with a simple weather tool:

```typescript
// app/api/chat-with-tools/route.ts
import { openai } from '@ai-sdk/openai'
import { streamText, tool } from 'ai'
import { z } from 'zod'

// Define the weather tool
const getWeather = tool({
  description: 'Get current weather for a location',
  parameters: z.object({
    location: z.string().describe('The city or location to get weather for'),
  }),
  execute: async ({ location }) => {
    // Simulate weather API call
    console.log(`Getting weather for: ${location}`)

    // In a real app, you'd call a weather API here
    const weatherData = {
      location,
      temperature: Math.floor(Math.random() * 30) + 10,
      condition: ['Sunny', 'Cloudy', 'Rainy', 'Snowy'][Math.floor(Math.random() * 4)],
      humidity: Math.floor(Math.random() * 40) + 40,
    }

    return weatherData
  },
})

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
    tools: {
      getWeather,
    },
  })

  return result.toDataStreamResponse()
}
```

## Creating Multiple Tools

Let's build a comprehensive toolkit:

```typescript
// tools/index.ts
import { tool } from 'ai'
import { z } from 'zod'

// Calculator tool
export const calculator = tool({
  description: 'Perform mathematical calculations',
  parameters: z.object({
    expression: z.string().describe('The mathematical expression to evaluate (e.g., "2 + 3 * 4")'),
  }),
  execute: async ({ expression }) => {
    try {
      // Simple evaluation (in production, use a safe math library)
      const result = Function('"use strict"; return (' + expression + ')')()
      return { result, expression }
    } catch (error) {
      return { error: 'Invalid expression', expression }
    }
  },
})

// Search tool
export const webSearch = tool({
  description: 'Search the web for current information',
  parameters: z.object({
    query: z.string().describe('The search query'),
    maxResults: z.number().optional().describe('Maximum number of results to return'),
  }),
  execute: async ({ query, maxResults = 5 }) => {
    // Simulate search API call
    const mockResults = [
      { title: `${query} - Wikipedia`, url: `https://en.wikipedia.org/wiki/${query}`, snippet: `Information about ${query}` },
      { title: `${query} News`, url: `https://news.example.com/${query}`, snippet: `Latest news about ${query}` },
      { title: `${query} Guide`, url: `https://guide.example.com/${query}`, snippet: `Complete guide to ${query}` },
    ].slice(0, maxResults)

    return { query, results: mockResults }
  },
})

// Code execution tool
export const runCode = tool({
  description: 'Execute JavaScript code and return the result',
  parameters: z.object({
    code: z.string().describe('The JavaScript code to execute'),
    timeout: z.number().optional().describe('Execution timeout in milliseconds'),
  }),
  execute: async ({ code, timeout = 5000 }) => {
    try {
      // In production, use a sandboxed environment
      const result = await Promise.race([
        Function('"use strict"; return (' + code + ')')(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Code execution timeout')), timeout)
        )
      ])

      return { result, success: true }
    } catch (error) {
      return { error: error.message, success: false }
    }
  },
})

// Database query tool
export const queryDatabase = tool({
  description: 'Query a database with SQL',
  parameters: z.object({
    query: z.string().describe('The SQL query to execute'),
    database: z.string().optional().describe('The database name'),
  }),
  execute: async ({ query, database = 'default' }) => {
    // Simulate database query
    console.log(`Executing query on ${database}: ${query}`)

    // In production, connect to actual database
    const mockResult = {
      rows: [
        { id: 1, name: 'Sample Data', value: 42 },
        { id: 2, name: 'More Data', value: 24 },
      ],
      rowCount: 2,
    }

    return mockResult
  },
})
```

## Building an AI Assistant with Tools

Now let's create a comprehensive AI assistant:

```typescript
// app/api/assistant/route.ts
import { openai } from '@ai-sdk/openai'
import { streamText } from 'ai'
import { calculator, webSearch, runCode, queryDatabase } from '@/tools'

export async function POST(req: Request) {
  const { messages } = await req.json()

  const systemPrompt = `You are a helpful AI assistant with access to various tools.

You can:
- Calculate mathematical expressions using the calculator tool
- Search the web for current information using webSearch
- Execute JavaScript code using runCode
- Query databases using queryDatabase

When a user asks for something you can accomplish with these tools, use the appropriate tool.
Always explain what you're doing and why you're using a particular tool.

If you need to use multiple tools, explain your plan first.`

  const result = await streamText({
    model: openai('gpt-4'),
    messages: [
      { role: 'system', content: systemPrompt },
      ...messages,
    ],
    tools: {
      calculator,
      webSearch,
      runCode,
      queryDatabase,
    },
  })

  return result.toDataStreamResponse()
}
```

## Handling Tool Results in the UI

Let's create a UI that shows tool usage:

```tsx
// components/ToolCallIndicator.tsx
'use client'

interface ToolCall {
  id: string
  name: string
  args: any
  result?: any
  status: 'pending' | 'running' | 'completed' | 'error'
}

interface ToolCallIndicatorProps {
  toolCalls: ToolCall[]
}

export function ToolCallIndicator({ toolCalls }: ToolCallIndicatorProps) {
  if (toolCalls.length === 0) return null

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 my-4">
      <h3 className="text-sm font-medium text-blue-900 mb-2">AI is using tools:</h3>
      <div className="space-y-2">
        {toolCalls.map((call) => (
          <div key={call.id} className="flex items-center space-x-2 text-sm">
            <div className={`w-2 h-2 rounded-full ${
              call.status === 'pending' ? 'bg-yellow-400' :
              call.status === 'running' ? 'bg-blue-400 animate-pulse' :
              call.status === 'completed' ? 'bg-green-400' :
              'bg-red-400'
            }`} />
            <span className="font-medium">{call.name}</span>
            <span className="text-gray-600">
              {call.status === 'pending' && 'Preparing...'}
              {call.status === 'running' && 'Running...'}
              {call.status === 'completed' && 'Completed'}
              {call.status === 'error' && 'Error'}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Advanced Tool Patterns

### Conditional Tool Execution

```typescript
// tools/conditional-tools.ts
import { tool } from 'ai'
import { z } from 'zod'

export const smartSearch = tool({
  description: 'Perform intelligent search with automatic result filtering',
  parameters: z.object({
    query: z.string().describe('The search query'),
    filters: z.object({
      dateRange: z.string().optional(),
      source: z.string().optional(),
      language: z.string().optional(),
    }).optional(),
  }),
  execute: async ({ query, filters }) => {
    console.log(`Smart search for: ${query}`, filters)

    // Conditional logic based on query type
    if (query.includes('weather')) {
      // Use weather API
      return { type: 'weather', data: await getWeatherData(query) }
    } else if (query.includes('code') || query.includes('programming')) {
      // Use code search
      return { type: 'code', data: await searchCode(query) }
    } else {
      // Use general web search
      return { type: 'web', data: await searchWeb(query, filters) }
    }
  },
})

// Helper functions
async function getWeatherData(location: string) {
  // Weather API logic
  return { location, temperature: 22, condition: 'Sunny' }
}

async function searchCode(query: string) {
  // Code search logic
  return { results: [], total: 0 }
}

async function searchWeb(query: string, filters?: any) {
  // Web search logic
  return { results: [], total: 0 }
}
```

### Tool Chaining

```typescript
// tools/tool-chain.ts
import { tool } from 'ai'
import { z } from 'zod'

export const analyzeAndReport = tool({
  description: 'Analyze data and generate a comprehensive report',
  parameters: z.object({
    topic: z.string().describe('The topic to analyze'),
    includeCharts: z.boolean().optional().describe('Whether to include chart recommendations'),
  }),
  execute: async ({ topic, includeCharts = false }) => {
    console.log(`Analyzing topic: ${topic}`)

    // Chain multiple operations
    const searchResults = await webSearch.execute({ query: topic })
    const analysis = await analyzeData(searchResults)
    const report = await generateReport(analysis, includeCharts)

    return {
      topic,
      searchResults: searchResults.results,
      analysis,
      report,
      charts: includeCharts ? generateCharts(analysis) : null,
    }
  },
})

// Helper functions for the chain
async function analyzeData(data: any) {
  return { summary: 'Analysis complete', insights: [] }
}

async function generateReport(analysis: any, includeCharts: boolean) {
  return { title: 'Analysis Report', sections: [] }
}

function generateCharts(analysis: any) {
  return { chartTypes: ['bar', 'line'], data: {} }
}
```

## Error Handling for Tools

```typescript
// utils/tool-error-handler.ts
export class ToolError extends Error {
  constructor(
    message: string,
    public tool: string,
    public code: string,
    public retryable: boolean = false
  ) {
    super(message)
    this.name = 'ToolError'
  }
}

export function handleToolError(error: any, toolName: string): ToolError {
  if (error.message?.includes('timeout')) {
    return new ToolError(
      `Tool ${toolName} timed out`,
      toolName,
      'TIMEOUT',
      true
    )
  }

  if (error.message?.includes('rate limit')) {
    return new ToolError(
      `Tool ${toolName} rate limited`,
      toolName,
      'RATE_LIMIT',
      true
    )
  }

  if (error.message?.includes('authentication')) {
    return new ToolError(
      `Tool ${toolName} authentication failed`,
      toolName,
      'AUTH_ERROR',
      false
    )
  }

  return new ToolError(
    `Tool ${toolName} failed: ${error.message}`,
    toolName,
    'UNKNOWN_ERROR',
    false
  )
}
```

## Building a Tool Manager

```typescript
// lib/tool-manager.ts
export class ToolManager {
  private tools = new Map<string, any>()
  private metrics = new Map<string, { calls: number, errors: number, avgTime: number }>()

  registerTool(name: string, tool: any) {
    this.tools.set(name, tool)
    this.metrics.set(name, { calls: 0, errors: 0, avgTime: 0 })
  }

  async executeTool(name: string, args: any) {
    const tool = this.tools.get(name)
    if (!tool) {
      throw new Error(`Tool ${name} not found`)
    }

    const startTime = Date.now()
    const metric = this.metrics.get(name)!

    try {
      metric.calls++
      const result = await tool.execute(args)

      const duration = Date.now() - startTime
      metric.avgTime = (metric.avgTime + duration) / metric.calls

      return result
    } catch (error) {
      metric.errors++
      throw error
    }
  }

  getMetrics() {
    return Object.fromEntries(this.metrics)
  }

  getAvailableTools() {
    return Array.from(this.tools.keys())
  }
}

export const toolManager = new ToolManager()
```

## Real-World Example: AI Data Analyst

Let's build a complete AI data analyst:

```tsx
// components/DataAnalyst.tsx
'use client'

import { useState } from 'react'
import { ToolCallIndicator } from './ToolCallIndicator'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  toolCalls?: any[]
}

export function DataAnalyst() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [toolCalls, setToolCalls] = useState<any[]>([])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setToolCalls([])

    try {
      const response = await fetch('/api/assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage],
        }),
      })

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.content,
        toolCalls: data.toolCalls,
      }

      setMessages(prev => [...prev, assistantMessage])
      setToolCalls(data.toolCalls || [])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">AI Data Analyst</h1>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="h-96 overflow-auto mb-4 p-4 border rounded">
          {messages.map((message) => (
            <div key={message.id} className="mb-4">
              <strong className="text-blue-600">
                {message.role === 'user' ? 'You' : 'AI Analyst'}:
              </strong>
              <p className="mt-1">{message.content}</p>
            </div>
          ))}

          {isLoading && (
            <div className="text-gray-500 italic">AI is analyzing...</div>
          )}
        </div>

        <ToolCallIndicator toolCalls={toolCalls} />

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me to analyze data, run calculations, or search for information..."
            className="flex-1 p-2 border rounded"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            Analyze
          </button>
        </form>
      </div>
    </div>
  )
}
```

## What We've Accomplished

Outstanding! 🎉 You've mastered function calling:

1. **Basic tool creation** with proper parameter validation
2. **Multiple tool integration** in AI assistants
3. **Tool result handling** in the user interface
4. **Advanced patterns** like conditional execution and chaining
5. **Error handling** for robust tool operations
6. **Tool management** with metrics and monitoring
7. **Real-world applications** like AI data analysts

## Next Steps

Ready to generate structured data with type safety? In [Chapter 5: Structured Outputs](05-structured-outputs.md), we'll explore how to make AI generate consistent, parseable data formats!

---

**Practice what you've learned:**
1. Create a custom tool for your specific use case
2. Build a tool that chains multiple operations
3. Add authentication and rate limiting to your tools
4. Create a dashboard showing tool usage metrics
5. Implement tool versioning and rollback capabilities

*What powerful tools will you create for your AI assistant?* 🛠️

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `query`, `tool`, `error` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Function Calling` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `className`, `tools`, `call` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Function Calling` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `query`.
2. **Input normalization**: shape incoming data so `tool` receives stable contracts.
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
- search upstream code for `query` and `tool` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Streaming Responses](03-streaming-responses.md)
- [Next Chapter: Chapter 5: Structured Outputs](05-structured-outputs.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
