---
layout: default
title: "Chapter 1: Getting Started and Deployment Paths"
nav_order: 1
parent: VibeSDK Tutorial
---

# Chapter 1: Getting Started and Deployment Paths

This chapter gets `cloudflare/vibesdk` running in a local development loop, then maps the path to production-style deployment.

## Learning Goals

By the end of this chapter, you should be able to:

- pick the right deployment mode for your team stage
- complete a first-time setup without hidden blockers
- validate the platform end-to-end after bootstrapping
- prepare environment variables and Cloudflare resources for future production rollout

## Deployment Modes

| Mode | Best For | Required Inputs | Tradeoffs |
|:-----|:---------|:----------------|:----------|
| local-only | architecture changes and feature development | Node.js 18+, Bun, Docker, local env vars | fast iteration, but no production route checks |
| deploy-button bootstrap | fastest hosted trial and stakeholder demos | Cloudflare account + setup wizard | minimal setup effort, less explicit infra control |
| scripted deployment | repeatable team environments and CI | managed secrets, explicit `wrangler` strategy, rollout process | highest control, highest operational overhead |

## Prerequisites You Should Verify First

- Node.js 18+
- Bun installed (`bun --version`)
- Docker Desktop or equivalent runtime running
- Cloudflare account with API token permissions for Workers, KV, D1, R2, and Containers
- optional custom domain (recommended for production deployment and nicer preview URLs)

If you are using Cloudflare WARP and local previews fail, upstream docs note this can interfere with anonymous Cloudflared tunnels. Disable full-mode WARP while debugging local previews.

## Fast Setup Path

```bash
bun install
bun run setup
bun run db:migrate:local
bun run dev
```

`bun run setup` is the most important step. It collects credentials, creates/binds resources, and writes local configuration files.

## What the Setup Script Configures

| Area | Typical Outputs |
|:-----|:----------------|
| account identity | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` |
| secrets baseline | `JWT_SECRET`, `WEBHOOK_SECRET`, encryption-related vars |
| AI routing | provider keys, optional AI Gateway token plumbing |
| storage/bindings | KV, D1, R2 resource IDs and `wrangler.jsonc` updates |
| local runtime | `.dev.vars`, local migration readiness |

## Environment Variable Strategy

Split variables into explicit tiers early:

- local dev: `.dev.vars`
- production deploy: `.prod.vars` or your managed secret store
- CI: pipeline-bound secrets with least privilege

Avoid reusing production tokens in local development.

## First Validation Checklist

After startup, validate all four before moving on:

1. authentication flow works (email or OAuth path)
2. generation starts and phase/status updates stream in UI
3. preview URL loads generated app
4. a test deploy/export path succeeds (or fails with clear, expected config messages)

## Common Early Failures and Fixes

| Failure | Typical Root Cause | First Fix |
|:--------|:-------------------|:----------|
| D1/KV/R2 unauthorized | missing API token permissions or plan limits | regenerate token with required scopes, then rerun setup |
| preview URL unavailable | Cloudflared tunnel timing or network interference | wait/retry, disable WARP full mode, confirm Docker runtime |
| generation fails quickly | model/provider mismatch in config | verify keys and provider mapping in `worker/agents/inferutils/config.ts` |
| deploy-from-chat unavailable | missing custom domain + dispatch setup | complete initial remote deployment and domain wiring |

## Recommended Graduation Path

1. run local-only until generation and preview loops are stable
2. deploy a staging instance with production-like bindings
3. enable controlled user access and monitor runtime behavior
4. promote to production after cost, reliability, and governance checks pass

## Source References

- [VibeSDK Setup Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/setup.md)
- [VibeSDK Repository](https://github.com/cloudflare/vibesdk)

## Summary

You now have a practical bootstrap playbook for VibeSDK and a clear path from local development to managed deployment.

Next: [Chapter 2: System Architecture](02-system-architecture.md)
