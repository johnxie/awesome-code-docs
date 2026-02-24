---
layout: default
title: "Chapter 5: Structured Outputs"
parent: "Vercel AI Tutorial"
nav_order: 5
---

# Chapter 5: Structured Outputs

Welcome to the world of predictable AI! Structured outputs are the secret sauce that transforms AI from a creative storyteller into a reliable data generator. Instead of getting free-form text that you have to parse, you get perfectly formatted, type-safe data structures.

## Why Structured Outputs Matter

Imagine building:
- **API endpoints** that return consistent JSON
- **Data processing pipelines** with predictable formats
- **Forms and interfaces** auto-generated from AI responses
- **Database records** created directly from AI output

Structured outputs eliminate parsing errors and make AI responses machine-readable.

## Basic Structured Output with Zod

Vercel AI uses Zod for schema validation:

```typescript
// app/api/structured-chat/route.ts
import { openai } from '@ai-sdk/openai'
import { generateObject } from 'ai'
import { z } from 'zod'

// Define the output schema
const recipeSchema = z.object({
  name: z.string().describe('The name of the recipe'),
  ingredients: z.array(z.object({
    name: z.string(),
    amount: z.string(),
    unit: z.string().optional(),
  })).describe('List of ingredients with amounts'),
  instructions: z.array(z.string()).describe('Step-by-step cooking instructions'),
  prepTime: z.number().describe('Preparation time in minutes'),
  cookTime: z.number().describe('Cooking time in minutes'),
  servings: z.number().describe('Number of servings'),
  difficulty: z.enum(['easy', 'medium', 'hard']).describe('Recipe difficulty level'),
})

export async function POST(req: Request) {
  const { prompt } = await req.json()

  try {
    const { object } = await generateObject({
      model: openai('gpt-4'),
      schema: recipeSchema,
      prompt: `Generate a recipe for: ${prompt}`,
    })

    return Response.json({ success: true, recipe: object })
  } catch (error) {
    return Response.json(
      { success: false, error: error.message },
      { status: 500 }
    )
  }
}
```

## Creating Different Output Schemas

Let's build a variety of structured output examples:

```typescript
// schemas/index.ts
import { z } from 'zod'

// Product schema
export const productSchema = z.object({
  name: z.string(),
  description: z.string(),
  price: z.number(),
  category: z.string(),
  tags: z.array(z.string()),
  specifications: z.record(z.string(), z.string()),
  availability: z.boolean(),
})

// Task management schema
export const taskSchema = z.object({
  title: z.string(),
  description: z.string(),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  dueDate: z.string().datetime().optional(),
  assignee: z.string().optional(),
  tags: z.array(z.string()),
  subtasks: z.array(z.object({
    title: z.string(),
    completed: z.boolean(),
  })),
})

// Code analysis schema
export const codeAnalysisSchema = z.object({
  language: z.string(),
  complexity: z.enum(['low', 'medium', 'high']),
  functions: z.array(z.object({
    name: z.string(),
    parameters: z.array(z.string()),
    returnType: z.string(),
    lines: z.number(),
  })),
  issues: z.array(z.object({
    type: z.enum(['error', 'warning', 'info']),
    message: z.string(),
    line: z.number().optional(),
    suggestion: z.string().optional(),
  })),
  suggestions: z.array(z.string()),
})

// API response schema
export const apiResponseSchema = z.object({
  status: z.enum(['success', 'error', 'partial']),
  data: z.any(),
  message: z.string().optional(),
  timestamp: z.string().datetime(),
  requestId: z.string(),
  pagination: z.object({
    page: z.number(),
    limit: z.number(),
    total: z.number(),
    hasNext: z.boolean(),
  }).optional(),
})
```

## Building a Schema Generator

