---
layout: default
title: "CopilotKit Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 8: Production Deployment - Secure, Scalable Copilot Apps

Welcome to **Chapter 8: Production Deployment - Secure, Scalable Copilot Apps**. In this part of **CopilotKit Tutorial: Building AI Copilots for React Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Take your CopilotKit app to production with hardened configs, observability, and deployment patterns for cloud and self-hosted environments.

## Overview

This chapter covers production hardening for CopilotKit applications: secure environment configuration, deployment options (Vercel, Docker, Kubernetes), performance tuning, observability, testing, and operational runbooks.

## Production Architecture

```mermaid
graph TB
    subgraph Client["Client Layer"]
        REACT[React App<br/>CopilotKit Provider]
        UI[CopilotChat / CopilotTextarea]
    end

    subgraph Edge["Edge / CDN"]
        CDN[Static Assets]
        EDGE_FN[Edge Functions]
    end

    subgraph Backend["Backend"]
        API[/api/copilotkit<br/>CopilotRuntime]
        AUTH[Auth Middleware]
        RATE[Rate Limiter]
        LOG[Logger / Tracer]
    end

    subgraph Providers["AI Providers"]
        OAI[OpenAI]
        ANTH[Anthropic]
        AZURE[Azure OpenAI]
    end

    Client --> Edge
    Edge --> AUTH
    AUTH --> RATE
    RATE --> API
    API --> LOG
    API --> Providers
```

## Production Readiness Checklist

```markdown
## Pre-Deployment
- [ ] Secrets stored in secret manager (Vault, AWS SM, Doppler)
- [ ] All Copilot endpoints require user authentication
- [ ] Rate limiting configured on /api/copilotkit
- [ ] CORS restricted to your domains only
- [ ] Tool parameters validated server-side
- [ ] PII redaction in logs configured

## Infrastructure
- [ ] Health check endpoint at /api/health
- [ ] Docker multi-stage build optimized
- [ ] Resource limits set (memory, CPU)
- [ ] TLS termination configured
- [ ] Error tracking (Sentry, Bugsnag) integrated

## Observability
- [ ] Structured logging with request IDs
- [ ] Latency, error rate, and token usage metrics
- [ ] Alerting on p95 latency > threshold
- [ ] Cost tracking per tenant/user

## Testing
- [ ] E2E tests for critical copilot flows
- [ ] API contract tests with mocked LLM responses
- [ ] Security tests (blocked origins, missing auth)
- [ ] CI pipeline runs tests before deploy
```

## Environment & Secrets

Create a dedicated production env file or inject via your platform's secret store.

```bash
# .env.production
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
NEXT_PUBLIC_COPILOT_API=/api/copilotkit
LOG_LEVEL=info
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX=120
ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com

# Per-tenant routing (optional)
DEFAULT_MODEL_PROVIDER=openai
DEFAULT_MODEL=gpt-4o
FALLBACK_MODEL_PROVIDER=anthropic
FALLBACK_MODEL=claude-sonnet-4-20250514
```

Load secrets with your platform's runtime (Vercel env vars, Docker secrets, Kubernetes `Secret`). Never bake keys into the client bundle.

### Secret Manager Integration

```typescript
// utils/secrets.ts
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

const client = new SecretsManagerClient({ region: "us-east-1" });

const secretCache = new Map<string, { value: string; expiresAt: number }>();

export async function getSecret(secretName: string): Promise<string> {
  // Check cache (5-minute TTL)
  const cached = secretCache.get(secretName);
  if (cached && cached.expiresAt > Date.now()) {
    return cached.value;
  }

  const response = await client.send(
    new GetSecretValueCommand({ SecretId: secretName })
  );

  const value = response.SecretString!;
  secretCache.set(secretName, {
    value,
    expiresAt: Date.now() + 5 * 60 * 1000,
  });

  return value;
}

// Usage in CopilotKit runtime
export async function getOpenAIKey(): Promise<string> {
  if (process.env.NODE_ENV === "development") {
    return process.env.OPENAI_API_KEY!;
  }
  return getSecret("prod/copilotkit/openai-key");
}
```

