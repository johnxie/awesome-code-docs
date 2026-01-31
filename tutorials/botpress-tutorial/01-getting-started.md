---
layout: default
title: "Chapter 1: Getting Started with Botpress"
parent: "Botpress Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Botpress

Welcome to Botpress! In this chapter, we'll install Botpress, set up our development environment, and create our first chatbot.

## 🚀 Installation

### Option 1: Botpress Cloud (Recommended for beginners)

```bash
# Sign up at botpress.com
# Create your first bot from the dashboard
# Botpress Cloud provides hosting and monitoring
```

### Option 2: Local Installation with Docker

```bash
# Pull the official Docker image
docker pull botpress/server

# Run Botpress locally
docker run -p 3000:3000 -v botpress_data:/botpress/data botpress/server
```

### Option 3: Manual Installation

```bash
# Install Node.js (v16 or higher)
node --version

# Install Botpress CLI globally
npm install -g @botpress/cli

# Verify installation
bp --version
```

## ⚙️ Creating Your First Bot

### Using Botpress CLI

```bash
# Create a new bot project
bp create my-first-bot

# Navigate to project directory
cd my-first-bot

# Start development server
bp dev
```

### Project Structure

```
my-first-bot/
├── bot.config.ts          # Bot configuration
├── package.json           # Dependencies
├── src/
│   ├── actions/          # Custom actions
│   ├── hooks/            # Bot hooks
│   ├── index.ts          # Main entry point
│   └── workflows/        # Conversation workflows
├── bots/                 # Bot definitions
│   └── myFirstBot.botpress/
│       ├── config/
│       ├── flows/        # Conversation flows
│       ├── intents/      # NLP intents
│       ├── entities/     # NLP entities
│       └── qna/          # Q&A knowledge base
└── workspaces/           # Bot workspaces
```

## 🎯 Hello World Bot

Let's create a simple greeting bot:

### 1. Access Botpress Studio

```bash
# Open your browser to http://localhost:3000
# Or use Botpress Cloud dashboard
```

### 2. Create Main Flow

```typescript
// In Botpress Studio, create a new flow called "main"
// Add a trigger node for "New Conversation"
```

### 3. Add Greeting Message

```typescript
// Add a "Send Message" action
const greeting = "Hello! I'm your friendly chatbot assistant. How can I help you today?"

// Configure the message node
{
  type: "text",
  text: greeting
}
```

### 4. Test Your Bot

```bash
# In Botpress Studio, use the built-in emulator
# Type: "Hello" or "Hi"
# Expected response: "Hello! I'm your friendly chatbot assistant..."
```

## 🔧 Configuration

### Bot Configuration

```typescript
// bot.config.ts
import { BotConfig } from '@botpress/sdk'

export default {
  name: 'my-first-bot',
  version: '0.0.1',
  description: 'My first Botpress chatbot',
  languages: ['en'],
  entities: [],
  intents: []
} satisfies BotConfig
```

### Environment Variables

```bash
# .env file
BPFS_STORAGE=database
DATABASE_URL=postgresql://user:password@localhost:5432/botpress
REDIS_URL=redis://localhost:6379
BP_WEBHOOK_URL=https://your-domain.com/webhooks
```

## 📱 Web Chat Integration

### Adding Web Chat to Your Website

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Website</title>
</head>
<body>
  <h1>Welcome to My Website</h1>

  <!-- Botpress Web Chat -->
  <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
  <script src="https://mediafiles.botpress.cloud/{botId}/webchat/config.js"></script>
</body>
</html>
```

### Customizing Web Chat

```javascript
// Custom web chat configuration
window.botpressWebChat.init({
  botId: 'your-bot-id',
  hostUrl: 'https://cdn.botpress.cloud/webchat/v1',
  messagingUrl: 'https://messaging.botpress.cloud',
  clientId: 'your-client-id',
  showPoweredBy: false,
  theme: {
    primaryColor: '#007bff',
    textColorOnPrimary: '#ffffff'
  }
})
```

## 🎮 Interactive Testing

### Using the Emulator

```typescript
// Test different conversation scenarios
const testScenarios = [
  {
    input: "Hello",
    expected: "Hello! I'm your friendly chatbot assistant..."
  },
  {
    input: "Hi there",
    expected: "Hello! I'm your friendly chatbot assistant..."
  },
  {
    input: "Good morning",
    expected: "Hello! I'm your friendly chatbot assistant..."
  }
]

// Run tests in Botpress Studio emulator
```

### Conversation Flow Testing

```typescript
// Test complete conversation flows
const conversationTest = async () => {
  // Simulate user inputs
  const inputs = [
    "Hello",
    "I need help",
    "What's your name?",
    "Goodbye"
  ]

  for (const input of inputs) {
    console.log(`User: ${input}`)
    // Process through bot
    const response = await processMessage(input)
    console.log(`Bot: ${response}`)
  }
}
```

## 🔍 Understanding Botpress Concepts

### Flows vs Workflows

- **Flows**: Visual conversation diagrams in Botpress Studio
- **Workflows**: Programmatic conversation handling in code

### Nodes and Actions

```typescript
// Common node types
const nodeTypes = {
  trigger: "Starts conversation flow",
  message: "Sends message to user",
  action: "Executes custom code",
  router: "Routes to different flows",
  listen: "Waits for user input",
  end: "Ends conversation"
}
```

### Events and Hooks

```typescript
// Botpress events
const events = {
  'bp:started': 'Bot started',
  'bp:user:joined': 'User joined conversation',
  'bp:message:received': 'Message received',
  'bp:message:send': 'Message sent'
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Bot Not Responding**
   ```bash
   # Check if development server is running
   bp dev

   # Check logs
   bp logs
   ```

2. **Studio Not Loading**
   ```bash
   # Clear cache and restart
   bp kill
   bp dev --port 3000
   ```

3. **Web Chat Not Working**
   ```javascript
   // Check console for errors
   console.log('Botpress Web Chat Debug')

   // Verify bot ID and configuration
   window.botpressWebChat.init({
     botId: 'your-correct-bot-id',
     debug: true
   })
   ```

## 📊 First Bot Analytics

### Basic Metrics

```typescript
// Track basic bot interactions
const analytics = {
  totalConversations: 0,
  totalMessages: 0,
  averageResponseTime: 0,
  popularIntents: {}
}

// Log conversation start
const logConversationStart = () => {
  analytics.totalConversations++
  console.log(`Conversation #${analytics.totalConversations} started`)
}
```

## 🎯 Next Steps

In the next chapter, we'll explore the Visual Flow Builder to create more complex conversation flows with branching logic and user choice handling.

## 📝 Chapter Summary

- ✅ Installed Botpress using CLI or Docker
- ✅ Created first bot project with proper structure
- ✅ Built simple greeting bot with basic flow
- ✅ Integrated web chat into website
- ✅ Tested bot using built-in emulator
- ✅ Understood core Botpress concepts

**Key Takeaways:**
- Botpress provides both visual and code-based development
- Flows are created using drag-and-drop interface
- Web chat integration is straightforward
- Testing is built into the development environment
- Project structure organizes different bot components