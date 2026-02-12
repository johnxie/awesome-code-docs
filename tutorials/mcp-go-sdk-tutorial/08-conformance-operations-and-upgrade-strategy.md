---
layout: default
title: "Chapter 8: Conformance, Operations, and Upgrade Strategy"
nav_order: 8
parent: MCP Go SDK Tutorial
---

# Chapter 8: Conformance, Operations, and Upgrade Strategy

Conformance and release discipline keep Go MCP systems reliable across protocol evolution.

## Learning Goals

- run client and server conformance workflows continuously
- interpret baseline skips and failure classes pragmatically
- connect SDK upgrades to protocol revision planning
- maintain a stable release process for MCP services

## Conformance Loop

- run `scripts/server-conformance.sh` and `scripts/client-conformance.sh` in CI
- store result artifacts for trend analysis and regression triage
- review `conformance/baseline.yml` regularly to shrink accepted exceptions
- pair conformance with service-level integration tests

## Upgrade Strategy

1. track protocol revision deltas from the specification changelog
2. map SDK release notes to impacted capabilities in your services
3. stage transport/auth upgrades behind feature flags when possible
4. publish internal migration notes for all MCP-consuming teams

## Source References

- [Server Conformance Script](https://github.com/modelcontextprotocol/go-sdk/blob/main/scripts/server-conformance.sh)
- [Client Conformance Script](https://github.com/modelcontextprotocol/go-sdk/blob/main/scripts/client-conformance.sh)
- [Conformance Baseline](https://github.com/modelcontextprotocol/go-sdk/blob/main/conformance/baseline.yml)
- [Go SDK Releases](https://github.com/modelcontextprotocol/go-sdk/releases)
- [MCP Specification Changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)

## Summary

You now have an operations-ready model for validating and evolving Go SDK MCP deployments over time.

Next: Continue with [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)
