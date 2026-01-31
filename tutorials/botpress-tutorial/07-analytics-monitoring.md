---
layout: default
title: "Chapter 7: Analytics & Monitoring"
parent: "Botpress Tutorial"
nav_order: 7
---

# Chapter 7: Analytics & Monitoring

This chapter covers analytics, monitoring, and performance tracking for Botpress bots to ensure optimal operation and continuous improvement.

## 📊 Built-in Analytics

### Basic Metrics

```typescript
// Access built-in analytics
const getBotAnalytics = async (botId, timeRange) => {
  const analytics = await botpress.getAnalytics(botId, {
    startDate: timeRange.start,
    endDate: timeRange.end,
    metrics: [
      'messages_sent',
      'messages_received',
      'unique_users',
      'average_response_time'
    ]
  })

  return analytics
}

// Key metrics to track
const essentialMetrics = {
  totalMessages: 'Total messages processed',
  uniqueUsers: 'Unique users interacted',
  averageSessionLength: 'Average conversation length',
  fallbackRate: 'Rate of fallback responses',
  userSatisfaction: 'User satisfaction score'
}
```

### Conversation Analytics

```typescript
// Analyze conversation patterns
const analyzeConversations = async (conversations) => {
  const analysis = {
    totalConversations: conversations.length,
    averageMessagesPerConversation: 0,
    topIntents: {},
    conversationLengths: [],
    completionRate: 0
  }

  conversations.forEach(conv => {
    analysis.averageMessagesPerConversation += conv.messages.length
    analysis.conversationLengths.push(conv.messages.length)

    // Track intents
    conv.messages.forEach(msg => {
      if (msg.intent) {
        analysis.topIntents[msg.intent] = (analysis.topIntents[msg.intent] || 0) + 1
      }
    })

    // Check completion
    if (conv.completed) {
      analysis.completionRate++
    }
  })

  analysis.averageMessagesPerConversation /= conversations.length
  analysis.completionRate /= conversations.length

  return analysis
}
```

## 📈 Custom Analytics

### Message Tracking

```typescript
// Custom message analytics
class MessageAnalytics {
  constructor() {
    this.messages = []
    this.metrics = {
      totalSent: 0,
      totalReceived: 0,
      averageResponseTime: 0,
      messagesByHour: new Array(24).fill(0),
      messagesByDay: new Array(7).fill(0)
    }
  }

  trackMessage(message, type = 'received') {
    const timestamp = new Date(message.timestamp)
    const hour = timestamp.getHours()
    const day = timestamp.getDay()

    this.messages.push({
      ...message,
      type,
      timestamp
    })

    if (type === 'sent') {
      this.metrics.totalSent++
    } else {
      this.metrics.totalReceived++
    }

    this.metrics.messagesByHour[hour]++
    this.metrics.messagesByDay[day]++
  }

  getMetrics() {
    return {
      ...this.metrics,
      messagesByHour: this.metrics.messagesByHour,
      messagesByDay: this.metrics.messagesByDay.map((count, index) => ({
        day: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][index],
        count
      }))
    }
  }
}
```

### User Behavior Analytics

```typescript
// Track user behavior patterns
const userBehaviorAnalytics = {
  trackUserJourney: (userId, events) => {
    // Analyze user journey through bot
    const journey = {
      userId,
      startTime: events[0]?.timestamp,
      endTime: events[events.length - 1]?.timestamp,
      events: events.length,
      intents: {},
      channels: new Set(),
      completionRate: 0
    }

    events.forEach(event => {
      journey.channels.add(event.channel)
      if (event.intent) {
        journey.intents[event.intent] = (journey.intents[event.intent] || 0) + 1
      }
    })

    return journey
  },

  calculateEngagement: (userJourneys) => {
    return userJourneys.map(journey => ({
      ...journey,
      engagementScore: calculateEngagementScore(journey),
      sessionDuration: journey.endTime - journey.startTime
    }))
  }
}
```

## 🔍 Monitoring Setup

