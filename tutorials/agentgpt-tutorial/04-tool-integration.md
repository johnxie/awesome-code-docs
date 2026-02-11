---
layout: default
title: "Chapter 4: Tool Integration & APIs"
parent: "AgentGPT Tutorial"
nav_order: 4
---

# Chapter 4: Tool Integration & APIs

This chapter covers how AgentGPT agents integrate with external tools and APIs to extend their capabilities and perform real-world actions.

## 🔧 Tool Integration Fundamentals

### Tool Definition Structure

```typescript
// Define a tool for agent use
interface Tool {
  name: string
  description: string
  parameters: Parameter[]
  execute: (params: any) => Promise<any>
  validate?: (params: any) => boolean
  cost?: number
  rateLimit?: RateLimit
}

interface Parameter {
  name: string
  type: 'string' | 'number' | 'boolean' | 'array' | 'object'
  description: string
  required: boolean
  default?: any
}
```

### Tool Registry

```typescript
// Registry for managing available tools
class ToolRegistry {
  private tools = new Map<string, Tool>()

  register(tool: Tool) {
    this.tools.set(tool.name, tool)
  }

  get(name: string): Tool | undefined {
    return this.tools.get(name)
  }

  list(): Tool[] {
    return Array.from(this.tools.values())
  }

  findByCapability(capability: string): Tool[] {
    return this.list().filter(tool =>
      tool.description.toLowerCase().includes(capability.toLowerCase())
    )
  }
}
```

## 🌐 API Integration Patterns

### REST API Integration

```typescript
// Generic REST API tool
class RESTAPITool implements Tool {
  name = 'rest_api'
  description = 'Make HTTP requests to REST APIs'

  parameters = [
    {
      name: 'method',
      type: 'string' as const,
      description: 'HTTP method (GET, POST, PUT, DELETE)',
      required: true
    },
    {
      name: 'url',
      type: 'string' as const,
      description: 'API endpoint URL',
      required: true
    },
    {
      name: 'headers',
      type: 'object' as const,
      description: 'HTTP headers',
      required: false
    },
    {
      name: 'body',
      type: 'object' as const,
      description: 'Request body for POST/PUT',
      required: false
    }
  ]

  async execute(params: any) {
    const { method, url, headers = {}, body } = params

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: body ? JSON.stringify(body) : undefined
    })

    return {
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
      data: await response.json().catch(() => null)
    }
  }
}
```

### GraphQL API Integration

```typescript
// GraphQL API tool
class GraphQLTool implements Tool {
  name = 'graphql_api'
  description = 'Execute GraphQL queries and mutations'

  async execute(params: any) {
    const { endpoint, query, variables, headers = {} } = params

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: JSON.stringify({ query, variables })
    })

    const result = await response.json()

    if (result.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`)
    }

    return result.data
  }
}
```

## 🛠️ Built-in Tools

### Web Search Tool

```typescript
// Web search capability
class WebSearchTool implements Tool {
  name = 'web_search'
  description = 'Search the web for information'

  async execute(params: any) {
    const { query, numResults = 5 } = params

    // Use a search API (Google, Bing, etc.)
    const searchResults = await this.performSearch(query, numResults)

    return {
      query,
      results: searchResults.map(result => ({
        title: result.title,
        url: result.url,
        snippet: result.snippet
      }))
    }
  }

  private async performSearch(query: string, numResults: number) {
    // Implementation using search API
    const apiKey = process.env.SEARCH_API_KEY
    const response = await fetch(`https://api.searchservice.com/search?q=${encodeURIComponent(query)}&num=${numResults}`, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    })

    return response.json()
  }
}
```

### File Operations Tool

```typescript
// File system operations
class FileOperationsTool implements Tool {
  name = 'file_operations'
  description = 'Perform file system operations'

