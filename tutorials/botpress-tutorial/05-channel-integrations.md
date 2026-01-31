---
layout: default
title: "Chapter 5: Channel Integrations"
parent: "Botpress Tutorial"
nav_order: 5
---

# Chapter 5: Channel Integrations

This chapter covers connecting your Botpress bots to various messaging platforms and channels, enabling omnichannel communication.

## 💬 Web Chat Integration

### Basic Web Chat Setup

```html
<!DOCTYPE html>
<html>
<head>
  <title>Botpress Web Chat</title>
</head>
<body>
  <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
  <script src="https://mediafiles.botpress.cloud/YOUR_BOT_ID/webchat/config.js"></script>
</body>
</html>
```

### Advanced Web Chat Configuration

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
    textColorOnPrimary: '#ffffff',
    backgroundColor: '#f8f9fa'
  },
  botName: 'Support Bot',
  avatarUrl: 'https://example.com/bot-avatar.png'
})
```

## 📱 Facebook Messenger

### Facebook App Setup

```typescript
// Configure Facebook channel
const facebookConfig = {
  appId: 'your-facebook-app-id',
  appSecret: 'your-facebook-app-secret',
  verifyToken: 'your-verify-token',
  pageAccessToken: 'your-page-access-token'
}
```

### Botpress Facebook Integration

```typescript
// In your bot configuration
export default {
  channels: {
    facebook: {
      enabled: true,
      config: facebookConfig
    }
  }
}
```

## 💬 WhatsApp Business

### WhatsApp Business API Setup

```typescript
// WhatsApp configuration
const whatsAppConfig = {
  phoneNumberId: 'your-phone-number-id',
  accessToken: 'your-access-token',
  verifyToken: 'your-verify-token',
  businessAccountId: 'your-business-account-id'
}
```

### Message Handling

```typescript
// Handle WhatsApp messages
const handleWhatsAppMessage = async (message) => {
  const { from, body, type } = message

  // Process different message types
  switch (type) {
    case 'text':
      return await processTextMessage(body)
    case 'image':
      return await processImageMessage(message)
    case 'location':
      return await processLocationMessage(message)
  }
}
```

## 💼 Slack Integration

### Slack App Configuration

```typescript
// Slack bot configuration
const slackConfig = {
  botToken: 'xoxb-your-bot-token',
  signingSecret: 'your-signing-secret',
  appToken: 'xapp-your-app-token'
}
```

### Slack Event Handling

```typescript
// Handle Slack events
const handleSlackEvent = async (event) => {
  switch (event.type) {
    case 'app_mention':
      return await handleMention(event)
    case 'message':
      return await handleMessage(event)
    case 'app_home_opened':
      return await handleHomeOpened(event)
  }
}
```

## 📧 Email Integration

### SMTP Configuration

```typescript
// Email channel setup
const emailConfig = {
  smtp: {
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
      user: 'your-email@gmail.com',
      pass: 'your-app-password'
    }
  },
  fromEmail: 'bot@yourdomain.com',
  fromName: 'Support Bot'
}
```

### Email Message Processing

```typescript
// Process incoming emails
const processEmail = async (email) => {
  const { subject, body, from } = email

  // Extract intent from email
  const intent = await classifyEmailIntent(subject, body)

  // Generate response
  const response = await generateEmailResponse(intent, email)

  // Send reply
  await sendEmailReply(from, response)
}
```

## 🌐 REST API Channel

### API Endpoint Setup

```typescript
// REST API channel
const apiChannel = {
  endpoint: '/api/bot/messages',
  methods: ['POST'],
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your-api-key'
  }
}
```

### API Message Handling

```typescript
// Handle API messages
app.post('/api/bot/messages', async (req, res) => {
  const { message, userId, conversationId } = req.body

  try {
    // Process message through Botpress
    const response = await botpress.processMessage({
      message,
      userId,
      conversationId
    })

    res.json({ response })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})
```

## 🎯 Multi-Channel Strategy

### Unified Message Format

```typescript
// Normalize messages across channels
const normalizeMessage = (channelMessage, channelType) => {
  const normalizers = {
    web: (msg) => ({ text: msg.payload.text, user: msg.user.id }),
    facebook: (msg) => ({ text: msg.message.text, user: msg.sender.id }),
    whatsapp: (msg) => ({ text: msg.body, user: msg.from }),
    slack: (msg) => ({ text: msg.text, user: msg.user })
  }

  return normalizers[channelType](channelMessage)
}
```

### Channel-Specific Responses

```typescript
// Adapt responses for different channels
const adaptResponse = (response, channelType) => {
  const adapters = {
    web: (res) => res, // No adaptation needed
    facebook: (res) => ({
      ...res,
      quick_replies: res.quick_replies?.map(qr => ({
        content_type: 'text',
        title: qr.title,
        payload: qr.payload
      }))
    }),
    whatsapp: (res) => ({
      ...res,
      // WhatsApp specific formatting
      text: res.text?.replace(/\*([^*]+)\*/g, '_$1_') // Convert *bold* to _italic_
    })
  }

  return adapters[channelType](response)
}
```

## 📊 Channel Analytics

### Message Tracking

```typescript
// Track messages across channels
class ChannelAnalytics {
  constructor() {
    this.metrics = {
      messagesByChannel: {},
      responseTimesByChannel: {},
      userSatisfactionByChannel: {}
    }
  }

  trackMessage(channel, message, responseTime) {
    // Track message count
    this.metrics.messagesByChannel[channel] =
      (this.metrics.messagesByChannel[channel] || 0) + 1

    // Track response time
    if (!this.metrics.responseTimesByChannel[channel]) {
      this.metrics.responseTimesByChannel[channel] = []
    }
    this.metrics.responseTimesByChannel[channel].push(responseTime)
  }

  getAnalytics() {
    return {
      ...this.metrics,
      averageResponseTimeByChannel: this.calculateAverages()
    }
  }
}
```

## 🔧 Channel Management

### Channel Switching

```typescript
// Allow users to switch channels
const handleChannelSwitch = async (userId, newChannel) => {
  // Get current conversation
  const conversation = await getUserConversation(userId)

  // Transfer context to new channel
  await transferConversationContext(conversation, newChannel)

  // Send welcome message in new channel
  await sendChannelMessage(newChannel, userId, {
    type: 'text',
    text: 'Welcome! You can continue our conversation here.'
  })
}
```

### Fallback Channels

```typescript
// Fallback to alternative channels
const fallbackChannels = {
  primary: 'web',
  fallback: ['email', 'sms']
}

const sendWithFallback = async (message, userId, preferredChannel) => {
  try {
    await sendMessage(preferredChannel, userId, message)
  } catch (error) {
    // Try fallback channels
    for (const channel of fallbackChannels.fallback) {
      try {
        await sendMessage(channel, userId, message)
        break
      } catch (fallbackError) {
        console.error(`Fallback to ${channel} failed:`, fallbackError)
      }
    }
  }
}
```

## 🚀 Advanced Integrations

### Custom Channel Development

```typescript
// Create custom channel integration
class CustomChannel {
  constructor(config) {
    this.config = config
    this.messageQueue = []
  }

  async sendMessage(userId, message) {
    // Implement custom sending logic
    const result = await this.customSend(userId, message)
    return result
  }

  async receiveMessage(rawMessage) {
    // Normalize incoming message
    const normalized = this.normalizeMessage(rawMessage)

    // Add to processing queue
    this.messageQueue.push(normalized)

    return normalized
  }

  normalizeMessage(rawMessage) {
    // Convert to Botpress message format
    return {
      type: 'text',
      text: rawMessage.content,
      user: rawMessage.sender,
      channel: 'custom'
    }
  }
}
```

### Channel-Specific Features

```typescript
// Utilize channel-specific features
const channelFeatures = {
  facebook: {
    sendTypingIndicator: async (userId) => {
      await facebookAPI.sendTyping(userId)
    },
    sendQuickReplies: async (userId, replies) => {
      await facebookAPI.sendQuickReplies(userId, replies)
    }
  },
  slack: {
    sendBlocks: async (channel, blocks) => {
      await slackAPI.sendBlocks(channel, blocks)
    },
    getUserInfo: async (userId) => {
      return await slackAPI.getUserInfo(userId)
    }
  }
}
```

## 📝 Chapter Summary

- ✅ Integrated web chat with custom configuration
- ✅ Connected Facebook Messenger and WhatsApp
- ✅ Set up Slack and email integrations
- ✅ Built REST API channel for custom integrations
- ✅ Implemented multi-channel message handling
- ✅ Added channel analytics and tracking
- ✅ Created custom channel integrations

**Key Takeaways:**
- Multiple channels reach users where they are
- Message normalization ensures consistent processing
- Channel-specific features enhance user experience
- Analytics help optimize channel performance
- Fallback mechanisms ensure message delivery
- Custom integrations extend platform capabilities
