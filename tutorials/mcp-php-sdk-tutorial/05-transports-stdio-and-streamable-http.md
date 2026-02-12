---
layout: default
title: "Chapter 5: Transports: STDIO and Streamable HTTP"
nav_order: 5
parent: MCP PHP SDK Tutorial
---

# Chapter 5: Transports: STDIO and Streamable HTTP

This chapter maps transport choice to runtime and operational constraints.

## Learning Goals

- choose stdio vs streamable HTTP by workload
- understand HTTP method/session behavior requirements
- integrate streamable HTTP into framework middleware stacks
- validate transport behavior with Inspector and curl workflows

## Transport Matrix

| Transport | Best Fit |
|:----------|:---------|
| STDIO | local MCP clients, desktop integrations, subprocess servers |
| Streamable HTTP | web apps, framework routes, distributed services |

## Implementation Notes

- stdio is simplest for local testing and client config bootstrapping.
- HTTP transport requires PSR-17 factories and careful session/header handling.
- framework integrations (Symfony/Laravel/Slim) should wrap transport lifecycle cleanly.

## Source References

- [Transports Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md)
- [Server Examples README](https://github.com/modelcontextprotocol/php-sdk/blob/main/examples/server/README.md)
- [Examples Guide - Running Examples](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md#running-examples)

## Summary

You now have a transport selection model for PHP MCP deployment contexts.

Next: [Chapter 6: Client Communication: Sampling, Logging, and Progress](06-client-communication-sampling-logging-and-progress.md)
