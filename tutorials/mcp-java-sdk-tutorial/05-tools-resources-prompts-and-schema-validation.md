---
layout: default
title: "Chapter 5: Tools, Resources, Prompts, and Schema Validation"
nav_order: 5
parent: MCP Java SDK Tutorial
---

# Chapter 5: Tools, Resources, Prompts, and Schema Validation

This chapter focuses on building clear server capabilities that clients can trust.

## Learning Goals

- design tool/resource/prompt surfaces with precise contracts
- enforce schema validation and tool naming discipline
- support mixed content responses where needed
- prevent capability sprawl inside a single server

## Capability Quality Checklist

- define strict JSON schemas for tool inputs and outputs
- validate tool names and avoid ambiguous naming patterns
- keep resource URI structure stable and meaningful
- expose only primitives that match the server's real domain boundary

## Source References

- [Server Feature Coverage (Conformance Server)](https://github.com/modelcontextprotocol/java-sdk/blob/main/conformance-tests/server-servlet/README.md)
- [Tool Name Validator](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/util/ToolNameValidator.java)
- [JSON Schema Validator Interface](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/spec/JsonSchemaValidator.java)

## Summary

You now have a quality model for Java MCP primitives that improves interoperability and operational clarity.

Next: [Chapter 6: Security, Authorization, and Runtime Controls](06-security-authorization-and-runtime-controls.md)