  async execute(params: any) {
    const { operation, path, content, destination } = params

    switch (operation) {
      case 'read':
        return await this.readFile(path)
      case 'write':
        return await this.writeFile(path, content)
      case 'list':
        return await this.listDirectory(path)
      case 'move':
        return await this.moveFile(path, destination)
      case 'delete':
        return await this.deleteFile(path)
      default:
        throw new Error(`Unknown operation: ${operation}`)
    }
  }

  private async readFile(path: string) {
    const content = await fs.promises.readFile(path, 'utf8')
    return { content, path }
  }

  private async writeFile(path: string, content: string) {
    await fs.promises.writeFile(path, content, 'utf8')
    return { success: true, path }
  }
}
```

### Database Tool

```typescript
// Database operations
class DatabaseTool implements Tool {
  name = 'database'
  description = 'Execute database queries'

  async execute(params: any) {
    const { query, parameters = [] } = params

    const result = await this.executeQuery(query, parameters)

    return {
      query,
      rows: result.rows,
      rowCount: result.rowCount,
      fields: result.fields?.map(f => f.name)
    }
  }

  private async executeQuery(query: string, parameters: any[]) {
    // Database connection and query execution
    const client = await this.getDatabaseClient()
    try {
      return await client.query(query, parameters)
    } finally {
      client.release()
    }
  }
}
```

## 🔐 Authentication & Security

### API Key Management

```typescript
// Secure API key management
class APIKeyManager {
  private keys = new Map<string, APIKeyConfig>()

  register(service: string, config: APIKeyConfig) {
    this.keys.set(service, config)
  }

  async getKey(service: string): Promise<string> {
    const config = this.keys.get(service)
    if (!config) {
      throw new Error(`No API key configured for ${service}`)
    }

    // Handle key rotation and refresh
    if (this.needsRefresh(config)) {
      await this.refreshKey(service, config)
    }

    return config.key
  }

  private needsRefresh(config: APIKeyConfig): boolean {
    return Date.now() - config.lastRefresh > config.refreshInterval
  }
}
```

### Rate Limiting

```typescript
// Rate limiting for API calls
class RateLimiter {
  private requests = new Map<string, number[]>()

  async checkLimit(service: string, limit: number, windowMs: number): Promise<boolean> {
    const now = Date.now()
    const windowStart = now - windowMs

    const serviceRequests = this.requests.get(service) || []
    const recentRequests = serviceRequests.filter(time => time > windowStart)

    if (recentRequests.length >= limit) {
      return false
    }

    recentRequests.push(now)
    this.requests.set(service, recentRequests)

    return true
  }

  async waitForLimit(service: string, limit: number, windowMs: number): Promise<void> {
    while (!(await this.checkLimit(service, limit, windowMs))) {
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }
}
```

## 🎯 Tool Selection & Execution

### Tool Selection Strategy

```typescript
// Intelligent tool selection
class ToolSelector {
  async selectTool(task: string, availableTools: Tool[]): Promise<Tool[]> {
    const taskAnalysis = await this.analyzeTask(task)
    const relevantTools = await this.findRelevantTools(taskAnalysis, availableTools)

    return this.rankTools(relevantTools, taskAnalysis)
  }

  private async analyzeTask(task: string) {
    // Analyze task requirements
    return {
      requiredCapabilities: await this.extractCapabilities(task),
      complexity: this.assessComplexity(task),
      dependencies: this.identifyDependencies(task)
    }
  }

