---
layout: default
title: "Chapter 1: Getting Started and Deployment Paths"
nav_order: 1
parent: VibeSDK Tutorial
---

# Chapter 1: Getting Started and Deployment Paths

This chapter gets VibeSDK running either locally for development or via Cloudflare deployment for team usage.

## Two Onboarding Paths

| Path | Best For | Core Requirement |
|:-----|:---------|:-----------------|
| Local development | Platform customization and debugging | Node.js 18+, Bun, Docker |
| Deploy button | Fast hosted environment setup | Cloudflare paid Workers setup |

## Local Setup Flow

```bash
bun install
bun run setup
bun run db:migrate:local
bun run dev
```

The setup script configures Cloudflare account values, API keys, and resource IDs into your local env files.

## Required Environment Areas

| Area | Examples |
|:-----|:---------|
| Cloudflare identity | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` |
| Security | `JWT_SECRET`, `WEBHOOK_SECRET`, `SECRETS_ENCRYPTION_KEY` |
| AI providers | `GOOGLE_AI_STUDIO_API_KEY` and/or provider-specific keys |
| Domain/routing | `CUSTOM_DOMAIN`, dispatch namespace values |

## Deploy-to-Cloudflare Path

1. trigger the deploy button from the upstream repository
2. set required variables and account bindings
3. configure wildcard/custom-domain routing for previews
4. validate app generation and preview URLs

If you use a first-level subdomain model (for example `abc.xyz.com`), certificate and DNS setup must be aligned before previews resolve.

## First Validation Checklist

- authenticated user can open the chat workspace
- generation request produces phase events
- preview container URL becomes reachable
- generated app can be deployed/exported

## Summary

You now have a working baseline environment and a repeatable setup checklist.

Next: [Chapter 2: System Architecture](02-system-architecture.md)