### Health Checks

```typescript
// Comprehensive health monitoring
const healthMonitor = {
  checks: {
    database: async () => {
      try {
        await db.query('SELECT 1')
        return { status: 'healthy', responseTime: Date.now() }
      } catch (error) {
        return { status: 'unhealthy', error: error.message }
      }
    },

    nlu: async () => {
      try {
        const result = await nlu.predict('hello')
        return { status: 'healthy', confidence: result.confidence }
      } catch (error) {
        return { status: 'unhealthy', error: error.message }
      }
    },

    channels: async () => {
      const channelStatuses = {}
      for (const channel of ['web', 'facebook', 'slack']) {
        try {
          await testChannelConnection(channel)
          channelStatuses[channel] = 'healthy'
        } catch (error) {
          channelStatuses[channel] = 'unhealthy'
        }
      }
      return channelStatuses
    }
  },

  runHealthChecks: async () => {
    const results = {}
    for (const [name, check] of Object.entries(this.checks)) {
      results[name] = await check()
    }
    return results
  }
}
```

### Performance Monitoring

```typescript
// Performance metrics collection
class PerformanceMonitor {
  constructor() {
    this.metrics = {
      responseTimes: [],
      memoryUsage: [],
      cpuUsage: [],
      errorRates: []
    }
    this.startTime = Date.now()
  }

  trackResponseTime(startTime) {
    const responseTime = Date.now() - startTime
    this.metrics.responseTimes.push(responseTime)

    // Keep only last 1000 measurements
    if (this.metrics.responseTimes.length > 1000) {
      this.metrics.responseTimes.shift()
    }
  }

  trackSystemMetrics() {
    const memUsage = process.memoryUsage()
    const cpuUsage = process.cpuUsage()

    this.metrics.memoryUsage.push(memUsage)
    this.metrics.cpuUsage.push(cpuUsage)

    // Keep only last 100 measurements
    if (this.metrics.memoryUsage.length > 100) {
      this.metrics.memoryUsage.shift()
      this.metrics.cpuUsage.shift()
    }
  }

  getPerformanceReport() {
    const responseTimes = this.metrics.responseTimes
    const avgResponseTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length

    return {
      averageResponseTime: avgResponseTime,
      p95ResponseTime: this.calculatePercentile(responseTimes, 95),
      memoryUsage: this.getLatestMemoryUsage(),
      uptime: Date.now() - this.startTime
    }
  }

  calculatePercentile(arr, percentile) {
    const sorted = arr.sort((a, b) => a - b)
    const index = (percentile / 100) * (sorted.length - 1)
    return sorted[Math.floor(index)]
  }

  getLatestMemoryUsage() {
    const latest = this.metrics.memoryUsage[this.metrics.memoryUsage.length - 1]
    return latest ? {
      rss: Math.round(latest.rss / 1024 / 1024), // MB
      heapUsed: Math.round(latest.heapUsed / 1024 / 1024), // MB
      heapTotal: Math.round(latest.heapTotal / 1024 / 1024) // MB
    } : null
  }
}
```

## 📊 Dashboard Creation

### Real-time Dashboard

```typescript
// Create monitoring dashboard
const createMonitoringDashboard = () => {
  const dashboard = {
    widgets: [
      {
        type: 'metric',
        title: 'Active Users',
        data: () => analytics.getActiveUsers()
      },
      {
        type: 'chart',
        title: 'Messages Over Time',
        data: () => analytics.getMessagesOverTime()
      },
      {
        type: 'gauge',
        title: 'System Health',
        data: () => healthMonitor.runHealthChecks()
      },
      {
        type: 'table',
        title: 'Top Intents',
        data: () => analytics.getTopIntents()
      }
    ],

    refresh: async () => {
      const data = {}
      for (const widget of dashboard.widgets) {
        data[widget.title] = await widget.data()
      }
      return data
    }
  }

  return dashboard
}
```

### Alert System

