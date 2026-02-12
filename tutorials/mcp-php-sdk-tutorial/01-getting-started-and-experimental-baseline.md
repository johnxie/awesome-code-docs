---
layout: default
title: "Chapter 1: Getting Started and Experimental Baseline"
nav_order: 1
parent: MCP PHP SDK Tutorial
---

# Chapter 1: Getting Started and Experimental Baseline

This chapter sets a reproducible starting point for the evolving PHP SDK.

## Learning Goals

- install the SDK with a pinned dependency baseline
- align expectations for an experimental API surface
- run a minimal server-first workflow before advanced integrations
- reduce upgrade risk during early adoption

## Baseline Setup

```bash
composer require mcp/sdk
```

Start with a simple stdio server and validate end-to-end tool calls before adding frameworks or custom handlers.

## Adoption Guardrails

1. pin dependency versions in `composer.lock`
2. validate each upgrade against changelog and example behavior
3. treat API surfaces as potentially shifting until major stabilization
4. isolate your MCP integration behind thin adapters for easier refactor

## Source References

- [PHP SDK README - Installation](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#installation)
- [PHP SDK README - Roadmap](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#roadmap)
- [PHP SDK Changelog](https://github.com/modelcontextprotocol/php-sdk/blob/main/CHANGELOG.md)

## Summary

You now have a practical baseline for adopting the PHP SDK with controlled risk.

Next: [Chapter 2: Server Builder and Capability Registration](02-server-builder-and-capability-registration.md)
