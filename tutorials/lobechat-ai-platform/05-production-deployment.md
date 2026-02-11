---
layout: default
title: "Chapter 5: Production Deployment"
nav_order: 5
has_children: false
parent: "LobeChat AI Platform"
---

# Chapter 5: Production Deployment

> Scaling, monitoring, and maintaining LobeChat applications in production

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- Deploying LobeChat with Docker and Kubernetes
- Implementing monitoring and observability
- Setting up CI/CD pipelines
- Performance optimization and caching
- Security hardening and compliance

## 🐳 Docker Deployment

### **Production Docker Setup**

```dockerfile
# Dockerfile for production LobeChat deployment
FROM node:18-alpine AS base

# Install dependencies for native compilation
RUN apk add --no-cache python3 make g++ sqlite-dev

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile --production=false

# Copy source code
COPY . .

# Build application
RUN yarn build

# Production stage
FROM node:18-alpine AS production

# Install production runtime dependencies
RUN apk add --no-cache sqlite python3 curl

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 nodejs && \
    adduser -S lobe -u 1001

# Copy built application
COPY --from=base /app/.next ./.next
COPY --from=base /app/public ./public
COPY --from=base /app/package*.json ./
COPY --from=base /app/yarn.lock ./
COPY --from=base /app/next.config.js ./

# Install production dependencies only
RUN yarn install --frozen-lockfile --production=true && \
    yarn cache clean

# Create data directories
RUN mkdir -p /app/data && \
    chown -R lobe:nodejs /app

USER lobe

# Expose port
EXPOSE 3210

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3210/api/health || exit 1

# Start application
CMD ["yarn", "start"]
```

### **Docker Compose Configuration**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  lobe-chat:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3210:3210"
    environment:
      - NODE_ENV=production
      - NEXTAUTH_URL=https://your-domain.com
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://lobe:password@postgres:5432/lobe_chat
      - REDIS_URL=redis://redis:6379
      - S3_ACCESS_KEY=${S3_ACCESS_KEY}
      - S3_SECRET_KEY=${S3_SECRET_KEY}
      - S3_BUCKET=${S3_BUCKET}
      - S3_ENDPOINT=${S3_ENDPOINT}
    depends_on:
      - postgres
      - redis
    volumes:
      - lobe_data:/app/data
    restart: unless-stopped
    networks:
      - lobe_network

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=lobe_chat
      - POSTGRES_USER=lobe
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
    networks:
      - lobe_network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - lobe_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl/certs:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - lobe-chat
    networks:
      - lobe_network
    restart: unless-stopped

volumes:
  lobe_data:
  postgres_data:
  redis_data:
  nginx_logs:

networks:
  lobe_network:
    driver: bridge
```

## ☸️ Kubernetes Deployment

### **Kubernetes Manifests**

```yaml
# lobe-chat-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lobe-chat
  namespace: lobe-chat-prod
  labels:
    app: lobe-chat
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lobe-chat
  template:
    metadata:
      labels:
        app: lobe-chat
    spec:
      containers:
      - name: lobe-chat
        image: your-registry/lobe-chat:latest
        ports:
        - containerPort: 3210
        env:
        - name: NODE_ENV
          value: "production"
        - name: NEXTAUTH_URL
          value: "https://your-domain.com"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: lobe-chat-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: lobe-chat-secrets
              key: redis-url
        - name: NEXTAUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: lobe-chat-secrets
              key: nextauth-secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3210
            httpHeaders:
            - name: User-Agent
              value: Kubernetes-Liveness-Probe
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3210
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
        volumeMounts:
        - name: lobe-storage
          mountPath: /app/data
      volumes:
      - name: lobe-storage
        persistentVolumeClaim:
          claimName: lobe-chat-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: lobe-chat-service
  namespace: lobe-chat-prod
spec:
  selector:
    app: lobe-chat
  ports:
  - port: 3210
    targetPort: 3210
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: lobe-chat-ingress
  namespace: lobe-chat-prod
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - your-lobe-chat-domain.com
    secretName: lobe-chat-tls
  rules:
  - host: your-lobe-chat-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: lobe-chat-service
            port:
              number: 3210
```

### **Horizontal Pod Autoscaling**

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: lobe-chat-hpa
  namespace: lobe-chat-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: lobe-chat
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: 50
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
```

## 📊 Monitoring and Observability

### **Prometheus Metrics**

