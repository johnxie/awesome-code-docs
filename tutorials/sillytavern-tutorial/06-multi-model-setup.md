---
layout: default
title: "Chapter 6: Multi-Model Setup"
parent: "SillyTavern Tutorial"
nav_order: 6
---

# Chapter 6: Multi-Model Setup

Welcome to **Chapter 6: Multi-Model Setup**. In this part of **SillyTavern Tutorial: Advanced LLM Frontend for Power Users**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Configure and switch between multiple LLM providers for optimal results.

## Overview

SillyTavern supports numerous AI backends, from cloud APIs to local models. This chapter covers setting up multiple providers, optimizing settings for each, and switching between them seamlessly.

## Supported Backends

### Provider Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Supported AI Backends                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CLOUD PROVIDERS                                               │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │   OpenAI    │  │   Claude    │  │   Google    │            │
│   │   GPT-4o    │  │   Opus/Sonnet│  │   Gemini   │            │
│   │   GPT-4     │  │   Haiku     │  │             │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │   Cohere    │  │  Mistral AI │  │  OpenRouter │            │
│   │  Command R+ │  │  Large/Med  │  │  (Multi)    │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│   LOCAL/SELF-HOSTED                                             │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │  KoboldAI   │  │ Text Gen UI │  │  LM Studio  │            │
│   │  (koboldcpp)│  │ (oobabooga) │  │             │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │   Ollama    │  │   vLLM      │  │   llamafile │            │
│   │             │  │             │  │             │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Cloud Provider Configuration

### OpenAI Setup

```javascript
// OpenAI configuration
const openAIConfig = {
  // API Settings
  apiKey: "sk-...",
  apiUrl: "https://api.openai.com/v1",

  // Model selection
  model: "gpt-4o",  // or gpt-4, gpt-4-turbo, gpt-3.5-turbo

  // Generation parameters
  parameters: {
    temperature: 0.8,      // 0.0-2.0: creativity level
    top_p: 0.9,           // 0.0-1.0: nucleus sampling
    max_tokens: 2048,      // Maximum response length
    presence_penalty: 0.0, // -2.0 to 2.0: new topic encouragement
    frequency_penalty: 0.0 // -2.0 to 2.0: repetition penalty
  },

  // Advanced options
  advanced: {
    streamingEnabled: true,
    logitBias: {},        // Token manipulation
    stop: [],             // Stop sequences
    seed: null            // For reproducibility
  }
};

// Testing connection
async function testOpenAI(config) {
  try {
    const response = await fetch(`${config.apiUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.apiKey}`
      },
      body: JSON.stringify({
        model: config.model,
        messages: [{ role: 'user', content: 'Hello!' }],
        max_tokens: 10
      })
    });

    const data = await response.json();
    return { success: true, model: config.model, response: data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

### Claude (Anthropic) Setup

```javascript
// Claude configuration
const claudeConfig = {
  apiKey: "sk-ant-...",
  apiUrl: "https://api.anthropic.com",

  // Model selection
  model: "claude-opus-4-20250514",  // or claude-sonnet-4-20250514, claude-3-5-haiku-20241022

  parameters: {
    temperature: 0.8,
    max_tokens: 4096,
    top_p: 0.9,
    top_k: 40
  },

  // Claude-specific features
  features: {
    systemPromptPosition: "system",  // Claude supports system role
    supportsImages: true,             // Vision capabilities
    supportsTools: true               // Function calling
  }
};

