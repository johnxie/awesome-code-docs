---
layout: default
title: "Chapter 7: Configuration and Security"
nav_order: 7
parent: HAPI Tutorial
---

# Chapter 7: Configuration and Security

HAPI security depends on disciplined token management, environment separation, and controlled exposure.

## Key Configuration Domains

| Domain | Examples |
|:-------|:---------|
| auth/token | `CLI_API_TOKEN`, access token settings |
| endpoint config | `HAPI_API_URL`, listen host/port, `publicUrl` |
| notifications | Telegram token/settings |
| optional voice | ElevenLabs key and agent settings |

## Hardening Checklist

- keep secrets outside version control
- rotate tokens on schedule and after incidents
- segregate dev/stage/prod hub deployments
- restrict externally reachable surfaces to required endpoints

## Governance Controls

- audit log review for auth failures and approval anomalies
- machine offboarding process with token revocation
- periodic configuration drift audits against baseline policy

## Summary

You now have a security baseline for moving HAPI from personal setup to team deployment.

Next: [Chapter 8: Production Operations](08-production-operations.md)
