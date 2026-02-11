---
layout: default
title: "Chapter 7: Security, Auth, and Governance"
nav_order: 7
parent: VibeSDK Tutorial
---

# Chapter 7: Security, Auth, and Governance

VibeSDK security spans identity, secret handling, abuse controls, and operational policy.

## Security Domains

| Domain | Controls |
|:-------|:---------|
| identity | OAuth/email auth and session governance |
| session integrity | JWT controls and rotation |
| secret management | encrypted storage and scoped env vars |
| abuse protection | API/auth rate limit bindings |
| access policy | allowlists and environment separation |

## Deployment-Level Controls

`wrangler.jsonc` commonly includes:

- API/auth rate limiter bindings
- secure vars for provider/auth credentials
- feature capability toggles and route controls

## Governance Practices

- separate dev/stage/prod credentials and bindings
- require review for provider/model config changes
- retain audit trails for generation and deploy actions
- define retention and deletion policies for session artifacts

## Practical Runbook Checks

| Check | Frequency |
|:------|:----------|
| token/secret rotation audit | monthly |
| permission/policy drift review | bi-weekly |
| auth failure anomaly review | daily |
| emergency rollback drill | quarterly |

## Summary

You now have a security and governance baseline for multi-user VibeSDK rollout.

Next: [Chapter 8: Production Operations and Scaling](08-production-operations-and-scaling.md)