```typescript
// lib/schema-generator.ts
import { z } from 'zod'

export class SchemaGenerator {
  static createProductSchema(customFields: Record<string, any> = {}) {
    return z.object({
      name: z.string(),
      description: z.string(),
      price: z.number(),
      category: z.string(),
      ...customFields,
    })
  }

  static createListSchema(itemSchema: z.ZodType, options: {
    minItems?: number
    maxItems?: number
  } = {}) {
    let listSchema = z.array(itemSchema)

    if (options.minItems) {
      listSchema = listSchema.min(options.minItems)
    }

    if (options.maxItems) {
      listSchema = listSchema.max(options.maxItems)
    }

    return listSchema
  }

  static createEnumSchema(values: string[]) {
    return z.enum(values as [string, ...string[]])
  }

  static createRecordSchema(keySchema: z.ZodType, valueSchema: z.ZodType) {
    return z.record(keySchema, valueSchema)
  }
}

// Usage examples
const customProductSchema = SchemaGenerator.createProductSchema({
  warranty: z.string().optional(),
  color: z.string(),
})

const tagListSchema = SchemaGenerator.createListSchema(
  z.string(),
  { minItems: 1, maxItems: 10 }
)

const configSchema = SchemaGenerator.createRecordSchema(
  z.string(),
  z.union([z.string(), z.number(), z.boolean()])
)
```

## Structured Output API Routes

Let's create a comprehensive API with multiple structured outputs:

```typescript
// app/api/structured/[type]/route.ts
import { openai } from '@ai-sdk/openai'
import { generateObject } from 'ai'
import { z } from 'zod'
import {
  productSchema,
  taskSchema,
  codeAnalysisSchema,
  apiResponseSchema
} from '@/schemas'

const schemas = {
  product: productSchema,
  task: taskSchema,
  codeAnalysis: codeAnalysisSchema,
}

export async function POST(
  req: Request,
  { params }: { params: { type: string } }
) {
  const { prompt, options = {} } = await req.json()
  const schemaType = params.type as keyof typeof schemas

  if (!schemas[schemaType]) {
    return Response.json(
      { error: 'Invalid schema type' },
      { status: 400 }
    )
  }

  try {
    const schema = schemas[schemaType]
    const enhancedPrompt = enhancePromptWithSchema(prompt, schema, options)

    const { object } = await generateObject({
      model: openai('gpt-4'),
      schema,
      prompt: enhancedPrompt,
      temperature: options.temperature || 0.1, // Lower temperature for structured output
    })

    const response = apiResponseSchema.parse({
      status: 'success',
      data: object,
      timestamp: new Date().toISOString(),
      requestId: generateRequestId(),
    })

    return Response.json(response)
  } catch (error) {
    const errorResponse = apiResponseSchema.parse({
      status: 'error',
      data: null,
      message: error.message,
      timestamp: new Date().toISOString(),
      requestId: generateRequestId(),
    })

    return Response.json(errorResponse, { status: 500 })
  }
}

function enhancePromptWithSchema(prompt: string, schema: z.ZodType, options: any): string {
  const schemaDescription = generateSchemaDescription(schema)

  return `
${prompt}

Please provide the response in the following structure:
${schemaDescription}

Ensure the response matches this exact structure and data types.
${options.strict ? 'Be extremely precise with the format.' : ''}
  `.trim()
}

function generateSchemaDescription(schema: z.ZodType): string {
  // This would generate a human-readable description of the schema
  // For simplicity, we'll return a basic description
  return 'Structured JSON response matching the specified schema'
}

function generateRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}
```

## Building a Structured Output UI

