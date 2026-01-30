---
layout: default
title: "Chapter 8: Deployment and Sharing"
parent: "Dyad Tutorial"
nav_order: 8
---

# Chapter 8: Deployment and Sharing

You have built, styled, and tested your Dyad application -- now it is time to get it in front of users. Deployment transforms your local development project into a live, accessible application. In this final chapter, we will cover the full deployment lifecycle: building optimized production bundles, choosing the right hosting platform, configuring CI/CD pipelines, setting up custom domains, and sharing your projects with collaborators and the world.

## The Deployment Pipeline

A well-structured deployment pipeline takes your code from a local repository to a production environment with confidence. Dyad applications follow standard modern web deployment patterns.

```mermaid
flowchart TD
    A[Local Development] --> B[Git Push]
    B --> C[CI Pipeline Triggered]
    C --> D[Install Dependencies]
    D --> E[Lint & Type Check]
    E --> F[Run Tests]
    F --> G[Build Production Bundle]
    G --> H{Tests Passed?}
    H -->|Yes| I[Deploy to Staging]
    H -->|No| J[Notify Developer]
    I --> K[Smoke Tests]
    K --> L{Staging OK?}
    L -->|Yes| M[Deploy to Production]
    L -->|No| J
    M --> N[Health Check]
    N --> O[Live Application]

    classDef local fill:#e1f5fe,stroke:#01579b
    classDef ci fill:#fff3e0,stroke:#ef6c00
    classDef check fill:#f3e5f5,stroke:#4a148c
    classDef deploy fill:#e8f5e8,stroke:#1b5e20
    classDef fail fill:#ffebee,stroke:#b71c1c

    class A,B local
    class C,D,E,F,G ci
    class H,K,L check
    class I,M,N,O deploy
    class J fail
```

## Building for Production

Before deploying, you need an optimized production build. Dyad applications use Vite, which produces highly optimized bundles with tree shaking, code splitting, and asset optimization.

### Build Configuration

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist",
    sourcemap: true,
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          router: ["react-router-dom"],
          ui: ["@headlessui/react"],
        },
      },
    },
    chunkSizeWarningLimit: 500,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Build Commands

```bash
# Create production build
npm run build

# Preview the production build locally
npm run preview

# Analyze bundle size
npx vite-bundle-visualizer
```

### Build Output Optimization

| Optimization | Technique | Impact |
|-------------|-----------|--------|
| Tree Shaking | Remove unused exports | 20-40% size reduction |
| Code Splitting | Lazy load routes and heavy components | Faster initial load |
| Minification | Terser compression | 60-70% size reduction |
| Asset Hashing | Content-based filenames | Optimal cache invalidation |
| Gzip / Brotli | Server-level compression | 70-80% transfer reduction |
| Image Optimization | WebP conversion, lazy loading | Significant bandwidth savings |

## Deployment Platforms

### Vercel

Vercel offers the smoothest deployment experience for React applications with automatic CI/CD, edge functions, and a global CDN.

```mermaid
flowchart LR
    A[Git Push] --> B[Vercel Detects Change]
    B --> C[Build Triggered]
    C --> D[Deploy to Preview]
    D --> E{PR Merged?}
    E -->|Yes| F[Deploy to Production]
    E -->|No| G[Preview URL Available]

    F --> H[Global CDN]
    H --> I[Edge Network]
    I --> J[Users Worldwide]

    classDef trigger fill:#e1f5fe,stroke:#01579b
    classDef build fill:#fff3e0,stroke:#ef6c00
    classDef deploy fill:#e8f5e8,stroke:#1b5e20
    classDef edge fill:#f3e5f5,stroke:#4a148c

    class A trigger
    class B,C build
    class D,E,F,G deploy
    class H,I,J edge
```

#### Vercel Configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

#### Deploying to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Set environment variables
vercel env add VITE_API_BASE_URL production
vercel env add VITE_GA_MEASUREMENT_ID production
```

### Netlify

Netlify provides powerful deployment with built-in form handling, serverless functions, and split testing.

#### Netlify Configuration

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "DENY"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:;"
```

#### Deploying to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize project
netlify init

# Deploy to preview (draft)
netlify deploy

# Deploy to production
netlify deploy --prod

# Set environment variables
netlify env:set VITE_API_BASE_URL https://api.example.com
```

### Self-Hosting with Docker

For full control over your deployment environment, Docker containers offer portability and consistency.

#### Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:80/health || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Nginx Configuration

```nginx
# nginx.conf
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }

    # Serve static assets with long cache
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 256;

    # SPA fallback - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

