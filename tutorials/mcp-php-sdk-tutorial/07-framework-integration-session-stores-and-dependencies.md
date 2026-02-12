---
layout: default
title: "Chapter 7: Framework Integration, Session Stores, and Dependencies"
nav_order: 7
parent: MCP PHP SDK Tutorial
---

# Chapter 7: Framework Integration, Session Stores, and Dependencies

This chapter covers infrastructure decisions for production-grade PHP MCP services.

## Learning Goals

- choose session stores by scale and durability requirements
- wire SDK dependencies into framework containers and middleware
- apply framework-specific HTTP integration patterns safely
- avoid deployment failures from session or dependency misconfiguration

## Session Store Options

| Store | Best Fit |
|:------|:---------|
| in-memory | single-instance/local development |
| file-based | simple persistent session state |
| PSR-16 cache | distributed deployments (Redis/multi-node) |

## Integration Guidance

- centralize transport wiring at the framework edge.
- keep container bindings for handlers/services explicit.
- separate MCP protocol concerns from application domain services.

## Source References

- [PHP SDK README - Session Management](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#session-management)
- [Transports Guide - Framework Integration](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md#framework-integration)
- [Server Builder Guide - Service Dependencies](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md#service-dependencies)

## Summary

You now have a framework-aware infrastructure model for PHP MCP deployments.

Next: [Chapter 8: Roadmap, Release Strategy, and Production Readiness](08-roadmap-release-strategy-and-production-readiness.md)
