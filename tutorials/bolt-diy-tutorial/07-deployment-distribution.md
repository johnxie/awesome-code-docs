---
layout: default
title: "Chapter 7: Deployment and Distribution"
nav_order: 7
parent: Bolt.diy Tutorial
---

# Chapter 7: Deployment and Distribution

bolt.diy supports multiple delivery targets. This chapter helps you select the right one for your audience, constraints, and operational maturity.

## Deployment Targets in Practice

Project documentation and scripts indicate support for:

- web deployment paths (for example Vercel, Netlify, GitHub Pages style workflows)
- containerized self-hosted runtime
- desktop distribution via Electron build flow

## Decision Matrix

| Target | Best For | Strengths | Tradeoffs |
|:-------|:---------|:----------|:----------|
| managed web hosting | internal demos and broad access | fastest sharing and iteration | tighter platform/runtime constraints |
| self-hosted Docker | security-conscious teams | runtime control and network policy alignment | higher ops overhead |
| desktop (Electron) | local-first users | local environment and offline-friendly workflows | update and packaging complexity |

## Pre-Deployment Hardening

Before shipping any target:

1. pin provider defaults and fallbacks
2. enforce environment-specific secret injection
3. run smoke tests for generation + diff + validation loop
4. document rollback command path

## Environment Strategy

Use explicit config partitions:

- `dev`: broad experimentation, low blast radius
- `stage`: production-like configuration for final validation
- `prod`: locked policies, guarded credentials, audit logging

Never reuse dev credentials in production.

## Container Path (Recommended Baseline for Teams)

A container baseline reduces machine drift and supports policy controls:

- versioned image build
- fixed runtime dependencies
- predictable startup scripts
- easier infra handoff to platform teams

### Container release checklist

- image pinned by digest/tag
- runtime env vars validated at startup
- health endpoint or smoke check available
- logs exported to central collector

## Web Deployment Path

Choose this when onboarding speed matters most.

Minimum controls:

- CI-gated deployment
- secret configuration in hosting platform
- environment-specific base URLs and provider settings
- rollback to prior release artifact

## Desktop Distribution Path

Electron workflows are useful for local-first operator experience.

Controls to add:

- signed artifact strategy where applicable
- update channel policy (stable/beta)
- runtime permission and secure storage review
- crash and telemetry visibility (privacy-aware)

## Release Process Template

```text
1) Cut release branch
2) Run docs + tests + smoke checks
3) Build target artifact (web/container/desktop)
4) Deploy to stage
5) Validate task loop end-to-end
6) Promote to production
7) Monitor for regressions and rollback triggers
```

## Rollback Design

For each target, define rollback before first production launch:

- web: previous deployment alias
- container: previous image tag + config set
- desktop: prior stable version and update channel fallback

## Chapter Summary

You now have a deployment framework that aligns target choice with:

- team maturity
- compliance and control needs
- operational cost and complexity

Next: [Chapter 8: Production Operations](08-production-operations.md)
