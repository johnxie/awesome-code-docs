---
layout: default
title: "Chapter 6: Edge Functions"
parent: "Supabase Tutorial"
nav_order: 6
---

# Chapter 6: Edge Functions

Extend Supabase with serverless APIs, hooks, and middleware.

## Objectives
- Create and deploy Edge Functions
- Secure functions with JWT verification
- Use functions for webhooks and scheduled tasks
- Connect functions to database and storage

## Create Function
```bash
supabase functions new process-upload
```

`supabase/functions/process-upload/index.ts`:
```typescript
import { createClient } from '@supabase/supabase-js'
import { serve } from "https://deno.land/std/http/server.ts"

serve(async (req) => {
  const supabase = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
  const payload = await req.json()

  // Example: write an audit log
  await supabase.from('upload_logs').insert({ path: payload.path, user_id: payload.user_id })

  return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" } })
})
```

## Deploy Function
```bash
supabase functions deploy process-upload --project-ref YOUR_PROJECT
```

## Protect with JWT
- Validate `Authorization` header; reject missing/invalid tokens
- Use service role only inside the function, not in clients

## Webhooks
- Receive events from Stripe/GitHub; validate signatures
- Write normalized events into Postgres; trigger downstream processing

## Scheduled Tasks
- Use external scheduler (GitHub Actions, cron) to call functions periodically

## Troubleshooting
- 401/403: verify JWT audience; ensure correct project ref
- Cold starts: keep functions lightweight; avoid heavy deps
- Timeouts: optimize DB calls; add timeouts and retries

## Performance Notes
- Use connection pooling for Postgres via Supabase client
- Avoid large bundle sizes; tree-shake dependencies

## Security Notes
- Store secrets in function environment variables
- Validate all inbound payloads; log suspicious events

## Next Steps
Chapter 7 covers advanced queries, RLS hardening, and performance tuning.
