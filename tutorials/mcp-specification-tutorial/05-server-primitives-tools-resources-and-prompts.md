---
layout: default
title: "Chapter 5: Server Primitives: Tools, Resources, and Prompts"
nav_order: 5
parent: MCP Specification Tutorial
---

# Chapter 5: Server Primitives: Tools, Resources, and Prompts

Server primitives define how useful and safe an MCP integration becomes in real clients.

## Learning Goals

- model tools, resources, and prompts with predictable semantics
- design list-changed/update flows that clients can consume reliably
- align content formats and error behavior with spec expectations
- avoid overloading a single server with unrelated responsibility domains

## Primitive Design Guidance

| Primitive | Primary Use | Common Pitfall |
|:----------|:------------|:---------------|
| Tools | side-effectful or compute actions | weak input schemas and ambiguous naming |
| Resources | retrievable context/data by URI | inconsistent URI schemes and stale update signaling |
| Prompts | reusable structured prompt templates | embedding server-private assumptions into prompt arguments |

## Quality Checklist

- keep tool names clear and format-compliant
- validate and normalize resource URIs
- provide accurate metadata for clients to render or reason over capabilities
- expose change notifications only when your server can maintain correct state

## Source References

- [Server Overview](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/index.mdx)
- [Tools](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx)
- [Resources](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/resources.mdx)
- [Prompts](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/prompts.mdx)
- [Completion Utility](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/utilities/completion.mdx)

## Summary

You now have a practical design framework for server primitives that is easier for hosts and clients to operate safely.

Next: [Chapter 6: Client Primitives: Roots, Sampling, Elicitation, and Tasks](06-client-primitives-roots-sampling-elicitation-and-tasks.md)
