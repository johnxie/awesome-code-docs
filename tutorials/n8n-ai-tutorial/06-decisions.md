---
layout: default
title: "n8n AI Tutorial - Chapter 6: Smart Decisions"
nav_order: 6
has_children: false
parent: n8n AI Tutorial
---

# Chapter 6: AI-Powered Decision Making and Routing

Welcome to **Chapter 6: AI-Powered Decision Making and Routing**. In this part of **n8n AI Tutorial: Workflow Automation with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build intelligent workflows that make decisions, route data, and adapt based on AI analysis.

## Conditional Logic with AI

### AI-Powered Routing

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "Analyze the input and classify it. Return only: 'urgent', 'normal', or 'low_priority'."
          },
          {
            "role": "user",
            "content": "{{ $json.input_text }}"
          }
        ],
        "maxTokens": 10
      },
      "name": "Priority Classifier",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.choices[0].message.content.trim().toLowerCase() }}",
              "operation": "equal",
              "value2": "urgent"
            }
          ]
        }
      },
      "name": "Urgent Check",
      "type": "n8n-nodes-base.if"
    }
  ],
  "connections": {
    "Priority Classifier": {
      "main": [
        [
          {
            "node": "Urgent Check",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### Multi-Way Routing

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Categorize this request into: support, sales, billing, technical, or other. Return only the category name."
      },
      {
        "role": "user",
        "content": "{{ $json.customer_message }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Category Classifier",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Intelligent Switch Nodes

### Content-Based Routing

```json
{
  "parameters": {
    "routing": {
      "rules": [
        {
          "condition": "={{ $json.category === 'support' }}",
          "output": 0
        },
        {
          "condition": "={{ $json.category === 'sales' }}",
          "output": 1
        },
        {
          "condition": "={{ $json.category === 'billing' }}",
          "output": 2
        }
      ],
      "defaultOutput": 3
    }
  },
  "name": "Smart Router",
  "type": "n8n-nodes-base.switch"
}
```

## Sentiment Analysis for Decisions

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Analyze sentiment and return JSON: {\"sentiment\": \"positive|negative|neutral\", \"confidence\": 0-1, \"urgency\": \"high|medium|low\"}"
      },
      {
        "role": "user",
        "content": "Analyze: {{ $json.feedback_text }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Sentiment Analyzer",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Adaptive Workflows

### Dynamic Agent Assignment

```javascript
// Assign tasks based on AI analysis
const task = $input.item.json.task_description;
const complexity = $input.item.json.complexity_score;

let assignedAgent;
if (complexity > 0.8) {
  assignedAgent = "expert_agent";
} else if (complexity > 0.5) {
  assignedAgent = "intermediate_agent";
} else {
  assignedAgent = "basic_agent";
}

return [{
  json: {
    task: task,
    assigned_agent: assignedAgent,
    complexity: complexity,
    assignment_reason: `Complexity score ${complexity} requires ${assignedAgent}`
  }
}];
```

## Quality Gates

### Response Validation

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Check if this response is appropriate, accurate, and complete. Return JSON: {\"approved\": boolean, \"issues\": [\"list\", \"of\", \"problems\"]}"
      },
      {
        "role": "user",
        "content": "Validate: {{ $json.ai_response }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Quality Gate",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Error Handling and Recovery

### Intelligent Retry Logic

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "{{ $json.query }}"}]
      },
      "name": "AI Processor",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "continueOnFail": true
    },
    {
      "parameters": {
        "errorsToCatch": "all",
        "resume": "withDifferentBranch"
      },
      "name": "Error Detector",
      "type": "n8n-nodes-base.errorTrigger"
    },
    {
      "parameters": {
        "model": "gpt-3.5-turbo",
        "messages": [
          {
            "role": "user",
            "content": "Simplify this request and provide a basic answer: {{ $json.original_query }}"
          }
        ]
      },
      "name": "Fallback Processor",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Business Rule Engines

### AI-Enhanced Rules

```javascript
// Complex business logic with AI
const order = $input.item.json.order;
const customer = $input.item.json.customer;
const riskScore = $input.item.json.risk_score;

let decision = "approve";
let reasons = [];

if (order.amount > 10000) {
  if (customer.status !== "premium") {
    decision = "review";
    reasons.push("Large order from non-premium customer");
  }
}

if (riskScore > 0.7) {
  decision = "deny";
  reasons.push("High risk score");
}

if (order.items.some(item => item.category === "restricted")) {
  decision = "escalate";
  reasons.push("Contains restricted items");
}

return [{
  json: {
    order_id: order.id,
    decision: decision,
    reasons: reasons,
    risk_score: riskScore,
    review_required: decision !== "approve"
  }
}];
```

## Workflow Optimization

### Performance-Based Routing

```json
{
  "parameters": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Estimate processing complexity (1-10): {{ $json.task_description }}"
      }
    ]
  },
  "name": "Complexity Estimator",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Monitoring and Analytics

### Decision Tracking

```javascript
// Track AI decisions for analysis
const decisionLog = $workflow.expression.get('decision_log') || [];

decisionLog.push({
  timestamp: new Date().toISOString(),
  input: $input.item.json,
  decision: $input.item.json.decision,
  confidence: $input.item.json.confidence,
  model: $input.item.json.model_used
});

// Keep only recent decisions
if (decisionLog.length > 1000) {
  decisionLog = decisionLog.slice(-500);
}

$workflow.expression.set('decision_log', decisionLog);

return [{
  json: {
    logged: true,
    total_decisions: decisionLog.length
  }
}];
```

## Best Practices

1. **Clear Decision Criteria**: Define explicit rules for AI-powered decisions
2. **Fallback Strategies**: Always have manual override options
3. **Monitoring**: Track decision accuracy and business impact
4. **Explainability**: Log reasoning behind AI decisions
5. **Testing**: Validate decision logic with comprehensive test cases
6. **Gradual Rollout**: Start with low-risk decisions, expand gradually
7. **Human Oversight**: Include human review for critical decisions
8. **Continuous Learning**: Use decision outcomes to improve models

AI-powered decisions transform static workflows into intelligent, adaptive systems. The next chapter explores building custom AI tools and integrations.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `json`, `nodes`, `content` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: AI-Powered Decision Making and Routing` as an operating subsystem inside **n8n AI Tutorial: Workflow Automation with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `role`, `input`, `name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: AI-Powered Decision Making and Routing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `json`.
2. **Input normalization**: shape incoming data so `nodes` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `content`.
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
- [Previous Chapter: Chapter 5: Retrieval-Augmented Generation (RAG)](05-rag.md)
- [Next Chapter: Chapter 7: Building Custom AI Tools and Integrations](07-custom-tools.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
