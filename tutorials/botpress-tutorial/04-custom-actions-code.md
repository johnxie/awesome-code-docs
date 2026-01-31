---
layout: default
title: "Chapter 4: Custom Actions & Code"
parent: "Botpress Tutorial"
nav_order: 4
---

# Chapter 4: Custom Actions & Code

This chapter teaches you how to extend Botpress functionality with custom actions, JavaScript/TypeScript code, and external API integrations.

## 🎯 Custom Actions

### Creating Actions

```typescript
// actions/greeting.ts
import { ActionDefinition, ActionContext } from '@botpress/sdk'

export const greeting: ActionDefinition = {
  name: 'greeting',
  description: 'Generate personalized greeting',
  input: {
    schema: {
      type: 'object',
      properties: {
        name: { type: 'string' },
        timeOfDay: { type: 'string', enum: ['morning', 'afternoon', 'evening'] }
      },
      required: ['name']
    }
  },
  output: {
    schema: {
      type: 'object',
      properties: {
        message: { type: 'string' }
      }
    }
  },
  handler: async (context: ActionContext) => {
    const { name, timeOfDay = 'morning' } = context.input

    const greetings = {
      morning: 'Good morning',
      afternoon: 'Good afternoon',
      evening: 'Good evening'
    }

    const message = `${greetings[timeOfDay]} ${name}! How can I help you today?`

    return { message }
  }
}
```

### Using Actions in Flows

```typescript
// In your flow configuration
{
  type: "action",
  action: "greeting",
  args: {
    name: "{{user.firstName}}",
    timeOfDay: "morning"
  },
  output: {
    greetingMessage: "{{action.message}}"
  }
}
```

## 🔧 JavaScript/TypeScript Integration

### Basic Code Actions

```typescript
// actions/calculate.ts
export const calculate: ActionDefinition = {
  name: 'calculate',
  input: {
    schema: {
      type: 'object',
      properties: {
        operation: { type: 'string', enum: ['add', 'subtract', 'multiply', 'divide'] },
        a: { type: 'number' },
        b: { type: 'number' }
      },
      required: ['operation', 'a', 'b']
    }
  },
  output: {
    schema: {
      type: 'object',
      properties: {
        result: { type: 'number' }
      }
    }
  },
  handler: async ({ input }) => {
    const { operation, a, b } = input
    let result: number

    switch (operation) {
      case 'add':
        result = a + b
        break
      case 'subtract':
        result = a - b
        break
      case 'multiply':
        result = a * b
        break
      case 'divide':
        result = a / b
        break
      default:
        throw new Error('Invalid operation')
    }

    return { result }
  }
}
```

### Advanced Code Features

```typescript
// actions/weather.ts
import axios from 'axios'

export const getWeather: ActionDefinition = {
  name: 'getWeather',
  input: {
    schema: {
      type: 'object',
      properties: {
        city: { type: 'string' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'], default: 'celsius' }
      },
      required: ['city']
    }
  },
  output: {
    schema: {
      type: 'object',
      properties: {
        temperature: { type: 'number' },
        condition: { type: 'string' },
        city: { type: 'string' }
      }
    }
  },
  handler: async ({ input }) => {
    try {
      const { city, unit = 'celsius' } = input
      const apiKey = process.env.WEATHER_API_KEY

      const response = await axios.get(
        `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=${unit === 'celsius' ? 'metric' : 'imperial'}`
      )

      const { main, weather } = response.data

      return {
        temperature: main.temp,
        condition: weather[0].description,
        city: response.data.name
      }
    } catch (error) {
      throw new Error(`Weather API error: ${error.message}`)
    }
  }
}
```

## 🌐 External API Integration

### REST API Calls

