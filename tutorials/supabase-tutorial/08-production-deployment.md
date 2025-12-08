---
layout: default
title: "Chapter 8: Production Deployment"
parent: "Supabase Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Ship Supabase apps with confidence: scaling, monitoring, security, and backups.

## Objectives
- Configure environments and secrets
- Set up monitoring and logging
- Plan backups and recovery
- Harden security and cost controls

## Environment Management
- Separate dev/stage/prod projects
- Store keys in env vars, never in repos
- Use service role only server-side; rotate regularly

## Observability
- Enable database logs and log drains
- Monitor p95 latency for auth, db, storage
- Create alerts for error rates, failed logins, storage 4xx/5xx

## Backups & DR
- Enable automated backups; test restore quarterly
- Export critical tables (e.g., users, profiles) for off-site backups
- Document recovery steps; run drills

## Performance & Scaling
- Connection pooling via Supavisor
- Caching layer (CDN for storage, HTTP cache for APIs)
- Use pagination and proper indexes to reduce load

## Security Hardening
- Enforce RLS on user data; default deny
- HTTPS everywhere; HSTS enabled
- Least privilege keys for CI/CD and backend
- Secret scanning in CI

## Cost Controls
- Clean unused storage; lifecycle policies
- Monitor row counts and function invocations
- Right-size instances; archive cold data

## Go-Live Checklist
- [ ] RLS enabled and tested on all user tables
- [ ] Keys rotated; no secrets in client bundles
- [ ] Backups enabled and restore tested
- [ ] Monitoring/alerts configured
- [ ] Load test completed on critical flows

## Next Steps
Iterate on performance, security, and developer experience; add analytics (PostHog) for product insights.
