---
layout: default
title: "Chapter 2: Visual Flow Builder"
parent: "Botpress Tutorial"
nav_order: 2
---

# Chapter 2: Visual Flow Builder

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
