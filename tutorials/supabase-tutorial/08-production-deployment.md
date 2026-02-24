---
layout: default
title: "Chapter 8: Production Deployment"
parent: "Supabase Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Welcome to **Chapter 8: Production Deployment**. In this part of **Supabase Tutorial: Building Modern Backend Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In [Chapter 7](07-advanced-queries.md), you hardened your queries and RLS policies for performance and security. Now it is time to ship your application to real users. Moving from development to production involves more than flipping a switch -- you need proper environment management, monitoring, backups, security hardening, performance tuning, and a systematic launch process. This chapter walks through every step of preparing and operating a production Supabase application.

## Production Architecture Overview

A production Supabase deployment involves multiple environments, CI/CD pipelines, monitoring, and operational procedures.

```mermaid
flowchart TD
    A[Developer] --> B[Local Supabase]
    B --> C[Git Push]
    C --> D[CI/CD Pipeline]
    D --> E{Tests Pass?}
    E -->|Yes| F[Deploy to Staging]
    E -->|No| G[Fix & Retry]
    F --> H[QA Verification]
    H --> I{Approved?}
    I -->|Yes| J[Deploy to Production]
    I -->|No| G
    J --> K[Production Supabase]

    K --> L[Monitoring]
    K --> M[Backups]
    K --> N[Alerts]

    classDef dev fill:#e1f5fe,stroke:#01579b
    classDef ci fill:#f3e5f5,stroke:#4a148c
    classDef prod fill:#e8f5e8,stroke:#1b5e20
    classDef ops fill:#fff3e0,stroke:#ef6c00

    class A,B dev
    class C,D,E,G ci
    class F,H,I,J,K prod
    class L,M,N ops
```

## Environment Management

### Separate Projects for Each Environment

| Environment | Purpose | Supabase Project | Branch |
|---|---|---|---|
| **Local** | Development and testing | `supabase start` (Docker) | Feature branches |
| **Staging** | Pre-production verification | Separate Supabase project | `staging` branch |
| **Production** | Live user traffic | Separate Supabase project | `main` branch |

### Environment Configuration

```bash
# .env.local (development)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-local-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-local-service-role-key
SUPABASE_DB_URL=postgresql://postgres:postgres@localhost:54322/postgres

# .env.staging
NEXT_PUBLIC_SUPABASE_URL=https://staging-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=staging-anon-key
SUPABASE_SERVICE_ROLE_KEY=staging-service-role-key

# .env.production
NEXT_PUBLIC_SUPABASE_URL=https://prod-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=prod-anon-key
SUPABASE_SERVICE_ROLE_KEY=prod-service-role-key
```

### Supabase Configuration per Environment

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from '../types/supabase'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
  },
  db: {
    schema: 'public',
  },
  global: {
    headers: {
      'x-application-name': 'my-app',
    },
  },
})
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Supabase

on:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run type checks
        run: npm run type-check

      - name: Run tests
        run: npm test

      - name: Run linter
        run: npm run lint

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Link to staging project
        run: supabase link --project-ref ${{ secrets.STAGING_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Push database migrations
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Deploy Edge Functions
        run: supabase functions deploy --project-ref ${{ secrets.STAGING_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Generate types
        run: |
          supabase gen types typescript --project-id ${{ secrets.STAGING_PROJECT_REF }} > src/types/supabase.ts
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Setup Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Link to production project
        run: supabase link --project-ref ${{ secrets.PRODUCTION_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Push database migrations
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Deploy Edge Functions
        run: supabase functions deploy --project-ref ${{ secrets.PRODUCTION_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

### Secret Scanning

```yaml
# .github/workflows/security.yml
name: Security Checks

on: [push, pull_request]

jobs:
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

  dependency-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --production
```

## Database Migration Strategy

### Safe Migration Practices

```mermaid
flowchart LR
    A[Write Migration] --> B[Test Locally]
    B --> C[Push to Staging]
    C --> D[Verify Staging]
    D --> E[Push to Production]
    E --> F[Monitor for Errors]

    classDef safe fill:#e8f5e8,stroke:#1b5e20
    classDef verify fill:#fff3e0,stroke:#ef6c00

    class A,B safe
    class C,D verify
    class E,F verify
```

```bash
# Development workflow
supabase db diff --file add_user_preferences    # Generate migration
supabase db reset                                 # Test locally
supabase db push --db-url $STAGING_DB_URL        # Deploy to staging

# After verification
supabase db push --db-url $PRODUCTION_DB_URL     # Deploy to production
```

### Migration Safety Rules

| Rule | Why | Example |
|---|---|---|
| Never drop columns directly | Breaks running application | Add new column first, migrate data, then drop old column in a later release |
| Add indexes concurrently | Avoids table locks | `CREATE INDEX CONCURRENTLY ...` |
| Use `IF NOT EXISTS` | Makes migrations idempotent | `CREATE TABLE IF NOT EXISTS ...` |
| Test with production-like data | Prevents surprises at scale | Seed staging with anonymized prod data |
| Back up before major changes | Recovery if something goes wrong | `pg_dump` before running migration |

### Handling Breaking Schema Changes

```sql
-- Step 1: Add new column (non-breaking)
ALTER TABLE public.profiles ADD COLUMN display_name TEXT;

-- Step 2: Backfill data from old column
UPDATE public.profiles SET display_name = full_name WHERE display_name IS NULL;

-- Step 3: Update application code to use display_name
-- (Deploy application changes)

-- Step 4: In a future migration, drop the old column
-- ALTER TABLE public.profiles DROP COLUMN full_name;
```

## Monitoring and Observability

### Database Monitoring

```sql
-- Check active connections
SELECT
  datname,
  usename,
  state,
  COUNT(*) AS connection_count
FROM pg_stat_activity
GROUP BY datname, usename, state
ORDER BY connection_count DESC;

-- Find slow queries
SELECT
  query,
  calls,
  mean_exec_time,
  total_exec_time,
  rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Check table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
  pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS data_size,
  pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename::regclass)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;

-- Check index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan AS times_used,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;
```

### Application-Level Health Check

```typescript
// src/lib/healthcheck.ts
import { supabase } from './supabase'

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  checks: {
    database: { ok: boolean; latency_ms: number }
    auth: { ok: boolean; latency_ms: number }
    storage: { ok: boolean; latency_ms: number }
  }
  timestamp: string
}

export async function checkHealth(): Promise<HealthStatus> {
  const checks = {
    database: { ok: false, latency_ms: 0 },
    auth: { ok: false, latency_ms: 0 },
    storage: { ok: false, latency_ms: 0 },
  }

  // Database check
  const dbStart = Date.now()
  try {
    const { error } = await supabase.from('profiles').select('count').limit(1)
    checks.database.ok = !error
    checks.database.latency_ms = Date.now() - dbStart
  } catch {
    checks.database.latency_ms = Date.now() - dbStart
  }

  // Auth check
  const authStart = Date.now()
  try {
    const { error } = await supabase.auth.getSession()
    checks.auth.ok = !error
    checks.auth.latency_ms = Date.now() - authStart
  } catch {
    checks.auth.latency_ms = Date.now() - authStart
  }

  // Storage check
  const storageStart = Date.now()
  try {
    const { error } = await supabase.storage.listBuckets()
    checks.storage.ok = !error
    checks.storage.latency_ms = Date.now() - storageStart
  } catch {
    checks.storage.latency_ms = Date.now() - storageStart
  }

  const allOk = Object.values(checks).every(c => c.ok)
  const anyFailed = Object.values(checks).some(c => !c.ok)

  return {
    status: allOk ? 'healthy' : anyFailed ? 'unhealthy' : 'degraded',
    checks,
    timestamp: new Date().toISOString(),
  }
}
```

### Setting Up Alerts

```typescript
// supabase/functions/monitoring-alert/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createAdminClient } from "../_shared/supabase-client.ts"

serve(async (req: Request) => {
  const supabase = createAdminClient()

  // Check for failed login attempts (brute force detection)
  const { data: failedLogins } = await supabase
    .rpc('count_failed_logins_last_hour')

  if (failedLogins && failedLogins > 100) {
    await sendAlert({
      severity: 'high',
      message: `${failedLogins} failed login attempts in the last hour`,
      channel: 'security',
    })
  }

  // Check database connection count
  const { data: connections } = await supabase
    .rpc('get_active_connections')

  if (connections && connections > 80) {
    await sendAlert({
      severity: 'warning',
      message: `Database connections at ${connections}% capacity`,
      channel: 'infrastructure',
    })
  }

  return new Response(JSON.stringify({ checked: true }), {
    headers: { 'Content-Type': 'application/json' },
  })
})

async function sendAlert(alert: {
  severity: string
  message: string
  channel: string
}) {
  // Send to Slack
  await fetch(Deno.env.get('SLACK_WEBHOOK_URL')!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `[${alert.severity.toUpperCase()}] ${alert.message}`,
      channel: `#${alert.channel}`,
    }),
  })
}
```

## Backups and Disaster Recovery

### Backup Strategy

```mermaid
flowchart TD
    A[Supabase Automated Backups] --> B[Daily Snapshots]
    B --> C[7-Day Retention - Free Tier]
    B --> D[30-Day Retention - Pro Tier]

    E[Manual Backups] --> F[pg_dump Export]
    F --> G[Store in S3 / GCS]

    H[Point-in-Time Recovery] --> I[Pro Tier Feature]
    I --> J[Restore to Any Second]

    K[Backup Verification] --> L[Monthly Restore Test]
    L --> M[Verify Data Integrity]

    classDef auto fill:#e8f5e8,stroke:#1b5e20
    classDef manual fill:#e1f5fe,stroke:#01579b
    classDef verify fill:#fff3e0,stroke:#ef6c00

    class A,B,C,D auto
    class E,F,G manual
    class H,I,J auto
    class K,L,M verify
```

### Manual Backup Script

```bash
#!/bin/bash
# scripts/backup.sh

set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
BACKUP_FILE="${BACKUP_DIR}/backup_${DATE}.sql.gz"

mkdir -p "${BACKUP_DIR}"

echo "Starting database backup..."

# Export database using pg_dump
pg_dump "${SUPABASE_DB_URL}" \
  --no-owner \
  --no-privileges \
  --clean \
  --if-exists \
  --schema=public \
  --schema=auth \
  --schema=storage \
  | gzip > "${BACKUP_FILE}"

echo "Backup saved to ${BACKUP_FILE}"
echo "Size: $(du -sh ${BACKUP_FILE} | cut -f1)"

# Upload to cloud storage (optional)
# aws s3 cp "${BACKUP_FILE}" "s3://your-backups-bucket/supabase/${DATE}/"
# gsutil cp "${BACKUP_FILE}" "gs://your-backups-bucket/supabase/${DATE}/"

# Clean up old local backups (keep last 7)
ls -t "${BACKUP_DIR}"/backup_*.sql.gz | tail -n +8 | xargs -r rm

echo "Backup complete."
```

### Disaster Recovery Procedure

| Step | Action | Command / Tool |
|---|---|---|
| 1 | Identify the issue | Check Supabase Dashboard logs and alerts |
| 2 | Stop writes (if needed) | Pause the application or enable maintenance mode |
| 3 | Restore from backup | `psql $DB_URL < backup.sql` or Dashboard restore |
| 4 | Verify data integrity | Run data validation queries |
| 5 | Resume traffic | Remove maintenance mode; verify application health |
| 6 | Post-mortem | Document what happened and update runbook |

## Performance and Scaling

### Connection Pooling with Supavisor

Supabase uses Supavisor for connection pooling. Configure your application to use the pooler URL.

```typescript
// For server-side code that opens many connections
const supabaseServer = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    db: {
      // Use the pooler connection for serverless environments
      // Supabase provides this URL in the Dashboard
      schema: 'public',
    },
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
)
```

### Caching Strategy

```typescript
// API-level caching with Cache-Control headers
// (in Next.js API routes or Edge Functions)
export async function GET(request: Request) {
  const { data } = await supabase
    .from('articles')
    .select('id, title, slug, summary')
    .eq('status', 'published')
    .order('published_at', { ascending: false })
    .limit(20)

  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      // Cache for 5 minutes, revalidate in background
      'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
    },
  })
}
```

### Performance Tuning Checklist

| Area | Action | Impact |
|---|---|---|
| Database | Add indexes for frequent queries | Reduces query time from seconds to milliseconds |
| Database | Use connection pooling | Prevents connection exhaustion in serverless |
| Database | Materialized views for dashboards | Eliminates repeated expensive aggregations |
| API | Select only needed columns | Reduces payload size and transfer time |
| API | Implement pagination | Prevents loading entire tables |
| Storage | Use CDN for public assets | Reduces latency for static files |
| Storage | Image transformations | Serves optimized images per device |
| Client | Implement caching | Reduces API calls and improves perceived speed |
| Client | Optimistic updates | Makes UI feel instant |
| Edge Functions | Minimize dependencies | Reduces cold start time |

## Security Hardening

### Pre-Launch Security Checklist

```sql
-- 1. Verify RLS is enabled on all user-facing tables
SELECT
  schemaname,
  tablename,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Every table should have rowsecurity = true

