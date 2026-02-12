---
layout: default
title: "Chapter 7: v1 to v2 Migration Strategy"
nav_order: 7
parent: MCP TypeScript SDK Tutorial
---

# Chapter 7: v1 to v2 Migration Strategy

Migration success depends on sequencing: package split, imports, API updates, then behavior tests.

## Learning Goals

- map old monolithic package usage to v2 split packages
- plan Node/ESM/runtime prerequisites before refactoring
- update API usage (`registerTool`, method-string handlers, header model)
- manage mixed v1/v2 environments during migration windows

## Migration Order

1. align runtime and module format (Node 20+, ESM)
2. migrate dependencies/imports
3. update server/client API calls and schema shapes
4. run regression and conformance checks
5. roll out by service boundary, not by giant all-at-once PR

## Source References

- [Migration Guide](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/migration.md)
- [Migration Skill Guide](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/migration-SKILL.md)
- [FAQ - v1 branch guidance](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/faq.md)

## Summary

You now have a phased migration plan that reduces production breakage risk.

Next: [Chapter 8: Conformance Testing and Contribution Workflows](08-conformance-testing-and-contribution-workflows.md)
