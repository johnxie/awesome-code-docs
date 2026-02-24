---
layout: default
title: "Chapter 3: AI Provider Integration"
parent: "Chatbox Tutorial"
nav_order: 3
---

# Chapter 3: AI Provider Integration

Welcome to **Chapter 3: AI Provider Integration**. In this part of **Chatbox Tutorial: Building Modern AI Chat Interfaces**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers integrating multiple AI providers and managing different language models in chat applications.

## 🤖 AI Provider Architecture

### Provider Management System

```typescript
// Multi-provider architecture
interface AIProvider {
  name: string
  models: AIModel[]
  authenticate(credentials: ProviderCredentials): Promise<boolean>
  sendMessage(message: ChatMessage, model: string): Promise<AIResponse>
  getModels(): Promise<AIModel[]>
  checkLimits(): Promise<UsageLimits>
}

class ProviderManager {
  private providers: Map<string, AIProvider> = new Map()
  private activeProvider: string | null = null

  registerProvider(provider: AIProvider) {
    this.providers.set(provider.name, provider)
  }

  async setActiveProvider(providerName: string, credentials: ProviderCredentials) {
    const provider = this.providers.get(providerName)
    if (!provider) {
      throw new Error(`Provider ${providerName} not found`)
    }

    const authenticated = await provider.authenticate(credentials)
    if (!authenticated) {
      throw new Error(`Authentication failed for ${providerName}`)
    }

    this.activeProvider = providerName
  }

  async sendMessage(message: ChatMessage, model?: string): Promise<AIResponse> {
    if (!this.activeProvider) {
      throw new Error('No active provider set')
    }

    const provider = this.providers.get(this.activeProvider)!
    const targetModel = model || provider.models[0].id

    return await provider.sendMessage(message, targetModel)
  }

  getAvailableProviders(): string[] {
    return Array.from(this.providers.keys())
  }

  getProviderModels(providerName: string): AIModel[] {
    const provider = this.providers.get(providerName)
    return provider ? provider.models : []
  }
}
```

## 🌐 Popular AI Providers

### OpenAI Integration

```typescript
// OpenAI provider implementation
class OpenAIProvider implements AIProvider {
  name = 'OpenAI'
  models = [
    { id: 'gpt-4', name: 'GPT-4', contextWindow: 8192 },
    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', contextWindow: 4096 },
    { id: 'gpt-3.5-turbo-16k', name: 'GPT-3.5 Turbo 16K', contextWindow: 16384 }
  ]

  private apiKey: string | null = null

  async authenticate(credentials: ProviderCredentials): Promise<boolean> {
    this.apiKey = credentials.apiKey
    try {
      // Test authentication with a simple request
      const response = await fetch('https://api.openai.com/v1/models', {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      })
      return response.ok
    } catch (error) {
      return false
    }
  }

  async sendMessage(message: ChatMessage, model: string): Promise<AIResponse> {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model,
        messages: [{
          role: 'user',
          content: message.content
        }],
        max_tokens: 1000,
        temperature: 0.7
      })
    })

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.statusText}`)
    }

    const data = await response.json()
    return {
      content: data.choices[0].message.content,
      usage: {
        promptTokens: data.usage.prompt_tokens,
        completionTokens: data.usage.completion_tokens,
        totalTokens: data.usage.total_tokens
      }
    }
  }

  async getModels(): Promise<AIModel[]> {
    const response = await fetch('https://api.openai.com/v1/models', {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()
    return data.data.map(model => ({
      id: model.id,
      name: model.id,
      contextWindow: this.getContextWindow(model.id)
    }))
  }

  private getContextWindow(modelId: string): number {
    const contextWindows = {
      'gpt-4': 8192,
      'gpt-4-32k': 32768,
      'gpt-3.5-turbo': 4096,
      'gpt-3.5-turbo-16k': 16384
    }
    return contextWindows[modelId] || 4096
  }
}
```

### Anthropic Claude Integration

```typescript
// Anthropic Claude provider
class ClaudeProvider implements AIProvider {
  name = 'Anthropic'
  models = [
    { id: 'claude-2', name: 'Claude 2', contextWindow: 100000 },
    { id: 'claude-instant-1', name: 'Claude Instant', contextWindow: 100000 }
  ]

  async sendMessage(message: ChatMessage, model: string): Promise<AIResponse> {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        model,
        max_tokens: 1000,
        messages: [{
          role: 'user',
          content: message.content
        }]
      })
    })

    const data = await response.json()
    return {
      content: data.content[0].text,
      usage: {
        promptTokens: data.usage.input_tokens,
        completionTokens: data.usage.output_tokens,
        totalTokens: data.usage.input_tokens + data.usage.output_tokens
      }
    }
  }
}
```

### Local Model Integration

```typescript
// Local model provider (Ollama, LM Studio, etc.)
class LocalProvider implements AIProvider {
  name = 'Local'
  models = []

