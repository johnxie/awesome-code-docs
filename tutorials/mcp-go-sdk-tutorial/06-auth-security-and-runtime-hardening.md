---
layout: default
title: "Chapter 6: Auth, Security, and Runtime Hardening"
nav_order: 6
parent: MCP Go SDK Tutorial
---

# Chapter 6: Auth, Security, and Runtime Hardening

This chapter turns Go SDK auth features into a production hardening baseline.

## Learning Goals

- apply bearer-token enforcement middleware to streamable HTTP endpoints
- expose OAuth protected resource metadata correctly
- manage session and request verification defensively
- align runtime controls with MCP security best practices

## Hardening Baseline

| Control | Go SDK Path |
|:--------|:------------|
| bearer token verification | `auth.RequireBearerToken` |
| protected resource metadata endpoint | `auth.ProtectedResourceMetadataHandler` |
| token context propagation | `auth.TokenInfoFromContext` and request extras |
| session defense | secure IDs + inbound request verification |

## Deployment Checklist

- enforce auth on all MCP HTTP endpoints except explicit public metadata routes
- configure CORS intentionally for metadata and MCP endpoints
- validate scopes for tool categories with different blast radius
- log authentication failures with actionable context

## Source References

- [Protocol Authorization](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md#authorization)
- [Auth Middleware Example](https://github.com/modelcontextprotocol/go-sdk/blob/main/examples/server/auth-middleware/README.md)
- [Security Policy](https://github.com/modelcontextprotocol/go-sdk/blob/main/SECURITY.md)

## Summary

You now have an implementation-level auth and security baseline for Go MCP deployments.

Next: [Chapter 7: Testing, Troubleshooting, and Rough Edges](07-testing-troubleshooting-and-rough-edges.md)
