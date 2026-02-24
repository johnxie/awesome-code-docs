---
layout: default
title: "n8n AI Tutorial - Chapter 4: AI Agents"
nav_order: 4
has_children: false
parent: n8n AI Tutorial
---

# Chapter 4: Building AI Agents with Tools

Welcome to **Chapter 4: Building AI Agents with Tools**. In this part of **n8n AI Tutorial: Workflow Automation with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Create autonomous AI agents that can use tools, make decisions, and perform complex tasks.

## AI Agent Fundamentals

AI agents in n8n can access tools, maintain memory, and make autonomous decisions to accomplish goals.

## Basic Agent Configuration

### Simple Tool-Using Agent

```json
{
  "parameters": {
    "model": "gpt-4o",
    "prompt": "You are a helpful assistant with access to tools. Use tools when needed to answer questions accurately.\n\nAvailable tools:\n{{ $json.tools }}\n\nCurrent task: {{ $json.task }}",
    "maxIterations": 3,
    "returnIntermediateSteps": true,
    "memory": "buffer",
    "tools": [
      {
        "name": "web_search",
        "description": "Search the web for current information",
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
  "name": "Basic Agent",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "credentials": {
    "openAiApi": "openai-api"
  }
}
```

## Tool Integration

### Web Search Tool

```json
{
  "parameters": {
    "url": "https://api.duckduckgo.com/",
    "method": "GET",
    "queryParameters": {
      "q": "={{ $json.query }}",
      "format": "json",
      "no_html": 1
    }
  },
  "name": "Web Search",
  "type": "n8n-nodes-base.httpRequest"
}
```

### Calculator Tool

```javascript
// Calculator tool implementation
const expression = $input.item.json.expression;

// Simple evaluation (use with caution)
let result;
try {
  // Only allow safe mathematical operations
  if (!/[^0-9+\-*/().\s]/.test(expression)) {
    result = eval(expression);
  } else {
    result = "Error: Invalid expression";
  }
} catch (error) {
  result = `Error: ${error.message}`;
}

return [{
  json: {
    expression: expression,
    result: result,
    timestamp: new Date().toISOString()
  }
}];
```

### Database Query Tool

```json
{
  "parameters": {
    "operation": "select",
    "query": "={{ $json.sql_query }}",
    "additionalFields": {}
  },
  "name": "Database Query",
  "type": "n8n-nodes-base.postgres",
  "credentials": {
    "postgres": "postgres-credentials"
  }
}
```

## Advanced Agent Patterns

### Research Agent

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "You are a research assistant. Use web search and analysis tools to gather comprehensive information.\n\nAvailable tools:\n- web_search: Search for information\n- summarize: Create summaries\n- extract_facts: Extract key facts\n\nTask: {{ $json.research_topic }}",
        "maxIterations": 5,
        "tools": [
          {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": {
              "query": "string"
            }
          },
          {
            "name": "summarize",
            "description": "Create a summary of provided text",
            "parameters": {
              "text": "string",
              "max_length": "number"
            }
          }
        ]
      },
      "name": "Research Agent",
      "type": "@n8n/n8n-nodes-langchain.agent"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "user",
            "content": "Create a comprehensive summary of this research:\n\n{{ $json.agent_response }}"
          }
        ]
      },
      "name": "Final Summary",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

### Customer Support Agent

```json
{
  "parameters": {
    "model": "gpt-4o",
    "prompt": "You are a customer support agent. Help customers with their inquiries using available tools.\n\nTools:\n- check_order_status: Check order information\n- search_kb: Search knowledge base\n- create_ticket: Create support ticket\n- send_email: Send response email\n\nCustomer inquiry: {{ $json.customer_message }}",
    "maxIterations": 4,
    "memory": "conversation",
    "tools": [
      {
        "name": "check_order_status",
        "description": "Check order status by order ID",
        "parameters": {
          "order_id": "string"
        }
      },
      {
        "name": "search_kb",
        "description": "Search knowledge base for solutions",
        "parameters": {
          "query": "string"
        }
      },
      {
        "name": "create_ticket",
        "description": "Create a support ticket",
        "parameters": {
          "issue": "string",
          "priority": "string"
        }
      }
    ]
  },
  "name": "Support Agent",
  "type": "@n8n/n8n-nodes-langchain.agent"
}
```