```typescript
// metrics/monitoring.ts
import promClient from 'prom-client';

// Create registry
export const register = new promClient.Registry();

// Add default metrics
promClient.collectDefaultMetrics({ register });

// Custom metrics
export const httpRequestDuration = new promClient.Histogram({
  name: 'lobe_http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5, 10]
});

export const chatRequestsTotal = new promClient.Counter({
  name: 'lobe_chat_requests_total',
  help: 'Total number of chat requests',
  labelNames: ['provider', 'model', 'status']
});

export const streamingConnections = new promClient.Gauge({
  name: 'lobe_streaming_connections_active',
  help: 'Number of active streaming connections'
});

export const messageTokensTotal = new promClient.Counter({
  name: 'lobe_message_tokens_total',
  help: 'Total number of tokens processed',
  labelNames: ['type', 'provider']
});

export const userSessionsActive = new promClient.Gauge({
  name: 'lobe_user_sessions_active',
  help: 'Number of active user sessions'
});

export const databaseQueryDuration = new promClient.Histogram({
  name: 'lobe_database_query_duration_seconds',
  help: 'Duration of database queries',
  labelNames: ['operation', 'table'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
});

// Middleware for collecting metrics
export function metricsMiddleware(req: any, res: any, next: any) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;

    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });

  next();
}

// Chat metrics collector
export class ChatMetricsCollector {
  recordChatRequest(provider: string, model: string, status: 'success' | 'error') {
    chatRequestsTotal.inc({ provider, model, status });
  }

  recordTokenUsage(type: 'input' | 'output', provider: string, tokens: number) {
    messageTokensTotal.inc({ type, provider }, tokens);
  }

  updateStreamingConnections(count: number) {
    streamingConnections.set(count);
  }

  updateActiveSessions(count: number) {
    userSessionsActive.set(count);
  }

  recordDatabaseQuery(operation: string, table: string, duration: number) {
    databaseQueryDuration
      .labels(operation, table)
      .observe(duration);
  }
}
```

### **Grafana Dashboards**

```json
// grafana-dashboard.json
{
  "dashboard": {
    "title": "LobeChat Production Monitoring",
    "tags": ["lobechat", "ai", "chat"],
    "timezone": "browser",
    "panels": [
      {
        "title": "HTTP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(lobe_http_request_duration_seconds_count[5m])",
            "legendFormat": "{{method}} {{route}}"
          }
        ]
      },
      {
        "title": "Chat Request Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(lobe_chat_requests_total{status='success'}[5m]) / rate(lobe_chat_requests_total[5m]) * 100",
            "legendFormat": "Success Rate %"
          }
        ]
      },
      {
        "title": "Token Usage by Provider",
        "type": "barchart",
        "targets": [
          {
            "expr": "rate(lobe_message_tokens_total[5m])",
            "legendFormat": "{{provider}} - {{type}}"
          }
        ]
      },
      {
        "title": "Active Streaming Connections",
        "type": "gauge",
        "targets": [
          {
            "expr": "lobe_streaming_connections_active",
            "legendFormat": "Active Connections"
          }
        ]
      },
      {
        "title": "Database Query Performance",
        "type": "heatmap",
        "targets": [
          {
            "expr": "lobe_database_query_duration_seconds",
            "legendFormat": "{{operation}} on {{table}}"
          }
        ]
      },
      {
        "title": "System Resources",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage %"
          },
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "legendFormat": "Memory Usage %"
          }
        ]
      }
    ]
  }
}
```

## 🔄 CI/CD Pipeline

### **GitHub Actions Workflow**

