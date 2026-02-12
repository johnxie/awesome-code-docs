---
layout: default
title: "Chapter 4: Tool, Resource, Prompt Design and Completions"
nav_order: 4
parent: MCP TypeScript SDK Tutorial
---

# Chapter 4: Tool, Resource, Prompt Design and Completions

Core server interface quality depends on well-structured tools, resources, and prompts.

## Learning Goals

- build tool handlers with explicit input and output schemas
- expose resources for stable read-oriented access patterns
- design prompt templates for repeatable human/model workflows
- use completions for better UX in prompt/resource argument entry

## Design Rules

| Surface | Rule of Thumb |
|:--------|:--------------|
| Tools | side effects allowed, schemas should be strict |
| Resources | read-focused, low side effects |
| Prompts | reusable templates, minimal ambiguity |
| Completions | assist selection without hiding underlying model |

## Source References

- [Server Docs - Tools, Resources, Prompts](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md)
- [Simple Streamable HTTP Example](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/simpleStreamableHttp.ts)

## Summary

You now have clearer interface design standards for MCP server surfaces.

Next: [Chapter 5: Sampling, Elicitation, and Experimental Tasks](05-sampling-elicitation-and-experimental-tasks.md)
