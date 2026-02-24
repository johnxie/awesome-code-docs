---
layout: default
title: "n8n AI Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: n8n AI Tutorial
---

# Chapter 1: Getting Started with n8n AI

Welcome to **Chapter 1: Getting Started with n8n AI**. In this part of **n8n AI Tutorial: Workflow Automation with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Install n8n, create your first workflow, and add AI capabilities to your automations.

## Overview

n8n is a powerful workflow automation platform that integrates AI capabilities. This chapter covers installation, basic setup, and your first AI-powered workflow.

## Installation Options

### Docker (Recommended)

```bash
# Pull and run n8n
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_ENCRYPTION_KEY="your-encryption-key" \
  n8nio/n8n:latest

# Access at http://localhost:5678
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_ENCRYPTION_KEY=your-encryption-key-here
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped

volumes:
  n8n_data:
```

```bash
docker-compose up -d
```

### npm Installation

```bash
# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install n8n globally
npm install n8n -g

# Start n8n
n8n start
```

### Cloud Option

For quick testing, you can use n8n Cloud at https://app.n8n.cloud

## First Login

1. Open http://localhost:5678 in your browser
2. Create your admin account
3. Explore the dashboard

## Understanding the Interface

### Canvas
- **Drag & Drop**: Visual workflow builder
- **Nodes**: Individual steps in your workflow
- **Connections**: Data flow between nodes
- **Canvas Menu**: Zoom, pan, and workflow options

### Nodes Panel
- **Triggers**: Start workflows (webhooks, schedules, manual)
- **Actions**: Perform tasks (HTTP requests, database operations)
- **Transformers**: Process data (set, function, merge)
- **AI Nodes**: LLM integrations and AI tools

### Workflow Settings
- **Active/Inactive**: Control workflow execution
- **Save**: Persist your workflow
- **Execute**: Manual test runs

## Your First Workflow

### Manual Trigger → AI Chat

1. **Add Manual Trigger**
   - Drag "Manual Trigger" from the Triggers panel
   - This creates a workflow that runs when you click "Execute"

2. **Add AI Node**
   - Drag "OpenAI" node from the AI panel
   - Connect Manual Trigger to OpenAI node

3. **Configure OpenAI Node**
   - Add your OpenAI API key
   - Set model to "gpt-3.5-turbo"
   - Add prompt: "Hello! Can you tell me a joke?"

4. **Execute Workflow**
   - Click "Execute" button
   - View the AI response in the output panel

## Adding AI Capabilities

### Setting Up AI Providers

#### OpenAI Integration

```json
// OpenAI Node Configuration
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "={{ $json.input }}"
    }
  ],
  "temperature": 0.7,
  "maxTokens": 1000
}
```

#### Anthropic Claude

```json
// Anthropic Node Configuration
{
  "model": "claude-3-sonnet-20240229",
  "prompt": "Human: {{ $json.question }}\n\nAssistant:",
  "maxTokensToSample": 1000,
  "temperature": 0.7
}
```

#### Local AI with Ollama

```json
// Ollama Node Configuration
{
  "baseUrl": "http://localhost:11434",
  "model": "llama2",
  "prompt": "{{ $json.prompt }}",
  "options": {
    "temperature": 0.7,
    "num_predict": 100
  }
}
```

## Basic Workflow Patterns

### Data Flow Example

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "webhook",
        "responseMode": "responseNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "model": "gpt-3.5-turbo",
        "messages": [
          {
            "role": "system",
            "content": "Process this input and provide a structured response."
          },
          {
            "role": "user",
            "content": "={{ $json.body }}"
          }
        ]
      },
      "name": "OpenAI",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1,
      "position": [460, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      },
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [680, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "OpenAI",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "OpenAI": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### Conditional Logic

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-3.5-turbo",
        "messages": [
          {
            "role": "user",
            "content": "Analyze this text and respond with 'positive', 'negative', or 'neutral': {{ $json.text }}"
          }
        ]
      },
      "name": "Sentiment Analysis",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.choices[0].message.content }}",
              "operation": "equal",
              "value2": "positive"
            }
          ]
        }
      },
      "name": "IF Positive",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [460, 320]
    }
  ],
  "connections": {
    "Sentiment Analysis": {
      "main": [
        [
          {
            "node": "IF Positive",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Testing and Debugging

### Manual Execution

1. Click "Execute" button on any node
2. View input/output data in the panel below
3. Check execution logs in the console

### Debug Mode

```yaml
# Enable debug logging
environment:
  - DEBUG=*
  - EXECUTIONS_PROCESS=main
```

### Error Handling

```json
// Error Handler Node
{
  "parameters": {
    "mode": "merge",
    "mergeByKeys": "id",
    "options": {}
  },
  "name": "Error Handler",
  "type": "n8n-nodes-base.mergeByIndex",
  "typeVersion": 1,
  "position": [680, 400]
}
```

## API Access

### REST API

```bash
# Get workflow execution status
curl -X GET http://localhost:5678/rest/workflows/1/executions

# Execute workflow via API
curl -X POST http://localhost:5678/webhook/workflow-webhook \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from API"}'
```

### Webhook Integration

```python
import requests

# Trigger n8n workflow
response = requests.post(
    "http://localhost:5678/webhook/your-webhook-id",
    json={"data": "your payload"}
)

print(response.json())
```

## Saving and Sharing

### Export Workflows

```json
// Export workflow as JSON
{
  "meta": {
    "instanceId": "your-instance-id"
  },
  "nodes": [...],
  "connections": {...},
  "settings": {...}
}
```

### Import Workflows

1. Click "Import" in n8n UI
2. Upload JSON file or paste JSON content
3. Configure credentials and test

## Best Practices

1. **Start Simple**: Begin with basic trigger → AI → output workflows
2. **Test Frequently**: Execute workflows after each change
3. **Use Comments**: Add sticky notes to document workflow logic
4. **Organize Nodes**: Keep workflows readable with proper spacing
5. **Version Control**: Export and save workflow versions
6. **Error Handling**: Add error handlers for production workflows
7. **Credentials**: Store API keys securely in n8n credentials manager

## Next Steps

Now that you have n8n running with basic AI capabilities, let's explore different AI nodes and providers in the next chapter to build more sophisticated automations.

## Example Workflow: AI Email Responder

```json
{
  "nodes": [
    {
      "parameters": {
        "resource": "message",
        "operation": "getAll",
        "options": {
          "filter": "is:unread"
        }
      },
      "name": "Gmail",
      "type": "n8n-nodes-base.gmail",
      "credentials": {
        "gmailOAuth2": "gmail-oauth2"
      }
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful email assistant. Draft appropriate responses to emails."
          },
          {
            "role": "user",
            "content": "Subject: {{ $json.subject }}\nFrom: {{ $json.from }}\nBody: {{ $json.body }}"
          }
        ]
      },
      "name": "AI Responder",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "resource": "message",
        "operation": "reply",
        "messageId": "={{ $json.messageId }}",
        "additionalFields": {}
      },
      "name": "Reply",
      "type": "n8n-nodes-base.gmail"
    }
  ]
}
```

This basic setup gives you the foundation for building AI-powered automations. The visual interface makes it easy to experiment and iterate on your workflows.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `json`, `nodes`, `name` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with n8n AI` as an operating subsystem inside **n8n AI Tutorial: Workflow Automation with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `parameters`, `content`, `role` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with n8n AI` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `json`.
2. **Input normalization**: shape incoming data so `nodes` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `name`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/n8n-io/n8n)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `json` and `nodes` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: AI Nodes and LLM Integration](02-ai-nodes.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
