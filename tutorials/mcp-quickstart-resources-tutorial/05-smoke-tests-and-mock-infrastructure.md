---
layout: default
title: "Chapter 5: Smoke Tests and Mock Infrastructure"
nav_order: 5
parent: MCP Quickstart Resources Tutorial
---

# Chapter 5: Smoke Tests and Mock Infrastructure

This chapter explains the lightweight test harness used to verify quickstart behavior.

## Learning Goals

- run smoke tests across supported language examples
- use mock client/server helpers for isolated protocol checks
- extend test coverage without external API dependencies
- integrate quickstart tests into CI workflows

## Test Infrastructure Components

| Helper | Role |
|:-------|:-----|
| `mcp-test-client.ts` | probes server readiness and tool listing |
| `mock-mcp-server.ts` | validates client-side protocol calls |
| `smoke-test.sh` | orchestrates cross-runtime checks |

## Source References

- [Smoke Tests Guide](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/tests/README.md)
- [CI Workflow](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/.github/workflows/ci.yml)

## Summary

You now have a repeatable validation loop for quickstart server/client quality.

Next: [Chapter 6: Cross-Language Consistency and Extension Strategy](06-cross-language-consistency-and-extension-strategy.md)
