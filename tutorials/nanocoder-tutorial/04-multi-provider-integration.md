---
layout: default
title: "Nanocoder - Chapter 4: Multi-Provider Integration"
nav_order: 4
has_children: false
parent: "Nanocoder - AI Coding Agent Deep Dive"
---

# Chapter 4: Multi-Provider Integration

Welcome to **Chapter 4: Multi-Provider Integration**. In this part of **Nanocoder Tutorial: Building and Understanding AI Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> How AI coding agents abstract over multiple LLM backends through a unified provider interface.

## Overview

One of nanocoder's design goals is provider independence—the ability to work with any LLM that supports the OpenAI chat completions API format. This chapter explores the provider abstraction layer: the interface that unifies local models (Ollama, llama.cpp, LM Studio) and cloud APIs (OpenRouter, GitHub Models) behind a single contract.

## The Provider Interface

Every LLM backend must implement this interface:

```typescript
interface ChatRequest {
  messages: Message[];
  tools?: ToolDefinition[];
  stream?: boolean;
  temperature?: number;
  maxTokens?: number;
}

interface ChatResponse {
  content: string;
  toolCalls?: ToolCall[];
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  finishReason: "stop" | "tool_calls" | "length";
}

interface LLMProvider {
  name: string;
  chat(request: ChatRequest): Promise<ChatResponse>;
  chatStream(
    request: ChatRequest
  ): AsyncIterable<StreamChunk>;
  listModels(): Promise<string[]>;
  getModelInfo(model: string): Promise<ModelInfo>;
}
```

```mermaid
flowchart LR
    subgraph Agent["Agent Core"]
        Loop[Agent Loop]
    end

    subgraph Interface["Provider Interface"]
        Contract[LLMProvider]
    end

    subgraph Implementations["Provider Implementations"]
        OL[OllamaProvider]
        OA[OpenAIProvider]
        OR[OpenRouterProvider]
        LC[LlamaCppProvider]
        LM[LMStudioProvider]
    end

    Loop --> Contract
    Contract --> OL
    Contract --> OA
    Contract --> OR
    Contract --> LC
    Contract --> LM
```

## OpenAI-Compatible Provider

The base provider handles any server that implements the OpenAI chat completions API:

```typescript
class OpenAICompatibleProvider implements LLMProvider {
  name: string;
  private apiBase: string;
  private apiKey: string;
  private model: string;

  constructor(config: ProviderConfig) {
    this.name = config.name;
    this.apiBase = config.apiBase;
    this.apiKey = config.apiKey;
    this.model = config.model;
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(
      `${this.apiBase}/chat/completions`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify({
          model: this.model,
          messages: request.messages,
          tools: request.tools,
          temperature: request.temperature ?? 0.1,
          max_tokens: request.maxTokens ?? 4096,
          stream: false,
        }),
      }
    );

    if (!response.ok) {
      const error = await response.text();
      throw new ProviderError(
        `API request failed (${response.status}): ${error}`
      );
    }

    const data = await response.json();
    const choice = data.choices[0];

    return {
      content: choice.message.content ?? "",
      toolCalls: choice.message.tool_calls,
      usage: data.usage
        ? {
            promptTokens: data.usage.prompt_tokens,
            completionTokens: data.usage.completion_tokens,
            totalTokens: data.usage.total_tokens,
          }
        : undefined,
      finishReason: choice.finish_reason,
    };
  }

  async *chatStream(
    request: ChatRequest
  ): AsyncIterable<StreamChunk> {
    const response = await fetch(
      `${this.apiBase}/chat/completions`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify({
          model: this.model,
          messages: request.messages,
          tools: request.tools,
          temperature: request.temperature ?? 0.1,
          max_tokens: request.maxTokens ?? 4096,
          stream: true,
        }),
      }
    );

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = line.slice(6);
        if (data === "[DONE]") return;

        const chunk = JSON.parse(data);
        const delta = chunk.choices[0]?.delta;

        if (delta?.content) {
          yield { type: "content_delta", text: delta.content };
        }

        if (delta?.tool_calls) {
          for (const tc of delta.tool_calls) {
            yield {
              type: "tool_call_delta",
              id: tc.id,
              functionName: tc.function?.name,
              argumentsDelta: tc.function?.arguments ?? "",
            };
          }
        }
      }
    }
  }

  async listModels(): Promise<string[]> {
    const response = await fetch(`${this.apiBase}/models`, {
      headers: { Authorization: `Bearer ${this.apiKey}` },
    });
    const data = await response.json();
    return data.data.map((m: { id: string }) => m.id);
  }
}
```

## Ollama Provider

Ollama has its own API format but also supports OpenAI compatibility:

