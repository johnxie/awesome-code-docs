---
layout: default
title: "Chapter 5: Sampling, Elicitation, and Experimental Tasks"
nav_order: 5
parent: MCP TypeScript SDK Tutorial
---

# Chapter 5: Sampling, Elicitation, and Experimental Tasks

Advanced capabilities should be introduced intentionally, with clear user and security boundaries.

## Learning Goals

- add sampling for server-initiated model calls when appropriate
- choose form vs URL elicitation based on data sensitivity
- understand task-based execution lifecycle and experimental status
- avoid coupling experimental task APIs to critical production paths

## Capability Safety Guidance

- use form elicitation only for non-sensitive input
- use URL elicitation for sensitive/credential workflows
- treat experimental tasks API as opt-in with rollback plan

## Source References

- [Capabilities Docs](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/capabilities.md)
- [Elicitation Form Example](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/elicitationFormExample.ts)
- [Elicitation URL Example](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/elicitationUrlExample.ts)
- [Task + Sampling Example](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/toolWithSampleServer.ts)

## Summary

You now understand when and how to use advanced capability flows without overexposing risk.

Next: [Chapter 6: Middleware, Security, and Host Validation](06-middleware-security-and-host-validation.md)
