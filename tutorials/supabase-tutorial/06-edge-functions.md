---
layout: default
title: "Chapter 6: Edge Functions"
parent: "Supabase Tutorial"
nav_order: 6
---

# Chapter 6: Edge Functions

Welcome to **Chapter 6: Edge Functions**. In this part of **Supabase Tutorial: Building Modern Backend Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In [Chapter 5](05-storage-management.md), you built a complete file management system with uploads, transformations, and access control. But some backend logic cannot live in the database or the client -- payment processing, third-party API calls, webhook handling, email sending, and data transformations all need a server-side runtime. Supabase Edge Functions are serverless TypeScript functions that run on Deno Deploy, executing close to your users at the edge. In this chapter you will create, test, and deploy Edge Functions; secure them with JWT verification; handle webhooks from services like Stripe; build custom API endpoints; connect functions to your database and storage; and set up scheduled tasks.

## How Edge Functions Work

Edge Functions run on Deno, a secure TypeScript/JavaScript runtime. They execute in isolated V8 environments with no cold-start file system access, and they can call your Supabase database, storage, and auth services using the standard client library.

```mermaid
flowchart TD
    A[Client / Webhook / Cron] -->|HTTP Request| B[Edge Function Runtime]
    B --> C[Deno Isolate]
    C --> D[Your Function Code]
    D --> E[Supabase Client]
    E --> F[Database]
    E --> G[Storage]
    E --> H[Auth]
    D --> I[Third-Party APIs]
    D --> J[Response to Caller]

    classDef trigger fill:#e1f5fe,stroke:#01579b
    classDef runtime fill:#f3e5f5,stroke:#4a148c
    classDef services fill:#e8f5e8,stroke:#1b5e20
    classDef external fill:#fff3e0,stroke:#ef6c00

    class A trigger
    class B,C,D runtime
    class E,F,G,H services
    class I,J external
```

### Edge Functions vs Database Functions

| Feature | Edge Functions | Database Functions (PL/pgSQL) |
|---|---|---|
| Runtime | Deno (TypeScript/JavaScript) | PostgreSQL |
| Use case | HTTP endpoints, webhooks, external APIs | Data transformations, triggers, RPC |
| Access | HTTP request/response | SQL queries and triggers |
| Third-party calls | Yes -- fetch, npm packages | Limited (pg_net extension) |
| Cold start | ~50-200ms | None (always running) |
| Timeout | 150s (default) | Configurable |
| Scaling | Automatic, global edge | Scales with database |

## Creating Your First Edge Function

### Scaffold and Structure

```bash
# Create a new Edge Function
supabase functions new hello-world

# This creates the following structure:
# supabase/functions/hello-world/index.ts
```

```
supabase/
  functions/
    hello-world/
      index.ts          # Main entry point
    send-email/
      index.ts
    process-payment/
      index.ts
    _shared/
      cors.ts           # Shared utilities (prefixed with _)
      supabase-client.ts
```

### Basic Function

```typescript
// supabase/functions/hello-world/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"

serve(async (req: Request) => {
  // Parse the request
  const { name } = await req.json()

  // Return a JSON response
  return new Response(
    JSON.stringify({ message: `Hello, ${name || 'World'}!` }),
    {
      headers: { "Content-Type": "application/json" },
      status: 200,
    }
  )
})
```

### Local Development

```bash
# Start functions locally (watches for changes)
supabase functions serve

# Serve a specific function
supabase functions serve hello-world --env-file .env.local

# Test with curl
curl -i --location --request POST \
  'http://localhost:54321/functions/v1/hello-world' \
  --header 'Authorization: Bearer YOUR_ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"name": "Supabase"}'
```

### Deployment

```bash
# Deploy a single function
supabase functions deploy hello-world --project-ref YOUR_PROJECT_REF

# Deploy all functions
supabase functions deploy --project-ref YOUR_PROJECT_REF

# Deploy with environment variables
supabase secrets set STRIPE_SECRET_KEY=sk_live_xxx --project-ref YOUR_PROJECT_REF
supabase functions deploy process-payment --project-ref YOUR_PROJECT_REF
```