## Deploying to Vercel (Next.js)

### Configuration

```json
// vercel.json
{
  "functions": {
    "app/api/copilotkit/route.ts": {
      "maxDuration": 60,
      "memory": 1024
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ]
}
```

### Vercel Deployment Checklist

- Set env vars in Vercel project settings and mark `OPENAI_API_KEY` as secret
- Ensure the Copilot runtime endpoint stays within the same project (`/api/copilotkit`) to avoid CORS
- Enable `edge` runtime only if your adapter supports it; otherwise keep `nodejs` for compatibility
- Set function max duration to 60s for streaming responses
- Add an uptime check against `/api/copilotkit` and key user flows
- Configure preview deployments for PR testing

## Deploying with Docker

### Multi-Stage Dockerfile

```dockerfile
# Dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

FROM node:22-alpine AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Security: run as non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.9"
services:
  copilotkit:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - NEXT_PUBLIC_COPILOT_API=/api/copilotkit
      - LOG_LEVEL=info
      - RATE_LIMIT_MAX=120
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "1.0"
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "5"
```

## Deploying to Kubernetes

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: copilotkit-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: copilotkit
  template:
    metadata:
      labels:
        app: copilotkit
    spec:
      containers:
        - name: copilotkit
          image: your-registry/copilotkit:latest
          ports:
            - containerPort: 3000
          envFrom:
            - secretRef:
                name: copilotkit-secrets
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
          readinessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 30
---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: copilotkit-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: copilotkit-app
  minReplicas: 2
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
---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: copilotkit-service
spec:
  type: ClusterIP
  selector:
    app: copilotkit
  ports:
    - port: 80
      targetPort: 3000
---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: copilotkit-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "120"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "120"
    # Rate limiting at ingress level
    nginx.ingress.kubernetes.io/limit-rps: "20"
    nginx.ingress.kubernetes.io/limit-burst-multiplier: "5"
spec:
  tls:
    - hosts:
        - copilot.example.com
      secretName: copilot-tls
  rules:
    - host: copilot.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: copilotkit-service
                port:
                  number: 80
```

## Security Hardening

### CORS Configuration

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map(o => o.trim());

export function middleware(request: NextRequest) {
  const origin = request.headers.get("origin");

  // CORS check for API routes
  if (request.nextUrl.pathname.startsWith("/api/")) {
    if (origin && !ALLOWED_ORIGINS.includes(origin)) {
      return new NextResponse(null, {
        status: 403,
        statusText: "Forbidden",
      });
    }

    const response = NextResponse.next();
    if (origin) {
      response.headers.set("Access-Control-Allow-Origin", origin);
      response.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS");
      response.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }
    return response;
  }

  return NextResponse.next();
}
```

### Authentication Middleware

```typescript
// lib/auth.ts
import { getServerSession } from "next-auth";
import { authOptions } from "./auth-options";

export async function requireAuth(req: Request) {
  const session = await getServerSession(authOptions);

  if (!session?.user) {
    throw new Response("Unauthorized", { status: 401 });
  }

  return session;
}

// app/api/copilotkit/route.ts
import { requireAuth } from "@/lib/auth";

export async function POST(req: Request) {
  const session = await requireAuth(req);

  const { handleRequest } = copilotkitStream({
    runtime: new CopilotRuntime(),
    serviceAdapter: new OpenAIAdapter({
      apiKey: process.env.OPENAI_API_KEY!,
      model: "gpt-4o",
    }),
    // Pass user context to the runtime
    properties: {
      userId: session.user.id,
      tenantId: session.user.tenantId,
    },
  });

  return handleRequest(req);
}
```

### Tool Parameter Validation

