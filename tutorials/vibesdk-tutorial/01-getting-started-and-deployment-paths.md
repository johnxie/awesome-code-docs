---
layout: default
title: "Chapter 1: Getting Started and Deployment Paths"
nav_order: 1
parent: VibeSDK Tutorial
---

# Chapter 1: Getting Started and Deployment Paths

This chapter gets VibeSDK running in a local development loop and explains when to use hosted deployment.

## Deployment Modes

| Mode | Best For | Key Requirement |
|:-----|:---------|:----------------|
| local development | platform customization and debugging | Node 18+, Bun, Docker |
| deploy-button bootstrap | fast hosted trial | Cloudflare paid Workers setup |
| scripted deployment | repeatable team environments | managed env vars and CI controls |

## Local Setup Workflow

```bash
bun install
bun run setup
bun run db:migrate:local
bun run dev
```

The setup flow configures account IDs, keys, resource bindings, and local vars.

## Core Configuration Areas

| Area | Typical Variables |
|:-----|:------------------|
| cloud identity | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` |
| security | `JWT_SECRET`, `WEBHOOK_SECRET`, `SECRETS_ENCRYPTION_KEY` |
| AI providers | `GOOGLE_AI_STUDIO_API_KEY` and provider-specific keys |
| runtime shape | `CUSTOM_DOMAIN`, `MAX_SANDBOX_INSTANCES`, `SANDBOX_INSTANCE_TYPE` |

## First Validation Checklist

- chat interface loads after auth
- generation request emits phase progression
- preview URL resolves and app runs
- export/deploy flow completes for a sample app

## Common Early Failures

- missing Cloudflare permissions for D1/KV/R2/containers
- domain/certificate mismatch for preview routes
- model configuration mismatch with selected provider strategy

## Summary

You now have a repeatable setup baseline for VibeSDK development and deployment.

Next: [Chapter 2: System Architecture](02-system-architecture.md)
