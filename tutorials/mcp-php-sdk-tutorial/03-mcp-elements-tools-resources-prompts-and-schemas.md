---
layout: default
title: "Chapter 3: MCP Elements: Tools, Resources, Prompts, and Schemas"
nav_order: 3
parent: MCP PHP SDK Tutorial
---

# Chapter 3: MCP Elements: Tools, Resources, Prompts, and Schemas

This chapter covers primitive design and schema-quality controls in the PHP SDK.

## Learning Goals

- model tools/resources/prompts using PHP attributes or explicit registration
- control schema generation and validation depth
- return content in protocol-compliant formats
- avoid primitive drift that breaks client behavior

## Primitive Surface Overview

| Primitive | Attribute |
|:----------|:----------|
| Tool | `#[McpTool]` |
| Resource | `#[McpResource]` |
| Resource Template | `#[McpResourceTemplate]` |
| Prompt | `#[McpPrompt]` |

## Schema Discipline Checklist

1. prefer explicit parameter typing and docblocks for schema quality
2. use `#[Schema]` overrides for complex argument contracts
3. validate error/result content shapes before release
4. keep names/descriptions stable for client discoverability

## Source References

- [MCP Elements Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md)
- [PHP SDK README - Attribute Discovery](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#attribute-based-discovery)

## Summary

You now have a schema-first primitive strategy for PHP MCP servers.

Next: [Chapter 4: Discovery, Manual Registration, and Caching](04-discovery-manual-registration-and-caching.md)