```typescript
// Validate tool inputs server-side to prevent injection
import { z } from "zod";

const createTodoSchema = z.object({
  title: z.string().min(1).max(500),
  priority: z.enum(["low", "medium", "high"]),
  dueDate: z.string().datetime().optional(),
});

const deleteFileSchema = z.object({
  path: z.string()
    .refine(p => !p.includes(".."), "Path traversal not allowed")
    .refine(p => p.startsWith("/allowed/"), "Access denied"),
});

// In your action handler
useCopilotAction({
  name: "createTodo",
  handler: async (params) => {
    // Validate before execution
    const validated = createTodoSchema.parse(params);
    return await createTodo(validated);
  },
});
```

## Rate Limiting & Abuse Controls

### Token Bucket Rate Limiter

```typescript
// lib/rate-limit.ts
interface RateLimitEntry {
  tokens: number;
  lastRefill: number;
}

class TokenBucketLimiter {
  private buckets: Map<string, RateLimitEntry> = new Map();
  private capacity: number;
  private refillRate: number; // tokens per second

  constructor(capacity = 120, refillRate = 2) {
    this.capacity = capacity;
    this.refillRate = refillRate;
  }

  check(key: string): { allowed: boolean; remaining: number } {
    let entry = this.buckets.get(key);

    if (!entry) {
      entry = { tokens: this.capacity, lastRefill: Date.now() };
      this.buckets.set(key, entry);
    }

    // Refill tokens based on time elapsed
    const now = Date.now();
    const elapsed = (now - entry.lastRefill) / 1000;
    entry.tokens = Math.min(
      this.capacity,
      entry.tokens + elapsed * this.refillRate
    );
    entry.lastRefill = now;

    if (entry.tokens < 1) {
      return { allowed: false, remaining: 0 };
    }

    entry.tokens -= 1;
    return { allowed: true, remaining: Math.floor(entry.tokens) };
  }
}

export const rateLimiter = new TokenBucketLimiter();

// Usage in API route
export async function POST(req: Request) {
  const userId = getUserId(req);
  const { allowed, remaining } = rateLimiter.check(userId);

  if (!allowed) {
    return new Response("Rate limit exceeded", {
      status: 429,
      headers: {
        "Retry-After": "30",
        "X-RateLimit-Remaining": String(remaining),
      },
    });
  }

  // Continue with CopilotKit handling...
}
```

### Per-Tenant Token Budgets

```typescript
// lib/budget.ts
interface TenantBudget {
  maxTokensPerDay: number;
  usedToday: number;
  resetAt: number;
}

class BudgetManager {
  private budgets: Map<string, TenantBudget> = new Map();

  async checkBudget(tenantId: string, estimatedTokens: number): Promise<boolean> {
    const budget = await this.getBudget(tenantId);

    // Reset daily budget if past reset time
    if (Date.now() > budget.resetAt) {
      budget.usedToday = 0;
      budget.resetAt = this.getNextMidnight();
    }

    if (budget.usedToday + estimatedTokens > budget.maxTokensPerDay) {
      return false; // Budget exceeded
    }

    return true;
  }

  async recordUsage(tenantId: string, tokens: number) {
    const budget = await this.getBudget(tenantId);
    budget.usedToday += tokens;
    await this.saveBudget(tenantId, budget);
  }
}
```

## Observability: Logging, Tracing, Metrics

### Structured Logging

```typescript
// utils/logger.ts
import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport: process.env.NODE_ENV !== "production"
    ? { target: "pino-pretty", options: { colorize: true } }
    : undefined,
  serializers: {
    err: pino.stdSerializers.err,
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
  },
  // Redact sensitive fields
  redact: {
    paths: ["req.headers.authorization", "req.headers.cookie", "*.apiKey", "*.token"],
    censor: "[REDACTED]",
  },
});

// Usage
export async function POST(req: Request) {
  const requestId = crypto.randomUUID();
  const start = Date.now();

  const childLogger = logger.child({ requestId, path: "/api/copilotkit" });

  try {
    childLogger.info("Processing copilot request");
    const response = await handleCopilotRequest(req);

    childLogger.info({
      duration_ms: Date.now() - start,
      status: response.status,
      tokens_used: response.headers.get("x-tokens-used"),
    }, "Copilot request completed");

    return response;
  } catch (err) {
    childLogger.error({ err, duration_ms: Date.now() - start }, "Copilot request failed");
    throw err;
  }
}
```

