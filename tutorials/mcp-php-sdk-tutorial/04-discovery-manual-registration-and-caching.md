---
layout: default
title: "Chapter 4: Discovery, Manual Registration, and Caching"
nav_order: 4
parent: MCP PHP SDK Tutorial
---

# Chapter 4: Discovery, Manual Registration, and Caching

This chapter compares registration strategies and startup optimization patterns.

## Learning Goals

- choose between attribute discovery and explicit registration
- apply hybrid registration models where needed
- use discovery caching to reduce startup overhead
- keep capability inventories deterministic across environments

## Strategy Matrix

| Strategy | Best Fit |
|:---------|:---------|
| discovery-only | fast onboarding and convention-driven projects |
| manual-only | strict control and explicit governance requirements |
| hybrid | mixed legacy/new codebases with phased migration |

## Caching Guidance

- use PSR-16 caching for discovery metadata in larger codebases.
- invalidate cache on deployment/version changes.
- monitor cache misses during cold starts to detect configuration regressions.

## Source References

- [Server Builder Guide - Discovery Configuration](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md#discovery-configuration)
- [PHP SDK README - Discovery Caching](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#discovery-caching)
- [Examples Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md)

## Summary

You now have a registration strategy framework that balances speed and control.

Next: [Chapter 5: Transports: STDIO and Streamable HTTP](05-transports-stdio-and-streamable-http.md)