// Claude API call
async function callClaude(config, messages) {
  const response = await fetch(`${config.apiUrl}/v1/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': config.apiKey,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: config.model,
      max_tokens: config.parameters.max_tokens,
      messages: messages,
      temperature: config.parameters.temperature
    })
  });

  return response.json();
}
```

### OpenRouter (Multi-Provider)

```javascript
// OpenRouter configuration (access many models with one API)
const openRouterConfig = {
  apiKey: "sk-or-...",
  apiUrl: "https://openrouter.ai/api/v1",

  // Model examples
  models: {
    // Anthropic through OpenRouter
    claude: "anthropic/claude-3-opus",

    // OpenAI through OpenRouter
    gpt4: "openai/gpt-4-turbo",

    // Open source models
    llama: "meta-llama/llama-3-70b-instruct",
    mistral: "mistralai/mistral-large",

    // Specialized models
    creative: "anthropic/claude-3-opus",
    coding: "deepseek/deepseek-coder"
  },

  // Routing preferences
  routing: {
    fallback: true,        // Use fallback if primary fails
    order: ["anthropic/claude-3-opus", "openai/gpt-4"],
    costOptimize: false    // Prefer quality over cost
  }
};
```

## Local Model Configuration

### KoboldAI / koboldcpp

```javascript
// KoboldAI configuration
const koboldConfig = {
  endpoint: "http://localhost:5001",

  // Generation settings
  parameters: {
    max_context_length: 4096,
    max_length: 200,           // Response length
    temperature: 0.7,
    top_p: 0.9,
    top_k: 40,
    typical_p: 1.0,
    tfs: 1.0,                   // Tail-free sampling
    rep_pen: 1.1,               // Repetition penalty
    rep_pen_range: 2048,        // How far back to check
    rep_pen_slope: 0.7,
    sampler_order: [6, 0, 1, 3, 4, 2, 5]
  },

  // KoboldAI specific
  kobold: {
    useLlama: true,            // Using llama.cpp backend
    gpuLayers: 35,             // Layers offloaded to GPU
    contextShift: true,        // Smart context handling
    mirostat: 0                // 0=off, 1=v1, 2=v2
  }
};

// KoboldAI generate call
async function callKobold(config, prompt) {
  const response = await fetch(`${config.endpoint}/api/v1/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      ...config.parameters
    })
  });

  const data = await response.json();
  return data.results[0].text;
}
```

### Text Generation WebUI (Oobabooga)

```javascript
// Text Gen WebUI configuration
const textGenConfig = {
  endpoint: "http://localhost:5000",

  // API mode (OpenAI compatible or native)
  apiMode: "openai",  // or "blocking", "streaming"

  // Generation parameters
  parameters: {
    max_new_tokens: 250,
    temperature: 0.7,
    top_p: 0.9,
    top_k: 40,
    repetition_penalty: 1.18,
    encoder_repetition_penalty: 1.0,
    do_sample: true,

    // Advanced sampling
    min_p: 0.0,
    top_a: 0.0,
    tfs: 1.0,
    epsilon_cutoff: 0,
    eta_cutoff: 0
  },

  // Chat template
  chatTemplate: {
    name: "chatml",  // or "llama-2", "alpaca", "vicuna"
    systemPrefix: "<|im_start|>system\n",
    systemSuffix: "<|im_end|>\n",
    userPrefix: "<|im_start|>user\n",
    userSuffix: "<|im_end|>\n",
    assistantPrefix: "<|im_start|>assistant\n",
    assistantSuffix: "<|im_end|>\n"
  }
};
```

### Ollama

```javascript
// Ollama configuration
const ollamaConfig = {
  endpoint: "http://localhost:11434",

  // Model management
  model: "llama3:70b",  // or mistral, mixtral, neural-chat, etc.

  parameters: {
    temperature: 0.8,
    top_p: 0.9,
    top_k: 40,
    repeat_penalty: 1.1,
    num_predict: 256,
    num_ctx: 4096
  },

  // Ollama-specific options
  options: {
    mirostat: 0,
    mirostat_eta: 0.1,
    mirostat_tau: 5.0,
    num_gqa: null,       // For grouped query attention
    num_gpu: null,       // Layers on GPU
    num_thread: null     // CPU threads
  }
};