```yaml
# .github/workflows/deploy.yml
name: Deploy LobeChat to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'yarn'

      - name: Install dependencies
        run: yarn install --frozen-lockfile

      - name: Run linting
        run: yarn lint

      - name: Run type checking
        run: yarn type-check

      - name: Run tests
        run: yarn test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'yarn'

      - name: Install dependencies
        run: yarn install --frozen-lockfile

      - name: Build application
        run: yarn build

      - name: Build Docker image
        run: |
          docker build -t lobe-chat:${{ github.sha }} .
          docker tag lobe-chat:${{ github.sha }} lobe-chat:latest

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin your-registry.com
          docker tag lobe-chat:${{ github.sha }} your-registry.com/lobe-chat:${{ github.sha }}
          docker push your-registry.com/lobe-chat:${{ github.sha }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/lobe-chat lobe-chat=your-registry.com/lobe-chat:${{ github.sha }} --namespace=lobe-chat-staging
          kubectl rollout status deployment/lobe-chat --namespace=lobe-chat-staging

      - name: Run integration tests
        run: |
          # Wait for deployment
          kubectl wait --for=condition=available --timeout=300s deployment/lobe-chat -n lobe-chat-staging

          # Run tests against staging
          npm run test:e2e -- --url=https://staging.your-domain.com

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/lobe-chat lobe-chat=your-registry.com/lobe-chat:${{ github.sha }} --namespace=lobe-chat-prod
          kubectl rollout status deployment/lobe-chat --namespace=lobe-chat-prod

      - name: Run smoke tests
        run: |
          # Wait for deployment
          kubectl wait --for=condition=available --timeout=300s deployment/lobe-chat -n lobe-chat-prod

          # Run smoke tests
          npm run test:smoke -- --url=https://your-domain.com

      - name: Notify deployment
        run: |
          curl -X POST -H 'Content-type: application/json' \
            --data '{"text":"LobeChat deployed to production successfully 🚀"}' \
            ${{ secrets.SLACK_WEBHOOK }}
```

## ⚡ Performance Optimization

### **Caching Strategy**

```typescript
// Multi-level caching system
class CacheManager {
  private memoryCache: Map<string, CacheEntry> = new Map();
  private redisClient: any;
  private maxMemorySize: number = 100 * 1024 * 1024; // 100MB
  private currentMemorySize: number = 0;

  constructor(redisUrl?: string) {
    if (redisUrl) {
      // Initialize Redis client
      this.redisClient = require('redis').createClient({ url: redisUrl });
      this.redisClient.connect();
    }
  }

  async get<T>(key: string, fetchFunction?: () => Promise<T>, ttl: number = 300): Promise<T | null> {
    // Check memory cache first
    const memoryEntry = this.memoryCache.get(key);
    if (memoryEntry && !this.isExpired(memoryEntry)) {
      return memoryEntry.data as T;
    }

    // Check Redis cache
    if (this.redisClient) {
      try {
        const redisData = await this.redisClient.get(key);
        if (redisData) {
          const parsed = JSON.parse(redisData);
          // Populate memory cache
          this.setMemoryCache(key, parsed, ttl);
          return parsed as T;
        }
      } catch (error) {
        console.warn('Redis cache error:', error);
      }
    }

    // Fetch from source
    if (fetchFunction) {
      const data = await fetchFunction();
      await this.set(key, data, ttl);
      return data;
    }

    return null;
  }

  async set(key: string, data: any, ttl: number = 300): Promise<void> {
    // Set in memory cache
    this.setMemoryCache(key, data, ttl);

    // Set in Redis cache
    if (this.redisClient) {
      try {
        await this.redisClient.setEx(key, ttl, JSON.stringify(data));
      } catch (error) {
        console.warn('Redis cache set error:', error);
      }
    }
  }

  private setMemoryCache(key: string, data: any, ttl: number): void {
    const entry: CacheEntry = {
      data,
      expiry: Date.now() + (ttl * 1000),
      size: this.calculateSize(data)
    };

    // Check if we need to evict entries
    if (this.currentMemorySize + entry.size > this.maxMemorySize) {
      this.evictExpiredEntries();
      this.evictLRU();
    }

    // Remove old entry if exists
    const oldEntry = this.memoryCache.get(key);
    if (oldEntry) {
      this.currentMemorySize -= oldEntry.size;
    }

    this.memoryCache.set(key, entry);
    this.currentMemorySize += entry.size;
  }

  private isExpired(entry: CacheEntry): boolean {
    return Date.now() > entry.expiry;
  }

  private calculateSize(data: any): number {
    return JSON.stringify(data).length * 2; // Rough estimation
  }

  private evictExpiredEntries(): void {
    const now = Date.now();
    for (const [key, entry] of this.memoryCache) {
      if (now > entry.expiry) {
        this.memoryCache.delete(key);
        this.currentMemorySize -= entry.size;
      }
    }
  }

  private evictLRU(): void {
    // Simple LRU eviction - remove oldest entries
    const entries = Array.from(this.memoryCache.entries())
      .sort(([, a], [, b]) => a.expiry - b.expiry);

    let freedSpace = 0;
    const targetFreeSpace = this.maxMemorySize * 0.2; // Free 20%

    for (const [key, entry] of entries) {
      if (freedSpace >= targetFreeSpace) break;

      this.memoryCache.delete(key);
      this.currentMemorySize -= entry.size;
      freedSpace += entry.size;
    }
  }

  async invalidate(pattern: string = '*'): Promise<void> {
    // Clear memory cache
    this.memoryCache.clear();
    this.currentMemorySize = 0;

    // Clear Redis cache
    if (this.redisClient) {
      try {
        const keys = await this.redisClient.keys(pattern);
        if (keys.length > 0) {
          await this.redisClient.del(keys);
        }
      } catch (error) {
        console.warn('Redis cache invalidation error:', error);
      }
    }
  }

  // Application-specific caching methods
  async cacheChatResponse(sessionId: string, messages: Message[], response: string): Promise<void> {
    const key = `chat:${sessionId}:${this.hashMessages(messages)}`;
    await this.set(key, response, 1800); // 30 minutes
  }

  async getCachedChatResponse(sessionId: string, messages: Message[]): Promise<string | null> {
    const key = `chat:${sessionId}:${this.hashMessages(messages)}`;
    return await this.get(key);
  }

  private hashMessages(messages: Message[]): string {
    const content = messages.map(m => m.content).join('');
    const crypto = require('crypto');
    return crypto.createHash('md5').update(content).digest('hex');
  }

  getStats(): CacheStats {
    return {
      memoryEntries: this.memoryCache.size,
      memorySize: this.currentMemorySize,
      maxMemorySize: this.maxMemorySize,
      memoryUtilization: (this.currentMemorySize / this.maxMemorySize) * 100
    };
  }
}

interface CacheEntry {
  data: any;
  expiry: number;
  size: number;
}

interface CacheStats {
  memoryEntries: number;
  memorySize: number;
  maxMemorySize: number;
  memoryUtilization: number;
}
```

