---
layout: default
title: "Chapter 4: Sampling, Human-in-the-Loop, and Error Handling"
nav_order: 4
parent: MCP Swift SDK Tutorial
---

# Chapter 4: Sampling, Human-in-the-Loop, and Error Handling

Sampling is powerful and risky; this chapter focuses on safe control points.

## Learning Goals

- implement sampling handlers with explicit user-control steps
- reason about message flow between server, client, user, and LLM
- handle MCP and runtime errors with clear fallback behavior
- prevent silent failures in AI-assisted workflows

## Control Checklist

- review incoming sampling requests before forwarding to model providers
- inspect and optionally edit model output before sending response
- log sampling flow metadata for auditability
- standardize error surfaces for upstream callers

## Source References

- [Swift SDK README - Sampling](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#sampling)
- [Swift SDK README - Error Handling](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#error-handling)

## Summary

You now have a human-in-the-loop sampling pattern for safer Swift client operation.

Next: [Chapter 5: Server Setup, Hooks, and Primitive Authoring](05-server-setup-hooks-and-primitive-authoring.md)
