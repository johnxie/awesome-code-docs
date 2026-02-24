---
layout: default
title: "Chapter 4: AI Integration Patterns"
nav_order: 4
has_children: false
parent: "LobeChat AI Platform"
---

# Chapter 4: AI Integration Patterns

Welcome to **Chapter 4: AI Integration Patterns**. In this part of **LobeChat AI Platform: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Multi-provider AI orchestration and advanced integration techniques

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- Multi-provider AI model orchestration
- Dynamic provider selection and failover
- Advanced prompt engineering techniques
- Function calling and tool integration
- Custom AI pipeline creation

## 🤖 Multi-Provider Orchestration

### **Intelligent Provider Selection**

LobeChat's core strength is seamless integration with multiple AI providers:

```typescript
// AI provider orchestration system
class AIOrchestrator {
  private providers: Map<string, AIProvider> = new Map();
  private metrics: ProviderMetrics;

  constructor() {
    this.initializeProviders();
    this.metrics = new ProviderMetrics();
  }

  private initializeProviders() {
    // OpenAI providers
    this.providers.set('gpt-4', new OpenAIProvider({
      model: 'gpt-4',
      apiKey: process.env.OPENAI_API_KEY,
      capabilities: ['chat', 'function_calling', 'vision']
    }));

    this.providers.set('gpt-3.5-turbo', new OpenAIProvider({
      model: 'gpt-3.5-turbo',
      apiKey: process.env.OPENAI_API_KEY,
      capabilities: ['chat', 'function_calling']
    }));

    // Anthropic providers
    this.providers.set('claude-3-opus', new AnthropicProvider({
      model: 'claude-3-opus-20240229',
      apiKey: process.env.ANTHROPIC_API_KEY,
      capabilities: ['chat', 'vision']
    }));

    // Google providers
    this.providers.set('gemini-pro', new GoogleProvider({
      model: 'gemini-pro',
      apiKey: process.env.GOOGLE_API_KEY,
      capabilities: ['chat', 'function_calling']
    }));

    // Local providers
    this.providers.set('ollama-llama2', new OllamaProvider({
      model: 'llama2:7b',
      endpoint: process.env.OLLAMA_ENDPOINT,
      capabilities: ['chat']
    }));
  }

  async selectProvider(requirements: ProviderRequirements): Promise<AIProvider> {
    const candidates = this.rankProviders(requirements);

    for (const candidate of candidates) {
      if (await this.isProviderAvailable(candidate.provider)) {
        return candidate.provider;
      }
    }

    throw new Error('No suitable AI provider available');
  }

  private rankProviders(requirements: ProviderRequirements): ProviderCandidate[] {
    const candidates: ProviderCandidate[] = [];

    for (const [id, provider] of this.providers) {
      const score = this.calculateProviderScore(provider, requirements, id);
      candidates.push({ provider, score, id });
    }

    return candidates.sort((a, b) => b.score - a.score);
  }

  private calculateProviderScore(
    provider: AIProvider,
    requirements: ProviderRequirements,
    providerId: string
  ): number {
    let score = 0;

    // Capability matching (40 points max)
    if (requirements.capabilities) {
      for (const capability of requirements.capabilities) {
        if (provider.hasCapability(capability)) {
          score += 10;
        }
      }
    }

    // Model preference (20 points max)
    if (requirements.preferredModels?.includes(providerId)) {
      score += 20;
    }

    // Cost efficiency (15 points max)
    if (requirements.budgetPriority) {
      score += (1 - this.getProviderCostScore(providerId)) * 15;
    }

    // Performance metrics (15 points max)
    const metrics = this.metrics.getProviderMetrics(providerId);
    score += metrics.successRate * 15;

    // Latency preference (10 points max)
    if (requirements.lowLatency) {
      score += Math.max(0, 10 - (metrics.averageLatency / 100)); // Lower latency = higher score
    }

    return score;
  }

  private getProviderCostScore(providerId: string): number {
    const costScores: Record<string, number> = {
      'gpt-4': 0.9,           // Expensive
      'claude-3-opus': 0.8,   // Very expensive
      'gpt-3.5-turbo': 0.3,   // Moderate
      'gemini-pro': 0.2,      // Cheap
      'ollama-llama2': 0.0    // Free
    };

    return costScores[providerId] || 0.5;
  }

  private async isProviderAvailable(provider: AIProvider): Promise<boolean> {
    try {
      await provider.healthCheck();
      return true;
    } catch (error) {
      return false;
    }
  }

  async executeWithProviderSelection(
    messages: Message[],
    requirements: ProviderRequirements = {}
  ): Promise<AIResponse> {
    const provider = await this.selectProvider(requirements);
    const startTime = Date.now();

    try {
      const response = await provider.chat(messages, requirements);
      const latency = Date.now() - startTime;

      // Record metrics
      await this.metrics.recordRequest(provider.getId(), true, latency, response.usage);

      return {
        ...response,
        provider: provider.getId(),
        latency
      };

    } catch (error) {
      const latency = Date.now() - startTime;
      await this.metrics.recordRequest(provider.getId(), false, latency);

      throw error;
    }
  }
}

interface ProviderRequirements {
  capabilities?: string[];
  preferredModels?: string[];
  budgetPriority?: boolean;
  lowLatency?: boolean;
  maxTokens?: number;
  temperature?: number;
}

interface ProviderCandidate {
  provider: AIProvider;
  score: number;
  id: string;
}

interface AIResponse {
  content: string;
  usage: TokenUsage;
  finishReason: string;
  provider: string;
  latency: number;
}
```