  constructor(private baseUrl: string = 'http://localhost:11434') {}

  async sendMessage(message: ChatMessage, model: string): Promise<AIResponse> {
    const response = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model,
        prompt: message.content,
        stream: false
      })
    })

    const data = await response.json()
    return {
      content: data.response,
      usage: {
        promptTokens: this.estimateTokens(message.content),
        completionTokens: this.estimateTokens(data.response),
        totalTokens: this.estimateTokens(message.content + data.response)
      }
    }
  }

  async getModels(): Promise<AIModel[]> {
    const response = await fetch(`${this.baseUrl}/api/tags`)
    const data = await response.json()

    return data.models.map(model => ({
      id: model.name,
      name: model.name,
      contextWindow: 4096 // Default, can be model-specific
    }))
  }

  private estimateTokens(text: string): number {
    // Rough estimation: 1 token ≈ 4 characters
    return Math.ceil(text.length / 4)
  }
}
```

## 🔄 Provider Switching

### Dynamic Provider Selection

```typescript
// Intelligent provider switching
class SmartProviderSwitcher {
  private providers: Map<string, AIProvider> = new Map()
  private usageStats: Map<string, ProviderStats> = new Map()

  async selectProvider(message: ChatMessage, requirements: MessageRequirements): Promise<string> {
    const candidates = []

    for (const [name, provider] of this.providers) {
      const stats = this.usageStats.get(name) || { rateLimitRemaining: 100, avgResponseTime: 1000 }

      if (this.meetsRequirements(provider, requirements, stats)) {
        candidates.push({
          name,
          score: this.calculateProviderScore(provider, requirements, stats)
        })
      }
    }

    if (candidates.length === 0) {
      throw new Error('No suitable provider available')
    }

    // Return provider with highest score
    candidates.sort((a, b) => b.score - a.score)
    return candidates[0].name
  }

  private meetsRequirements(provider: AIProvider, requirements: MessageRequirements, stats: ProviderStats): boolean {
    // Check model capabilities
    const hasRequiredModel = requirements.preferredModel ?
      provider.models.some(m => m.id === requirements.preferredModel) :
      true

    // Check context window
    const hasContextWindow = requirements.maxTokens ?
      provider.models.some(m => m.contextWindow >= requirements.maxTokens) :
      true

    // Check rate limits
    const hasRateLimit = stats.rateLimitRemaining > 10

    return hasRequiredModel && hasContextWindow && hasRateLimit
  }

  private calculateProviderScore(provider: AIProvider, requirements: MessageRequirements, stats: ProviderStats): number {
    let score = 0

    // Prefer faster providers
    score += Math.max(0, 1000 - stats.avgResponseTime) / 100

    // Prefer providers with remaining rate limits
    score += stats.rateLimitRemaining / 10

    // Prefer providers with requested model
    if (requirements.preferredModel && provider.models.some(m => m.id === requirements.preferredModel)) {
      score += 50
    }

    return score
  }

  updateStats(providerName: string, responseTime: number, tokensUsed: number) {
    const stats = this.usageStats.get(providerName) || {
      rateLimitRemaining: 100,
      avgResponseTime: 1000,
      totalRequests: 0
    }

    stats.totalRequests++
    stats.avgResponseTime = (stats.avgResponseTime + responseTime) / 2
    stats.rateLimitRemaining = Math.max(0, stats.rateLimitRemaining - 1)

    this.usageStats.set(providerName, stats)
  }
}
```

## 📊 Usage Tracking & Billing

### Cost Management

```typescript
// Multi-provider cost tracking
class CostManager {
  private pricing: Map<string, ModelPricing> = new Map()
  private usage: Map<string, ProviderUsage> = new Map()

  constructor() {
    this.initializePricing()
  }

  private initializePricing() {
    // OpenAI pricing (per 1K tokens)
    this.pricing.set('openai', {
      'gpt-4': { input: 0.03, output: 0.06 },
      'gpt-3.5-turbo': { input: 0.0015, output: 0.002 }
    })

    // Anthropic pricing
    this.pricing.set('anthropic', {
      'claude-2': { input: 0.008, output: 0.024 },
      'claude-instant-1': { input: 0.00163, output: 0.00551 }
    })
  }