### OpenTelemetry Integration

```typescript
// instrumentation.ts
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-http";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";

const sdk = new NodeSDK({
  serviceName: "copilotkit-app",
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4318/v1/traces",
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4318/v1/metrics",
    }),
    exportIntervalMillis: 30000,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

### Custom Metrics

```typescript
// lib/metrics.ts
import { Counter, Histogram, Gauge } from "prom-client";

export const copilotMetrics = {
  requestsTotal: new Counter({
    name: "copilotkit_requests_total",
    help: "Total copilot requests",
    labelNames: ["status", "model", "tenant"],
  }),

  responseLatency: new Histogram({
    name: "copilotkit_response_latency_seconds",
    help: "Response latency in seconds",
    labelNames: ["model"],
    buckets: [0.5, 1, 2, 5, 10, 30, 60],
  }),

  tokensUsed: new Counter({
    name: "copilotkit_tokens_used_total",
    help: "Total tokens consumed",
    labelNames: ["model", "type", "tenant"],
  }),

  activeSessions: new Gauge({
    name: "copilotkit_active_sessions",
    help: "Currently active copilot sessions",
  }),

  toolExecutions: new Counter({
    name: "copilotkit_tool_executions_total",
    help: "Total tool executions",
    labelNames: ["tool", "status"],
  }),

  costEstimate: new Counter({
    name: "copilotkit_cost_usd_total",
    help: "Estimated cost in USD",
    labelNames: ["model", "tenant"],
  }),
};
```

### Alerting Rules

```yaml
# prometheus-alerts.yaml
groups:
  - name: copilotkit
    rules:
      - alert: HighErrorRate
        expr: rate(copilotkit_requests_total{status="error"}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CopilotKit error rate above 5%"

      - alert: HighLatency
        expr: histogram_quantile(0.95, copilotkit_response_latency_seconds) > 15
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CopilotKit p95 latency above 15 seconds"

      - alert: BudgetExceeded
        expr: copilotkit_cost_usd_total > 100
        labels:
          severity: critical
        annotations:
          summary: "Daily cost budget exceeded"
```

## Performance Optimization

### Streaming Best Practices

```typescript
// Ensure streaming is properly configured
export async function POST(req: Request) {
  const { handleRequest } = copilotkitStream({
    runtime: new CopilotRuntime(),
    serviceAdapter: new OpenAIAdapter({
      apiKey: process.env.OPENAI_API_KEY!,
      model: "gpt-4o",
    }),
  });

  const response = await handleRequest(req);

  // Add streaming-friendly headers
  return new Response(response.body, {
    headers: {
      ...Object.fromEntries(response.headers),
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Connection": "keep-alive",
      "X-Accel-Buffering": "no", // Disable Nginx buffering
    },
  });
}
```

### Model Routing for Cost Optimization

```typescript
// Route to different models based on task complexity
class ModelRouter {
  route(task: CopilotTask): ModelConfig {
    // Classification / simple routing → cheap model
    if (task.type === "classification" || task.type === "extraction") {
      return { provider: "openai", model: "gpt-4o-mini" };
    }

    // Complex reasoning / code generation → premium model
    if (task.type === "code_generation" || task.type === "analysis") {
      return { provider: "anthropic", model: "claude-sonnet-4-20250514" };
    }

    // Default
    return { provider: "openai", model: "gpt-4o" };
  }
}
```

### Context Optimization

```typescript
// Optimize context window usage
function optimizeContext(messages: Message[], maxTokens: number): Message[] {
  // Keep system prompt and last N messages
  const systemMessages = messages.filter(m => m.role === "system");
  const conversationMessages = messages.filter(m => m.role !== "system");

  // Summarize old messages if context is too long
  let tokenCount = estimateTokens(systemMessages);
  const optimized = [...systemMessages];

  // Add messages from newest to oldest until budget exhausted
  for (let i = conversationMessages.length - 1; i >= 0; i--) {
    const msgTokens = estimateTokens([conversationMessages[i]]);
    if (tokenCount + msgTokens > maxTokens * 0.8) break;
    optimized.splice(systemMessages.length, 0, conversationMessages[i]);
    tokenCount += msgTokens;
  }

  return optimized;
}
```

## Testing & Quality Gates

### E2E Tests with Playwright

```typescript
// tests/copilotkit.e2e.spec.ts
import { test, expect } from "@playwright/test";

test.describe("CopilotKit Integration", () => {
  test("copilot can add a todo item", async ({ page }) => {
    await page.goto("http://localhost:3000");

    // Open copilot chat
    await page.getByTestId("copilot-trigger").click();

    // Send a message
    await page.getByTestId("copilot-input").fill("Add a todo to buy milk");
    await page.getByTestId("copilot-send").click();

    // Wait for action execution
    await expect(page.getByText("buy milk")).toBeVisible({ timeout: 30000 });
  });

  test("copilot handles rate limiting gracefully", async ({ page }) => {
    await page.goto("http://localhost:3000");

    // Simulate rapid requests
    for (let i = 0; i < 5; i++) {
      await page.getByTestId("copilot-input").fill(`Request ${i}`);
      await page.getByTestId("copilot-send").click();
    }

    // Should not crash — might show rate limit message
    await expect(page.locator(".error-boundary")).not.toBeVisible();
  });

  test("copilot rejects unauthorized requests", async ({ request }) => {
    const response = await request.post("/api/copilotkit", {
      data: { messages: [{ role: "user", content: "test" }] },
      // No auth header
    });

    expect(response.status()).toBe(401);
  });
});
```

### API Contract Tests

```typescript
// tests/api.test.ts
import { describe, it, expect } from "vitest";

describe("/api/copilotkit", () => {
  it("returns 200 with valid request", async () => {
    const response = await fetch("http://localhost:3000/api/copilotkit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${testToken}`,
      },
      body: JSON.stringify({
        messages: [{ role: "user", content: "Hello" }],
      }),
    });

    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toContain("text/event-stream");
  });

  it("rejects requests from blocked origins", async () => {
    const response = await fetch("http://localhost:3000/api/copilotkit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Origin": "https://malicious-site.com",
      },
      body: JSON.stringify({ messages: [] }),
    });

    expect(response.status).toBe(403);
  });
});
```

## Operations Playbook

### Health Check Endpoint

```typescript
// app/api/health/route.ts
export async function GET() {
  const checks = {
    status: "healthy",
    version: process.env.BUILD_SHA || "unknown",
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    checks: {
      openai: await checkProvider("openai"),
      memory: {
        heapUsed: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
        heapTotal: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
      },
    },
  };

  const isHealthy = Object.values(checks.checks).every(
    (c) => typeof c === "object" ? c.status !== "error" : true
  );

  return Response.json(checks, {
    status: isHealthy ? 200 : 503,
  });
}

