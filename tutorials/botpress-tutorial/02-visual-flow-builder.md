---
layout: default
title: "Chapter 2: Visual Flow Builder"
parent: "Botpress Tutorial"
nav_order: 2
---

# Chapter 2: Visual Flow Builder

Welcome to **Chapter 2: Visual Flow Builder**. In this part of **Botpress Tutorial: Open Source Conversational AI Platform**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter dives into Botpress's visual flow builder, teaching you how to design complex conversation flows with branching logic, user choices, and conditional routing.

## 🎨 Flow Builder Interface

### Accessing the Flow Builder

```bash
# Open Botpress Studio
# Navigate to your bot
# Click on "Flows" in the left sidebar
# Open "main.flow" or create a new flow
```

### Flow Canvas Overview

```
┌─────────────────────────────────────┐
│ Flow Canvas                          │
│                                     │
│  ┌─────────┐    ┌─────────┐         │
│  │ Trigger │───▶│ Message │         │
│  └─────────┘    └─────────┘         │
│                                     │
│  ┌─────────┐    ┌─────────┐         │
│  │ Choice  │───▶│ Action  │         │
│  └─────────┘    └─────────┘         │
│                                     │
└─────────────────────────────────────┘
```

## 🎯 Basic Flow Elements

### Trigger Nodes

```typescript
// Trigger types
const triggerTypes = {
  newConversation: "When user starts new conversation",
  intent: "When specific intent is detected",
  keyword: "When specific keyword is mentioned",
  event: "When custom event is triggered"
}

// Example: New conversation trigger
{
  type: "trigger",
  trigger: "newConversation",
  conditions: []
}
```

### Message Nodes

```typescript
// Text message
{
  type: "message",
  content: {
    type: "text",
    text: "Hello! How can I help you today?"
  }
}

// Image message
{
  type: "message",
  content: {
    type: "image",
    image: "https://example.com/image.jpg",
    title: "Product Image"
  }
}

// Quick replies
{
  type: "message",
  content: {
    type: "text",
    text: "What would you like to do?",
    quick_replies: [
      { title: "Get Help", payload: "help" },
      { title: "Contact Support", payload: "support" }
    ]
  }
}
```

### Action Nodes

```typescript
// Built-in actions
const builtInActions = {
  sendMessage: "Send message to user",
  callAPI: "Make HTTP request",
  setVariable: "Store value in memory",
  getUserInfo: "Get user information",
  executeCode: "Run custom JavaScript"
}

// Example: Set user variable
{
  type: "action",
  action: "setVariable",
  args: {
    name: "userName",
    value: "{{event.payload.text}}"
  }
}
```

## 🌳 Branching Logic

### Choice Nodes

```typescript
// User choice branching
{
  type: "choice",
  choices: [
    {
      condition: "{{event.payload.text}} === 'yes'",
      node: "positive_flow"
    },
    {
      condition: "{{event.payload.text}} === 'no'",
      node: "negative_flow"
    }
  ],
  fallback: "default_choice"
}
```

### Conditional Routing

```typescript
// Router node for complex conditions
{
  type: "router",
  routes: [
    {
      condition: "{{user.subscription}} === 'premium'",
      flow: "premium_support"
    },
    {
      condition: "{{user.location}} === 'US'",
      flow: "us_support"
    }
  ],
  defaultFlow: "general_support"
}
```

## 🔄 Loops and Repetition

### Loop Structures

```typescript
// Simple loop for retries
{
  type: "loop",
  maxIterations: 3,
  condition: "{{retryCount}} < 3",
  body: [
    {
      type: "message",
      content: {
        type: "text",
        text: "Please try again..."
      }
    }
  ]
}
```

### Conversation Loops

```typescript
// Keep conversation going
const conversationLoop = {
  type: "choice",
  choices: [
    {
      condition: "intent === 'continue'",
      node: "continue_conversation"
    },
    {
      condition: "intent === 'end'",
      node: "end_conversation"
    }
  ],
  fallback: "ask_for_clarification"
}
```

## 💾 Memory and Variables

### User Variables

```typescript
// Store user information
const userMemory = {
  firstName: "{{user.firstName}}",
  lastName: "{{user.lastName}}",
  preferences: "{{user.preferences}}",
  lastInteraction: "{{event.createdAt}}"
}

// Set user variable
{
  type: "action",
  action: "setUserVariable",
  args: {
    name: "preferredLanguage",
    value: "en"
  }
}
```

### Session Variables

```typescript
// Temporary session storage
const sessionVars = {
  currentTopic: "support",
  conversationState: "awaiting_response",
  retryCount: 0
}

// Update session variable
{
  type: "action",
  action: "setSessionVariable",
  args: {
    name: "retryCount",
    value: "{{retryCount}} + 1"
  }
}
```

## 🎯 Advanced Flow Patterns

### Fallback Handling