## Agent Memory and Context

### Conversation Memory

```json
{
  "parameters": {
    "memoryType": "conversation",
    "maxTokenLimit": 2000,
    "returnMessages": false
  },
  "name": "Conversation Memory",
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow"
}
```

### Custom Memory Management

```javascript
// Custom memory with summarization
const MAX_MEMORY_ITEMS = 10;
const memory = $workflow.expression.get('agent_memory') || [];

if ($input.item.json.new_message) {
  memory.push({
    role: 'user',
    content: $input.item.json.new_message,
    timestamp: new Date().toISOString()
  });
}

if ($input.item.json.agent_response) {
  memory.push({
    role: 'assistant',
    content: $input.item.json.agent_response,
    timestamp: new Date().toISOString()
  });
}

// Summarize if too long
if (memory.length > MAX_MEMORY_ITEMS) {
  const recentMemory = memory.slice(-MAX_MEMORY_ITEMS);
  memory.length = 0;
  memory.push(...recentMemory);
}

$workflow.expression.set('agent_memory', memory);

return [{
  json: {
    memory: memory,
    memory_length: memory.length,
    summary: memory.length > MAX_MEMORY_ITEMS ? "Memory summarized" : "Full memory"
  }
}];
```

## Multi-Agent Systems

### Agent Collaboration

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "You are a project manager. Coordinate with other agents to complete tasks.\nAvailable agents: researcher, writer, reviewer\n\nTask: {{ $json.project_task }}",
        "tools": [
          {
            "name": "delegate_to_researcher",
            "description": "Send task to research agent"
          },
          {
            "name": "delegate_to_writer",
            "description": "Send task to writing agent"
          },
          {
            "name": "delegate_to_reviewer",
            "description": "Send task to review agent"
          }
        ]
      },
      "name": "Project Manager",
      "type": "@n8n/n8n-nodes-langchain.agent"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "You are a research specialist. Gather and analyze information.\n\nTask: {{ $json.delegated_task }}",
        "maxIterations": 3
      },
      "name": "Research Agent",
      "type": "@n8n/n8n-nodes-langchain.agent"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "You are a content writer. Create engaging written content.\n\nTask: {{ $json.delegated_task }}",
        "maxIterations": 3
      },
      "name": "Writing Agent",
      "type": "@n8n/n8n-nodes-langchain.agent"
    }
  ]
}
```

### Agent Handover Logic

```json
{
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json.current_agent }}",
          "operation": "equal",
          "value2": "research_complete"
        }
      ]
    }
  },
  "name": "Handover Check",
  "type": "n8n-nodes-base.if"
}
```

## Custom Tools Development

### HTTP API Tool

```json
{
  "parameters": {
    "name": "weather_api",
    "description": "Get weather information for a city",
    "parameters": {
      "city": {
        "type": "string",
        "description": "City name"
      }
    }
  },
  "name": "Weather Tool",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.openweathermap.org/data/2.5/weather",
    "method": "GET",
    "queryParameters": {
      "q": "={{ $json.city }}",
      "appid": "={{ $credentials.openWeatherMapApi.apiKey }}",
      "units": "metric"
    }
  }
}
```

### JavaScript Custom Tool

```javascript
// Custom email analysis tool
const emailContent = $input.item.json.email_body;

// Analyze email for key information
const analysis = {
  has_questions: /\?/.test(emailContent),
  urgency_level: emailContent.toLowerCase().includes('urgent') ? 'high' :
                 emailContent.toLowerCase().includes('asap') ? 'medium' : 'low',
  sentiment: emailContent.includes('!') ? 'excited' :
             emailContent.toLowerCase().includes('problem') ? 'concerned' : 'neutral',
  category: emailContent.toLowerCase().includes('order') ? 'order' :
            emailContent.toLowerCase().includes('support') ? 'support' :
            emailContent.toLowerCase().includes('billing') ? 'billing' : 'general'
};

