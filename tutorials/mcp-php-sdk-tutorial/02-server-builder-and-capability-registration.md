---
layout: default
title: "Chapter 2: Server Builder and Capability Registration"
nav_order: 2
parent: MCP PHP SDK Tutorial
---

# Chapter 2: Server Builder and Capability Registration

This chapter explains how `Server::builder()` composes MCP runtime behavior.

## Learning Goals

- understand builder-driven server composition
- configure server info, instructions, pagination, and discovery
- register capabilities manually when discovery is not enough
- add dependency wiring (container/logger/event dispatcher) safely

## Builder Responsibilities

| Area | Typical Controls |
|:-----|:-----------------|
| Server metadata | name, version, instructions |
| Capability setup | discovery scan or explicit registration |
| Runtime dependencies | container, logger, event dispatcher |
| Session behavior | session store + TTL strategy |

## Design Guidance

- use the static builder method as the default setup path.
- keep explicit registration for business-critical handlers requiring strict ownership.
- keep capability declarations and actual handler availability aligned.

## Source References

- [Server Builder Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md)
- [PHP SDK README - Quick Start](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#quick-start)

## Summary

You now have a builder-centric model for composing PHP MCP servers.

Next: [Chapter 3: MCP Elements: Tools, Resources, Prompts, and Schemas](03-mcp-elements-tools-resources-prompts-and-schemas.md)