## 🔐 Security and Compliance

### **Authentication and Authorization**

```typescript
// NextAuth.js configuration for production
export const NextAuthConfig = {
  providers: [
    // OAuth providers
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
    // Add more providers as needed
  ],

  session: {
    strategy: 'jwt',
    maxAge: 24 * 60 * 60, // 24 hours
  },

  jwt: {
    secret: process.env.NEXTAUTH_SECRET,
    encryption: true,
  },

  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },

  callbacks: {
    async jwt({ token, user, account }) {
      // Add custom claims to JWT
      if (user) {
        token.role = user.role;
        token.plan = user.plan;
      }
      return token;
    },

    async session({ session, token }) {
      // Add custom properties to session
      session.user.role = token.role;
      session.user.plan = token.plan;
      return session;
    },

    async signIn({ user, account, profile }) {
      // Custom sign-in logic
      if (account?.provider === 'google') {
        // Check if user is allowed to sign in
        const allowedDomains = process.env.ALLOWED_EMAIL_DOMAINS?.split(',') || [];
        const userDomain = user.email?.split('@')[1];

        if (allowedDomains.length > 0 && !allowedDomains.includes(userDomain!)) {
          return false;
        }
      }

      return true;
    },
  },

  events: {
    async signIn({ user, account, isNewUser }) {
      // Log sign-in events
      console.log(`User ${user.email} signed in via ${account?.provider}`);
    },

    async signOut({ token }) {
      // Log sign-out events
      console.log(`User ${token.email} signed out`);
    },
  },
};
```

### **API Rate Limiting**

```typescript
// Rate limiting implementation
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

export const createRateLimiter = (redisClient: any) => {
  return rateLimit({
    store: new RedisStore({
      client: redisClient,
      prefix: 'rl:',
    }),
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: {
      error: 'Too many requests from this IP, please try again later.',
    },
    standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
    legacyHeaders: false, // Disable the `X-RateLimit-*` headers
    skip: (req) => {
      // Skip rate limiting for health checks
      return req.path === '/api/health';
    },
    onLimitReached: (req, res) => {
      console.warn(`Rate limit exceeded for IP: ${req.ip}`);
    },
  });
};

// Advanced rate limiting with different tiers
export const createTieredRateLimiter = (redisClient: any) => {
  const getTierLimits = (userTier: string) => {
    switch (userTier) {
      case 'free':
        return { windowMs: 60 * 1000, max: 10 }; // 10 requests per minute
      case 'basic':
        return { windowMs: 60 * 1000, max: 100 }; // 100 requests per minute
      case 'premium':
        return { windowMs: 60 * 1000, max: 1000 }; // 1000 requests per minute
      case 'enterprise':
        return { windowMs: 60 * 1000, max: 10000 }; // 10000 requests per minute
      default:
        return { windowMs: 60 * 1000, max: 10 };
    }
  };

  return (req: any, res: any, next: any) => {
    // Get user tier from session/JWT
    const userTier = req.user?.plan || 'free';
    const limits = getTierLimits(userTier);

    const limiter = rateLimit({
      store: new RedisStore({
        client: redisClient,
        prefix: `rl:${userTier}:`,
      }),
      windowMs: limits.windowMs,
      max: limits.max,
      message: {
        error: `Rate limit exceeded for ${userTier} tier. Please upgrade your plan.`,
      },
      standardHeaders: true,
    });

    limiter(req, res, next);
  };
};
```

