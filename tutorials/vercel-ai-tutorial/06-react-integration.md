---
layout: default
title: "Chapter 6: React Integration"
parent: "Vercel AI Tutorial"
nav_order: 6
---

# Chapter 6: React Integration

Welcome to the exciting world of AI-powered React applications! This chapter is where theory meets practice - we'll build interactive, intelligent user interfaces that leverage the full power of Vercel AI with React's component system.

## Why React Integration Matters

React and AI are a perfect match because:
- **Real-time updates** - Components can react to streaming AI responses
- **State management** - Complex AI conversations fit naturally into React state
- **Component composition** - Build reusable AI-powered components
- **User experience** - Smooth, interactive AI interfaces

Let's build some amazing AI-powered React components!

## Basic AI Chat Component

```tsx
// components/AIChat.tsx
'use client'

import { useState, useRef, useEffect } from 'react'
import { Message } from '@/types/chat'

interface AIChatProps {
  apiEndpoint?: string
  placeholder?: string
  className?: string
}

export function AIChat({
  apiEndpoint = '/api/chat',
  placeholder = 'Ask me anything...',
  className = ''
}: AIChatProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [streamingMessage, setStreamingMessage] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingMessage])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setStreamingMessage('')

    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage],
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get AI response')
      }

      const reader = response.body?.getReader()
      if (!reader) throw new Error('No response stream')

      const decoder = new TextDecoder()
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
              const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: accumulatedMessage,
                timestamp: new Date(),
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
            } catch {
              // Skip invalid JSON
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={`flex flex-col h-full max-w-4xl mx-auto ${className}`}>
      {/* Messages Area */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.length === 0 && !streamingMessage && (
          <div className="text-center text-gray-500 py-8">
            <div className="text-4xl mb-4">🤖</div>
            <p>Start a conversation with AI</p>
          </div>
        )}

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
              <p className="whitespace-pre-wrap">{message.content}</p>
              <span className="text-xs opacity-70 mt-1 block">
                {message.timestamp?.toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}

        {/* Streaming Message */}
        {streamingMessage && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
              <p className="whitespace-pre-wrap">{streamingMessage}</p>
              <span className="animate-pulse">|</span>
            </div>
          </div>
        )}

        {/* Loading State */}
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
            placeholder={placeholder}
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

## AI-Powered Form Component

```tsx
// components/AIForm.tsx
'use client'

import { useState } from 'react'
import { generateObject } from 'ai'
import { openai } from '@ai-sdk/openai'
import { z } from 'zod'

interface AIFormProps {
  schema: z.ZodSchema
  onSubmit: (data: any) => void
  prompt: string
  className?: string
}

