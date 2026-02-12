---
layout: default
title: "Chapter 8: Conformance Testing and Contribution Workflows"
nav_order: 8
parent: MCP TypeScript SDK Tutorial
---

# Chapter 8: Conformance Testing and Contribution Workflows

Long-term reliability comes from conformance + integration testing, then disciplined contribution boundaries.

## Learning Goals

- run conformance suites for both client and server behaviors
- combine conformance checks with repo-specific integration tests
- align PR scope and issue-first workflow with maintainer expectations
- support v1.x maintenance while adopting v2 paths deliberately

## Operational Testing Loop

- run `test:conformance:client` and `test:conformance:server`
- run package-level integration tests for your specific transports
- keep migration changes small and reviewable
- document branch targeting (`main` vs `v1.x`) in team workflow docs

## Source References

- [Conformance README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/test/conformance/README.md)
- [Contributing Guide](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/CONTRIBUTING.md)
- [TypeScript SDK Releases](https://github.com/modelcontextprotocol/typescript-sdk/releases)

## Summary

You now have a production-aligned approach for maintaining and extending MCP TypeScript SDK usage over time.

Next: Continue with [MCP Use Tutorial](../mcp-use-tutorial/)