## 💰 Cost Optimization

### **Usage Monitoring and Billing**

```typescript
// Cost monitoring and optimization
class CostMonitor {
  private usageTracker: Map<string, UserUsage> = new Map();
  private providerCosts: Map<string, ProviderPricing> = new Map();

  constructor() {
    this.initializeProviderCosts();
  }

  private initializeProviderCosts() {
    this.providerCosts.set('openai', {
      currency: 'USD',
      models: {
        'gpt-4': { input: 0.03, output: 0.06 },
        'gpt-3.5-turbo': { input: 0.0015, output: 0.002 }
      }
    });

    this.providerCosts.set('anthropic', {
      currency: 'USD',
      models: {
        'claude-3-opus': { input: 0.015, output: 0.075 },
        'claude-3-sonnet': { input: 0.003, output: 0.015 }
      }
    });
  }

  trackUsage(userId: string, usage: TokenUsage) {
    if (!this.usageTracker.has(userId)) {
      this.usageTracker.set(userId, {
        userId,
        periodStart: new Date(),
        totalTokens: 0,
        totalCost: 0,
        requests: 0,
        byProvider: new Map(),
        byModel: new Map()
      });
    }

    const userUsage = this.usageTracker.get(userId)!;

    // Update totals
    userUsage.totalTokens += usage.promptTokens + usage.completionTokens;
    userUsage.requests += 1;

    // Calculate cost
    const cost = this.calculateCost(usage.provider, usage.model, usage);
    userUsage.totalCost += cost;

    // Update provider breakdown
    const providerUsage = userUsage.byProvider.get(usage.provider) || {
      tokens: 0,
      cost: 0,
      requests: 0
    };
    providerUsage.tokens += usage.promptTokens + usage.completionTokens;
    providerUsage.cost += cost;
    providerUsage.requests += 1;
    userUsage.byProvider.set(usage.provider, providerUsage);

    // Update model breakdown
    const modelUsage = userUsage.byModel.get(usage.model) || {
      tokens: 0,
      cost: 0,
      requests: 0
    };
    modelUsage.tokens += usage.promptTokens + usage.completionTokens;
    modelUsage.cost += cost;
    modelUsage.requests += 1;
    userUsage.byModel.set(usage.model, modelUsage);
  }

  calculateCost(provider: string, model: string, usage: TokenUsage): number {
    const pricing = this.providerCosts.get(provider);
    if (!pricing || !pricing.models[model]) {
      return 0; // Unknown provider/model
    }

    const modelPricing = pricing.models[model];
    const inputCost = (usage.promptTokens / 1000) * modelPricing.input;
    const outputCost = (usage.completionTokens / 1000) * modelPricing.output;

    return inputCost + outputCost;
  }

  getUserUsage(userId: string): UserUsage | null {
    return this.usageTracker.get(userId) || null;
  }

  checkUsageLimits(userId: string, plan: SubscriptionPlan): UsageCheckResult {
    const usage = this.usageTracker.get(userId);
    if (!usage) {
      return { withinLimits: true };
    }

    const violations: string[] = [];

    if (plan.maxTokens && usage.totalTokens > plan.maxTokens) {
      violations.push(`Token limit exceeded: ${usage.totalTokens}/${plan.maxTokens}`);
    }

    if (plan.maxCost && usage.totalCost > plan.maxCost) {
      violations.push(`Cost limit exceeded: $${usage.totalCost.toFixed(2)}/$${plan.maxCost}`);
    }

    if (plan.maxRequests && usage.requests > plan.maxRequests) {
      violations.push(`Request limit exceeded: ${usage.requests}/${plan.maxRequests}`);
    }

    return {
      withinLimits: violations.length === 0,
      violations,
      currentUsage: {
        tokens: usage.totalTokens,
        cost: usage.totalCost,
        requests: usage.requests
      }
    };
  }

  getCostOptimizationSuggestions(userId: string): CostOptimizationSuggestion[] {
    const usage = this.usageTracker.get(userId);
    if (!usage) return [];

    const suggestions: CostOptimizationSuggestion[] = [];

    // Analyze model usage
    const modelUsage = Array.from(usage.byModel.entries())
      .sort(([, a], [, b]) => b.cost - a.cost);

    if (modelUsage.length > 1) {
      const mostExpensive = modelUsage[0];
      const cheaperAlternative = modelUsage.find(([, u]) => u.cost < mostExpensive[1].cost);

      if (cheaperAlternative) {
        suggestions.push({
          type: 'model_switch',
          description: `Consider switching from ${mostExpensive[0]} to ${cheaperAlternative[0]} to reduce costs by $${(mostExpensive[1].cost - cheaperAlternative[1].cost).toFixed(2)}`,
          potentialSavings: mostExpensive[1].cost - cheaperAlternative[1].cost
        });
      }
    }

    // Check for caching opportunities
    const cacheableRequests = usage.requests * 0.3; // Assume 30% could be cached
    if (cacheableRequests > 10) {
      suggestions.push({
        type: 'implement_caching',
        description: `Implement response caching to potentially save on ${Math.round(cacheableRequests)} repeated requests`,
        potentialSavings: 0 // Would need more analysis
      });
    }

    return suggestions;
  }

  resetUsagePeriod(userId: string) {
    // Reset usage for new billing period
    const usage = this.usageTracker.get(userId);
    if (usage) {
      usage.periodStart = new Date();
      usage.totalTokens = 0;
      usage.totalCost = 0;
      usage.requests = 0;
      usage.byProvider.clear();
      usage.byModel.clear();
    }
  }
}

interface ProviderPricing {
  currency: string;
  models: Record<string, { input: number; output: number }>;
}

interface UserUsage {
  userId: string;
  periodStart: Date;
  totalTokens: number;
  totalCost: number;
  requests: number;
  byProvider: Map<string, { tokens: number; cost: number; requests: number }>;
  byModel: Map<string, { tokens: number; cost: number; requests: number }>;
}

interface SubscriptionPlan {
  maxTokens?: number;
  maxCost?: number;
  maxRequests?: number;
}

interface UsageCheckResult {
  withinLimits: boolean;
  violations?: string[];
  currentUsage?: {
    tokens: number;
    cost: number;
    requests: number;
  };
}

interface CostOptimizationSuggestion {
  type: string;
  description: string;
  potentialSavings: number;
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 90 minutes**

1. **Docker Production Setup**: Create production-ready Docker containers with proper security and optimization
2. **Kubernetes Deployment**: Deploy LobeChat to Kubernetes with autoscaling and proper resource management
3. **Monitoring Implementation**: Set up comprehensive monitoring with Prometheus, Grafana, and custom metrics
4. **CI/CD Pipeline**: Create automated deployment pipeline with testing and rollback capabilities
5. **Performance Optimization**: Implement caching, rate limiting, and cost optimization features
6. **Security Hardening**: Configure authentication, authorization, and security best practices

---

**🎉 Congratulations!** You've completed the comprehensive **LobeChat AI Platform Deep Dive** tutorial. You now have the knowledge to build, deploy, and maintain production-grade AI chat applications with streaming responses, multi-provider support, and enterprise features.

## 🎯 What You've Learned

1. **Modern Chat Architecture**: Streaming responses, real-time updates, and responsive UI
2. **Multi-Provider Integration**: Intelligent provider selection, failover, and load balancing
3. **Advanced UI Patterns**: Message rendering, input handling, and accessibility
4. **Streaming Infrastructure**: Real-time communication, state management, and performance optimization
5. **Production Deployment**: Docker, Kubernetes, monitoring, CI/CD, and cost optimization

## 🚀 Next Steps

- **Build Custom Chatbots**: Create specialized chat interfaces for different use cases
- **Multi-Provider Orchestration**: Implement advanced provider selection and failover logic
- **Enterprise Integration**: Connect with existing business systems and workflows
- **Plugin Ecosystem**: Develop and distribute custom plugins for LobeChat
- **Scalability**: Optimize for high-throughput chat applications with thousands of users

**Happy chatting! 💬✨**