export function AIForm({ schema, onSubmit, prompt, className = '' }: AIFormProps) {
  const [formData, setFormData] = useState<any>({})
  const [isGenerating, setIsGenerating] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const handleGenerate = async () => {
    setIsGenerating(true)
    try {
      const { object } = await generateObject({
        model: openai('gpt-4'),
        schema,
        prompt,
      })
      setFormData(object)
      setErrors({})
    } catch (error) {
      console.error('Generation error:', error)
      setErrors({ general: 'Failed to generate form data' })
    } finally {
      setIsGenerating(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const renderField = (key: string, value: any, path: string[] = []) => {
    const fullPath = [...path, key].join('.')

    if (typeof value === 'string') {
      return (
        <div key={key} className="mb-4">
          <label className="block text-sm font-medium mb-2 capitalize">
            {key.replace(/([A-Z])/g, ' $1')}
          </label>
          <input
            type="text"
            value={value}
            onChange={(e) => {
              const newData = { ...formData }
              let current = newData
              for (let i = 0; i < path.length; i++) {
                current = current[path[i]]
              }
              current[key] = e.target.value
              setFormData(newData)
            }}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )
    }

    if (typeof value === 'number') {
      return (
        <div key={key} className="mb-4">
          <label className="block text-sm font-medium mb-2 capitalize">
            {key.replace(/([A-Z])/g, ' $1')}
          </label>
          <input
            type="number"
            value={value}
            onChange={(e) => {
              const newData = { ...formData }
              let current = newData
              for (let i = 0; i < path.length; i++) {
                current = current[path[i]]
              }
              current[key] = parseFloat(e.target.value)
              setFormData(newData)
            }}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )
    }

    if (Array.isArray(value)) {
      return (
        <div key={key} className="mb-4">
          <label className="block text-sm font-medium mb-2 capitalize">
            {key.replace(/([A-Z])/g, ' $1')}
          </label>
          <div className="space-y-2">
            {value.map((item, index) => (
              <div key={index} className="flex items-center space-x-2">
                <input
                  type="text"
                  value={item}
                  onChange={(e) => {
                    const newData = { ...formData }
                    let current = newData
                    for (let i = 0; i < path.length; i++) {
                      current = current[path[i]]
                    }
                    current[key][index] = e.target.value
                    setFormData(newData)
                  }}
                  className="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="button"
                  onClick={() => {
                    const newData = { ...formData }
                    let current = newData
                    for (let i = 0; i < path.length; i++) {
                      current = current[path[i]]
                    }
                    current[key].splice(index, 1)
                    setFormData(newData)
                  }}
                  className="px-2 py-1 text-red-600 hover:bg-red-50 rounded"
                >
                  ✕
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={() => {
                const newData = { ...formData }
                let current = newData
                for (let i = 0; i < path.length; i++) {
                  current = current[path[i]]
                }
                current[key].push('')
                setFormData(newData)
              }}
              className="px-3 py-1 text-blue-600 hover:bg-blue-50 rounded border"
            >
              + Add Item
            </button>
          </div>
        </div>
      )
    }

    if (typeof value === 'object' && value !== null) {
      return (
        <div key={key} className="mb-4 p-4 border rounded">
          <h3 className="font-medium mb-2 capitalize">
            {key.replace(/([A-Z])/g, ' $1')}
          </h3>
          <div className="pl-4">
            {Object.entries(value).map(([subKey, subValue]) =>
              renderField(subKey, subValue, [...path, key])
            )}
          </div>
        </div>
      )
    }

    return null
  }

  return (
    <div className={`max-w-2xl mx-auto ${className}`}>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">AI-Powered Form</h2>
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
          >
            {isGenerating ? 'Generating...' : 'Generate with AI'}
          </button>
        </div>

        {errors.general && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {Object.entries(formData).map(([key, value]) =>
            renderField(key, value)
          )}

          <div className="flex justify-end space-x-2 mt-6">
            <button
              type="button"
              onClick={() => setFormData({})}
              className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
            >
              Clear
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
```

## AI Content Editor Component

```tsx
// components/AIContentEditor.tsx
'use client'

import { useState, useCallback } from 'react'
import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'

interface AIContentEditorProps {
  initialContent?: string
  onContentChange?: (content: string) => void
  className?: string
}

export function AIContentEditor({
  initialContent = '',
  onContentChange,
  className = ''
}: AIContentEditorProps) {
  const [content, setContent] = useState(initialContent)
  const [isGenerating, setIsGenerating] = useState(false)
  const [selectedText, setSelectedText] = useState('')

  const handleContentChange = (newContent: string) => {
    setContent(newContent)
    onContentChange?.(newContent)
  }

  const handleTextSelection = () => {
    const selection = window.getSelection()
    if (selection) {
      setSelectedText(selection.toString())
    }
  }

  const aiActions = {
    improve: async () => {
      if (!selectedText) return
      setIsGenerating(true)
      try {
        const { text } = await generateText({
          model: openai('gpt-4'),
          prompt: `Improve this text while keeping the same meaning: "${selectedText}"`,
        })
        replaceSelectedText(text)
      } catch (error) {
        console.error('AI improvement error:', error)
      } finally {
        setIsGenerating(false)
      }
    },

    expand: async () => {
      if (!selectedText) return
      setIsGenerating(true)
      try {
        const { text } = await generateText({
          model: openai('gpt-4'),
          prompt: `Expand on this text with more details: "${selectedText}"`,
        })
        replaceSelectedText(text)
      } catch (error) {
        console.error('AI expansion error:', error)
      } finally {
        setIsGenerating(false)
      }
    },

    summarize: async () => {
      if (!selectedText) return
      setIsGenerating(true)
      try {
        const { text } = await generateText({
          model: openai('gpt-4'),
          prompt: `Summarize this text concisely: "${selectedText}"`,
        })
        replaceSelectedText(text)
      } catch (error) {
        console.error('AI summarization error:', error)
      } finally {
        setIsGenerating(false)
      }
    },

    translate: async (language: string) => {
      if (!selectedText) return
      setIsGenerating(true)
      try {
        const { text } = await generateText({
          model: openai('gpt-4'),
          prompt: `Translate this text to ${language}: "${selectedText}"`,
        })
        replaceSelectedText(text)
      } catch (error) {
        console.error('AI translation error:', error)
      } finally {
        setIsGenerating(false)
      }
    },
  }

  const replaceSelectedText = (newText: string) => {
    const textarea = document.getElementById('content-editor') as HTMLTextAreaElement
    const start = textarea.selectionStart
    const end = textarea.selectionEnd

    const newContent = content.substring(0, start) + newText + content.substring(end)
    handleContentChange(newContent)

    // Restore cursor position
    setTimeout(() => {
      textarea.selectionStart = textarea.selectionEnd = start + newText.length
      textarea.focus()
    }, 0)
  }

  return (
    <div className={`max-w-4xl mx-auto ${className}`}>
      <div className="bg-white rounded-lg shadow-lg">
        {/* Toolbar */}
        <div className="border-b p-4">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={aiActions.improve}
              disabled={!selectedText || isGenerating}
              className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
            >
              Improve
            </button>
            <button
              onClick={aiActions.expand}
              disabled={!selectedText || isGenerating}
              className="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
            >
              Expand
            </button>
            <button
              onClick={aiActions.summarize}
              disabled={!selectedText || isGenerating}
              className="px-3 py-1 text-sm bg-purple-500 text-white rounded hover:bg-purple-600 disabled:opacity-50"
            >
              Summarize
            </button>
            <button
              onClick={() => aiActions.translate('Spanish')}
              disabled={!selectedText || isGenerating}
              className="px-3 py-1 text-sm bg-orange-500 text-white rounded hover:bg-orange-600 disabled:opacity-50"
            >
              Translate to Spanish
            </button>
          </div>

          {selectedText && (
            <div className="mt-2 text-sm text-gray-600">
              Selected: "{selectedText.length > 50 ? selectedText.substring(0, 50) + '...' : selectedText}"
            </div>
          )}
        </div>

        {/* Editor */}
        <div className="p-4">
          <textarea
            id="content-editor"
            value={content}
            onChange={(e) => handleContentChange(e.target.value)}
            onSelect={handleTextSelection}
            placeholder="Start writing or paste your content here..."
            className="w-full h-64 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />

          {isGenerating && (
            <div className="mt-2 text-sm text-gray-600 flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-2"></div>
              AI is processing your text...
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="border-t px-4 py-2 text-sm text-gray-600">
          {content.split(' ').filter(word => word.length > 0).length} words |
          {content.length} characters
        </div>
      </div>
    </div>
  )
}
```

## AI Image Generator Component

```tsx
// components/AIImageGenerator.tsx
'use client'

import { useState } from 'react'
import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'

interface GeneratedImage {
  url: string
  prompt: string
  timestamp: Date
}

export function AIImageGenerator() {
  const [prompt, setPrompt] = useState('')
  const [images, setImages] = useState<GeneratedImage[]>([])
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setIsGenerating(true)
    try {
      // In a real implementation, you'd use DALL-E or another image generation API
      // For this example, we'll simulate image generation
      const enhancedPrompt = await enhancePrompt(prompt)

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 2000))

      const newImage: GeneratedImage = {
        url: `https://picsum.photos/400/300?random=${Date.now()}`, // Placeholder
        prompt: enhancedPrompt,
        timestamp: new Date(),
      }

      setImages(prev => [newImage, ...prev])
    } catch (error) {
      console.error('Image generation error:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const enhancePrompt = async (basePrompt: string): Promise<string> => {
    try {
      const { text } = await generateText({
        model: openai('gpt-4'),
        prompt: `Enhance this image generation prompt to be more descriptive and artistic: "${basePrompt}"`,
      })
      return text
    } catch {
      return basePrompt // Fallback to original prompt
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">AI Image Generator</h2>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the image you want to generate..."
            className="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
          />
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating}
            className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {isGenerating ? 'Generating...' : 'Generate'}
          </button>
        </div>
      </div>

      {/* Generated Images */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {images.map((image, index) => (
          <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
            <img
              src={image.url}
              alt={image.prompt}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <p className="text-sm text-gray-600 mb-2">{image.prompt}</p>
              <p className="text-xs text-gray-400">
                {image.timestamp.toLocaleString()}
              </p>
            </div>
          </div>
        ))}
      </div>

      {images.length === 0 && !isGenerating && (
        <div className="text-center text-gray-500 py-12">
          <div className="text-6xl mb-4">🎨</div>
          <p>Generate your first AI image above</p>
        </div>
      )}
    </div>
  )
}
```

## Custom Hook for AI State Management

```tsx
// hooks/useAI.ts
import { useState, useCallback } from 'react'
import { generateText, generateObject, streamText } from 'ai'
import { openai } from '@ai-sdk/openai'
import { z } from 'zod'

interface UseAIOptions {
  model?: string
  temperature?: number
  onError?: (error: Error) => void
}

export function useAI(options: UseAIOptions = {}) {
  const { model = 'gpt-4', temperature = 0.7, onError } = options
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const generateText = useCallback(async (
    prompt: string,
    genOptions?: { temperature?: number }
  ) => {
    setIsLoading(true)
    setError(null)

    try {
      const { text } = await generateText({
        model: openai(model),
        prompt,
        temperature: genOptions?.temperature || temperature,
      })

      return text
    } catch (err) {
      const error = err as Error
      setError(error)
      onError?.(error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [model, temperature, onError])

  const generateObject = useCallback(async <T>(
    schema: z.ZodSchema<T>,
    prompt: string,
    genOptions?: { temperature?: number }
  ): Promise<T> => {
    setIsLoading(true)
    setError(null)

    try {
      const { object } = await generateObject({
        model: openai(model),
        schema,
        prompt,
        temperature: genOptions?.temperature || temperature,
      })

      return object
    } catch (err) {
      const error = err as Error
      setError(error)
      onError?.(error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [model, temperature, onError])

  const streamText = useCallback(async (
    prompt: string,
    onChunk?: (chunk: string) => void,
    genOptions?: { temperature?: number }
  ) => {
    setIsLoading(true)
    setError(null)

    try {
      const result = await streamText({
        model: openai(model),
        prompt,
        temperature: genOptions?.temperature || temperature,
      })

      let fullText = ''
      for await (const delta of result.textStream) {
        fullText += delta
        onChunk?.(delta)
      }

      return fullText
    } catch (err) {
      const error = err as Error
      setError(error)
      onError?.(error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [model, temperature, onError])

  return {
    generateText,
    generateObject,
    streamText,
    isLoading,
    error,
  }
}
```

## What We've Accomplished

Amazing! 🎉 You've mastered React integration with Vercel AI:

1. **AI Chat Component** - Real-time streaming conversations
2. **AI Form Generator** - Dynamic forms with AI assistance
3. **AI Content Editor** - Smart text editing with AI actions
4. **AI Image Generator** - Creative image generation interface
5. **Custom AI Hook** - Reusable AI state management
6. **Component Composition** - Building complex AI-powered UIs
7. **Real-time Updates** - Streaming responses in React components
8. **Error Handling** - Robust error management in React

## Next Steps

Ready to build full-stack AI applications? In [Chapter 7: Next.js Applications](07-nextjs-applications.md), we'll create complete AI-powered Next.js applications with databases, authentication, and production deployment!

---

**Practice what you've learned:**
1. Build a custom AI component for your specific use case
2. Create a dashboard with multiple AI-powered widgets
3. Implement AI-powered search and filtering
4. Add voice input to your AI chat component
5. Create an AI-powered data visualization component

*What AI-powered React component will you build next?* ⚛️

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `className`, `text`, `error` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: React Integration` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `rounded`, `button`, `prompt` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: React Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `className`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
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
- search upstream code for `className` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Structured Outputs](05-structured-outputs.md)
- [Next Chapter: Chapter 7: Next.js Applications](07-nextjs-applications.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