async function checkProvider(name: string) {
  try {
    // Lightweight check — verify API key is valid
    const response = await fetch("https://api.openai.com/v1/models", {
      headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    });
    return { status: response.ok ? "ok" : "error" };
  } catch {
    return { status: "error" };
  }
}
```

### Rollback Procedure

```bash
# Vercel: instant rollback to previous deployment
vercel rollback

# Docker: tag-based rollback
docker compose down
docker compose pull  # Uses previous tag
docker compose up -d

# Kubernetes: rollback to previous revision
kubectl rollout undo deployment/copilotkit-app
kubectl rollout status deployment/copilotkit-app
```

### Feature Flags for Tool Rollout

```typescript
// lib/feature-flags.ts
const featureFlags: Record<string, FeatureFlag> = {
  "tool:file-upload": { enabled: false, rolloutPercent: 0 },
  "tool:code-execution": { enabled: true, rolloutPercent: 50 },
  "model:claude": { enabled: true, rolloutPercent: 100 },
};

export function isFeatureEnabled(flag: string, userId?: string): boolean {
  const config = featureFlags[flag];
  if (!config || !config.enabled) return false;

  if (config.rolloutPercent >= 100) return true;

  // Consistent hashing for gradual rollout
  if (userId) {
    const hash = hashCode(userId + flag);
    return (hash % 100) < config.rolloutPercent;
  }

  return false;
}
```

## Multi-Provider Failover

```typescript
// lib/provider-failover.ts
class ProviderFailover {
  private providers: ProviderConfig[];

