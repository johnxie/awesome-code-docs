---
layout: default
title: "Chapter 7: Security, Runtime Controls, and Production Hardening"
nav_order: 7
parent: MCP Use Tutorial
---

# Chapter 7: Security, Runtime Controls, and Production Hardening

MCP systems are high-power by nature, so production readiness depends on hard runtime boundaries.

## Learning Goals

- apply API key and secret management best practices
- constrain agent tool and network reach by design
- configure allowed origins and environment-aware security defaults
- define production deployment controls for server runtimes

## Hardening Checklist

| Area | Control |
|:-----|:--------|
| Secrets | environment variables or managed secret stores |
| Tool scope | disallow dangerous tools by default |
| Origin/network | explicit allowlists in production |
| Runtime | non-root containers, rate limits, auth middleware |

## Source References

- [TypeScript Security Best Practices](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/development/security.mdx)
- [TypeScript Server Configuration](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/server/configuration.mdx)
- [Python Development Security](https://github.com/mcp-use/mcp-use/blob/main/docs/python/development/security.mdx)

## Summary

You now have a pragmatic hardening baseline for mcp-use deployments.

Next: [Chapter 8: Operations, Observability, and Contribution Model](08-operations-observability-and-contribution-model.md)