### **Failover and Load Balancing**

```typescript
// Advanced provider failover system
class ProviderFailoverManager {
  private primaryProviders: AIProvider[];
  private backupProviders: AIProvider[];
  private failureCounts: Map<string, number> = new Map();
  private circuitBreakers: Map<string, CircuitBreaker> = new Map();

  constructor(primaryProviders: AIProvider[], backupProviders: AIProvider[] = []) {
    this.primaryProviders = primaryProviders;
    this.backupProviders = backupProviders;

    // Initialize circuit breakers
    [...primaryProviders, ...backupProviders].forEach(provider => {
      this.circuitBreakers.set(provider.getId(), new CircuitBreaker());
    });
  }

  async executeWithFailover(
    messages: Message[],
    options: ExecutionOptions = {}
  ): Promise<AIResponse> {
    const errors: Error[] = [];

    // Try primary providers first
    for (const provider of this.primaryProviders) {
      if (this.isCircuitBreakerOpen(provider.getId())) {
        continue; // Skip failed providers
      }

      try {
        const response = await provider.chat(messages, options);
        this.recordSuccess(provider.getId());
        return { ...response, provider: provider.getId() };
      } catch (error) {
        errors.push(error);
        this.recordFailure(provider.getId(), error);
      }
    }

    // Try backup providers if primary failed
    for (const provider of this.backupProviders) {
      if (this.isCircuitBreakerOpen(provider.getId())) {
        continue;
      }

      try {
        const response = await provider.chat(messages, {
          ...options,
          fallbackMode: true // Indicate this is a fallback
        });
        this.recordSuccess(provider.getId());
        return { ...response, provider: provider.getId(), fallback: true };
      } catch (error) {
        errors.push(error);
        this.recordFailure(provider.getId(), error);
      }
    }

    // All providers failed
    throw new AggregateError(
      errors,
      `All AI providers failed. Last error: ${errors[errors.length - 1]?.message}`
    );
  }

  private recordSuccess(providerId: string): void {
    this.failureCounts.set(providerId, 0);
    const circuitBreaker = this.circuitBreakers.get(providerId);
    circuitBreaker?.recordSuccess();
  }

  private recordFailure(providerId: string, error: Error): void {
    const currentFailures = this.failureCounts.get(providerId) || 0;
    this.failureCounts.set(providerId, currentFailures + 1);

    const circuitBreaker = this.circuitBreakers.get(providerId);
    circuitBreaker?.recordFailure();
  }

  private isCircuitBreakerOpen(providerId: string): boolean {
    const circuitBreaker = this.circuitBreakers.get(providerId);
    return circuitBreaker?.isOpen() || false;
  }

  getProviderHealth(): ProviderHealth[] {
    return [...this.primaryProviders, ...this.backupProviders].map(provider => {
      const failureCount = this.failureCounts.get(provider.getId()) || 0;
      const circuitBreaker = this.circuitBreakers.get(provider.getId());

      return {
        providerId: provider.getId(),
        failureCount,
        circuitBreakerState: circuitBreaker?.getState() || 'closed',
        isHealthy: !this.isCircuitBreakerOpen(provider.getId())
      };
    });
  }
}

interface ExecutionOptions {
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
  functions?: FunctionDefinition[];
}

interface ProviderHealth {
  providerId: string;
  failureCount: number;
  circuitBreakerState: string;
  isHealthy: boolean;
}
```