```typescript
// Handle unrecognized inputs
const fallbackFlow = {
  type: "fallback",
  actions: [
    {
      type: "message",
      content: {
        type: "text",
        text: "I'm sorry, I didn't understand that. Let me help you with our main services:"
      }
    },
    {
      type: "message",
      content: {
        type: "quick_replies",
        text: "What would you like to do?",
        quick_replies: [
          { title: "Product Info", payload: "products" },
          { title: "Support", payload: "support" },
          { title: "Contact Us", payload: "contact" }
        ]
      }
    }
  ]
}
```

### Multi-turn Conversations

```typescript
// Handle complex multi-step processes
const bookingFlow = [
  {
    step: 1,
    message: "What service would you like to book?",
    next: "service_selection"
  },
  {
    step: 2,
    message: "When would you like to schedule it?",
    next: "date_selection"
  },
  {
    step: 3,
    message: "Please confirm your booking details:",
    next: "confirmation"
  }
]
```

## 🎨 Visual Design Best Practices

### Flow Organization

```typescript
// Organize flows logically
const flowStructure = {
  main: {
    purpose: "Entry point and routing",
    nodes: ["greeting", "main_menu", "router"]
  },
  support: {
    purpose: "Customer support flow",
    nodes: ["issue_type", "escalation", "resolution"]
  },
  booking: {
    purpose: "Appointment booking",
    nodes: ["service_select", "time_select", "confirm"]
  }
}
```

### Node Naming Conventions

```typescript
// Consistent naming
const namingConvention = {
  triggers: "trigger_*",
  messages: "msg_*",
  actions: "action_*",
  choices: "choice_*",
  routers: "router_*"
}

// Examples
const nodeNames = {
  "trigger_new_conversation": "New conversation trigger",
  "msg_welcome": "Welcome message",
  "action_set_user": "Set user information",
  "choice_main_menu": "Main menu selection",
  "router_department": "Department routing"
}
```

## 🔧 Flow Testing and Debugging

### Flow Validation

```typescript
// Validate flow structure
const validateFlow = (flow) => {
  const errors = []

  // Check for orphaned nodes
  const connectedNodes = new Set()
  flow.nodes.forEach(node => {
    node.connections?.forEach(conn => {
      connectedNodes.add(conn.target)
    })
  })

  flow.nodes.forEach(node => {
    if (!connectedNodes.has(node.id) && node.type !== 'trigger') {
      errors.push(`Orphaned node: ${node.id}`)
    }
  })

  return errors
}
```

### Test Scenarios

```typescript
// Define test cases
const testScenarios = [
  {
    name: "New User Flow",
    steps: [
      { input: "Hello", expected: "Welcome message" },
      { input: "I need help", expected: "Support options" }
    ]
  },
  {
    name: "Booking Flow",
    steps: [
      { input: "Book appointment", expected: "Service selection" },
      { input: "Consultation", expected: "Time selection" }
    ]
  }
]
```

## 📊 Flow Analytics

### Performance Metrics

```typescript
// Track flow performance
const flowMetrics = {
  totalExecutions: 0,
  averageCompletionTime: 0,
  dropOffPoints: {},
  popularPaths: {}
}

// Track flow execution
const trackFlowExecution = (flowId, userId, startTime) => {
  const duration = Date.now() - startTime
  flowMetrics.totalExecutions++
  flowMetrics.averageCompletionTime =
    (flowMetrics.averageCompletionTime + duration) / 2
}
```

## 🚀 Advanced Features

### Subflows and Reusability

```typescript
// Create reusable subflows
const commonFlows = {
  authentication: {
    nodes: ["login_prompt", "credential_check", "success"],
    reusable: true
  },
  error_handling: {
    nodes: ["error_message", "retry_option", "escalation"],
    reusable: true
  }
}

// Use subflow in main flow
{
  type: "subflow",
  flowId: "authentication",
  input: { userType: "customer" }
}
```

### Dynamic Flow Generation

```typescript
// Generate flows programmatically
const generateDynamicFlow = (userType) => {
  const flow = {
    nodes: [],
    connections: []
  }

  if (userType === 'premium') {
    flow.nodes.push({
      id: 'premium_options',
      type: 'message',
      content: 'Premium features available...'
    })
  }

  return flow
}
```

## 📝 Chapter Summary

- ✅ Mastered visual flow builder interface
- ✅ Created complex branching logic with choice nodes
- ✅ Implemented loops and conditional routing
- ✅ Managed user and session variables
- ✅ Designed multi-turn conversation flows
- ✅ Applied visual design best practices
- ✅ Tested and debugged flow logic

**Key Takeaways:**
- Visual flows make conversation design intuitive
- Branching logic handles different user paths
- Variables store conversation state and user data
- Testing ensures flows work as expected
- Organization and naming conventions improve maintainability
- Subflows enable reusable conversation components

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `flow`, `message`, `user` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Visual Flow Builder` as an operating subsystem inside **Botpress Tutorial: Open Source Conversational AI Platform**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `text`, `node`, `nodes` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Visual Flow Builder` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `flow`.
2. **Input normalization**: shape incoming data so `message` receives stable contracts.
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
- search upstream code for `flow` and `message` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Botpress](01-getting-started.md)
- [Next Chapter: Chapter 3: Natural Language Understanding](03-natural-language-understanding.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