```typescript
// actions/apiCall.ts
import axios from 'axios'

export const apiCall: ActionDefinition = {
  name: 'apiCall',
  input: {
    schema: {
      type: 'object',
      properties: {
        url: { type: 'string' },
        method: { type: 'string', enum: ['GET', 'POST', 'PUT', 'DELETE'], default: 'GET' },
        headers: { type: 'object' },
        body: { type: 'object' }
      },
      required: ['url']
    }
  },
  output: {
    schema: {
      type: 'object',
      properties: {
        status: { type: 'number' },
        data: { type: 'object' },
        headers: { type: 'object' }
      }
    }
  },
  handler: async ({ input }) => {
    const { url, method = 'GET', headers = {}, body } = input

    try {
      const response = await axios({
        method,
        url,
        headers,
        data: body
      })

      return {
        status: response.status,
        data: response.data,
        headers: response.headers
      }
    } catch (error) {
      return {
        status: error.response?.status || 500,
        data: { error: error.message },
        headers: {}
      }
    }
  }
}
```

### Database Integration

```typescript
// actions/database.ts
import { Client } from 'pg'

export const queryDatabase: ActionDefinition = {
  name: 'queryDatabase',
  input: {
    schema: {
      type: 'object',
      properties: {
        query: { type: 'string' },
        params: { type: 'array' }
      },
      required: ['query']
    }
  },
  output: {
    schema: {
      type: 'object',
      properties: {
        rows: { type: 'array' },
        rowCount: { type: 'number' }
      }
    }
  },
  handler: async ({ input }) => {
    const client = new Client({
      connectionString: process.env.DATABASE_URL
    })

    try {
      await client.connect()
      const result = await client.query(input.query, input.params || [])

      return {
        rows: result.rows,
        rowCount: result.rowCount
      }
    } finally {
      await client.end()
    }
  }
}
```

## 🔄 Middleware and Hooks

### Before Message Hooks

```typescript
// hooks/beforeMessage.ts
import { HookDefinition } from '@botpress/sdk'

export const beforeMessage: HookDefinition = {
  name: 'beforeMessage',
  description: 'Process message before bot handles it',
  handler: async ({ message, user, conversation }) => {
    // Log message
    console.log(`Message from ${user.id}: ${message.payload.text}`)

    // Add timestamp
    message.payload.timestamp = new Date().toISOString()

    // Check for spam
    if (isSpam(message.payload.text)) {
      message.payload.isSpam = true
    }

    return message
  }
}

function isSpam(text: string): boolean {
  const spamPatterns = [
    /free money/i,
    /click here/i,
    /urgent/i
  ]

  return spamPatterns.some(pattern => pattern.test(text))
}
```

### After Message Hooks

```typescript
// hooks/afterMessage.ts
export const afterMessage: HookDefinition = {
  name: 'afterMessage',
  description: 'Process after bot sends message',
  handler: async ({ message, user, conversation }) => {
    // Analytics tracking
    await trackMessage(user.id, message.payload.text)

    // Auto-save conversation
    await saveConversation(conversation.id, message)

    // Trigger notifications if needed
    if (message.payload.text.includes('urgent')) {
      await sendNotification(user.id, 'Urgent message sent')
    }
  }
}
```

## 🎨 Advanced Custom Features

### Custom Components

```typescript
// components/CustomCard.tsx
import React from 'react'

interface CustomCardProps {
  title: string
  description: string
  imageUrl?: string
  buttons: Array<{ title: string; payload: string }>
}

export const CustomCard: React.FC<CustomCardProps> = ({
  title,
  description,
  imageUrl,
  buttons
}) => {
  return (
    <div className="custom-card">
      {imageUrl && <img src={imageUrl} alt={title} />}
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="buttons">
        {buttons.map((button, index) => (
          <button key={index} onClick={() => sendPayload(button.payload)}>
            {button.title}
          </button>
        ))}
      </div>
    </div>
  )
}
```

### File Upload Handling

