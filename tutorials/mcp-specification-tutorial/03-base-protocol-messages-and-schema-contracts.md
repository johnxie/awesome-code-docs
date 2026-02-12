---
layout: default
title: "Chapter 3: Base Protocol Messages and Schema Contracts"
nav_order: 3
parent: MCP Specification Tutorial
---

# Chapter 3: Base Protocol Messages and Schema Contracts

This chapter covers the core message and schema rules that keep implementations interoperable.

## Learning Goals

- distinguish requests, responses, and notifications correctly
- apply JSON-RPC and MCP field constraints with fewer wire bugs
- use JSON Schema dialect rules consistently
- handle `_meta` and rich metadata fields predictably

## Wire-Contract Rules That Matter

| Area | Practical Rule |
|:-----|:---------------|
| JSON encoding | UTF-8 encoded JSON-RPC messages only |
| Message framing | transport-specific framing must preserve one valid JSON-RPC message per unit |
| Requests vs notifications | requests expect response; notifications do not |
| Schema defaults | JSON Schema 2020-12 is the default dialect in current revisions |
| Validation | validate input and output schemas at boundaries, not deep inside tool logic |

## Implementation Guidance

- maintain strict schema validation for tool/resource payloads
- treat protocol errors separately from tool execution errors
- enforce method-level payload shape expectations in a shared layer
- pin schema artifacts by protocol revision when generating SDK bindings

## Source References

- [Base Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/index.mdx)
- [Schema Documentation](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/schema.mdx)
- [Protocol Changelog - Schema Updates](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)
- [Draft Schema Source](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/draft/schema.ts)

## Summary

You now have a protocol-contract baseline that reduces cross-client/server serialization and validation failures.

Next: [Chapter 4: Transport Model: stdio, Streamable HTTP, and Sessions](04-transport-model-stdio-streamable-http-and-sessions.md)
