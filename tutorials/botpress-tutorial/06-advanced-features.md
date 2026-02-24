---
layout: default
title: "Chapter 6: Advanced Features"
parent: "Botpress Tutorial"
nav_order: 6
---

# Chapter 6: Advanced Features

Welcome to **Chapter 6: Advanced Features**. In this part of **Botpress Tutorial: Open Source Conversational AI Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explores advanced Botpress features including hooks, middleware, plugins, and custom integrations.

## 🎣 Hooks System

### Message Hooks

```typescript
// hooks/beforeIncomingMessage.ts
import { HookDefinition } from '@botpress/sdk'

export const beforeIncomingMessage: HookDefinition = {
  name: 'beforeIncomingMessage',
  description: 'Process messages before they reach the bot',
  handler: async ({ message, user, conversation }) => {
    // Log incoming message
    console.log(`Incoming: ${message.payload.text}`)

    // Add metadata
    message.metadata = {
      ...message.metadata,
      processedAt: new Date().toISOString(),
      channel: message.channel
    }

    // Content filtering
    if (containsProfanity(message.payload.text)) {
      message.payload.isFiltered = true
      message.payload.originalText = message.payload.text
      message.payload.text = '[Content filtered]'
    }

    return message
  }
}

// hooks/afterOutgoingMessage.ts
export const afterOutgoingMessage: HookDefinition = {
  name: 'afterOutgoingMessage',
  description: 'Process messages after bot sends them',
  handler: async ({ message, user, conversation }) => {
    // Analytics tracking
    await trackMessageAnalytics(message, user, conversation)

    // Message logging
    await logMessage(message)

    // Trigger notifications for urgent messages
    if (message.payload.text.includes('urgent')) {
      await sendUrgentNotification(message)
    }
  }
}
```

### State Hooks

```typescript
// hooks/beforeStateChanged.ts
export const beforeStateChanged: HookDefinition = {
  name: 'beforeStateChanged',
  description: 'Validate state changes',
  handler: async ({ newState, oldState, user }) => {
    // Validate state transition
    if (!isValidTransition(oldState, newState)) {
      throw new Error('Invalid state transition')
    }

    // Log state change
    await logStateChange(user.id, oldState, newState)

    return newState
  }
}
```

## 🔧 Middleware

### Custom Middleware

```typescript
// middleware/auth.ts
import { MiddlewareDefinition } from '@botpress/sdk'

export const authMiddleware: MiddlewareDefinition = {
  name: 'auth',
  description: 'Authentication middleware',
  handler: async (request, next) => {
    const token = request.headers.authorization

    if (!token) {
      throw new Error('No authentication token provided')
    }

    // Verify token
    const user = await verifyToken(token)

    // Add user to request context
    request.user = user

    return next(request)
  }
}

// middleware/rateLimit.ts
export const rateLimitMiddleware: MiddlewareDefinition = {
  name: 'rateLimit',
  description: 'Rate limiting middleware',
  handler: async (request, next) => {
    const clientId = request.user?.id || request.ip
    const isAllowed = await checkRateLimit(clientId)

    if (!isAllowed) {
      throw new Error('Rate limit exceeded')
    }

    return next(request)
  }
}
```

### Middleware Chain

```typescript
// Configure middleware chain
const middlewareChain = [
  authMiddleware,
  rateLimitMiddleware,
  loggingMiddleware,
  errorHandlingMiddleware
]

// Apply middleware
export const processWithMiddleware = async (request) => {
  let currentRequest = request

  for (const middleware of middlewareChain) {
    currentRequest = await middleware.handler(currentRequest, async (req) => req)
  }

  return currentRequest
}
```

## 🔌 Plugins System

### Creating Plugins

```typescript
// plugins/analytics.ts
import { PluginDefinition } from '@botpress/sdk'

export const analyticsPlugin: PluginDefinition = {
  name: 'analytics',
  version: '1.0.0',
  description: 'Analytics and tracking plugin',

  actions: {
    trackEvent: {
      name: 'trackEvent',
      handler: async ({ input }) => {
        const { event, properties } = input
        await analytics.track(event, properties)
      }
    }
  },

  hooks: {
    afterOutgoingMessage: {
      handler: async ({ message, user }) => {
        await analytics.track('message_sent', {
          userId: user.id,
          messageLength: message.payload.text.length,
          timestamp: new Date()
        })
      }
    }
  },

  channels: {
    custom: {
      name: 'Custom Analytics Channel',
      description: 'Send analytics data to custom endpoint',
      handler: async (data) => {
        await sendToAnalyticsEndpoint(data)
      }
    }
  }
}
```

### Plugin Configuration

```typescript
// Plugin configuration
const pluginConfig = {
  analytics: {
    enabled: true,
    apiKey: process.env.ANALYTICS_API_KEY,
    endpoint: 'https://analytics.example.com/track'
  },
  crm: {
    enabled: true,
    apiUrl: 'https://crm.example.com/api',
    apiKey: process.env.CRM_API_KEY
  }
}
```

## 🎯 Advanced NLU Features

### Custom NLU Pipeline

```typescript
// Custom NLU processing
const customNLUPipeline = {
  preprocess: (text) => {
    // Custom preprocessing
    return text.toLowerCase().trim()
  },

  extractFeatures: (text) => {
    // Extract custom features
    return {
      wordCount: text.split(' ').length,
      hasQuestionMark: text.includes('?'),
      sentiment: analyzeSentiment(text)
    }
  },

  classifyIntent: async (text, features) => {
    // Custom classification logic
    const model = await loadCustomModel()
    return model.predict(text, features)
  }
}
```