  private async findRelevantTools(analysis: any, tools: Tool[]): Promise<Tool[]> {
    const relevant = []

    for (const tool of tools) {
      const relevance = await this.calculateRelevance(tool, analysis)
      if (relevance > 0.5) { // Relevance threshold
        relevant.push({ tool, relevance })
      }
    }

    return relevant.sort((a, b) => b.relevance - a.relevance)
  }
}
```

### Tool Execution Pipeline

```typescript
// Execute tools with error handling and retries
class ToolExecutor {
  async executeTool(tool: Tool, params: any, options: ExecutionOptions = {}): Promise<any> {
    const { maxRetries = 3, timeout = 30000 } = options

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const result = await this.executeWithTimeout(tool, params, timeout)
        await this.logExecution(tool, params, result, attempt)
        return result
      } catch (error) {
        await this.logError(tool, params, error, attempt)

        if (attempt === maxRetries) {
          throw new Error(`Tool execution failed after ${maxRetries} attempts: ${error.message}`)
        }

        await this.waitForRetry(attempt)
      }
    }
  }

  private async executeWithTimeout(tool: Tool, params: any, timeout: number): Promise<any> {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error('Tool execution timed out'))
      }, timeout)

      tool.execute(params)
        .then(result => {
          clearTimeout(timeoutId)
          resolve(result)
        })
        .catch(error => {
          clearTimeout(timeoutId)
          reject(error)
        })
    })
  }
}
```

## 📊 Tool Performance Monitoring

### Execution Metrics

```typescript
// Track tool performance
class ToolMonitor {
  private metrics = new Map<string, ToolMetrics>()

  recordExecution(toolName: string, duration: number, success: boolean, error?: string) {
    const metrics = this.metrics.get(toolName) || {
      executions: 0,
      successes: 0,
      failures: 0,
      totalDuration: 0,
      errors: []
    }

    metrics.executions++
    metrics.totalDuration += duration

    if (success) {
      metrics.successes++
    } else {
      metrics.failures++
      if (error) metrics.errors.push(error)
    }

    this.metrics.set(toolName, metrics)
  }

  getMetrics(toolName?: string) {
    if (toolName) {
      return this.metrics.get(toolName)
    }

    return Object.fromEntries(this.metrics.entries())
  }

  getSuccessRate(toolName: string): number {
    const metrics = this.metrics.get(toolName)
    if (!metrics) return 0

    return metrics.successes / metrics.executions
  }
}
```

## 🚀 Advanced Tool Features

### Tool Chaining

```typescript
// Chain multiple tools together
class ToolChain {
  private tools: Tool[] = []

  addTool(tool: Tool) {
    this.tools.push(tool)
  }

  async executeChain(input: any): Promise<any> {
    let currentInput = input

    for (const tool of this.tools) {
      currentInput = await tool.execute(currentInput)
    }

    return currentInput
  }

  async executeParallel(input: any): Promise<any[]> {
    const promises = this.tools.map(tool => tool.execute(input))
    return Promise.all(promises)
  }
}
```

### Custom Tool Development

```typescript
// Framework for custom tool development
abstract class BaseTool implements Tool {
  abstract name: string
  abstract description: string
  abstract parameters: Parameter[]

  async execute(params: any): Promise<any> {
    // Pre-execution validation
    this.validateParams(params)

    // Execute with error handling
    try {
      const result = await this.performExecution(params)
      await this.postExecution(result)
      return result
    } catch (error) {
      await this.handleError(error, params)
      throw error
    }
  }

  protected abstract performExecution(params: any): Promise<any>

  protected validateParams(params: any) {
    // Parameter validation logic
  }

  protected async postExecution(result: any) {
    // Post-execution cleanup/logging
  }

  protected async handleError(error: Error, params: any) {
    // Error handling logic
  }
}
```

## 📝 Chapter Summary

- ✅ Understood tool integration fundamentals
- ✅ Implemented REST and GraphQL API integrations
- ✅ Built web search and file operation tools
- ✅ Set up authentication and rate limiting
- ✅ Created intelligent tool selection systems
- ✅ Implemented performance monitoring
- ✅ Developed tool chaining and custom tools

**Key Takeaways:**
- Tools extend agent capabilities significantly
- Proper authentication and rate limiting are crucial
- Tool selection should be intelligent and context-aware
- Error handling and retries improve reliability
- Performance monitoring enables optimization
- Tool chaining enables complex workflows