return [{
  json: {
    analysis: analysis,
    processed_at: new Date().toISOString(),
    email_length: emailContent.length
  }
}];
```

## Agent Orchestration

### Workflow-Based Agent Control

```json
{
  "nodes": [
    {
      "parameters": {
        "workflowId": "agent-workflow-123",
        "input": {
          "task": "={{ $json.user_request }}",
          "agent_type": "researcher"
        }
      },
      "name": "Trigger Agent Workflow",
      "type": "n8n-nodes-base.workflowTrigger"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "Based on the agent results, create a final response.\n\nAgent output: {{ $json.agent_result }}\nOriginal request: {{ $json.original_request }}",
        "maxTokens": 500
      },
      "name": "Synthesize Response",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Error Handling and Recovery

### Agent Error Recovery

```json
{
  "parameters": {
    "errorsToCatch": "all",
    "resume": "withDifferentBranch"
  },
  "name": "Agent Error Handler",
  "type": "n8n-nodes-base.errorTrigger"
}
```

### Fallback Strategies

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "prompt": "Complex task: {{ $json.task }}",
        "maxIterations": 5
      },
      "name": "Complex Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "continueOnFail": true
    },
    {
      "parameters": {
        "model": "gpt-3.5-turbo",
        "prompt": "Simplified task: {{ $json.task }}",
        "maxIterations": 2
      },
      "name": "Simple Agent Fallback",
      "type": "@n8n/n8n-nodes-langchain.agent"
    }
  ]
}
```

## Performance Optimization

### Agent Caching

```json
{
  "parameters": {
    "dataToSave": {
      "task": "={{ $json.task }}",
      "result": "={{ $json.result }}",
      "agent": "={{ $json.agent_used }}"
    },
    "keys": {
      "task_hash": "={{ $json.task_hash }}"
    },
    "ttl": 3600
  },
  "name": "Agent Cache",
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow"
}
```

### Parallel Agent Execution

```json
{
  "parameters": {
    "mode": "parallel",
    "batchSize": 3,
    "options": {
      "reset": false
    }
  },
  "name": "Parallel Agents",
  "type": "n8n-nodes-base.splitInBatches"
}
```

## Monitoring and Analytics

### Agent Performance Tracking

```javascript
// Track agent performance
const agentMetrics = $workflow.expression.get('agent_metrics') || {
  total_runs: 0,
  successful_runs: 0,
  failed_runs: 0,
  average_time: 0,
  total_time: 0
};

agentMetrics.total_runs += 1;

if ($input.item.json.success) {
  agentMetrics.successful_runs += 1;
} else {
  agentMetrics.failed_runs += 1;
}

if ($input.item.json.execution_time) {
  agentMetrics.total_time += $input.item.json.execution_time;
  agentMetrics.average_time = agentMetrics.total_time / agentMetrics.total_runs;
}

$workflow.expression.set('agent_metrics', agentMetrics);

return [{
  json: {
    metrics: agentMetrics,
    success_rate: (agentMetrics.successful_runs / agentMetrics.total_runs * 100).toFixed(2) + '%'
  }
}];
```

## Best Practices

1. **Tool Design**: Create clear, specific tools with good descriptions
2. **Memory Management**: Use appropriate memory strategies for conversation context
3. **Error Handling**: Implement fallback strategies and error recovery
4. **Performance**: Monitor and optimize agent execution times
5. **Security**: Validate tool inputs and limit agent capabilities
6. **Testing**: Thoroughly test agent workflows before production
7. **Monitoring**: Track agent performance and success rates
8. **Updates**: Regularly update agent prompts and tools

AI agents bring autonomy to n8n workflows. The next chapter explores RAG (Retrieval-Augmented Generation) for knowledge-based AI applications.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `json`, `name`, `parameters` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Building AI Agents with Tools` as an operating subsystem inside **n8n AI Tutorial: Workflow Automation with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `nodes`, `memory`, `agent` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Building AI Agents with Tools` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `json`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `parameters`.
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
- search upstream code for `json` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Document AI and Content Processing](03-document-ai.md)
- [Next Chapter: Chapter 5: Retrieval-Augmented Generation (RAG)](05-rag.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
