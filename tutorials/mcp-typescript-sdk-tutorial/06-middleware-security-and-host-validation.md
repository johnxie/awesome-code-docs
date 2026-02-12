---
layout: default
title: "Chapter 6: Middleware, Security, and Host Validation"
nav_order: 6
parent: MCP TypeScript SDK Tutorial
---

# Chapter 6: Middleware, Security, and Host Validation

Most server risk in local and internal environments comes from weak host/binding controls, not tool code.

## Learning Goals

- apply framework adapter defaults that reduce exposure
- configure host header validation and allowed hostnames
- align localhost development and network-access behavior safely
- separate runtime adapter concerns from protocol concerns

## Security Checklist

| Control | Recommendation |
|:--------|:---------------|
| Local host binding | default to localhost/loopback |
| Host validation | explicit allowlist when externally bound |
| Adapter choice | match runtime, keep adapters thin |
| Legacy SSE | keep only for compatibility windows |

## Source References

- [Server Docs - DNS rebinding protection](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md)
- [Express Adapter README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/middleware/express/README.md)
- [Hono Adapter README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/middleware/hono/README.md)

## Summary

You now have concrete controls for hardening local and remote server exposure.

Next: [Chapter 7: v1 to v2 Migration Strategy](07-v1-to-v2-migration-strategy.md)