## Shared Utilities

Create reusable modules in the `_shared` directory (the underscore prefix prevents deployment as a standalone function).

### CORS Handler

```typescript
// supabase/functions/_shared/cors.ts
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
}

export function handleCors(req: Request): Response | null {
  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }
  return null
}
```

### Supabase Client Factory

```typescript
// supabase/functions/_shared/supabase-client.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Client authenticated as the calling user (respects RLS)
export function createUserClient(req: Request) {
  const authHeader = req.headers.get('Authorization')
  if (!authHeader) throw new Error('Missing Authorization header')

  return createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    {
      global: {
        headers: { Authorization: authHeader },
      },
    }
  )
}

// Admin client that bypasses RLS (use with caution)
export function createAdminClient() {
  return createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  )
}
```

## Securing Edge Functions

### JWT Verification

```typescript
// supabase/functions/protected-action/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { corsHeaders, handleCors } from "../_shared/cors.ts"
import { createUserClient } from "../_shared/supabase-client.ts"

serve(async (req: Request) => {
  // Handle CORS preflight
  const corsResponse = handleCors(req)
  if (corsResponse) return corsResponse

  try {
    // Create a client authenticated as the calling user
    const supabase = createUserClient(req)

    // Verify the user is authenticated
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    // User is verified -- proceed with business logic
    const { data, error } = await supabase
      .from('tasks')
      .select('*')
      .eq('assignee_id', user.id)

    if (error) throw error

    return new Response(
      JSON.stringify({ tasks: data, user: user.email }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

### Calling Edge Functions from the Client

```typescript
// The Supabase client automatically sends the JWT
const { data, error } = await supabase.functions.invoke('protected-action', {
  body: { taskId: 42 },
})

if (error) {
  console.error('Function error:', error)
} else {
  console.log('Result:', data)
}
```

## Building a Payment Processing Function

```mermaid
sequenceDiagram
    participant Client
    participant Edge as Edge Function
    participant Stripe
    participant DB as PostgreSQL

    Client->>Edge: POST /process-payment { priceId, quantity }
    Edge->>Edge: Verify JWT
    Edge->>DB: Get user profile
    Edge->>Stripe: Create Checkout Session
    Stripe->>Edge: Return session URL
    Edge->>Client: Return checkout URL
    Client->>Stripe: Redirect to Checkout
    Stripe->>Edge: Webhook: checkout.session.completed
    Edge->>DB: Update subscription status
    Edge->>Stripe: Return 200 OK
```

### Payment Function

```typescript
// supabase/functions/create-checkout/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import Stripe from "https://esm.sh/stripe@13?target=deno"
import { corsHeaders, handleCors } from "../_shared/cors.ts"
import { createUserClient } from "../_shared/supabase-client.ts"

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
})