-- 2. Check for tables without any policies (RLS enabled but no rules = deny all)
SELECT
  t.schemaname,
  t.tablename,
  COUNT(p.policyname) AS policy_count
FROM pg_tables t
LEFT JOIN pg_policies p ON p.schemaname = t.schemaname AND p.tablename = t.tablename
WHERE t.schemaname = 'public' AND t.rowsecurity = true
GROUP BY t.schemaname, t.tablename
HAVING COUNT(p.policyname) = 0;

-- 3. Review all policies
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- 4. Check for functions with SECURITY DEFINER (elevated privileges)
SELECT
  proname AS function_name,
  prosecdef AS is_security_definer,
  provolatile AS volatility
FROM pg_proc
JOIN pg_namespace ON pg_namespace.oid = pg_proc.pronamespace
WHERE nspname = 'public' AND prosecdef = true;
```

### Key Rotation

```bash
# Rotate API keys from the Supabase Dashboard:
# Settings > API > Regenerate API Keys

# After rotation, update all environments:
# 1. CI/CD secrets in GitHub/GitLab
# 2. Environment variables in hosting platform (Vercel, Netlify, etc.)
# 3. Edge Function secrets
supabase secrets set SUPABASE_ANON_KEY=new-key --project-ref YOUR_PROJECT
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=new-key --project-ref YOUR_PROJECT

