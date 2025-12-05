---
layout: default
title: "CopilotKit Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 8: Production Deployment - Secure, Scalable Copilot Apps

> Take your CopilotKit app to production with hardened configs, observability, and deployment patterns for cloud and self-hosted environments.

## Overview

This chapter covers production hardening for CopilotKit applications: secure environment configuration, deployment options (Vercel, Docker, Kubernetes), performance tuning, observability, testing, and operational runbooks.

## Production Readiness Checklist

- **Secrets**: Use `.env.production` and a secret manager (Vault, AWS Secrets Manager, Doppler) — never hardcode keys.
- **Auth**: Require user auth or signed requests for all Copilot endpoints; scope tokens to tenants/projects.
- **Rate limiting**: Protect `/api/copilotkit` and any tool-calling endpoints.
- **Logging/Tracing**: Structured logs, request IDs, and tracing for LLM/tool calls.
- **Monitoring**: Health checks, saturation signals (latency, error rate), cost and token usage tracking.
- **Safety**: Prompt injection and output validation for tool-calling actions.
- **Testing**: E2E happy path, guarded actions, regression suite before deploy.

## Environment & Secrets

Create a dedicated production env file or inject via your platform’s secret store.

```
# .env.production
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_COPILOT_API=/api/copilotkit
LOG_LEVEL=info
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX=120
ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com
```

Load secrets with your platform’s runtime (Vercel env vars, Docker secrets, Kubernetes `Secret`). Never bake keys into the client bundle.

## Deploying to Vercel (Next.js)

- Set env vars in Vercel project settings and mark `OPENAI_API_KEY` as secret.
- Ensure the Copilot runtime endpoint stays within the same project (`/api/copilotkit`) to avoid CORS.
- Enable `edge` runtime only if your adapter supports it; otherwise keep `nodejs` for compatibility.
- Add an uptime check against `/api/copilotkit` and key user flows (e.g., sample chat).

## Deploying with Docker

```dockerfile
# Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=deps /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "run", "start"]
```

```yaml
# docker-compose.yml (example)
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
    restart: unless-stopped
```

## Deploying to Kubernetes

- Use a `Deployment` with `readinessProbe` on `/api/health` and `livenessProbe` on `/api/copilotkit`.
- Mount secrets via `envFrom: secretRef`.
- Add a `HorizontalPodAutoscaler` based on CPU and optionally custom metrics (latency, p95).
- Place an API gateway/ingress with TLS termination and rate limiting (e.g., NGINX Ingress + limiters).

## Security Hardening

- **CORS**: Restrict origins to your domains; block wildcard.
- **AuthZ**: Require a user session or signed JWT on Copilot requests; include user/tenant metadata.
- **Tool safety**: Validate parameters server-side; whitelist commands/integrations; sanitize file paths and URLs.
- **Data handling**: Redact PII in logs; avoid persisting raw prompts/responses unless needed; encrypt at rest if stored.
- **Dependency hygiene**: Regularly update `@copilotkit/*`, adapters, and Next.js; enable `npm audit` in CI.

## Rate Limiting & Abuse Controls

```ts
// app/api/copilotkit/route.ts (snippet)
import rateLimit from "express-rate-limit";
import { CopilotRuntime, OpenAIAdapter, copilotkitStream } from "@copilotkit/runtime";

const limiter = rateLimit({
  windowMs: Number(process.env.RATE_LIMIT_WINDOW_MS || 60000),
  max: Number(process.env.RATE_LIMIT_MAX || 120),
});

export async function POST(req: Request) {
  await limiter.check?.(req as any, {} as any); // adapt limiter to Next handler

  const { handleRequest } = copilotkitStream({
    runtime: new CopilotRuntime(),
    serviceAdapter: new OpenAIAdapter({
      apiKey: process.env.OPENAI_API_KEY!,
      model: "gpt-4o",
    }),
  });

  return handleRequest(req);
}
```

If you need finer control, add per-user/tenant quotas and burst limits at the gateway level.

## Observability: Logging, Tracing, Metrics

```ts
// utils/logger.ts
import pino from "pino";
export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport: { target: "pino-pretty", options: { colorize: true } },
});
```

```ts
// app/api/copilotkit/route.ts (instrumentation)
import { logger } from "@/utils/logger";

export async function POST(req: Request) {
  const start = Date.now();
  const { handleRequest } = copilotkitStream({ /* ... */ });
  const response = await handleRequest(req);
  logger.info({
    path: "/api/copilotkit",
    duration_ms: Date.now() - start,
    status: response.status,
  });
  return response;
}
```

- Add request IDs to correlate frontend logs with backend traces.
- Export metrics (latency, errors, tokens per request) to Prometheus or your APM; alert on p95 latency and error rate.

## Performance Tips

- Stream responses to reduce perceived latency.
- Prefer concise system prompts; chunk large context and summarize old turns.
- Cache static context (product docs, FAQs) in memory or an edge cache.
- Use smaller models for non-critical paths (classification, routing) and reserve premium models for high-value actions.

## Testing & Quality Gates

```ts
// tests/copilotkit.e2e.spec.ts (Playwright pseudo-code)
import { test, expect } from "@playwright/test";

test("copilot can add a todo", async ({ page }) => {
  await page.goto("http://localhost:3000");
  await page.getByText("Add a todo to buy milk").click();
  await page.getByText("AI-Powered Todo App"); // wait for UI
  await expect(page.getByText("buy milk")).toBeVisible();
});
```

- Add API contract tests for `/api/copilotkit` with mocked LLM responses.
- Include security tests: blocked origins, missing auth, invalid tool parameters.
- Run tests in CI before deploy; fail on lint/type errors and high vuln severity.

## Operations Playbook

- **Health**: Implement `/api/health` returning build SHA and dependencies status.
- **Rollback**: Keep previous image/tag; support fast revert via your platform (Vercel preview/rollback, Kubernetes canary + scale down).
- **Feature flags**: Gate new tools/actions; enable gradual rollout.
- **Cost controls**: Track tokens per tenant; alert on anomalies; add per-user budgets.

## What’s Next

- Add custom adapters (Anthropic/Bedrock/Azure OpenAI) with per-tenant routing.
- Build tool-specific guardrails (input schemas, policy checks) for sensitive actions.
- Integrate with your observability stack (Datadog, Grafana, OpenTelemetry) for unified traces across frontend, backend, and LLM calls.