serve(async (req: Request) => {
  const corsResponse = handleCors(req)
  if (corsResponse) return corsResponse

  try {
    const supabase = createUserClient(req)
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const { priceId } = await req.json()

    // Check if user already has a Stripe customer ID
    const { data: profile } = await supabase
      .from('profiles')
      .select('stripe_customer_id')
      .eq('id', user.id)
      .single()

    let customerId = profile?.stripe_customer_id

    // Create Stripe customer if needed
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        metadata: { supabase_user_id: user.id },
      })
      customerId = customer.id

      // Save customer ID to profile
      await supabase
        .from('profiles')
        .update({ stripe_customer_id: customerId })
        .eq('id', user.id)
    }

    // Create checkout session
    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      success_url: `${req.headers.get('origin')}/billing?success=true`,
      cancel_url: `${req.headers.get('origin')}/billing?canceled=true`,
      metadata: { supabase_user_id: user.id },
    })

    return new Response(
      JSON.stringify({ url: session.url }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

## Handling Webhooks

### Stripe Webhook Handler

```typescript
// supabase/functions/stripe-webhook/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import Stripe from "https://esm.sh/stripe@13?target=deno"
import { createAdminClient } from "../_shared/supabase-client.ts"

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
})

const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET')!

serve(async (req: Request) => {
  const signature = req.headers.get('stripe-signature')
  if (!signature) {
    return new Response('Missing signature', { status: 400 })
  }

  try {
    const body = await req.text()

    // Verify the webhook signature
    const event = stripe.webhooks.constructEvent(body, signature, webhookSecret)

    const supabase = createAdminClient()

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session
        const userId = session.metadata?.supabase_user_id

        if (userId) {
          await supabase
            .from('profiles')
            .update({
              subscription_status: 'active',
              subscription_id: session.subscription,
            })
            .eq('id', userId)
        }
        break
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription
        const customerId = subscription.customer as string

        // Find user by Stripe customer ID
        const { data: profile } = await supabase
          .from('profiles')
          .select('id')
          .eq('stripe_customer_id', customerId)
          .single()

        if (profile) {
          await supabase
            .from('profiles')
            .update({
              subscription_status: 'canceled',
              subscription_id: null,
            })
            .eq('id', profile.id)
        }
        break
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice
        const customerId = invoice.customer as string

        const { data: profile } = await supabase
          .from('profiles')
          .select('id')
          .eq('stripe_customer_id', customerId)
          .single()

        if (profile) {
          await supabase
            .from('profiles')
            .update({ subscription_status: 'past_due' })
            .eq('id', profile.id)
        }
        break
      }

      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    return new Response(JSON.stringify({ received: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    console.error('Webhook error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
```

## Email Sending Function

```typescript
// supabase/functions/send-email/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { corsHeaders, handleCors } from "../_shared/cors.ts"
import { createUserClient } from "../_shared/supabase-client.ts"

serve(async (req: Request) => {
  const corsResponse = handleCors(req)
  if (corsResponse) return corsResponse

  try {
    const supabase = createUserClient(req)
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const { to, subject, html } = await req.json()

    // Send email via Resend (or any email provider)
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('RESEND_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'noreply@yourdomain.com',
        to: [to],
        subject,
        html,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || 'Failed to send email')
    }

    const result = await response.json()

    // Log the email in the database
    await supabase.from('email_logs').insert({
      user_id: user.id,
      to_address: to,
      subject,
      status: 'sent',
      provider_id: result.id,
    })

    return new Response(
      JSON.stringify({ success: true, id: result.id }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

## Database Trigger to Edge Function

You can invoke an Edge Function automatically when a database event occurs using `pg_net`.

```sql
-- Enable the pg_net extension
CREATE EXTENSION IF NOT EXISTS pg_net;

-- Function that calls an Edge Function when a new order is created
CREATE OR REPLACE FUNCTION public.notify_new_order()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM net.http_post(
    url := CONCAT(
      current_setting('app.settings.supabase_url'),
      '/functions/v1/process-order'
    ),
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', CONCAT('Bearer ', current_setting('app.settings.service_role_key'))
    ),
    body := jsonb_build_object(
      'order_id', NEW.id,
      'user_id', NEW.user_id,
      'total', NEW.total
    )
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_new_order
  AFTER INSERT ON public.orders
  FOR EACH ROW
  EXECUTE FUNCTION public.notify_new_order();
```

## Scheduled Tasks

### Using pg_cron (Database-Level)

```sql
-- Enable the pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule an Edge Function call every hour
SELECT cron.schedule(
  'hourly-cleanup',
  '0 * * * *',  -- Every hour
  $$
  SELECT net.http_post(
    url := 'https://YOUR_PROJECT.supabase.co/functions/v1/cleanup-expired',
    headers := '{"Authorization": "Bearer YOUR_SERVICE_ROLE_KEY", "Content-Type": "application/json"}'::jsonb,
    body := '{}'::jsonb
  );
  $$
);

-- List scheduled jobs
SELECT * FROM cron.job;

-- Remove a scheduled job
SELECT cron.unschedule('hourly-cleanup');
```

### Cleanup Function

```typescript
// supabase/functions/cleanup-expired/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createAdminClient } from "../_shared/supabase-client.ts"

serve(async (req: Request) => {
  // Verify this is called by a trusted source
  const authHeader = req.headers.get('Authorization')
  if (authHeader !== `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const supabase = createAdminClient()

  // Delete expired sessions
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

  const { count: deletedSessions } = await supabase
    .from('sessions')
    .delete()
    .lt('last_active_at', thirtyDaysAgo.toISOString())

  // Clean up orphaned storage files
  const { data: orphanedFiles } = await supabase
    .from('upload_logs')
    .select('path')
    .eq('status', 'orphaned')
    .lt('created_at', thirtyDaysAgo.toISOString())

  if (orphanedFiles && orphanedFiles.length > 0) {
    const paths = orphanedFiles.map(f => f.path)
    await supabase.storage.from('documents').remove(paths)
  }

  return new Response(
    JSON.stringify({
      deleted_sessions: deletedSessions,
      cleaned_files: orphanedFiles?.length || 0,
    }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  )
})
```

## Environment Variables and Secrets

```bash
# Set secrets for your project
supabase secrets set STRIPE_SECRET_KEY=sk_live_xxx
supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_xxx
supabase secrets set RESEND_API_KEY=re_xxx

# List current secrets
supabase secrets list

# Remove a secret
supabase secrets unset STRIPE_SECRET_KEY

# For local development, use a .env.local file
# supabase/functions/.env.local
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_test_xxx
RESEND_API_KEY=re_test_xxx
```

## Troubleshooting Edge Functions

| Problem | Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Missing or invalid JWT | Include `Authorization: Bearer <token>` header |
| `403 Forbidden` | Function requires service role | Use `SUPABASE_SERVICE_ROLE_KEY` for admin calls |
| CORS errors | Missing CORS headers | Import and return `corsHeaders` on every response; handle OPTIONS |
| Cold start latency | First invocation after idle | Keep functions lightweight; avoid large dependencies |
| Timeout (504) | Function takes too long | Optimize DB queries; add timeouts to external API calls |
| Import errors | Wrong Deno import URL | Use `https://esm.sh/` for npm packages; pin versions |
| Environment variable missing | Secret not set | Run `supabase secrets set VAR=value` |
| Build failure on deploy | TypeScript errors | Test locally with `supabase functions serve` first |

## Summary

In this chapter you built serverless backend logic with Supabase Edge Functions. You created and deployed functions with the CLI, set up shared utilities for CORS and Supabase clients, secured functions with JWT verification, built a complete Stripe payment integration with checkout and webhooks, implemented an email sending function, triggered Edge Functions from database events using `pg_net`, set up scheduled tasks with `pg_cron`, and managed environment secrets.

## Key Takeaways

1. **Edge Functions run on Deno** -- use ES module imports from `https://esm.sh/` and Deno standard library.
2. **Always handle CORS** by returning appropriate headers on every response and handling OPTIONS preflight requests.
3. **Use the user client for RLS-aware queries** and the admin client only when you need to bypass RLS.
4. **Verify webhook signatures** before processing events from third-party services.
5. **Store secrets with `supabase secrets set`** -- never hard-code API keys in function code.
6. **Use `pg_net` and `pg_cron`** to trigger and schedule Edge Function calls from the database.
7. **Keep functions lightweight** -- minimize dependencies and bundle size to reduce cold start latency.

## Next Steps

Your application now has custom backend logic at the edge. In [Chapter 7: Advanced Queries & RLS](07-advanced-queries.md), you will master complex queries, full-text search, cursor-based pagination, multi-tenant RLS patterns, and database performance optimization.

---

*Built with insights from the [Supabase](https://github.com/supabase/supabase) project.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `supabase`, `error`, `functions` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Edge Functions` as an operating subsystem inside **Supabase Tutorial: Building Modern Backend Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `headers`, `json`, `user` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Edge Functions` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `supabase`.
2. **Input normalization**: shape incoming data so `error` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `functions`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/supabase/supabase)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `supabase` and `error` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Storage & File Management](05-storage-management.md)
- [Next Chapter: Chapter 7: Advanced Queries & RLS](07-advanced-queries.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
