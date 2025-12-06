---
layout: default
title: "n8n AI Tutorial - Chapter 2: AI Nodes"
nav_order: 2
has_children: false
parent: n8n AI Tutorial
---

# Chapter 2: AI Nodes and LLM Integration

> Configure and use different AI providers, manage credentials, and build multi-model workflows.

## AI Node Overview

n8n provides dedicated nodes for various AI providers, each with specific capabilities and configuration options.

## OpenAI Nodes

### Chat Completion Node

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant specialized in {{ $json.domain }}."
      },
      {
        "role": "user",
        "content": "={{ $json.question }}"
      }
    ],
    "temperature": 0.7,
    "maxTokens": 1000,
    "topP": 0.9,
    "frequencyPenalty": 0.0,
    "presencePenalty": 0.0,
    "responseFormat": "text"
  },
  "name": "OpenAI Chat",
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "credentials": {
    "openAiApi": "openai-api"
  }
}
```

### Embeddings Node

```json
{
  "parameters": {
    "model": "text-embedding-ada-002",
    "input": "={{ $json.texts }}",
    "encodingFormat": "float"
  },
  "name": "OpenAI Embeddings",
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "credentials": {
    "openAiApi": "openai-api"
  }
}
```

### Function Calling

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": "Check the weather in {{ $json.location }}"
      }
    ],
    "functions": [
      {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City and country"
            }
          },
          "required": ["location"]
        }
      }
    ]
  },
  "name": "OpenAI Functions",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Anthropic Claude Nodes

### Claude Chat

```json
{
  "parameters": {
    "model": "claude-3-sonnet-20240229",
    "prompt": "Human: {{ $json.question }}\n\nAssistant:",
    "maxTokensToSample": 1000,
    "temperature": 0.7,
    "topP": 0.9,
    "topK": 250
  },
  "name": "Claude Chat",
  "type": "@n8n/n8n-nodes-langchain.anthropic",
  "credentials": {
    "anthropicApi": "anthropic-api"
  }
}
```

## Local AI with Ollama

### Ollama Integration

```json
{
  "parameters": {
    "baseUrl": "http://localhost:11434",
    "model": "llama2:13b",
    "prompt": "{{ $json.prompt }}",
    "options": {
      "temperature": 0.7,
      "top_p": 0.9,
      "num_predict": 500,
      "stop": ["Human:", "\n\n"]
    }
  },
  "name": "Ollama Chat",
  "type": "@n8n/n8n-nodes-langchain.ollama",
  "typeVersion": 1
}
```

### Running Ollama Locally

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama
ollama pull mistral

# Start Ollama service
ollama serve
```

## Hugging Face Models

### Text Generation

```json
{
  "parameters": {
    "model": "gpt2",
    "inputs": "{{ $json.text }}",
    "parameters": {
      "max_new_tokens": 100,
      "temperature": 0.7,
      "do_sample": true,
      "pad_token_id": 50256
    },
    "options": {
      "use_gpu": false,
      "device": "cpu"
    }
  },
  "name": "HuggingFace Text Gen",
  "type": "@n8n/n8n-nodes-langchain.huggingFaceInference",
  "credentials": {
    "huggingFaceApi": "huggingface-api"
  }
}
```

## AI Agent Node

### Basic Agent Configuration

```json
{
  "parameters": {
    "model": "gpt-4o",
    "prompt": "You are a helpful AI assistant. Use the available tools to answer questions.\n\nAvailable tools:\n{{ $json.tools }}\n\nQuestion: {{ $json.question }}",
    "maxIterations": 5,
    "returnIntermediateSteps": false,
    "memory": "buffer",
    "tools": [
      {
        "name": "web_search",
        "description": "Search the web for information",
        "parameters": {
          "query": "string"
        }
      },
      {
        "name": "calculator",
        "description": "Perform mathematical calculations",
        "parameters": {
          "expression": "string"
        }
      }
    ]
  },
  "name": "AI Agent",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "credentials": {
    "openAiApi": "openai-api"
  }
}
```

## Vector Store Integration

### Pinecone Setup

```json
{
  "parameters": {
    "operation": "upsert",
    "pineconeIndex": "my-index",
    "items": [
      {
        "id": "={{ $json.id }}",
        "values": "={{ $json.embedding }}",
        "metadata": {
          "text": "={{ $json.text }}",
          "source": "={{ $json.source }}"
        }
      }
    ]
  },
  "name": "Pinecone Upsert",
  "type": "@n8n/n8n-nodes-langchain.pinecone",
  "credentials": {
    "pineconeApi": "pinecone-api"
  }
}
```

### Similarity Search

```json
{
  "parameters": {
    "operation": "getMany",
    "pineconeIndex": "my-index",
    "query": "={{ $json.embedding }}",
    "numberOfResults": 5,
    "includeValues": false,
    "includeMetadata": true
  },
  "name": "Pinecone Search",
  "type": "@n8n/n8n-nodes-langchain.pinecone",
  "credentials": {
    "pineconeApi": "pinecone-api"
  }
}
```

## Credential Management

### Setting Up Credentials

1. Go to Settings → Credentials in n8n UI
2. Click "Add Credential"
3. Select credential type (OpenAI, Anthropic, etc.)
4. Enter API keys and other required information
5. Test connection
6. Save credential

### Credential Types

```json
// OpenAI Credential
{
  "name": "OpenAI API",
  "type": "openAiApi",
  "data": {
    "apiKey": "sk-..."
  }
}

// Anthropic Credential
{
  "name": "Anthropic API",
  "type": "anthropicApi",
  "data": {
    "apiKey": "sk-ant-..."
  }
}

// Pinecone Credential
{
  "name": "Pinecone API",
  "type": "pineconeApi",
  "data": {
    "apiKey": "...",
    "environment": "us-east-1-aws"
  }
}
```

