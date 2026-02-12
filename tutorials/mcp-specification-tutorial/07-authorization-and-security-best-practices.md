---
layout: default
title: "Chapter 7: Authorization and Security Best Practices"
nav_order: 7
parent: MCP Specification Tutorial
---

# Chapter 7: Authorization and Security Best Practices

This chapter converts MCP auth and threat guidance into an implementation playbook.

## Learning Goals

- implement OAuth discovery and scope negotiation flows correctly
- separate stdio credential handling from HTTP authorization flows
- mitigate confused deputy, token passthrough, and session hijacking classes
- align server/client/operator responsibilities with the trust model

## Security Control Baseline

| Threat Class | Required Direction |
|:-------------|:-------------------|
| Confused deputy | enforce per-client consent before third-party auth hops |
| Token passthrough | never accept tokens not issued for the MCP server |
| Session hijacking | secure and bind session identifiers, verify every inbound request |
| Scope creep | request least privilege and honor challenge scope guidance |

## Authorization Implementation Notes

- support both `WWW-Authenticate`-based discovery and `.well-known` fallback
- parse and honor `scope` challenges from unauthorized responses
- support OAuth metadata discovery priority order for issuer URLs with/without paths
- for stdio-based local servers, do not force HTTP OAuth flow patterns that do not apply

## Source References

- [Authorization Specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/authorization.mdx)
- [Security Best Practices](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/security_best_practices.mdx)
- [Security Policy (Trust Model)](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md)
- [Security Tutorial - Authorization](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/tutorials/security/authorization.mdx)

## Summary

You now have a concrete security baseline for authorization, session handling, and operator controls.

Next: [Chapter 8: Governance, SEPs, and Contribution Workflow](08-governance-seps-and-contribution-workflow.md)