```tsx
// components/StructuredGenerator.tsx
'use client'

import { useState } from 'react'
import { z } from 'zod'

// Define available schemas
const availableSchemas = {
  product: 'Product Description',
  task: 'Task Management',
  codeAnalysis: 'Code Analysis',
}

type SchemaType = keyof typeof availableSchemas

interface GeneratedData {
  [key: string]: any
}

export function StructuredGenerator() {
  const [selectedSchema, setSelectedSchema] = useState<SchemaType>('product')
  const [prompt, setPrompt] = useState('')
  const [result, setResult] = useState<GeneratedData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`/api/structured/${selectedSchema}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      })

      const data = await response.json()

      if (data.status === 'success') {
        setResult(data.data)
      } else {
        setError(data.message || 'Generation failed')
      }
    } catch (err) {
      setError('Network error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Structured Output Generator</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Output Type
            </label>
            <select
              value={selectedSchema}
              onChange={(e) => setSelectedSchema(e.target.value as SchemaType)}
              className="w-full p-2 border rounded"
            >
              {Object.entries(availableSchemas).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Prompt
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={`Describe what you want to generate as a ${availableSchemas[selectedSchema].toLowerCase()}...`}
              className="w-full h-32 p-2 border rounded"
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !prompt.trim()}
            className="w-full px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Generate Structured Output'}
          </button>
        </div>

        {/* Output Panel */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Generated Result
          </label>
          <div className="h-64 p-4 border rounded bg-gray-50 overflow-auto">
            {error && (
              <div className="text-red-600">
                <strong>Error:</strong> {error}
              </div>
            )}

            {result && !error && (
              <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                {JSON.stringify(result, null, 2)}
              </pre>
            )}

            {!result && !error && !loading && (
              <div className="text-gray-500 italic">
                Your structured output will appear here...
              </div>
            )}

            {loading && (
              <div className="text-gray-500 italic">
                Generating structured output...
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Schema Preview */}
      <div className="mt-6">
        <details className="bg-gray-50 p-4 rounded">
          <summary className="font-medium cursor-pointer">
            Schema Preview for {availableSchemas[selectedSchema]}
          </summary>
          <pre className="mt-2 text-sm text-gray-700">
            {getSchemaPreview(selectedSchema)}
          </pre>
        </details>
      </div>
    </div>
  )
}

function getSchemaPreview(schemaType: SchemaType): string {
  const previews = {
    product: `{
  "name": "string",
  "description": "string",
  "price": "number",
  "category": "string",
  "tags": ["string"],
  "specifications": {"key": "value"},
  "availability": "boolean"
}`,
    task: `{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high|urgent",
  "dueDate": "ISO datetime (optional)",
  "assignee": "string (optional)",
  "tags": ["string"],
  "subtasks": [{"title": "string", "completed": "boolean"}]
}`,
    codeAnalysis: `{
  "language": "string",
  "complexity": "low|medium|high",
  "functions": [{"name": "string", "parameters": ["string"], "returnType": "string", "lines": "number"}],
  "issues": [{"type": "error|warning|info", "message": "string", "line": "number", "suggestion": "string"}],
  "suggestions": ["string"]
}`,
  }

  return previews[schemaType]
}
```

## Advanced Structured Output Patterns

### Conditional Schemas

```typescript
// schemas/conditional.ts
import { z } from 'zod'

export const conditionalProductSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('physical'),
    name: z.string(),
    weight: z.number(),
    dimensions: z.object({
      length: z.number(),
      width: z.number(),
      height: z.number(),
    }),
  }),
  z.object({
    type: z.literal('digital'),
    name: z.string(),
    fileSize: z.number(),
    downloadUrl: z.string().url(),
    format: z.string(),
  }),
])

// Usage
const physicalProduct = {
  type: 'physical',
  name: 'Laptop',
  weight: 2.5,
  dimensions: { length: 35, width: 25, height: 2 },
}

const digitalProduct = {
  type: 'digital',
  name: 'E-book',
  fileSize: 5.2,
  downloadUrl: 'https://example.com/book.pdf',
  format: 'PDF',
}
```

### Nested and Complex Schemas

```typescript
// schemas/complex.ts
import { z } from 'zod'

