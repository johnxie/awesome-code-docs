---
layout: default
title: "Chapter 4: Authentication Models and Namespace Ownership"
nav_order: 4
parent: MCP Registry Tutorial
---

# Chapter 4: Authentication Models and Namespace Ownership

Authentication method and server-name namespace must align, or publishing is rejected.

## Learning Goals

- choose auth mode based on namespace strategy
- implement GitHub, DNS, or HTTP verification paths
- handle CI-friendly auth flows with least friction
- prevent namespace mismatch errors early

## Auth Decision Table

| Auth Method | Namespace Pattern | Typical Context |
|:------------|:------------------|:----------------|
| GitHub OAuth/OIDC | `io.github.<user-or-org>/*` | open-source repo publishers |
| DNS | reverse-domain namespace | owned domains with DNS control |
| HTTP | reverse-domain namespace | owned domains with `.well-known` control |
| OIDC admin exchange | admin workflows | registry operations |

## Practical Guardrail

Define server naming convention first, then standardize one primary auth path in docs and CI templates.

## Source References

- [Authentication Guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/authentication.mdx)
- [Registry Authorization Spec](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/registry-authorization.md)
- [Official Registry API - Authentication](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md#authentication)

## Summary

You now have a reliable mapping from namespace policy to authentication workflow.

Next: [Chapter 5: API Consumption, Subregistries, and Sync Strategies](05-api-consumption-subregistries-and-sync-strategies.md)