## Multi-Provider Workflows

### Fallback Strategy

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "={{ $json.question }}"}]
      },
      "name": "Primary AI (GPT-4)",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "continueOnFail": true
    },
    {
      "parameters": {
        "model": "claude-3-sonnet-20240229",
        "prompt": "Human: {{ $json.question }}\n\nAssistant:"
      },
      "name": "Fallback AI (Claude)",
      "type": "@n8n/n8n-nodes-langchain.anthropic"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $node['Primary AI (GPT-4)'].error }}",
              "operation": "isEmpty"
            }
          ]
        }
      },
      "name": "Check Primary Success",
      "type": "n8n-nodes-base.if"
    }
  ],
  "connections": {
    "Primary AI (GPT-4)": {
      "main": [
        [
          {
            "node": "Check Primary Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check Primary Success": {
      "main": [
        [
          {
            "node": "Fallback AI (Claude)",
            "type": "main",
            "index": 1
          }
        ]
      ]
    }
  }
}
```

### Model Selection Logic

```json
{
  "nodes": [
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "model_choice",
              "value": "={{ $json.complexity === 'high' ? 'gpt-4o' : 'gpt-3.5-turbo' }}"
            }
          ]
        }
      },
      "name": "Model Selector",
      "type": "n8n-nodes-base.set"
    },
    {
      "parameters": {
        "model": "={{ $json.model_choice }}",
        "messages": [{"role": "user", "content": "={{ $json.question }}"}]
      },
      "name": "Dynamic AI",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Custom AI Nodes

### JavaScript Code Node

```javascript
// Custom AI processing
const response = await $node.openAi.default.sendMessage({
  model: 'gpt-4o',
  messages: [
    {
      role: 'system',
      content: 'You are a data analyst. Provide insights in JSON format.'
    },
    {
      role: 'user',
      content: $input.item.json.data
    }
  ]
});

// Parse and structure response
const insights = JSON.parse(response.choices[0].message.content);

return [{
  json: {
    insights: insights,
    timestamp: new Date().toISOString(),
    model: response.model
  }
}];
```

### HTTP Request Node for Custom APIs

```json
{
  "parameters": {
    "method": "POST",
    "url": "https://api.custom-ai.com/generate",
    "sendBody": true,
    "bodyContentType": "json",
    "bodyParameters": {
      "parameters": [
        {
          "name": "prompt",
          "value": "={{ $json.prompt }}"
        },
        {
          "name": "model",
          "value": "custom-model-v1"
        }
      ]
    },
    "options": {}
  },
  "name": "Custom AI API",
  "type": "n8n-nodes-base.httpRequest"
}
```

## Rate Limiting and Cost Control

### API Rate Limiting

```json
{
  "parameters": {
    "mode": "queue",
    "batchSize": 1,
    "concurrency": 1,
    "options": {
      "reset": false
    }
  },
  "name": "Rate Limiter",
  "type": "n8n-nodes-base.splitInBatches"
}
```

### Cost Tracking

```javascript
// Track API costs
const startTime = new Date();
const response = await $node.openAi.default.sendMessage({
  model: 'gpt-4o',
  messages: $input.item.json.messages
});

const endTime = new Date();
const duration = endTime - startTime;

// Estimate cost (rough calculation)
const inputTokens = response.usage.prompt_tokens;
const outputTokens = response.usage.completion_tokens;
const estimatedCost = (inputTokens * 0.00003 + outputTokens * 0.00006);

return [{
  json: {
    response: response.choices[0].message.content,
    usage: response.usage,
    estimated_cost: estimatedCost,
    processing_time: duration,
    model: response.model
  }
}];
```

## Error Handling

### Retry Logic

```json
{
  "parameters": {
    "mode": "retry",
    "retryCount": 3,
    "retryInterval": 1000,
    "continueOnFail": true
  },
  "name": "Retry on Error",
  "type": "n8n-nodes-base.errorTrigger"
}
```

### Fallback Workflows

```json
{
  "nodes": [
    {
      "parameters": {
        "errorsToCatch": "all",
        "resume": "withDifferentBranch"
      },
      "name": "Catch Errors",
      "type": "n8n-nodes-base.errorTrigger"
    },
    {
      "parameters": {
        "model": "gpt-3.5-turbo",
        "messages": [
          {
            "role": "user",
            "content": "Simplify this request for a smaller model: {{ $json.original_question }}"
          }
        ]
      },
      "name": "Fallback Model",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Performance Optimization

### Batch Processing

```json
{
  "parameters": {
    "batchSize": 10,
    "options": {
      "merge": false
    }
  },
  "name": "Batch AI Requests",
  "type": "n8n-nodes-base.splitInBatches"
}
```

### Caching

```json
{
  "parameters": {
    "dataToSave": {
      "question": "={{ $json.question }}",
      "answer": "={{ $json.answer }}",
      "timestamp": "={{ new Date() }}"
    },
    "keys": {
      "question": "={{ $json.question }}"
    },
    "ttl": 86400
  },
  "name": "Cache Responses",
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow"
}
```

## Best Practices

1. **Credential Security**: Store API keys securely, never in workflow JSON
2. **Error Handling**: Implement comprehensive error handling and fallbacks
3. **Rate Limiting**: Respect API limits and implement queuing
4. **Cost Monitoring**: Track usage and set budget alerts
5. **Model Selection**: Choose appropriate models based on task complexity
6. **Caching**: Cache frequent queries to reduce API calls
7. **Testing**: Thoroughly test workflows before production deployment
8. **Documentation**: Document complex workflows and custom logic

These AI nodes provide powerful capabilities for building intelligent automations. The next chapter will explore document processing with AI. 