```typescript
// Alert configuration and monitoring
const alertSystem = {
  thresholds: {
    responseTime: 5000, // 5 seconds
    errorRate: 0.05,    // 5%
    memoryUsage: 0.8    // 80%
  },

  alerts: [],

  checkThresholds: (metrics) => {
    const newAlerts = []

    if (metrics.averageResponseTime > this.thresholds.responseTime) {
      newAlerts.push({
        type: 'warning',
        message: 'High response time detected',
        value: metrics.averageResponseTime
      })
    }

    if (metrics.errorRate > this.thresholds.errorRate) {
      newAlerts.push({
        type: 'error',
        message: 'High error rate detected',
        value: metrics.errorRate
      })
    }

    this.alerts.push(...newAlerts)
    return newAlerts
  },

  getActiveAlerts: () => {
    return this.alerts.filter(alert => alert.active !== false)
  }
}
```

## 📈 A/B Testing

### Experiment Setup

```typescript
// A/B testing for bot improvements
class ABTesting {
  constructor() {
    this.experiments = {}
    this.results = {}
  }

  createExperiment(name, variants, distribution = [0.5, 0.5]) {
    this.experiments[name] = {
      variants,
      distribution,
      participants: new Map()
    }
  }

  assignVariant(experimentName, userId) {
    const experiment = this.experiments[experimentName]
    if (!experiment) return null

    // Simple hash-based assignment for consistency
    const hash = this.hashString(userId)
    const normalizedHash = hash / Number.MAX_SAFE_INTEGER
    let cumulative = 0

    for (let i = 0; i < experiment.distribution.length; i++) {
      cumulative += experiment.distribution[i]
      if (normalizedHash <= cumulative) {
        experiment.participants.set(userId, i)
        return experiment.variants[i]
      }
    }

    return experiment.variants[0]
  }

  trackResult(experimentName, userId, metric, value) {
    const experiment = this.experiments[experimentName]
    if (!experiment) return

    const variantIndex = experiment.participants.get(userId)
    if (variantIndex === undefined) return

    const variant = experiment.variants[variantIndex]
    if (!this.results[experimentName]) {
      this.results[experimentName] = {}
    }
    if (!this.results[experimentName][variant]) {
      this.results[experimentName][variant] = {}
    }

    this.results[experimentName][variant][metric] = value
  }

  hashString(str) {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash // Convert to 32-bit integer
    }
    return Math.abs(hash)
  }
}
```

## 🔧 Logging Configuration

### Structured Logging

```typescript
// Advanced logging setup
const logger = {
  levels: {
    ERROR: 0,
    WARN: 1,
    INFO: 2,
    DEBUG: 3
  },

  currentLevel: 2,

  log: (level, message, meta = {}) => {
    if (level > this.currentLevel) return

    const logEntry = {
      timestamp: new Date().toISOString(),
      level: Object.keys(this.levels)[level],
      message,
      ...meta
    }

    console.log(JSON.stringify(logEntry))

    // Send to external logging service
    if (process.env.LOGGING_SERVICE_URL) {
      this.sendToExternalService(logEntry)
    }
  },

  error: (message, error, meta = {}) => {
    this.log(this.levels.ERROR, message, {
      ...meta,
      error: {
        message: error.message,
        stack: error.stack
      }
    })
  },

  info: (message, meta = {}) => {
    this.log(this.levels.INFO, message, meta)
  },

  debug: (message, meta = {}) => {
    this.log(this.levels.DEBUG, message, meta)
  }
}
```

## 📝 Chapter Summary

- ✅ Set up comprehensive analytics tracking
- ✅ Implemented health monitoring systems
- ✅ Created performance monitoring dashboard
- ✅ Built alert system for issue detection
- ✅ Configured A/B testing framework
- ✅ Established structured logging

**Key Takeaways:**
- Analytics provide insights for optimization
- Monitoring ensures system reliability
- Performance tracking identifies bottlenecks
- Alerts enable proactive issue resolution
- A/B testing validates improvements
- Structured logging aids debugging
