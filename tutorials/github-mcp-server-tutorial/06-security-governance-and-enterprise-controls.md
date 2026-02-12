---
layout: default
title: "Chapter 6: Security, Governance, and Enterprise Controls"
nav_order: 6
parent: GitHub MCP Server Tutorial
---

# Chapter 6: Security, Governance, and Enterprise Controls

This chapter covers policy and governance controls needed for enterprise adoption.

## Learning Goals

- map GitHub MCP usage to organization policy controls
- understand where OAuth app, GitHub App, and PAT policies apply
- enforce SSO and least-privilege defaults
- separate first-party and third-party host governance implications

## Governance Layers

| Layer | Control Examples |
|:------|:------------------|
| host policy | MCP enable/disable controls in supported editors |
| app policy | OAuth app or GitHub App restrictions |
| token policy | fine-grained PAT restrictions and expiration |
| org enforcement | SSO and installation governance |

## Source References

- [Policies and Governance](https://github.com/github/github-mcp-server/blob/main/docs/policies-and-governance.md)
- [README: Token Security Best Practices](https://github.com/github/github-mcp-server/blob/main/README.md#token-security-best-practices)
- [GitHub Security Policy](https://github.com/github/github-mcp-server/blob/main/SECURITY.md)

## Summary

You now have a governance model for secure, policy-aligned GitHub MCP usage.

Next: [Chapter 7: Troubleshooting, Read-Only, and Lockdown Operations](07-troubleshooting-read-only-and-lockdown-operations.md)
