---
layout: default
title: "Chapter 7: Security, Auth, and Governance"
nav_order: 7
parent: VibeSDK Tutorial
---

# Chapter 7: Security, Auth, and Governance

VibeSDK includes security controls across identity, secret handling, and abuse protection.

## Security Domains

| Domain | Controls |
|:-------|:---------|
| Authentication | email auth and OAuth providers |
| Session integrity | JWT signing and secret rotation |
| Secrets protection | encrypted secret storage patterns |
| Abuse prevention | API/auth rate limit bindings |
| Access control | allowlist patterns such as `ALLOWED_EMAIL` |

## Config Signals in Deployment

`wrangler.jsonc` typically includes:

- rate limiter bindings for API and auth paths
- secure bindings/vars for auth and provider credentials
- controlled feature toggles via platform capability vars

## Governance Practices

- separate dev, staging, and production credential scopes
- enforce minimum review standards for model/provider changes
- centralize audit logs for generation requests and deploy actions
- define data retention policies for generated artifacts and sessions

## Summary

You now understand the baseline controls required before multi-user rollout.

Next: [Chapter 8: Production Operations and Scaling](08-production-operations-and-scaling.md)
