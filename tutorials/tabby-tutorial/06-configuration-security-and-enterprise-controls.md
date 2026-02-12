---
layout: default
title: "Chapter 6: Configuration, Security, and Enterprise Controls"
nav_order: 6
parent: Tabby Tutorial
---

# Chapter 6: Configuration, Security, and Enterprise Controls

As Tabby moves from single-user setup to team deployment, security and policy controls become central.

## Learning Goals

- use `config.toml` as the primary behavior contract
- enforce authentication and network boundaries
- evaluate enterprise-only controls without vendor lock assumptions

## Configuration Priorities

| Priority | Why |
|:---------|:----|
| auth and token policy | protects API access boundaries |
| model endpoint policy | avoids accidental data egress |
| prompt/system behavior | enforces assistant behavior constraints |
| reverse proxy + TLS | secures external access |

## Example Prompt Policy

```toml
[answer]
system_prompt = """
You are Tabby for internal engineering support.
Prefer codebase-grounded answers and explicit uncertainty.
"""
```

## Access Controls to Plan

- SSO and enterprise identity integrations (where applicable)
- role and membership governance for multi-user instances
- explicit public/private network exposure policy

## Security Review Questions

1. which model providers receive source code content?
2. what audit trail exists for admin changes?
3. which roles can change indexing and model config?
4. how are secrets stored and rotated?

## Source References

- [Config TOML](https://tabby.tabbyml.com/docs/administration/config-toml)
- [Administration: Reverse Proxy](https://tabby.tabbyml.com/docs/administration/reverse-proxy)
- [Administration: SSO](https://tabby.tabbyml.com/docs/administration/sso)
- [Administration: User](https://tabby.tabbyml.com/docs/administration/user)

## Summary

You now have a concrete security checklist for moving Tabby into shared environments.

Next: [Chapter 7: Operations, Upgrades, and Observability](07-operations-upgrades-and-observability.md)