  trackUsage(provider: string, model: string, usage: TokenUsage) {
    const providerUsage = this.usage.get(provider) || {
      totalCost: 0,
      totalTokens: 0,
      modelUsage: new Map()
    }

    const pricing = this.pricing.get(provider)?.[model]
    if (pricing) {
      const cost = (usage.promptTokens * pricing.input + usage.completionTokens * pricing.output) / 1000
      providerUsage.totalCost += cost
    }

    providerUsage.totalTokens += usage.totalTokens

    const modelUsage = providerUsage.modelUsage.get(model) || { tokens: 0, cost: 0, requests: 0 }
    modelUsage.tokens += usage.totalTokens
    modelUsage.requests++
    providerUsage.modelUsage.set(model, modelUsage)

    this.usage.set(provider, providerUsage)
  }

  getTotalCost(): number {
    return Array.from(this.usage.values())
      .reduce((total, usage) => total + usage.totalCost, 0)
  }

  getProviderCosts(): Record<string, number> {
    const costs = {}
    for (const [provider, usage] of this.usage) {
      costs[provider] = usage.totalCost
    }
    return costs
  }
}
```

## ⚡ Performance Optimization

### Response Caching

```typescript
// Intelligent response caching
class ResponseCache {
  private cache: Map<string, CachedResponse> = new Map()
  private maxSize = 1000
  private ttl = 30 * 60 * 1000 // 30 minutes

  get(message: ChatMessage, model: string): CachedResponse | null {
    const key = this.generateKey(message, model)
    const cached = this.cache.get(key)

    if (!cached) return null

    if (Date.now() - cached.timestamp > this.ttl) {
      this.cache.delete(key)
      return null
    }

    return cached
  }

  set(message: ChatMessage, model: string, response: AIResponse) {
    const key = this.generateKey(message, model)

    if (this.cache.size >= this.maxSize) {
      // Remove oldest entry
      const oldestKey = Array.from(this.cache.entries())
        .sort((a, b) => a[1].timestamp - b[1].timestamp)[0][0]
      this.cache.delete(oldestKey)
    }

    this.cache.set(key, {
      response,
      timestamp: Date.now(),
      hits: 0
    })
  }

  private generateKey(message: ChatMessage, model: string): string {
    // Create deterministic key from message content
    const content = message.content.toLowerCase().trim()
    return `${model}:${this.hashString(content)}`
  }

  private hashString(str: string): string {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash
    }
    return hash.toString()
  }
}
```

## 🔧 Fallback Strategies

### Provider Failover

```typescript
// Automatic provider failover
class ProviderFailover {
  private providers: string[] = []
  private currentIndex = 0
  private failures: Map<string, number> = new Map()

  constructor(providers: string[]) {
    this.providers = [...providers]
  }

  async sendWithFailover(message: ChatMessage, primaryProvider: string): Promise<AIResponse> {
    const triedProviders = new Set()

    // Try primary provider first
    try {
      return await this.tryProvider(primaryProvider, message)
    } catch (error) {
      triedProviders.add(primaryProvider)
      this.recordFailure(primaryProvider)
    }

    // Try other providers in order
    for (const provider of this.providers) {
      if (triedProviders.has(provider)) continue

      try {
        return await this.tryProvider(provider, message)
      } catch (error) {
        triedProviders.add(provider)
        this.recordFailure(provider)
      }
    }

    throw new Error('All providers failed')
  }

  private async tryProvider(provider: string, message: ChatMessage): Promise<AIResponse> {
    const providerInstance = this.getProviderInstance(provider)
    return await providerInstance.sendMessage(message)
  }

  private recordFailure(provider: string) {
    const failures = this.failures.get(provider) || 0
    this.failures.set(provider, failures + 1)
  }

  getHealthyProviders(): string[] {
    return this.providers.filter(provider => {
      const failures = this.failures.get(provider) || 0
      return failures < 3 // Allow up to 2 failures
    })
  }
}
```

## 📝 Chapter Summary

- ✅ Built multi-provider architecture
- ✅ Integrated OpenAI, Anthropic, and local models
- ✅ Implemented intelligent provider switching
- ✅ Added cost tracking and management
- ✅ Created response caching system
- ✅ Built provider failover mechanisms

**Key Takeaways:**
- Multiple providers ensure reliability
- Cost tracking prevents budget overruns
- Intelligent switching optimizes performance
- Caching reduces API calls and costs
- Failover ensures continuous operation
- Usage analytics inform provider selection

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `provider`, `model`, `message` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: AI Provider Integration` as an operating subsystem inside **Chatbox Tutorial: Building Modern AI Chat Interfaces**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `usage`, `response`, `providers` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: AI Provider Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `provider`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `message`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/Bin-Huang/chatbox)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `provider` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: UI Architecture & Components](02-ui-architecture.md)
- [Next Chapter: Chapter 4: Conversation Management](04-conversation-management.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