## 🛠️ Function Calling and Tools

### **Tool Integration Framework**

```typescript
// Function calling and tool integration
class ToolManager {
  private tools: Map<string, ToolDefinition> = new Map();
  private toolExecutors: Map<string, ToolExecutor> = new Map();

  registerTool(tool: ToolDefinition): void {
    this.tools.set(tool.name, tool);
    this.toolExecutors.set(tool.name, new ToolExecutor(tool));
  }

  getAvailableTools(): ToolDefinition[] {
    return Array.from(this.tools.values());
  }

  getToolFunctionDefinitions(): FunctionDefinition[] {
    return this.getAvailableTools().map(tool => ({
      name: tool.name,
      description: tool.description,
      parameters: tool.parameters
    }));
  }

  async executeTool(toolName: string, parameters: any): Promise<ToolResult> {
    const executor = this.toolExecutors.get(toolName);
    if (!executor) {
      throw new Error(`Tool ${toolName} not found`);
    }

    return await executor.execute(parameters);
  }

  async executeToolCall(toolCall: ToolCall): Promise<ToolResult> {
    return await this.executeTool(toolCall.name, toolCall.parameters);
  }
}

interface ToolDefinition {
  name: string;
  description: string;
  parameters: JSONSchema;
  execute: (params: any) => Promise<ToolResult>;
  category?: string;
  tags?: string[];
}

interface ToolResult {
  success: boolean;
  data?: any;
  error?: string;
  metadata?: {
    executionTime: number;
    toolVersion: string;
  };
}

interface ToolCall {
  name: string;
  parameters: any;
}

// Built-in tool implementations
class WebSearchTool implements ToolDefinition {
  name = 'web_search';
  description = 'Search the web for information';

  parameters = {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Search query'
      },
      limit: {
        type: 'number',
        description: 'Maximum number of results',
        default: 5
      }
    },
    required: ['query']
  };

  async execute(params: { query: string; limit?: number }): Promise<ToolResult> {
    try {
      const results = await this.performWebSearch(params.query, params.limit || 5);
      return {
        success: true,
        data: results,
        metadata: {
          executionTime: Date.now(),
          toolVersion: '1.0.0'
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  private async performWebSearch(query: string, limit: number): Promise<SearchResult[]> {
    // Integration with search API (e.g., Bing, Google, DuckDuckGo)
    const response = await fetch(`https://api.search-provider.com/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    const data = await response.json();

    return data.results.map(result => ({
      title: result.title,
      url: result.url,
      snippet: result.snippet
    }));
  }
}

interface SearchResult {
  title: string;
  url: string;
  snippet: string;
}
```

### **Conversational Tool Use**

```typescript
// Conversational AI with tool integration
class ConversationalAgent {
  private toolManager: ToolManager;
  private conversationHistory: Message[];
  private systemPrompt: string;

  constructor(toolManager: ToolManager) {
    this.toolManager = toolManager;
    this.conversationHistory = [];
    this.systemPrompt = this.buildSystemPrompt();
  }