# 4. Restart/redeploy the application
```

### Content Security Policy

```typescript
// next.config.js -- configure security headers
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      `connect-src 'self' ${process.env.NEXT_PUBLIC_SUPABASE_URL} wss://*.supabase.co`,
      "img-src 'self' blob: data: *.supabase.co",
      "script-src 'self' 'unsafe-eval' 'unsafe-inline'",
      "style-src 'self' 'unsafe-inline'",
    ].join('; '),
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
]

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: securityHeaders,
      },
    ]
  },
}
```

## Cost Management

### Monitoring Usage

| Resource | Free Tier Limit | Pro Tier Limit | How to Monitor |
|---|---|---|---|
| Database | 500 MB | 8 GB (expandable) | Dashboard > Database > Disk Usage |
| Storage | 1 GB | 100 GB (expandable) | Dashboard > Storage > Usage |
| Bandwidth | 2 GB | 250 GB | Dashboard > Settings > Usage |
| Edge Functions | 500K invocations | 2M invocations | Dashboard > Edge Functions > Logs |
| Realtime | 200 concurrent | 500 concurrent | Dashboard > Realtime > Connections |
| Auth | 50K MAU | Unlimited | Dashboard > Auth > Users |

### Cost Optimization Tips

```sql
-- Find unused indexes (wasting space and slowing writes)
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find large tables that might need archiving
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size('public.' || tablename)) AS size,
  n_live_tup AS row_count
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size('public.' || tablename) DESC;

-- Archive old data to reduce active dataset
CREATE TABLE public.tasks_archive (LIKE public.tasks INCLUDING ALL);

INSERT INTO public.tasks_archive
SELECT * FROM public.tasks
WHERE status = 'done' AND updated_at < NOW() - INTERVAL '1 year';