```typescript
// actions/handleFile.ts
export const handleFile: ActionDefinition = {
  name: 'handleFile',
  input: {
    schema: {
      type: 'object',
      properties: {
        file: { type: 'object' },
        allowedTypes: { type: 'array', items: { type: 'string' } }
      },
      required: ['file']
    }
  },
  output: {
    schema: {
      type: 'object',
      properties: {
        fileUrl: { type: 'string' },
        fileType: { type: 'string' },
        fileSize: { type: 'number' }
      }
    }
  },
  handler: async ({ input }) => {
    const { file, allowedTypes = [] } = input

    // Validate file type
    if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
      throw new Error(`File type ${file.type} not allowed`)
    }

    // Upload file
    const fileUrl = await uploadToStorage(file)

    return {
      fileUrl,
      fileType: file.type,
      fileSize: file.size
    }
  }
}
```

## 🧪 Testing Custom Code

### Unit Tests

```typescript
// __tests__/actions/calculate.test.ts
import { calculate } from '../actions/calculate'

describe('Calculate Action', () => {
  test('adds two numbers', async () => {
    const result = await calculate.handler({
      input: { operation: 'add', a: 5, b: 3 }
    })

    expect(result.result).toBe(8)
  })

  test('handles division by zero', async () => {
    await expect(
      calculate.handler({
        input: { operation: 'divide', a: 10, b: 0 }
      })
    ).rejects.toThrow('Division by zero')
  })
})
```

### Integration Tests

```typescript
// __tests__/integration/weather.test.ts
import { getWeather } from '../actions/weather'

describe('Weather Integration', () => {
  test('fetches weather data', async () => {
    const result = await getWeather.handler({
      input: { city: 'London' }
    })

    expect(result).toHaveProperty('temperature')
    expect(result).toHaveProperty('condition')
    expect(result.city.toLowerCase()).toBe('london')
  })
})
```

## 🚀 Performance Optimization

### Caching

```typescript
// actions/cachedApi.ts
import NodeCache from 'node-cache'

const cache = new NodeCache({ stdTTL: 300 }) // 5 minutes

export const cachedApiCall: ActionDefinition = {
  name: 'cachedApiCall',
  handler: async ({ input }) => {
    const cacheKey = JSON.stringify(input)
    const cached = cache.get(cacheKey)

    if (cached) {
      return cached
    }

    const result = await makeApiCall(input)
    cache.set(cacheKey, result)

    return result
  }
}
```

### Async Processing

```typescript
// actions/asyncProcess.ts
export const asyncProcess: ActionDefinition = {
  name: 'asyncProcess',
  handler: async ({ input }) => {
    // Start async process
    const jobId = await queueProcess(input)

    // Return immediately with job ID
    return {
      jobId,
      status: 'processing',
      message: 'Your request is being processed'
    }
  }
}

// Check status later
export const checkProcessStatus: ActionDefinition = {
  name: 'checkProcessStatus',
  handler: async ({ input: { jobId } }) => {
    const status = await getJobStatus(jobId)
    return status
  }
}
```

## 🔒 Security Best Practices

### Input Validation

```typescript
// actions/secureAction.ts
import validator from 'validator'

export const secureAction: ActionDefinition = {
  name: 'secureAction',
  handler: async ({ input }) => {
    const { email, url } = input

    // Validate email
    if (!validator.isEmail(email)) {
      throw new Error('Invalid email format')
    }

    // Sanitize URL
    const safeUrl = validator.escape(url)

    return { email, safeUrl }
  }
}
```

### Rate Limiting

```typescript
// middleware/rateLimit.ts
import rateLimit from 'express-rate-limit'

export const createRateLimit = (windowMs: number, max: number) => {
  return rateLimit({
    windowMs,
    max,
    message: 'Too many requests from this IP',
    standardHeaders: true,
    legacyHeaders: false
  })
}
```

## 📝 Chapter Summary

- ✅ Created custom actions with TypeScript
- ✅ Integrated external APIs and databases
- ✅ Implemented middleware and hooks
- ✅ Built custom UI components
- ✅ Added comprehensive testing
- ✅ Optimized performance with caching
- ✅ Applied security best practices

**Key Takeaways:**
- Custom actions extend Botpress functionality
- TypeScript provides type safety and better IDE support
- External integrations enable complex workflows
- Hooks allow preprocessing and postprocessing
- Testing ensures code reliability
- Caching improves performance
- Security validation protects against attacks