  constructor(providers: ProviderConfig[]) {
    this.providers = providers;
  }

  async createAdapter(): Promise<ServiceAdapter> {
    for (const provider of this.providers) {
      try {
        const adapter = this.createProviderAdapter(provider);
        // Quick health check
        await adapter.healthCheck();
        return adapter;
      } catch (err) {
        logger.warn({ provider: provider.name, err }, "Provider unavailable, trying next");
      }
    }
    throw new Error("All providers unavailable");
  }

  private createProviderAdapter(config: ProviderConfig) {
    switch (config.name) {
      case "openai":
        return new OpenAIAdapter({ apiKey: config.apiKey, model: config.model });
      case "anthropic":
        return new AnthropicAdapter({ apiKey: config.apiKey, model: config.model });
      case "azure":
        return new AzureOpenAIAdapter({ ...config });
      default:
        throw new Error(`Unknown provider: ${config.name}`);
    }
  }
}

// Usage
const failover = new ProviderFailover([
  { name: "openai", model: "gpt-4o", apiKey: process.env.OPENAI_API_KEY! },
  { name: "anthropic", model: "claude-sonnet-4-20250514", apiKey: process.env.ANTHROPIC_API_KEY! },
]);

export async function POST(req: Request) {
  const adapter = await failover.createAdapter();
  const { handleRequest } = copilotkitStream({
    runtime: new CopilotRuntime(),
    serviceAdapter: adapter,
  });
  return handleRequest(req);
}
```

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Secrets** | Use secret managers (Vault, AWS SM); never hardcode or bundle keys |
| **Deployment** | Vercel for quick start; Docker for control; Kubernetes for scale |
| **Security** | CORS restriction, auth middleware, Zod tool validation, PII redaction |
| **Rate Limiting** | Token bucket per user/tenant; budget caps for cost control |
| **Observability** | Structured logging (pino), OpenTelemetry traces, Prometheus metrics |
| **Performance** | Stream responses, route to appropriate models, optimize context |
| **Testing** | E2E with Playwright, API contract tests, security tests in CI |
| **Operations** | Health endpoints, instant rollback, feature flags for gradual rollout |
| **Failover** | Multi-provider with automatic failover (OpenAI → Anthropic → Azure) |

---

This concludes the CopilotKit Tutorial. You now have a comprehensive understanding of the framework — from app context and copilot actions through chat components, generative UI, CoAgents, human-in-the-loop, and production deployment.

---

*Built with insights from the [CopilotKit repository](https://github.com/CopilotKit/CopilotKit) and community documentation.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `copilotkit`, `name`, `response` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment - Secure, Scalable Copilot Apps` as an operating subsystem inside **CopilotKit Tutorial: Building AI Copilots for React Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model`, `headers`, `status` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment - Secure, Scalable Copilot Apps` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `copilotkit`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `response`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/CopilotKit/CopilotKit)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `copilotkit` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Human-in-the-Loop - User Approval Flows and Interrupts](07-human-in-loop.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
