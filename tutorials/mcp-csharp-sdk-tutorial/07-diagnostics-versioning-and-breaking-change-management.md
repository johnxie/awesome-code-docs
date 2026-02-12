---
layout: default
title: "Chapter 7: Diagnostics, Versioning, and Breaking-Change Management"
nav_order: 7
parent: MCP C# SDK Tutorial
---

# Chapter 7: Diagnostics, Versioning, and Breaking-Change Management

Preview-stage SDKs need explicit guardrails for change management.

## Learning Goals

- use SDK diagnostics to catch misuse and compatibility risks early
- apply the repository's versioning policy in dependency planning
- separate protocol/schema shifts from SDK API changes
- reduce upgrade regressions with staged rollout patterns

## Risk-Control Strategy

- treat preview package updates as change events requiring regression testing
- track documented diagnostics and wire them into CI quality gates
- evaluate breaking changes against both API consumers and MCP behavior
- keep a compatibility note per service for protocol revision + SDK package versions

## Source References

- [Diagnostics List](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/list-of-diagnostics.md)
- [Versioning Policy](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/versioning.md)
- [Concepts Documentation Index](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/index.md)

## Summary

You now have a change-management model for keeping C# MCP deployments stable while the SDK evolves.

Next: [Chapter 8: Testing, Operations, and Contribution Workflows](08-testing-operations-and-contribution-workflows.md)