  async processMessage(userMessage: string): Promise<AgentResponse> {
    // Add user message to history
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    });

    // Get available tools
    const tools = this.toolManager.getToolFunctionDefinitions();

    // Prepare messages for AI
    const messages: Message[] = [
      { role: 'system', content: this.systemPrompt },
      ...this.conversationHistory
    ];

    // Call AI with tool support
    const aiResponse = await this.callAIWithTools(messages, tools);

    // Handle tool calls if present
    if (aiResponse.toolCalls && aiResponse.toolCalls.length > 0) {
      const toolResults = await this.executeToolCalls(aiResponse.toolCalls);

      // Add tool results to conversation
      this.conversationHistory.push({
        role: 'assistant',
        content: aiResponse.content,
        toolCalls: aiResponse.toolCalls
      });

      for (const result of toolResults) {
        this.conversationHistory.push({
          role: 'tool',
          content: JSON.stringify(result),
          toolCallId: result.toolCallId
        });
      }

      // Get final response with tool results
      const finalMessages = [...messages, aiResponse.message, ...toolResults.map(r => ({
        role: 'tool' as const,
        content: JSON.stringify(r)
      }))];

      const finalResponse = await this.callAIWithTools(finalMessages, tools, false);
      this.conversationHistory.push(finalResponse.message);

      return {
        message: finalResponse.content,
        toolResults
      };
    } else {
      // No tool calls, return direct response
      this.conversationHistory.push(aiResponse.message);
      return {
        message: aiResponse.content
      };
    }
  }

  private buildSystemPrompt(): string {
    const tools = this.toolManager.getAvailableTools();
    const toolDescriptions = tools.map(tool =>
      `${tool.name}: ${tool.description}`
    ).join('\n');

    return `You are a helpful AI assistant with access to various tools.

Available tools:
${toolDescriptions}

When a user asks something that would benefit from using a tool, use the appropriate tool by calling it with the function_call syntax. Otherwise, respond normally.

Guidelines:
- Use tools when the user asks for current information, calculations, or external data
- Explain what you're doing when using tools
- Be concise but helpful
- Ask for clarification if the request is ambiguous`;
  }

  private async callAIWithTools(
    messages: Message[],
    tools: FunctionDefinition[],
    allowToolCalls: boolean = true
  ): Promise<AIResponseWithTools> {
    const provider = await this.orchestrator.selectProvider({
      capabilities: allowToolCalls ? ['function_calling'] : ['chat']
    });

    return await provider.chat(messages, {
      functions: allowToolCalls ? tools : undefined,
      temperature: 0.7
    });
  }

  private async executeToolCalls(toolCalls: ToolCall[]): Promise<ToolResultWithId[]> {
    const results: ToolResultWithId[] = [];

    for (const toolCall of toolCalls) {
      try {
        const result = await this.toolManager.executeToolCall(toolCall);
        results.push({
          ...result,
          toolCallId: toolCall.id
        });
      } catch (error) {
        results.push({
          success: false,
          error: error.message,
          toolCallId: toolCall.id
        });
      }
    }

    return results;
  }
}

interface AgentResponse {
  message: string;
  toolResults?: ToolResultWithId[];
}

interface ToolResultWithId extends ToolResult {
  toolCallId: string;
}
```

## 🎨 Advanced Prompt Engineering

### **Dynamic Prompt Construction**

```typescript
// Advanced prompt engineering system
class PromptEngineer {
  private promptTemplates: Map<string, PromptTemplate> = new Map();
  private contextProviders: Map<string, ContextProvider> = new Map();

  registerTemplate(name: string, template: PromptTemplate): void {
    this.promptTemplates.set(name, template);
  }

  registerContextProvider(name: string, provider: ContextProvider): void {
    this.contextProviders.set(name, provider);
  }

  async buildPrompt(
    templateName: string,
    variables: Record<string, any>,
    context: PromptContext = {}
  ): Promise<string> {
    const template = this.promptTemplates.get(templateName);
    if (!template) {
      throw new Error(`Template ${templateName} not found`);
    }

    // Gather context from providers
    const contextData = await this.gatherContext(context);

    // Merge variables with context
    const allVariables = { ...variables, ...contextData };

    // Render template
    return this.renderTemplate(template, allVariables);
  }