#### Docker Compose for Full Stack

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    environment:
      - NODE_ENV=production
    depends_on:
      - api
    restart: unless-stopped

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dyad_app
      - API_SECRET_KEY=${API_SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dyad_app
    restart: unless-stopped

volumes:
  postgres_data:
```

```bash
# Build and start all services
docker compose up -d --build

# View logs
docker compose logs -f app

# Stop all services
docker compose down
```

## Hosting Platform Comparison

| Feature | Vercel | Netlify | Docker / Self-Host | GitHub Pages |
|---------|--------|---------|-------------------|-------------|
| Free Tier | Yes | Yes | No (server cost) | Yes |
| Custom Domains | Yes | Yes | Yes | Yes |
| SSL Certificates | Automatic | Automatic | Manual / Let's Encrypt | Automatic |
| Serverless Functions | Yes | Yes | Manual setup | No |
| Global CDN | Yes | Yes | Optional (Cloudflare) | Yes |
| Preview Deployments | Automatic | Automatic | Manual | No |
| Build Minutes / Month | 6000 | 300 | Unlimited | 2000 |
| Backend Support | Edge Functions | Functions | Full control | Static only |
| Best For | React/Next.js SPAs | JAMstack sites | Complex architectures | Simple static sites |

## CI/CD with GitHub Actions

Automate your deployment pipeline with GitHub Actions to ensure every change goes through testing before reaching production.

```yaml
# .github/workflows/deploy.yml
name: Build, Test, and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: "20"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Run unit and integration tests
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          VITE_API_BASE_URL: ${{ secrets.VITE_API_BASE_URL }}
          VITE_GA_MEASUREMENT_ID: ${{ secrets.VITE_GA_MEASUREMENT_ID }}

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  e2e:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/

  deploy:
    needs: [test, build, e2e]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
```

## Custom Domain Setup

Setting up a custom domain gives your application a professional identity.

### DNS Configuration

| Record Type | Name | Value | TTL |
|------------|------|-------|-----|
| A | `@` | Platform IP (e.g., `76.76.21.21`) | 3600 |
| CNAME | `www` | `your-app.vercel.app` | 3600 |
| TXT | `@` | Domain verification string | 3600 |

### SSL Certificate Setup

```mermaid
flowchart LR
    A[Configure DNS] --> B[Platform Detects Domain]
    B --> C[Request SSL Certificate]
    C --> D[Domain Validation]
    D --> E[Certificate Issued]
    E --> F[HTTPS Enabled]
    F --> G[Auto-Renewal]

    classDef config fill:#e1f5fe,stroke:#01579b
    classDef process fill:#fff3e0,stroke:#ef6c00
    classDef done fill:#e8f5e8,stroke:#1b5e20

    class A config
    class B,C,D process
    class E,F,G done
```

## Sharing and Collaboration

### Sharing Your Dyad Project

Dyad makes it easy to share projects with others through multiple channels.

#### Exporting Your Project

```bash
# Export as a zip archive
zip -r my-dyad-app.zip . -x "node_modules/*" ".git/*" "dist/*"

# Or use git archive
git archive --format=zip --output=my-dyad-app.zip HEAD
```

#### Setting Up for Collaborators

Create a comprehensive setup script that new collaborators can run:

```typescript
// scripts/setup.ts
import { execSync } from "child_process";
import { existsSync, copyFileSync } from "fs";

function run(cmd: string): void {
  console.log(`Running: ${cmd}`);
  execSync(cmd, { stdio: "inherit" });
}

function setup(): void {
  console.log("Setting up Dyad application...\n");

  // Check Node.js version
  const nodeVersion = process.version;
  const major = parseInt(nodeVersion.slice(1).split(".")[0]);
  if (major < 18) {
    console.error("Node.js 18 or later is required");
    process.exit(1);
  }
  console.log(`Node.js ${nodeVersion} detected\n`);

  // Install dependencies
  run("npm install");

  // Set up environment file
  if (!existsSync(".env.local")) {
    if (existsSync(".env.example")) {
      copyFileSync(".env.example", ".env.local");
      console.log("\nCreated .env.local from .env.example");
      console.log("Please update .env.local with your actual values\n");
    }
  }

  // Run database migrations if applicable
  if (existsSync("prisma/schema.prisma")) {
    run("npx prisma generate");
    run("npx prisma db push");
    console.log("\nDatabase schema synchronized\n");
  }

  // Verify build
  run("npm run build");

  console.log("\nSetup complete! Run 'npm run dev' to start developing.\n");
}

setup();
```

#### Environment Example File

```bash
# .env.example (commit this to git)
# Copy this file to .env.local and fill in the values

# Application
VITE_APP_NAME=My Dyad App
VITE_APP_URL=http://localhost:5173

# API Configuration
VITE_API_BASE_URL=http://localhost:4000/api

# Authentication (get keys from your OAuth provider)
VITE_OAUTH_CLIENT_ID=
VITE_OAUTH_REDIRECT_URI=http://localhost:5173/auth/callback

# Third-Party Services
VITE_GA_MEASUREMENT_ID=
VITE_WEATHER_API_KEY=

# Server-side only (not exposed to browser)
API_SECRET_KEY=
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
```

### Monitoring and Analytics

Once deployed, monitor your application's performance and usage.

```typescript
// services/monitoring.ts
interface PerformanceMetrics {
  fcp: number;   // First Contentful Paint
  lcp: number;   // Largest Contentful Paint
  fid: number;   // First Input Delay
  cls: number;   // Cumulative Layout Shift
  ttfb: number;  // Time to First Byte
}

export function reportWebVitals(): void {
  if (typeof window === "undefined") return;

  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const metric = {
        name: entry.name,
        value: entry.startTime,
        id: crypto.randomUUID(),
        page: window.location.pathname,
      };

      // Send to analytics endpoint
      if (navigator.sendBeacon) {
        navigator.sendBeacon(
          "/api/analytics/vitals",
          JSON.stringify(metric)
        );
      }

      console.log(`[Web Vital] ${entry.name}: ${entry.startTime.toFixed(2)}ms`);
    }
  });

  observer.observe({ type: "largest-contentful-paint", buffered: true });
  observer.observe({ type: "first-input", buffered: true });
  observer.observe({ type: "layout-shift", buffered: true });
}