### Multi-Language Support

```typescript
// Multi-language NLU
const multiLanguageNLU = {
  detectLanguage: async (text) => {
    // Language detection
    return await languageDetector.detect(text)
  },

  routeToLanguageModel: (text, language) => {
    const models = {
      'en': englishModel,
      'fr': frenchModel,
      'es': spanishModel
    }

    return models[language] || models['en']
  },

  translateIfNeeded: async (text, targetLanguage) => {
    const detected = await languageDetector.detect(text)

    if (detected !== targetLanguage) {
      return await translator.translate(text, targetLanguage)
    }

    return text
  }
}
```

## 🚀 Performance Optimization

### Caching Strategy

```typescript
// Multi-level caching
class BotpressCache {
  constructor() {
    this.memoryCache = new Map()
    this.redisCache = redis.createClient()
    this.ttl = {
      short: 300,    // 5 minutes
      medium: 3600,  // 1 hour
      long: 86400    // 1 day
    }
  }

  async get(key, level = 'all') {
    // Try memory first
    if (level === 'memory' || level === 'all') {
      const memoryValue = this.memoryCache.get(key)
      if (memoryValue) return memoryValue
    }

    // Try Redis
    if (level === 'redis' || level === 'all') {
      const redisValue = await this.redisCache.get(key)
      if (redisValue) return JSON.parse(redisValue)
    }

    return null
  }

  async set(key, value, ttl = 'medium') {
    const expiry = this.ttl[ttl]

    // Set in memory
    this.memoryCache.set(key, value)

    // Set in Redis
    await this.redisCache.setex(key, expiry, JSON.stringify(value))
  }
}
```

### Connection Pooling

```typescript
// Database connection pooling
const createConnectionPool = (config) => {
  return new Pool({
    host: config.host,
    port: config.port,
    database: config.database,
    user: config.user,
    password: config.password,
    max: 20,        // Maximum connections
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000
  })
}

// API client pooling
const createAPIClientPool = (baseURL, poolSize = 10) => {
  const clients = []

  for (let i = 0; i < poolSize; i++) {
    clients.push(axios.create({ baseURL }))
  }

  return {
    getClient: () => clients[Math.floor(Math.random() * clients.length)],
    destroy: () => clients.forEach(client => client = null)
  }
}
```

## 🔒 Security Features

### Input Sanitization

```typescript
// Comprehensive input sanitization
const sanitizeInput = (input) => {
  const sanitized = {}

  for (const [key, value] of Object.entries(input)) {
    if (typeof value === 'string') {
      sanitized[key] = sanitizeString(value)
    } else if (typeof value === 'object') {
      sanitized[key] = sanitizeObject(value)
    } else {
      sanitized[key] = value
    }
  }

  return sanitized
}

const sanitizeString = (str) => {
  return str
    .replace(/[<>]/g, '') // Remove potential HTML
    .replace(/javascript:/gi, '') // Remove JS protocol
    .trim()
}
```

### Authentication & Authorization

```typescript
// JWT-based authentication
const authenticateUser = async (token) => {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    return await getUserById(decoded.userId)
  } catch (error) {
    throw new Error('Invalid authentication token')
  }
}

// Role-based authorization
const authorizeAction = (user, action, resource) => {
  const permissions = user.roles.flatMap(role => role.permissions)

  return permissions.some(permission =>
    permission.action === action && permission.resource === resource
  )
}
```

## 📊 Advanced Analytics

### Real-time Metrics

```typescript
// Real-time analytics collection
class RealTimeAnalytics {
  constructor() {
    this.metrics = {
      activeUsers: new Set(),
      messagesPerMinute: 0,
      averageResponseTime: 0,
      errorRate: 0
    }

    this.messageCount = 0
    this.startTime = Date.now()
  }

  trackMessage(message) {
    this.activeUsers.add(message.user.id)
    this.messageCount++

    // Calculate messages per minute
    const elapsedMinutes = (Date.now() - this.startTime) / 60000
    this.metrics.messagesPerMinute = this.messageCount / elapsedMinutes
  }

  getRealTimeMetrics() {
    return {
      ...this.metrics,
      activeUserCount: this.metrics.activeUsers.size
    }
  }
}
```

## 📝 Chapter Summary

- ✅ Implemented comprehensive hooks system
- ✅ Created custom middleware for processing
- ✅ Built plugins for extensibility
- ✅ Enhanced NLU with custom pipelines
- ✅ Optimized performance with caching
- ✅ Added security measures and sanitization
- ✅ Implemented real-time analytics

**Key Takeaways:**
- Hooks enable custom processing at key points
- Middleware provides cross-cutting concerns
- Plugins make the system extensible
- Custom NLU improves understanding
- Caching and pooling enhance performance
- Security measures protect the system
- Analytics provide insights for optimization

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `message`, `text`, `user` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Advanced Features` as an operating subsystem inside **Botpress Tutorial: Open Source Conversational AI Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `request`, `handler`, `name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Advanced Features` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `message`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `user`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [github.com/botpress/botpress](https://github.com/botpress/botpress)
  Why it matters: authoritative reference on `github.com/botpress/botpress` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `message` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Channel Integrations](05-channel-integrations.md)
- [Next Chapter: Chapter 7: Analytics & Monitoring](07-analytics-monitoring.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
