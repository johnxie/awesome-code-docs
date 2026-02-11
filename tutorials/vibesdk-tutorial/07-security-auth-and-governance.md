---
layout: default
title: "Chapter 7: Security, Auth, and Governance"
nav_order: 7
parent: VibeSDK Tutorial
---

# Chapter 7: Security, Auth, and Governance

VibeSDK security is a cross-layer concern: identity, secret management, execution controls, and policy enforcement all matter.

## Learning Goals

By the end of this chapter, you should be able to:

- define a baseline security posture for multi-user VibeSDK environments
- separate auth, token, and secret responsibilities clearly
- design governance checks for model/provider and deployment changes
- prepare recurring operational audits and incident drills

## Security Domains

| Domain | Core Controls |
|:-------|:--------------|
| identity and access | OAuth/email auth flows, session guardrails, role-aware endpoints |
| token/session integrity | JWT signing controls, token rotation cadence, revocation paths |
| secret management | least-privilege API keys, env isolation, secure secret distribution |
| abuse prevention | rate limits, quota caps, workload isolation |
| change governance | review gates for model routing, deployment bindings, policy updates |

## Deployment-Level Security Controls

At minimum, enforce:

- separate credentials for dev/stage/prod
- explicit Cloudflare API token scopes (avoid overbroad tokens)
- environment-specific rate-limit bindings
- clear default-deny behavior for sensitive operations

## Governance Practices That Scale

1. require review for changes in `worker/agents/inferutils/config.ts`
2. log deployment and generation actions with actor identity
3. document retention/deletion policy for generated artifacts and logs
4. tie emergency rollback procedures to named on-call owners

## Security Runbook Checks

| Check | Frequency | Owner |
|:------|:----------|:------|
| secret/token rotation audit | monthly | platform security |
| permission drift review | bi-weekly | platform engineering |
| auth anomaly triage | daily | on-call engineer |
| rollback simulation | quarterly | incident response team |

## High-Risk Mistakes to Avoid

- sharing production API tokens in developer-local environments
- enabling broad provider access without per-environment controls
- skipping review on model/provider fallback changes
- missing retention policies for sensitive generation artifacts

## Source References

- [VibeSDK Setup Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/setup.md)
- [VibeSDK LLM Developer Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/llm.md)

## Summary

You now have a practical security and governance baseline for operating VibeSDK beyond a single-user demo setup.

Next: [Chapter 8: Production Operations and Scaling](08-production-operations-and-scaling.md)