export function reportError(error: Error, context?: Record<string, unknown>): void {
  const payload = {
    message: error.message,
    stack: error.stack,
    url: window.location.href,
    userAgent: navigator.userAgent,
    timestamp: new Date().toISOString(),
    context,
  };

  fetch("/api/analytics/errors", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).catch(() => {
    // Silently fail if error reporting itself fails
  });
}

// Global error handler
window.addEventListener("error", (event) => {
  reportError(event.error ?? new Error(event.message));
});

window.addEventListener("unhandledrejection", (event) => {
  reportError(
    event.reason instanceof Error
      ? event.reason
      : new Error(String(event.reason))
  );
});
```

### Performance Budget

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| First Contentful Paint | < 1.8s | 1.8s - 3.0s | > 3.0s |
| Largest Contentful Paint | < 2.5s | 2.5s - 4.0s | > 4.0s |
| First Input Delay | < 100ms | 100ms - 300ms | > 300ms |
| Cumulative Layout Shift | < 0.1 | 0.1 - 0.25 | > 0.25 |
| Time to First Byte | < 200ms | 200ms - 500ms | > 500ms |
| Total Bundle Size (gzipped) | < 200KB | 200KB - 500KB | > 500KB |

## Post-Deployment Checklist

Before considering your deployment complete, verify the following:

| Category | Check | Status |
|----------|-------|--------|
| **Build** | Production build succeeds without warnings | Required |
| **Build** | Bundle size within performance budget | Required |
| **Security** | Environment variables are set (not hardcoded) | Required |
| **Security** | Security headers configured (CSP, X-Frame-Options) | Required |
| **Security** | HTTPS enabled with valid SSL certificate | Required |
| **Performance** | Assets served with cache headers | Recommended |
| **Performance** | Gzip or Brotli compression enabled | Recommended |
| **Performance** | Images optimized and lazy-loaded | Recommended |
| **Routing** | SPA fallback configured (serves index.html for all routes) | Required |
| **Monitoring** | Error tracking configured | Recommended |
| **Monitoring** | Web Vitals reporting active | Recommended |
| **SEO** | Meta tags and Open Graph tags present | Recommended |
| **Accessibility** | Lighthouse accessibility score > 90 | Recommended |

---

## Summary

Deploying your Dyad application is the final step in the journey from idea to live product. In this chapter, you learned how to create optimized production builds with Vite, deploy to popular platforms including Vercel, Netlify, and self-hosted Docker containers, automate your pipeline with GitHub Actions CI/CD, configure custom domains with SSL, set up collaboration workflows for team members, and implement production monitoring with Web Vitals and error tracking. Each hosting option offers different trade-offs between simplicity, control, and cost -- choose the one that best fits your project's needs.

## Key Takeaways

- **Build optimization** -- Vite's tree shaking, code splitting, and minification produce small, fast production bundles out of the box.
- **Platform choice matters** -- Vercel and Netlify provide zero-config deployments for most Dyad apps; Docker gives full control for complex architectures.
- **Automate everything** -- GitHub Actions CI/CD pipelines ensure every change is linted, tested, built, and deployed automatically.
- **Security by default** -- Configure security headers, use HTTPS, and keep secrets in environment variables, never in source code.
- **Monitor in production** -- Web Vitals tracking and error reporting help you catch issues before users report them.
- **Share with intention** -- Provide `.env.example` files, setup scripts, and clear documentation to make collaboration seamless.

## Congratulations!

You have completed the Dyad tutorial. You now have the knowledge and tools to build full-stack web applications using natural language, from initial prompt to production deployment. Here is a recap of everything you have learned across all eight chapters:

1. **Getting Started** -- Installing Dyad and creating your first AI-generated application
2. **Natural Language Building** -- Crafting effective prompts for sophisticated applications
3. **Component Integration** -- Adding UI components and extending functionality
4. **Data Management** -- Connecting databases and managing application data
5. **API Integration** -- Connecting to external services with typed API clients
6. **Customization and Styling** -- Building theme systems, responsive layouts, and animations
7. **Testing and Validation** -- Ensuring reliability with unit, integration, and E2E tests
8. **Deployment and Sharing** -- Taking your application live and collaborating with others

**Happy building with Dyad!**

---

*Built with insights from the [Dyad](https://github.com/dyad-sh/dyad) project.*