  private async gatherContext(context: PromptContext): Promise<Record<string, any>> {
    const contextData: Record<string, any> = {};

    for (const [key, providerName] of Object.entries(context)) {
      const provider = this.contextProviders.get(providerName);
      if (provider) {
        contextData[key] = await provider.getContext();
      }
    }

    return contextData;
  }

  private renderTemplate(template: PromptTemplate, variables: Record<string, any>): string {
    let prompt = template.template;

    // Replace variables
    for (const [key, value] of Object.entries(variables)) {
      const placeholder = new RegExp(`\\$\\{${key}\\}`, 'g');
      prompt = prompt.replace(placeholder, String(value));
    }

    // Apply template transformations
    if (template.transformations) {
      for (const transformation of template.transformations) {
        prompt = this.applyTransformation(prompt, transformation);
      }
    }

    return prompt;
  }

  private applyTransformation(prompt: string, transformation: PromptTransformation): string {
    switch (transformation.type) {
      case 'uppercase':
        return prompt.toUpperCase();
      case 'lowercase':
        return prompt.toLowerCase();
      case 'trim':
        return prompt.trim();
      case 'prefix':
        return `${transformation.value}${prompt}`;
      case 'suffix':
        return `${prompt}${transformation.value}`;
      case 'replace':
        return prompt.replace(new RegExp(transformation.pattern, 'g'), transformation.value);
      default:
        return prompt;
    }
  }
}

interface PromptTemplate {
  name: string;
  description: string;
  template: string;
  requiredVariables: string[];
  optionalVariables?: string[];
  transformations?: PromptTransformation[];
  category?: string;
}

interface PromptTransformation {
  type: 'uppercase' | 'lowercase' | 'trim' | 'prefix' | 'suffix' | 'replace';
  pattern?: string;
  value: string;
}

interface ContextProvider {
  getContext(): Promise<any>;
}

interface PromptContext {
  [variableName: string]: string; // Context provider name
}

// Example context providers
class ConversationContextProvider implements ContextProvider {
  constructor(private conversation: Message[]) {}

  async getContext(): Promise<string> {
    // Return recent conversation summary
    const recentMessages = this.conversation.slice(-5);
    return recentMessages.map(msg => `${msg.role}: ${msg.content}`).join('\n');
  }
}

class UserPreferencesProvider implements ContextProvider {
  constructor(private userId: string) {}

  async getContext(): Promise<any> {
    // Return user preferences from database
    return {
      preferredLanguage: 'en',
      expertiseLevel: 'intermediate',
      preferredStyle: 'concise'
    };
  }
}
```

### **Prompt Optimization**

```typescript
// Automatic prompt optimization
class PromptOptimizer {
  private optimizationRules: OptimizationRule[] = [];

  constructor() {
    this.initializeRules();
  }

  private initializeRules() {
    this.optimizationRules = [
      {
        name: 'remove_redundancy',
        condition: (prompt: string) => prompt.length > 1000,
        action: (prompt: string) => this.removeRedundantInstructions(prompt)
      },
      {
        name: 'clarify_ambiguity',
        condition: (prompt: string) => this.hasAmbiguousTerms(prompt),
        action: (prompt: string) => this.addClarifications(prompt)
      },
      {
        name: 'optimize_structure',
        condition: () => true, // Always apply
        action: (prompt: string) => this.optimizeStructure(prompt)
      },
      {
        name: 'add_examples',
        condition: (prompt: string) => !prompt.includes('Example'),
        action: (prompt: string) => this.addExamples(prompt)
      }
    ];
  }

  optimizePrompt(prompt: string, context?: PromptContext): string {
    let optimizedPrompt = prompt;

    for (const rule of this.optimizationRules) {
      if (rule.condition(optimizedPrompt)) {
        optimizedPrompt = rule.action(optimizedPrompt);
      }
    }

    return optimizedPrompt;
  }