// Ollama generate
async function callOllama(config, prompt, system) {
  const response = await fetch(`${config.endpoint}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: config.model,
      prompt,
      system,
      options: config.parameters,
      stream: false
    })
  });

  return response.json();
}
```

## Preset Management

### Creating Model Presets

```javascript
// Preset structure
const modelPreset = {
  name: "Creative Writing",
  description: "Optimized for creative, narrative content",

  // Which providers this works with
  compatibleProviders: ["openai", "claude", "local"],

  // Shared parameters
  shared: {
    temperature: 0.95,
    top_p: 0.92,
    max_tokens: 500
  },

  // Provider-specific overrides
  overrides: {
    openai: {
      presence_penalty: 0.6,
      frequency_penalty: 0.3
    },
    claude: {
      top_k: 50
    },
    local: {
      rep_pen: 1.15,
      tfs: 0.95
    }
  }
};

// Preset manager
const presetManager = {
  presets: new Map(),

  // Add preset
  add(preset) {
    this.presets.set(preset.name, preset);
    this.save();
  },

  // Apply preset to current config
  apply(presetName, currentProvider) {
    const preset = this.presets.get(presetName);
    if (!preset) throw new Error('Preset not found');

    const settings = {
      ...preset.shared,
      ...(preset.overrides[currentProvider] || {})
    };

    return settings;
  },

  // Import/export presets
  export(presetName) {
    return JSON.stringify(this.presets.get(presetName), null, 2);
  },

  import(json) {
    const preset = JSON.parse(json);
    this.add(preset);
  }
};
```

### Common Presets

```javascript
// Built-in preset library
const builtInPresets = {
  // For roleplay and creative content
  creative: {
    name: "Creative",
    temperature: 0.9,
    top_p: 0.95,
    presence_penalty: 0.3,
    frequency_penalty: 0.3,
    max_tokens: 400
  },

  // For consistent, focused responses
  consistent: {
    name: "Consistent",
    temperature: 0.6,
    top_p: 0.85,
    presence_penalty: 0.0,
    frequency_penalty: 0.2,
    max_tokens: 300
  },

  // For technical or precise content
  precise: {
    name: "Precise",
    temperature: 0.3,
    top_p: 0.8,
    presence_penalty: 0.0,
    frequency_penalty: 0.0,
    max_tokens: 500
  },

  // For long-form content
  verbose: {
    name: "Verbose",
    temperature: 0.85,
    top_p: 0.92,
    presence_penalty: 0.4,
    frequency_penalty: 0.2,
    max_tokens: 800
  }
};
```

## Model Switching

### Quick Switch System

```javascript
// Model switcher
const modelSwitcher = {
  current: null,
  providers: new Map(),

  // Register provider
  register(name, config) {
    this.providers.set(name, {
      config,
      status: 'unknown',
      lastUsed: null
    });
  },

  // Switch to provider
  async switchTo(name) {
    const provider = this.providers.get(name);
    if (!provider) throw new Error('Provider not registered');

    // Test connection
    const healthy = await this.testConnection(name);
    if (!healthy) {
      throw new Error('Provider unavailable');
    }

    this.current = name;
    provider.lastUsed = new Date();

    return { success: true, provider: name };
  },

  // Test provider connection
  async testConnection(name) {
    const provider = this.providers.get(name);
    try {
      // Send minimal test request
      await provider.config.testFunction();
      provider.status = 'healthy';
      return true;
    } catch (error) {
      provider.status = 'unhealthy';
      provider.error = error.message;
      return false;
    }
  },

  // Get status of all providers
  getStatus() {
    const status = {};
    for (const [name, provider] of this.providers) {
      status[name] = {
        status: provider.status,
        lastUsed: provider.lastUsed,
        error: provider.error
      };
    }
    return status;
  }
};
```

### Automatic Fallback

```javascript
// Fallback system
const fallbackSystem = {
  primaryProvider: 'claude',
  fallbackOrder: ['openai', 'kobold', 'ollama'],

  // Try providers in order
  async generate(messages) {
    const allProviders = [this.primaryProvider, ...this.fallbackOrder];

    for (const providerName of allProviders) {
      try {
        const result = await this.tryProvider(providerName, messages);
        return {
          success: true,
          provider: providerName,
          response: result
        };
      } catch (error) {
        console.warn(`Provider ${providerName} failed:`, error.message);
        continue;
      }
    }

    throw new Error('All providers failed');
  },

  // Try single provider
  async tryProvider(name, messages) {
    const provider = modelSwitcher.providers.get(name);
    const timeout = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), 30000)
    );

    return Promise.race([
      provider.config.generate(messages),
      timeout
    ]);
  }
};
```

## Performance Optimization

### Model-Specific Tuning

```javascript
// Optimization profiles by model family
const optimizationProfiles = {
  // GPT-4 optimizations
  'gpt-4': {
    contextStrategy: 'full',     // Use full context window
    streamingChunkSize: 100,     // Characters per stream chunk
    retryAttempts: 3,
    timeout: 60000,

    promptOptimizations: {
      compressSystemPrompt: false,
      summarizeHistory: true,
      summaryThreshold: 50       // Summarize after N messages
    }
  },

  // Claude optimizations
  'claude': {
    contextStrategy: 'full',
    streamingChunkSize: 150,
    retryAttempts: 2,
    timeout: 90000,

    promptOptimizations: {
      useXmlTags: true,          // Claude responds well to XML
      structuredOutput: true
    }
  },

  // Local model optimizations
  'local': {
    contextStrategy: 'sliding',  // Sliding window for limited context
    streamingChunkSize: 50,
    retryAttempts: 1,
    timeout: 120000,

    promptOptimizations: {
      compressSystemPrompt: true,
      useMinimalFormatting: true,
      maxHistoryMessages: 20
    }
  }
};
```

## Summary

In this chapter, you've learned:

- **Backend Options**: Cloud APIs and local model setups
- **Provider Configuration**: Setting up OpenAI, Claude, and local models
- **Presets**: Creating and managing model presets
- **Model Switching**: Quickly switching between providers
- **Fallback Systems**: Automatic failover when providers are unavailable
- **Optimization**: Tuning settings for different model families

## Key Takeaways

1. **Diversity is strength**: Multiple providers prevent single points of failure
2. **Presets save time**: Create presets for different use cases
3. **Test connections**: Always verify providers work before relying on them
4. **Optimize per model**: Each model family has different optimal settings
5. **Local backup**: Local models provide offline capability

## Next Steps

Now that you can configure multiple models, let's explore advanced power user features in Chapter 7: Advanced Features.

---

**Ready for Chapter 7?** [Advanced Features](07-advanced-features.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `config`, `name`, `provider` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Multi-Model Setup` as an operating subsystem inside **SillyTavern Tutorial: Advanced LLM Frontend for Power Users**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model`, `parameters`, `temperature` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Multi-Model Setup` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `config`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `provider`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/SillyTavern/SillyTavern)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [Extension Directory](https://github.com/SillyTavern/SillyTavern#extensions)
  Why it matters: authoritative reference on `Extension Directory` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `config` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Extensions Ecosystem](05-extensions-ecosystem.md)
- [Next Chapter: Chapter 7: Advanced Features](07-advanced-features.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