DELETE FROM public.tasks
WHERE status = 'done' AND updated_at < NOW() - INTERVAL '1 year';
```

## Go-Live Checklist

Use this checklist before launching to production.

### Database

- [ ] RLS enabled on all tables with user data
- [ ] All RLS policies tested with multiple user roles
- [ ] Indexes added for all frequent query patterns
- [ ] Migrations tested against staging with production-like data
- [ ] Database functions use `SECURITY DEFINER` only where necessary
- [ ] `ANALYZE` run on all tables for accurate query planning

### Authentication

- [ ] Email confirmation enabled for signups
- [ ] Password policy enforced (minimum length, complexity)
- [ ] OAuth redirect URLs configured for production domain
- [ ] Site URL set to production domain in Auth settings
- [ ] Rate limiting configured for auth endpoints
- [ ] Service role key not exposed in client code

### Storage

- [ ] Private buckets used for user-uploaded files
- [ ] Storage policies created for all buckets
- [ ] File size limits configured per bucket
- [ ] MIME type restrictions set for upload buckets

### Edge Functions

- [ ] All secrets set with `supabase secrets set`
- [ ] CORS headers configured for production domain
- [ ] Webhook signatures verified for all external services
- [ ] Error handling returns appropriate status codes
- [ ] Functions tested with production-like load

### Infrastructure

- [ ] Environment variables set in hosting platform
- [ ] CI/CD pipeline tested end-to-end
- [ ] Automated backups enabled and tested
- [ ] Monitoring and alerting configured
- [ ] DNS and SSL configured for custom domain
- [ ] CDN enabled for storage assets

### Security

- [ ] API keys rotated from default values
- [ ] No secrets in client-side code or Git repository
- [ ] Content Security Policy headers configured
- [ ] HTTPS enforced everywhere
- [ ] Secret scanning enabled in CI
- [ ] Dependency audit passing with no critical vulnerabilities

## Post-Launch Operations

### Runbook Template

```markdown
## Incident Response

### High Error Rate
1. Check Supabase Dashboard > Logs for error patterns
2. Check pg_stat_activity for connection issues
3. Review recent deployments for regressions
4. Scale up if load-related; rollback if deployment-related

### Database Connection Exhaustion
1. Check active connections: SELECT count(*) FROM pg_stat_activity
2. Identify idle connections: SELECT * FROM pg_stat_activity WHERE state = 'idle'
3. Terminate idle connections if needed: SELECT pg_terminate_backend(pid)
4. Verify connection pooling is configured correctly

### Authentication Failures
1. Check Supabase Dashboard > Auth > Logs
2. Verify JWT secret has not changed
3. Check OAuth provider status pages
4. Verify redirect URLs are correct for the environment
```

### Regular Maintenance Schedule

| Task | Frequency | How |
|---|---|---|
| Review slow query log | Weekly | `pg_stat_statements` top queries by mean time |
| Check unused indexes | Monthly | Query `pg_stat_user_indexes` for `idx_scan = 0` |
| Rotate API keys | Quarterly | Dashboard > Settings > API |
| Test backup restore | Quarterly | Restore to a test environment |
| Review RLS policies | On schema changes | `pg_policies` audit |
| Update dependencies | Monthly | `npm audit` and `npm update` |
| Review Edge Function logs | Weekly | Dashboard > Edge Functions > Logs |

## Summary

In this chapter you prepared your Supabase application for production. You set up separate environments for development, staging, and production; built a CI/CD pipeline with GitHub Actions for automated migrations and deployments; implemented a safe migration strategy with rollback procedures; configured monitoring with health checks and alerting; established backup and disaster recovery procedures; tuned performance with connection pooling, caching, and indexing; hardened security with RLS audits, key rotation, and CSP headers; set up cost monitoring and optimization; and worked through a comprehensive go-live checklist.

## Key Takeaways

1. **Use separate Supabase projects** for staging and production -- never test against production data.
2. **Automate migrations and deployments** through CI/CD to eliminate manual errors.
3. **Never drop columns or tables directly** -- use a multi-step migration strategy.
4. **Monitor actively** with health checks, slow query logs, and connection tracking.
5. **Test backup restores regularly** -- a backup you have never restored is a backup you cannot trust.
6. **Audit RLS policies** on every schema change to prevent security regressions.
7. **Rotate keys quarterly** and never commit secrets to version control.
8. **Use the go-live checklist** before every production launch.

## Next Steps

Congratulations -- you have built, secured, and deployed a production-ready Supabase application. From here, consider adding analytics with PostHog or Plausible, implementing feature flags for gradual rollouts, setting up end-to-end testing with Playwright, and exploring Supabase's vector and AI capabilities for intelligent search and recommendations.

---

*Built with insights from the [Supabase](https://github.com/supabase/supabase) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `supabase`, `schemaname`, `name` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Production Deployment` as an operating subsystem inside **Supabase Tutorial: Building Modern Backend Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `secrets`, `tablename`, `checks` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Production Deployment` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `supabase`.
2. **Input normalization**: shape incoming data so `schemaname` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `name`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/supabase/supabase)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `supabase` and `schemaname` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Advanced Queries & RLS](07-advanced-queries.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