```typescript
class OllamaProvider extends OpenAICompatibleProvider {
  constructor(config?: Partial<ProviderConfig>) {
    super({
      name: "ollama",
      apiBase:
        config?.apiBase ?? "http://localhost:11434/v1",
      apiKey: config?.apiKey ?? "ollama", // Ollama ignores API keys
      model: config?.model ?? "qwen2.5-coder:7b",
    });
  }

  // Override model listing to use Ollama's native API
  async listModels(): Promise<string[]> {
    const baseUrl = this.apiBase.replace("/v1", "");
    const response = await fetch(`${baseUrl}/api/tags`);
    const data = await response.json();
    return data.models.map((m: { name: string }) => m.name);
  }

  // Check if Ollama is running
  async isAvailable(): Promise<boolean> {
    try {
      const baseUrl = this.apiBase.replace("/v1", "");
      const response = await fetch(baseUrl);
      return response.ok;
    } catch {
      return false;
    }
  }
}
```

## Provider Router

The router selects the right provider based on configuration and availability:

```typescript
class ProviderRouter {
  private providers: Map<string, LLMProvider> = new Map();
  private activeProvider: string;

  constructor(config: AgentConfig) {
    // Register configured providers
    if (config.providers) {
      for (const [name, providerConfig] of Object.entries(
        config.providers
      )) {
        this.registerProvider(name, providerConfig);
      }
    }

    // Auto-detect local providers
    this.autoDetect();

    this.activeProvider =
      config.defaultProvider ?? this.getFirstAvailable();
  }

  private registerProvider(
    name: string,
    config: ProviderConfig
  ): void {
    switch (config.type ?? name) {
      case "ollama":
        this.providers.set(
          name,
          new OllamaProvider(config)
        );
        break;
      default:
        this.providers.set(
          name,
          new OpenAICompatibleProvider({
            ...config,
            name,
          })
        );
    }
  }

  private async autoDetect(): Promise<void> {
    // Check for Ollama on default port
    if (!this.providers.has("ollama")) {
      const ollama = new OllamaProvider();
      if (await ollama.isAvailable()) {
        this.providers.set("ollama", ollama);
      }
    }
  }

  getActive(): LLMProvider {
    const provider = this.providers.get(this.activeProvider);
    if (!provider) {
      throw new Error(
        `No provider available. Configure one in agents.config.json`
      );
    }
    return provider;
  }

  switchProvider(name: string): void {
    if (!this.providers.has(name)) {
      throw new Error(
        `Unknown provider: ${name}. Available: ${[...this.providers.keys()].join(", ")}`
      );
    }
    this.activeProvider = name;
  }
}
```

## Model Capability Detection

Not all models support tool calling. The provider layer handles this:

```typescript
interface ModelCapabilities {
  supportsToolCalling: boolean;
  supportsStreaming: boolean;
  contextWindow: number;
  maxOutputTokens: number;
}

// Known model capabilities
const MODEL_CAPS: Record<string, Partial<ModelCapabilities>> = {
  "qwen2.5-coder": {
    supportsToolCalling: true,
    contextWindow: 32768,
  },
  "llama3.1": {
    supportsToolCalling: true,
    contextWindow: 128000,
  },
  "codellama": {
    supportsToolCalling: false,
    contextWindow: 16384,
  },
};

// Fallback for models without tool calling:
// Convert tools to system prompt instructions
function toolsToPromptFallback(
  tools: ToolDefinition[]
): string {
  let prompt = "You have access to these tools. ";
  prompt +=
    "To use a tool, respond with a JSON block:\n\n";
  prompt += '```json\n{"tool": "name", "args": {...}}\n```\n\n';

  for (const tool of tools) {
    prompt += `### ${tool.function.name}\n`;
    prompt += `${tool.function.description}\n`;
    prompt += `Parameters: ${JSON.stringify(tool.function.parameters, null, 2)}\n\n`;
  }

  return prompt;
}
```

## Environment Variable Interpolation

Configuration supports environment variable references for secure credential management:

```typescript
function interpolateEnvVars(value: string): string {
  return value.replace(
    /\$\{(\w+)\}/g,
    (match, varName) => {
      const envValue = process.env[varName];
      if (!envValue) {
        throw new Error(
          `Environment variable ${varName} is not set`
        );
      }
      return envValue;
    }
  );
}

// Usage in config loading
function loadProviderConfig(
  raw: RawProviderConfig
): ProviderConfig {
  return {
    name: raw.name,
    apiBase: raw.apiBase,
    apiKey: interpolateEnvVars(raw.apiKey), // "${OPENROUTER_API_KEY}" → actual key
    model: raw.model,
  };
}
```

## Cost Tracking

Cloud providers charge per token. Tracking costs helps users manage spend:

```typescript
class CostTracker {
  private sessions: SessionCost[] = [];