  private removeRedundantInstructions(prompt: string): string {
    // Remove duplicate instructions
    const lines = prompt.split('\n');
    const seen = new Set<string>();
    const uniqueLines: string[] = [];

    for (const line of lines) {
      const normalized = line.trim().toLowerCase();
      if (!seen.has(normalized) && normalized.length > 0) {
        seen.add(normalized);
        uniqueLines.push(line);
      }
    }

    return uniqueLines.join('\n');
  }

  private hasAmbiguousTerms(prompt: string): boolean {
    const ambiguousTerms = ['good', 'bad', 'nice', 'etc', 'etc.'];
    return ambiguousTerms.some(term => prompt.toLowerCase().includes(term));
  }

  private addClarifications(prompt: string): string {
    // Add specific clarifications for ambiguous terms
    let clarified = prompt;

    clarified = clarified.replace(/\bgood\b/gi, 'high-quality, well-written');
    clarified = clarified.replace(/\bbad\b/gi, 'low-quality, poorly-written');
    clarified = clarified.replace(/\betc\b/gi, 'and other relevant items');

    return clarified;
  }

  private optimizeStructure(prompt: string): string {
    // Reorganize prompt for better AI comprehension
    const sections = this.identifySections(prompt);

    if (sections.instructions && sections.examples && sections.context) {
      // Reorder: Context -> Instructions -> Examples
      return `${sections.context}\n\n${sections.instructions}\n\n${sections.examples}`;
    }

    return prompt;
  }

  private addExamples(prompt: string): string {
    // Add relevant examples based on prompt content
    if (prompt.toLowerCase().includes('code')) {
      return prompt + '\n\nExample:\n```javascript\nfunction greet(name) {\n  return `Hello, ${name}!`;\n}\n```';
    }

    if (prompt.toLowerCase().includes('write') || prompt.toLowerCase().includes('essay')) {
      return prompt + '\n\nExample structure:\n1. Introduction\n2. Main points\n3. Conclusion';
    }

    return prompt;
  }

  private identifySections(prompt: string): Record<string, string> {
    const sections: Record<string, string> = {};
    const lines = prompt.split('\n');

    let currentSection = '';
    let currentContent: string[] = [];

    for (const line of lines) {
      if (line.match(/^(Context|Instructions?|Examples?|Requirements?):/i)) {
        // Save previous section
        if (currentSection && currentContent.length > 0) {
          sections[currentSection.toLowerCase()] = currentContent.join('\n');
        }

        // Start new section
        currentSection = line.replace(/[:\s]+$/, '');
        currentContent = [];
      } else {
        currentContent.push(line);
      }
    }

    // Save last section
    if (currentSection && currentContent.length > 0) {
      sections[currentSection.toLowerCase()] = currentContent.join('\n');
    }

    return sections;
  }
}

interface OptimizationRule {
  name: string;
  condition: (prompt: string) => boolean;
  action: (prompt: string) => string;
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 75 minutes**

1. **Multi-Provider Setup**: Configure multiple AI providers and implement intelligent selection
2. **Tool Integration**: Create custom tools and integrate them into conversations
3. **Advanced Prompting**: Build dynamic prompt templates with context providers
4. **Conversational Agent**: Implement a complete agent with tool use and conversation memory
5. **Performance Testing**: Compare different providers and optimization techniques

---

**Ready for production?** Continue to [Chapter 5: Production Deployment](05-production-deployment.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `provider`, `prompt`, `tool` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: AI Integration Patterns` as an operating subsystem inside **LobeChat AI Platform: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `providers`, `error` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: AI Integration Patterns` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `provider`.
2. **Input normalization**: shape incoming data so `prompt` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `tool`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LobeChat](https://github.com/lobehub/lobe-chat)
  Why it matters: authoritative reference on `LobeChat` (github.com).

Suggested trace strategy:
- search upstream code for `provider` and `prompt` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Streaming Architecture](03-streaming-architecture.md)
- [Next Chapter: Chapter 5: Production Deployment](05-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
