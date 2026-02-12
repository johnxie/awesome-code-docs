---
layout: default
title: "Chapter 3: Authentication and Token Strategy"
nav_order: 3
parent: GitHub MCP Server Tutorial
---

# Chapter 3: Authentication and Token Strategy

This chapter covers secure authentication choices and scope minimization.

## Learning Goals

- choose between OAuth and PAT approaches by context
- minimize scopes while preserving required functionality
- understand scope filtering behavior in different auth flows
- reduce token handling risk in local and shared environments

## Auth Decision Matrix

| Method | Typical Use | Security Consideration |
|:-------|:------------|:-----------------------|
| OAuth (remote) | interactive hosts with app support | strong user flow, host-dependent behavior |
| fine-grained PAT | local/portable compatibility | scope discipline required |
| classic PAT | legacy compatibility only | broader risk surface |

## Token Hygiene Baseline

- prefer fine-grained PATs
- scope to required repos and operations only
- avoid hardcoding in committed config
- rotate credentials on schedule or incident

## Source References

- [README: Token Security Best Practices](https://github.com/github/github-mcp-server/blob/main/README.md#token-security-best-practices)
- [Server Configuration: Scope Filtering](https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md#scope-filtering)
- [Policies and Governance](https://github.com/github/github-mcp-server/blob/main/docs/policies-and-governance.md)

## Summary

You now have an authentication strategy that balances compatibility and risk.

Next: [Chapter 4: Toolsets, Tools, and Dynamic Discovery](04-toolsets-tools-and-dynamic-discovery.md)