  recordUsage(
    provider: string,
    model: string,
    usage: TokenUsage
  ): void {
    const pricing = this.getPricing(model);
    const cost =
      (usage.promptTokens * pricing.inputPerMillion) /
        1_000_000 +
      (usage.completionTokens * pricing.outputPerMillion) /
        1_000_000;

    this.sessions.push({
      timestamp: Date.now(),
      provider,
      model,
      tokens: usage,
      cost,
    });
  }

  getSessionTotal(): number {
    return this.sessions.reduce((sum, s) => sum + s.cost, 0);
  }

  private getPricing(model: string): ModelPricing {
    // Pricing per million tokens (approximate)
    const pricing: Record<string, ModelPricing> = {
      "claude-sonnet-4-20250514": {
        inputPerMillion: 3.0,
        outputPerMillion: 15.0,
      },
      "gpt-4o": {
        inputPerMillion: 2.5,
        outputPerMillion: 10.0,
      },
      "llama3.1:70b": {
        inputPerMillion: 0,
        outputPerMillion: 0,
      }, // Local
    };
    return (
      pricing[model] ?? {
        inputPerMillion: 0,
        outputPerMillion: 0,
      }
    );
  }
}
```

## Summary

Provider abstraction is what makes an AI coding agent truly flexible. By standardizing on the OpenAI chat completions format, nanocoder can work with any LLM backend—from a free local model on Ollama to a frontier model through a cloud API. The key patterns are the provider interface, automatic detection of local servers, and graceful fallbacks for models that lack tool calling support.

## Key Takeaways

1. The provider interface (`chat`, `chatStream`, `listModels`) abstracts all LLM differences
2. OpenAI's chat completions format has become the de facto standard for LLM APIs
3. Ollama provides local inference with OpenAI-compatible endpoints out of the box
4. Environment variable interpolation keeps credentials out of config files
5. Models without native tool calling can use a prompt-based fallback
6. Cost tracking is essential for cloud provider usage management

## Next Steps

In [Chapter 5: Context Management](05-context-management.md), we'll explore how AI coding agents manage the limited context window—fitting the right code into the right number of tokens.

---

*Built with insights from the [Nanocoder](https://github.com/Nano-Collective/nanocoder) project.*

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Nanocoder Tutorial: Building and Understanding AI Coding Agents**
- tutorial slug: **nanocoder-tutorial**
- chapter focus: **Chapter 4: Multi-Provider Integration**
- system context: **Nanocoder Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 4: Multi-Provider Integration`.
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

- [Nanocoder Repository](https://github.com/Nano-Collective/nanocoder)
- [Nanocoder Releases](https://github.com/Nano-Collective/nanocoder/releases)
- [Nanocoder Documentation Directory](https://github.com/Nano-Collective/nanocoder/tree/main/docs)
- [Nanocoder MCP Configuration Guide](https://github.com/Nano-Collective/nanocoder/blob/main/docs/mcp-configuration.md)
- [Nano Collective Website](https://nanocollective.org/)

### Cross-Tutorial Connection Map

- [Aider Tutorial](../aider-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [Continue Tutorial](../continue-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 4: Multi-Provider Integration`.
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

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `name`, `config`, `request` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Multi-Provider Integration` as an operating subsystem inside **Nanocoder Tutorial: Building and Understanding AI Coding Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `providers`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Multi-Provider Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `name`.
2. **Input normalization**: shape incoming data so `config` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `request`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Nanocoder Repository](https://github.com/Nano-Collective/nanocoder)
  Why it matters: authoritative reference on `Nanocoder Repository` (github.com).
- [Nanocoder Releases](https://github.com/Nano-Collective/nanocoder/releases)
  Why it matters: authoritative reference on `Nanocoder Releases` (github.com).
- [Nanocoder Documentation Directory](https://github.com/Nano-Collective/nanocoder/tree/main/docs)
  Why it matters: authoritative reference on `Nanocoder Documentation Directory` (github.com).
- [Nanocoder MCP Configuration Guide](https://github.com/Nano-Collective/nanocoder/blob/main/docs/mcp-configuration.md)
  Why it matters: authoritative reference on `Nanocoder MCP Configuration Guide` (github.com).
- [Nano Collective Website](https://nanocollective.org/)
  Why it matters: authoritative reference on `Nano Collective Website` (nanocollective.org).

Suggested trace strategy:
- search upstream code for `name` and `config` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Tool System Internals](03-tool-system-internals.md)
- [Next Chapter: Chapter 5: Context Management](05-context-management.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
