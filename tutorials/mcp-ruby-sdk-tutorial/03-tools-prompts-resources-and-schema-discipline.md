---
layout: default
title: "Chapter 3: Tools, Prompts, Resources, and Schema Discipline"
nav_order: 3
parent: MCP Ruby SDK Tutorial
---

# Chapter 3: Tools, Prompts, Resources, and Schema Discipline

This chapter focuses on modeling MCP primitives with predictable behavior and schema quality.

## Learning Goals

- design tool schemas that validate arguments and output shapes reliably
- structure prompt and resource handlers for maintainable growth
- use annotations and metadata consistently across primitives
- avoid schema drift that breaks client interoperability

## Primitive Implementation Checklist

1. define explicit tool argument schemas and output contracts
2. model prompt arguments with stable names and titles
3. expose resource identifiers and templates with clear naming patterns
4. test edge cases for empty, invalid, and over-broad input payloads

## Source References

- [Ruby SDK README - Tools](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#tools)
- [Ruby SDK README - Tool Output Schemas](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#tool-output-schemas)
- [Ruby SDK README - Prompts](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#prompts)
- [Ruby SDK README - Resources](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#resources)

## Summary

You now have a schema-first primitive strategy for Ruby MCP servers.

Next: [Chapter 4: Notifications, Logging, and Observability](04-notifications-logging-and-observability.md)
