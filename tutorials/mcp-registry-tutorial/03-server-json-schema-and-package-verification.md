---
layout: default
title: "Chapter 3: server.json Schema and Package Verification"
nav_order: 3
parent: MCP Registry Tutorial
---

# Chapter 3: server.json Schema and Package Verification

The `server.json` spec is the core contract between publishers, registries, and consumers.

## Learning Goals

- model required fields and extension metadata safely
- understand supported package types and registry constraints
- satisfy ownership verification rules for each package ecosystem
- avoid common validation failures before publish

## Verification Overview

| Package Type | Ownership Signal |
|:-------------|:-----------------|
| npm | `mcpName` in `package.json` |
| PyPI / NuGet | `mcp-name: <server-name>` marker in README |
| OCI | `io.modelcontextprotocol.server.name` image annotation |
| MCPB | artifact URL pattern + file SHA-256 metadata |

## High-Value Validation Habit

Run `mcp-publisher validate` locally before each publish attempt and treat warnings as pre-release review items.

## Source References

- [server.json Format Specification](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/generic-server-json.md)
- [Official Registry Requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
- [Supported Package Types](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/package-types.mdx)
- [Publisher Validate Command](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/cli/commands.md#mcp-publisher-validate)

## Summary

You can now design metadata that is far less likely to fail publication checks.

Next: [Chapter 4: Authentication Models and Namespace Ownership](04-authentication-models-and-namespace-ownership.md)
