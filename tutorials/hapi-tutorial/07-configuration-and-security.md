---
layout: default
title: "Chapter 7: Configuration and Security"
nav_order: 7
parent: HAPI Tutorial
---

# Chapter 7: Configuration and Security

HAPI security depends on token management, network boundaries, and environment discipline.

## Critical Configuration Areas

| Area | Examples |
|:-----|:---------|
| hub auth | `CLI_API_TOKEN`, access token settings |
| endpoint config | `HAPI_API_URL`, host/port/public URL values |
| notification integration | Telegram bot and notification toggles |
| voice integration | ElevenLabs key/agent settings (if used) |

## Hardening Practices

- keep tokens out of source control
- scope public exposure to necessary interfaces only
- rotate tokens and integration secrets on schedule
- separate dev/stage/prod hub deployments

## Governance Controls

- least-privilege machine access
- audit logging for auth and approvals
- documented offboarding and token revocation paths

## Summary

You now have a baseline security model for operating HAPI beyond personal use.

Next: [Chapter 8: Production Operations](08-production-operations.md)