export const organizationSchema = z.object({
  name: z.string(),
  founded: z.string().datetime(),
  employees: z.array(z.object({
    id: z.string(),
    name: z.string(),
    role: z.string(),
    department: z.string(),
    salary: z.number(),
    skills: z.array(z.string()),
    manager: z.string().optional(),
  })),
  departments: z.array(z.object({
    name: z.string(),
    head: z.string(),
    budget: z.number(),
    projects: z.array(z.object({
      name: z.string(),
      status: z.enum(['planning', 'active', 'completed', 'on-hold']),
      deadline: z.string().datetime().optional(),
      team: z.array(z.string()),
      budget: z.number(),
    })),
  })),
  metrics: z.object({
    revenue: z.number(),
    growth: z.number(),
    satisfaction: z.number(),
    retention: z.number(),
  }),
})
```

## Error Handling and Validation

```typescript
// utils/structured-validation.ts
import { z } from 'zod'

export class StructuredOutputError extends Error {
  constructor(
    message: string,
    public schema: string,
    public input: any,
    public validationErrors: z.ZodError | null = null
  ) {
    super(message)
    this.name = 'StructuredOutputError'
  }
}

export function validateStructuredOutput<T>(
  schema: z.ZodSchema<T>,
  data: any,
  schemaName: string
): T {
  try {
    return schema.parse(data)
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new StructuredOutputError(
        `Validation failed for ${schemaName}`,
        schemaName,
        data,
        error
      )
    }
    throw new StructuredOutputError(
      `Unexpected error validating ${schemaName}`,
      schemaName,
      data
    )
  }
}

export function getValidationErrors(error: StructuredOutputError): string[] {
  if (!error.validationErrors) return []

  return error.validationErrors.errors.map(err =>
    `${err.path.join('.')}: ${err.message}`
  )
}
```

## Real-World Example: API Documentation Generator

```typescript
// app/api/generate-docs/route.ts
import { openai } from '@ai-sdk/openai'
import { generateObject } from 'ai'
import { z } from 'zod'

const apiDocsSchema = z.object({
  title: z.string(),
  description: z.string(),
  version: z.string(),
  endpoints: z.array(z.object({
    path: z.string(),
    method: z.enum(['GET', 'POST', 'PUT', 'DELETE', 'PATCH']),
    description: z.string(),
    parameters: z.array(z.object({
      name: z.string(),
      type: z.string(),
      required: z.boolean(),
      description: z.string(),
    })),
    requestBody: z.object({
      type: z.string(),
      schema: z.any(),
    }).optional(),
    responses: z.record(z.string(), z.object({
      description: z.string(),
      schema: z.any(),
    })),
  })),
  authentication: z.object({
    type: z.string(),
    description: z.string(),
  }),
})

export async function POST(req: Request) {
  const { apiDescription } = await req.json()

  const { object } = await generateObject({
    model: openai('gpt-4'),
    schema: apiDocsSchema,
    prompt: `Generate comprehensive API documentation for: ${apiDescription}`,
  })

  return Response.json(object)
}
```

## What We've Accomplished

Fantastic! 🎉 You've mastered structured outputs:

1. **Schema definition** with Zod for type-safe validation
2. **Basic structured generation** with `generateObject`
3. **Multiple schema types** for different use cases
4. **Schema generators** for dynamic schema creation
5. **API routes** with proper error handling
6. **Interactive UI** for structured output generation
7. **Advanced patterns** like conditional and nested schemas
8. **Validation and error handling** for robust applications
9. **Real-world examples** like API documentation generation

## Next Steps

Ready to integrate AI into React applications? In [Chapter 6: React Integration](06-react-integration.md), we'll explore building interactive AI-powered React components!

---

**Practice what you've learned:**
1. Create a custom schema for your specific use case
2. Build a schema validation dashboard
3. Implement schema versioning and migration
4. Create a schema marketplace for sharing reusable schemas
5. Add schema auto-completion and suggestions

*What structured data will you generate with AI?* 📊

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `object`, `error`, `schema` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Structured Outputs` as an operating subsystem inside **Vercel AI SDK Tutorial: Production TypeScript AI Apps and Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `className`, `name`, `array` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Structured Outputs` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `object`.
2. **Input normalization**: shape incoming data so `error` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `schema`.
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
- search upstream code for `object` and `error` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Function Calling](04-function-calling.md)
- [Next Chapter: Chapter 6: React Integration](06-react-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
